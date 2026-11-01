# LearnOT — Nifty & BankNifty Option Buying System (OpenAlgo + Zerodha)

A mechanical **Intraday Option Buying Analyzer, Signal Engine, Trading Desk UI & Auto-Journal** built for **NSE/BSE Index Options (`NIFTY`, `BANKNIFTY`, `SENSEX`)** using **[OpenAlgo](https://openalgo.in/) (`http://127.0.0.1:5000`)** connected with **Zerodha**.

---

## Key Features

1. **3-Minute (`180s`) NSE Open Interest Engine:** Polls OpenAlgo every 3 minutes to match NSE's exact Open Interest broadcast cycle and computes **3m $\Delta\text{OI}$**, **15m $\Delta\text{OI}$**, **Session VWAP**, **Synthetic Future Basis**, and **ATM Straddle Decay** in local SQLite.
2. **4-Quadrant OI Matrix:** Automatically classifies every Call and Put strike into `SHORT_COVERING` (Trapped Option Writers panicking — your #1 Option Buying edge), `LONG_BUILDUP`, `SHORT_BUILDUP`, or `LONG_UNWINDING`.
3. **6-Point Mechanical "Gamma Blast" Checklist:** Scores both Bullish ATM CE and Bearish ATM PE out of 6, with built-in **Anti-Theta** and **Anti-IV-Crush** guardrails.
4. **Instant Official Gmail Setup Alerts:** Sends a rich HTML + Plain-Text Trade Card (`Entry LTP`, `-18% Hard SL`, `+25%/+45% Targets`, `15m Time-Stop`) to your Gmail whenever a `6/6` setup triggers.
5. **Auto-Generated Fine-Tuning Trading Journal (`Score >= 3/6`):** Automatically records every snapshot where at least **3 out of 6 conditions** are met into [`doc/TRADING_JOURNAL.md`](doc/TRADING_JOURNAL.md), detailing **What Was Good Today** vs. **Why It Missed 6/6**, and tracks forward option LTP (`Max Gain %`) to identify `MISSED WINNER` vs. `FILTER SAVED LOSS`.
6. **Zero-Dependency Web UI Trading Desk (`http://127.0.0.1:8080`):** Live Option Chain, 6-Point Checklist, OI Wall Bars, Gmail Alert Config, Fine-Tuning Journal Table, and Practice Trade Log with a **15-Minute Anti-Theta Time-Stop**.

---

## Documentation

* **[Strategy Blueprint & Daily Rulebook](STRATEGY_BLUEPRINT_AND_RULEBOOK.md)** — Complete explanation of the 6-Point Trapped Seller strategy, Position Sizing, and Anti-Theta rules.
* **[How It Works (Architecture & Workflow)](doc/HOW_IT_WORKS.md)** — End-to-end architecture diagram and step-by-step pipeline guide.
* **[Daily Trading & Fine-Tuning Journal](doc/TRADING_JOURNAL.md)** — Auto-generated journal of all $\ge 3/6$ setups and rule-blocker insights.

---

## Quick Start (Using `uv`)

### 1. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` to add your `OPENALGO_API_KEY` (from `http://127.0.0.1:5000/apikey`), `GMAIL_USER`, and 16-character `GMAIL_APP_PASSWORD` (from [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)).

### 2. Launch the Interactive Web UI Trading Desk
```bash
uv run dashboard_ui.py --port 8080
```
Open **`http://127.0.0.1:8080`** in your browser. Works 24/7 in **Practice Simulator (Demo)** mode and during market hours (`09:15 AM – 03:30 PM IST`) in **Live OpenAlgo** mode.

### 3. Run Terminal Analyzer / Simulation
```bash
# Run 3-step Trapped-Seller Simulation & Test Gmail Alert (works anytime 24/7):
uv run option_chain_analyzer.py --test-email

# Run Live 3-Minute Option Chain Analyzer during market hours (09:15 AM - 03:30 PM IST):
uv run option_chain_analyzer.py --underlying NIFTY --interval 180 --auto-paper
```
