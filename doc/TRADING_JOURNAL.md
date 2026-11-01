# LearnOT Daily Trading & Fine-Tuning Journal (2026-11-01 — NIFTY)

> **How to Use This Journal:**
> 1. **🌅 Section 0 (Pre-Market Plan vs. Post-Market Deviation):** Compares your morning pre-plan (PDH/PDL, Gap, Bull/Bear Triggers, Bias) against actual market action and your executed trades.
> 2. **✅ What Was Good Today (`Score >= 3/6`):** Which conditions aligned in your favor (with exact numbers).
> 3. **❌ Why It Did Not Meet 6/6:** Which specific rule(s) failed (e.g., PCR, 15m dOI, Volume Burst, or Option VWAP) with exact live numbers.
> 4. **📈 What Happened Next (Outcome Tracking):** How high the option premium moved *after* that snapshot (`Max LTP After` & `Max Gain %`) so you can decide whether to fine-tune a strict condition or keep it.

---

## 0. Pre-Market Plan vs. Post-Market Deviation Review

| Metric | Morning Pre-Plan (`09:08 AM`) | Actual Intraday Outcome (`09:15 AM – 03:30 PM`) | Match / Deviation Verdict |
| :--- | :--- | :--- | :--- |
| **Opening & Range** | Pre-Open: `24492.0` (PDC `24470.0`, PDH `24520.0`, PDL `24390.0`) | Open `24495.0` / High `24536.0` / Low `24495.0` / Last `24536.0` | `FLAT_OPEN (+22.0 pts — Best for Breakout)` |
| **Volatility & OI Walls** | `IDEAL_VOL (13.8 — Standard +25% / +45% Targets)` / Walls: `24400 PE` – `24500 CE` | Spot moved `41.0` pts intraday | `✅ Bull Trigger (24510) CROSSED (High reached 24536.0) ;; 🛡️ Bear Trigger (24440) held (Low 24495.0) ;; Broke above PDH (24520)` |
| **Bias & Trigger Levels** | Bias: **`BULLISH_ABOVE_TRIGGER`** (Bull `>24510` / Bear `<24440`) | Trades Taken: **`0/2`** (PnL: `₹+0.00`) | **`PARTIAL MATCH (85%)`** |
| **Execution vs. Plan** | *Morning Note:* Buy ATM 24500 CE only if Spot crosses 24510 and 24500 Call Writers start covering (3m dOI < 0). | *Post-Market Note:* Waited patiently through 09:21 AM 5/6 setup; entered on 09:24 AM 6/6 breakout above 24510. | 💡 MISSED PLANNED SETUP: Pre-plan trigger + 6/6 Signal fired (CE:1, PE:0), but 0 trades executed ;; ✔️ Trade Count Discipline (0/2 max) |

---

## 1. Fine-Tuning Rule Blocker Summary (Which Condition Held Back Good Trades Today?)

| Condition That Failed | Times Failed (at >=3/6) | Missed Winners (>= +12% Move) | Avg Max Gain After | Fine-Tuning Action |
| :--- | :---: | :---: | :---: | :--- |
| **R4: Volume Burst** | 3 | **2** | `+12.2%` | TUNING CANDIDATE: Blocked 2 winning move(s) (Avg Max +12.2%). Consider relaxing R4: Volume Burst threshold. |
| **R2: Option > VWAP** | 3 | **1** | `+7.2%` | TUNING CANDIDATE: Blocked 1 winning move(s) (Avg Max +7.2%). Consider relaxing R2: Option > VWAP threshold. |
| **R3: Trapped Writers / PCR / dOI** | 3 | **1** | `+7.2%` | TUNING CANDIDATE: Blocked 1 winning move(s) (Avg Max +7.2%). Consider relaxing R3: Trapped Writers / PCR / dOI threshold. |
| **R1: Spot/Basis Trend** | 1 | **0** | `+0.0%` | GOOD GUARDRAIL: Blocked 1 setup(s) (Avg Max +0.0%). |

---

## 2. Setup-by-Setup Breakdown: What Was Good vs. Why It Missed 6/6

### Entry #1 — `21:47:50` | **NIFTY05NOV2624500PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `24495.0` (VWAP `24495.0`) | PCR `0.89` | 3m dOI `+0` (`NEUTRAL`) | 15m PE dOI `+0` vs CE dOI `+0` | Vol Ratio `1.00x` | IV `13.2%` | Delta `-0.46` | Theta Bleed `11.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0))**
  - ✔️ **R5: IV Stability (PE IV 13.20% (3m dIV +0.00%))**
  - ✔️ **R6: Greeks & Theta (|Delta| 0.46, Daily Theta Bleed 11.0% (Max 18%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 98.00 vs VWAP 98.00 (3m dLTP +0.00))**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m CE dOI +0 vs PE dOI +0, PE: NEUTRAL, PCR 0.89)**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 1625 vs AskQty 1450)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹98.00` &rarr; Latest `₹76.00` | **Max LTP After:** `₹98.00` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-22.4%)**

### Entry #2 — `21:47:50` | **NIFTY05NOV2624500CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `24495.0` (VWAP `24495.0`) | PCR `0.89` | 3m dOI `+0` (`NEUTRAL`) | 15m PE dOI `+0` vs CE dOI `+0` | Vol Ratio `1.00x` | IV `12.8%` | Delta `0.54` | Theta Bleed `11.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0))**
  - ✔️ **R5: IV Stability (CE IV 12.80% (3m dIV +0.00%))**
  - ✔️ **R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 11.1% (Max 18%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 104.00 vs VWAP 104.00 (3m dLTP +0.00))**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m PE dOI +0 vs CE dOI +0, CE: NEUTRAL, PCR 0.89)**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 1950 vs AskQty 1300)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹104.00` &rarr; Latest `₹126.50` | **Max LTP After:** `₹126.50` (**`+21.6%`**) &rarr; **MISSED WINNER (+21.6% -> Tune Missing Rule!)**

### Entry #3 — `21:50:50` | **NIFTY05NOV2624500CE** (CE) — **5/6** [🟡 NEAR-MISS (5/6)]
* **Option Chain Context:** Spot `24508.0` (VWAP `24501.5`) | PCR `0.96` | 3m dOI `+20,000` (`LONG_BUILDUP`) | 15m PE dOI `+1,070,000` vs CE dOI `+100,000` | Vol Ratio `1.00x` | IV `12.9%` | Delta `0.54` | Theta Bleed `10.5%`
* **✅ What Was Good Today (5 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 24508.0 vs VWAP 24501.5 (Basis +6.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 110.00 vs VWAP 105.20 (3m dLTP +6.00))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +1,070,000 vs CE dOI +100,000, CE: LONG_BUILDUP, PCR 0.96)**
  - ✔️ **R5: IV Stability (CE IV 12.90% (3m dIV +0.10%))**
  - ✔️ **R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 10.5% (Max 18%))**
* **❌ Why It Did Not Meet 6/6 (1 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 1950 vs AskQty 1300)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹110.00` &rarr; Latest `₹126.50` | **Max LTP After:** `₹126.50` (**`+15.0%`**) &rarr; **MISSED WINNER (+15.0% -> Tune Missing Rule!)**

### Entry #4 — `21:53:50` | **NIFTY05NOV2624500PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `24536.0` (VWAP `24513.0`) | PCR `1.09` | 3m dOI `+700,000` (`SHORT_BUILDUP`) | 15m PE dOI `+2,500,000` vs CE dOI `-360,000` | Vol Ratio `1.38x` | IV `12.9%` | Delta `-0.46` | Theta Bleed `14.2%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.38x, BidQty 1625 vs AskQty 1450)**
  - ✔️ **R5: IV Stability (PE IV 12.90% (3m dIV -0.20%))**
  - ✔️ **R6: Greeks & Theta (|Delta| 0.46, Daily Theta Bleed 14.2% (Max 18%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 24536.0 vs VWAP 24513.0 (Basis +8.0))**
  - ❌ **R2: Option > VWAP (PE LTP 76.00 vs VWAP 90.90 (3m dLTP -15.00))**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m CE dOI -360,000 vs PE dOI +2,500,000, PE: SHORT_BUILDUP, PCR 1.09)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹76.00` &rarr; Latest `₹76.00` | **Max LTP After:** `₹76.00` (**`+0.0%`**) &rarr; **NEW ENTRY (Tracking...)**

### Entry #5 — `21:53:50` | **NIFTY05NOV2624500CE** (CE) — **6/6** [🟢 FULL 6/6 TRIGGER]
* **Option Chain Context:** Spot `24536.0` (VWAP `24513.0`) | PCR `1.09` | 3m dOI `-340,000` (`SHORT_COVERING`) | 15m PE dOI `+2,500,000` vs CE dOI `-360,000` | Vol Ratio `2.50x` | IV `13.4%` | Delta `0.54` | Theta Bleed `9.1%`
* **✅ What Was Good Today (6 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 24536.0 vs VWAP 24513.0 (Basis +8.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 126.50 vs VWAP 112.30 (3m dLTP +16.50))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +2,500,000 vs CE dOI -360,000, CE: SHORT_COVERING, PCR 1.09)**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.50x, BidQty 1950 vs AskQty 1300)**
  - ✔️ **R5: IV Stability (CE IV 13.40% (3m dIV +0.50%))**
  - ✔️ **R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 9.1% (Max 18%))**
* **❌ Why It Did Not Meet 6/6:** *None — All 6 conditions were satisfied and trade signal fired!*
* **📈 Forward Outcome & Verdict:** Entry LTP `₹126.50` &rarr; Latest `₹126.50` | **Max LTP After:** `₹126.50` (**`+0.0%`**) &rarr; **6/6 TRIGGERED (0.0%)**

---

## 3. Quick Comparison Table (`Score >= 3/6`)

| Time | Symbol | Side | Score | Entry LTP | Max LTP After | Max Gain % | Verdict | What Was Good (Passed) | Why It Missed 6/6 (Failed) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| `21:47:50` | **NIFTY05NOV2624500PE** | PE | **3/6** | ₹98.00 | ₹98.00 | **`+0.0%`** | **FILTER SAVED LOSS (-22.4%)** | R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0)) ;; R5: IV Stability (PE IV 13.20% (3m dIV +0.00%)) ;; R6: Greeks & Theta (/Delta/ 0.46, Daily Theta Bleed 11.0% (Max 18%)) | R2: Option > VWAP (PE LTP 98.00 vs VWAP 98.00 (3m dLTP +0.00)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +0 vs PE dOI +0, PE: NEUTRAL, PCR 0.89) ;; R4: Volume Burst (Vol Ratio 1.00x, BidQty 1625 vs AskQty 1450) |
| `21:47:50` | **NIFTY05NOV2624500CE** | CE | **3/6** | ₹104.00 | ₹126.50 | **`+21.6%`** | **MISSED WINNER (+21.6% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0)) ;; R5: IV Stability (CE IV 12.80% (3m dIV +0.00%)) ;; R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 11.1% (Max 18%)) | R2: Option > VWAP (CE LTP 104.00 vs VWAP 104.00 (3m dLTP +0.00)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +0 vs CE dOI +0, CE: NEUTRAL, PCR 0.89) ;; R4: Volume Burst (Vol Ratio 1.00x, BidQty 1950 vs AskQty 1300) |
| `21:50:50` | **NIFTY05NOV2624500CE** | CE | **5/6** | ₹110.00 | ₹126.50 | **`+15.0%`** | **MISSED WINNER (+15.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 24508.0 vs VWAP 24501.5 (Basis +6.0)) ;; R2: Option > VWAP (CE LTP 110.00 vs VWAP 105.20 (3m dLTP +6.00)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +1,070,000 vs CE dOI +100,000, CE: LONG_BUILDUP, PCR 0.96) ;; R5: IV Stability (CE IV 12.90% (3m dIV +0.10%)) ;; R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 10.5% (Max 18%)) | R4: Volume Burst (Vol Ratio 1.00x, BidQty 1950 vs AskQty 1300) |
| `21:53:50` | **NIFTY05NOV2624500PE** | PE | **3/6** | ₹76.00 | ₹76.00 | **`+0.0%`** | **NEW ENTRY (Tracking...)** | R4: Volume Burst (Vol Ratio 1.38x, BidQty 1625 vs AskQty 1450) ;; R5: IV Stability (PE IV 12.90% (3m dIV -0.20%)) ;; R6: Greeks & Theta (/Delta/ 0.46, Daily Theta Bleed 14.2% (Max 18%)) | R1: Spot/Basis Trend (Spot 24536.0 vs VWAP 24513.0 (Basis +8.0)) ;; R2: Option > VWAP (PE LTP 76.00 vs VWAP 90.90 (3m dLTP -15.00)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -360,000 vs PE dOI +2,500,000, PE: SHORT_BUILDUP, PCR 1.09) |
| `21:53:50` | **NIFTY05NOV2624500CE** | CE | **6/6** | ₹126.50 | ₹126.50 | **`+0.0%`** | **6/6 TRIGGERED (0.0%)** | R1: Spot/Basis Trend (Spot 24536.0 vs VWAP 24513.0 (Basis +8.0)) ;; R2: Option > VWAP (CE LTP 126.50 vs VWAP 112.30 (3m dLTP +16.50)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +2,500,000 vs CE dOI -360,000, CE: SHORT_COVERING, PCR 1.09) ;; R4: Volume Burst (Vol Ratio 2.50x, BidQty 1950 vs AskQty 1300) ;; R5: IV Stability (CE IV 13.40% (3m dIV +0.50%)) ;; R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 9.1% (Max 18%)) | NONE (All 6 Met!) |

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
