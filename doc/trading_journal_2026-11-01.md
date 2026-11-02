# LearnOT Daily Trading & Fine-Tuning Journal (2026-11-01 — NIFTY)

> **How to Use This Journal:**
> 1. **🌅 Section 0 (Pre-Market Sentiment Signal vs. Post-Market Deviation):** Synthesizes GIFT/SGX Nifty, Global Sentiment, Prev Day PCR (Reversal vs Trend), and India VIX (`13.5–16.5` Goldilocks vs High-IV No-Trade) into a Pre-Market Signal and audits how your trades matched or deviated.
> 2. **✅ What Was Good Today (`Score >= 3/6`):** Which conditions aligned in your favor (with exact numbers).
> 3. **❌ Why It Did Not Meet 6/6:** Which specific rule(s) failed (e.g., PCR, 15m dOI, Volume Burst, or Option VWAP) with exact live numbers.
> 4. **📈 What Happened Next (Outcome Tracking):** How high the option premium moved *after* that snapshot (`Max LTP After` & `Max Gain %`) so you can decide whether to fine-tune a strict condition or keep it.

---

## 0. Pre-Market Sentiment Signal vs. Post-Market Deviation Review

| Metric | Morning Pre-Market Sentiment (`09:00 AM`) | Actual Intraday Outcome (`09:15 AM – 03:30 PM`) | System Signal & Deviation Verdict |
| :--- | :--- | :--- | :--- |
| **GIFT Nifty & Global Cues** | GIFT Gap: `+32.0` pts / Global: `NEUTRAL_MIXED` / FII: `FII_NET_SHORT` | Open `23053.1` / High `23053.1` / Low `23053.1` / Close `23053.1` | **`GAP-UP / FLAT OPEN INTO PROFIT-BOOKING REVERSAL (Prev PCR 1.54 Overbought)`** |
| **Prev Day PCR & VIX Regime** | Prev Day PCR: **`1.54`** / India VIX: **`15.2`** (`NORMAL_DAY`) | Intraday Range: `0.0` pts (Walls: `22800 PE` – `23200 CE`) | `🟢 GOLDILOCKS OPTION BUYING DAY (VIX 15.2 in 13.5–16.5 Sweet Spot: No IV bloat, steady Gamma expansion, ideal for +25% / +45% targets!)` |
| **System Pre-Market Signal** | **`🔄 BEARISH REVERSAL WATCH (Prev PCR 1.54 High -> Do NOT chase Gap-Up CE; Buy ATM PE if Spot breaks below Opening 15m Low / VWAP)`** | `✅ Bull Trigger (23050) CROSSED (High 23053.1) ;; 🛡️ Bear Trigger (23025) held (Low 23053.1)` | PDH `23078` / PDL `22993` / PDC `23033` |
| **Planned Bias & Triggers** | Bias: **`BEARISH_BELOW_TRIGGER`** (Bull `>23050` / Bear `<23025`) | Trades Taken: **`0/3`** (PnL: `₹+0.00`) | **`PLAN ALIGNED (100% Discipline)`** |
| **Execution vs. Pre-Plan** | *Morning Note:* Prev Day PCR 1.54 is extreme overbought (>1.45)! Avoid chasing Gap-Up CE; wait for VWAP breakdown to buy ATM PE. | *Post-Market Note:* Add reflection in Web UI Portal | ✔️ Trade Count Discipline (0/3 max) |

---

## 1. Fine-Tuning Rule Blocker Summary (Which Condition Held Back Good Trades Today?)

*No near-miss (`3/6` to `5/6`) setups recorded yet in this session.*

---

## 2. Setup-by-Setup Breakdown: What Was Good vs. Why It Missed 6/6

---

## 3. Quick Comparison Table (`Score >= 3/6`)

| Time | Symbol | Side | Score | Entry LTP | Max LTP After | Max Gain % | Verdict | What Was Good (Passed) | Why It Missed 6/6 (Failed) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |

---

## 4. End-of-Day Fine-Tuning Guide (When to Adjust a Rule)

1. **If `R3: Trapped Writers / PCR / dOI` blocked 3+ winning moves (`MISSED WINNER`):**
   * *Why it happens:* On strong trending mornings, 15m $\Delta\text{OI}$ builds up before overall PCR crosses `0.95` (for CE) or `1.05` (for PE).
   * *Fine-Tune:* Relax the PCR check in `evaluate_checklist()` from `0.95` to `0.85` when 15m $\Delta\text{OI}$ and `SHORT_COVERING` are already aligned.
2. **If `R4: Volume Burst` blocked 3+ winning moves (`MISSED WINNER`):**
   * *Why it happens:* Steady institutional accumulation can happen at `1.15x–1.25x` volume ratio before the `1.30x` spike.
   * *Fine-Tune:* Lower the Volume Burst threshold from `1.30x` to `1.15x` when `BidQty > AskQty`.
3. **If a missing rule shows `FILTER SAVED LOSS`:**
   * *Keep that rule strict!* It prevented you from buying into Theta decay or an IV crush.
