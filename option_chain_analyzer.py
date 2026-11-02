#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
LearnOT - Nifty & BankNifty Option Chain Analyzer & Trapped-Seller Signal Engine
Built for OpenAlgo (http://127.0.0.1:5000) + Zerodha

Features:
1. Connects to OpenAlgo REST API / SDK at http://127.0.0.1:5000
2. Verifies OpenAlgo Analyze Mode (Simulator) before any order routing
3. Dynamically discovers nearest NFO Option Expiry (never hardcodes dates)
4. Fetches Option Chain with live quotes, OI, Volume, Bid/Ask & Greeks (Delta, Gamma, Theta, Vega, IV)
5. Logs snapshots to SQLite to compute 5m/15m Change in OI (dOI), Intraday dPCR, Session VWAP & Straddle Decay
6. Evaluates the 6-Point "Trapped Seller Gamma Blast" Option Buying Checklist
7. Enforces Anti-Theta (15-min Time Stop) and Anti-IV-Crush Guardrails
"""

import argparse
import csv
import datetime as dt
from email.message import EmailMessage
import json
import math
import os
import smtplib
import sqlite3
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Environment & Configuration Loader
# ---------------------------------------------------------------------------

def load_dotenv_file(env_path: Path) -> None:
    """Lightweight .env loader (no external dependency required)."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = val


BASE_DIR = Path(__file__).resolve().parent
load_dotenv_file(BASE_DIR / ".env")


# ---------------------------------------------------------------------------
# OpenAlgo API Client (Works with or without `openalgo` pip package)
# ---------------------------------------------------------------------------

class OpenAlgoGateway:
    """Unified gateway to local OpenAlgo instance at http://127.0.0.1:5000."""

    def __init__(self, host: str, api_key: str, timeout: int = 10):
        self.host = host.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.host}{endpoint}"
        body = {"apikey": self.api_key, **payload}
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            err_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAlgo HTTP {exc.code} on {endpoint}: {err_body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Cannot reach OpenAlgo at {self.host} ({exc.reason}). "
                "Ensure OpenAlgo is running on http://127.0.0.1:5000."
            ) from exc

    def analyzer_status(self) -> Dict[str, Any]:
        """Check whether OpenAlgo Analyze Mode (Simulator) is ON."""
        return self._post("/api/v1/analyzer", {})

    def find_nearest_expiry(self, underlying: str, exchange: str = "NFO") -> Tuple[str, int]:
        """Discover nearest active option expiry in DDMMMYY format and days to expiry."""
        resp = self._post(
            "/api/v1/expiry",
            {"symbol": underlying, "exchange": exchange, "instrumenttype": "options"},
        )
        if resp.get("status") != "success" or not resp.get("data"):
            raise RuntimeError(f"Failed to fetch expiry for {underlying}: {resp}")

        today = dt.datetime.now().date()
        valid_dates: List[dt.date] = []
        for raw_d in resp["data"]:
            for fmt in ("%d-%b-%y", "%d%b%y", "%Y-%m-%d", "%d-%b-%Y"):
                try:
                    parsed = dt.datetime.strptime(raw_d.upper(), fmt).date()
                    if parsed >= today:
                        valid_dates.append(parsed)
                    break
                except ValueError:
                    continue

        if not valid_dates:
            raise RuntimeError(f"No future expiry dates found for {underlying}: {resp['data'][:5]}")

        nearest = sorted(set(valid_dates))[0]
        compact = nearest.strftime("%d%b%y").upper()
        days_to_expiry = (nearest - today).days
        return compact, days_to_expiry

    def fetch_option_chain(
        self,
        underlying: str,
        expiry_date: str,
        exchange: str = "NSE_INDEX",
        strike_count: int = 5,
        with_greeks: bool = True,
    ) -> Dict[str, Any]:
        """Fetch live option chain with quotes and Greeks from OpenAlgo."""
        payload = {
            "underlying": underlying,
            "exchange": exchange,
            "expiry_date": expiry_date,
            "strike_count": strike_count,
            "with_greeks": with_greeks,
            "interest_rate": 6.5,
        }
        return self._post("/api/v1/optionchain", payload)

    def fetch_synthetic_future(
        self, underlying: str, expiry_date: str, exchange: str = "NSE_INDEX"
    ) -> Optional[Dict[str, Any]]:
        """Fetch synthetic future fair value via put-call parity."""
        try:
            resp = self._post(
                "/api/v1/syntheticfuture",
                {"underlying": underlying, "exchange": exchange, "expiry_date": expiry_date},
            )
            if resp.get("status") == "success":
                return resp
        except Exception:
            pass
        return None

    def place_options_order(
        self,
        underlying: str,
        expiry_date: str,
        offset: str,
        option_type: str,
        action: str,
        quantity: int,
        exchange: str = "NSE_INDEX",
        product: str = "NRML",
        pricetype: str = "MARKET",
        strategy: str = "LearnOT_GammaBlast",
    ) -> Dict[str, Any]:
        """Place an option order via OpenAlgo /api/v1/optionsorder."""
        return self._post(
            "/api/v1/optionsorder",
            {
                "strategy": strategy,
                "underlying": underlying,
                "exchange": exchange,
                "expiry_date": expiry_date,
                "offset": offset,
                "option_type": option_type,
                "action": action,
                "quantity": quantity,
                "pricetype": pricetype,
                "product": product,
                "splitsize": 0,
            },
        )


# ---------------------------------------------------------------------------
# SQLite Snapshot & Paper Trade Store
# ---------------------------------------------------------------------------

class SnapshotStore:
    """Persists intraday Option Chain snapshots, session VWAP, signals, and paper trades."""

    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS chain_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER NOT NULL,
                session_date TEXT NOT NULL,
                underlying TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                spot_ltp REAL NOT NULL,
                atm_strike REAL NOT NULL,
                synthetic_future REAL,
                basis REAL,
                atm_straddle_ltp REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS strike_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,
                ts INTEGER NOT NULL,
                session_date TEXT NOT NULL,
                underlying TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                strike REAL NOT NULL,
                option_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                label TEXT NOT NULL,
                ltp REAL NOT NULL,
                volume INTEGER NOT NULL,
                oi INTEGER NOT NULL,
                bid REAL,
                ask REAL,
                bid_qty INTEGER,
                ask_qty INTEGER,
                iv REAL,
                delta REAL,
                gamma REAL,
                theta REAL,
                vega REAL,
                lotsize INTEGER,
                FOREIGN KEY(snapshot_id) REFERENCES chain_snapshots(id)
            );

            CREATE INDEX IF NOT EXISTS idx_strike_lookup
            ON strike_snapshots(session_date, underlying, expiry_date, symbol, ts);

            CREATE TABLE IF NOT EXISTS signals_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER NOT NULL,
                session_date TEXT NOT NULL,
                underlying TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                strike REAL NOT NULL,
                option_type TEXT NOT NULL,
                entry_ltp REAL NOT NULL,
                stop_loss REAL NOT NULL,
                target_1 REAL NOT NULL,
                target_2 REAL NOT NULL,
                score INTEGER NOT NULL,
                rationale TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS paper_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_ts INTEGER NOT NULL,
                exit_ts INTEGER,
                session_date TEXT NOT NULL,
                underlying TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                symbol TEXT NOT NULL,
                offset_label TEXT NOT NULL,
                option_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                entry_price REAL NOT NULL,
                stop_loss REAL NOT NULL,
                target_1 REAL NOT NULL,
                target_2 REAL NOT NULL,
                exit_price REAL,
                pnl_points REAL,
                pnl_rupees REAL,
                status TEXT NOT NULL DEFAULT 'OPEN',
                exit_reason TEXT,
                openalgo_order_id TEXT
            );

            CREATE TABLE IF NOT EXISTS whatsapp_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER NOT NULL,
                session_date TEXT NOT NULL,
                underlying TEXT NOT NULL,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                provider TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT NOT NULL,
                response_detail TEXT
            );

            CREATE TABLE IF NOT EXISTS setup_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts INTEGER NOT NULL,
                session_date TEXT NOT NULL,
                time_str TEXT NOT NULL,
                underlying TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                option_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                strike REAL NOT NULL,
                score INTEGER NOT NULL,
                status_label TEXT NOT NULL,
                passed_rules TEXT NOT NULL,
                missing_rules TEXT NOT NULL,
                missing_rule_keys TEXT NOT NULL,
                entry_ltp REAL NOT NULL,
                latest_ltp REAL NOT NULL,
                max_ltp_after REAL NOT NULL,
                max_gain_pct REAL NOT NULL DEFAULT 0.0,
                latest_gain_pct REAL NOT NULL DEFAULT 0.0,
                verdict TEXT NOT NULL DEFAULT 'TRACKING',
                spot_ltp REAL NOT NULL,
                spot_vwap REAL NOT NULL,
                overall_pcr REAL NOT NULL,
                quadrant TEXT NOT NULL,
                doi_3m INTEGER NOT NULL,
                near_pe_doi_15m INTEGER NOT NULL,
                near_ce_doi_15m INTEGER NOT NULL,
                vol_burst_ratio REAL NOT NULL,
                iv REAL NOT NULL,
                delta REAL NOT NULL,
                theta_bleed_pct REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS daily_pre_market_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_date TEXT NOT NULL,
                underlying TEXT NOT NULL,
                pdh REAL NOT NULL DEFAULT 0.0,
                pdl REAL NOT NULL DEFAULT 0.0,
                pdc REAL NOT NULL DEFAULT 0.0,
                pre_open_spot REAL NOT NULL DEFAULT 0.0,
                gift_nifty_gap REAL NOT NULL DEFAULT 0.0,
                global_sentiment TEXT NOT NULL DEFAULT 'NEUTRAL_MIXED',
                asian_markets TEXT NOT NULL DEFAULT 'POSITIVE_MOMENTUM',
                prev_day_pcr REAL NOT NULL DEFAULT 1.0,
                fii_flow TEXT NOT NULL DEFAULT 'NEUTRAL_MIXED',
                brent_crude TEXT NOT NULL DEFAULT 'STABLE_NEUTRAL',
                dxy_usdinr TEXT NOT NULL DEFAULT 'STABLE_NEUTRAL',
                preopen_adv_dec TEXT NOT NULL DEFAULT 'MODERATE_ADVANCES',
                event_context TEXT NOT NULL DEFAULT 'NORMAL_DAY',
                gap_pts REAL NOT NULL DEFAULT 0.0,
                gap_regime TEXT NOT NULL DEFAULT 'FLAT',
                india_vix REAL NOT NULL DEFAULT 14.5,
                vix_regime TEXT NOT NULL DEFAULT 'IDEAL_VOL (14-16)',
                expected_open_type TEXT NOT NULL DEFAULT '',
                option_buying_env TEXT NOT NULL DEFAULT '',
                system_premarket_signal TEXT NOT NULL DEFAULT '',
                system_premarket_reasons TEXT NOT NULL DEFAULT '',
                call_wall_strike REAL NOT NULL DEFAULT 0.0,
                put_wall_strike REAL NOT NULL DEFAULT 0.0,
                planned_bias TEXT NOT NULL DEFAULT 'TWO_WAY',
                bull_trigger REAL NOT NULL DEFAULT 0.0,
                bear_trigger REAL NOT NULL DEFAULT 0.0,
                max_trades INTEGER NOT NULL DEFAULT 3,
                pre_plan_notes TEXT NOT NULL DEFAULT '',
                post_market_notes TEXT NOT NULL DEFAULT '',
                actual_open REAL NOT NULL DEFAULT 0.0,
                actual_high REAL NOT NULL DEFAULT 0.0,
                actual_low REAL NOT NULL DEFAULT 0.0,
                actual_close REAL NOT NULL DEFAULT 0.0,
                actual_trades_count INTEGER NOT NULL DEFAULT 0,
                actual_pnl_rupees REAL NOT NULL DEFAULT 0.0,
                plan_match_status TEXT NOT NULL DEFAULT 'WAITING_FOR_DATA',
                market_vs_plan_detail TEXT NOT NULL DEFAULT '',
                trade_vs_plan_detail TEXT NOT NULL DEFAULT '',
                alignment_score INTEGER NOT NULL DEFAULT 100,
                updated_ts INTEGER NOT NULL DEFAULT 0,
                UNIQUE(session_date, underlying)
            );
            """
        )
        # Ensure existing databases get new Pre-Market Sentiment columns seamlessly
        new_cols = [
            ("gift_nifty_gap", "REAL NOT NULL DEFAULT 0.0"),
            ("global_sentiment", "TEXT NOT NULL DEFAULT 'NEUTRAL_MIXED'"),
            ("asian_markets", "TEXT NOT NULL DEFAULT 'POSITIVE_MOMENTUM'"),
            ("prev_day_pcr", "REAL NOT NULL DEFAULT 1.0"),
            ("fii_flow", "TEXT NOT NULL DEFAULT 'NEUTRAL_MIXED'"),
            ("brent_crude", "TEXT NOT NULL DEFAULT 'STABLE_NEUTRAL'"),
            ("dxy_usdinr", "TEXT NOT NULL DEFAULT 'STABLE_NEUTRAL'"),
            ("preopen_adv_dec", "TEXT NOT NULL DEFAULT 'MODERATE_ADVANCES'"),
            ("event_context", "TEXT NOT NULL DEFAULT 'NORMAL_DAY'"),
            ("expected_open_type", "TEXT NOT NULL DEFAULT ''"),
            ("option_buying_env", "TEXT NOT NULL DEFAULT ''"),
            ("system_premarket_signal", "TEXT NOT NULL DEFAULT ''"),
            ("system_premarket_reasons", "TEXT NOT NULL DEFAULT ''"),
        ]
        for col_name, col_def in new_cols:
            try:
                cur.execute(f"ALTER TABLE daily_pre_market_plans ADD COLUMN {col_name} {col_def}")
            except sqlite3.OperationalError:
                pass
        self.conn.commit()

    def save_snapshot(
        self,
        ts: int,
        underlying: str,
        expiry_date: str,
        spot_ltp: float,
        atm_strike: float,
        synthetic_future: Optional[float],
        basis: Optional[float],
        atm_straddle_ltp: float,
        chain_rows: List[Dict[str, Any]],
    ) -> int:
        session_date = dt.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO chain_snapshots
            (ts, session_date, underlying, expiry_date, spot_ltp, atm_strike, synthetic_future, basis, atm_straddle_ltp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ts,
                session_date,
                underlying,
                expiry_date,
                spot_ltp,
                atm_strike,
                synthetic_future,
                basis,
                atm_straddle_ltp,
            ),
        )
        snapshot_id = cur.lastrowid

        for row in chain_rows:
            strike = float(row["strike"])
            for opt_type in ("ce", "pe"):
                leg = row.get(opt_type)
                if not leg:
                    continue
                cur.execute(
                    """
                    INSERT INTO strike_snapshots
                    (snapshot_id, ts, session_date, underlying, expiry_date, strike, option_type,
                     symbol, label, ltp, volume, oi, bid, ask, bid_qty, ask_qty,
                     iv, delta, gamma, theta, vega, lotsize)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        snapshot_id,
                        ts,
                        session_date,
                        underlying,
                        expiry_date,
                        strike,
                        opt_type.upper(),
                        leg.get("symbol", ""),
                        leg.get("label", ""),
                        float(leg.get("ltp") or 0.0),
                        int(leg.get("volume") or 0),
                        int(leg.get("oi") or 0),
                        float(leg.get("bid") or 0.0),
                        float(leg.get("ask") or 0.0),
                        int(leg.get("bid_qty") or 0),
                        int(leg.get("ask_qty") or 0),
                        float(leg["implied_volatility"]) if leg.get("implied_volatility") is not None else None,
                        float(leg["delta"]) if leg.get("delta") is not None else None,
                        float(leg["gamma"]) if leg.get("gamma") is not None else None,
                        float(leg["theta"]) if leg.get("theta") is not None else None,
                        float(leg["vega"]) if leg.get("vega") is not None else None,
                        int(leg.get("lotsize") or 0),
                    ),
                )
        self.conn.commit()
        return int(snapshot_id)

    def get_historical_leg_metrics(
        self, session_date: str, underlying: str, expiry_date: str, symbol: str, now_ts: int
    ) -> Dict[str, Any]:
        """
        Compute Session VWAP, 3m (1 NSE OI cycle) & 15m (5 NSE OI cycles) dOI,
        dLTP, dIV, and volume burst for a specific option symbol.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT ts, ltp, volume, oi, iv
            FROM strike_snapshots
            WHERE session_date = ? AND underlying = ? AND expiry_date = ? AND symbol = ?
            ORDER BY ts ASC
            """,
            (session_date, underlying, expiry_date, symbol),
        )
        rows = cur.fetchall()
        if not rows:
            return {
                "vwap": 0.0,
                "doi_3m": 0,
                "doi_5m": 0,
                "doi_15m": 0,
                "dltp_3m": 0.0,
                "dltp_5m": 0.0,
                "div_3m": 0.0,
                "div_5m": 0.0,
                "vol_burst_ratio": 1.0,
                "samples": 0,
            }

        # Compute cumulative intraday VWAP weighted by incremental volume (or average if volume static)
        cum_pv = 0.0
        cum_vol = 0
        prev_vol = None
        vol_deltas: List[int] = []
        for r in rows:
            ltp = float(r["ltp"])
            vol = int(r["volume"])
            delta_v = vol - prev_vol if (prev_vol is not None and vol >= prev_vol) else max(vol, 1)
            if prev_vol is not None:
                vol_deltas.append(max(vol - prev_vol, 0))
            prev_vol = vol
            cum_pv += ltp * max(delta_v, 1)
            cum_vol += max(delta_v, 1)

        vwap = cum_pv / cum_vol if cum_vol > 0 else float(rows[-1]["ltp"])

        latest = rows[-1]
        # Find snapshot closest to 3 minutes ago (180s - 1 NSE OI refresh cycle) and 15 minutes ago (900s - 5 cycles)
        ref_3m = rows[-2] if len(rows) >= 2 else rows[0]
        ref_15m = rows[0]
        for r in reversed(rows[:-1]):
            if now_ts - int(r["ts"]) >= 150:
                ref_3m = r
                break
        for r in reversed(rows[:-1]):
            if now_ts - int(r["ts"]) >= 780:
                ref_15m = r
                break

        doi_3m = int(latest["oi"]) - int(ref_3m["oi"])
        doi_15m = int(latest["oi"]) - int(ref_15m["oi"])
        dltp_3m = float(latest["ltp"]) - float(ref_3m["ltp"])

        div_3m = 0.0
        if latest["iv"] is not None and ref_3m["iv"] is not None:
            div_3m = float(latest["iv"]) - float(ref_3m["iv"])

        vol_burst_ratio = 1.0
        if len(vol_deltas) >= 2:
            recent_v = vol_deltas[-1]
            avg_v = sum(vol_deltas[:-1]) / max(len(vol_deltas) - 1, 1)
            if avg_v > 0:
                vol_burst_ratio = recent_v / avg_v

        return {
            "vwap": round(vwap, 2),
            "doi_3m": doi_3m,
            "doi_5m": doi_3m,
            "doi_15m": doi_15m,
            "dltp_3m": round(dltp_3m, 2),
            "dltp_5m": round(dltp_3m, 2),
            "div_3m": round(div_3m, 2),
            "div_5m": round(div_3m, 2),
            "vol_burst_ratio": round(vol_burst_ratio, 2),
            "samples": len(rows),
        }

    def get_session_chain_context(
        self, session_date: str, underlying: str, expiry_date: str
    ) -> Dict[str, Any]:
        """Compute Spot Session Proxy VWAP and Opening Straddle Premium."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT spot_ltp, atm_straddle_ltp
            FROM chain_snapshots
            WHERE session_date = ? AND underlying = ? AND expiry_date = ?
            ORDER BY ts ASC
            """,
            (session_date, underlying, expiry_date),
        )
        rows = cur.fetchall()
        if not rows:
            return {"spot_vwap": 0.0, "opening_straddle": 0.0, "snapshots_count": 0}
        spot_vwap = sum(float(r["spot_ltp"]) for r in rows) / len(rows)
        opening_straddle = float(rows[0]["atm_straddle_ltp"])
        return {
            "spot_vwap": round(spot_vwap, 2),
            "opening_straddle": round(opening_straddle, 2),
            "snapshots_count": len(rows),
        }


# ---------------------------------------------------------------------------
# Quantitative Option Chain & Signal Engine
# ---------------------------------------------------------------------------

def classify_quadrant(dltp: float, doi: int) -> str:
    """Classify 4-Quadrant Price + OI action."""
    if doi == 0 and abs(dltp) < 0.05:
        return "NEUTRAL"
    if dltp > 0 and doi > 0:
        return "LONG_BUILDUP"
    if dltp < 0 and doi > 0:
        return "SHORT_BUILDUP"
    if dltp > 0 and doi < 0:
        return "SHORT_COVERING"
    if dltp < 0 and doi < 0:
        return "LONG_UNWINDING"
    return "NEUTRAL"


def estimate_greeks_fallback(
    spot: float, strike: float, ltp: float, option_type: str, days_to_expiry: int
) -> Dict[str, float]:
    """Lightweight approximation if broker adapter returns greeks_included=False."""
    t_days = max(days_to_expiry, 0.5)
    moneyness = (spot - strike) / max(spot, 1.0)
    if option_type.upper() == "CE":
        delta = max(0.05, min(0.95, 0.52 + moneyness * 18.0))
    else:
        delta = -max(0.05, min(0.95, 0.52 - moneyness * 18.0))
    iv = max(8.0, min(45.0, (ltp / max(spot, 1.0)) * math.sqrt(365.0 / t_days) * 250.0))
    theta = -round((ltp * 0.45) / t_days, 2)
    gamma = round(0.0012 * (1.0 - abs(abs(delta) - 0.5)), 5)
    vega = round(spot * 0.0005 * math.sqrt(t_days / 365.0) * 100, 2)
    return {
        "implied_volatility": round(iv, 2),
        "delta": round(delta, 3),
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
    }


def analyze_option_chain(
    store: SnapshotStore,
    underlying: str,
    expiry_date: str,
    days_to_expiry: int,
    chain_resp: Dict[str, Any],
    synth_resp: Optional[Dict[str, Any]],
    now_ts: Optional[int] = None,
) -> Dict[str, Any]:
    """Run full 4-Pillar Option Chain analysis & evaluate the 6-Point Gamma Blast Checklist."""
    ts = now_ts or int(time.time())
    session_date = dt.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    spot_ltp = float(chain_resp.get("underlying_ltp") or 0.0)
    atm_strike = float(chain_resp.get("atm_strike") or 0.0)
    chain_rows = chain_resp.get("chain") or []

    synthetic_future = None
    basis = 0.0
    if synth_resp and synth_resp.get("synthetic_future_price"):
        synthetic_future = float(synth_resp["synthetic_future_price"])
        basis = round(synthetic_future - spot_ltp, 2)

    # Find ATM CE & PE to compute ATM Straddle combined premium
    atm_ce_ltp = 0.0
    atm_pe_ltp = 0.0
    for r in chain_rows:
        if abs(float(r["strike"]) - atm_strike) < 0.01:
            atm_ce_ltp = float((r.get("ce") or {}).get("ltp") or 0.0)
            atm_pe_ltp = float((r.get("pe") or {}).get("ltp") or 0.0)
            break
    atm_straddle_ltp = round(atm_ce_ltp + atm_pe_ltp, 2)

    # Ensure Greeks are populated (use OpenAlgo Greeks if included, else fallback estimator)
    for r in chain_rows:
        strike = float(r["strike"])
        for opt_key in ("ce", "pe"):
            leg = r.get(opt_key)
            if not leg:
                continue
            if leg.get("delta") is None:
                est = estimate_greeks_fallback(
                    spot_ltp, strike, float(leg.get("ltp") or 0.0), opt_key.upper(), days_to_expiry
                )
                leg.update(est)

    # Save current snapshot to SQLite
    store.save_snapshot(
        ts=ts,
        underlying=underlying,
        expiry_date=expiry_date,
        spot_ltp=spot_ltp,
        atm_strike=atm_strike,
        synthetic_future=synthetic_future,
        basis=basis,
        atm_straddle_ltp=atm_straddle_ltp,
        chain_rows=chain_rows,
    )

    session_ctx = store.get_session_chain_context(session_date, underlying, expiry_date)
    spot_vwap = session_ctx["spot_vwap"]
    opening_straddle = session_ctx["opening_straddle"]
    straddle_change_pct = (
        round(((atm_straddle_ltp - opening_straddle) / opening_straddle) * 100.0, 2)
        if opening_straddle > 0
        else 0.0
    )

    # Enrich every strike with historical dOI, VWAP, Quadrant & aggregate metrics
    enriched_strikes: List[Dict[str, Any]] = []
    total_ce_oi = 0
    total_pe_oi = 0
    near_ce_doi_15m = 0
    near_pe_doi_15m = 0
    max_ce_oi = (-1, 0.0)
    max_pe_oi = (-1, 0.0)

    atm_row_enriched: Optional[Dict[str, Any]] = None

    for r in chain_rows:
        strike = float(r["strike"])
        ce = dict(r.get("ce") or {})
        pe = dict(r.get("pe") or {})

        ce_hist = store.get_historical_leg_metrics(
            session_date, underlying, expiry_date, ce.get("symbol", ""), ts
        )
        pe_hist = store.get_historical_leg_metrics(
            session_date, underlying, expiry_date, pe.get("symbol", ""), ts
        )

        ce["vwap"] = ce_hist["vwap"]
        ce["doi_3m"] = ce_hist["doi_3m"]
        ce["doi_5m"] = ce_hist["doi_5m"]
        ce["doi_15m"] = ce_hist["doi_15m"]
        ce["dltp_3m"] = ce_hist["dltp_3m"]
        ce["dltp_5m"] = ce_hist["dltp_5m"]
        ce["div_3m"] = ce_hist["div_3m"]
        ce["div_5m"] = ce_hist["div_5m"]
        ce["vol_burst_ratio"] = ce_hist["vol_burst_ratio"]
        ce["quadrant"] = classify_quadrant(ce["dltp_3m"], ce["doi_3m"])

        pe["vwap"] = pe_hist["vwap"]
        pe["doi_3m"] = pe_hist["doi_3m"]
        pe["doi_5m"] = pe_hist["doi_5m"]
        pe["doi_15m"] = pe_hist["doi_15m"]
        pe["dltp_3m"] = pe_hist["dltp_3m"]
        pe["dltp_5m"] = pe_hist["dltp_5m"]
        pe["div_3m"] = pe_hist["div_3m"]
        pe["div_5m"] = pe_hist["div_5m"]
        pe["vol_burst_ratio"] = pe_hist["vol_burst_ratio"]
        pe["quadrant"] = classify_quadrant(pe["dltp_3m"], pe["doi_3m"])

        ce_oi = int(ce.get("oi") or 0)
        pe_oi = int(pe.get("oi") or 0)
        total_ce_oi += ce_oi
        total_pe_oi += pe_oi

        if ce_oi > max_ce_oi[0]:
            max_ce_oi = (ce_oi, strike)
        if pe_oi > max_pe_oi[0]:
            max_pe_oi = (pe_oi, strike)

        # Near-ATM (+/- 3 strikes) aggregate dOI
        label = str(ce.get("label") or "")
        if label in ("ATM", "ITM1", "ITM2", "ITM3", "OTM1", "OTM2", "OTM3"):
            near_ce_doi_15m += ce["doi_15m"]
            near_pe_doi_15m += pe["doi_15m"]

        row_item = {"strike": strike, "ce": ce, "pe": pe}
        if abs(strike - atm_strike) < 0.01:
            atm_row_enriched = row_item
        enriched_strikes.append(row_item)

    overall_pcr = round(total_pe_oi / max(total_ce_oi, 1), 2) if total_ce_oi > 0 else 1.0

    # Evaluate the 6-Point Checklist for ATM CE and ATM PE
    signals = evaluate_checklist(
        underlying=underlying,
        spot_ltp=spot_ltp,
        spot_vwap=spot_vwap,
        basis=basis,
        overall_pcr=overall_pcr,
        near_ce_doi_15m=near_ce_doi_15m,
        near_pe_doi_15m=near_pe_doi_15m,
        straddle_change_pct=straddle_change_pct,
        atm_row=atm_row_enriched,
        days_to_expiry=days_to_expiry,
    )

    report = {
        "ts": ts,
        "session_date": session_date,
        "underlying": underlying,
        "expiry_date": expiry_date,
        "days_to_expiry": days_to_expiry,
        "spot_ltp": spot_ltp,
        "spot_vwap": spot_vwap,
        "atm_strike": atm_strike,
        "synthetic_future": synthetic_future,
        "basis": basis,
        "atm_straddle_ltp": atm_straddle_ltp,
        "opening_straddle": opening_straddle,
        "straddle_change_pct": straddle_change_pct,
        "overall_pcr": overall_pcr,
        "near_ce_doi_15m": near_ce_doi_15m,
        "near_pe_doi_15m": near_pe_doi_15m,
        "resistance_strike": max_ce_oi[1],
        "resistance_oi": max_ce_oi[0],
        "support_strike": max_pe_oi[1],
        "support_oi": max_pe_oi[0],
        "snapshots_count": session_ctx["snapshots_count"],
        "strikes": enriched_strikes,
        "signals": signals,
    }
    report["journal"] = update_and_write_setup_journal(store, report, min_score=3)
    return report


def evaluate_checklist(
    underlying: str,
    spot_ltp: float,
    spot_vwap: float,
    basis: float,
    overall_pcr: float,
    near_ce_doi_15m: int,
    near_pe_doi_15m: int,
    straddle_change_pct: float,
    atm_row: Optional[Dict[str, Any]],
    days_to_expiry: int,
) -> Dict[str, Any]:
    """Evaluate 6-Point Trapped Writer Checklist for Bullish (CE) and Bearish (PE) setups."""
    if not atm_row:
        return {"action": "WAIT", "reason": "ATM row unavailable", "ce_checks": [], "pe_checks": []}

    ce = atm_row["ce"]
    pe = atm_row["pe"]

    # Check if market is in a Theta Trap (Straddle decaying + both CE & PE OI building up)
    theta_trap = (
        straddle_change_pct < -2.5
        and near_ce_doi_15m > 0
        and near_pe_doi_15m > 0
        and 0.88 <= overall_pcr <= 1.12
    )

    # --- BULLISH (BUY ATM CE) 6-POINT CHECKLIST ---
    ce_ltp = float(ce.get("ltp") or 0.0)
    ce_vwap = float(ce.get("vwap") or ce_ltp)
    ce_delta = abs(float(ce.get("delta") or 0.5))
    ce_theta = abs(float(ce.get("theta") or 0.0))
    ce_theta_ratio = (ce_theta / max(ce_ltp, 1.0)) * 100.0
    max_theta_pct = 30.0 if days_to_expiry <= 1 else 18.0

    ce_checks = [
        (
            "1. Spot >= Spot VWAP & Basis Stable",
            spot_ltp >= spot_vwap and basis >= -15.0,
            f"Spot {spot_ltp:.1f} vs VWAP {spot_vwap:.1f} (Basis {basis:+.1f})",
        ),
        (
            "2. CE LTP > Option Session VWAP",
            ce_ltp > ce_vwap and ce.get("dltp_3m", 0.0) > 0,
            f"CE LTP {ce_ltp:.2f} vs VWAP {ce_vwap:.2f} (3m dLTP {ce.get('dltp_3m', 0):+.2f})",
        ),
        (
            "3. Trapped Call Writers / Put Writing Support",
            (near_pe_doi_15m > near_ce_doi_15m and near_pe_doi_15m > 0)
            or ce.get("quadrant") == "SHORT_COVERING"
            or overall_pcr >= 1.15,
            f"15m PE dOI {near_pe_doi_15m:+,} vs CE dOI {near_ce_doi_15m:+,} | CE: {ce.get('quadrant')} | PCR {overall_pcr:.2f}",
        ),
        (
            "4. Volume Burst & Order Flow",
            ce.get("vol_burst_ratio", 1.0) >= 1.2
            and int(ce.get("bid_qty") or 1) >= 0.7 * int(ce.get("ask_qty") or 1),
            f"Vol Ratio {ce.get('vol_burst_ratio', 1.0):.2f}x | BidQty {ce.get('bid_qty', 0)} vs AskQty {ce.get('ask_qty', 0)}",
        ),
        (
            "5. Anti-IV-Crush Guardrail (IV Stable/Rising)",
            float(ce.get("div_3m") or 0.0) >= -0.30,
            f"CE IV {ce.get('implied_volatility', 0):.2f}% (3m dIV {ce.get('div_3m', 0):+.2f}%)",
        ),
        (
            "6. Greeks Filter (Delta 0.45-0.70 & Low Theta Bleed)",
            0.45 <= ce_delta <= 0.70 and ce_theta_ratio <= max_theta_pct,
            f"Delta {ce_delta:.2f} | Daily Theta Bleed {ce_theta_ratio:.1f}% (Max {max_theta_pct:.0f}%)",
        ),
    ]

    # --- BEARISH (BUY ATM PE) 6-POINT CHECKLIST ---
    pe_ltp = float(pe.get("ltp") or 0.0)
    pe_vwap = float(pe.get("vwap") or pe_ltp)
    pe_delta = abs(float(pe.get("delta") or 0.5))
    pe_theta = abs(float(pe.get("theta") or 0.0))
    pe_theta_ratio = (pe_theta / max(pe_ltp, 1.0)) * 100.0

    pe_checks = [
        (
            "1. Spot <= Spot VWAP & Basis Weak",
            spot_ltp <= spot_vwap and basis <= 15.0,
            f"Spot {spot_ltp:.1f} vs VWAP {spot_vwap:.1f} (Basis {basis:+.1f})",
        ),
        (
            "2. PE LTP > Option Session VWAP",
            pe_ltp > pe_vwap and pe.get("dltp_3m", 0.0) > 0,
            f"PE LTP {pe_ltp:.2f} vs VWAP {pe_vwap:.2f} (3m dLTP {pe.get('dltp_3m', 0):+.2f})",
        ),
        (
            "3. Trapped Put Writers / Call Writing Resistance",
            (near_ce_doi_15m > near_pe_doi_15m and near_ce_doi_15m > 0)
            or pe.get("quadrant") == "SHORT_COVERING"
            or overall_pcr <= 0.85,
            f"15m CE dOI {near_ce_doi_15m:+,} vs PE dOI {near_pe_doi_15m:+,} | PE: {pe.get('quadrant')} | PCR {overall_pcr:.2f}",
        ),
        (
            "4. Volume Burst & Order Flow",
            pe.get("vol_burst_ratio", 1.0) >= 1.2
            and int(pe.get("bid_qty") or 1) >= 0.7 * int(pe.get("ask_qty") or 1),
            f"Vol Ratio {pe.get('vol_burst_ratio', 1.0):.2f}x | BidQty {pe.get('bid_qty', 0)} vs AskQty {pe.get('ask_qty', 0)}",
        ),
        (
            "5. Anti-IV-Crush Guardrail (IV Stable/Rising)",
            float(pe.get("div_3m") or 0.0) >= -0.30,
            f"PE IV {pe.get('implied_volatility', 0):.2f}% (3m dIV {pe.get('div_3m', 0):+.2f}%)",
        ),
        (
            "6. Greeks Filter (|Delta| 0.45-0.70 & Low Theta Bleed)",
            0.45 <= pe_delta <= 0.70 and pe_theta_ratio <= max_theta_pct,
            f"|Delta| {pe_delta:.2f} | Daily Theta Bleed {pe_theta_ratio:.1f}% (Max {max_theta_pct:.0f}%)",
        ),
    ]

    ce_score = sum(1 for _, passed, _ in ce_checks if passed)
    pe_score = sum(1 for _, passed, _ in pe_checks if passed)

    sl_pct = 0.15 if days_to_expiry <= 1 else 0.18
    action = "WAIT"
    trade_plan = None

    if theta_trap:
        action = "THETA_TRAP_NO_TRADE"
    elif ce_score == 6:
        action = "BUY_ATM_CE"
        trade_plan = {
            "option_type": "CE",
            "offset": "ATM",
            "symbol": ce.get("symbol", ""),
            "strike": atm_row["strike"],
            "lotsize": int(ce.get("lotsize") or 65),
            "entry_ltp": ce_ltp,
            "stop_loss": round(ce_ltp * (1.0 - sl_pct), 2),
            "target_1": round(ce_ltp * 1.25, 2),
            "target_2": round(ce_ltp * 1.45, 2),
            "time_stop_mins": 15,
            "score": ce_score,
        }
    elif pe_score == 6:
        action = "BUY_ATM_PE"
        trade_plan = {
            "option_type": "PE",
            "offset": "ATM",
            "symbol": pe.get("symbol", ""),
            "strike": atm_row["strike"],
            "lotsize": int(pe.get("lotsize") or 65),
            "entry_ltp": pe_ltp,
            "stop_loss": round(pe_ltp * (1.0 - sl_pct), 2),
            "target_1": round(pe.get("ltp", 0.0) * 1.25, 2),
            "target_2": round(pe.get("ltp", 0.0) * 1.45, 2),
            "time_stop_mins": 15,
            "score": pe_score,
        }

    return {
        "action": action,
        "theta_trap": theta_trap,
        "ce_score": ce_score,
        "pe_score": pe_score,
        "ce_checks": ce_checks,
        "pe_checks": pe_checks,
        "trade_plan": trade_plan,
    }


# ---------------------------------------------------------------------------
# Setup & Fine-Tuning Journal Engine (Logs Setups with >= 3/6 Conditions Met)
# ---------------------------------------------------------------------------

RULE_SHORT_NAMES: Dict[int, str] = {
    1: "R1: Spot/Basis Trend",
    2: "R2: Option > VWAP",
    3: "R3: Trapped Writers / PCR / dOI",
    4: "R4: Volume Burst",
    5: "R5: IV Stability",
    6: "R6: Greeks & Theta",
}


def update_and_write_setup_journal(
    store: SnapshotStore,
    report: Dict[str, Any],
    min_score: int = 3,
) -> Dict[str, Any]:
    """
    1. Updates forward LTP / Max Gain % outcomes for all prior journal entries today.
    2. Records any setup where score >= min_score (default: 3 out of 6) along with
       exact PASSED rules, MISSING rules (with live metric values), and option chain context.
    3. Computes a Rule-Blocker Leaderboard showing which missing rule blocked the most
       winning moves so the trader can fine-tune thresholds.
    4. Writes human-readable Markdown (journal/setup_journal_<date>.md + journal/LATEST_JOURNAL.md)
       and CSV (journal/setup_journal.csv).
    """
    cur = store.conn.cursor()
    session_date = report["session_date"]
    underlying = report["underlying"]
    expiry_date = report["expiry_date"]
    now_ts = int(report["ts"])
    time_str = dt.datetime.fromtimestamp(now_ts).strftime("%H:%M:%S")

    # Build symbol -> current LTP map from current chain
    ltp_map: Dict[str, float] = {}
    atm_row: Optional[Dict[str, Any]] = None
    for row in report.get("strikes", []):
        if abs(float(row["strike"]) - float(report["atm_strike"])) < 0.01:
            atm_row = row
        for side_key in ("ce", "pe"):
            leg = row.get(side_key) or {}
            sym = leg.get("symbol")
            if sym:
                ltp_map[sym] = float(leg.get("ltp") or 0.0)

    # Step 1: Update forward outcomes of earlier journal entries from today
    cur.execute(
        """
        SELECT id, symbol, score, entry_ltp, max_ltp_after
        FROM setup_journal
        WHERE session_date = ? AND underlying = ?
        """,
        (session_date, underlying),
    )
    prior_rows = cur.fetchall()
    for pr in prior_rows:
        sym = pr["symbol"]
        if sym not in ltp_map:
            continue
        cur_ltp = ltp_map[sym]
        entry_ltp = float(pr["entry_ltp"] or 1.0)
        new_max = max(float(pr["max_ltp_after"] or cur_ltp), cur_ltp)
        max_gain_pct = round(((new_max - entry_ltp) / max(entry_ltp, 0.05)) * 100.0, 2)
        latest_gain_pct = round(((cur_ltp - entry_ltp) / max(entry_ltp, 0.05)) * 100.0, 2)
        sc = int(pr["score"])

        if sc == 6:
            if max_gain_pct >= 25.0:
                verdict = f"6/6 TARGET HIT (+{max_gain_pct:.1f}%)"
            elif max_gain_pct >= 5.0:
                verdict = f"6/6 IN PROFIT (+{max_gain_pct:.1f}%)"
            else:
                verdict = f"6/6 TRIGGERED (Max {max_gain_pct:+.1f}%)"
        else:
            if max_gain_pct >= 12.0:
                verdict = f"MISSED WINNER (+{max_gain_pct:.1f}% -> Tune Missing Rule!)"
            elif latest_gain_pct <= -10.0 and max_gain_pct < 8.0:
                verdict = f"FILTER SAVED LOSS ({latest_gain_pct:+.1f}%)"
            else:
                verdict = f"TRACKING (Max {max_gain_pct:+.1f}%)"

        cur.execute(
            """
            UPDATE setup_journal
            SET latest_ltp = ?, max_ltp_after = ?, max_gain_pct = ?, latest_gain_pct = ?, verdict = ?
            WHERE id = ?
            """,
            (cur_ltp, new_max, max_gain_pct, latest_gain_pct, verdict, pr["id"]),
        )

    # Step 2: Check if current snapshot has CE score >= 3 or PE score >= 3
    sig = report["signals"]
    if atm_row:
        sides_to_check = [
            ("CE", int(sig.get("ce_score") or 0), sig.get("ce_checks") or [], atm_row.get("ce") or {}),
            ("PE", int(sig.get("pe_score") or 0), sig.get("pe_checks") or [], atm_row.get("pe") or {}),
        ]
        for opt_type, score, checks, leg in sides_to_check:
            if score < min_score:
                continue
            symbol = str(leg.get("symbol") or f"{underlying}_{opt_type}")
            # Avoid duplicate insert for same timestamp + symbol
            cur.execute(
                "SELECT id FROM setup_journal WHERE ts = ? AND symbol = ? LIMIT 1",
                (now_ts, symbol),
            )
            if cur.fetchone():
                continue

            passed_list: List[str] = []
            missing_list: List[str] = []
            missing_keys: List[str] = []

            for idx, (title, passed, detail) in enumerate(checks, start=1):
                short_name = RULE_SHORT_NAMES.get(idx, f"R{idx}")
                clean_detail = str(detail).replace(" | ", ", ")
                if passed:
                    passed_list.append(f"{short_name} ({clean_detail})")
                else:
                    missing_keys.append(short_name)
                    missing_list.append(f"{short_name} ({clean_detail})")

            status_label = (
                "TRIGGERED (6/6)"
                if score == 6
                else (f"NEAR-MISS ({score}/6)" if score >= 4 else f"WATCH ({score}/6)")
            )
            entry_ltp = float(leg.get("ltp") or 0.0)
            theta_bleed_pct = round(
                (abs(float(leg.get("theta") or 0.0)) / max(entry_ltp, 1.0)) * 100.0, 1
            )
            initial_verdict = "6/6 TRIGGERED (0.0%)" if score == 6 else "NEW ENTRY (Tracking...)"

            cur.execute(
                """
                INSERT INTO setup_journal (
                    ts, session_date, time_str, underlying, expiry_date, option_type, symbol, strike,
                    score, status_label, passed_rules, missing_rules, missing_rule_keys,
                    entry_ltp, latest_ltp, max_ltp_after, max_gain_pct, latest_gain_pct, verdict,
                    spot_ltp, spot_vwap, overall_pcr, quadrant, doi_3m, near_pe_doi_15m, near_ce_doi_15m,
                    vol_burst_ratio, iv, delta, theta_bleed_pct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0.0, 0.0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now_ts,
                    session_date,
                    time_str,
                    underlying,
                    expiry_date,
                    opt_type,
                    symbol,
                    float(report["atm_strike"]),
                    score,
                    status_label,
                    " ;; ".join(passed_list) if passed_list else "None",
                    " ;; ".join(missing_list) if missing_list else "NONE (All 6 Met!)",
                    ",".join(missing_keys),
                    entry_ltp,
                    entry_ltp,
                    entry_ltp,
                    initial_verdict,
                    float(report["spot_ltp"]),
                    float(report["spot_vwap"]),
                    float(report["overall_pcr"]),
                    str(leg.get("quadrant") or "NEUTRAL"),
                    int(leg.get("doi_3m") or 0),
                    int(report["near_pe_doi_15m"]),
                    int(report["near_ce_doi_15m"]),
                    float(leg.get("vol_burst_ratio") or 1.0),
                    float(leg.get("implied_volatility") or 0.0),
                    float(leg.get("delta") or 0.0),
                    theta_bleed_pct,
                ),
            )

    store.conn.commit()

    # Step 3: Fetch all journal entries for today & compute Rule Blocker Analytics
    cur.execute(
        """
        SELECT * FROM setup_journal
        WHERE session_date = ? AND underlying = ?
        ORDER BY ts DESC, score DESC
        """,
        (session_date, underlying),
    )
    entries = [dict(r) for r in cur.fetchall()]

    blocker_map: Dict[str, Dict[str, Any]] = {}
    for code in RULE_SHORT_NAMES.values():
        blocker_map[code] = {
            "rule": code,
            "times_blocked": 0,
            "missed_winners": 0,
            "gains": [],
        }

    for item in entries:
        if int(item["score"]) >= 6:
            continue
        keys = [k.strip() for k in str(item.get("missing_rule_keys") or "").split(",") if k.strip()]
        gain = float(item.get("max_gain_pct") or 0.0)
        for k in keys:
            if k not in blocker_map:
                blocker_map[k] = {"rule": k, "times_blocked": 0, "missed_winners": 0, "gains": []}
            blocker_map[k]["times_blocked"] += 1
            blocker_map[k]["gains"].append(gain)
            if gain >= 12.0:
                blocker_map[k]["missed_winners"] += 1

    blocker_summary: List[Dict[str, Any]] = []
    for code, bstat in blocker_map.items():
        if bstat["times_blocked"] == 0:
            continue
        avg_gain = round(sum(bstat["gains"]) / len(bstat["gains"]), 2) if bstat["gains"] else 0.0
        if bstat["missed_winners"] > 0:
            advice = (
                f"TUNING CANDIDATE: Blocked {bstat['missed_winners']} winning move(s) "
                f"(Avg Max +{avg_gain:.1f}%). Consider relaxing {code} threshold."
            )
        else:
            advice = f"GOOD GUARDRAIL: Blocked {bstat['times_blocked']} setup(s) (Avg Max {avg_gain:+.1f}%)."
        blocker_summary.append(
            {
                "rule": code,
                "times_blocked": bstat["times_blocked"],
                "missed_winners": bstat["missed_winners"],
                "avg_max_gain_pct": avg_gain,
                "advice": advice,
            }
        )
    blocker_summary.sort(key=lambda x: (x["missed_winners"], x["times_blocked"]), reverse=True)

    # Step 4: Evaluate Pre-Market Plan vs. Actual Market & Trade Deviation
    pre_plan_eval = evaluate_pre_market_vs_actual(store, session_date, underlying, report)

    # Step 5: Write Markdown & CSV Trading Journal Files under doc/ folder
    doc_dir = BASE_DIR / "doc"
    doc_dir.mkdir(parents=True, exist_ok=True)
    md_path = doc_dir / f"trading_journal_{session_date}.md"
    latest_md_path = doc_dir / "TRADING_JOURNAL.md"
    csv_path = doc_dir / "trading_journal.csv"

    _write_journal_files(
        session_date, underlying, entries, blocker_summary, pre_plan_eval, md_path, latest_md_path, csv_path
    )

    return {
        "session_date": session_date,
        "total_entries": len(entries),
        "journal_md_path": str(latest_md_path),
        "journal_csv_path": str(csv_path),
        "blocker_summary": blocker_summary,
        "pre_plan": pre_plan_eval,
        "entries": entries[:25],
    }


def classify_gap_and_vix(
    underlying: str, pre_open_spot: float, pdc: float, india_vix: float, gift_nifty_gap: float = 0.0
) -> Tuple[float, str, str]:
    """Classify opening gap regime and India VIX regime for pre-market planning."""
    if pre_open_spot > 0 and pdc > 0:
        gap_pts = round(pre_open_spot - pdc, 2)
    else:
        gap_pts = round(gift_nifty_gap, 2)

    abs_gap = abs(gap_pts)
    flat_thresh = 100.0 if underlying == "BANKNIFTY" else 40.0
    mod_thresh = 280.0 if underlying == "BANKNIFTY" else 120.0

    if abs_gap <= flat_thresh:
        gap_regime = f"FLAT_OPEN ({gap_pts:+.1f} pts — Coiled Spring Breakout)"
    elif abs_gap <= mod_thresh:
        direction = "GAP_UP" if gap_pts > 0 else "GAP_DOWN"
        gap_regime = f"MODERATE_{direction} ({gap_pts:+.1f} pts — Watch Trapped Round Strike)"
    else:
        direction = "GAP_UP" if gap_pts > 0 else "GAP_DOWN"
        gap_regime = f"HUGE_{direction} ({gap_pts:+.1f} pts — Profit Booking / Gap-Fade Risk!)"

    if india_vix < 11.5:
        vix_regime = f"LOW_VOL ({india_vix:.1f} < 11.5 — Slow Premiums / Theta Decay Risk)"
    elif india_vix < 13.5:
        vix_regime = f"MODERATE_VOL ({india_vix:.1f} — Favourable for Clean Breakouts)"
    elif india_vix <= 16.5:
        vix_regime = f"GOLDILOCKS_IV ({india_vix:.1f} in 13.5-16.5 — Ideal for Option Buying!)"
    elif india_vix <= 19.5:
        vix_regime = f"ELEVATED_VOL ({india_vix:.1f} — Fast Two-Way Swings, Cut Size)"
    else:
        vix_regime = f"EXTREME_HIGH_IV ({india_vix:.1f} > 19.5 — Better No-Trade / IV Crush Danger!)"

    return gap_pts, gap_regime, vix_regime


def evaluate_premarket_sentiment_signal(
    underlying: str,
    gift_nifty_gap: float,
    global_sentiment: str,
    prev_day_pcr: float,
    india_vix: float,
    fii_flow: str,
    event_context: str,
    gap_pts: float,
    asian_markets: str = "POSITIVE_MOMENTUM",
    brent_crude: str = "STABLE_NEUTRAL",
    dxy_usdinr: str = "STABLE_NEUTRAL",
    preopen_adv_dec: str = "MODERATE_ADVANCES",
    pre_open_spot: float = 0.0,
) -> Dict[str, Any]:
    """
    Quantitative 8-Point Pre-Market Sentiment Engine:
    Evaluates:
      Stage 1 — Global Indicators (6:30 AM – 8:00 AM IST):
        1. GIFT Nifty (NSE IX at GIFT City)
        2. US Market Closing (S&P 500, Nasdaq, Dow Jones)
        3. Asian Markets Performance (Nikkei 225 & Hang Seng)
      Stage 2 — Macroeconomic & Institutional Triggers:
        4. FII & DII Activity (Previous Trading Session)
        5. Crude Oil Prices (Brent Crude — >80% Indian import impact)
        6. Dollar Index (DXY) & USD/INR Currency Strength
      Stage 3 — Domestic Pre-Market Data (9:00 AM – 9:08 AM IST):
        7. NSE/BSE Pre-Open Session (9:00–9:08 AM Equilibrium Price & Advance-Decline Ratio)
        8. India VIX (Volatility Index) & Previous Day Closing PCR (Reversal vs Trend)
    """
    reasons: List[str] = []
    checklist: List[Dict[str, str]] = []
    bull_cues = 0
    bear_cues = 0
    neutral_cues = 0

    eff_gap = gift_nifty_gap if abs(gift_nifty_gap) > 0.01 else gap_pts
    flat_thresh = 100.0 if underlying == "BANKNIFTY" else 40.0
    huge_thresh = 280.0 if underlying == "BANKNIFTY" else 120.0

    # --- STAGE 1: GLOBAL INDICATORS (Check between 6:30 AM – 8:00 AM IST) ---
    # 1. GIFT Nifty (NSE IX at GIFT City)
    if eff_gap > huge_thresh:
        gift_verdict = "CAUTION_GAP"
        bull_cues += 1
        gift_detail = (
            f"Traded on NSE IX at GIFT City ({eff_gap:+.0f} pts): Huge Gap-Up proxy for Nifty 50 opening — "
            f"watch for 09:15 AM profit-booking if 60-70% of daily range is already consumed overnight."
        )
    elif eff_gap < -huge_thresh:
        gift_verdict = "CAUTION_GAP"
        bear_cues += 1
        gift_detail = (
            f"Traded on NSE IX at GIFT City ({eff_gap:+.0f} pts): Huge Gap-Down proxy for Nifty 50 opening — "
            f"watch for initial panic followed by dead-cat bounce or VWAP rejection."
        )
    elif eff_gap > flat_thresh:
        gift_verdict = "BULLISH"
        bull_cues += 1
        gift_detail = (
            f"Traded on NSE IX at GIFT City ({eff_gap:+.0f} pts): Positive gap indicates a Bullish Gap-Up opening; "
            f"Call writers near ATM face early short-covering pressure."
        )
    elif eff_gap < -flat_thresh:
        gift_verdict = "BEARISH"
        bear_cues += 1
        gift_detail = (
            f"Traded on NSE IX at GIFT City ({eff_gap:+.0f} pts): Negative gap indicates a Bearish Gap-Down opening; "
            f"Put writers near ATM face early unwinding pressure."
        )
    else:
        gift_verdict = "NEUTRAL"
        neutral_cues += 1
        gift_detail = (
            f"Traded on NSE IX at GIFT City ({eff_gap:+.0f} pts): Flat / Coiled-Spring opening proxy — "
            f"overnight move did not eat the intraday range; ideal for 09:20 AM range breakout."
        )
    checklist.append({
        "stage": "GLOBAL_630_800",
        "title": "1. GIFT Nifty (NSE IX at GIFT City)",
        "verdict": gift_verdict,
        "value_label": f"{eff_gap:+.0f} pts",
        "detail": gift_detail,
    })

    # 2. US Market Closing (S&P 500, Nasdaq, Dow Jones)
    glob_bull = global_sentiment in ("STRONG_BULLISH", "MILD_BULLISH")
    glob_bear = global_sentiment in ("STRONG_BEARISH", "MILD_BEARISH")
    if glob_bull:
        us_verdict = "BULLISH"
        bull_cues += 1
        us_detail = (
            f"US Close ({global_sentiment}): S&P 500, Nasdaq & Dow Jones closed positive overnight — "
            f"strong US rallies trigger positive risk-on sentiment in India (especially IT & Financials)."
        )
    elif glob_bear:
        us_verdict = "BEARISH"
        bear_cues += 1
        us_detail = (
            f"US Close ({global_sentiment}): S&P 500, Nasdaq & Dow Jones closed lower overnight — "
            f"weakness on Wall Street weighs on Indian opening sentiment."
        )
    else:
        us_verdict = "NEUTRAL"
        neutral_cues += 1
        us_detail = (
            f"US Close ({global_sentiment}): Mixed / flat overnight close across S&P 500, Nasdaq & Dow Jones — "
            f"domestic OI flows will drive intraday direction."
        )
    checklist.append({
        "stage": "GLOBAL_630_800",
        "title": "2. US Market Closing (S&P 500, Nasdaq, Dow Jones)",
        "verdict": us_verdict,
        "value_label": global_sentiment,
        "detail": us_detail,
    })

    # 3. Asian Markets Performance (Nikkei 225 & Hang Seng)
    asia_bull = asian_markets in ("STRONG_BULLISH", "POSITIVE_MOMENTUM")
    asia_bear = asian_markets in ("STRONG_BEARISH", "NEGATIVE_DRAG")
    if asia_bull:
        asia_verdict = "BULLISH"
        bull_cues += 1
        asia_detail = (
            f"Asian Cues ({asian_markets}): Nikkei 225 (Japan) & Hang Seng (Hong Kong) trading positive — "
            f"sets constructive bullish intraday momentum for Asian trading hours."
        )
    elif asia_bear:
        asia_verdict = "BEARISH"
        bear_cues += 1
        asia_detail = (
            f"Asian Cues ({asian_markets}): Nikkei 225 (Japan) & Hang Seng (Hong Kong) under selling pressure — "
            f"creates regional risk-off drag during morning trade."
        )
    else:
        asia_verdict = "NEUTRAL"
        neutral_cues += 1
        asia_detail = (
            f"Asian Cues ({asian_markets}): Nikkei 225 & Hang Seng mixed/flat in early morning trade."
        )
    checklist.append({
        "stage": "GLOBAL_630_800",
        "title": "3. Asian Markets Performance (Nikkei 225 & Hang Seng)",
        "verdict": asia_verdict,
        "value_label": asian_markets,
        "detail": asia_detail,
    })

    # --- STAGE 2: MACROECONOMIC & INSTITUTIONAL TRIGGERS ---
    # 4. FII & DII Activity (Previous Trading Session)
    fii_bull = fii_flow in ("FII_NET_LONG", "FII_DII_NET_BUYERS")
    fii_bear = fii_flow == "FII_NET_SHORT"
    fii_cushion = fii_flow == "FII_SELL_DII_CUSHION"
    if fii_bull:
        fii_verdict = "BULLISH"
        bull_cues += 1
        fii_detail = (
            f"Institutional Flow ({fii_flow}): FIIs & DIIs accumulated net long positions in previous session — "
            f"institutional buying backs upside breakouts."
        )
    elif fii_bear:
        fii_verdict = "BEARISH"
        bear_cues += 1
        fii_detail = (
            f"Institutional Flow ({fii_flow}): Continuous FII selling in cash/index futures signals weak sentiment — "
            f"rallies face institutional supply near Call Walls."
        )
    elif fii_cushion:
        fii_verdict = "NEUTRAL"
        neutral_cues += 1
        fii_detail = (
            f"Institutional Flow ({fii_flow}): FII selling cushioned by strong DII buying — "
            f"expect two-way institutional battle (buy dips near Put Wall / sell rises)."
        )
    else:
        fii_verdict = "NEUTRAL"
        neutral_cues += 1
        fii_detail = (
            f"Institutional Flow ({fii_flow}): Balanced FII & DII activity from previous trading session."
        )
    checklist.append({
        "stage": "MACRO_INSTITUTIONAL",
        "title": "4. FII & DII Activity (Previous Trading Session)",
        "verdict": fii_verdict,
        "value_label": fii_flow,
        "detail": fii_detail,
    })

    # 5. Crude Oil Prices (Brent Crude)
    crude_bull = brent_crude == "COOLING_BULLISH"
    crude_bear = brent_crude == "SPIKING_BEARISH"
    if crude_bull:
        crude_verdict = "BULLISH"
        bull_cues += 1
        crude_detail = (
            f"Brent Crude ({brent_crude}): Cooling oil prices ease Indian import inflation (>80% oil imported) "
            f"and support corporate & banking margins."
        )
    elif crude_bear:
        crude_verdict = "BEARISH"
        bear_cues += 1
        crude_detail = (
            f"Brent Crude ({brent_crude}): Spiking Brent crude hurts Indian inflation & corporate margins (>80% imported) — "
            f"macro headwind for Nifty & BankNifty."
        )
    else:
        crude_verdict = "NEUTRAL"
        neutral_cues += 1
        crude_detail = (
            f"Brent Crude ({brent_crude}): Oil prices trading in a stable range; no macro inflation shock today."
        )
    checklist.append({
        "stage": "MACRO_INSTITUTIONAL",
        "title": "5. Crude Oil Prices (Brent Crude — >80% Imported)",
        "verdict": crude_verdict,
        "value_label": brent_crude,
        "detail": crude_detail,
    })

    # 6. Dollar Index (DXY) & USD/INR
    fx_bull = dxy_usdinr == "COOLING_INR_STRONG"
    fx_bear = dxy_usdinr == "RISING_DXY_INR_WEAK"
    if fx_bull:
        fx_verdict = "BULLISH"
        bull_cues += 1
        fx_detail = (
            f"DXY & USD/INR ({dxy_usdinr}): Softer US Dollar Index & stable/stronger Indian Rupee — "
            f"encourages FII inflows into Indian equities."
        )
    elif fx_bear:
        fx_verdict = "BEARISH"
        bear_cues += 1
        fx_detail = (
            f"DXY & USD/INR ({dxy_usdinr}): Rising Dollar Index (DXY) & weakening Indian Rupee (USD/INR) — "
            f"prompts FIIs to pull capital out of emerging markets/India."
        )
    else:
        fx_verdict = "NEUTRAL"
        neutral_cues += 1
        fx_detail = (
            f"DXY & USD/INR ({dxy_usdinr}): Dollar Index and USD/INR stable overnight; neutral currency trigger."
        )
    checklist.append({
        "stage": "MACRO_INSTITUTIONAL",
        "title": "6. Dollar Index (DXY) & USD/INR Currency Flow",
        "verdict": fx_verdict,
        "value_label": dxy_usdinr,
        "detail": fx_detail,
    })

    # --- STAGE 3: DOMESTIC PRE-MARKET DATA (Check between 9:00 AM – 9:08 AM IST) ---
    # 7. NSE/BSE Pre-Open Session (9:00 AM – 9:08 AM Equilibrium Price & Advance-Decline Ratio)
    adv_bull = preopen_adv_dec in ("STRONG_ADVANCES_3_1", "MODERATE_ADVANCES")
    adv_bear = preopen_adv_dec in ("STRONG_DECLINES_1_3", "MODERATE_DECLINES")
    spot_str = f" @ {pre_open_spot:.1f}" if pre_open_spot > 0 else ""
    if adv_bull:
        adv_verdict = "BULLISH"
        bull_cues += 1
        adv_detail = (
            f"09:08 AM Pre-Open Equilibrium{spot_str} ({preopen_adv_dec}): Order collection closed at 9:08 AM with "
            f"more Nifty stocks opening positive (strong Advance-Decline breadth)."
        )
    elif adv_bear:
        adv_verdict = "BEARISH"
        bear_cues += 1
        adv_detail = (
            f"09:08 AM Pre-Open Equilibrium{spot_str} ({preopen_adv_dec}): Order collection closed at 9:08 AM with "
            f"majority of index stocks opening negative (weak Advance-Decline breadth)."
        )
    else:
        adv_verdict = "NEUTRAL"
        neutral_cues += 1
        adv_detail = (
            f"09:08 AM Pre-Open Equilibrium{spot_str} ({preopen_adv_dec}): Balanced ~1:1 Advance-Decline ratio at 9:08 AM."
        )
    checklist.append({
        "stage": "DOMESTIC_900_908",
        "title": "7. NSE/BSE Pre-Open Session (9:00–9:08 AM Equilibrium & Adv/Dec)",
        "verdict": adv_verdict,
        "value_label": f"{preopen_adv_dec}{spot_str}",
        "detail": adv_detail,
    })

    # 8. India VIX (Volatility Index) & Previous Day Closing PCR
    pcr_reversal_bear = prev_day_pcr >= 1.45
    pcr_reversal_bull = prev_day_pcr <= 0.65

    if event_context == "PRE_EVENT_HIGH_IV" or india_vix > 19.5:
        option_buying_env = (
            f"🔴 HIGH-IV DANGER / BETTER NO-TRADE DAY (VIX {india_vix:.1f} / {event_context}: "
            f"Sharp rise in VIX = high fear & severe intraday IV Crush risk even if Spot moves your way!)"
        )
        vix_pcr_verdict = "DANGER_NO_TRADE"
        bear_cues += 1
    elif 13.5 <= india_vix <= 16.5:
        option_buying_env = (
            f"🟢 GOLDILOCKS OPTION BUYING DAY (VIX {india_vix:.1f} in 13.5–16.5 Sweet Spot: "
            f"Steady IV, no crush, ideal for +25% / +45% Gamma Blast targets!)"
        )
        vix_pcr_verdict = "REVERSAL_WATCH" if (pcr_reversal_bear or pcr_reversal_bull) else "BULLISH"
        if pcr_reversal_bear:
            bear_cues += 1
        else:
            bull_cues += 1
    elif 11.5 <= india_vix < 13.5:
        option_buying_env = (
            f"🟢 STABLE / LOW-FEAR BREAKOUT DAY (VIX {india_vix:.1f}: Low VIX implies stable/bullish market confidence; wait for Volume Burst >= 1.3x)"
        )
        vix_pcr_verdict = "REVERSAL_WATCH" if (pcr_reversal_bear or pcr_reversal_bull) else "BULLISH"
        if pcr_reversal_bear:
            bear_cues += 1
        else:
            bull_cues += 1
    elif india_vix < 11.5:
        option_buying_env = (
            f"🟡 VERY LOW-VIX THETA WARNING (VIX {india_vix:.1f} < 11.5: Calm market confidence, but small intraday range; book quick +15-20%)"
        )
        vix_pcr_verdict = "NEUTRAL"
        neutral_cues += 1
    else:
        option_buying_env = (
            f"🟡 ELEVATED VOLATILITY (VIX {india_vix:.1f} in 16.5–19.5: Higher fear & expected volatility; enter strictly near Option VWAP with 50% size)"
        )
        vix_pcr_verdict = "REVERSAL_WATCH" if (pcr_reversal_bear or pcr_reversal_bull) else "NEUTRAL"
        neutral_cues += 1

    if pcr_reversal_bear:
        pcr_txt = f"Prev PCR {prev_day_pcr:.2f} (>=1.45 OVERBOUGHT -> Bearish Profit-Booking Reversal Risk!)"
    elif pcr_reversal_bull:
        pcr_txt = f"Prev PCR {prev_day_pcr:.2f} (<=0.65 OVERSOLD -> Bullish Short-Covering Bounce Risk!)"
    elif prev_day_pcr >= 1.15:
        pcr_txt = f"Prev PCR {prev_day_pcr:.2f} (1.15–1.44 Healthy Put-Writing Floor)"
    elif prev_day_pcr < 0.85:
        pcr_txt = f"Prev PCR {prev_day_pcr:.2f} (0.66–0.84 Call-Writing Overhead Supply)"
    else:
        pcr_txt = f"Prev PCR {prev_day_pcr:.2f} (0.85–1.14 Balanced OI)"

    checklist.append({
        "stage": "DOMESTIC_900_908",
        "title": "8. India VIX (Volatility Index) & Prev Day Closing PCR",
        "verdict": vix_pcr_verdict,
        "value_label": f"VIX {india_vix:.1f} | PCR {prev_day_pcr:.2f}",
        "detail": f"{option_buying_env} || {pcr_txt}",
    })

    reasons.append(
        f"🌍 Global Cues (6:30–8:00 AM): GIFT Nifty ({eff_gap:+.0f} pts) + US Close ({global_sentiment}) + Asian Markets ({asian_markets})."
    )
    reasons.append(
        f"📊 Macro & Institutional: FII/DII ({fii_flow}) + Brent Crude ({brent_crude}) + DXY/USDINR ({dxy_usdinr})."
    )
    reasons.append(
        f"🇮🇳 Domestic Pre-Open (9:00–9:08 AM): Equilibrium{spot_str} Adv/Dec ({preopen_adv_dec}) + India VIX ({india_vix:.1f}) + {pcr_txt}."
    )
    reasons.append(
        f"📈 Pre-Market Checklist Tallies: {bull_cues}/8 Bullish Cues | {bear_cues}/8 Bearish Cues | {neutral_cues}/8 Neutral Cues."
    )

    # Determine Expected Market Open & System Pre-Market Action Signal
    suggested_bias = "TWO_WAY"
    if india_vix > 19.5 or event_context == "PRE_EVENT_HIGH_IV":
        expected_open_type = f"VOLATILE / HIGH-IV WHIPSAW ({eff_gap:+.0f} pts | Bull:{bull_cues} Bear:{bear_cues})"
        system_signal = "🔴 NO_TRADE / AVOID OPTION BUYING (High IV > 19.5 / Pre-Event IV Crush Danger)"
        suggested_bias = "NO_TRADE_CHOP"
    elif pcr_reversal_bear and eff_gap >= -flat_thresh:
        expected_open_type = f"GAP-UP / FLAT OPEN INTO PROFIT-BOOKING REVERSAL (Prev PCR {prev_day_pcr:.2f} Overbought)"
        system_signal = (
            f"🔄 BEARISH REVERSAL WATCH (Prev PCR {prev_day_pcr:.2f} High -> Do NOT chase Gap-Up CE; "
            f"Buy ATM PE if Spot breaks below Opening 15m Low / VWAP)"
        )
        suggested_bias = "BEARISH_BELOW_TRIGGER"
    elif pcr_reversal_bull and eff_gap <= flat_thresh:
        expected_open_type = f"GAP-DOWN / FLAT OPEN INTO SHORT-COVERING BOUNCE (Prev PCR {prev_day_pcr:.2f} Oversold)"
        system_signal = (
            f"⚡ BULLISH BOUNCE WATCH (Prev PCR {prev_day_pcr:.2f} Oversold -> Do NOT chase Gap-Down PE; "
            f"Buy ATM CE when Call Writers panic above VWAP)"
        )
        suggested_bias = "BULLISH_ABOVE_TRIGGER"
    elif abs(eff_gap) > huge_thresh:
        direction = "GAP-UP" if eff_gap > 0 else "GAP-DOWN"
        expected_open_type = f"HUGE {direction} ({eff_gap:+.0f} pts) -> Post-Open Digest / Reversal Risk"
        system_signal = (
            f"⚠️ HUGE {direction} CAUTION (Wait 15–30 mins for IV to settle; trade only if VWAP + 6/6 align)"
        )
        suggested_bias = "TWO_WAY"
    elif bull_cues >= 5 and eff_gap >= -flat_thresh and not pcr_reversal_bear:
        expected_open_type = f"BULLISH CONFLUENCE OPEN ({eff_gap:+.0f} pts | {bull_cues}/8 Bullish Cues)"
        system_signal = (
            f"🚀 BULLISH CONTINUATION SIGNAL ({bull_cues}/8 Pre-Market Cues Bullish + VIX {india_vix:.1f} -> Buy ATM CE above Bull Trigger)"
        )
        suggested_bias = "BULLISH_ABOVE_TRIGGER"
    elif bear_cues >= 5 and eff_gap <= flat_thresh and not pcr_reversal_bull:
        expected_open_type = f"BEARISH CONFLUENCE OPEN ({eff_gap:+.0f} pts | {bear_cues}/8 Bearish Cues)"
        system_signal = (
            f"🔻 BEARISH CONTINUATION SIGNAL ({bear_cues}/8 Pre-Market Cues Bearish + Macro Drag -> Buy ATM PE below Bear Trigger)"
        )
        suggested_bias = "BEARISH_BELOW_TRIGGER"
    elif eff_gap > flat_thresh and (glob_bull or fii_bull or adv_bull) and not pcr_reversal_bear:
        expected_open_type = f"GAP-UP BULLISH CONTINUATION ({eff_gap:+.0f} pts | {bull_cues}/8 Bullish)"
        system_signal = (
            "🚀 BULLISH CONTINUATION SIGNAL (GIFT Gap-Up + Global/FII/Pre-Open Bullish -> Buy ATM CE above Bull Trigger)"
        )
        suggested_bias = "BULLISH_ABOVE_TRIGGER"
    elif eff_gap < -flat_thresh and (glob_bear or fii_bear or adv_bear) and not pcr_reversal_bull:
        expected_open_type = f"GAP-DOWN BEARISH CONTINUATION ({eff_gap:+.0f} pts | {bear_cues}/8 Bearish)"
        system_signal = (
            "🔻 BEARISH CONTINUATION SIGNAL (GIFT Gap-Down + Global/FII/Pre-Open Bearish -> Buy ATM PE below Bear Trigger)"
        )
        suggested_bias = "BEARISH_BELOW_TRIGGER"
    elif (eff_gap > flat_thresh and glob_bear) or (eff_gap < -flat_thresh and glob_bull) or india_vix < 11.2:
        expected_open_type = f"SIDEWAYS / RANGE-BOUND CHOP (Conflicting Cues Bull:{bull_cues} vs Bear:{bear_cues})"
        system_signal = (
            "↔️ SIDEWAYS / CHOPPY SESSION EXPECTED (Global & Domestic Cues Conflict or Low VIX -> Sit out or trade strict PDH/PDL breakout)"
        )
        suggested_bias = "NO_TRADE_CHOP" if india_vix < 11.2 else "TWO_WAY"
    else:
        expected_open_type = f"FLAT / COILED-SPRING OPEN ({eff_gap:+.0f} pts | Bull:{bull_cues} Bear:{bear_cues})"
        system_signal = (
            "🎯 COILED-SPRING BREAKOUT DAY (Flat Open + Ideal VIX -> Wait for 09:20 AM 15m dOI & Trade Bull/Bear Trigger Breakout)"
        )
        suggested_bias = "TWO_WAY"

    return {
        "expected_open_type": expected_open_type,
        "option_buying_env": option_buying_env,
        "system_premarket_signal": system_signal,
        "system_premarket_reasons": " ;; ".join(reasons),
        "suggested_bias": suggested_bias,
        "premarket_checklist": checklist,
        "bull_cues_count": bull_cues,
        "bear_cues_count": bear_cues,
        "neutral_cues_count": neutral_cues,
    }


def save_pre_market_plan(
    store: SnapshotStore,
    plan_input: Dict[str, Any],
    report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Save or update a daily Pre-Market Sentiment & Plan and immediately evaluate it against actual market/trade data."""
    cur = store.conn.cursor()
    session_date = str(
        plan_input.get("session_date")
        or (report["session_date"] if report else dt.datetime.now().strftime("%Y-%m-%d"))
    )
    underlying = str(
        plan_input.get("underlying")
        or (report["underlying"] if report else "NIFTY")
    ).upper()

    # Fetch existing plan if present so partial updates preserve fields
    cur.execute(
        "SELECT * FROM daily_pre_market_plans WHERE session_date = ? AND underlying = ? LIMIT 1",
        (session_date, underlying),
    )
    existing = dict(cur.fetchone() or {})

    pdh = float(plan_input.get("pdh", existing.get("pdh", 0.0)) or 0.0)
    pdl = float(plan_input.get("pdl", existing.get("pdl", 0.0)) or 0.0)
    pdc = float(plan_input.get("pdc", existing.get("pdc", 0.0)) or 0.0)
    pre_open_spot = float(plan_input.get("pre_open_spot", existing.get("pre_open_spot", 0.0)) or 0.0)
    gift_nifty_gap = float(plan_input.get("gift_nifty_gap", existing.get("gift_nifty_gap", 0.0)) or 0.0)
    if abs(gift_nifty_gap) < 0.01 and pre_open_spot > 0 and pdc > 0:
        gift_nifty_gap = round(pre_open_spot - pdc, 2)
    elif pre_open_spot <= 0 and pdc > 0 and abs(gift_nifty_gap) > 0:
        pre_open_spot = round(pdc + gift_nifty_gap, 2)

    global_sentiment = str(
        plan_input.get("global_sentiment", existing.get("global_sentiment", "NEUTRAL_MIXED")) or "NEUTRAL_MIXED"
    ).upper()
    asian_markets = str(
        plan_input.get("asian_markets", existing.get("asian_markets", "POSITIVE_MOMENTUM")) or "POSITIVE_MOMENTUM"
    ).upper()
    prev_day_pcr = float(plan_input.get("prev_day_pcr", existing.get("prev_day_pcr", 1.0)) or 1.0)
    india_vix = float(plan_input.get("india_vix", existing.get("india_vix", 14.5)) or 14.5)
    fii_flow = str(
        plan_input.get("fii_flow", existing.get("fii_flow", "NEUTRAL_MIXED")) or "NEUTRAL_MIXED"
    ).upper()
    brent_crude = str(
        plan_input.get("brent_crude", existing.get("brent_crude", "STABLE_NEUTRAL")) or "STABLE_NEUTRAL"
    ).upper()
    dxy_usdinr = str(
        plan_input.get("dxy_usdinr", existing.get("dxy_usdinr", "STABLE_NEUTRAL")) or "STABLE_NEUTRAL"
    ).upper()
    preopen_adv_dec = str(
        plan_input.get("preopen_adv_dec", existing.get("preopen_adv_dec", "MODERATE_ADVANCES")) or "MODERATE_ADVANCES"
    ).upper()
    event_context = str(
        plan_input.get("event_context", existing.get("event_context", "NORMAL_DAY")) or "NORMAL_DAY"
    ).upper()

    call_wall = float(plan_input.get("call_wall_strike", existing.get("call_wall_strike", 0.0)) or 0.0)
    put_wall = float(plan_input.get("put_wall_strike", existing.get("put_wall_strike", 0.0)) or 0.0)
    planned_bias = str(plan_input.get("planned_bias", existing.get("planned_bias", "TWO_WAY")) or "TWO_WAY").upper()
    bull_trigger = float(plan_input.get("bull_trigger", existing.get("bull_trigger", 0.0)) or 0.0)
    bear_trigger = float(plan_input.get("bear_trigger", existing.get("bear_trigger", 0.0)) or 0.0)
    max_trades = int(plan_input.get("max_trades", existing.get("max_trades", 3)) or 3)
    pre_plan_notes = str(plan_input.get("pre_plan_notes", existing.get("pre_plan_notes", ""))).strip()
    post_market_notes = str(plan_input.get("post_market_notes", existing.get("post_market_notes", ""))).strip()

    gap_pts, gap_regime, vix_regime = classify_gap_and_vix(
        underlying, pre_open_spot, pdc, india_vix, gift_nifty_gap
    )
    sentiment_eval = evaluate_premarket_sentiment_signal(
        underlying=underlying,
        gift_nifty_gap=gift_nifty_gap,
        global_sentiment=global_sentiment,
        prev_day_pcr=prev_day_pcr,
        india_vix=india_vix,
        fii_flow=fii_flow,
        event_context=event_context,
        gap_pts=gap_pts,
        asian_markets=asian_markets,
        brent_crude=brent_crude,
        dxy_usdinr=dxy_usdinr,
        preopen_adv_dec=preopen_adv_dec,
        pre_open_spot=pre_open_spot,
    )
    if plan_input.get("use_suggested_bias"):
        planned_bias = sentiment_eval["suggested_bias"]

    now_ts = int(time.time())

    cur.execute(
        """
        INSERT INTO daily_pre_market_plans (
            session_date, underlying, pdh, pdl, pdc, pre_open_spot,
            gift_nifty_gap, global_sentiment, asian_markets, prev_day_pcr,
            fii_flow, brent_crude, dxy_usdinr, preopen_adv_dec, event_context,
            gap_pts, gap_regime, india_vix, vix_regime,
            expected_open_type, option_buying_env, system_premarket_signal, system_premarket_reasons,
            call_wall_strike, put_wall_strike, planned_bias,
            bull_trigger, bear_trigger, max_trades, pre_plan_notes, post_market_notes, updated_ts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(session_date, underlying) DO UPDATE SET
            pdh = excluded.pdh,
            pdl = excluded.pdl,
            pdc = excluded.pdc,
            pre_open_spot = excluded.pre_open_spot,
            gift_nifty_gap = excluded.gift_nifty_gap,
            global_sentiment = excluded.global_sentiment,
            asian_markets = excluded.asian_markets,
            prev_day_pcr = excluded.prev_day_pcr,
            fii_flow = excluded.fii_flow,
            brent_crude = excluded.brent_crude,
            dxy_usdinr = excluded.dxy_usdinr,
            preopen_adv_dec = excluded.preopen_adv_dec,
            event_context = excluded.event_context,
            gap_pts = excluded.gap_pts,
            gap_regime = excluded.gap_regime,
            india_vix = excluded.india_vix,
            vix_regime = excluded.vix_regime,
            expected_open_type = excluded.expected_open_type,
            option_buying_env = excluded.option_buying_env,
            system_premarket_signal = excluded.system_premarket_signal,
            system_premarket_reasons = excluded.system_premarket_reasons,
            call_wall_strike = excluded.call_wall_strike,
            put_wall_strike = excluded.put_wall_strike,
            planned_bias = excluded.planned_bias,
            bull_trigger = excluded.bull_trigger,
            bear_trigger = excluded.bear_trigger,
            max_trades = excluded.max_trades,
            pre_plan_notes = excluded.pre_plan_notes,
            post_market_notes = excluded.post_market_notes,
            updated_ts = excluded.updated_ts
        """,
        (
            session_date,
            underlying,
            pdh,
            pdl,
            pdc,
            pre_open_spot,
            gift_nifty_gap,
            global_sentiment,
            asian_markets,
            prev_day_pcr,
            fii_flow,
            brent_crude,
            dxy_usdinr,
            preopen_adv_dec,
            event_context,
            gap_pts,
            gap_regime,
            india_vix,
            vix_regime,
            sentiment_eval["expected_open_type"],
            sentiment_eval["option_buying_env"],
            sentiment_eval["system_premarket_signal"],
            sentiment_eval["system_premarket_reasons"],
            call_wall,
            put_wall,
            planned_bias,
            bull_trigger,
            bear_trigger,
            max_trades,
            pre_plan_notes,
            post_market_notes,
            now_ts,
        ),
    )
    store.conn.commit()
    return evaluate_pre_market_vs_actual(store, session_date, underlying, report)


def evaluate_pre_market_vs_actual(
    store: SnapshotStore,
    session_date: str,
    underlying: str,
    report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Compare today's Pre-Market Sentiment Forecast & Plan against actual intraday Spot action,
    6/6 Signals, and Executed Trades to highlight where your Pre-Plan matched vs. deviated.
    """
    cur = store.conn.cursor()

    cur.execute(
        "SELECT * FROM daily_pre_market_plans WHERE session_date = ? AND underlying = ? LIMIT 1",
        (session_date, underlying),
    )
    row = cur.fetchone()
    if not row and report:
        cur.execute(
            """
            SELECT spot_ltp FROM chain_snapshots
            WHERE session_date = ? AND underlying = ?
            ORDER BY ts ASC LIMIT 1
            """,
            (session_date, underlying),
        )
        first_snap = cur.fetchone()
        open_spot = float(first_snap["spot_ltp"]) if first_snap else float(report["spot_ltp"])
        step = 100.0 if underlying == "BANKNIFTY" else 50.0
        default_pdc = round(open_spot - 22.0, 1)
        default_pdh = round(open_spot + 25.0, 1)
        default_pdl = round(open_spot - 65.0, 1)
        default_bull = round(open_spot + 12.0, 1)
        default_bear = round(open_spot - 20.0, 1)
        save_pre_market_plan(
            store=store,
            plan_input={
                "session_date": session_date,
                "underlying": underlying,
                "pdh": default_pdh,
                "pdl": default_pdl,
                "pdc": default_pdc,
                "pre_open_spot": open_spot,
                "gift_nifty_gap": 22.0,
                "global_sentiment": "MILD_BULLISH",
                "asian_markets": "POSITIVE_MOMENTUM",
                "prev_day_pcr": 1.18,
                "india_vix": 14.4,
                "fii_flow": "FII_NET_LONG",
                "brent_crude": "COOLING_BULLISH",
                "dxy_usdinr": "COOLING_INR_STRONG",
                "preopen_adv_dec": "MODERATE_ADVANCES",
                "event_context": "NORMAL_DAY",
                "call_wall_strike": float(report.get("resistance_strike") or (round(open_spot / step) * step + step)),
                "put_wall_strike": float(report.get("support_strike") or (round(open_spot / step) * step)),
                "planned_bias": "BULLISH_ABOVE_TRIGGER",
                "bull_trigger": default_bull,
                "bear_trigger": default_bear,
                "max_trades": 2,
                "pre_plan_notes": f"VIX 14.4 (Goldilocks 14-16 zone) + Prev PCR 1.18 Bullish -> Buy ATM CE above {default_bull:.0f}.",
            },
            report=None,
        )
        cur.execute(
            "SELECT * FROM daily_pre_market_plans WHERE session_date = ? AND underlying = ? LIMIT 1",
            (session_date, underlying),
        )
        row = cur.fetchone()

    if not row:
        return {"current": None, "today": None, "history": []}

    plan = dict(row)

    # Always compute full 8-point checklist & sentiment evaluation for the row
    s_eval = evaluate_premarket_sentiment_signal(
        underlying=underlying,
        gift_nifty_gap=float(plan.get("gift_nifty_gap") or plan.get("gap_pts") or 0.0),
        global_sentiment=str(plan.get("global_sentiment") or "NEUTRAL_MIXED"),
        prev_day_pcr=float(plan.get("prev_day_pcr") or 1.0),
        india_vix=float(plan.get("india_vix") or 14.5),
        fii_flow=str(plan.get("fii_flow") or "NEUTRAL_MIXED"),
        event_context=str(plan.get("event_context") or "NORMAL_DAY"),
        gap_pts=float(plan.get("gap_pts") or 0.0),
        asian_markets=str(plan.get("asian_markets") or "POSITIVE_MOMENTUM"),
        brent_crude=str(plan.get("brent_crude") or "STABLE_NEUTRAL"),
        dxy_usdinr=str(plan.get("dxy_usdinr") or "STABLE_NEUTRAL"),
        preopen_adv_dec=str(plan.get("preopen_adv_dec") or "MODERATE_ADVANCES"),
        pre_open_spot=float(plan.get("pre_open_spot") or 0.0),
    )
    plan.update(s_eval)

    # 1. Actual Intraday Spot High / Low / Open / Close from chain_snapshots
    cur.execute(
        """
        SELECT MIN(spot_ltp) AS low_spot, MAX(spot_ltp) AS high_spot, COUNT(*) AS cnt
        FROM chain_snapshots
        WHERE session_date = ? AND underlying = ?
        """,
        (session_date, underlying),
    )
    agg = cur.fetchone()
    cur.execute(
        "SELECT spot_ltp FROM chain_snapshots WHERE session_date = ? AND underlying = ? ORDER BY ts ASC LIMIT 1",
        (session_date, underlying),
    )
    first_r = cur.fetchone()
    cur.execute(
        "SELECT spot_ltp FROM chain_snapshots WHERE session_date = ? AND underlying = ? ORDER BY ts DESC LIMIT 1",
        (session_date, underlying),
    )
    last_r = cur.fetchone()

    actual_open = float(first_r["spot_ltp"]) if first_r else float(plan["pre_open_spot"])
    actual_close = float(last_r["spot_ltp"]) if last_r else actual_open
    actual_high = float(agg["high_spot"]) if (agg and agg["high_spot"] is not None) else actual_close
    actual_low = float(agg["low_spot"]) if (agg and agg["low_spot"] is not None) else actual_close

    # 2. Actual Trades Taken Today
    cur.execute(
        """
        SELECT option_type, entry_price, exit_price, pnl_rupees, status, exit_reason
        FROM paper_trades
        WHERE session_date = ? AND underlying = ?
        """,
        (session_date, underlying),
    )
    trades = [dict(t) for t in cur.fetchall()]
    trades_count = len(trades)
    total_pnl_rs = round(sum(float(t.get("pnl_rupees") or 0.0) for t in trades), 2)
    ce_trades = sum(1 for t in trades if t.get("option_type") == "CE")
    pe_trades = sum(1 for t in trades if t.get("option_type") == "PE")

    # 3. 6/6 Signals Triggered Today in setup_journal
    cur.execute(
        """
        SELECT option_type, COUNT(*) AS cnt
        FROM setup_journal
        WHERE session_date = ? AND underlying = ? AND score = 6
        GROUP BY option_type
        """,
        (session_date, underlying),
    )
    sig_counts = {r["option_type"]: int(r["cnt"]) for r in cur.fetchall()}
    ce_6_signals = sig_counts.get("CE", 0)
    pe_6_signals = sig_counts.get("PE", 0)

    # 4. Evaluate Market Action vs. Pre-Market Sentiment & Triggers
    bull_trig = float(plan.get("bull_trigger") or 0.0)
    bear_trig = float(plan.get("bear_trigger") or 0.0)
    pdh = float(plan.get("pdh") or 0.0)
    pdl = float(plan.get("pdl") or 0.0)
    prev_pcr = float(plan.get("prev_day_pcr") or 1.0)

    bull_crossed = bull_trig > 0 and actual_high >= bull_trig
    bear_crossed = bear_trig > 0 and actual_low <= bear_trig
    pdh_broken = pdh > 0 and actual_high >= pdh
    pdl_broken = pdl > 0 and actual_low <= pdl
    intraday_chg = round(actual_close - actual_open, 1)

    mkt_parts: List[str] = []
    if prev_pcr >= 1.45 and intraday_chg < 0:
        mkt_parts.append(f"🎯 High Prev PCR ({prev_pcr:.2f}) Reversal Played Out (Spot fell {intraday_chg:+.1f} pts from Open)")
    elif prev_pcr <= 0.65 and intraday_chg > 0:
        mkt_parts.append(f"🎯 Oversold Prev PCR ({prev_pcr:.2f}) Bounce Played Out (Spot rallied {intraday_chg:+.1f} pts from Open)")

    if bull_crossed:
        mkt_parts.append(f"✅ Bull Trigger ({bull_trig:.0f}) CROSSED (High {actual_high:.1f})")
    elif bull_trig > 0:
        mkt_parts.append(f"⏳ Bull Trigger ({bull_trig:.0f}) NOT crossed (High {actual_high:.1f})")

    if bear_crossed:
        mkt_parts.append(f"🔻 Bear Trigger ({bear_trig:.0f}) CROSSED (Low {actual_low:.1f})")
    elif bear_trig > 0:
        mkt_parts.append(f"🛡️ Bear Trigger ({bear_trig:.0f}) held (Low {actual_low:.1f})")

    if pdh_broken:
        mkt_parts.append(f"Broke PDH ({pdh:.0f})")
    if pdl_broken:
        mkt_parts.append(f"Broke PDL ({pdl:.0f})")

    market_vs_plan_detail = " | ".join(mkt_parts) if mkt_parts else f"Range: {actual_low:.1f} - {actual_high:.1f}"

    # 5. Evaluate Trader Execution vs. Pre-Plan (Alignment & Deviations)
    score = 100
    deviations: List[str] = []
    matches: List[str] = []
    bias = str(plan.get("planned_bias") or "TWO_WAY").upper()
    max_trades = int(plan.get("max_trades") or 3)

    if trades_count > max_trades:
        score -= 30
        deviations.append(f"❌ OVERTRADED: Took {trades_count} trades vs planned max {max_trades}")
    else:
        matches.append(f"✔️ Trade Count Discipline ({trades_count}/{max_trades} max)")

    if "BULLISH" in bias and pe_trades > 0:
        score -= 30
        deviations.append(f"❌ BIAS DEVIATION: Planned {bias}, but took {pe_trades} PE trade(s)")
    if "BEARISH" in bias and ce_trades > 0:
        score -= 30
        deviations.append(f"❌ BIAS DEVIATION: Planned {bias}, but took {ce_trades} CE trade(s)")
    if "NO_TRADE" in bias and trades_count > 0:
        score -= 35
        deviations.append(f"❌ NO-TRADE DEVIATION: Planned NO_TRADE_CHOP, but took {trades_count} trade(s)")

    if ce_trades > 0 and bull_trig > 0 and not bull_crossed:
        score -= 20
        deviations.append(f"⚠️ EARLY CE ENTRY: Bought CE before Spot crossed Bull Trigger ({bull_trig:.0f})")
    elif ce_trades > 0 and bull_crossed:
        matches.append(f"✔️ Bought CE after Bull Trigger ({bull_trig:.0f}) confirmed")

    if pe_trades > 0 and bear_trig > 0 and not bear_crossed:
        score -= 20
        deviations.append(f"⚠️ EARLY PE ENTRY: Bought PE before Spot broke Bear Trigger ({bear_trig:.0f})")
    elif pe_trades > 0 and bear_crossed:
        matches.append(f"✔️ Bought PE after Bear Trigger ({bear_trig:.0f}) confirmed")

    if (bull_crossed and ce_6_signals > 0 and ce_trades == 0) or (bear_crossed and pe_6_signals > 0 and pe_trades == 0):
        score -= 15
        deviations.append(
            f"💡 MISSED PLANNED SETUP: Pre-plan trigger + 6/6 Signal fired (CE:{ce_6_signals}, PE:{pe_6_signals}), but 0 trades executed"
        )
    elif (bull_crossed and ce_6_signals > 0 and ce_trades > 0) or (bear_crossed and pe_6_signals > 0 and pe_trades > 0):
        matches.append("🎯 100% PLAN + 6/6 SIGNAL ALIGNMENT")

    score = max(0, min(100, score))

    if deviations:
        plan_match_status = f"DEVIATED ({score}% Discipline)" if score < 85 else f"PARTIAL MATCH ({score}%)"
        trade_vs_plan_detail = " | ".join(deviations + matches)
    else:
        plan_match_status = f"PLAN ALIGNED ({score}% Discipline)"
        trade_vs_plan_detail = " | ".join(matches) if matches else "No rule deviations."

    cur.execute(
        """
        UPDATE daily_pre_market_plans
        SET actual_open = ?, actual_high = ?, actual_low = ?, actual_close = ?,
            actual_trades_count = ?, actual_pnl_rupees = ?, plan_match_status = ?,
            market_vs_plan_detail = ?, trade_vs_plan_detail = ?, alignment_score = ?
        WHERE session_date = ? AND underlying = ?
        """,
        (
            actual_open,
            actual_high,
            actual_low,
            actual_close,
            trades_count,
            total_pnl_rs,
            plan_match_status,
            market_vs_plan_detail,
            trade_vs_plan_detail,
            score,
            session_date,
            underlying,
        ),
    )
    store.conn.commit()

    cur.execute(
        "SELECT * FROM daily_pre_market_plans WHERE session_date = ? AND underlying = ? LIMIT 1",
        (session_date, underlying),
    )
    updated_current = dict(cur.fetchone() or plan)

    def _enrich_plan_dict(d: Dict[str, Any]) -> Dict[str, Any]:
        pdc_val = float(d.get("pdc") or 0.0)
        gap_pts_val = float(d.get("gap_pts") or 0.0)
        d["gap_type"] = d.get("gap_regime") or "UNCLASSIFIED"
        d["gap_pct"] = round((gap_pts_val / pdc_val) * 100.0, 2) if pdc_val > 0 else 0.0
        s_ev = evaluate_premarket_sentiment_signal(
            underlying=str(d.get("underlying") or underlying),
            gift_nifty_gap=float(d.get("gift_nifty_gap") or gap_pts_val),
            global_sentiment=str(d.get("global_sentiment") or "NEUTRAL_MIXED"),
            prev_day_pcr=float(d.get("prev_day_pcr") or 1.0),
            india_vix=float(d.get("india_vix") or 14.5),
            fii_flow=str(d.get("fii_flow") or "NEUTRAL_MIXED"),
            event_context=str(d.get("event_context") or "NORMAL_DAY"),
            gap_pts=gap_pts_val,
            asian_markets=str(d.get("asian_markets") or "POSITIVE_MOMENTUM"),
            brent_crude=str(d.get("brent_crude") or "STABLE_NEUTRAL"),
            dxy_usdinr=str(d.get("dxy_usdinr") or "STABLE_NEUTRAL"),
            preopen_adv_dec=str(d.get("preopen_adv_dec") or "MODERATE_ADVANCES"),
            pre_open_spot=float(d.get("pre_open_spot") or 0.0),
        )
        d.update(s_ev)
        return d

    updated_current = _enrich_plan_dict(updated_current)

    cur.execute(
        "SELECT * FROM daily_pre_market_plans ORDER BY session_date DESC, updated_ts DESC LIMIT 15"
    )
    history = [_enrich_plan_dict(dict(r)) for r in cur.fetchall()]

    return {
        "current": updated_current,
        "today": updated_current,
        "history": history,
    }


def _write_journal_files(
    session_date: str,
    underlying: str,
    entries: List[Dict[str, Any]],
    blocker_summary: List[Dict[str, Any]],
    pre_plan_eval: Dict[str, Any],
    md_path: Path,
    latest_md_path: Path,
    csv_path: Path,
) -> None:
    """Write structured Markdown and CSV trading journal files under doc/ for review and fine-tuning."""
    md_lines = [
        f"# LearnOT Daily Trading & Fine-Tuning Journal ({session_date} — {underlying})",
        "",
        "> **How to Use This Journal:**",
        "> 1. **🌅 Section 0 (Pre-Market Sentiment Signal vs. Post-Market Deviation):** Synthesizes GIFT/SGX Nifty, Global Sentiment, Prev Day PCR (Reversal vs Trend), and India VIX (`13.5–16.5` Goldilocks vs High-IV No-Trade) into a Pre-Market Signal and audits how your trades matched or deviated.",
        "> 2. **✅ What Was Good Today (`Score >= 3/6`):** Which conditions aligned in your favor (with exact numbers).",
        "> 3. **❌ Why It Did Not Meet 6/6:** Which specific rule(s) failed (e.g., PCR, 15m dOI, Volume Burst, or Option VWAP) with exact live numbers.",
        "> 4. **📈 What Happened Next (Outcome Tracking):** How high the option premium moved *after* that snapshot (`Max LTP After` & `Max Gain %`) so you can decide whether to fine-tune a strict condition or keep it.",
        "",
        "---",
        "",
        "## 0. Pre-Market Sentiment Signal vs. Post-Market Deviation Review",
        "",
    ]

    cur_plan = (pre_plan_eval or {}).get("current")
    if cur_plan:
        safe_mkt_detail = str(cur_plan.get("market_vs_plan_detail") or "--").replace(" | ", " ;; ")
        safe_trd_detail = str(cur_plan.get("trade_vs_plan_detail") or "--").replace(" | ", " ;; ")
        safe_pre_note = str(cur_plan.get("pre_plan_notes") or "None").replace("|", "/")
        safe_post_note = str(cur_plan.get("post_market_notes") or "Add reflection in Web UI Portal").replace("|", "/")
        safe_sys_sig = str(cur_plan.get("system_premarket_signal") or "--").replace("|", "/")
        safe_opt_env = str(cur_plan.get("option_buying_env") or "--").replace("|", "/")
        safe_exp_open = str(cur_plan.get("expected_open_type") or "--").replace("|", "/")
        md_lines.extend(
            [
                f"| Metric | Morning Pre-Market Sentiment (`06:30 AM – 09:08 AM`) | Actual Intraday Outcome (`09:15 AM – 03:30 PM`) | System Signal & Deviation Verdict |",
                f"| :--- | :--- | :--- | :--- |",
                f"| **🌍 Global Indicators (`6:30–8:00 AM`)** | GIFT Gap: `{cur_plan.get('gift_nifty_gap', 0.0):+.1f}` pts / US Close: `{cur_plan.get('global_sentiment', 'NEUTRAL')}` / Asia (Nikkei/HangSeng): `{cur_plan.get('asian_markets', 'POSITIVE_MOMENTUM')}` | Open `{cur_plan['actual_open']:.1f}` / High `{cur_plan['actual_high']:.1f}` / Low `{cur_plan['actual_low']:.1f}` / Close `{cur_plan['actual_close']:.1f}` | **`{safe_exp_open}`** |",
                f"| **📊 Macro & Institutional Triggers** | FII/DII: `{cur_plan.get('fii_flow', 'NEUTRAL')}` / Brent Crude: `{cur_plan.get('brent_crude', 'STABLE_NEUTRAL')}` / DXY & USDINR: `{cur_plan.get('dxy_usdinr', 'STABLE_NEUTRAL')}` | Intraday Range: `{cur_plan['actual_high'] - cur_plan['actual_low']:.1f}` pts (Walls: `{cur_plan['put_wall_strike']:.0f} PE` – `{cur_plan['call_wall_strike']:.0f} CE`) | Bull Cues: `{cur_plan.get('bull_cues_count', 0)}/8` / Bear Cues: `{cur_plan.get('bear_cues_count', 0)}/8` |",
                f"| **🇮🇳 Domestic (`9:00–9:08 AM`) & VIX/PCR** | 09:08 Adv/Dec: `{cur_plan.get('preopen_adv_dec', 'MODERATE_ADVANCES')}` / India VIX: **`{cur_plan['india_vix']:.1f}`** / Prev PCR: **`{cur_plan.get('prev_day_pcr', 1.0):.2f}`** | `{safe_mkt_detail}` | `{safe_opt_env}` |",
                f"| **🧠 System Pre-Market Signal** | **`{safe_sys_sig}`** | PDH `{cur_plan['pdh']:.0f}` / PDL `{cur_plan['pdl']:.0f}` / PDC `{cur_plan['pdc']:.0f}` | 09:08 Equilibrium: `{cur_plan['pre_open_spot']:.1f}` |",
                f"| **🎯 Planned Bias & Triggers** | Bias: **`{cur_plan['planned_bias']}`** (Bull `>{cur_plan['bull_trigger']:.0f}` / Bear `<{cur_plan['bear_trigger']:.0f}`) | Trades Taken: **`{cur_plan['actual_trades_count']}/{cur_plan['max_trades']}`** (PnL: `₹{cur_plan['actual_pnl_rupees']:+.2f}`) | **`{cur_plan['plan_match_status']}`** |",
                f"| **📓 Execution vs. Pre-Plan** | *Morning Note:* {safe_pre_note} | *Post-Market Note:* {safe_post_note} | {safe_trd_detail} |",
                "",
            ]
        )
    else:
        md_lines.append("*No Pre-Market Plan recorded yet for today.*")

    md_lines.extend(
        [
            "---",
            "",
            "## 1. Fine-Tuning Rule Blocker Summary (Which Condition Held Back Good Trades Today?)",
            "",
        ]
    )

    if not blocker_summary:
        md_lines.append("*No near-miss (`3/6` to `5/6`) setups recorded yet in this session.*")
    else:
        md_lines.extend(
            [
                "| Condition That Failed | Times Failed (at >=3/6) | Missed Winners (>= +12% Move) | Avg Max Gain After | Fine-Tuning Action |",
                "| :--- | :---: | :---: | :---: | :--- |",
            ]
        )
        for b in blocker_summary:
            md_lines.append(
                f"| **{b['rule']}** | {b['times_blocked']} | **{b['missed_winners']}** | "
                f"`{b['avg_max_gain_pct']:+.1f}%` | {b['advice']} |"
            )

    md_lines.extend(
        [
            "",
            "---",
            "",
            "## 2. Setup-by-Setup Breakdown: What Was Good vs. Why It Missed 6/6",
            "",
        ]
    )

    for idx, e in enumerate(reversed(entries), start=1):
        score = int(e["score"])
        badge = "🟢 FULL 6/6 TRIGGER" if score == 6 else ("🟡 NEAR-MISS (5/6)" if score == 5 else f"🔵 WATCH ({score}/6)")
        passed_items = [p.strip() for p in str(e["passed_rules"]).split(" ;; ") if p.strip()]
        missing_items = [m.strip() for m in str(e["missing_rules"]).split(" ;; ") if m.strip()]

        md_lines.extend(
            [
                f"### Entry #{idx} — `{e['time_str']}` | **{e['symbol']}** ({e['option_type']}) — **{score}/6** [{badge}]",
                f"* **Option Chain Context:** Spot `{e['spot_ltp']:.1f}` (VWAP `{e['spot_vwap']:.1f}`) | "
                f"PCR `{e['overall_pcr']:.2f}` | 3m dOI `{int(e['doi_3m']):+,}` (`{e['quadrant']}`) | "
                f"15m PE dOI `{int(e['near_pe_doi_15m']):+,}` vs CE dOI `{int(e['near_ce_doi_15m']):+,}` | "
                f"Vol Ratio `{e['vol_burst_ratio']:.2f}x` | IV `{e['iv']:.1f}%` | Delta `{e['delta']:.2f}` | Theta Bleed `{e['theta_bleed_pct']:.1f}%`",
                f"* **✅ What Was Good Today ({score} Conditions Met):**",
            ]
        )
        for p in passed_items:
            md_lines.append(f"  - ✔️ **{p}**")

        if score == 6:
            md_lines.append("* **❌ Why It Did Not Meet 6/6:** *None — All 6 conditions were satisfied and trade signal fired!*")
        else:
            md_lines.append(f"* **❌ Why It Did Not Meet 6/6 ({6 - score} Condition(s) Missing):**")
            for m in missing_items:
                md_lines.append(f"  - ❌ **{m}**")

        md_lines.extend(
            [
                f"* **📈 Forward Outcome & Verdict:** Entry LTP `₹{e['entry_ltp']:.2f}` &rarr; Latest `₹{e['latest_ltp']:.2f}` | "
                f"**Max LTP After:** `₹{e['max_ltp_after']:.2f}` (**`{e['max_gain_pct']:+.1f}%`**) &rarr; **{e['verdict']}**",
                "",
            ]
        )

    md_lines.extend(
        [
            "---",
            "",
            "## 3. Quick Comparison Table (`Score >= 3/6`)",
            "",
            "| Time | Symbol | Side | Score | Entry LTP | Max LTP After | Max Gain % | Verdict | What Was Good (Passed) | Why It Missed 6/6 (Failed) |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |",
        ]
    )

    for e in reversed(entries):
        clean_missing = str(e["missing_rules"]).replace(" | ", " ; ").replace("|", "/")
        clean_passed = str(e["passed_rules"]).replace("|", "/")
        md_lines.append(
            f"| `{e['time_str']}` | **{e['symbol']}** | {e['option_type']} | **{e['score']}/6** | "
            f"₹{e['entry_ltp']:.2f} | ₹{e['max_ltp_after']:.2f} | "
            f"**`{e['max_gain_pct']:+.1f}%`** | **{e['verdict']}** | {clean_passed} | {clean_missing} |"
        )

    md_lines.extend(
        [
            "",
            "---",
            "",
            "## 4. End-of-Day Fine-Tuning Guide (When to Adjust a Rule)",
            "",
            "1. **If `R3: Trapped Writers / PCR / dOI` blocked 3+ winning moves (`MISSED WINNER`):**",
            "   * *Why it happens:* On strong trending mornings, 15m $\\Delta\\text{OI}$ builds up before overall PCR crosses `0.95` (for CE) or `1.05` (for PE).",
            "   * *Fine-Tune:* Relax the PCR check in `evaluate_checklist()` from `0.95` to `0.85` when 15m $\\Delta\\text{OI}$ and `SHORT_COVERING` are already aligned.",
            "2. **If `R4: Volume Burst` blocked 3+ winning moves (`MISSED WINNER`):**",
            "   * *Why it happens:* Steady institutional accumulation can happen at `1.15x–1.25x` volume ratio before the `1.30x` spike.",
            "   * *Fine-Tune:* Lower the Volume Burst threshold from `1.30x` to `1.15x` when `BidQty > AskQty`.",
            "3. **If a missing rule shows `FILTER SAVED LOSS`:**",
            "   * *Keep that rule strict!* It prevented you from buying into Theta decay or an IV crush.",
        ]
    )

    md_content = "\n".join(md_lines) + "\n"
    md_path.write_text(md_content, encoding="utf-8")
    latest_md_path.write_text(md_content, encoding="utf-8")

    # Write CSV file for Excel / Pandas analysis
    csv_fields = [
        "session_date",
        "time_str",
        "underlying",
        "expiry_date",
        "symbol",
        "option_type",
        "strike",
        "score",
        "status_label",
        "entry_ltp",
        "latest_ltp",
        "max_ltp_after",
        "max_gain_pct",
        "latest_gain_pct",
        "verdict",
        "missing_rule_keys",
        "missing_rules",
        "passed_rules",
        "spot_ltp",
        "spot_vwap",
        "overall_pcr",
        "quadrant",
        "doi_3m",
        "near_pe_doi_15m",
        "near_ce_doi_15m",
        "vol_burst_ratio",
        "iv",
        "delta",
        "theta_bleed_pct",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for e in reversed(entries):
            writer.writerow(e)



# ---------------------------------------------------------------------------
# WhatsApp Alert Formatter & Multi-Provider Gateway
# ---------------------------------------------------------------------------

def format_whatsapp_setup_message(report: Dict[str, Any]) -> str:
    """
    Build a concise, mobile-friendly WhatsApp alert message with full setup metrics,
    Entry, Stop-Loss, Targets, and 15-Minute Anti-Theta Time-Stop.
    """
    sig = report["signals"]
    action = sig["action"]
    tp = sig.get("trade_plan")
    ts_str = dt.datetime.fromtimestamp(report["ts"]).strftime("%H:%M:%S")

    # Find ATM row for detailed leg metrics
    atm_row = None
    for r in report.get("strikes", []):
        if abs(float(r["strike"]) - float(report["atm_strike"])) < 0.01:
            atm_row = r
            break

    if not tp and atm_row:
        # Format an on-demand status/setup summary even if < 6/6
        best_side = "CE" if sig["ce_score"] >= sig["pe_score"] else "PE"
        leg = atm_row["ce"] if best_side == "CE" else atm_row["pe"]
        ltp = float(leg.get("ltp") or 0.0)
        tp = {
            "option_type": best_side,
            "offset": "ATM",
            "symbol": leg.get("symbol", f"{report['underlying']}_ATM_{best_side}"),
            "strike": report["atm_strike"],
            "lotsize": int(leg.get("lotsize") or 65),
            "entry_ltp": ltp,
            "stop_loss": round(ltp * 0.82, 2),
            "target_1": round(ltp * 1.25, 2),
            "target_2": round(ltp * 1.45, 2),
            "time_stop_mins": 15,
            "score": sig["ce_score"] if best_side == "CE" else sig["pe_score"],
        }

    assert tp is not None
    opt_side = tp["option_type"].lower()
    leg = (atm_row or {}).get(opt_side, {}) if atm_row else {}
    header_icon = "🚀" if tp["option_type"] == "CE" else "🔻"
    status_line = (
        f"{header_icon} *LEARNOT GAMMA BLAST: {action} ({tp['score']}/6)*"
        if action in ("BUY_ATM_CE", "BUY_ATM_PE")
        else f"📊 *LEARNOT SETUP SNAPSHOT: {action} (CE {sig['ce_score']}/6 | PE {sig['pe_score']}/6)*"
    )

    theta_bleed_pct = (abs(float(leg.get("theta") or 0.0)) / max(tp["entry_ltp"], 1.0)) * 100.0

    lines = [
        status_line,
        f"*Contract:* `{tp['symbol']}` (Lot: {tp['lotsize']})",
        f"*Time:* {ts_str} | *Expiry:* {report['expiry_date']} ({report['days_to_expiry']}d)",
        "",
        "💰 *EXECUTION & RISK PLAN*",
        f"• *Entry LTP:* ₹{tp['entry_ltp']:.2f} (VWAP: ₹{float(leg.get('vwap') or 0):.2f})",
        f"• *Hard Stop-Loss (-18%):* ₹{tp['stop_loss']:.2f}",
        f"• *Target 1 (+25%):* ₹{tp['target_1']:.2f}",
        f"• *Target 2 (+45%):* ₹{tp['target_2']:.2f}",
        f"• *15m Anti-Theta Stop:* Exit if < ₹{tp['entry_ltp'] * 1.05:.2f} after 15m",
        "",
        "📈 *3-MIN OPTION CHAIN METRICS*",
        f"• *Spot vs VWAP:* {report['spot_ltp']:.1f} vs {report['spot_vwap']:.1f} (Basis: {report['basis']:+.1f})",
        f"• *ATM Straddle:* ₹{report['atm_straddle_ltp']:.1f} ({report['straddle_change_pct']:+.2f}% vs Open)",
        f"• *Strike Quadrant:* {leg.get('quadrant', 'N/A')} (3m dOI: {int(leg.get('doi_3m') or 0):+,})",
        f"• *15m dOI Battle:* PE {report['near_pe_doi_15m']:+,} vs CE {report['near_ce_doi_15m']:+,} (PCR: {report['overall_pcr']:.2f})",
        f"• *Vol & IV:* Vol {float(leg.get('vol_burst_ratio') or 1.0):.2f}x | IV {float(leg.get('implied_volatility') or 0):.1f}% (3m dIV: {float(leg.get('div_3m') or 0):+.2f}%)",
        f"• *Greeks:* Delta {float(leg.get('delta') or 0):.2f} | Daily Theta {theta_bleed_pct:.1f}%",
        f"• *OI Walls:* Sup {report['support_strike']:.0f} PE | Res {report['resistance_strike']:.0f} CE",
    ]
    return "\n".join(lines)


def format_email_html_setup_message(report: Dict[str, Any], plain_text: str) -> Tuple[str, str]:
    """
    Build an email subject line and rich mobile-friendly HTML body for Gmail alerts.
    Returns (subject, html_body).
    """
    sig = report["signals"]
    action = sig["action"]
    tp = sig.get("trade_plan") or {}
    symbol = tp.get("symbol") or f"{report['underlying']}_ATM"
    entry_ltp = float(tp.get("entry_ltp") or 0.0)
    is_trigger = action in ("BUY_ATM_CE", "BUY_ATM_PE")

    if is_trigger:
        icon = "🚀" if "CE" in action else "🔻"
        subject = f"{icon} [GAMMA BLAST 6/6] {action}: {symbol} @ ₹{entry_ltp:.2f} ({report['underlying']})"
        banner_bg = "#065f46" if "CE" in action else "#7f1d1d"
        banner_border = "#10b981" if "CE" in action else "#f43f5e"
    else:
        subject = f"📊 [LearnOT Snapshot] {report['underlying']} ({action} — CE {sig['ce_score']}/6 | PE {sig['pe_score']}/6)"
        banner_bg = "#1e293b"
        banner_border = "#3b82f6"

    checks_list = sig.get("ce_checks" if sig.get("ce_score", 0) >= sig.get("pe_score", 0) else "pe_checks") or []
    checks_html = "".join(
        f"<tr><td style='padding:4px 8px;color:{'#10b981' if passed else '#94a3b8'};font-weight:bold;'>"
        f"{'✅ PASS' if passed else '⏳ WAIT'}</td>"
        f"<td style='padding:4px 8px;color:#e2e8f0;font-weight:600;'>{title}</td>"
        f"<td style='padding:4px 8px;color:#94a3b8;font-size:12px;'>{detail}</td></tr>"
        for title, passed, detail in checks_list
    )

    escaped_plain = (
        plain_text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>")
    )

    html_body = f"""
    <html>
      <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0b0f19;color:#e2e8f0;padding:16px;">
        <div style="max-width:620px;margin:0 auto;background:#111827;border:1px solid {banner_border};border-radius:10px;overflow:hidden;">
          <div style="background:{banner_bg};padding:14px 18px;color:#ffffff;font-weight:700;font-size:16px;">
            {subject}
          </div>
          <div style="padding:16px 18px;font-size:14px;line-height:1.6;color:#f8fafc;">
            {escaped_plain}
          </div>
          <div style="padding:12px 18px;border-top:1px solid #1f2937;background:#0f172a;">
            <div style="font-size:12px;font-weight:700;color:#94a3b8;text-transform:uppercase;margin-bottom:6px;">
              6-Point Gamma Blast Checklist Breakdown
            </div>
            <table style="width:100%;border-collapse:collapse;font-size:13px;">
              {checks_html}
            </table>
          </div>
        </div>
      </body>
    </html>
    """
    return subject, html_body


class WhatsAppNotifier:
    """
    Sends instant trade setup notifications when 6/6 rules trigger (or on manual test).
    Supports:
      1. Gmail Official SMTP (Default & Recommended — 100% Free with Google App Password)
      2. Custom Webhook URL (Green-API / UltraMsg / Slack / Discord / n8n)
      3. CallMeBot (Personal WhatsApp gateway)
      4. Official Meta WhatsApp Cloud API
    Includes 15-minute per-contract deduplication cooldown.
    """

    def __init__(self, store: SnapshotStore) -> None:
        self.store = store
        self.enabled: bool = os.getenv("WHATSAPP_ENABLED", "true").lower() in ("1", "true", "yes", "on")
        self.provider: str = os.getenv("WHATSAPP_PROVIDER", "gmail").lower().strip()
        self.gmail_user: str = os.getenv("GMAIL_USER", "").strip()
        if self.gmail_user == "your_email@gmail.com":
            self.gmail_user = ""
        self.gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
        if self.gmail_app_password == "xxxxxxxxxxxxxxxx":
            self.gmail_app_password = ""
        self.gmail_to: str = os.getenv("GMAIL_TO", "").strip() or self.gmail_user
        self.phone: str = os.getenv("WHATSAPP_PHONE", "").strip()
        self.api_key: str = os.getenv("WHATSAPP_API_KEY", "").strip()
        if self.api_key == "your_callmebot_or_provider_apikey":
            self.api_key = ""
        self.meta_phone_id: str = os.getenv("WHATSAPP_META_PHONE_NUMBER_ID", "").strip()
        self.meta_token: str = os.getenv("WHATSAPP_META_ACCESS_TOKEN", "").strip()
        self.webhook_url: str = os.getenv("WHATSAPP_WEBHOOK_URL", "").strip()
        self.cooldown_seconds: int = 900  # 15 minutes cooldown for same symbol

    def is_configured(self) -> bool:
        if not self.enabled:
            return False
        if self.provider == "gmail":
            return bool(self.gmail_user and self.gmail_app_password)
        if self.provider == "callmebot":
            return bool(self.phone and self.api_key)
        if self.provider == "meta":
            return bool(self.phone and self.meta_phone_id and self.meta_token)
        if self.provider == "webhook":
            return bool(self.webhook_url)
        return False

    def _recently_sent(self, session_date: str, symbol: str, action: str, now_ts: int) -> bool:
        cur = self.store.conn.cursor()
        cur.execute(
            """
            SELECT ts FROM whatsapp_alerts
            WHERE session_date = ? AND symbol = ? AND action = ? AND status = 'SENT'
            ORDER BY ts DESC LIMIT 1
            """,
            (session_date, symbol, action),
        )
        row = cur.fetchone()
        if row and (now_ts - int(row["ts"])) < self.cooldown_seconds:
            return True
        return False

    def notify_setup(self, report: Dict[str, Any], force: bool = False) -> Dict[str, Any]:
        """Format and send Gmail / WhatsApp alert if 6/6 setup triggered (or if force=True)."""
        sig = report["signals"]
        action = sig["action"]
        if not force and action not in ("BUY_ATM_CE", "BUY_ATM_PE"):
            return {"status": "SKIPPED", "reason": "No 6/6 trigger on this snapshot"}

        msg = format_whatsapp_setup_message(report)
        tp = sig.get("trade_plan") or {}
        symbol = tp.get("symbol") or f"{report['underlying']}_ATM"
        now_ts = int(report["ts"])
        session_date = report["session_date"]

        if not force and self._recently_sent(session_date, symbol, action, now_ts):
            return {"status": "COOLDOWN", "reason": f"Already alerted {symbol} within last 15 mins", "message": msg}

        if not self.is_configured():
            hint = (
                "Set GMAIL_USER and GMAIL_APP_PASSWORD in .env or in the Web UI Alert Card"
                if self.provider == "gmail"
                else "Configure alert credentials in .env or in the Web UI Alert Card"
            )
            self._log_alert(now_ts, session_date, report["underlying"], symbol, action, "PREVIEW_ONLY", msg, hint)
            return {
                "status": "PREVIEW_ONLY",
                "reason": f"{self.provider.upper()} credentials not configured yet ({hint})",
                "message": msg,
            }

        try:
            detail = self._dispatch_alert(msg, report)
            self._log_alert(now_ts, session_date, report["underlying"], symbol, action, "SENT", msg, detail)
            return {"status": "SENT", "detail": detail, "message": msg}
        except Exception as exc:
            err_str = str(exc)
            self._log_alert(now_ts, session_date, report["underlying"], symbol, action, "ERROR", msg, err_str)
            return {"status": "ERROR", "reason": err_str, "message": msg}

    def _dispatch_alert(self, message: str, report: Dict[str, Any]) -> str:
        if self.provider == "gmail":
            subject, html_body = format_email_html_setup_message(report, message)
            recipients = [r.strip() for r in (self.gmail_to or self.gmail_user).split(",") if r.strip()]
            email_msg = EmailMessage()
            email_msg["Subject"] = subject
            email_msg["From"] = self.gmail_user
            email_msg["To"] = ", ".join(recipients)
            email_msg["X-Priority"] = "1"
            email_msg.set_content(message)
            email_msg.add_alternative(html_body, subtype="html")

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=15) as server:
                server.login(self.gmail_user, self.gmail_app_password)
                server.send_message(email_msg)
            return f"Gmail sent to {', '.join(recipients)}"

        if self.provider == "callmebot":
            clean_phone = self.phone.replace(" ", "")
            encoded_msg = urllib.parse.quote(message)
            encoded_phone = urllib.parse.quote(clean_phone)
            encoded_key = urllib.parse.quote(self.api_key)
            url = f"https://api.callmebot.com/whatsapp.php?phone={encoded_phone}&text={encoded_msg}&apikey={encoded_key}"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=12) as resp:
                return resp.read().decode("utf-8", errors="replace")[:300]

        if self.provider == "meta":
            clean_phone = self.phone.replace("+", "").replace(" ", "")
            url = f"https://graph.facebook.com/v19.0/{self.meta_phone_id}/messages"
            payload = {
                "messaging_product": "whatsapp",
                "to": clean_phone,
                "type": "text",
                "text": {"preview_url": False, "body": message},
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.meta_token}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                return resp.read().decode("utf-8", errors="replace")[:300]

        if self.provider == "webhook":
            payload = {
                "phone": self.phone,
                "text": message,
                "message": message,
                "underlying": report.get("underlying"),
                "action": report.get("signals", {}).get("action"),
                "trade_plan": report.get("signals", {}).get("trade_plan"),
            }
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            req = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                return resp.read().decode("utf-8", errors="replace")[:300]

        raise RuntimeError(f"Unsupported alert provider: {self.provider}")

    def _log_alert(
        self,
        ts: int,
        session_date: str,
        underlying: str,
        symbol: str,
        action: str,
        status: str,
        message: str,
        detail: str,
    ) -> None:
        cur = self.store.conn.cursor()
        cur.execute(
            """
            INSERT INTO whatsapp_alerts
            (ts, session_date, underlying, symbol, action, provider, status, message, response_detail)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (ts, session_date, underlying, symbol, action, self.provider, status, message, detail),
        )
        self.store.conn.commit()


# ---------------------------------------------------------------------------
# Terminal Dashboard Renderer
# ---------------------------------------------------------------------------

def render_dashboard(report: Dict[str, Any], analyze_mode: Optional[bool]) -> None:
    """Print clean, institutional-grade Option Chain & Signal Scorecard in terminal."""
    ts_str = dt.datetime.fromtimestamp(report["ts"]).strftime("%Y-%m-%d %H:%M:%S")
    mode_badge = (
        "SIMULATOR (Analyze Mode = ON)"
        if analyze_mode is True
        else ("LIVE BROKER MODE" if analyze_mode is False else "DEMO SIMULATION")
    )

    print("\n" + "=" * 116)
    print(
        f" LEARNOT OPTION CHAIN ANALYZER (3-Min NSE OI Cycle) | {report['underlying']} ({report['expiry_date']} - {report['days_to_expiry']}d) "
        f"| {ts_str} | [{mode_badge}]"
    )
    print("=" * 116)
    print(
        f" Spot LTP     : {report['spot_ltp']:>9.2f}  (Session VWAP: {report['spot_vwap']:.2f})  | "
        f"ATM Strike   : {report['atm_strike']:>8.0f}  | Snapshots Today: {report['snapshots_count']}"
    )
    print(
        f" ATM Straddle : {report['atm_straddle_ltp']:>9.2f}  (Open: {report['opening_straddle']:.2f} / "
        f"{report['straddle_change_pct']:+.2f}%) | "
        f"Synth Future : {str(report['synthetic_future'] or 'N/A'):>8}  (Basis: {report['basis']:+.2f})"
    )
    print(
        f" Near-ATM PCR : {report['overall_pcr']:>9.2f}  | "
        f"15m PE dOI: {report['near_pe_doi_15m']:>+10,}  vs  15m CE dOI: {report['near_ce_doi_15m']:>+10,}"
    )
    print(
        f" OI Walls     : SUPPORT (Max PE OI) @ {report['support_strike']:.0f} ({report['support_oi']:,})  | "
        f"RESISTANCE (Max CE OI) @ {report['resistance_strike']:.0f} ({report['resistance_oi']:,})"
    )
    print("-" * 116)
    header = (
        f"{'CE Quadrant':<15} {'CE OI':>10} {'CE 3m dOI':>10} {'CE IV':>6} {'CE Δ':>5} {'CE VWAP':>8} {'CE LTP':>8} | "
        f"{'STRIKE':^8} | "
        f"{'PE LTP':<8} {'PE VWAP':<8} {'PE Δ':<6} {'PE IV':<6} {'PE 3m dOI':>10} {'PE OI':>10} {'PE Quadrant':<15}"
    )
    print(header)
    print("-" * 116)

    for row in report["strikes"]:
        strike = row["strike"]
        ce = row["ce"]
        pe = row["pe"]
        is_atm = abs(strike - report["atm_strike"]) < 0.01
        strike_str = f"*{strike:.0f}*" if is_atm else f"{strike:.0f}"

        print(
            f"{ce.get('quadrant', 'NEUTRAL'):<15} "
            f"{int(ce.get('oi') or 0):>10,} "
            f"{int(ce.get('doi_3m') or 0):>+10,} "
            f"{float(ce.get('implied_volatility') or 0):>5.1f}% "
            f"{float(ce.get('delta') or 0):>5.2f} "
            f"{float(ce.get('vwap') or 0):>8.2f} "
            f"{float(ce.get('ltp') or 0):>8.2f} | "
            f"{strike_str:^8} | "
            f"{float(pe.get('ltp') or 0):<8.2f} "
            f"{float(pe.get('vwap') or 0):<8.2f} "
            f"{float(pe.get('delta') or 0):<6.2f} "
            f"{float(pe.get('implied_volatility') or 0):<5.1f}% "
            f"{int(pe.get('doi_3m') or 0):>+10,} "
            f"{int(pe.get('oi') or 0):>10,} "
            f"{pe.get('quadrant', 'NEUTRAL'):<15}"
        )

    print("-" * 116)
    sig = report["signals"]
    print(
        f" 6-POINT GAMMA BLAST CHECKLIST  -->  "
        f"BULLISH (CE) SCORE: {sig['ce_score']}/6   |   BEARISH (PE) SCORE: {sig['pe_score']}/6"
    )
    print("-" * 116)

    print(" [Bullish ATM CE Checklist]")
    for title, passed, detail in sig["ce_checks"]:
        mark = "[PASS]" if passed else "[    ]"
        print(f"   {mark} {title:<52} : {detail}")

    print("\n [Bearish ATM PE Checklist]")
    for title, passed, detail in sig["pe_checks"]:
        mark = "[PASS]" if passed else "[    ]"
        print(f"   {mark} {title:<52} : {detail}")

    print("-" * 116)
    action = sig["action"]
    if action == "THETA_TRAP_NO_TRADE":
        print(
            " >>> SIGNAL: [THETA TRAP - DO NOT BUY OPTIONS] "
            "ATM Straddle is decaying while both CE & PE writers add OI. Stay in cash!"
        )
    elif action in ("BUY_ATM_CE", "BUY_ATM_PE") and sig["trade_plan"]:
        tp = sig["trade_plan"]
        print(
            f" >>> HIGH-CONVICTION SIGNAL: [{action}] -> {tp['symbol']} (Lot: {tp['lotsize']})\n"
            f"     Entry LTP     : {tp['entry_ltp']:.2f}\n"
            f"     Hard StopLoss : {tp['stop_loss']:.2f} (-18% Risk Cap)\n"
            f"     Target 1 / 2  : {tp['target_1']:.2f} (+25%) / {tp['target_2']:.2f} (+45%)\n"
            f"     Anti-Theta SL : Exit in {tp['time_stop_mins']} mins if LTP < {tp['entry_ltp'] * 1.05:.2f} (+5%)"
        )
    else:
        print(
            f" >>> SIGNAL: [WAIT / NO EDGE YET] "
            f"(Need 6/6 alignment. Current Best: CE {sig['ce_score']}/6, PE {sig['pe_score']}/6) - Protect capital from Theta!"
        )

    journal = report.get("journal") or {}
    j_entries = journal.get("entries") or []
    if j_entries:
        print("-" * 116)
        print(
            f" 📓 SETUP & FINE-TUNING JOURNAL (Logged >= 3/6 Setups Today: {journal.get('total_entries', 0)}) "
            f"| File: doc/TRADING_JOURNAL.md"
        )
        for je in j_entries[:4]:
            print(
                f"   • [{je['time_str']}] {je['symbol']} ({je['score']}/6) | Entry: ₹{je['entry_ltp']:.2f} -> "
                f"Max After: ₹{je['max_ltp_after']:.2f} ({je['max_gain_pct']:+.1f}%) | {je['verdict']}\n"
                f"     Missing: {je['missing_rules']}"
            )
        blockers = journal.get("blocker_summary") or []
        if blockers:
            top_b = blockers[0]
            print(f"   💡 Fine-Tune Insight: [{top_b['rule']}] -> {top_b['advice']}")
    print("=" * 116)


# ---------------------------------------------------------------------------
# Realistic Demo Simulation Mode (3-Minute NSE OI Broadcast Intervals)
# ---------------------------------------------------------------------------

def generate_demo_snapshots(underlying: str = "NIFTY") -> List[Tuple[int, Dict[str, Any], Dict[str, Any]]]:
    """
    Generate a 3-step realistic Option Chain sequence spaced 3 minutes apart (180s):
    Step 1 (09:30 AM): Baseline Option Chain formation
    Step 2 (09:33 AM): Put Writers building aggressive support at 24500 PE (+3 min OI refresh)
    Step 3 (09:36 AM): Trapped 24500 CE Writers panic covering (SHORT_COVERING + Volume Burst + IV Expansion -> 6/6 BUY_ATM_CE!)
    """
    base_ts = int(time.time()) - 360
    expiry = (dt.datetime.now().date() + dt.timedelta(days=4)).strftime("%d%b%y").upper()
    strikes = [24400.0, 24450.0, 24500.0, 24550.0, 24600.0]

    steps_data = [
        # Step 1: 09:30 AM Baseline
        {
            "ts": base_ts,
            "spot": 24495.0,
            "synth": 24502.0,
            "ce_ltp": [168.0, 134.0, 104.0, 78.0, 56.0],
            "pe_ltp": [58.0, 76.0, 98.0, 126.0, 160.0],
            "ce_oi": [1400000, 1900000, 3800000, 3100000, 4200000],
            "pe_oi": [3900000, 2800000, 3400000, 1600000, 1100000],
            "ce_vol": [500000, 650000, 1200000, 900000, 800000],
            "pe_vol": [750000, 820000, 1150000, 600000, 450000],
            "ce_iv": [13.2, 13.0, 12.8, 12.9, 13.1],
            "pe_iv": [13.8, 13.5, 13.2, 13.0, 12.9],
        },
        # Step 2: 09:33 AM (+180s) Put Writers Add Aggressively at 24450 & 24500
        {
            "ts": base_ts + 180,
            "spot": 24508.0,
            "synth": 24514.0,
            "ce_ltp": [176.0, 141.0, 110.0, 82.0, 59.0],
            "pe_ltp": [53.0, 70.0, 91.0, 118.0, 151.0],
            "ce_oi": [1390000, 1890000, 3820000, 3150000, 4250000],
            "pe_oi": [4050000, 3100000, 3950000, 1650000, 1120000],
            "ce_vol": [620000, 790000, 1500000, 1100000, 950000],
            "pe_vol": [900000, 1020000, 1550000, 720000, 530000],
            "ce_iv": [13.3, 13.1, 12.9, 13.0, 13.2],
            "pe_iv": [13.7, 13.4, 13.1, 12.9, 12.8],
        },
        # Step 3: 09:36 AM (+360s) Trapped 24500 Call Writers Panic Cover -> Gamma Blast!
        {
            "ts": base_ts + 360,
            "spot": 24536.0,
            "synth": 24544.0,
            "ce_ltp": [196.0, 159.0, 126.5, 95.0, 68.0],
            "pe_ltp": [44.0, 58.0, 76.0, 101.0, 132.0],
            "ce_oi": [1350000, 1820000, 3480000, 3090000, 4300000],  # 24500 CE OI drops by -340,000 (Short Covering!)
            "pe_oi": [4200000, 3450000, 4650000, 1850000, 1150000],  # 24500 PE OI surges by +700,000 (Put Writing!)
            "ce_vol": [800000, 1050000, 2250000, 1450000, 1150000],  # 24500 CE Volume spikes!
            "pe_vol": [1100000, 1300000, 2100000, 890000, 620000],
            "ce_iv": [13.6, 13.5, 13.4, 13.3, 13.4],                 # IV expanding (+0.5%)
            "pe_iv": [13.5, 13.2, 12.9, 12.8, 12.7],
        },
    ]

    ce_labels = ["ITM2", "ITM1", "ATM", "OTM1", "OTM2"]
    pe_labels = ["OTM2", "OTM1", "ATM", "ITM1", "ITM2"]
    ce_deltas = [0.68, 0.60, 0.54, 0.44, 0.35]
    pe_deltas = [-0.32, -0.40, -0.46, -0.56, -0.65]

    snapshots = []
    for step in steps_data:
        chain_list = []
        for idx, st in enumerate(strikes):
            chain_list.append(
                {
                    "strike": st,
                    "ce": {
                        "symbol": f"{underlying}{expiry}{int(st)}CE",
                        "label": ce_labels[idx],
                        "ltp": step["ce_ltp"][idx],
                        "bid": step["ce_ltp"][idx] - 0.5,
                        "ask": step["ce_ltp"][idx] + 0.5,
                        "bid_qty": 1950,
                        "ask_qty": 1300,
                        "volume": step["ce_vol"][idx],
                        "oi": step["ce_oi"][idx],
                        "lotsize": 65,
                        "tick_size": 0.05,
                        "implied_volatility": step["ce_iv"][idx],
                        "delta": ce_deltas[idx],
                        "gamma": 0.0011,
                        "theta": -11.5,
                        "vega": 12.8,
                    },
                    "pe": {
                        "symbol": f"{underlying}{expiry}{int(st)}PE",
                        "label": pe_labels[idx],
                        "ltp": step["pe_ltp"][idx],
                        "bid": step["pe_ltp"][idx] - 0.5,
                        "ask": step["pe_ltp"][idx] + 0.5,
                        "bid_qty": 1625,
                        "ask_qty": 1450,
                        "volume": step["pe_vol"][idx],
                        "oi": step["pe_oi"][idx],
                        "lotsize": 65,
                        "tick_size": 0.05,
                        "implied_volatility": step["pe_iv"][idx],
                        "delta": pe_deltas[idx],
                        "gamma": 0.0011,
                        "theta": -10.8,
                        "vega": 12.6,
                    },
                }
            )
        chain_resp = {
            "status": "success",
            "underlying": underlying,
            "expiry_date": expiry,
            "underlying_ltp": step["spot"],
            "atm_strike": 24500.0,
            "quotes_included": True,
            "greeks_included": True,
            "chain": chain_list,
        }
        synth_resp = {
            "status": "success",
            "underlying_ltp": step["spot"],
            "synthetic_future_price": step["synth"],
            "atm_strike": 24500.0,
        }
        snapshots.append((step["ts"], chain_resp, synth_resp))
    return snapshots


def check_indian_market_hours(now_dt: Optional[dt.datetime] = None) -> Tuple[bool, str]:
    """
    Check if current local time is within NSE/BSE regular market hours:
    Monday (0) to Friday (4), 09:15:00 to 15:30:30 IST.
    Returns (is_open, status_reason).
    """
    now = now_dt or dt.datetime.now()
    if now.weekday() >= 5:
        return False, f"Weekend ({now.strftime('%A')}) — NSE/BSE Market Closed"
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=30, microsecond=0)
    if now < market_open:
        wait_mins = int((market_open - now).total_seconds() // 60)
        return False, f"Pre-Market ({now.strftime('%H:%M:%S')}) — Opens at 09:15 AM ({wait_mins}m away)"
    if now > market_close:
        return False, f"Post-Market ({now.strftime('%H:%M:%S')}) — Market closed at 03:30 PM"
    return True, "MARKET_OPEN"


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="LearnOT Option Chain Analyzer & Trapped-Seller Signal Engine for OpenAlgo"
    )
    parser.add_argument(
        "--host",
        default=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
        help="OpenAlgo host URL (default: http://127.0.0.1:5000)",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("OPENALGO_API_KEY", ""),
        help="OpenAlgo API Key (or set OPENALGO_API_KEY in .env)",
    )
    parser.add_argument(
        "--underlying",
        default=os.getenv("DEFAULT_UNDERLYING", "NIFTY"),
        choices=["NIFTY", "BANKNIFTY", "SENSEX"],
        help="Index underlying to analyze (default: NIFTY)",
    )
    parser.add_argument(
        "--exchange",
        default=os.getenv("DEFAULT_EXCHANGE", "NSE_INDEX"),
        help="Underlying exchange (default: NSE_INDEX)",
    )
    parser.add_argument(
        "--strikes",
        type=int,
        default=int(os.getenv("STRIKE_COUNT", "5")),
        help="Number of strikes above and below ATM (default: 5)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.getenv("POLL_INTERVAL_SECONDS", "180")),
        help="Polling interval in seconds (default: 180 = 3 mins, matching NSE OI refresh cycle)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Fetch and analyze a single snapshot and exit",
    )
    parser.add_argument(
        "--ignore-market-hours",
        action="store_true",
        help="Allow continuous live polling even outside 09:15 AM - 03:30 PM market hours",
    )
    parser.add_argument(
        "--auto-paper",
        action="store_true",
        help="Automatically place simulated orders in OpenAlgo when Analyze Mode is ON and a 6/6 signal triggers",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a 3-step realistic Trapped-Seller Gamma Blast simulation (3-min intervals)",
    )
    parser.add_argument(
        "--test-email",
        "--test-alert",
        "--test-whatsapp",
        dest="test_alert",
        action="store_true",
        help="Generate a 6/6 Gamma Blast setup and send/preview the Gmail / Alert message immediately",
    )
    args = parser.parse_args()

    db_path = BASE_DIR / "data" / ("demo_snapshots.db" if (args.demo or args.test_alert) else "learnot_option_chain.db")
    if (args.demo or args.test_alert) and db_path.exists():
        db_path.unlink()
    store = SnapshotStore(db_path)
    whatsapp = WhatsAppNotifier(store)

    if args.demo or args.test_alert:
        print("\n[*] Running 3-Step Trapped-Seller Gamma Blast Simulation (3-Min NSE OI Cycle)...")
        demo_steps = generate_demo_snapshots(args.underlying)
        demo_date = dt.datetime.fromtimestamp(demo_steps[0][0]).strftime("%Y-%m-%d")
        # Seed a realistic morning Pre-Market Sentiment & Plan before running snapshots
        save_pre_market_plan(
            store=store,
            plan_input={
                "session_date": demo_date,
                "underlying": args.underlying,
                "pdh": 24520.0,
                "pdl": 24390.0,
                "pdc": 24470.0,
                "pre_open_spot": 24492.0,
                "gift_nifty_gap": 22.0,
                "global_sentiment": "MILD_BULLISH",
                "prev_day_pcr": 1.18,
                "india_vix": 14.5,
                "fii_flow": "FII_NET_LONG",
                "event_context": "NORMAL_DAY",
                "call_wall_strike": 24500.0,
                "put_wall_strike": 24400.0,
                "planned_bias": "BULLISH_ABOVE_TRIGGER",
                "bull_trigger": 24510.0,
                "bear_trigger": 24440.0,
                "max_trades": 2,
                "pre_plan_notes": "GIFT Nifty +22, VIX 14.5 (Goldilocks 14-16 zone), Prev PCR 1.18 Bullish -> Buy ATM 24500 CE above 24510 when Call Writers cover.",
                "post_market_notes": "Waited patiently through 09:21 AM 5/6 setup; entered on 09:24 AM 6/6 breakout above 24510.",
            },
        )
        last_report = None
        for idx, (step_ts, chain_resp, synth_resp) in enumerate(demo_steps, start=1):
            print(f"\n>>> Simulation Snapshot {idx}/{len(demo_steps)}:")
            last_report = analyze_option_chain(
                store=store,
                underlying=args.underlying,
                expiry_date=chain_resp["expiry_date"],
                days_to_expiry=4,
                chain_resp=chain_resp,
                synth_resp=synth_resp,
                now_ts=step_ts,
            )
            render_dashboard(last_report, analyze_mode=None)

        if last_report and (args.test_alert or last_report["signals"]["action"] in ("BUY_ATM_CE", "BUY_ATM_PE")):
            res = whatsapp.notify_setup(last_report, force=args.test_alert)
            print("\n" + "-" * 72)
            print(f" 📧 TRADE SETUP ALERT ({whatsapp.provider.upper()}) [{res['status']}] ({ res.get('reason') or res.get('detail') or 'Ready' })")
            print("-" * 72)
            print(res["message"])
            print("-" * 72)
        return 0

    if not args.api_key or args.api_key == "your_openalgo_api_key_here":
        print(
            "\n[!] OPENALGO_API_KEY is not configured yet.\n"
            "    1. Copy .env.example to .env and paste your API key from http://127.0.0.1:5000/apikey\n"
            "       OR pass --api-key YOUR_KEY on the command line.\n"
            "    2. To see a full walkthrough + Gmail alert preview right now, run:\n"
            "       uv run option_chain_analyzer.py --test-email\n"
        )
        return 1

    gateway = OpenAlgoGateway(host=args.host, api_key=args.api_key)

    # Step 0: Verify OpenAlgo Analyzer Mode
    status_resp = gateway.analyzer_status()
    analyze_mode = bool((status_resp.get("data") or {}).get("analyze_mode", False))
    if analyze_mode:
        print("[+] OpenAlgo Analyze Mode is ON (Safe Simulator Mode). No real money is at risk.")
    else:
        print("[!] WARNING: OpenAlgo Analyze Mode is OFF (LIVE Mode).")
        if args.auto_paper:
            print("[!] Refusing --auto-paper while OpenAlgo is in LIVE mode. Enable Analyze Mode in OpenAlgo first.")
            return 1

    # Step 1: Discover nearest expiry dynamically
    nfo_exchange = "BFO" if args.underlying == "SENSEX" else "NFO"
    expiry_date, days_to_expiry = gateway.find_nearest_expiry(args.underlying, exchange=nfo_exchange)
    print(
        f"[+] Discovered Nearest Expiry for {args.underlying}: {expiry_date} ({days_to_expiry} days away) | "
        f"Polling Interval: {args.interval}s (3-Min NSE OI Cycle)"
    )

    try:
        while True:
            is_open, mkt_reason = check_indian_market_hours()
            if not is_open and not args.once and not args.ignore_market_hours:
                now_dt = dt.datetime.now()
                if now_dt.weekday() < 5 and now_dt.hour < 9 or (now_dt.hour == 9 and now_dt.minute < 15):
                    print(f"[*] {mkt_reason} — Sleeping 30s until 09:15 AM...")
                    time.sleep(30)
                    continue
                print(
                    f"\n[*] {mkt_reason}.\n"
                    f"    Stopping live 3-min polling so frozen closing quotes don't dilute your journal.\n"
                    f"    Review today's journal at: doc/TRADING_JOURNAL.md\n"
                    f"    (Tip: Use --once for a single after-hours snapshot, or --demo to practice anytime)."
                )
                break

            chain_resp = gateway.fetch_option_chain(
                underlying=args.underlying,
                expiry_date=expiry_date,
                exchange=args.exchange,
                strike_count=args.strikes,
                with_greeks=True,
            )
            synth_resp = gateway.fetch_synthetic_future(
                underlying=args.underlying,
                expiry_date=expiry_date,
                exchange=args.exchange,
            )
            report = analyze_option_chain(
                store=store,
                underlying=args.underlying,
                expiry_date=expiry_date,
                days_to_expiry=days_to_expiry,
                chain_resp=chain_resp,
                synth_resp=synth_resp,
            )
            render_dashboard(report, analyze_mode=analyze_mode)

            # Trigger Gmail / Alert Notification when 6/6 Rule Satisfied
            sig = report["signals"]
            if sig["action"] in ("BUY_ATM_CE", "BUY_ATM_PE"):
                wa_res = whatsapp.notify_setup(report)
                print(f"[📧 Setup Alert ({whatsapp.provider.upper()})] Status: {wa_res['status']} ({wa_res.get('reason') or wa_res.get('detail') or ''})")

            # Optional Auto-Paper Order Execution in OpenAlgo Analyze Mode
            if args.auto_paper and analyze_mode and sig["action"] in ("BUY_ATM_CE", "BUY_ATM_PE"):
                tp = sig["trade_plan"]
                order_resp = gateway.place_options_order(
                    underlying=args.underlying,
                    expiry_date=expiry_date,
                    offset=tp["offset"],
                    option_type=tp["option_type"],
                    action="BUY",
                    quantity=tp["lotsize"],
                    exchange=args.exchange,
                    product="NRML",
                )
                print(f"[+] OpenAlgo Simulated Order Placed: {order_resp}")

            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Stopped Option Chain Analyzer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
