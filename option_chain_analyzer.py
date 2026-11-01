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
            """
        )
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

    # Step 4: Write Markdown & CSV Trading Journal Files under doc/ folder
    doc_dir = BASE_DIR / "doc"
    doc_dir.mkdir(parents=True, exist_ok=True)
    md_path = doc_dir / f"trading_journal_{session_date}.md"
    latest_md_path = doc_dir / "TRADING_JOURNAL.md"
    csv_path = doc_dir / "trading_journal.csv"

    _write_journal_files(session_date, underlying, entries, blocker_summary, md_path, latest_md_path, csv_path)

    return {
        "session_date": session_date,
        "total_entries": len(entries),
        "journal_md_path": str(latest_md_path),
        "journal_csv_path": str(csv_path),
        "blocker_summary": blocker_summary,
        "entries": entries[:25],
    }


def _write_journal_files(
    session_date: str,
    underlying: str,
    entries: List[Dict[str, Any]],
    blocker_summary: List[Dict[str, Any]],
    md_path: Path,
    latest_md_path: Path,
    csv_path: Path,
) -> None:
    """Write structured Markdown and CSV trading journal files under doc/ for review and fine-tuning."""
    md_lines = [
        f"# LearnOT Daily Trading & Fine-Tuning Journal ({session_date} — {underlying})",
        "",
        "> **How to Use This Journal:**",
        "> Whenever at least **3 out of 6 conditions (`Score >= 3/6`)** are met on a 3-minute snapshot, this journal automatically records:",
        "> 1. **✅ What Was Good Today:** Which conditions aligned in your favor (with exact numbers).",
        "> 2. **❌ Why It Did Not Meet 6/6:** Which specific rule(s) failed (e.g., PCR, 15m dOI, Volume Burst, or Option VWAP) with exact live numbers.",
        "> 3. **📈 What Happened Next (Outcome Tracking):** How high the option premium moved *after* that snapshot (`Max LTP After` & `Max Gain %`) so you can decide whether to fine-tune a strict condition or keep it.",
        "",
        "---",
        "",
        "## 1. Fine-Tuning Rule Blocker Summary (Which Condition Held Back Good Trades Today?)",
        "",
    ]

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
