# LearnOT Weekly Strategy Learning & Fine-Tuning Tracker

> **Quantitative Rule-Tuning Principle (Anti-Overfitting):**
> Never modify strategy parameters based on a single day (`N = 1`). Log every session's post-market observations, rule-blocker statistics, and candidate hypotheses here. At the end of the trading week (`5 sessions` covering DTE 4 down to DTE 0), review which hypotheses held consistently across the full week before updating [`option_chain_analyzer.py`](../option_chain_analyzer.py).

---

## 📅 Week of 2026-11-02 — Daily Session Tracker

| Session Date | Underlying & Expiry | DTE | Market Regime & Range | Total Setups ($\ge 3/6$) | `6/6` Triggers | Missed Winners ($\ge +12\%$) | Filter Saved Losses ($\le -10\%$) | Top Rule Blockers |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **`2026-11-02` (Day 1)** | `NIFTY 03NOV26` | `1` | Whipsaw + Afternoon V-Rally (`23,218` – `23,441`, `222.5 pts`, VIX `14.4–16.8`) | `89` | `0` | `50` (Avg Max `+45.1%`) | `31` (Avg Saved `-55.3%`) | `R6` (`87x`), `R4` (`79x`), `R2` (`39x`), `R1` (`12x`) |
| **`2026-11-03` (Day 2)** | *Pending* | `0` | *To be logged post-market* | -- | -- | -- | -- | -- |
| **`2026-11-04` (Day 3)** | *Pending* | `4` | *To be logged post-market* | -- | -- | -- | -- | -- |
| **`2026-11-05` (Day 4)** | *Pending* | `3` | *To be logged post-market* | -- | -- | -- | -- | -- |
| **`2026-11-06` (Day 5)** | *Pending* | `2` | *To be logged post-market* | -- | -- | -- | -- | -- |

---

## 🔬 Candidate Hypotheses Under Observation (Do Not Apply Until Week-End Review)

### Hypothesis H1 — `R6: Greeks & Theta` DTE-Adaptive Threshold
- **Day 1 (`2026-11-02`, `DTE = 1`) Observation:**
  - `R6` blocked **`87 out of 89`** setups (`50` Missed Winners) because on `DTE = 1`, ATM premiums (`₹70–₹95`) naturally have a 24-hour Black-Scholes Theta of `37%–52%` of premium (`> 30%` cap), even though `|Delta|` was in the ideal `0.48–0.54` sweet spot.
  - Because intraday option buyers hold for **15–30 minutes** (not 24 hours), actual 15-minute Theta decay was only `~1.8%`.
- **What to Verify Over the Rest of the Week:**
  - Check how `R6` behaves on `DTE = 0` (Expiry Day) vs `DTE = 4, 3, 2` (Fresh Weekly Contract).
  - *Candidate Weekend Adjustment:* Scale `max_theta_pct` by DTE (`<= 20%` for `DTE >= 3`, `<= 32%` for `DTE == 2`, `<= 55%` for `DTE == 1`, `<= 75%` for `DTE == 0`).

### Hypothesis H2 — `R4: Volume Burst` 3-Minute Time-Normalized Rate
- **Day 1 (`2026-11-02`) Observation:**
  - `R4` blocked **`79 out of 89`** setups (`43` Missed Winners, including the `11:43 AM` `23300PE` `+70.0%` move and `14:38 PM` `23300CE` `+26.2%` move).
  - Cause 1: Starting the portal mid-session (`11:25 AM`) put the entire morning's cumulative volume into the first delta bucket, inflating the session average denominator.
  - Cause 2: Manual UI re-evaluations (`< 180s` apart) compared partial-window volume against full 3-minute intervals.
- **What to Verify Over the Rest of the Week:**
  - Observe `vol_burst_ratio` when the portal runs from `09:15 AM` market open without mid-day restarts.
  - *Candidate Weekend Adjustment:* Normalize volume rate per 180 seconds using `ref_3m` (`now_ts - ts >= 150s`) and exclude snapshot `#1`'s cumulative volume from the rolling baseline.

### Hypothesis H3 — `R1: Spot/Basis Trend` Structural Discount Tolerance
- **Day 1 (`2026-11-02`) Observation:**
  - `R1` blocked `12` setups (`5` Missed Winners) when Nifty Spot was above Session VWAP (`+6` to `+140` pts), because `Synthetic Future Basis` dipped to `-17.6` to `-96.1` (below the hardcoded `-15.0` floor).
- **What to Verify Over the Rest of the Week:**
  - Track whether negative synthetic basis on `DTE = 1 / 0` is a structural dividend/expiry artifact or genuine futures selling.

---

## 🏆 Day 1 (`2026-11-02`) Key Positive Validations (Keep Unchanged)

1. **`R1 (Spot vs VWAP) + R2 (Option > Option VWAP & 3m dLTP > 0) + R3 (15m Institutional dOI & Short Covering) + R5 (IV Stability)`:**
   - Accurately identified both major intraday trends at **`4/6 NEAR-MISS`**:
     - **`11:43:24` — `NIFTY03NOV2623300PE` @ `₹90.60`** &rarr; Rallied to **`₹154.05` (`+70.0%`)**.
     - **`14:38:26` — `NIFTY03NOV2623300CE` @ `₹84.70`** &rarr; Rallied to **`₹106.90` (`+26.2%`)**.
2. **`R2` & `R4` Guardrails at Market Turning Points (`FILTER SAVED LOSS`):**
   - Between `13:52` and `14:29` near the `23,220` bottom, `R2` (`PE LTP < VWAP` / `3m dLTP < 0`) blocked `31` late-put entries on `23250PE` and `23300PE` right before those puts crashed **`-55.3%` to `-65.7%`**.
