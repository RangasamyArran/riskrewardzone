#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
LearnOT - Interactive Web UI for Nifty & BankNifty Option Chain Analyzer
Connected to OpenAlgo (http://127.0.0.1:5000) + Zerodha

Zero external dependencies required! Uses Python's standard library HTTP server
and shares the quantitative engine & SQLite store with `option_chain_analyzer.py`.

Run with uv:
    uv run dashboard_ui.py --port 8080
Then open:
    http://127.0.0.1:8080
"""

import argparse
import datetime as dt
import json
import os
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

from option_chain_analyzer import (
    BASE_DIR,
    OpenAlgoGateway,
    SnapshotStore,
    WhatsAppNotifier,
    analyze_option_chain,
    check_indian_market_hours,
    format_whatsapp_setup_message,
    generate_demo_snapshots,
    log_evaluation_trace_offline,
    save_pre_market_plan,
    update_and_write_setup_journal,
)


# ---------------------------------------------------------------------------
# Application State Manager
# ---------------------------------------------------------------------------

class AnalyzerAppState:
    """Manages live OpenAlgo polling (3-min NSE OI cycle), WhatsApp alerts, demo progression, and paper trades."""

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.host: str = os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000")
        self.api_key: str = os.getenv("OPENALGO_API_KEY", "")
        if self.api_key == "your_openalgo_api_key_here":
            self.api_key = ""

        self.mode: str = "LIVE_OPENALGO" if self.api_key else "DEMO"
        self.underlying: str = os.getenv("DEFAULT_UNDERLYING", "NIFTY")
        self.exchange: str = os.getenv("DEFAULT_EXCHANGE", "NSE_INDEX")
        self.strike_count: int = int(os.getenv("STRIKE_COUNT", "5"))

        self.live_store = SnapshotStore(BASE_DIR / "data" / "learnot_option_chain.db")
        self.demo_store = SnapshotStore(BASE_DIR / "data" / "ui_demo_snapshots.db")

        self.demo_step_idx: int = 0
        self.demo_scenarios: List[Any] = []
        self.last_report: Optional[Dict[str, Any]] = None
        self.last_error: Optional[str] = None
        self.last_whatsapp_result: Optional[Dict[str, Any]] = None
        self.analyze_mode: Optional[bool] = None
        self.eval_cycle_count: int = 0
        self.last_eval_wall_time: str = ""
        self.last_eval_epoch: float = 0.0
        self.auto_poll_interval_sec: int = 180

        self._reset_demo(self.underlying)

    def _reset_demo(self, underlying: str) -> None:
        db_file = BASE_DIR / "data" / "ui_demo_snapshots.db"
        try:
            self.demo_store.conn.close()
        except Exception:
            pass
        if db_file.exists():
            db_file.unlink()
        self.demo_store = SnapshotStore(db_file)
        self.demo_scenarios = self._build_extended_demo(underlying)
        scale = 2.0 if underlying == "BANKNIFTY" else 1.0
        demo_dt = dt.datetime.fromtimestamp(self.demo_scenarios[0][0])
        prev_date = (demo_dt - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        demo_date = demo_dt.strftime("%Y-%m-%d")

        # Seed Yesterday's completed record (Example of High Prev PCR 1.54 Contrarian Bearish Reversal Day)
        save_pre_market_plan(
            store=self.demo_store,
            plan_input={
                "session_date": prev_date,
                "underlying": underlying,
                "pdh": round(24610.0 * scale, 2),
                "pdl": round(24440.0 * scale, 2),
                "pdc": round(24550.0 * scale, 2),
                "pre_open_spot": round(24585.0 * scale, 2),
                "gift_nifty_gap": round(35.0 * scale, 2),
                "global_sentiment": "NEUTRAL_MIXED",
                "asian_markets": "NEGATIVE_DRAG",
                "prev_day_pcr": 1.54,
                "india_vix": 15.2,
                "fii_flow": "FII_NET_SHORT",
                "brent_crude": "SPIKING_BEARISH",
                "dxy_usdinr": "RISING_DXY_INR_WEAK",
                "preopen_adv_dec": "MODERATE_DECLINES",
                "event_context": "NORMAL_DAY",
                "call_wall_strike": round(24600.0 * scale, 2),
                "put_wall_strike": round(24500.0 * scale, 2),
                "planned_bias": "BEARISH_BELOW_TRIGGER",
                "bull_trigger": round(24615.0 * scale, 2),
                "bear_trigger": round(24540.0 * scale, 2),
                "max_trades": 2,
                "pre_plan_notes": "Prev Day PCR 1.54 is extreme overbought! Do NOT chase gap-up CE; wait for VWAP/24540 breakdown to buy ATM PE.",
                "post_market_notes": "PCR 1.54 reversal worked textbook — market rejected 24590 at open and dropped to 24465.",
            },
        )
        self.demo_store.conn.execute(
            """
            UPDATE daily_pre_market_plans
            SET actual_open = ?, actual_high = ?, actual_low = ?, actual_close = ?,
                actual_trades_count = 1, actual_pnl_rupees = 2470.0,
                plan_match_status = 'PLAN ALIGNED (100% Discipline)',
                market_vs_plan_detail = '🎯 High Prev PCR (1.54) Reversal Played Out (Spot fell -115.0 pts from Open) | 🔻 Bear Trigger CROSSED'
            WHERE session_date = ? AND underlying = ?
            """,
            (
                round(24585.0 * scale, 2),
                round(24592.0 * scale, 2),
                round(24460.0 * scale, 2),
                round(24470.0 * scale, 2),
                prev_date,
                underlying,
            ),
        )
        self.demo_store.conn.commit()

        # Seed Today's session (Example of VIX 14.5 Goldilocks Option Buying + GIFT Nifty +22 Bullish Continuation)
        save_pre_market_plan(
            store=self.demo_store,
            plan_input={
                "session_date": demo_date,
                "underlying": underlying,
                "pdh": round(24520.0 * scale, 2),
                "pdl": round(24390.0 * scale, 2),
                "pdc": round(24470.0 * scale, 2),
                "pre_open_spot": round(24492.0 * scale, 2),
                "gift_nifty_gap": round(22.0 * scale, 2),
                "global_sentiment": "MILD_BULLISH",
                "asian_markets": "POSITIVE_MOMENTUM",
                "prev_day_pcr": 1.18,
                "india_vix": 14.5,
                "fii_flow": "FII_NET_LONG",
                "brent_crude": "COOLING_BULLISH",
                "dxy_usdinr": "COOLING_INR_STRONG",
                "preopen_adv_dec": "MODERATE_ADVANCES",
                "event_context": "NORMAL_DAY",
                "call_wall_strike": round(24500.0 * scale, 2),
                "put_wall_strike": round(24400.0 * scale, 2),
                "planned_bias": "BULLISH_ABOVE_TRIGGER",
                "bull_trigger": round(24510.0 * scale, 2),
                "bear_trigger": round(24440.0 * scale, 2),
                "max_trades": 2,
                "pre_plan_notes": f"GIFT Nifty +{int(22*scale)}, US/Asia Positive, Brent & DXY Cooling, VIX 14.5 (14-16 Goldilocks Zone), Prev PCR 1.18 -> Buy ATM {int(24500 * scale)} CE above {int(24510 * scale)}.",
                "post_market_notes": "Waited for 6/6 confirmation before entering.",
            },
        )
        self.demo_step_idx = 0
        self.last_report = None
        self.last_whatsapp_result = None

    def _build_extended_demo(self, underlying: str) -> List[Any]:
        """Build a 5-stage interactive practice scenario (3-min NSE OI intervals)."""
        base_steps = list(generate_demo_snapshots(underlying))
        base_ts = base_steps[-1][0]
        expiry = base_steps[0][1]["expiry_date"]
        strikes = [r["strike"] for r in base_steps[0][1]["chain"]]

        # Scale strikes if BANKNIFTY is selected in demo
        scale = 2.0 if underlying == "BANKNIFTY" else 1.0
        if scale != 1.0:
            strikes = [s * scale for s in strikes]
            for _, c_resp, s_resp in base_steps:
                c_resp["underlying_ltp"] = round(c_resp["underlying_ltp"] * scale, 2)
                c_resp["atm_strike"] = c_resp["atm_strike"] * scale
                s_resp["underlying_ltp"] = c_resp["underlying_ltp"]
                s_resp["synthetic_future_price"] = round(s_resp["synthetic_future_price"] * scale, 2)
                s_resp["atm_strike"] = c_resp["atm_strike"]
                for row in c_resp["chain"]:
                    row["strike"] = row["strike"] * scale
                    row["ce"]["symbol"] = f"{underlying}{expiry}{int(row['strike'])}CE"
                    row["pe"]["symbol"] = f"{underlying}{expiry}{int(row['strike'])}PE"
                    row["ce"]["lotsize"] = 30
                    row["pe"]["lotsize"] = 30

        # Step 4 (+180s = 3 mins): Follow-through rally (Target 1 achieved on 24500 CE!)
        step4_chain = json.loads(json.dumps(base_steps[-1][1]))
        step4_synth = json.loads(json.dumps(base_steps[-1][2]))
        step4_ts = base_ts + 180
        step4_chain["underlying_ltp"] = round(24572.0 * scale, 2)
        step4_synth["underlying_ltp"] = step4_chain["underlying_ltp"]
        step4_synth["synthetic_future_price"] = round(24581.0 * scale, 2)
        ce_ltps_4 = [226.0, 188.0, 159.5, 122.0, 91.0]
        pe_ltps_4 = [32.0, 43.0, 58.0, 79.0, 106.0]
        for i, row in enumerate(step4_chain["chain"]):
            row["ce"]["ltp"] = ce_ltps_4[i]
            row["pe"]["ltp"] = pe_ltps_4[i]
            row["ce"]["oi"] = max(500000, row["ce"]["oi"] - 180000)
            row["pe"]["oi"] = row["pe"]["oi"] + 320000
            row["ce"]["volume"] = row["ce"]["volume"] + 650000
            row["ce"]["implied_volatility"] = round(row["ce"]["implied_volatility"] + 0.4, 2)

        # Step 5 (+360s = 6 mins): Mid-day Sideways Theta Trap (Straddle decays while both CE and PE OI increase)
        step5_chain = json.loads(json.dumps(base_steps[0][1]))
        step5_synth = json.loads(json.dumps(base_steps[0][2]))
        step5_ts = base_ts + 360
        step5_chain["underlying_ltp"] = round(24501.0 * scale, 2)
        step5_synth["underlying_ltp"] = step5_chain["underlying_ltp"]
        step5_synth["synthetic_future_price"] = round(24502.0 * scale, 2)
        ce_ltps_5 = [158.0, 125.0, 96.0, 71.0, 50.0]
        pe_ltps_5 = [52.0, 69.0, 91.0, 118.0, 151.0]
        for i, row in enumerate(step5_chain["chain"]):
            row["ce"]["ltp"] = ce_ltps_5[i]
            row["pe"]["ltp"] = pe_ltps_5[i]
            row["ce"]["oi"] = base_steps[0][1]["chain"][i]["ce"]["oi"] + 650000
            row["pe"]["oi"] = base_steps[0][1]["chain"][i]["pe"]["oi"] + 640000
            row["ce"]["volume"] = step4_chain["chain"][i]["ce"]["volume"] + 90000
            row["pe"]["volume"] = step4_chain["chain"][i]["pe"]["volume"] + 90000
            row["ce"]["implied_volatility"] = 12.1
            row["pe"]["implied_volatility"] = 12.3

        base_steps.append((step4_ts, step4_chain, step4_synth))
        base_steps.append((step5_ts, step5_chain, step5_synth))
        return base_steps

    def get_active_store(self) -> SnapshotStore:
        return self.demo_store if self.mode == "DEMO" else self.live_store

    def step_or_poll(self, advance_demo: bool = False) -> Dict[str, Any]:
        """Fetch latest snapshot from OpenAlgo or advance demo scenario."""
        with self.lock:
            self.last_error = None
            self.last_eval_epoch = time.time()

            if self.mode == "DEMO":
                self.eval_cycle_count += 1
                self.last_eval_wall_time = dt.datetime.now().strftime("%H:%M:%S")
                if self.last_report is None:
                    ts, c_resp, s_resp = self.demo_scenarios[0]
                    self.demo_step_idx = 0
                    self.last_report = analyze_option_chain(
                        store=self.demo_store,
                        underlying=self.underlying,
                        expiry_date=c_resp["expiry_date"],
                        days_to_expiry=4,
                        chain_resp=json.loads(json.dumps(c_resp)),
                        synth_resp=json.loads(json.dumps(s_resp)),
                        now_ts=ts,
                        source_mode=f"DEMO_SIMULATOR (Step 1/{len(self.demo_scenarios)})",
                    )
                elif advance_demo:
                    self.demo_step_idx = (self.demo_step_idx + 1) % len(self.demo_scenarios)
                    if self.demo_step_idx == 0:
                        self._reset_demo(self.underlying)
                    ts, c_resp, s_resp = self.demo_scenarios[self.demo_step_idx]
                    self.last_report = analyze_option_chain(
                        store=self.demo_store,
                        underlying=self.underlying,
                        expiry_date=c_resp["expiry_date"],
                        days_to_expiry=4,
                        chain_resp=json.loads(json.dumps(c_resp)),
                        synth_resp=json.loads(json.dumps(s_resp)),
                        now_ts=ts,
                        source_mode=f"DEMO_SIMULATOR (Step {self.demo_step_idx + 1}/{len(self.demo_scenarios)})",
                    )
                else:
                    self.last_report["eval_log"] = log_evaluation_trace_offline(
                        self.last_report,
                        source_mode=f"DEMO_SIMULATOR_RE_EVAL (Step {self.demo_step_idx + 1}/{len(self.demo_scenarios)})",
                    )
                self._update_open_paper_trades(self.demo_store, self.last_report)
                self._check_auto_whatsapp(self.demo_store, self.last_report)
                return self._serialize_state(self.demo_store)

            # LIVE_OPENALGO mode
            is_open, mkt_reason = check_indian_market_hours()
            if not is_open and self.last_report is not None:
                self.last_error = f"{mkt_reason} — Live auto-polling & offline logging paused after 15:30 IST so frozen closing quotes don't dilute your journal."
                return self._serialize_state(self.live_store, log_to_console=False)

            self.eval_cycle_count += 1
            self.last_eval_wall_time = dt.datetime.now().strftime("%H:%M:%S")

            try:
                gateway = OpenAlgoGateway(host=self.host, api_key=self.api_key)
                status_resp = gateway.analyzer_status()
                self.analyze_mode = bool((status_resp.get("data") or {}).get("analyze_mode", False))

                nfo_exch = "BFO" if self.underlying == "SENSEX" else "NFO"
                expiry_date, days_to_expiry = gateway.find_nearest_expiry(
                    self.underlying, exchange=nfo_exch
                )
                chain_resp = gateway.fetch_option_chain(
                    underlying=self.underlying,
                    expiry_date=expiry_date,
                    exchange=self.exchange,
                    strike_count=self.strike_count,
                    with_greeks=True,
                )
                synth_resp = gateway.fetch_synthetic_future(
                    underlying=self.underlying,
                    expiry_date=expiry_date,
                    exchange=self.exchange,
                )
                self.last_report = analyze_option_chain(
                    store=self.live_store,
                    underlying=self.underlying,
                    expiry_date=expiry_date,
                    days_to_expiry=days_to_expiry,
                    chain_resp=chain_resp,
                    synth_resp=synth_resp,
                    source_mode=f"LIVE_OPENALGO ({self.host})",
                )
                self._update_open_paper_trades(self.live_store, self.last_report)
                self._check_auto_whatsapp(self.live_store, self.last_report)
                if not is_open:
                    self.last_error = f"{mkt_reason} — Loaded closing snapshot once; 3m auto-polling paused until 09:15 AM."
            except Exception as exc:
                self.last_error = str(exc)
                if self.last_report is None:
                    self.demo_step_idx = 0
                elif advance_demo:
                    self.demo_step_idx = (self.demo_step_idx + 1) % len(self.demo_scenarios)
                    if self.demo_step_idx == 0:
                        self._reset_demo(self.underlying)
                ts, c_resp, s_resp = self.demo_scenarios[self.demo_step_idx]
                self.last_report = analyze_option_chain(
                    store=self.demo_store,
                    underlying=self.underlying,
                    expiry_date=c_resp["expiry_date"],
                    days_to_expiry=4,
                    chain_resp=json.loads(json.dumps(c_resp)),
                    synth_resp=json.loads(json.dumps(s_resp)),
                    now_ts=ts,
                    source_mode=f"FALLBACK_DEMO_SIMULATOR (Step {self.demo_step_idx + 1}/{len(self.demo_scenarios)} — OpenAlgo Offline)",
                )
                self._update_open_paper_trades(self.demo_store, self.last_report)
            return self._serialize_state(self.get_active_store())

    def _check_auto_whatsapp(
        self, store: SnapshotStore, report: Optional[Dict[str, Any]]
    ) -> None:
        if not report:
            return
        sig = report.get("signals") or {}
        if sig.get("action") in ("BUY_ATM_CE", "BUY_ATM_PE"):
            notifier = WhatsAppNotifier(store)
            self.last_whatsapp_result = notifier.notify_setup(report, force=False)

    def send_manual_whatsapp(self) -> Dict[str, Any]:
        if not self.last_report:
            self.step_or_poll(advance_demo=False)
        store = self.get_active_store()
        notifier = WhatsAppNotifier(store)
        assert self.last_report is not None
        self.last_whatsapp_result = notifier.notify_setup(self.last_report, force=True)
        return self._serialize_state(store)

    def _update_open_paper_trades(
        self, store: SnapshotStore, report: Optional[Dict[str, Any]]
    ) -> None:
        """Update MTM PnL and auto-trigger SL / Target / 15-Min Anti-Theta Time Stop on open trades."""
        if not report:
            return
        cur = store.conn.cursor()
        cur.execute("SELECT * FROM paper_trades WHERE status = 'OPEN' ORDER BY id DESC")
        open_trades = cur.fetchall()
        if not open_trades:
            return

        # Map symbol -> current LTP
        ltp_map: Dict[str, float] = {}
        for row in report.get("strikes", []):
            for k in ("ce", "pe"):
                leg = row.get(k) or {}
                if leg.get("symbol"):
                    ltp_map[leg["symbol"]] = float(leg.get("ltp") or 0.0)

        now_ts = int(report["ts"])
        for t in open_trades:
            sym = t["symbol"]
            if sym not in ltp_map:
                continue
            cur_ltp = ltp_map[sym]
            entry_price = float(t["entry_price"])
            qty = int(t["quantity"])
            pnl_pts = round(cur_ltp - entry_price, 2)
            pnl_rs = round(pnl_pts * qty, 2)
            held_mins = max(0.0, (now_ts - int(t["entry_ts"])) / 60.0)

            exit_reason = None
            if cur_ltp <= float(t["stop_loss"]):
                exit_reason = "HARD_STOP_LOSS (-18%)"
            elif cur_ltp >= float(t["target_2"]):
                exit_reason = "TARGET_2_HIT (+45%)"
            elif cur_ltp >= float(t["target_1"]):
                exit_reason = "TARGET_1_HIT (+25%)"
            elif held_mins >= 15.0 and cur_ltp < entry_price * 1.05:
                exit_reason = "THETA_TIME_STOP (15m < +5%)"

            if exit_reason:
                cur.execute(
                    """
                    UPDATE paper_trades
                    SET exit_ts = ?, exit_price = ?, pnl_points = ?, pnl_rupees = ?,
                        status = 'CLOSED', exit_reason = ?
                    WHERE id = ?
                    """,
                    (now_ts, cur_ltp, pnl_pts, pnl_rs, exit_reason, t["id"]),
                )
            else:
                cur.execute(
                    """
                    UPDATE paper_trades
                    SET exit_price = ?, pnl_points = ?, pnl_rupees = ?
                    WHERE id = ?
                    """,
                    (cur_ltp, pnl_pts, pnl_rs, t["id"]),
                )
        store.conn.commit()
        report["journal"] = update_and_write_setup_journal(store, report, min_score=3)

    def save_pre_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update the daily Pre-Market Plan and Post-Market Reflection notes, and re-verify deviation."""
        if not self.last_report:
            self.step_or_poll(advance_demo=False)
        store = self.get_active_store()
        save_pre_market_plan(store, payload, self.last_report)
        if self.last_report:
            self.last_report["journal"] = update_and_write_setup_journal(
                store, self.last_report, min_score=3
            )
        return self._serialize_state(store)

    def create_paper_trade(self, option_type: str, offset: str = "ATM") -> Dict[str, Any]:
        """Place a paper trade (and route to OpenAlgo if in LIVE_OPENALGO + Analyze Mode)."""
        if not self.last_report:
            self.step_or_poll(advance_demo=False)
        report = self.last_report
        assert report is not None

        atm_strike = float(report["atm_strike"])
        selected_leg = None
        for r in report["strikes"]:
            if abs(float(r["strike"]) - atm_strike) < 0.01:
                selected_leg = r["ce"] if option_type.upper() == "CE" else r["pe"]
                break
        if not selected_leg:
            raise RuntimeError("ATM leg not found in current chain.")

        entry_ltp = float(selected_leg.get("ltp") or 0.0)
        lotsize = int(selected_leg.get("lotsize") or 65)
        symbol = str(selected_leg.get("symbol") or f"{self.underlying}_{option_type}")
        sl = round(entry_ltp * 0.82, 2)
        t1 = round(entry_ltp * 1.25, 2)
        t2 = round(entry_ltp * 1.45, 2)

        openalgo_order_id = "SIM-LOCAL"
        if self.mode == "LIVE_OPENALGO" and self.api_key:
            gateway = OpenAlgoGateway(host=self.host, api_key=self.api_key)
            status_resp = gateway.analyzer_status()
            is_analyze = bool((status_resp.get("data") or {}).get("analyze_mode", False))
            if not is_analyze:
                raise RuntimeError(
                    "OpenAlgo is in LIVE mode! Switch OpenAlgo to Analyze Mode first before placing practice orders."
                )
            resp = gateway.place_options_order(
                underlying=self.underlying,
                expiry_date=report["expiry_date"],
                offset=offset,
                option_type=option_type.upper(),
                action="BUY",
                quantity=lotsize,
                exchange=self.exchange,
                product="NRML",
            )
            openalgo_order_id = str(resp.get("orderid") or "OPENALGO-SIM")

        store = self.get_active_store()
        cur = store.conn.cursor()
        cur.execute(
            """
            INSERT INTO paper_trades
            (entry_ts, session_date, underlying, expiry_date, symbol, offset_label,
             option_type, quantity, entry_price, stop_loss, target_1, target_2,
             exit_price, pnl_points, pnl_rupees, status, openalgo_order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0.0, 0.0, 'OPEN', ?)
            """,
            (
                int(report["ts"]),
                report["session_date"],
                self.underlying,
                report["expiry_date"],
                symbol,
                offset,
                option_type.upper(),
                lotsize,
                entry_ltp,
                sl,
                t1,
                t2,
                entry_ltp,
                openalgo_order_id,
            ),
        )
        store.conn.commit()
        report["journal"] = update_and_write_setup_journal(store, report, min_score=3)
        return self._serialize_state(store)

    def close_paper_trade(self, trade_id: int) -> Dict[str, Any]:
        store = self.get_active_store()
        cur = store.conn.cursor()
        now_ts = int(self.last_report["ts"]) if self.last_report else int(time.time())
        cur.execute(
            """
            UPDATE paper_trades
            SET status = 'CLOSED', exit_ts = ?, exit_reason = 'MANUAL_SQUARE_OFF'
            WHERE id = ? AND status = 'OPEN'
            """,
            (now_ts, trade_id),
        )
        store.conn.commit()
        if self.last_report:
            self.last_report["journal"] = update_and_write_setup_journal(
                store, self.last_report, min_score=3
            )
        return self._serialize_state(store)

    def _build_evaluation_trace(self, report: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a transparent step-by-step evaluation log trace showing inputs considered, conditions met, and missing conditions."""
        if not report:
            return {
                "cycle_id": self.eval_cycle_count,
                "wall_time": self.last_eval_wall_time or dt.datetime.now().strftime("%H:%M:%S"),
                "status": "WAITING_FOR_SNAPSHOT",
            }

        atm_strike = float(report.get("atm_strike") or 0.0)
        atm_ce: Dict[str, Any] = {}
        atm_pe: Dict[str, Any] = {}
        for r in report.get("strikes", []):
            if abs(float(r.get("strike") or 0.0) - atm_strike) < 0.01:
                atm_ce = r.get("ce") or {}
                atm_pe = r.get("pe") or {}
                break

        sig = report.get("signals") or {}
        ce_checks = sig.get("ce_checks") or []
        pe_checks = sig.get("pe_checks") or []

        ce_passed = [{"rule": c[0], "detail": c[2]} for c in ce_checks if c[1]]
        ce_missing = [{"rule": c[0], "detail": c[2]} for c in ce_checks if not c[1]]
        pe_passed = [{"rule": c[0], "detail": c[2]} for c in pe_checks if c[1]]
        pe_missing = [{"rule": c[0], "detail": c[2]} for c in pe_checks if not c[1]]

        ce_score = int(sig.get("ce_score") or 0)
        pe_score = int(sig.get("pe_score") or 0)
        action = str(sig.get("action") or "WAIT")

        source_desc = (
            f"DEMO SIMULATOR (Snapshot {self.demo_step_idx + 1}/{len(self.demo_scenarios)})"
            if self.mode == "DEMO"
            else f"LIVE OPENALGO ({self.host})"
        )

        spot_ltp = float(report.get("spot_ltp") or 0.0)
        spot_vwap = float(report.get("spot_vwap") or 0.0)
        basis = report.get("basis")
        basis_str = f"{basis:+.2f}" if basis is not None else "N/A"
        synth_str = f"{report['synthetic_future']:.2f}" if report.get("synthetic_future") else "N/A"

        inputs = {
            "source_desc": source_desc,
            "underlying": report.get("underlying"),
            "expiry_date": report.get("expiry_date"),
            "days_to_expiry": report.get("days_to_expiry"),
            "snapshot_time": report.get("timestamp_str"),
            "snapshots_today": report.get("snapshots_count_today", 1),
            "spot_and_basis": (
                f"Spot LTP: {spot_ltp:,.2f} vs Session VWAP: {spot_vwap:,.2f} (Diff: {spot_ltp - spot_vwap:+.2f}) | "
                f"Synthetic Future: {synth_str} (Carry Basis: {basis_str})"
            ),
            "straddle_and_vol": (
                f"ATM {int(atm_strike)} Straddle LTP: ₹{float(report.get('atm_straddle_ltp') or 0):,.2f} vs "
                f"Open Straddle: ₹{float(report.get('opening_straddle') or 0):,.2f} ({float(report.get('straddle_change_pct') or 0):+.2f}%)"
            ),
            "oi_and_pcr": (
                f"Near-ATM PCR: {float(report.get('overall_pcr') or 0):.2f} | "
                f"15m PE dOI: {int(report.get('near_pe_doi_15m') or 0):+,} vs 15m CE dOI: {int(report.get('near_ce_doi_15m') or 0):+,} | "
                f"OI Walls: {int(report.get('support_strike') or 0)} PE (Sup) / {int(report.get('resistance_strike') or 0)} CE (Res)"
            ),
            "atm_ce_contract": (
                f"{atm_ce.get('symbol', 'ATM_CE')}: LTP ₹{float(atm_ce.get('ltp') or 0):.2f} vs Option VWAP ₹{float(atm_ce.get('vwap') or 0):.2f} "
                f"(3m dLTP {float(atm_ce.get('dltp_3m') or 0):+.2f}) | Quadrant: {atm_ce.get('quadrant', 'NEUTRAL')} "
                f"(3m dOI {int(atm_ce.get('doi_3m') or 0):+,}) | Vol Burst: {float(atm_ce.get('vol_burst_ratio') or 0):.2f}x "
                f"(BidQty {int(atm_ce.get('bid_qty') or 0)} vs AskQty {int(atm_ce.get('ask_qty') or 0)}) | "
                f"IV: {float(atm_ce.get('implied_volatility') or 0):.1f}% (3m dIV {float(atm_ce.get('div_3m') or 0):+.2f}%) | "
                f"Delta: {float(atm_ce.get('delta') or 0):.2f} | Daily Theta Bleed: {float(atm_ce.get('theta_bleed_pct') or 0):.1f}%"
            ),
            "atm_pe_contract": (
                f"{atm_pe.get('symbol', 'ATM_PE')}: LTP ₹{float(atm_pe.get('ltp') or 0):.2f} vs Option VWAP ₹{float(atm_pe.get('vwap') or 0):.2f} "
                f"(3m dLTP {float(atm_pe.get('dltp_3m') or 0):+.2f}) | Quadrant: {atm_pe.get('quadrant', 'NEUTRAL')} "
                f"(3m dOI {int(atm_pe.get('doi_3m') or 0):+,}) | Vol Burst: {float(atm_pe.get('vol_burst_ratio') or 0):.2f}x "
                f"(BidQty {int(atm_pe.get('bid_qty') or 0)} vs AskQty {int(atm_pe.get('ask_qty') or 0)}) | "
                f"IV: {float(atm_pe.get('implied_volatility') or 0):.1f}% (3m dIV {float(atm_pe.get('div_3m') or 0):+.2f}%) | "
                f"|Delta|: {abs(float(atm_pe.get('delta') or 0)):.2f} | Daily Theta Bleed: {float(atm_pe.get('theta_bleed_pct') or 0):.1f}%"
            ),
        }

        if ce_score >= 3 or pe_score >= 3:
            journal_note = (
                f"Logged to Setup Journal (CE {ce_score}/6, PE {pe_score}/6 met >= 3/6 threshold) -> doc/TRADING_JOURNAL.md"
            )
        else:
            journal_note = (
                f"Not logged to Setup Journal yet (CE {ce_score}/6, PE {pe_score}/6 both < 3/6 threshold)"
            )

        return {
            "cycle_id": self.eval_cycle_count,
            "wall_time": self.last_eval_wall_time or dt.datetime.now().strftime("%H:%M:%S"),
            "status": "EVALUATED",
            "inputs": inputs,
            "ce_eval": {
                "symbol": atm_ce.get("symbol", f"{int(atm_strike)}CE"),
                "score": ce_score,
                "passed": ce_passed,
                "missing": ce_missing,
            },
            "pe_eval": {
                "symbol": atm_pe.get("symbol", f"{int(atm_strike)}PE"),
                "score": pe_score,
                "passed": pe_passed,
                "missing": pe_missing,
            },
            "verdict": {
                "action": action,
                "journal_note": journal_note,
            },
            "offline_log": report.get("eval_log") or {},
        }

    def _serialize_state(self, store: SnapshotStore, log_to_console: bool = True) -> Dict[str, Any]:
        cur = store.conn.cursor()
        cur.execute(
            """
            SELECT ts, spot_ltp, atm_straddle_ltp, basis
            FROM chain_snapshots
            WHERE underlying = ?
            ORDER BY ts DESC LIMIT 30
            """,
            (self.underlying,),
        )
        history = [dict(r) for r in reversed(cur.fetchall())]

        cur.execute("SELECT * FROM paper_trades ORDER BY id DESC LIMIT 20")
        trades = [dict(r) for r in cur.fetchall()]

        wa_preview = (
            format_whatsapp_setup_message(self.last_report)
            if self.last_report
            else "Waiting for Option Chain snapshot..."
        )
        notifier = WhatsAppNotifier(store)
        eval_trace = self._build_evaluation_trace(self.last_report)
        if log_to_console and eval_trace.get("status") == "EVALUATED":
            ce_eval = eval_trace.get("ce_eval") or {}
            pe_eval = eval_trace.get("pe_eval") or {}
            v_info = eval_trace.get("verdict") or {}
            inp = eval_trace.get("inputs") or {}
            print(
                f"  [EVAL #{eval_trace.get('cycle_id')} @ {eval_trace.get('wall_time')}] "
                f"{inp.get('source_desc')} | {inp.get('spot_and_basis')} | "
                f"CE Score={ce_eval.get('score', 0)}/6 | PE Score={pe_eval.get('score', 0)}/6 | "
                f"Verdict={v_info.get('action')}"
            )

        is_open, mkt_reason = check_indian_market_hours()
        return {
            "mode": self.mode,
            "host": self.host,
            "has_api_key": bool(self.api_key),
            "analyze_mode": self.analyze_mode,
            "underlying": self.underlying,
            "market_open": is_open,
            "market_reason": mkt_reason,
            "demo_step": self.demo_step_idx + 1,
            "demo_total_steps": len(self.demo_scenarios),
            "error": self.last_error,
            "report": self.last_report,
            "eval_trace": eval_trace,
            "history": history,
            "trades": trades,
            "whatsapp": {
                "configured": notifier.is_configured(),
                "enabled": notifier.enabled,
                "provider": notifier.provider,
                "phone": notifier.gmail_user if notifier.provider == "gmail" else notifier.phone,
                "preview": wa_preview,
                "last_result": self.last_whatsapp_result,
            },
        }


APP_STATE = AnalyzerAppState()


# ---------------------------------------------------------------------------
# Embedded Single-Page Trading Desk UI (HTML + CSS + Vanilla JS)
# ---------------------------------------------------------------------------

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LearnOT — OpenAlgo Option Buying Desk (Nifty / BankNifty)</title>
  <style>
    :root {
      --bg: #0b0f19;
      --panel: #111827;
      --panel-alt: #1e293b;
      --border: #26334d;
      --text: #f1f5f9;
      --muted: #94a3b8;
      --green: #10b981;
      --green-bg: rgba(16, 185, 129, 0.14);
      --red: #f43f5e;
      --red-bg: rgba(244, 63, 94, 0.14);
      --cyan: #06b6d4;
      --cyan-bg: rgba(6, 182, 212, 0.16);
      --amber: #f59e0b;
      --amber-bg: rgba(245, 158, 11, 0.15);
      --blue: #3b82f6;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      font-size: 13px;
      line-height: 1.45;
      padding-bottom: 40px;
    }
    /* Top Navbar */
    .topbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 20px;
      background: #0f172a;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 16px;
      letter-spacing: -0.02em;
    }
    .badge {
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
    }
    .badge-sim { background: var(--cyan-bg); color: #22d3ee; border: 1px solid rgba(34,211,238,0.35); }
    .badge-live { background: var(--red-bg); color: #fb7185; border: 1px solid rgba(251,113,133,0.35); }
    .badge-demo { background: var(--amber-bg); color: #fbbf24; border: 1px solid rgba(251,191,36,0.35); }

    .controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }
    select, input, button {
      background: var(--panel-alt);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 12px;
      outline: none;
    }
    button {
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s ease;
    }
    button:hover { border-color: #475569; background: #283548; }
    .btn-primary { background: var(--blue); border-color: #2563eb; color: #fff; }
    .btn-primary:hover { background: #2563eb; }
    .btn-green { background: var(--green); border-color: #059669; color: #052e16; }
    .btn-green:hover { background: #059669; color: #fff; }
    .btn-red { background: var(--red); border-color: #e11d48; color: #fff; }
    .btn-amber { background: var(--amber); border-color: #d97706; color: #1e1b4b; }

    .container { max-width: 1560px; margin: 0 auto; padding: 16px 20px; }

    /* Error / Info Banner */
    .alert-banner {
      background: var(--red-bg);
      border: 1px solid var(--red);
      color: #fecdd3;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 14px;
      display: none;
    }

    /* KPI Strip */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .kpi-card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
    }
    .kpi-label { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
    .kpi-value { font-size: 20px; font-weight: 700; margin-top: 4px; font-variant-numeric: tabular-nums; }
    .kpi-sub { font-size: 12px; color: var(--muted); margin-top: 3px; font-variant-numeric: tabular-nums; }

    /* Signal Action Banner */
    .signal-banner {
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      border: 1px solid var(--border);
      background: var(--panel);
    }
    .signal-buy-ce { background: linear-gradient(90deg, rgba(16,185,129,0.18), rgba(17,24,39,0.95)); border-color: var(--green); }
    .signal-buy-pe { background: linear-gradient(90deg, rgba(244,63,94,0.18), rgba(17,24,39,0.95)); border-color: var(--red); }
    .signal-trap { background: linear-gradient(90deg, rgba(245,158,11,0.18), rgba(17,24,39,0.95)); border-color: var(--amber); }

    .signal-title { font-size: 16px; font-weight: 800; }
    .signal-meta { color: #cbd5e1; font-size: 12.5px; margin-top: 4px; }

    /* Main 2-Column Layout for Checklists & Visual Charts */
    .mid-grid {
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }
    @media (max-width: 1100px) { .mid-grid { grid-template-columns: 1fr; } }

    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
    }
    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
      margin-bottom: 12px;
      font-weight: 700;
      font-size: 14px;
    }

    .checklist-cols {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    @media (max-width: 768px) { .checklist-cols { grid-template-columns: 1fr; } }

    .check-box {
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
    }
    .check-item {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      padding: 6px 0;
      border-bottom: 1px dashed rgba(148, 163, 184, 0.15);
    }
    .check-item:last-child { border-bottom: none; }
    .pill-pass {
      background: var(--green-bg);
      color: #34d399;
      border: 1px solid rgba(52,211,153,0.35);
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      flex-shrink: 0;
      margin-top: 2px;
    }
    .pill-wait {
      background: rgba(148, 163, 184, 0.12);
      color: var(--muted);
      border: 1px solid rgba(148,163,184,0.2);
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      flex-shrink: 0;
      margin-top: 2px;
    }

    /* Option Chain Table */
    .table-wrap { overflow-x: auto; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-variant-numeric: tabular-nums;
      font-size: 12px;
    }
    th, td {
      padding: 8px 9px;
      border-bottom: 1px solid rgba(38, 51, 77, 0.7);
      text-align: right;
      white-space: nowrap;
    }
    th {
      background: #0f172a;
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 600;
    }
    td.strike-col, th.strike-col {
      text-align: center;
      font-weight: 800;
      background: #172033;
      color: #f8fafc;
      border-left: 1px solid var(--border);
      border-right: 1px solid var(--border);
    }
    tr.atm-row td { background: rgba(59, 130, 246, 0.09); }
    tr.atm-row td.strike-col { background: rgba(59, 130, 246, 0.28); color: #93c5fd; }

    .q-badge {
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      display: inline-block;
    }
    .q-SHORT_COVERING { background: var(--cyan-bg); color: #22d3ee; border: 1px solid rgba(34,211,238,0.4); }
    .q-LONG_BUILDUP { background: var(--green-bg); color: #34d399; }
    .q-SHORT_BUILDUP { background: var(--red-bg); color: #fb7185; }
    .q-LONG_UNWINDING { background: var(--amber-bg); color: #fbbf24; }
    .q-NEUTRAL { color: var(--muted); }

    /* Bar Chart inside OI */
    .oi-bars { display: flex; flex-direction: column; gap: 8px; }
    .oi-bar-row { display: grid; grid-template-columns: 1fr 64px 1fr; align-items: center; gap: 8px; font-size: 11px; }
    .bar-left-wrap { display: flex; justify-content: flex-end; align-items: center; gap: 6px; }
    .bar-right-wrap { display: flex; justify-content: flex-start; align-items: center; gap: 6px; }
    .bar-ce { height: 14px; background: linear-gradient(90deg, #f43f5e, #e11d48); border-radius: 3px; }
    .bar-pe { height: 14px; background: linear-gradient(90deg, #059669, #10b981); border-radius: 3px; }

    .pos-green { color: #34d399; }
    .neg-red { color: #fb7185; }
    .wa-pre {
      background: #09131c;
      border: 1px solid rgba(16,185,129,0.35);
      border-radius: 8px;
      padding: 10px 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 11.5px;
      white-space: pre-wrap;
      color: #d1fae5;
      max-height: 240px;
      overflow-y: auto;
    }
    /* Tab Switcher Bar */
    .tab-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 16px;
      padding: 8px 12px;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 10px;
    }
    .tab-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .tab-btn {
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--muted);
      cursor: pointer;
    }
    .tab-btn.active {
      background: linear-gradient(90deg, rgba(6,182,212,0.22), rgba(59,130,246,0.22));
      border-color: #22d3ee;
      color: #f8fafc;
      box-shadow: 0 0 12px rgba(6,182,212,0.2);
    }
    .guide-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }
    .guide-box {
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(51, 65, 85, 0.85);
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 11.5px;
    }
  </style>
</head>
<body>

  <!-- Top Navigation & OpenAlgo Controls -->
  <div class="topbar">
    <div class="brand">
      <span>⚡ LearnOT Option Buying Desk</span>
      <span id="modeBadge" class="badge badge-demo">DEMO SIMULATION</span>
      <span id="engineHeartbeatBadge" class="badge badge-sim" style="font-variant-numeric:tabular-nums;">🟢 ENGINE ACTIVE | Cycle #1</span>
    </div>

    <div class="controls">
      <label style="color:var(--muted)">Mode:</label>
      <select id="modeSelect" onchange="changeConfig()">
        <option value="DEMO">Practice Simulator (5-Stage Demo)</option>
        <option value="LIVE_OPENALGO">Live OpenAlgo (127.0.0.1:5000)</option>
      </select>

      <label style="color:var(--muted)">Index:</label>
      <select id="underlyingSelect" onchange="changeConfig()">
        <option value="NIFTY">NIFTY 50</option>
        <option value="BANKNIFTY">BANKNIFTY</option>
        <option value="SENSEX">SENSEX</option>
      </select>

      <input type="password" id="apiKeyInput" placeholder="OpenAlgo API Key (optional in Demo)" style="width:180px;" />
      <button onclick="saveApiKey()">Save Key</button>

      <button id="stepBtn" class="btn-amber" onclick="refreshData(true)">▶ Next Demo Snapshot (1/5)</button>
      <button class="btn-primary" onclick="refreshData(false)">↻ Evaluate Now</button>

      <select id="autoRefreshSelect" onchange="toggleAutoRefresh()">
        <option value="180" selected>Auto-Poll: 180s (3m NSE OI Cycle ★)</option>
        <option value="60">Auto-Poll: 60s</option>
        <option value="30">Auto-Poll: 30s</option>
        <option value="15">Auto-Step Demo: 15s</option>
        <option value="0">Auto-Poll: OFF</option>
      </select>
    </div>
  </div>

  <div class="container">
    <div id="errorBanner" class="alert-banner"></div>

    <!-- Dedicated Tab Switcher Bar -->
    <div class="tab-bar">
      <div class="tab-buttons">
        <button id="btnTabLive" class="tab-btn active" onclick="switchTab('LIVE')">
          ⚡ Tab 1: Live Option Buying Desk &amp; 6/6 Engine
        </button>
        <button id="btnTabPreMarket" class="tab-btn" onclick="switchTab('PREMARKET')">
          🌅 Tab 2: Pre-Market Sentiment Signal &amp; Deviation Portal (SGX/GIFT, Global, PCR, VIX)
        </button>
      </div>
      <div style="display:flex; align-items:center; gap:10px; font-size:12px;">
        <span style="color:var(--muted)">Today's Pre-Market Signal:</span>
        <span id="topBarPreSignal" class="badge badge-sim" style="cursor:pointer;" onclick="switchTab('PREMARKET')">Loading Signal...</span>
        <span id="prePlanStatusBadge" class="badge badge-demo" style="cursor:pointer;" onclick="switchTab('PREMARKET')">PENDING</span>
      </div>
    </div>

    <!-- ===================================================================== -->
    <!-- TAB 1: LIVE INTRADAY OPTION CHAIN & 6/6 GAMMA BLAST DESK              -->
    <!-- ===================================================================== -->
    <div id="tabLiveContent">
      <!-- KPI Cards -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Spot LTP vs Session VWAP</div>
          <div class="kpi-value" id="kpiSpot">--</div>
          <div class="kpi-sub" id="kpiSpotSub">Session VWAP: --</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">ATM Straddle (Theta vs Gamma)</div>
          <div class="kpi-value" id="kpiStraddle">--</div>
          <div class="kpi-sub" id="kpiStraddleSub">Open: -- | Change: --</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Near-ATM PCR & 15m dOI Battle</div>
          <div class="kpi-value" id="kpiPcr">--</div>
          <div class="kpi-sub" id="kpiDoiBattle">15m PE dOI: -- | CE dOI: --</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Institutional OI Walls</div>
          <div class="kpi-value" id="kpiWalls">--</div>
          <div class="kpi-sub" id="kpiWallsSub">Support (PE) vs Resistance (CE)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Synthetic Future & Carry Basis</div>
          <div class="kpi-value" id="kpiSynth">--</div>
          <div class="kpi-sub" id="kpiSynthSub">Put-Call Parity Fair Value</div>
        </div>
      </div>

      <!-- Action Signal Banner -->
      <div id="signalBanner" class="signal-banner">
        <div>
          <div class="signal-title" id="signalTitle">Evaluating 6-Point Gamma Blast Checklist...</div>
          <div class="signal-meta" id="signalMeta">Waiting for data snapshot...</div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
          <button class="btn-green" onclick="placePaperOrder('CE')">+ Practice Buy ATM CE</button>
          <button class="btn-red" onclick="placePaperOrder('PE')">+ Practice Buy ATM PE</button>
          <button class="btn-primary" onclick="sendWhatsAppNow()">📧 Send Setup Alert (Gmail)</button>
        </div>
      </div>

      <!-- =================================================================== -->
      <!-- LIVE OPTION CHAIN ANALYSIS & RULE EVALUATION LOG TRACER             -->
      <!-- =================================================================== -->
      <div class="card" style="margin-bottom:16px; border-color: rgba(6, 182, 212, 0.55); background: #0b1120;">
        <div class="card-header" style="border-bottom-color: rgba(34, 211, 238, 0.25);">
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <span style="color:#22d3ee;">🖥️ Live Option Chain Analysis &amp; Rule Evaluation Log Tracer</span>
            <span id="tracerStatusPill" class="badge badge-sim">ANALYSING...</span>
            <span id="tracerCountdownLabel" style="font-size:11.5px; color:var(--muted); font-variant-numeric:tabular-nums;">Next Poll: --</span>
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; font-size:12px;">
            <label style="display:flex; align-items:center; gap:5px; cursor:pointer; color:#cbd5e1; font-weight:500;">
              <input type="checkbox" id="chkClearEachCycle" checked />
              Clear Log on Each Evaluation Cycle
            </label>
            <button type="button" onclick="clearLogTracer()">🧹 Clear Log</button>
            <button type="button" onclick="window.open('/api/download_eval_log?format=log', '_blank')" title="Download persistent human-readable evaluation trace (.log) for offline analysis">📥 Offline Log (.log)</button>
            <button type="button" onclick="window.open('/api/download_eval_log?format=csv', '_blank')" title="Download tabular evaluation log (.csv) for Excel / Pandas offline analysis">📊 Offline CSV (.csv)</button>
            <button type="button" class="btn-amber" onclick="refreshData(true)">▶ Step Next Demo Snapshot</button>
            <button type="button" class="btn-primary" onclick="refreshData(false)">↻ Re-Evaluate Option Chain Now</button>
          </div>
        </div>
        <div id="logTracerContainer" style="font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; line-height: 1.5; max-height: 360px; overflow-y: auto; padding: 4px 2px;">
          Initializing Option Chain Analyzer Log Tracer...
        </div>
      </div>

      <!-- Middle Grid: 6-Point Checklists & OI Wall Chart + Gmail/Alert Preview -->
      <div class="mid-grid">
        <div class="card">
          <div class="card-header">
            <span>6-Point "Trapped Seller Gamma Blast" Mechanical Checklist (3-Min NSE OI Cycle)</span>
            <span id="scoreSummary" style="color:var(--muted); font-size:12px;">CE: 0/6 | PE: 0/6</span>
          </div>
          <div class="checklist-cols">
            <div class="check-box">
              <div style="font-weight:700; color:#34d399; margin-bottom:6px;" id="ceBoxTitle">Bullish ATM CE Setup (0/6)</div>
              <div id="ceCheckList"></div>
            </div>
            <div class="check-box">
              <div style="font-weight:700; color:#fb7185; margin-bottom:6px;" id="peBoxTitle">Bearish ATM PE Setup (0/6)</div>
              <div id="peCheckList"></div>
            </div>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:16px;">
          <div class="card">
            <div class="card-header">
              <span>Strike OI Walls & 3-Min Change in OI (3m dOI)</span>
              <span style="font-size:11px; color:var(--muted);">Red = Call Resistance | Green = Put Support</span>
            </div>
            <div id="oiBarsContainer" class="oi-bars"></div>
          </div>

          <div class="card">
            <div class="card-header">
              <span>📧 Gmail / Instant Setup Auto-Alert (Fires on 6/6 Setup)</span>
              <span id="waStatusBadge" class="badge badge-demo">PREVIEW MODE</span>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
              <select id="waProvider" style="width:140px;" onchange="updateAlertPlaceholders()">
                <option value="gmail" selected>Gmail (Official ★)</option>
                <option value="webhook">Custom Webhook</option>
                <option value="callmebot">CallMeBot</option>
                <option value="meta">Meta Cloud API</option>
              </select>
              <input type="text" id="waPhone" placeholder="your_email@gmail.com" style="width:165px;" />
              <input type="password" id="waKey" placeholder="16-char Google App Password" style="flex:1; min-width:150px;" />
              <button onclick="saveWhatsAppConfig()">Save Alert</button>
            </div>
            <div id="waPreviewBox" class="wa-pre">Loading setup alert message preview...</div>
          </div>
        </div>
      </div>

      <!-- Option Chain Table -->
      <div class="card" style="margin-bottom:16px;">
        <div class="card-header">
          <span id="chainHeaderTitle">Live Option Chain + Greeks + 4-Quadrant OI Matrix (3-Min NSE OI Cycle)</span>
          <span style="font-size:11px; color:var(--muted);">
            Cyan <b style="color:#22d3ee">SHORT_COVERING</b> = Trapped Option Sellers Panicking (Your #1 Buying Edge)
          </span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="text-align:left">CE Quadrant</th>
                <th>CE OI</th>
                <th>CE 3m dOI</th>
                <th>CE Vol Ratio</th>
                <th>CE IV</th>
                <th>CE Δ</th>
                <th>CE Θ</th>
                <th>CE VWAP</th>
                <th>CE LTP</th>
                <th class="strike-col">STRIKE</th>
                <th style="text-align:left">PE LTP</th>
                <th>PE VWAP</th>
                <th>PE Θ</th>
                <th>PE Δ</th>
                <th>PE IV</th>
                <th>PE Vol Ratio</th>
                <th>PE 3m dOI</th>
                <th>PE OI</th>
                <th style="text-align:left">PE Quadrant</th>
              </tr>
            </thead>
            <tbody id="chainTableBody"></tbody>
          </table>
        </div>
      </div>

      <!-- Setup & Fine-Tuning Journal (Score >= 3/6) -->
      <div class="card" style="margin-bottom:16px;">
        <div class="card-header">
          <span>📓 Setup &amp; Fine-Tuning Journal (Logs All Setups With &ge; 3/6 Conditions Met)</span>
          <span id="journalFileBadge" style="font-size:11px; color:#93c5fd;">Saved to: doc/TRADING_JOURNAL.md &amp; doc/trading_journal.csv</span>
        </div>
        <div id="journalBlockerBanner" style="padding:8px 12px; margin-bottom:10px; border-radius:6px; background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); font-size:12px; color:#e2e8f0;">
          Evaluating rule blockers (e.g., PCR, Volume Burst, VWAP)...
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="text-align:left">Time</th>
                <th style="text-align:left">Contract</th>
                <th>Side</th>
                <th>Score</th>
                <th>Entry LTP</th>
                <th>Max LTP After</th>
                <th>Max Gain %</th>
                <th style="text-align:left">Verdict (Outcome After Signal)</th>
                <th style="text-align:left">Missing Conditions (What Blocked 6/6)</th>
                <th style="text-align:left">Passed Conditions</th>
              </tr>
            </thead>
            <tbody id="journalTableBody"></tbody>
          </table>
        </div>
      </div>

      <!-- Practice / Paper Trades Log with 15-Minute Anti-Theta Timer -->
      <div class="card">
        <div class="card-header">
          <span>Practice & OpenAlgo Analyze-Mode Trade Log (With 15-Minute Anti-Theta Time-Stop)</span>
          <span style="font-size:11px; color:var(--muted);">Auto-exits at -18% SL, +25%/+45% Target, or after 15 mins if gain &lt; +5%</span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="text-align:left">ID</th>
                <th style="text-align:left">Symbol</th>
                <th>Type</th>
                <th>Qty</th>
                <th>Entry LTP</th>
                <th>Current / Exit</th>
                <th>Hard SL (-18%)</th>
                <th>Target 1 (+25%)</th>
                <th>Target 2 (+45%)</th>
                <th>PnL (Pts)</th>
                <th>PnL (₹)</th>
                <th>Status / Exit Reason</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="tradesTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ===================================================================== -->
    <!-- TAB 2: PRE-MARKET SENTIMENT SIGNAL & POST-MARKET DEVIATION PORTAL     -->
    <!-- ===================================================================== -->
    <div id="tabPreMarketContent" style="display:none;">

      <!-- 3-Stage Pre-Market Sentiment Checklist Reference Guide -->
      <div class="guide-grid" style="grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));">
        <div class="guide-box">
          <div style="font-weight:700; color:#22d3ee; margin-bottom:5px;">🌍 1. Global Indicators (Check 6:30 AM – 8:00 AM IST)</div>
          <div style="color:#cbd5e1; line-height:1.45;">
            • <b>GIFT Nifty (NSE IX):</b> Direct proxy for Nifty 50 opening. Positive/negative gap indicates gap-up or gap-down.<br/>
            • <b>US Market Closing:</b> Check S&amp;P 500, Nasdaq &amp; Dow Jones overnight close. Strong US rallies trigger positive sentiment.<br/>
            • <b>Asian Markets:</b> Early movements of <b>Nikkei 225</b> (Japan) &amp; <b>Hang Seng</b> (Hong Kong) set Asian intraday momentum.
          </div>
        </div>
        <div class="guide-box">
          <div style="font-weight:700; color:#fbbf24; margin-bottom:5px;">📊 2. Macroeconomic &amp; Institutional Triggers</div>
          <div style="color:#cbd5e1; line-height:1.45;">
            • <b>FII &amp; DII Activity:</b> Continuous FII selling signals weak sentiment; strong DII buying provides a cushion.<br/>
            • <b>Crude Oil (Brent Crude):</b> India imports &gt;80% of its oil. Spikes in Brent crude hurt inflation/margins (&rarr; Bearish).<br/>
            • <b>Dollar Index (DXY) &amp; USD/INR:</b> Rising DXY &amp; weakening Rupee (USD/INR) prompt FIIs to pull capital out of India.
          </div>
        </div>
        <div class="guide-box">
          <div style="font-weight:700; color:#34d399; margin-bottom:5px;">🇮🇳 3. Domestic Pre-Market Data (Check 9:00 AM – 9:08 AM IST)</div>
          <div style="color:#cbd5e1; line-height:1.45;">
            • <b>NSE/BSE Pre-Open (9:00–9:08 AM):</b> Order collection stops at <b>9:08 AM</b> (Equilibrium Price). Check <b>Advance-Decline Ratio</b>.<br/>
            • <b>India VIX (Volatility Index):</b> Sharp rise (&gt;19.5) = higher fear &amp; IV crush danger; <b>13.5–16.5 = Goldilocks Option Buying</b>; low VIX = stable confidence.<br/>
            • <b>Prev Day Closing PCR:</b> <b>&ge;1.45 Overbought</b> (Bearish reversal watch) | <b>&le;0.65 Oversold</b> (Bullish short-covering bounce).
          </div>
        </div>
      </div>

      <!-- Pre-Market Input & Signal Generator Card -->
      <div class="card" style="margin-bottom:16px; border-color: rgba(6, 182, 212, 0.55);">
        <div class="card-header">
          <span>🌅 Step 1: Complete Your Morning Pre-Market Sentiment Checklist (6:30 AM – 9:08 AM IST)</span>
          <div style="display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
            <button type="button" onclick="loadPresetScenario('HIGH_PCR_REVERSAL')" title="Test Prev Day PCR 1.54 Overbought Reversal">🧪 Preset: PCR 1.54 Reversal</button>
            <button type="button" onclick="loadPresetScenario('GOLDILOCKS_BULL')" title="Test VIX 14.5 Goldilocks Option Buying">🧪 Preset: VIX 14.5 Bullish</button>
            <button type="button" onclick="loadPresetScenario('HIGH_IV_NO_TRADE')" title="Test VIX 21.5 High IV No-Trade Day">🧪 Preset: High IV 21.5 No-Trade</button>
            <button type="button" onclick="autoFillPrePlan()">⚡ Auto-Fill From Chain</button>
            <button type="button" class="btn-primary" onclick="savePrePlan(false)">🧠 Evaluate 8-Point Checklist &amp; Save Plan</button>
          </div>
        </div>

        <!-- Stage 1 & Stage 2 Inputs -->
        <div style="font-size:11.5px; font-weight:700; color:#22d3ee; margin-bottom:6px; text-transform:uppercase;">
          🌍 Stage 1: Global Indicators (6:30–8:00 AM IST) &amp; 📊 Stage 2: Macroeconomic &amp; Institutional Triggers
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(195px, 1fr)); gap:10px; margin-bottom:14px;">
          <div>
            <label style="font-size:11px; color:#22d3ee; font-weight:600; display:block; margin-bottom:3px;">1. GIFT Nifty Gap (NSE IX Pts)</label>
            <input type="number" step="1" id="ppGiftGap" placeholder="e.g. +35 or -60" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:#22d3ee; font-weight:600; display:block; margin-bottom:3px;">2. US Market Close (S&amp;P / Nasdaq / Dow)</label>
            <select id="ppGlobal" style="width:100%;">
              <option value="STRONG_BULLISH">STRONG_BULLISH (US Rally +1%+)</option>
              <option value="MILD_BULLISH">MILD_BULLISH (Positive US Close)</option>
              <option value="NEUTRAL_MIXED">NEUTRAL_MIXED (Flat / Mixed US)</option>
              <option value="MILD_BEARISH">MILD_BEARISH (Negative US Close)</option>
              <option value="STRONG_BEARISH">STRONG_BEARISH (US Sell-Off -1%+)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:#22d3ee; font-weight:600; display:block; margin-bottom:3px;">3. Asian Markets (Nikkei 225 &amp; Hang Seng)</label>
            <select id="ppAsian" style="width:100%;">
              <option value="POSITIVE_MOMENTUM">POSITIVE_MOMENTUM (Nikkei/HangSeng Green)</option>
              <option value="NEUTRAL_MIXED">NEUTRAL_MIXED (Mixed / Flat Asia)</option>
              <option value="NEGATIVE_DRAG">NEGATIVE_DRAG (Nikkei/HangSeng Red)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:#fbbf24; font-weight:600; display:block; margin-bottom:3px;">4. FII &amp; DII Activity (Prev Session)</label>
            <select id="ppFii" style="width:100%;">
              <option value="FII_DII_NET_BUYERS">FII_DII_NET_BUYERS (Both Buying ★)</option>
              <option value="FII_NET_LONG">FII_NET_LONG (FII Bought Cash/Fut)</option>
              <option value="FII_SELL_DII_CUSHION">FII_SELL_DII_CUSHION (FII Sold / DII Cushioned)</option>
              <option value="NEUTRAL_MIXED">NEUTRAL_MIXED (Balanced Flows)</option>
              <option value="FII_NET_SHORT">FII_NET_SHORT (Heavy FII Selling)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:#fbbf24; font-weight:600; display:block; margin-bottom:3px;">5. Crude Oil (Brent Crude — &gt;80% Import)</label>
            <select id="ppBrent" style="width:100%;">
              <option value="COOLING_BULLISH">COOLING_BULLISH (Oil Falling &rarr; Bullish India)</option>
              <option value="STABLE_NEUTRAL">STABLE_NEUTRAL (Range-Bound Oil)</option>
              <option value="SPIKING_BEARISH">SPIKING_BEARISH (Oil Spiking &rarr; Bearish Inflation)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:#fbbf24; font-weight:600; display:block; margin-bottom:3px;">6. Dollar Index (DXY) &amp; USD/INR</label>
            <select id="ppDxyInr" style="width:100%;">
              <option value="COOLING_INR_STRONG">COOLING_INR_STRONG (DXY Down / INR Firm)</option>
              <option value="STABLE_NEUTRAL">STABLE_NEUTRAL (DXY &amp; USD/INR Flat)</option>
              <option value="RISING_DXY_INR_WEAK">RISING_DXY_INR_WEAK (DXY Up / FII Outflow Risk)</option>
            </select>
          </div>
        </div>

        <!-- Stage 3 Domestic Pre-Market Data & Key Reference Levels -->
        <div style="font-size:11.5px; font-weight:700; color:#34d399; margin-bottom:6px; text-transform:uppercase;">
          🇮🇳 Stage 3: Domestic Pre-Market Data (Check 9:00 AM – 9:08 AM IST) &amp; Key Option Chain Walls
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(155px, 1fr)); gap:10px; margin-bottom:14px;">
          <div>
            <label style="font-size:11px; color:#34d399; font-weight:600; display:block; margin-bottom:3px;">7a. 09:08 Equilibrium Spot</label>
            <input type="number" step="0.05" id="ppPreOpen" placeholder="e.g. 24485" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:#34d399; font-weight:600; display:block; margin-bottom:3px;">7b. 09:08 Advance-Decline</label>
            <select id="ppAdvDec" style="width:100%;">
              <option value="STRONG_ADVANCES_3_1">STRONG_ADVANCES (&gt;3:1 Bullish)</option>
              <option value="MODERATE_ADVANCES">MODERATE_ADVANCES (Positive Breadth)</option>
              <option value="BALANCED_1_1">BALANCED_1_1 (~1:1 Mixed)</option>
              <option value="MODERATE_DECLINES">MODERATE_DECLINES (Negative Breadth)</option>
              <option value="STRONG_DECLINES_1_3">STRONG_DECLINES (&lt;1:3 Bearish)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:#34d399; font-weight:600; display:block; margin-bottom:3px;">8a. India VIX (Volatility)</label>
            <input type="number" step="0.1" id="ppVix" placeholder="14-16 Ideal | >19.5 No-Trade" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:#fbbf24; font-weight:600; display:block; margin-bottom:3px;">8b. Prev Day Closing PCR</label>
            <input type="number" step="0.01" id="ppPrevPcr" placeholder="e.g. 1.54 or 1.18" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Session / Event Context</label>
            <select id="ppEvent" style="width:100%;">
              <option value="NORMAL_DAY">NORMAL_DAY (Standard)</option>
              <option value="WEEKLY_EXPIRY">WEEKLY_EXPIRY (High Gamma)</option>
              <option value="PRE_EVENT_HIGH_IV">PRE_EVENT_HIGH_IV (IV Crush!)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Prev Day High (PDH)</label>
            <input type="number" step="0.05" id="ppPdh" placeholder="e.g. 24560" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Prev Day Low (PDL)</label>
            <input type="number" step="0.05" id="ppPdl" placeholder="e.g. 24380" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Prev Day Close (PDC)</label>
            <input type="number" step="0.05" id="ppPdc" placeholder="e.g. 24450" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Call Wall (CE Res)</label>
            <input type="number" step="50" id="ppCallWall" placeholder="e.g. 24600" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Put Wall (PE Sup)</label>
            <input type="number" step="50" id="ppPutWall" placeholder="e.g. 24400" style="width:100%;" />
          </div>
        </div>

        <!-- Row 3: Your Trade Execution Plan & Post-Market Reflection -->
        <div style="font-size:11.5px; font-weight:700; color:#93c5fd; margin-bottom:6px; text-transform:uppercase;">
          🎯 Your Daily Execution Plan &amp; Post-Market Reflection Notes
        </div>
        <div style="display:grid; grid-template-columns: 1.3fr 0.8fr 0.8fr 0.6fr 1.5fr 1.5fr; gap:10px;">
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Your Planned Bias</label>
            <select id="ppBias" style="width:100%;">
              <option value="TWO_WAY">TWO_WAY (Play Bull or Bear Trigger)</option>
              <option value="BULLISH_ABOVE_TRIGGER">BULLISH_ABOVE_TRIGGER (Buy CE Only)</option>
              <option value="BEARISH_BELOW_TRIGGER">BEARISH_BELOW_TRIGGER (Buy PE Only)</option>
              <option value="NO_TRADE_CHOP">NO_TRADE_CHOP (Sit Out / High IV / Chop)</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:#34d399; display:block; margin-bottom:3px;">Bull Trigger Spot (&ge;)</label>
            <input type="number" step="0.05" id="ppBullTrig" placeholder="Buy CE above..." style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:#fb7185; display:block; margin-bottom:3px;">Bear Trigger Spot (&le;)</label>
            <input type="number" step="0.05" id="ppBearTrig" placeholder="Buy PE below..." style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:var(--muted); display:block; margin-bottom:3px;">Max Trades</label>
            <input type="number" step="1" min="0" max="10" id="ppMaxTrades" value="2" style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:#93c5fd; display:block; margin-bottom:3px;">Morning Pre-Plan Notes (09:08 AM)</label>
            <input type="text" id="ppPreNotes" placeholder="e.g. PCR 1.54 high -> watch for PE reversal below VWAP..." style="width:100%;" />
          </div>
          <div>
            <label style="font-size:11px; color:#fbbf24; display:block; margin-bottom:3px;">Post-Market Reflection / Correction (03:35 PM)</label>
            <input type="text" id="ppPostNotes" placeholder="e.g. Followed signal well / Deviated by taking early trade..." style="width:100%;" />
          </div>
        </div>
      </div>

      <!-- Step 2: System Pre-Market Signal & 8-Point Checklist Evaluation Card -->
      <div class="card" style="margin-bottom:16px; border-color: rgba(16, 185, 129, 0.5);">
        <div class="card-header">
          <span>🧠 Step 2: Live 8-Point Pre-Market Sentiment Checklist &amp; Opening Signal</span>
          <button type="button" class="btn-green" onclick="savePrePlan(true)">✓ Apply System Suggested Bias to My Plan</button>
        </div>
        <div id="preMarketSignalBox" style="padding:12px 16px; border-radius:8px; background:rgba(15,23,42,0.9); border:1px solid var(--border); margin-bottom:12px;">
          Generating Pre-Market Sentiment Signal...
        </div>

        <!-- Step 3: Live / Post-Market Verification Banner -->
        <div style="font-size:12px; font-weight:700; color:#fbbf24; margin-bottom:6px; text-transform:uppercase;">
          🌇 Step 3: Post-Market Audit — Did Market &amp; Your Trades Match the Pre-Plan?
        </div>
        <div id="prePlanComparisonBox" style="padding:12px 16px; border-radius:8px; background:rgba(15,23,42,0.85); border:1px solid var(--border); font-size:12px;">
          Loading Pre-Plan vs. Actual Market &amp; Trade Verification...
        </div>
      </div>

      <!-- Step 4: Multi-Day Pre-Market Sentiment vs Actual Outcome History Table -->
      <div class="card">
        <div class="card-header">
          <span>📅 Multi-Day Pre-Market Sentiment Signal vs. Actual Market &amp; Trade Deviation History</span>
          <span style="font-size:11px; color:#93c5fd;">Synced automatically to: doc/TRADING_JOURNAL.md (Section 0)</span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="text-align:left">Date</th>
                <th style="text-align:left">GIFT Gap &amp; Global</th>
                <th>Prev PCR</th>
                <th style="text-align:left">VIX &amp; Buying Env</th>
                <th style="text-align:left">System Pre-Market Signal</th>
                <th style="text-align:left">Your Planned Bias &amp; Triggers</th>
                <th>Actual O / H / L / C</th>
                <th>Trades &amp; PnL</th>
                <th style="text-align:left">Discipline Verdict</th>
                <th style="text-align:left">Actual vs. Plan Audit &amp; Notes</th>
              </tr>
            </thead>
            <tbody id="prePlanTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <script>
    let autoRefreshTimer = null;
    let countdownTickTimer = null;
    let countdownRemainingSec = 180;
    let latestReportCache = null;
    let prePlanFormInitializedForDate = null;
    let activeTab = "LIVE";

    function switchTab(tabName) {
      activeTab = tabName;
      document.getElementById("tabLiveContent").style.display = tabName === "LIVE" ? "block" : "none";
      document.getElementById("tabPreMarketContent").style.display = tabName === "PREMARKET" ? "block" : "none";
      document.getElementById("btnTabLive").classList.toggle("active", tabName === "LIVE");
      document.getElementById("btnTabPreMarket").classList.toggle("active", tabName === "PREMARKET");
    }

    function fmtNum(n, dec = 2) {
      if (n === null || n === undefined || isNaN(n)) return "--";
      return Number(n).toLocaleString("en-IN", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    }
    function fmtInt(n, signed = false) {
      if (n === null || n === undefined || isNaN(n)) return "--";
      const val = Math.round(Number(n));
      const s = Math.abs(val).toLocaleString("en-IN");
      if (val > 0) return (signed ? "+" : "") + s;
      if (val < 0) return "-" + s;
      return "0";
    }

    async function apiCall(path, method = "GET", body = null) {
      const opts = { method, headers: { "Content-Type": "application/json" } };
      if (body) opts.body = JSON.stringify(body);
      const res = await fetch(path, opts);
      return await res.json();
    }

    function clearLogTracer() {
      const box = document.getElementById("logTracerContainer");
      if (box) {
        box.innerHTML = `<div style="color:var(--muted); padding:8px;">🧹 Log Tracer cleared. Click "↻ Re-Evaluate Option Chain Now" or "▶ Step Next Demo Snapshot" to run a fresh evaluation cycle.</div>`;
      }
    }

    function updateCountdownLabels() {
      const sec = parseInt(document.getElementById("autoRefreshSelect").value, 10);
      const mode = document.getElementById("modeSelect").value;
      const hb = document.getElementById("engineHeartbeatBadge");
      const cd = document.getElementById("tracerCountdownLabel");
      const cycleNum = (latestReportCache && latestReportCache._cycle_id) || 1;
      const wallTime = (latestReportCache && latestReportCache._wall_time) || "--:--:--";
      const mktOpen = latestReportCache ? latestReportCache._market_open !== false : true;
      const mktReason = (latestReportCache && latestReportCache._market_reason) || "Market Closed (After 15:30 IST)";

      if (mode === "LIVE_OPENALGO" && !mktOpen) {
        if (hb) {
          hb.className = "badge badge-demo";
          hb.textContent = `🛑 MARKET CLOSED | Final Cycle #${cycleNum} (${wallTime}) | Live Polling Paused Until 09:15 AM`;
        }
        if (cd) cd.textContent = `🛑 ${mktReason} (Switch to Demo Simulator to practice after hours)`;
        return;
      }

      if (sec > 0) {
        if (hb) {
          hb.className = "badge badge-sim";
          hb.textContent = `🟢 ENGINE ACTIVE | Cycle #${cycleNum} (${wallTime}) | Next Poll: ${countdownRemainingSec}s`;
        }
        if (cd) cd.textContent = `Next Evaluation Cycle in ${countdownRemainingSec}s`;
      } else {
        if (hb) {
          hb.className = "badge badge-demo";
          hb.textContent = `🟡 MANUAL MODE | Cycle #${cycleNum} (${wallTime}) | Auto-Poll OFF`;
        }
        if (cd) cd.textContent = `Auto-Poll OFF (Click Re-Evaluate or Step Demo)`;
      }
    }

    async function refreshData(advanceDemo = false) {
      const pill = document.getElementById("tracerStatusPill");
      if (pill) {
        pill.className = "badge badge-demo";
        pill.textContent = "⚡ ANALYSING OPTION CHAIN...";
      }
      const sec = parseInt(document.getElementById("autoRefreshSelect").value, 10);
      if (sec > 0) countdownRemainingSec = sec;
      const data = await apiCall("/api/state?advance=" + (advanceDemo ? "1" : "0"));
      renderState(data);
    }

    async function changeConfig() {
      const mode = document.getElementById("modeSelect").value;
      const underlying = document.getElementById("underlyingSelect").value;
      prePlanFormInitializedForDate = null;
      const data = await apiCall("/api/config", "POST", { mode, underlying });
      renderState(data);
    }

    async function saveApiKey() {
      const apiKey = document.getElementById("apiKeyInput").value.trim();
      const data = await apiCall("/api/config", "POST", { api_key: apiKey, mode: apiKey ? "LIVE_OPENALGO" : "DEMO" });
      document.getElementById("apiKeyInput").value = "";
      renderState(data);
    }

    function autoFillPrePlan() {
      if (!latestReportCache) return;
      const rep = latestReportCache;
      const spot = Number(rep.spot_ltp || 0);
      const step = rep.underlying === "BANKNIFTY" ? 100 : 50;
      const atm = Number(rep.atm_strike || spot);
      const resStrike = Number(rep.resistance_strike || (atm + step));
      const supStrike = Number(rep.support_strike || (atm - step));

      let atmIv = 14.5;
      for (const r of (rep.strikes || [])) {
        if (Math.abs(r.strike - atm) < 0.01) {
          atmIv = Number(((r.ce.implied_volatility || 14.5) + (r.pe.implied_volatility || 14.5)) / 2).toFixed(2);
          break;
        }
      }

      const pdc = Number((spot - step * 0.4).toFixed(2));
      document.getElementById("ppPdh").value = (spot + step * 0.5).toFixed(2);
      document.getElementById("ppPdl").value = (spot - step * 1.2).toFixed(2);
      document.getElementById("ppPdc").value = pdc.toFixed(2);
      document.getElementById("ppPreOpen").value = spot.toFixed(2);
      document.getElementById("ppGiftGap").value = (spot - pdc).toFixed(0);
      document.getElementById("ppPrevPcr").value = Number(rep.overall_pcr || 1.12).toFixed(2);
      document.getElementById("ppVix").value = atmIv;
      document.getElementById("ppCallWall").value = resStrike;
      document.getElementById("ppPutWall").value = supStrike;
      document.getElementById("ppBullTrig").value = atm.toFixed(2);
      document.getElementById("ppBearTrig").value = (atm - step * 0.5).toFixed(2);
    }

    async function loadPresetScenario(presetType) {
      autoFillPrePlan();
      if (presetType === "HIGH_PCR_REVERSAL") {
        document.getElementById("ppGiftGap").value = "40";
        document.getElementById("ppGlobal").value = "NEUTRAL_MIXED";
        document.getElementById("ppAsian").value = "NEGATIVE_DRAG";
        document.getElementById("ppPrevPcr").value = "1.54";
        document.getElementById("ppVix").value = "15.2";
        document.getElementById("ppFii").value = "FII_NET_SHORT";
        document.getElementById("ppBrent").value = "SPIKING_BEARISH";
        document.getElementById("ppDxyInr").value = "RISING_DXY_INR_WEAK";
        document.getElementById("ppAdvDec").value = "MODERATE_DECLINES";
        document.getElementById("ppEvent").value = "NORMAL_DAY";
        document.getElementById("ppBias").value = "BEARISH_BELOW_TRIGGER";
        document.getElementById("ppPreNotes").value =
          "Prev Day PCR 1.54 is extreme overbought (>1.45) + FII Short + Brent/DXY rising! Avoid chasing Gap-Up CE; wait for VWAP breakdown to buy ATM PE.";
      } else if (presetType === "GOLDILOCKS_BULL") {
        document.getElementById("ppGiftGap").value = "35";
        document.getElementById("ppGlobal").value = "MILD_BULLISH";
        document.getElementById("ppAsian").value = "POSITIVE_MOMENTUM";
        document.getElementById("ppPrevPcr").value = "1.18";
        document.getElementById("ppVix").value = "14.5";
        document.getElementById("ppFii").value = "FII_DII_NET_BUYERS";
        document.getElementById("ppBrent").value = "COOLING_BULLISH";
        document.getElementById("ppDxyInr").value = "COOLING_INR_STRONG";
        document.getElementById("ppAdvDec").value = "STRONG_ADVANCES_3_1";
        document.getElementById("ppEvent").value = "NORMAL_DAY";
        document.getElementById("ppBias").value = "BULLISH_ABOVE_TRIGGER";
        document.getElementById("ppPreNotes").value =
          "8/8 Bullish Pre-Market Cues + India VIX 14.5 in 13.5-16.5 Goldilocks Option Buying Zone -> Buy ATM CE above Bull Trigger.";
      } else if (presetType === "HIGH_IV_NO_TRADE") {
        document.getElementById("ppGiftGap").value = "155";
        document.getElementById("ppGlobal").value = "NEUTRAL_MIXED";
        document.getElementById("ppAsian").value = "NEUTRAL_MIXED";
        document.getElementById("ppPrevPcr").value = "1.02";
        document.getElementById("ppVix").value = "21.5";
        document.getElementById("ppFii").value = "NEUTRAL_MIXED";
        document.getElementById("ppBrent").value = "SPIKING_BEARISH";
        document.getElementById("ppDxyInr").value = "RISING_DXY_INR_WEAK";
        document.getElementById("ppAdvDec").value = "BALANCED_1_1";
        document.getElementById("ppEvent").value = "PRE_EVENT_HIGH_IV";
        document.getElementById("ppBias").value = "NO_TRADE_CHOP";
        document.getElementById("ppMaxTrades").value = "0";
        document.getElementById("ppPreNotes").value =
          "VIX 21.5 (>19.5) + Huge Gap -> High IV Crush risk! Better No-Trade Day for option buying.";
      }
      await savePrePlan(false);
    }

    function populatePrePlanInputs(plan) {
      if (!plan) return;
      document.getElementById("ppGiftGap").value = plan.gift_nifty_gap !== undefined ? plan.gift_nifty_gap : (plan.gap_pts || 0);
      document.getElementById("ppGlobal").value = plan.global_sentiment || "NEUTRAL_MIXED";
      document.getElementById("ppAsian").value = plan.asian_markets || "POSITIVE_MOMENTUM";
      document.getElementById("ppPrevPcr").value = plan.prev_day_pcr !== undefined ? plan.prev_day_pcr : 1.0;
      document.getElementById("ppVix").value = plan.india_vix || 14.5;
      document.getElementById("ppFii").value = plan.fii_flow || "NEUTRAL_MIXED";
      document.getElementById("ppBrent").value = plan.brent_crude || "STABLE_NEUTRAL";
      document.getElementById("ppDxyInr").value = plan.dxy_usdinr || "STABLE_NEUTRAL";
      document.getElementById("ppAdvDec").value = plan.preopen_adv_dec || "MODERATE_ADVANCES";
      document.getElementById("ppEvent").value = plan.event_context || "NORMAL_DAY";
      document.getElementById("ppPdh").value = plan.pdh || "";
      document.getElementById("ppPdl").value = plan.pdl || "";
      document.getElementById("ppPdc").value = plan.pdc || "";
      document.getElementById("ppPreOpen").value = plan.pre_open_spot || "";
      document.getElementById("ppCallWall").value = plan.call_wall_strike || "";
      document.getElementById("ppPutWall").value = plan.put_wall_strike || "";
      document.getElementById("ppBias").value = plan.planned_bias || "TWO_WAY";
      document.getElementById("ppBullTrig").value = plan.bull_trigger || "";
      document.getElementById("ppBearTrig").value = plan.bear_trigger || "";
      document.getElementById("ppMaxTrades").value = plan.max_trades !== undefined ? plan.max_trades : 2;
      document.getElementById("ppPreNotes").value = plan.pre_plan_notes || "";
      document.getElementById("ppPostNotes").value = plan.post_market_notes || "";
    }

    async function savePrePlan(useSuggestedBias = false) {
      const payload = {
        gift_nifty_gap: parseFloat(document.getElementById("ppGiftGap").value || "0"),
        global_sentiment: document.getElementById("ppGlobal").value,
        asian_markets: document.getElementById("ppAsian").value,
        prev_day_pcr: parseFloat(document.getElementById("ppPrevPcr").value || "1.0"),
        india_vix: parseFloat(document.getElementById("ppVix").value || "14.5"),
        fii_flow: document.getElementById("ppFii").value,
        brent_crude: document.getElementById("ppBrent").value,
        dxy_usdinr: document.getElementById("ppDxyInr").value,
        preopen_adv_dec: document.getElementById("ppAdvDec").value,
        event_context: document.getElementById("ppEvent").value,
        pdh: parseFloat(document.getElementById("ppPdh").value || "0"),
        pdl: parseFloat(document.getElementById("ppPdl").value || "0"),
        pdc: parseFloat(document.getElementById("ppPdc").value || "0"),
        pre_open_spot: parseFloat(document.getElementById("ppPreOpen").value || "0"),
        call_wall_strike: parseFloat(document.getElementById("ppCallWall").value || "0"),
        put_wall_strike: parseFloat(document.getElementById("ppPutWall").value || "0"),
        planned_bias: document.getElementById("ppBias").value,
        bull_trigger: parseFloat(document.getElementById("ppBullTrig").value || "0"),
        bear_trigger: parseFloat(document.getElementById("ppBearTrig").value || "0"),
        max_trades: parseInt(document.getElementById("ppMaxTrades").value || "2", 10),
        pre_plan_notes: document.getElementById("ppPreNotes").value.trim(),
        post_market_notes: document.getElementById("ppPostNotes").value.trim(),
        use_suggested_bias: useSuggestedBias,
      };
      const data = await apiCall("/api/preplan", "POST", payload);
      if (data.report && data.report.journal && data.report.journal.pre_plan && data.report.journal.pre_plan.today) {
        populatePrePlanInputs(data.report.journal.pre_plan.today);
      }
      renderState(data);
    }

    function updateAlertPlaceholders() {
      const provider = document.getElementById("waProvider").value;
      const phoneInput = document.getElementById("waPhone");
      const keyInput = document.getElementById("waKey");
      if (provider === "gmail") {
        phoneInput.placeholder = "your_email@gmail.com";
        keyInput.placeholder = "16-char Google App Password";
      } else if (provider === "webhook") {
        phoneInput.placeholder = "Recipient / Channel (optional)";
        keyInput.placeholder = "https://your-webhook-url...";
      } else {
        phoneInput.placeholder = "+919876543210";
        keyInput.placeholder = "API Key / Access Token";
      }
    }

    async function saveWhatsAppConfig() {
      const provider = document.getElementById("waProvider").value;
      const phone = document.getElementById("waPhone").value.trim();
      const key = document.getElementById("waKey").value.trim();
      const data = await apiCall("/api/whatsapp", "POST", { action: "CONFIG", provider, phone, api_key: key });
      document.getElementById("waKey").value = "";
      renderState(data);
    }

    async function sendWhatsAppNow() {
      const data = await apiCall("/api/whatsapp", "POST", { action: "SEND_NOW" });
      renderState(data);
    }

    async function placePaperOrder(optionType) {
      const data = await apiCall("/api/trade", "POST", { action: "OPEN", option_type: optionType });
      renderState(data);
    }

    async function closePaperOrder(tradeId) {
      const data = await apiCall("/api/trade", "POST", { action: "CLOSE", trade_id: tradeId });
      renderState(data);
    }

    function toggleAutoRefresh(syncBackend = true) {
      if (autoRefreshTimer) clearInterval(autoRefreshTimer);
      if (countdownTickTimer) clearInterval(countdownTickTimer);
      const sec = parseInt(document.getElementById("autoRefreshSelect").value, 10);
      countdownRemainingSec = sec;
      updateCountdownLabels();
      if (syncBackend) {
        apiCall("/api/config", "POST", { auto_poll_sec: sec, skip_eval: true }).catch(() => {});
      }
      if (sec > 0) {
        countdownTickTimer = setInterval(() => {
          const mode = document.getElementById("modeSelect").value;
          const mktOpen = latestReportCache ? latestReportCache._market_open !== false : true;
          if (mode === "LIVE_OPENALGO" && !mktOpen) {
            updateCountdownLabels();
            return;
          }
          countdownRemainingSec = Math.max(0, countdownRemainingSec - 1);
          updateCountdownLabels();
          if (countdownRemainingSec === 0) {
            countdownRemainingSec = sec;
            refreshData(true);
          }
        }, 1000);
      }
    }

    function renderLogTracer(trace) {
      if (!trace || !trace.inputs) return;
      const container = document.getElementById("logTracerContainer");
      const pill = document.getElementById("tracerStatusPill");
      const clearEach = document.getElementById("chkClearEachCycle").checked;
      const mode = document.getElementById("modeSelect").value;
      const mktOpen = latestReportCache ? latestReportCache._market_open !== false : true;

      if (pill) {
        if (mode === "LIVE_OPENALGO" && !mktOpen) {
          pill.className = "badge badge-demo";
          pill.textContent = `🛑 MARKET CLOSED (PAUSED @ CYCLE #${trace.cycle_id})`;
        } else {
          pill.className = "badge badge-sim";
          pill.textContent = `✓ EVALUATED CYCLE #${trace.cycle_id} @ ${trace.wall_time}`;
        }
      }

      const inp = trace.inputs;
      const ce = trace.ce_eval || { passed: [], missing: [], score: 0 };
      const pe = trace.pe_eval || { passed: [], missing: [], score: 0 };
      const vd = trace.verdict || {};

      const renderRuleList = (items, isPass) => {
        if (!items || items.length === 0) {
          return `<div style="color:var(--muted); padding-left:8px;">${isPass ? '• None met yet (0/6)' : '• 🎉 NONE MISSING — ALL 6 CONDITIONS MET!'}</div>`;
        }
        return items.map(item => `
          <div style="padding-left:8px; margin-top:2px; color:${isPass ? '#86efac' : '#fca5a5'};">
            <b>${isPass ? '✔ [MET]' : '✘ [MISSING]'} ${item.rule}:</b> <span style="color:#e2e8f0">${item.detail}</span>
          </div>
        `).join("");
      };

      const off = trace.offline_log || {};
      const offLineStr = off.daily_log_path
        ? `💾 Offline Logger Saved: <code>${off.daily_log_path}</code> | <code>${off.daily_csv_path}</code> | <code>${off.daily_jsonl_path}</code>`
        : "";

      const cycleHtml = `
        <div style="border:1px solid rgba(51,65,85,0.9); border-radius:8px; padding:10px 12px; margin-bottom:10px; background:rgba(15,23,42,0.92);">
          <div style="display:flex; justify-content:space-between; flex-wrap:wrap; border-bottom:1px dashed rgba(148,163,184,0.25); padding-bottom:6px; margin-bottom:8px;">
            <span style="color:#22d3ee; font-weight:700;">
              [STEP 1 — ENGINE EVALUATION CYCLE #${trace.cycle_id}] Evaluated @ ${trace.wall_time} IST | Source: ${inp.source_desc}
            </span>
            <span style="color:#fbbf24; font-weight:700;">
              Snapshot Time: ${inp.snapshot_time} (${inp.underlying} Expiry ${inp.expiry_date} — ${inp.days_to_expiry}d | Snapshots Today: ${inp.snapshots_today})
            </span>
          </div>

          <div style="margin-bottom:8px;">
            <div style="color:#93c5fd; font-weight:700; margin-bottom:3px;">[STEP 2 — RAW OPTION CHAIN INPUTS CONSIDERED FOR EVALUATION]</div>
            <div style="padding-left:8px; color:#cbd5e1;">
              <div>• <b>Spot &amp; Futures Basis :</b> ${inp.spot_and_basis}</div>
              <div>• <b>Straddle &amp; Volatility:</b> ${inp.straddle_and_vol}</div>
              <div>• <b>OI &amp; PCR Battle      :</b> ${inp.oi_and_pcr}</div>
              <div style="color:#86efac;">• <b>ATM Call (CE) Inputs :</b> ${inp.atm_ce_contract}</div>
              <div style="color:#fda4af;">• <b>ATM Put  (PE) Inputs :</b> ${inp.atm_pe_contract}</div>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap:10px; margin-bottom:8px;">
            <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:8px 10px;">
              <div style="font-weight:700; color:#34d399; margin-bottom:4px;">
                [STEP 3 — BULLISH ATM CE EVALUATION: ${ce.symbol} &rarr; Score ${ce.score}/6]
              </div>
              <div style="font-weight:700; color:#86efac; font-size:11px; margin-top:4px;">✅ CONDITIONS MET (${ce.passed.length} Passed):</div>
              ${renderRuleList(ce.passed, true)}
              <div style="font-weight:700; color:#fca5a5; font-size:11px; margin-top:6px;">❌ MISSING CONDITIONS (${ce.missing.length} Blocking 6/6):</div>
              ${renderRuleList(ce.missing, false)}
            </div>

            <div style="background:rgba(244,63,94,0.06); border:1px solid rgba(244,63,94,0.3); border-radius:6px; padding:8px 10px;">
              <div style="font-weight:700; color:#fb7185; margin-bottom:4px;">
                [STEP 4 — BEARISH ATM PE EVALUATION: ${pe.symbol} &rarr; Score ${pe.score}/6]
              </div>
              <div style="font-weight:700; color:#86efac; font-size:11px; margin-top:4px;">✅ CONDITIONS MET (${pe.passed.length} Passed):</div>
              ${renderRuleList(pe.passed, true)}
              <div style="font-weight:700; color:#fca5a5; font-size:11px; margin-top:6px;">❌ MISSING CONDITIONS (${pe.missing.length} Blocking 6/6):</div>
              ${renderRuleList(pe.missing, false)}
            </div>
          </div>

          <div style="border-top:1px dashed rgba(148,163,184,0.25); padding-top:6px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <span><b style="color:#22d3ee;">[STEP 5 — FINAL ENGINE VERDICT]:</b> <b style="color:#f8fafc;">${vd.action}</b></span>
            <span style="color:#fbbf24;">📓 ${vd.journal_note}</span>
          </div>
          ${offLineStr ? `<div style="margin-top:4px; font-size:11px; color:#94a3b8;">${offLineStr}</div>` : ""}
        </div>
      `;

      if (clearEach) {
        container.innerHTML = cycleHtml;
      } else {
        if (container.innerHTML.includes("Initializing") || container.innerHTML.includes("cleared")) {
          container.innerHTML = cycleHtml;
        } else {
          container.innerHTML = cycleHtml + container.innerHTML;
        }
      }
    }

    function renderState(state) {
      document.getElementById("modeSelect").value = state.mode;
      document.getElementById("underlyingSelect").value = state.underlying;

      const badge = document.getElementById("modeBadge");
      const stepBtn = document.getElementById("stepBtn");
      if (state.mode === "DEMO") {
        badge.className = "badge badge-demo";
        badge.textContent = `PRACTICE SIMULATOR (STEP ${state.demo_step}/${state.demo_total_steps})`;
        stepBtn.style.display = "inline-block";
        stepBtn.textContent = `▶ Next Demo Snapshot (${state.demo_step}/${state.demo_total_steps})`;
      } else {
        stepBtn.style.display = "none";
        if (state.analyze_mode === true) {
          badge.className = "badge badge-sim";
          badge.textContent = "OPENALGO ANALYZE MODE (SAFE SIMULATOR)";
        } else if (state.analyze_mode === false) {
          badge.className = "badge badge-live";
          badge.textContent = "OPENALGO LIVE BROKER MODE";
        } else {
          badge.className = "badge badge-demo";
          badge.textContent = "OPENALGO CONNECTING...";
        }
      }

      const errBanner = document.getElementById("errorBanner");
      if (state.error) {
        errBanner.style.display = "block";
        errBanner.textContent = "OpenAlgo Notice: " + state.error;
      } else {
        errBanner.style.display = "none";
      }

      // Gmail / Setup Alert Panel
      if (state.whatsapp) {
        const wa = state.whatsapp;
        document.getElementById("waPreviewBox").textContent = wa.preview || "";
        if (wa.provider) {
          document.getElementById("waProvider").value = wa.provider;
          updateAlertPlaceholders();
        }
        if (wa.phone && !document.getElementById("waPhone").value) {
          document.getElementById("waPhone").value = wa.phone;
        }
        const waBadge = document.getElementById("waStatusBadge");
        if (wa.last_result && wa.last_result.status === "SENT") {
          waBadge.className = "badge badge-sim";
          waBadge.textContent = `${(wa.provider || "ALERT").toUpperCase()} SENT ✓`;
        } else if (wa.last_result && wa.last_result.status === "ERROR") {
          waBadge.className = "badge badge-live";
          waBadge.textContent = `ALERT ERROR`;
        } else if (wa.configured) {
          waBadge.className = "badge badge-sim";
          waBadge.textContent = `ARMED (${wa.provider.toUpperCase()})`;
        } else {
          waBadge.className = "badge badge-demo";
          waBadge.textContent = "PREVIEW MODE (Add Gmail App Password)";
        }
      }

      const rep = state.report;
      if (!rep) return;
      latestReportCache = rep;
      latestReportCache._market_open = state.market_open !== false;
      latestReportCache._market_reason = state.market_reason || "";
      if (state.eval_trace) {
        latestReportCache._cycle_id = state.eval_trace.cycle_id;
        latestReportCache._wall_time = state.eval_trace.wall_time;
        renderLogTracer(state.eval_trace);
      }
      updateCountdownLabels();

      // KPI Strip
      const spotDiff = rep.spot_ltp - rep.spot_vwap;
      document.getElementById("kpiSpot").innerHTML =
        `${fmtNum(rep.spot_ltp)} <span style="font-size:13px" class="${spotDiff >= 0 ? 'pos-green' : 'neg-red'}">(${spotDiff >= 0 ? '+' : ''}${fmtNum(spotDiff)})</span>`;
      document.getElementById("kpiSpotSub").textContent =
        `Session VWAP: ${fmtNum(rep.spot_vwap)} | ATM: ${fmtInt(rep.atm_strike)}`;

      const stradPct = rep.straddle_change_pct || 0;
      document.getElementById("kpiStraddle").innerHTML =
        `₹${fmtNum(rep.atm_straddle_ltp)} <span style="font-size:13px" class="${stradPct >= 0 ? 'pos-green' : 'neg-red'}">(${stradPct >= 0 ? '+' : ''}${fmtNum(stradPct)}%)</span>`;
      document.getElementById("kpiStraddleSub").textContent =
        `Open Straddle: ₹${fmtNum(rep.opening_straddle)} (${stradPct < -2 ? 'Theta Decaying' : 'Expanding/Stable'})`;

      document.getElementById("kpiPcr").textContent = `PCR ${fmtNum(rep.overall_pcr)}`;
      document.getElementById("kpiDoiBattle").innerHTML =
        `15m PE dOI: <b class="pos-green">${fmtInt(rep.near_pe_doi_15m, true)}</b> vs CE: <b class="neg-red">${fmtInt(rep.near_ce_doi_15m, true)}</b>`;

      document.getElementById("kpiWalls").textContent =
        `${fmtInt(rep.support_strike)} PE / ${fmtInt(rep.resistance_strike)} CE`;
      document.getElementById("kpiWallsSub").textContent =
        `Sup OI: ${fmtInt(rep.support_oi)} | Res OI: ${fmtInt(rep.resistance_oi)}`;

      document.getElementById("kpiSynth").textContent =
        rep.synthetic_future ? fmtNum(rep.synthetic_future) : "N/A";
      document.getElementById("kpiSynthSub").textContent =
        `Basis (Fair - Spot): ${rep.basis >= 0 ? '+' : ''}${fmtNum(rep.basis)} pts (${rep.expiry_date})`;

      // Signal Banner
      const sig = rep.signals;
      const sb = document.getElementById("signalBanner");
      const st = document.getElementById("signalTitle");
      const sm = document.getElementById("signalMeta");
      sb.className = "signal-banner";

      if (sig.action === "BUY_ATM_CE" && sig.trade_plan) {
        sb.classList.add("signal-buy-ce");
        const tp = sig.trade_plan;
        st.innerHTML = `🚀 HIGH-CONVICTION GAMMA BLAST: BUY ATM CALL (${tp.symbol}) — WhatsApp Ready!`;
        sm.innerHTML = `Entry LTP: <b>₹${fmtNum(tp.entry_ltp)}</b> | Hard Stop-Loss (-18%): <b>₹${fmtNum(tp.stop_loss)}</b> | Target 1 (+25%): <b>₹${fmtNum(tp.target_1)}</b> | Target 2 (+45%): <b>₹${fmtNum(tp.target_2)}</b> | <b>15m Anti-Theta Stop:</b> Exit if &lt; ₹${fmtNum(tp.entry_ltp * 1.05)}`;
      } else if (sig.action === "BUY_ATM_PE" && sig.trade_plan) {
        sb.classList.add("signal-buy-pe");
        const tp = sig.trade_plan;
        st.innerHTML = `🔻 HIGH-CONVICTION GAMMA BLAST: BUY ATM PUT (${tp.symbol}) — WhatsApp Ready!`;
        sm.innerHTML = `Entry LTP: <b>₹${fmtNum(tp.entry_ltp)}</b> | Hard Stop-Loss (-18%): <b>₹${fmtNum(tp.stop_loss)}</b> | Target 1 (+25%): <b>₹${fmtNum(tp.target_1)}</b> | Target 2 (+45%): <b>₹${fmtNum(tp.target_2)}</b> | <b>15m Anti-Theta Stop:</b> Exit if &lt; ₹${fmtNum(tp.entry_ltp * 1.05)}`;
      } else if (sig.action === "THETA_TRAP_NO_TRADE") {
        sb.classList.add("signal-trap");
        st.innerHTML = `⚠️ THETA TRAP DETECTED — DO NOT BUY OPTIONS RIGHT NOW`;
        sm.innerHTML = `ATM Straddle premium is decaying (${fmtNum(rep.straddle_change_pct)}%) while BOTH Call & Put Writers are adding OI. Institutional straddle sellers are eating Theta!`;
      } else {
        st.innerHTML = `⏳ WAIT FOR 6/6 ALIGNMENT (Current Best — Bullish CE: ${sig.ce_score}/6 | Bearish PE: ${sig.pe_score}/6)`;
        sm.innerHTML = `Polling every 3 mins (NSE OI Cycle). Wait for Trapped Writers (SHORT_COVERING) + Volume Burst + IV Stability.`;
      }

      // Checklists
      document.getElementById("scoreSummary").textContent =
        `CE Score: ${sig.ce_score}/6 | PE Score: ${sig.pe_score}/6`;
      document.getElementById("ceBoxTitle").textContent =
        `Bullish ATM CE Checklist (${sig.ce_score}/6)`;
      document.getElementById("peBoxTitle").textContent =
        `Bearish ATM PE Checklist (${sig.pe_score}/6)`;

      const renderChecks = (items) =>
        items.map(([title, passed, detail]) => `
          <div class="check-item">
            <span class="${passed ? 'pill-pass' : 'pill-wait'}">${passed ? 'PASS' : 'WAIT'}</span>
            <div>
              <div style="font-weight:600; color:${passed ? '#f8fafc' : '#94a3b8'}">${title}</div>
              <div style="font-size:11px; color:var(--muted)">${detail}</div>
            </div>
          </div>
        `).join("");

      document.getElementById("ceCheckList").innerHTML = renderChecks(sig.ce_checks || []);
      document.getElementById("peCheckList").innerHTML = renderChecks(sig.pe_checks || []);

      // OI Bars Visualization
      const maxOi = Math.max(
        1,
        ...rep.strikes.map(r => Math.max(r.ce.oi || 0, r.pe.oi || 0))
      );
      document.getElementById("oiBarsContainer").innerHTML = rep.strikes.map(r => {
        const ceW = Math.round(((r.ce.oi || 0) / maxOi) * 140);
        const peW = Math.round(((r.pe.oi || 0) / maxOi) * 140);
        const isAtm = Math.abs(r.strike - rep.atm_strike) < 0.01;
        return `
          <div class="oi-bar-row" style="${isAtm ? 'background:rgba(59,130,246,0.12); padding:3px 4px; border-radius:4px;' : ''}">
            <div class="bar-left-wrap">
              <span style="color:var(--muted)">${fmtInt(r.ce.doi_3m, true)}</span>
              <div class="bar-ce" style="width:${ceW}px"></div>
            </div>
            <div style="text-align:center; font-weight:700; color:${isAtm ? '#93c5fd' : '#e2e8f0'}">${fmtInt(r.strike)}</div>
            <div class="bar-right-wrap">
              <div class="bar-pe" style="width:${peW}px"></div>
              <span style="color:var(--muted)">${fmtInt(r.pe.doi_3m, true)}</span>
            </div>
          </div>
        `;
      }).join("");

      // Option Chain Table
      document.getElementById("chainHeaderTitle").textContent =
        `Live Option Chain (${rep.underlying} — Expiry ${rep.expiry_date} — ${rep.days_to_expiry}d to Expiry)`;

      document.getElementById("chainTableBody").innerHTML = rep.strikes.map(r => {
        const ce = r.ce || {};
        const pe = r.pe || {};
        const isAtm = Math.abs(r.strike - rep.atm_strike) < 0.01;
        return `
          <tr class="${isAtm ? 'atm-row' : ''}">
            <td style="text-align:left"><span class="q-badge q-${ce.quadrant}">${ce.quadrant}</span></td>
            <td>${fmtInt(ce.oi)}</td>
            <td class="${(ce.doi_3m || 0) < 0 ? 'pos-green' : 'neg-red'}">${fmtInt(ce.doi_3m, true)}</td>
            <td>${fmtNum(ce.vol_burst_ratio)}x</td>
            <td>${fmtNum(ce.implied_volatility, 1)}%</td>
            <td>${fmtNum(ce.delta, 2)}</td>
            <td>${fmtNum(ce.theta, 1)}</td>
            <td>${fmtNum(ce.vwap)}</td>
            <td style="font-weight:700; color:${ce.ltp >= ce.vwap ? '#34d399' : '#f8fafc'}">₹${fmtNum(ce.ltp)}</td>
            <td class="strike-col">${isAtm ? '★ ' : ''}${fmtInt(r.strike)}</td>
            <td style="text-align:left; font-weight:700; color:${pe.ltp >= pe.vwap ? '#34d399' : '#f8fafc'}">₹${fmtNum(pe.ltp)}</td>
            <td>${fmtNum(pe.vwap)}</td>
            <td>${fmtNum(pe.theta, 1)}</td>
            <td>${fmtNum(pe.delta, 2)}</td>
            <td>${fmtNum(pe.implied_volatility, 1)}%</td>
            <td>${fmtNum(pe.vol_burst_ratio)}x</td>
            <td class="${(pe.doi_3m || 0) > 0 ? 'pos-green' : 'neg-red'}">${fmtInt(pe.doi_3m, true)}</td>
            <td>${fmtInt(pe.oi)}</td>
            <td style="text-align:left"><span class="q-badge q-${pe.quadrant}">${pe.quadrant}</span></td>
          </tr>
        `;
      }).join("");

      // Pre-Market Sentiment Signal & Post-Market Deviation Portal (Tab 2 + Top Bar)
      const journal = rep.journal || {};
      const prePlanObj = journal.pre_plan || {};
      const todayPlan = prePlanObj.today;
      const planHistory = prePlanObj.history || [];
      const ppBadge = document.getElementById("prePlanStatusBadge");
      const topSigBadge = document.getElementById("topBarPreSignal");
      const ppSigBox = document.getElementById("preMarketSignalBox");
      const ppBox = document.getElementById("prePlanComparisonBox");

      if (todayPlan) {
        const keyTag = `${todayPlan.session_date}_${todayPlan.underlying}`;
        if (prePlanFormInitializedForDate !== keyTag) {
          populatePrePlanInputs(todayPlan);
          prePlanFormInitializedForDate = keyTag;
        }
        const statusStr = String(todayPlan.plan_match_status || "PENDING");
        if (statusStr.includes("ALIGNED") || statusStr.includes("100%")) {
          ppBadge.className = "badge badge-sim";
        } else if (statusStr.includes("DEVIATED")) {
          ppBadge.className = "badge badge-live";
        } else {
          ppBadge.className = "badge badge-demo";
        }
        ppBadge.textContent = statusStr;

        const sysSig = String(todayPlan.system_premarket_signal || "COMPUTING...");
        if (sysSig.includes("NO_TRADE") || sysSig.includes("HIGH-IV")) {
          topSigBadge.className = "badge badge-live";
        } else if (sysSig.includes("REVERSAL") || sysSig.includes("CAUTION") || sysSig.includes("SIDEWAYS")) {
          topSigBadge.className = "badge badge-demo";
        } else {
          topSigBadge.className = "badge badge-sim";
        }
        topSigBadge.textContent = sysSig.length > 48 ? sysSig.slice(0, 48) + "..." : sysSig;

        const reasonsList = String(todayPlan.system_premarket_reasons || "")
          .split(" ;; ")
          .filter(Boolean)
          .map(r => `<li style="margin-top:4px; color:#cbd5e1;">${r}</li>`)
          .join("");

        const chkItems = todayPlan.premarket_checklist || [];
        const renderStageChecklist = (stageCode) => {
          return chkItems
            .filter(item => item.stage === stageCode)
            .map(item => {
              let pillCls = "pill-wait";
              let pillText = item.verdict;
              if (item.verdict === "BULLISH") {
                pillCls = "pill-pass";
                pillText = "BULLISH";
              } else if (item.verdict === "BEARISH" || item.verdict === "DANGER_NO_TRADE") {
                pillCls = "q-badge q-SHORT_BUILDUP";
                pillText = item.verdict === "DANGER_NO_TRADE" ? "NO-TRADE IV" : "BEARISH";
              } else if (item.verdict === "REVERSAL_WATCH" || item.verdict === "CAUTION_GAP") {
                pillCls = "q-badge q-LONG_UNWINDING";
                pillText = item.verdict === "REVERSAL_WATCH" ? "REVERSAL" : "GAP CAUTION";
              }
              return `
                <div class="check-item">
                  <span class="${pillCls}" style="flex-shrink:0; margin-top:2px;">${pillText}</span>
                  <div>
                    <div style="font-weight:700; color:#f8fafc; font-size:12px;">
                      ${item.title} <span style="color:#22d3ee; font-weight:600;">[${item.value_label || ''}]</span>
                    </div>
                    <div style="font-size:11px; color:var(--muted); margin-top:2px;">${item.detail}</div>
                  </div>
                </div>
              `;
            })
            .join("");
        };

        const bullCnt = todayPlan.bull_cues_count !== undefined ? todayPlan.bull_cues_count : 0;
        const bearCnt = todayPlan.bear_cues_count !== undefined ? todayPlan.bear_cues_count : 0;
        const neutCnt = todayPlan.neutral_cues_count !== undefined ? todayPlan.neutral_cues_count : 0;

        ppSigBox.innerHTML = `
          <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:10px; border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:10px;">
            <div>
              <div style="font-size:11px; color:var(--muted); text-transform:uppercase;">
                Headline Pre-Market Signal (${todayPlan.session_date}) &mdash;
                <span class="pos-green">Bullish Cues: ${bullCnt}/8</span> |
                <span class="neg-red">Bearish Cues: ${bearCnt}/8</span> |
                <span>Neutral: ${neutCnt}/8</span>
              </div>
              <div style="font-size:16px; font-weight:800; color:#22d3ee; margin-top:2px;">${todayPlan.system_premarket_signal || '--'}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:11px; color:var(--muted);">Expected Market Open Structure</div>
              <div style="font-size:13px; font-weight:700; color:#fbbf24;">${todayPlan.expected_open_type || todayPlan.gap_regime || '--'}</div>
            </div>
          </div>
          <div style="margin-bottom:12px; font-size:13px; font-weight:700; color:#34d399;">
            ${todayPlan.option_buying_env || todayPlan.vix_regime || '--'}
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap:12px; margin-bottom:10px;">
            <div class="check-box">
              <div style="font-weight:700; color:#22d3ee; margin-bottom:6px; font-size:12.5px;">
                🌍 Global Indicators (6:30 AM – 8:00 AM IST)
              </div>
              ${renderStageChecklist("GLOBAL_630_800")}
            </div>
            <div class="check-box">
              <div style="font-weight:700; color:#fbbf24; margin-bottom:6px; font-size:12.5px;">
                📊 Macroeconomic &amp; Institutional Triggers
              </div>
              ${renderStageChecklist("MACRO_INSTITUTIONAL")}
            </div>
            <div class="check-box">
              <div style="font-weight:700; color:#34d399; margin-bottom:6px; font-size:12.5px;">
                🇮🇳 Domestic Pre-Market Data (9:00 AM – 9:08 AM IST)
              </div>
              ${renderStageChecklist("DOMESTIC_900_908")}
            </div>
          </div>

          <ul style="padding-left:18px; font-size:11.5px; margin-top:6px;">
            ${reasonsList}
          </ul>
        `;

        ppBox.innerHTML = `
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
            <div>
              <div style="color:#93c5fd; font-weight:700; margin-bottom:3px;">1. Morning Pre-Plan &amp; 8-Point Cues (${todayPlan.session_date})</div>
              <div><b>GIFT Gap:</b> ${todayPlan.gift_nifty_gap >= 0 ? '+' : ''}${fmtNum(todayPlan.gift_nifty_gap, 0)} pts | <b>US/Asia:</b> ${todayPlan.global_sentiment} / ${todayPlan.asian_markets || 'POS'}</div>
              <div><b>Macro:</b> ${todayPlan.fii_flow} | Oil: ${todayPlan.brent_crude || 'STABLE'} | DXY: ${todayPlan.dxy_usdinr || 'STABLE'}</div>
              <div><b>Your Planned Bias:</b> <span style="color:#22d3ee; font-weight:700">${todayPlan.planned_bias}</span> | <b>Triggers:</b> Bull &ge; ${fmtNum(todayPlan.bull_trigger, 0)} / Bear &le; ${fmtNum(todayPlan.bear_trigger, 0)}</div>
            </div>
            <div>
              <div style="color:#34d399; font-weight:700; margin-bottom:3px;">2. Actual Intraday Market Action vs. Pre-Plan</div>
              <div><b>Session O/H/L/C:</b> ${fmtNum(todayPlan.actual_open, 1)} / <b>${fmtNum(todayPlan.actual_high, 1)}</b> / <b>${fmtNum(todayPlan.actual_low, 1)}</b> / ${fmtNum(todayPlan.actual_close, 1)}</div>
              <div style="color:#cbd5e1">${todayPlan.market_vs_plan_detail || '--'}</div>
            </div>
            <div>
              <div style="color:#fbbf24; font-weight:700; margin-bottom:3px;">3. Actual Trade Execution vs. Pre-Plan Audit</div>
              <div><b>Verdict:</b> <b>${todayPlan.plan_match_status}</b> | <b>Trades:</b> ${todayPlan.actual_trades_count}/${todayPlan.max_trades} | <b>PnL:</b> ₹${fmtNum(todayPlan.actual_pnl_rupees)}</div>
              <div style="color:#cbd5e1">${todayPlan.trade_vs_plan_detail || '--'}</div>
            </div>
          </div>
        `;
      } else {
        ppBadge.className = "badge badge-demo";
        ppBadge.textContent = "NO PRE-PLAN SAVED TODAY";
        topSigBadge.textContent = "Open Pre-Market Portal";
      }

      if (planHistory.length === 0) {
        document.getElementById("prePlanTableBody").innerHTML =
          `<tr><td colspan="10" style="text-align:center; color:var(--muted); padding:12px;">No daily pre-plans saved yet. Click "🧠 Evaluate 8-Point Checklist & Save Plan" above!</td></tr>`;
      } else {
        document.getElementById("prePlanTableBody").innerHTML = planHistory.map(p => {
          const st = String(p.plan_match_status || "");
          const isDev = st.includes("DEVIATED");
          const isAligned = st.includes("ALIGNED");
          const pnl = Number(p.actual_pnl_rupees || 0);
          const pcrVal = Number(p.prev_day_pcr || 1.0);
          const pcrColor = pcrVal >= 1.45 ? "#fbbf24" : (pcrVal <= 0.65 ? "#22d3ee" : "#f8fafc");
          return `
            <tr style="${isDev ? 'background:rgba(244,63,94,0.08);' : (isAligned ? 'background:rgba(16,185,129,0.06);' : '')}">
              <td style="text-align:left; font-weight:700">${p.session_date}<br/><span style="font-size:10px; color:#34d399">Bull:${p.bull_cues_count || 0}/8</span> <span style="font-size:10px; color:#fb7185">Bear:${p.bear_cues_count || 0}/8</span></td>
              <td style="text-align:left">GIFT: <b>${(p.gift_nifty_gap || 0) >= 0 ? '+' : ''}${fmtNum(p.gift_nifty_gap || p.gap_pts, 0)}</b><br/><span style="color:var(--muted); font-size:11px;">US:${p.global_sentiment || 'NEUTRAL'} | Asia:${p.asian_markets || 'POS'}<br/>FII:${p.fii_flow || 'NEUTRAL'} | Oil:${p.brent_crude || 'STABLE'}</span></td>
              <td style="font-weight:700; color:${pcrColor}">${fmtNum(pcrVal, 2)}<br/><span style="font-size:10px; color:var(--muted)">${pcrVal >= 1.45 ? 'OVERBOUGHT' : (pcrVal <= 0.65 ? 'OVERSOLD' : 'NORMAL')}</span></td>
              <td style="text-align:left; white-space:normal; max-width:200px;"><b>VIX ${fmtNum(p.india_vix, 1)}</b> (${p.event_context || 'NORMAL'})<br/><span style="font-size:11px; color:var(--muted)">9:08 Adv/Dec: ${p.preopen_adv_dec || 'MOD'}</span></td>
              <td style="text-align:left; white-space:normal; max-width:250px; font-weight:600; color:#22d3ee">${p.system_premarket_signal || '--'}</td>
              <td style="text-align:left"><b>${p.planned_bias}</b><br/><span class="pos-green">&ge;${fmtNum(p.bull_trigger, 0)}</span> / <span class="neg-red">&le;${fmtNum(p.bear_trigger, 0)}</span></td>
              <td>O:${fmtNum(p.actual_open, 0)} H:${fmtNum(p.actual_high, 0)}<br/>L:${fmtNum(p.actual_low, 0)} C:${fmtNum(p.actual_close, 0)}</td>
              <td class="${pnl >= 0 ? 'pos-green' : 'neg-red'}" style="font-weight:700">${p.actual_trades_count}/${p.max_trades}<br/>${pnl >= 0 ? '+' : ''}₹${fmtNum(pnl)}</td>
              <td style="text-align:left; font-weight:700; color:${isDev ? '#fb7185' : (isAligned ? '#34d399' : '#fbbf24')}">${p.plan_match_status}</td>
              <td style="text-align:left; white-space:normal; max-width:340px;">
                <b>Mkt:</b> ${p.market_vs_plan_detail}<br/>
                <b>Trades:</b> ${p.trade_vs_plan_detail}<br/>
                <span style="color:#93c5fd"><b>AM:</b> ${p.pre_plan_notes || '--'}</span> | <span style="color:#fbbf24"><b>PM:</b> ${p.post_market_notes || '--'}</span>
              </td>
            </tr>
          `;
        }).join("");
      }

      // Setup & Fine-Tuning Journal (Score >= 3/6)
      const jEntries = journal.entries || [];
      const blockers = journal.blocker_summary || [];
      const blockerBanner = document.getElementById("journalBlockerBanner");
      if (blockers.length > 0) {
        blockerBanner.innerHTML = `<div style="font-weight:700; color:#93c5fd; margin-bottom:4px;">💡 Rule Blocker Fine-Tuning Insights (When &ge; 3/6 Conditions Met):</div>` +
          blockers.map(b =>
            `<div style="margin-top:2px;">• <b>${b.rule}</b> — Failed <b>${b.times_blocked}x</b> | Missed Winners (&ge;+12%): <b class="${b.missed_winners > 0 ? 'neg-red' : 'pos-green'}">${b.missed_winners}</b> | Avg Max Gain After: <b>${b.avg_max_gain_pct >= 0 ? '+' : ''}${fmtNum(b.avg_max_gain_pct, 1)}%</b> &rarr; <span style="color:#cbd5e1">${b.advice}</span></div>`
          ).join("");
      } else {
        blockerBanner.innerHTML = `💡 <b>Fine-Tuning Tracker Active:</b> Any snapshot scoring <b>3/6, 4/6, 5/6, or 6/6</b> is automatically logged here and to <code>doc/TRADING_JOURNAL.md</code> so you can see which missing condition (e.g., PCR, Volume Burst) blocked profitable moves.`;
      }

      if (jEntries.length === 0) {
        document.getElementById("journalTableBody").innerHTML =
          `<tr><td colspan="10" style="text-align:center; color:var(--muted); padding:14px;">No setups with &ge; 3/6 conditions met yet in this session.</td></tr>`;
      } else {
        document.getElementById("journalTableBody").innerHTML = jEntries.map(je => {
          const maxGain = Number(je.max_gain_pct || 0);
          const gainCls = maxGain >= 12 ? "pos-green" : (maxGain < 0 ? "neg-red" : "");
          const isMissedWinner = String(je.verdict || "").includes("MISSED WINNER");
          return `
            <tr style="${isMissedWinner ? 'background:rgba(245,158,11,0.08);' : ''}">
              <td style="text-align:left">${je.time_str}</td>
              <td style="text-align:left; font-weight:700">${je.symbol}</td>
              <td>${je.option_type}</td>
              <td style="font-weight:700; color:${je.score === 6 ? '#34d399' : '#fbbf24'}">${je.score}/6</td>
              <td>₹${fmtNum(je.entry_ltp)}</td>
              <td style="font-weight:700">₹${fmtNum(je.max_ltp_after)}</td>
              <td class="${gainCls}" style="font-weight:700">${maxGain >= 0 ? '+' : ''}${fmtNum(maxGain, 1)}%</td>
              <td style="text-align:left; font-weight:600; color:${isMissedWinner ? '#fbbf24' : '#e2e8f0'}">${je.verdict}</td>
              <td style="text-align:left; color:#fca5a5; white-space:normal; max-width:340px;">${je.missing_rules}</td>
              <td style="text-align:left; color:#86efac; white-space:normal; max-width:260px;">${je.passed_rules}</td>
            </tr>
          `;
        }).join("");
      }

      // Trades Table
      const trades = state.trades || [];
      if (trades.length === 0) {
        document.getElementById("tradesTableBody").innerHTML =
          `<tr><td colspan="13" style="text-align:center; color:var(--muted); padding:16px;">No practice trades yet. Click "+ Practice Buy ATM CE/PE" when a 6/6 Gamma Blast triggers!</td></tr>`;
      } else {
        document.getElementById("tradesTableBody").innerHTML = trades.map(t => {
          const pnlPts = Number(t.pnl_points || 0);
          const pnlRs = Number(t.pnl_rupees || 0);
          const cls = pnlRs >= 0 ? "pos-green" : "neg-red";
          return `
            <tr>
              <td style="text-align:left">#${t.id}</td>
              <td style="text-align:left; font-weight:700">${t.symbol}</td>
              <td>${t.option_type}</td>
              <td>${t.quantity}</td>
              <td>₹${fmtNum(t.entry_price)}</td>
              <td style="font-weight:700">₹${fmtNum(t.exit_price)}</td>
              <td class="neg-red">₹${fmtNum(t.stop_loss)}</td>
              <td class="pos-green">₹${fmtNum(t.target_1)}</td>
              <td class="pos-green">₹${fmtNum(t.target_2)}</td>
              <td class="${cls}">${pnlPts >= 0 ? '+' : ''}${fmtNum(pnlPts)}</td>
              <td class="${cls}" style="font-weight:700">${pnlRs >= 0 ? '+' : ''}₹${fmtNum(pnlRs)}</td>
              <td>${t.status === 'OPEN' ? '<span class="badge badge-sim">OPEN (Monitoring 15m Timer)</span>' : `<span class="badge badge-demo">${t.exit_reason || 'CLOSED'}</span>`}</td>
              <td>${t.status === 'OPEN' ? `<button onclick="closePaperOrder(${t.id})">Square Off</button>` : '--'}</td>
            </tr>
          `;
        }).join("");
      }
    }

    // Initial load + start auto-poll countdown timer
    refreshData(false);
    toggleAutoRefresh();
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# HTTP Server Request Handler
# ---------------------------------------------------------------------------

class DashboardRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            body = INDEX_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path == "/api/state":
            qs = urllib.parse.parse_qs(parsed.query)
            advance = qs.get("advance", ["0"])[0] == "1"
            state = APP_STATE.step_or_poll(advance_demo=advance)
            self._send_json(state)
            return

        if parsed.path == "/api/download_eval_log":
            qs = urllib.parse.parse_qs(parsed.query)
            fmt = qs.get("format", ["log"])[0].lower()
            logs_dir = BASE_DIR / "logs"
            session_date = (
                str((APP_STATE.last_report or {}).get("session_date") or dt.date.today().isoformat())
            )
            if fmt == "csv":
                target = logs_dir / f"evaluation_trace_{session_date}.csv"
                if not target.exists():
                    target = logs_dir / "evaluation_trace_all.csv"
                content_type = "text/csv; charset=utf-8"
                disp = f'attachment; filename="evaluation_trace_{session_date}.csv"'
            elif fmt == "jsonl":
                target = logs_dir / f"evaluation_trace_{session_date}.jsonl"
                content_type = "application/x-ndjson; charset=utf-8"
                disp = f'attachment; filename="evaluation_trace_{session_date}.jsonl"'
            else:
                target = logs_dir / f"evaluation_trace_{session_date}.log"
                if not target.exists():
                    target = logs_dir / "LATEST_EVALUATION_TRACE.log"
                content_type = "text/plain; charset=utf-8"
                disp = f'inline; filename="evaluation_trace_{session_date}.log"'

            if target.exists():
                body = target.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Disposition", disp)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._send_json({"error": f"Offline evaluation log not found yet at {target}"}, status=404)
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        data = json.loads(raw or "{}")

        if parsed.path == "/api/config":
            if "api_key" in data and data["api_key"]:
                APP_STATE.api_key = str(data["api_key"]).strip()
            if "mode" in data:
                APP_STATE.mode = str(data["mode"])
            if "underlying" in data and data["underlying"] != APP_STATE.underlying:
                APP_STATE.underlying = str(data["underlying"])
                APP_STATE._reset_demo(APP_STATE.underlying)
            if "auto_poll_sec" in data:
                APP_STATE.auto_poll_interval_sec = max(0, int(data["auto_poll_sec"]))
            if data.get("skip_eval"):
                self._send_json({"status": "ok", "auto_poll_sec": APP_STATE.auto_poll_interval_sec})
                return
            state = APP_STATE.step_or_poll(advance_demo=False)
            self._send_json(state)
            return

        if parsed.path == "/api/whatsapp":
            action = data.get("action")
            if action == "CONFIG":
                provider = str(data.get("provider", "gmail")).strip()
                phone = str(data.get("phone", "")).strip()
                key = str(data.get("api_key", "")).strip()
                os.environ["WHATSAPP_ENABLED"] = "true"
                os.environ["WHATSAPP_PROVIDER"] = provider
                if provider == "gmail":
                    if phone:
                        os.environ["GMAIL_USER"] = phone
                        os.environ["GMAIL_TO"] = phone
                    if key:
                        os.environ["GMAIL_APP_PASSWORD"] = key.replace(" ", "")
                else:
                    if phone:
                        os.environ["WHATSAPP_PHONE"] = phone
                    if key:
                        if provider == "webhook":
                            os.environ["WHATSAPP_WEBHOOK_URL"] = key
                        else:
                            os.environ["WHATSAPP_API_KEY"] = key
                self._send_json(APP_STATE._serialize_state(APP_STATE.get_active_store()))
                return
            if action == "SEND_NOW":
                state = APP_STATE.send_manual_whatsapp()
                self._send_json(state)
                return

        if parsed.path == "/api/preplan":
            try:
                state = APP_STATE.save_pre_plan(data)
                self._send_json(state)
            except Exception as exc:
                APP_STATE.last_error = str(exc)
                self._send_json(APP_STATE._serialize_state(APP_STATE.get_active_store()))
            return

        if parsed.path == "/api/trade":
            try:
                action = data.get("action")
                if action == "OPEN":
                    opt_type = str(data.get("option_type", "CE"))
                    state = APP_STATE.create_paper_trade(option_type=opt_type)
                elif action == "CLOSE":
                    trade_id = int(data.get("trade_id", 0))
                    state = APP_STATE.close_paper_trade(trade_id=trade_id)
                else:
                    state = APP_STATE.step_or_poll(advance_demo=False)
                self._send_json(state)
            except Exception as exc:
                APP_STATE.last_error = str(exc)
                self._send_json(APP_STATE._serialize_state(APP_STATE.get_active_store()))
            return

        self._send_json({"error": "Not found"}, status=404)


def _background_auto_poller() -> None:
    """
    Background daemon thread that guarantees automatic 3-minute Option Chain evaluation
    and dynamic offline logging (to logs/evaluation_trace_<YYYY-MM-DD>.log, .csv, .jsonl)
    even when no browser tab is open or the browser tab is minimized/throttled.
    Automatically pauses in LIVE_OPENALGO mode outside NSE market hours (09:15–15:30 IST).
    """
    while True:
        time.sleep(2.0)
        try:
            interval = APP_STATE.auto_poll_interval_sec
            if interval <= 0:
                continue
            if APP_STATE.mode == "LIVE_OPENALGO" and APP_STATE.last_report is not None:
                is_open, _ = check_indian_market_hours()
                if not is_open:
                    continue
            elapsed = time.time() - APP_STATE.last_eval_epoch
            if elapsed >= interval:
                APP_STATE.step_or_poll(advance_demo=True)
        except Exception as exc:
            print(f"  [AUTO-POLLER WARNING] {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="LearnOT Option Buying Web UI Desk")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="Port number (default: 8080)")
    args = parser.parse_args()

    # Run Cycle #1 immediately on startup so offline logs are initialized right away
    APP_STATE.step_or_poll(advance_demo=False)

    # Start background 3-minute auto-poller daemon thread
    poller_thread = threading.Thread(target=_background_auto_poller, name="LearnOT-3m-AutoPoller", daemon=True)
    poller_thread.start()

    server = HTTPServer((args.host, args.port), DashboardRequestHandler)
    print(f"\n======================================================================")
    print(f" LearnOT Option Buying UI Desk is running at: http://{args.host}:{args.port}")
    print(f" Connected OpenAlgo Target                  : {APP_STATE.host}")
    print(f" Auto-Polling & Offline Logger              : ACTIVE (Every {APP_STATE.auto_poll_interval_sec}s / 3m Cycle)")
    print(f" Offline Log Directory                      : {BASE_DIR / 'logs'}")
    print(f"======================================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down UI server.")
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
