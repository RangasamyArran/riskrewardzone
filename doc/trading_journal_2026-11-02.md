# LearnOT Daily Trading & Fine-Tuning Journal (2026-11-02 — NIFTY)

> **How to Use This Journal:**
> 1. **🌅 Section 0 (Pre-Market Sentiment Signal vs. Post-Market Deviation):** Synthesizes GIFT/SGX Nifty, Global Sentiment, Prev Day PCR (Reversal vs Trend), and India VIX (`13.5–16.5` Goldilocks vs High-IV No-Trade) into a Pre-Market Signal and audits how your trades matched or deviated.
> 2. **✅ What Was Good Today (`Score >= 3/6`):** Which conditions aligned in your favor (with exact numbers).
> 3. **❌ Why It Did Not Meet 6/6:** Which specific rule(s) failed (e.g., PCR, 15m dOI, Volume Burst, or Option VWAP) with exact live numbers.
> 4. **📈 What Happened Next (Outcome Tracking):** How high the option premium moved *after* that snapshot (`Max LTP After` & `Max Gain %`) so you can decide whether to fine-tune a strict condition or keep it.

---

## 0. Pre-Market Sentiment Signal vs. Post-Market Deviation Review

| Metric | Morning Pre-Market Sentiment (`06:30 AM – 09:08 AM`) | Actual Intraday Outcome (`09:15 AM – 03:30 PM`) | System Signal & Deviation Verdict |
| :--- | :--- | :--- | :--- |
| **🌍 Global Indicators (`6:30–8:00 AM`)** | GIFT Gap: `+22.0` pts / US Close: `MILD_BULLISH` / Asia (Nikkei/HangSeng): `POSITIVE_MOMENTUM` | Open `23313.0` / High `23440.8` / Low `23218.2` / Close `23440.8` | **`BULLISH CONFLUENCE OPEN (+22 pts / 7/8 Bullish Cues)`** |
| **📊 Macro & Institutional Triggers** | FII/DII: `FII_NET_LONG` / Brent Crude: `COOLING_BULLISH` / DXY & USDINR: `COOLING_INR_STRONG` | Intraday Range: `222.5` pts (Walls: `23300 PE` – `23300 CE`) | Bull Cues: `7/8` / Bear Cues: `0/8` |
| **🇮🇳 Domestic (`9:00–9:08 AM`) & VIX/PCR** | 09:08 Adv/Dec: `MODERATE_ADVANCES` / India VIX: **`14.4`** / Prev PCR: **`1.18`** | `✅ Bull Trigger (23325) CROSSED (High 23440.8) ;; 🔻 Bear Trigger (23293) CROSSED (Low 23218.2) ;; Broke PDH (23338) ;; Broke PDL (23248)` | `🟢 GOLDILOCKS OPTION BUYING DAY (VIX 14.4 in 13.5–16.5 Sweet Spot: Steady IV, no crush, ideal for +25% / +45% Gamma Blast targets!)` |
| **🧠 System Pre-Market Signal** | **`🚀 BULLISH CONTINUATION SIGNAL (7/8 Pre-Market Cues Bullish + VIX 14.4 -> Buy ATM CE above Bull Trigger)`** | PDH `23338` / PDL `23248` / PDC `23291` | 09:08 Equilibrium: `23313.0` |
| **🎯 Planned Bias & Triggers** | Bias: **`BULLISH_ABOVE_TRIGGER`** (Bull `>23325` / Bear `<23293`) | Trades Taken: **`0/2`** (PnL: `₹+0.00`) | **`PLAN ALIGNED (100% Discipline)`** |
| **📓 Execution vs. Pre-Plan** | *Morning Note:* VIX 14.4 (Goldilocks 14-16 zone) + Prev PCR 1.18 Bullish -> Buy ATM CE above 23325. | *Post-Market Note:* Add reflection in Web UI Portal | ✔️ Trade Count Discipline (0/2 max) |

---

## 1. Fine-Tuning Rule Blocker Summary (Which Condition Held Back Good Trades Today?)

| Condition That Failed | Times Failed (at >=3/6) | Missed Winners (>= +12% Move) | Avg Max Gain After | Fine-Tuning Action |
| :--- | :---: | :---: | :---: | :--- |
| **R6: Greeks & Theta** | 87 | **50** | `+27.0%` | TUNING CANDIDATE: Blocked 50 winning move(s) (Avg Max +27.0%). Consider relaxing R6: Greeks & Theta threshold. |
| **R4: Volume Burst** | 79 | **43** | `+24.6%` | TUNING CANDIDATE: Blocked 43 winning move(s) (Avg Max +24.6%). Consider relaxing R4: Volume Burst threshold. |
| **R2: Option > VWAP** | 39 | **17** | `+26.0%` | TUNING CANDIDATE: Blocked 17 winning move(s) (Avg Max +26.0%). Consider relaxing R2: Option > VWAP threshold. |
| **R1: Spot/Basis Trend** | 12 | **5** | `+28.2%` | TUNING CANDIDATE: Blocked 5 winning move(s) (Avg Max +28.2%). Consider relaxing R1: Spot/Basis Trend threshold. |
| **R3: Trapped Writers / PCR / dOI** | 1 | **1** | `+76.5%` | TUNING CANDIDATE: Blocked 1 winning move(s) (Avg Max +76.5%). Consider relaxing R3: Trapped Writers / PCR / dOI threshold. |
| **R5: IV Stability** | 1 | **1** | `+30.5%` | TUNING CANDIDATE: Blocked 1 winning move(s) (Avg Max +30.5%). Consider relaxing R5: IV Stability threshold. |

---

## 2. Setup-by-Setup Breakdown: What Was Good vs. Why It Missed 6/6

### Entry #1 — `11:25:06` | **NIFTY03NOV2623350CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23327.4` (VWAP `23320.2`) | PCR `0.89` | 3m dOI `+1,302,470` (`LONG_BUILDUP`) | 15m PE dOI `+14,037,725` vs CE dOI `-4,103,645` | Vol Ratio `1.00x` | IV `16.6%` | Delta `0.44` | Theta Bleed `52.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23327.4 vs VWAP 23320.2 (Basis -12.7))**
  - ✔️ **R2: Option > VWAP (CE LTP 70.75 vs VWAP 69.69 (3m dLTP +2.00))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +14,037,725 vs CE dOI -4,103,645, CE: LONG_BUILDUP, PCR 0.89)**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 4095 vs AskQty 5070)**
  - ❌ **R5: IV Stability (CE IV 16.56% (3m dIV -0.37%))**
  - ❌ **R6: Greeks & Theta (Delta 0.44, Daily Theta Bleed 52.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹70.75` &rarr; Latest `₹70.00` | **Max LTP After:** `₹92.35` (**`+30.5%`**) &rarr; **MISSED WINNER (+30.5% -> Tune Missing Rule!)**

### Entry #2 — `11:28:21` | **NIFTY03NOV2623350CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23330.7` (VWAP `23324.3`) | PCR `0.90` | 3m dOI `+135,005` (`LONG_BUILDUP`) | 15m PE dOI `+16,006,250` vs CE dOI `-3,867,760` | Vol Ratio `0.04x` | IV `16.6%` | Delta `0.43` | Theta Bleed `52.6%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R2: Option > VWAP (CE LTP 70.30 vs VWAP 69.69 (3m dLTP +0.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +16,006,250 vs CE dOI -3,867,760, CE: LONG_BUILDUP, PCR 0.90)**
  - ✔️ **R5: IV Stability (CE IV 16.63% (3m dIV +0.07%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23330.7 vs VWAP 23324.3 (Basis -17.6))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.04x, BidQty 975 vs AskQty 3120)**
  - ❌ **R6: Greeks & Theta (Delta 0.43, Daily Theta Bleed 52.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹70.30` &rarr; Latest `₹70.00` | **Max LTP After:** `₹92.35` (**`+31.4%`**) &rarr; **MISSED WINNER (+31.4% -> Tune Missing Rule!)**

### Entry #3 — `11:31:21` | **NIFTY03NOV2623350CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23338.0` (VWAP `23327.1`) | PCR `0.88` | 3m dOI `+181,025` (`LONG_BUILDUP`) | 15m PE dOI `+14,247,220` vs CE dOI `-2,614,755` | Vol Ratio `0.12x` | IV `16.4%` | Delta `0.46` | Theta Bleed `49.3%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23338.0 vs VWAP 23327.1 (Basis -12.8))**
  - ✔️ **R2: Option > VWAP (CE LTP 74.70 vs VWAP 69.78 (3m dLTP +4.40))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +14,247,220 vs CE dOI -2,614,755, CE: LONG_BUILDUP, PCR 0.88)**
  - ✔️ **R5: IV Stability (CE IV 16.45% (3m dIV -0.18%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.12x, BidQty 3965 vs AskQty 5980)**
  - ❌ **R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 49.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹74.70` &rarr; Latest `₹70.00` | **Max LTP After:** `₹92.35` (**`+23.6%`**) &rarr; **MISSED WINNER (+23.6% -> Tune Missing Rule!)**

### Entry #4 — `11:37:22` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23313.8` (VWAP `23323.9`) | PCR `1.07` | 3m dOI `+387,725` (`LONG_BUILDUP`) | 15m PE dOI `+16,558,750` vs CE dOI `-2,266,745` | Vol Ratio `0.33x` | IV `16.8%` | Delta `-0.50` | Theta Bleed `43.3%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23313.8 vs VWAP 23323.9 (Basis -13.3))**
  - ✔️ **R2: Option > VWAP (PE LTP 87.30 vs VWAP 86.91 (3m dLTP +1.70))**
  - ✔️ **R5: IV Stability (PE IV 16.76% (3m dIV -0.05%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m CE dOI -2,266,745 vs PE dOI +16,558,750, PE: LONG_BUILDUP, PCR 1.07)**
  - ❌ **R4: Volume Burst (Vol Ratio 0.33x, BidQty 260 vs AskQty 1625)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.50, Daily Theta Bleed 43.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹87.30` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+76.5%`**) &rarr; **MISSED WINNER (+76.5% -> Tune Missing Rule!)**

### Entry #5 — `11:40:23` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23311.0` (VWAP `23322.3`) | PCR `1.05` | 3m dOI `-351,585` (`LONG_UNWINDING`) | 15m PE dOI `+1,055,535` vs CE dOI `+2,891,005` | Vol Ratio `0.33x` | IV `16.7%` | Delta `-0.49` | Theta Bleed `43.5%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23311.0 vs VWAP 23322.3 (Basis -9.2))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +2,891,005 vs PE dOI +1,055,535, PE: LONG_UNWINDING, PCR 1.05)**
  - ✔️ **R5: IV Stability (PE IV 16.70% (3m dIV -0.06%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 86.60 vs VWAP 86.91 (3m dLTP -0.70))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.33x, BidQty 3445 vs AskQty 2535)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.49, Daily Theta Bleed 43.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹86.60` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+77.9%`**) &rarr; **MISSED WINNER (+77.9% -> Tune Missing Rule!)**

### Entry #6 — `11:43:24` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23307.9` (VWAP `23320.7`) | PCR `1.04` | 3m dOI `+23,530` (`LONG_BUILDUP`) | 15m PE dOI `-238,810` vs CE dOI `+3,198,520` | Vol Ratio `0.32x` | IV `16.7%` | Delta `-0.51` | Theta Bleed `41.7%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23307.9 vs VWAP 23320.7 (Basis -13.9))**
  - ✔️ **R2: Option > VWAP (PE LTP 90.60 vs VWAP 86.99 (3m dLTP +4.00))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,198,520 vs PE dOI -238,810, PE: LONG_BUILDUP, PCR 1.04)**
  - ✔️ **R5: IV Stability (PE IV 16.73% (3m dIV +0.03%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.32x, BidQty 2405 vs AskQty 4225)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.51, Daily Theta Bleed 41.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹90.60` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+70.0%`**) &rarr; **MISSED WINNER (+70.0% -> Tune Missing Rule!)**

### Entry #7 — `11:46:25` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23307.2` (VWAP `23319.4`) | PCR `1.01` | 3m dOI `-187,720` (`SHORT_COVERING`) | 15m PE dOI `-58,890` vs CE dOI `+3,661,450` | Vol Ratio `0.47x` | IV `16.7%` | Delta `-0.51` | Theta Bleed `41.4%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23307.2 vs VWAP 23319.4 (Basis -14.8))**
  - ✔️ **R2: Option > VWAP (PE LTP 91.10 vs VWAP 87.10 (3m dLTP +0.50))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,661,450 vs PE dOI -58,890, PE: SHORT_COVERING, PCR 1.01)**
  - ✔️ **R5: IV Stability (PE IV 16.69% (3m dIV -0.04%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.47x, BidQty 2665 vs AskQty 1820)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.51, Daily Theta Bleed 41.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹91.10` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+69.1%`**) &rarr; **MISSED WINNER (+69.1% -> Tune Missing Rule!)**

### Entry #8 — `11:49:26` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23294.5` (VWAP `23317.1`) | PCR `0.97` | 3m dOI `-1,042,600` (`SHORT_COVERING`) | 15m PE dOI `-4,639,830` vs CE dOI `+5,314,790` | Vol Ratio `0.61x` | IV `16.7%` | Delta `-0.53` | Theta Bleed `39.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23294.5 vs VWAP 23317.1 (Basis -12.7))**
  - ✔️ **R2: Option > VWAP (PE LTP 96.55 vs VWAP 87.42 (3m dLTP +5.45))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +5,314,790 vs PE dOI -4,639,830, PE: SHORT_COVERING, PCR 0.97)**
  - ✔️ **R5: IV Stability (PE IV 16.70% (3m dIV +0.01%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.61x, BidQty 910 vs AskQty 10075)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.53, Daily Theta Bleed 39.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹96.55` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+59.5%`**) &rarr; **MISSED WINNER (+59.5% -> Tune Missing Rule!)**

### Entry #9 — `11:52:27` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23288.8` (VWAP `23314.7`) | PCR `0.93` | 3m dOI `-823,810` (`SHORT_COVERING`) | 15m PE dOI `-7,647,770` vs CE dOI `+5,486,130` | Vol Ratio `0.62x` | IV `16.8%` | Delta `-0.54` | Theta Bleed `37.4%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23288.8 vs VWAP 23314.7 (Basis -13.9))**
  - ✔️ **R2: Option > VWAP (PE LTP 100.90 vs VWAP 87.85 (3m dLTP +4.35))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +5,486,130 vs PE dOI -7,647,770, PE: SHORT_COVERING, PCR 0.93)**
  - ✔️ **R5: IV Stability (PE IV 16.78% (3m dIV +0.08%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.62x, BidQty 4745 vs AskQty 2210)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.54, Daily Theta Bleed 37.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹100.90` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+52.7%`**) &rarr; **MISSED WINNER (+52.7% -> Tune Missing Rule!)**

### Entry #10 — `11:55:28` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23298.8` (VWAP `23313.5`) | PCR `0.86` | 3m dOI `-1,565,980` (`LONG_UNWINDING`) | 15m PE dOI `-10,776,675` vs CE dOI `+8,062,405` | Vol Ratio `0.54x` | IV `16.9%` | Delta `-0.53` | Theta Bleed `39.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23298.8 vs VWAP 23313.5 (Basis -17.5))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,062,405 vs PE dOI -10,776,675, PE: LONG_UNWINDING, PCR 0.86)**
  - ✔️ **R5: IV Stability (PE IV 16.90% (3m dIV +0.12%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 97.70 vs VWAP 88.10 (3m dLTP -3.20))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.54x, BidQty 65 vs AskQty 1235)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.53, Daily Theta Bleed 39.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹97.70` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+57.7%`**) &rarr; **MISSED WINNER (+57.7% -> Tune Missing Rule!)**

### Entry #11 — `11:58:29` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23309.3` (VWAP `23313.2`) | PCR `0.84` | 3m dOI `+79,820` (`SHORT_BUILDUP`) | 15m PE dOI `-11,520,535` vs CE dOI `+9,684,155` | Vol Ratio `0.30x` | IV `16.8%` | Delta `-0.52` | Theta Bleed `40.2%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23309.3 vs VWAP 23313.2 (Basis -23.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +9,684,155 vs PE dOI -11,520,535, PE: SHORT_BUILDUP, PCR 0.84)**
  - ✔️ **R5: IV Stability (PE IV 16.79% (3m dIV -0.11%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 94.70 vs VWAP 88.19 (3m dLTP -3.00))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.30x, BidQty 65 vs AskQty 65)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.52, Daily Theta Bleed 40.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹94.70` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+62.7%`**) &rarr; **MISSED WINNER (+62.7% -> Tune Missing Rule!)**

### Entry #12 — `12:05:21` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23303.5` (VWAP `23313.1`) | PCR `0.82` | 3m dOI `+249,600` (`LONG_BUILDUP`) | 15m PE dOI `-7,329,270` vs CE dOI `+7,816,380` | Vol Ratio `0.85x` | IV `16.7%` | Delta `-0.52` | Theta Bleed `40.4%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23303.5 vs VWAP 23313.1 (Basis -17.1))**
  - ✔️ **R2: Option > VWAP (PE LTP 93.80 vs VWAP 88.36 (3m dLTP +5.45))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +7,816,380 vs PE dOI -7,329,270, PE: LONG_BUILDUP, PCR 0.82)**
  - ✔️ **R5: IV Stability (PE IV 16.71% (3m dIV +0.07%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.85x, BidQty 520 vs AskQty 2275)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.52, Daily Theta Bleed 40.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹93.80` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+64.2%`**) &rarr; **MISSED WINNER (+64.2% -> Tune Missing Rule!)**

### Entry #13 — `12:06:14` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23304.8` (VWAP `23312.6`) | PCR `0.81` | 3m dOI `+351,455` (`LONG_BUILDUP`) | 15m PE dOI `-5,066,490` vs CE dOI `+6,977,295` | Vol Ratio `0.13x` | IV `16.6%` | Delta `-0.52` | Theta Bleed `41.1%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23304.8 vs VWAP 23312.6 (Basis -15.6))**
  - ✔️ **R2: Option > VWAP (PE LTP 91.95 vs VWAP 88.38 (3m dLTP +3.60))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,977,295 vs PE dOI -5,066,490, PE: LONG_BUILDUP, PCR 0.81)**
  - ✔️ **R5: IV Stability (PE IV 16.64% (3m dIV +0.00%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.13x, BidQty 650 vs AskQty 2600)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.52, Daily Theta Bleed 41.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹91.95` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+67.5%`**) &rarr; **MISSED WINNER (+67.5% -> Tune Missing Rule!)**

### Entry #14 — `12:09:14` | **NIFTY03NOV2623300CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23315.1` (VWAP `23312.8`) | PCR `0.83` | 3m dOI `-615,485` (`SHORT_COVERING`) | 15m PE dOI `-711,555` vs CE dOI `+791,570` | Vol Ratio `0.84x` | IV `17.0%` | Delta `0.51` | Theta Bleed `42.5%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23315.1 vs VWAP 23312.8 (Basis -9.6))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -711,555 vs CE dOI +791,570, CE: SHORT_COVERING, PCR 0.83)**
  - ✔️ **R5: IV Stability (CE IV 17.03% (3m dIV +0.39%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 91.25 vs VWAP 92.09 (3m dLTP +10.10))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.84x, BidQty 2795 vs AskQty 1170)**
  - ❌ **R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 42.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹91.25` &rarr; Latest `₹96.95` | **Max LTP After:** `₹121.35` (**`+33.0%`**) &rarr; **MISSED WINNER (+33.0% -> Tune Missing Rule!)**

### Entry #15 — `12:12:14` | **NIFTY03NOV2623350CE** (CE) — **5/6** [🟡 NEAR-MISS (5/6)]
* **Option Chain Context:** Spot `23335.1` (VWAP `23313.9`) | PCR `0.74` | 3m dOI `-1,897,220` (`SHORT_COVERING`) | 15m PE dOI `-615,095` vs CE dOI `-9,068,085` | Vol Ratio `1.61x` | IV `17.3%` | Delta `0.49` | Theta Bleed `45.7%`
* **✅ What Was Good Today (5 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23335.1 vs VWAP 23313.9 (Basis +7.7))**
  - ✔️ **R2: Option > VWAP (CE LTP 86.45 vs VWAP 68.88 (3m dLTP +19.65))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -615,095 vs CE dOI -9,068,085, CE: SHORT_COVERING, PCR 0.74)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.61x, BidQty 1950 vs AskQty 715)**
  - ✔️ **R5: IV Stability (CE IV 17.31% (3m dIV +0.53%))**
* **❌ Why It Did Not Meet 6/6 (1 Condition(s) Missing):**
  - ❌ **R6: Greeks & Theta (Delta 0.49, Daily Theta Bleed 45.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹86.45` &rarr; Latest `₹70.00` | **Max LTP After:** `₹92.35` (**`+6.8%`**) &rarr; **FILTER SAVED LOSS (-19.0%)**

### Entry #16 — `12:13:30` | **NIFTY03NOV2623350CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23331.7` (VWAP `23314.7`) | PCR `0.77` | 3m dOI `-2,524,990` (`SHORT_COVERING`) | 15m PE dOI `-282,165` vs CE dOI `-13,325,195` | Vol Ratio `0.55x` | IV `17.0%` | Delta `0.47` | Theta Bleed `48.4%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23331.7 vs VWAP 23314.7 (Basis +1.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 80.05 vs VWAP 69.07 (3m dLTP +13.25))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -282,165 vs CE dOI -13,325,195, CE: SHORT_COVERING, PCR 0.77)**
  - ✔️ **R5: IV Stability (CE IV 17.03% (3m dIV +0.25%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.55x, BidQty 1170 vs AskQty 260)**
  - ❌ **R6: Greeks & Theta (Delta 0.47, Daily Theta Bleed 48.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹80.05` &rarr; Latest `₹70.00` | **Max LTP After:** `₹92.35` (**`+15.4%`**) &rarr; **MISSED WINNER (+15.4% -> Tune Missing Rule!)**

### Entry #17 — `12:16:30` | **NIFTY03NOV2623350CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23349.1` (VWAP `23316.3`) | PCR `0.77` | 3m dOI `+610,675` (`LONG_BUILDUP`) | 15m PE dOI `+1,831,895` vs CE dOI `-15,841,150` | Vol Ratio `1.06x` | IV `17.5%` | Delta `0.51` | Theta Bleed `43.3%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23349.1 vs VWAP 23316.3 (Basis +4.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 92.35 vs VWAP 69.81 (3m dLTP +12.30))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +1,831,895 vs CE dOI -15,841,150, CE: LONG_BUILDUP, PCR 0.77)**
  - ✔️ **R5: IV Stability (CE IV 17.49% (3m dIV +0.46%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.06x, BidQty 910 vs AskQty 2080)**
  - ❌ **R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 43.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹92.35` &rarr; Latest `₹70.00` | **Max LTP After:** `₹92.35` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-24.2%)**

### Entry #18 — `12:19:30` | **NIFTY03NOV2623350CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23346.9` (VWAP `23317.6`) | PCR `0.82` | 3m dOI `-722,865` (`LONG_UNWINDING`) | 15m PE dOI `+3,315,975` vs CE dOI `-18,391,490` | Vol Ratio `0.83x` | IV `17.2%` | Delta `0.50` | Theta Bleed `44.3%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23346.9 vs VWAP 23317.6 (Basis +2.8))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +3,315,975 vs CE dOI -18,391,490, CE: LONG_UNWINDING, PCR 0.82)**
  - ✔️ **R5: IV Stability (CE IV 17.23% (3m dIV -0.26%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 89.15 vs VWAP 70.27 (3m dLTP -3.20))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.83x, BidQty 1755 vs AskQty 1820)**
  - ❌ **R6: Greeks & Theta (Delta 0.50, Daily Theta Bleed 44.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹89.15` &rarr; Latest `₹70.00` | **Max LTP After:** `₹89.15` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-21.5%)**

### Entry #19 — `12:25:31` | **NIFTY03NOV2623350CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23336.0` (VWAP `23319.7`) | PCR `0.86` | 3m dOI `+781,040` (`SHORT_BUILDUP`) | 15m PE dOI `+6,672,965` vs CE dOI `-8,006,115` | Vol Ratio `0.42x` | IV `16.8%` | Delta `0.48` | Theta Bleed `48.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23336.0 vs VWAP 23319.7 (Basis -0.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +6,672,965 vs CE dOI -8,006,115, CE: SHORT_BUILDUP, PCR 0.86)**
  - ✔️ **R5: IV Stability (CE IV 16.81% (3m dIV -0.05%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 80.00 vs VWAP 70.58 (3m dLTP -0.10))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.42x, BidQty 1950 vs AskQty 260)**
  - ❌ **R6: Greeks & Theta (Delta 0.48, Daily Theta Bleed 48.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹80.00` &rarr; Latest `₹70.00` | **Max LTP After:** `₹80.00` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-12.5%)**

### Entry #20 — `12:27:49` | **NIFTY03NOV2623350CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23335.1` (VWAP `23320.3`) | PCR `0.85` | 3m dOI `+1,120,275` (`SHORT_BUILDUP`) | 15m PE dOI `+6,866,535` vs CE dOI `-2,904,850` | Vol Ratio `0.25x` | IV `16.8%` | Delta `0.47` | Theta Bleed `48.6%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23335.1 vs VWAP 23320.3 (Basis -0.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +6,866,535 vs CE dOI -2,904,850, CE: SHORT_BUILDUP, PCR 0.85)**
  - ✔️ **R5: IV Stability (CE IV 16.76% (3m dIV -0.10%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 79.00 vs VWAP 70.63 (3m dLTP -1.10))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.25x, BidQty 325 vs AskQty 455)**
  - ❌ **R6: Greeks & Theta (Delta 0.47, Daily Theta Bleed 48.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹79.00` &rarr; Latest `₹70.00` | **Max LTP After:** `₹79.00` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-11.4%)**

### Entry #21 — `12:30:50` | **NIFTY03NOV2623350CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23327.0` (VWAP `23320.5`) | PCR `0.85` | 3m dOI `+363,025` (`SHORT_BUILDUP`) | 15m PE dOI `+6,181,305` vs CE dOI `-2,854,410` | Vol Ratio `0.53x` | IV `16.7%` | Delta `0.46` | Theta Bleed `50.9%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23327.0 vs VWAP 23320.5 (Basis -0.8))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +6,181,305 vs CE dOI -2,854,410, CE: SHORT_BUILDUP, PCR 0.85)**
  - ✔️ **R5: IV Stability (CE IV 16.66% (3m dIV -0.10%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 74.70 vs VWAP 70.69 (3m dLTP -4.30))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.53x, BidQty 520 vs AskQty 2795)**
  - ❌ **R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 50.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹74.70` &rarr; Latest `₹70.00` | **Max LTP After:** `₹77.55` (**`+3.8%`**) &rarr; **TRACKING (Max +3.8%)**

### Entry #22 — `12:33:51` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23294.3` (VWAP `23319.6`) | PCR `1.08` | 3m dOI `-184,925` (`SHORT_COVERING`) | 15m PE dOI `+3,494,270` vs CE dOI `-2,161,965` | Vol Ratio `1.79x` | IV `17.1%` | Delta `-0.53` | Theta Bleed `40.8%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23294.3 vs VWAP 23319.6 (Basis -9.6))**
  - ✔️ **R2: Option > VWAP (PE LTP 96.00 vs VWAP 87.06 (3m dLTP +20.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -2,161,965 vs PE dOI +3,494,270, PE: SHORT_COVERING, PCR 1.08)**
  - ✔️ **R5: IV Stability (PE IV 17.11% (3m dIV +0.11%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.79x, BidQty 715 vs AskQty 1950)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.53, Daily Theta Bleed 40.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹96.00` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+60.5%`**) &rarr; **MISSED WINNER (+60.5% -> Tune Missing Rule!)**

### Entry #23 — `12:36:17` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23306.9` (VWAP `23319.2`) | PCR `1.00` | 3m dOI `-1,675,635` (`SHORT_COVERING`) | 15m PE dOI `-3,652,805` vs CE dOI `+1,843,985` | Vol Ratio `0.97x` | IV `17.0%` | Delta `-0.49` | Theta Bleed `45.8%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23306.9 vs VWAP 23319.2 (Basis -2.1))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +1,843,985 vs PE dOI -3,652,805, PE: SHORT_COVERING, PCR 1.00)**
  - ✔️ **R5: IV Stability (PE IV 17.03% (3m dIV +0.03%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 85.35 vs VWAP 87.03 (3m dLTP +10.10))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.97x, BidQty 4485 vs AskQty 650)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.49, Daily Theta Bleed 45.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹85.35` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+80.5%`**) &rarr; **MISSED WINNER (+80.5% -> Tune Missing Rule!)**

### Entry #24 — `12:39:18` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23311.2` (VWAP `23319.0`) | PCR `0.98` | 3m dOI `+218,985` (`SHORT_BUILDUP`) | 15m PE dOI `-4,305,340` vs CE dOI `+1,907,230` | Vol Ratio `0.50x` | IV `16.8%` | Delta `-0.49` | Theta Bleed `46.2%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23311.2 vs VWAP 23319.0 (Basis -6.5))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +1,907,230 vs PE dOI -4,305,340, PE: SHORT_BUILDUP, PCR 0.98)**
  - ✔️ **R5: IV Stability (PE IV 16.83% (3m dIV -0.20%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 83.75 vs VWAP 86.99 (3m dLTP -1.60))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.50x, BidQty 65 vs AskQty 130)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.49, Daily Theta Bleed 46.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹83.75` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+83.9%`**) &rarr; **MISSED WINNER (+83.9% -> Tune Missing Rule!)**

### Entry #25 — `12:42:19` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23298.7` (VWAP `23318.3`) | PCR `1.00` | 3m dOI `+953,615` (`LONG_BUILDUP`) | 15m PE dOI `-2,570,685` vs CE dOI `+1,775,995` | Vol Ratio `0.77x` | IV `17.0%` | Delta `-0.51` | Theta Bleed `42.5%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23298.7 vs VWAP 23318.3 (Basis -7.7))**
  - ✔️ **R2: Option > VWAP (PE LTP 91.90 vs VWAP 87.07 (3m dLTP +8.15))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +1,775,995 vs PE dOI -2,570,685, PE: LONG_BUILDUP, PCR 1.00)**
  - ✔️ **R5: IV Stability (PE IV 16.99% (3m dIV +0.16%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.77x, BidQty 975 vs AskQty 2275)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.51, Daily Theta Bleed 42.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹91.90` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+67.6%`**) &rarr; **MISSED WINNER (+67.6% -> Tune Missing Rule!)**

### Entry #26 — `12:45:19` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23290.3` (VWAP `23317.5`) | PCR `0.97` | 3m dOI `-105,885` (`SHORT_COVERING`) | 15m PE dOI `-3,545,620` vs CE dOI `+3,229,135` | Vol Ratio `0.92x` | IV `17.1%` | Delta `-0.53` | Theta Bleed `40.9%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23290.3 vs VWAP 23317.5 (Basis -6.1))**
  - ✔️ **R2: Option > VWAP (PE LTP 95.65 vs VWAP 87.24 (3m dLTP +3.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,229,135 vs PE dOI -3,545,620, PE: SHORT_COVERING, PCR 0.97)**
  - ✔️ **R5: IV Stability (PE IV 17.06% (3m dIV +0.07%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.92x, BidQty 195 vs AskQty 1105)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.53, Daily Theta Bleed 40.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹95.65` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+61.1%`**) &rarr; **MISSED WINNER (+61.1% -> Tune Missing Rule!)**

### Entry #27 — `12:48:20` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23294.0` (VWAP `23316.8`) | PCR `0.92` | 3m dOI `-717,535` (`LONG_UNWINDING`) | 15m PE dOI `-4,790,825` vs CE dOI `+8,993,855` | Vol Ratio `0.69x` | IV `16.9%` | Delta `-0.52` | Theta Bleed `41.5%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23294.0 vs VWAP 23316.8 (Basis -7.5))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,993,855 vs PE dOI -4,790,825, PE: LONG_UNWINDING, PCR 0.92)**
  - ✔️ **R5: IV Stability (PE IV 16.90% (3m dIV -0.16%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 93.60 vs VWAP 87.33 (3m dLTP -2.05))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.69x, BidQty 1885 vs AskQty 1430)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.52, Daily Theta Bleed 41.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹93.60` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+64.6%`**) &rarr; **MISSED WINNER (+64.6% -> Tune Missing Rule!)**

### Entry #28 — `12:51:21` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23294.5` (VWAP `23316.2`) | PCR `0.89` | 3m dOI `-122,070` (`LONG_UNWINDING`) | 15m PE dOI `-1,427,335` vs CE dOI `+8,505,185` | Vol Ratio `0.59x` | IV `16.9%` | Delta `-0.52` | Theta Bleed `42.4%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23294.5 vs VWAP 23316.2 (Basis -7.0))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,505,185 vs PE dOI -1,427,335, PE: LONG_UNWINDING, PCR 0.89)**
  - ✔️ **R5: IV Stability (PE IV 16.91% (3m dIV +0.01%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 91.90 vs VWAP 87.38 (3m dLTP -1.70))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.59x, BidQty 4355 vs AskQty 2015)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.52, Daily Theta Bleed 42.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹91.90` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+67.6%`**) &rarr; **MISSED WINNER (+67.6% -> Tune Missing Rule!)**

### Entry #29 — `12:54:22` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23284.9` (VWAP `23315.3`) | PCR `0.92` | 3m dOI `+640,705` (`LONG_BUILDUP`) | 15m PE dOI `+48,425` vs CE dOI `+6,732,050` | Vol Ratio `0.86x` | IV `17.1%` | Delta `-0.54` | Theta Bleed `39.3%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23284.9 vs VWAP 23315.3 (Basis -8.3))**
  - ✔️ **R2: Option > VWAP (PE LTP 99.70 vs VWAP 87.59 (3m dLTP +7.80))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,732,050 vs PE dOI +48,425, PE: LONG_BUILDUP, PCR 0.92)**
  - ✔️ **R5: IV Stability (PE IV 17.06% (3m dIV +0.15%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.86x, BidQty 3380 vs AskQty 3315)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.54, Daily Theta Bleed 39.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹99.70` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+54.5%`**) &rarr; **MISSED WINNER (+54.5% -> Tune Missing Rule!)**

### Entry #30 — `12:57:23` | **NIFTY03NOV2623300PE** (PE) — **5/6** [🟡 NEAR-MISS (5/6)]
* **Option Chain Context:** Spot `23286.9` (VWAP `23314.5`) | PCR `0.81` | 3m dOI `-2,950,675` (`SHORT_COVERING`) | 15m PE dOI `-10,732,800` vs CE dOI `+8,070,530` | Vol Ratio `2.19x` | IV `17.1%` | Delta `-0.54` | Theta Bleed `38.9%`
* **✅ What Was Good Today (5 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23286.9 vs VWAP 23314.5 (Basis -12.4))**
  - ✔️ **R2: Option > VWAP (PE LTP 100.70 vs VWAP 88.13 (3m dLTP +1.00))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,070,530 vs PE dOI -10,732,800, PE: SHORT_COVERING, PCR 0.81)**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.19x, BidQty 910 vs AskQty 325)**
  - ✔️ **R5: IV Stability (PE IV 17.08% (3m dIV +0.02%))**
* **❌ Why It Did Not Meet 6/6 (1 Condition(s) Missing):**
  - ❌ **R6: Greeks & Theta (|Delta| 0.54, Daily Theta Bleed 38.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹100.70` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+53.0%`**) &rarr; **MISSED WINNER (+53.0% -> Tune Missing Rule!)**

### Entry #31 — `13:00:24` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23281.7` (VWAP `23313.7`) | PCR `0.80` | 3m dOI `-107,250` (`SHORT_COVERING`) | 15m PE dOI `-9,831,185` vs CE dOI `+7,256,600` | Vol Ratio `0.94x` | IV `17.2%` | Delta `-0.56` | Theta Bleed `36.6%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23281.7 vs VWAP 23313.7 (Basis -18.1))**
  - ✔️ **R2: Option > VWAP (PE LTP 107.05 vs VWAP 88.47 (3m dLTP +6.35))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +7,256,600 vs PE dOI -9,831,185, PE: SHORT_COVERING, PCR 0.80)**
  - ✔️ **R5: IV Stability (PE IV 17.16% (3m dIV +0.08%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.94x, BidQty 65 vs AskQty 585)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 36.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹107.05` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+43.9%`**) &rarr; **MISSED WINNER (+43.9% -> Tune Missing Rule!)**

### Entry #32 — `13:02:47` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23275.7` (VWAP `23312.7`) | PCR `0.79` | 3m dOI `-97,695` (`SHORT_COVERING`) | 15m PE dOI `-7,796,815` vs CE dOI `+6,240,650` | Vol Ratio `0.64x` | IV `17.2%` | Delta `-0.57` | Theta Bleed `36.1%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23275.7 vs VWAP 23312.7 (Basis -14.6))**
  - ✔️ **R2: Option > VWAP (PE LTP 108.55 vs VWAP 88.71 (3m dLTP +7.85))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,240,650 vs PE dOI -7,796,815, PE: SHORT_COVERING, PCR 0.79)**
  - ✔️ **R5: IV Stability (PE IV 17.19% (3m dIV +0.11%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.64x, BidQty 910 vs AskQty 2145)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.57, Daily Theta Bleed 36.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹108.55` &rarr; Latest `₹52.60` | **Max LTP After:** `₹154.05` (**`+41.9%`**) &rarr; **MISSED WINNER (+41.9% -> Tune Missing Rule!)**

### Entry #33 — `13:05:48` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23262.2` (VWAP `23311.4`) | PCR `0.95` | 3m dOI `-858,195` (`SHORT_COVERING`) | 15m PE dOI `-11,326,640` vs CE dOI `+4,733,040` | Vol Ratio `2.14x` | IV `17.5%` | Delta `-0.50` | Theta Bleed `44.5%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23262.2 vs VWAP 23311.4 (Basis -16.0))**
  - ✔️ **R2: Option > VWAP (PE LTP 91.20 vs VWAP 69.29 (3m dLTP +7.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +4,733,040 vs PE dOI -11,326,640, PE: SHORT_COVERING, PCR 0.95)**
  - ✔️ **R5: IV Stability (PE IV 17.54% (3m dIV +0.10%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 2.14x, BidQty 325 vs AskQty 2145)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.50, Daily Theta Bleed 44.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹91.20` &rarr; Latest `₹35.55` | **Max LTP After:** `₹121.05` (**`+32.7%`**) &rarr; **MISSED WINNER (+32.7% -> Tune Missing Rule!)**

### Entry #34 — `13:08:48` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23251.0` (VWAP `23309.9`) | PCR `0.89` | 3m dOI `-598,650` (`SHORT_COVERING`) | 15m PE dOI `-16,870,425` vs CE dOI `+8,000,330` | Vol Ratio `2.00x` | IV `17.6%` | Delta `-0.53` | Theta Bleed `40.9%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23251.0 vs VWAP 23309.9 (Basis -19.9))**
  - ✔️ **R2: Option > VWAP (PE LTP 99.35 vs VWAP 70.26 (3m dLTP +8.15))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,000,330 vs PE dOI -16,870,425, PE: SHORT_COVERING, PCR 0.89)**
  - ✔️ **R5: IV Stability (PE IV 17.62% (3m dIV +0.08%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 2.00x, BidQty 585 vs AskQty 1950)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.53, Daily Theta Bleed 40.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹99.35` &rarr; Latest `₹35.55` | **Max LTP After:** `₹121.05` (**`+21.8%`**) &rarr; **MISSED WINNER (+21.8% -> Tune Missing Rule!)**

### Entry #35 — `13:10:41` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23237.5` (VWAP `23308.2`) | PCR `0.78` | 3m dOI `-3,227,640` (`SHORT_COVERING`) | 15m PE dOI `-18,401,890` vs CE dOI `+6,187,025` | Vol Ratio `2.66x` | IV `18.0%` | Delta `-0.56` | Theta Bleed `37.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23237.5 vs VWAP 23308.2 (Basis -24.6))**
  - ✔️ **R2: Option > VWAP (PE LTP 111.15 vs VWAP 71.98 (3m dLTP +19.95))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,187,025 vs PE dOI -18,401,890, PE: SHORT_COVERING, PCR 0.78)**
  - ✔️ **R5: IV Stability (PE IV 17.99% (3m dIV +0.45%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 2.66x, BidQty 650 vs AskQty 1495)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 37.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹111.15` &rarr; Latest `₹35.55` | **Max LTP After:** `₹121.05` (**`+8.9%`**) &rarr; **TRACKING (Max +8.9%)**

### Entry #36 — `13:13:41` | **NIFTY03NOV2623200PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23223.9` (VWAP `23306.2`) | PCR `0.89` | 3m dOI `+25,025` (`LONG_BUILDUP`) | 15m PE dOI `-19,241,885` vs CE dOI `+9,767,940` | Vol Ratio `2.55x` | IV `18.2%` | Delta `-0.50` | Theta Bleed `44.8%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23223.9 vs VWAP 23306.2 (Basis -27.4))**
  - ✔️ **R2: Option > VWAP (PE LTP 94.05 vs VWAP 56.30 (3m dLTP +7.85))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +9,767,940 vs PE dOI -19,241,885, PE: LONG_BUILDUP, PCR 0.89)**
  - ✔️ **R5: IV Stability (PE IV 18.23% (3m dIV +0.00%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 2.55x, BidQty 260 vs AskQty 1170)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.50, Daily Theta Bleed 44.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹94.05` &rarr; Latest `₹23.35` | **Max LTP After:** `₹94.25` (**`+0.2%`**) &rarr; **FILTER SAVED LOSS (-75.2%)**

### Entry #37 — `13:16:42` | **NIFTY03NOV2623200PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23224.7` (VWAP `23304.4`) | PCR `0.84` | 3m dOI `+670,995` (`SHORT_BUILDUP`) | 15m PE dOI `-20,094,360` vs CE dOI `+12,769,835` | Vol Ratio `2.29x` | IV `18.1%` | Delta `-0.50` | Theta Bleed `44.9%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23224.7 vs VWAP 23304.4 (Basis -28.5))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +12,769,835 vs PE dOI -20,094,360, PE: SHORT_BUILDUP, PCR 0.84)**
  - ✔️ **R5: IV Stability (PE IV 18.10% (3m dIV -0.13%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 93.30 vs VWAP 57.64 (3m dLTP -0.75))**
  - ❌ **R4: Volume Burst (Vol Ratio 2.29x, BidQty 260 vs AskQty 455)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.50, Daily Theta Bleed 44.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹93.30` &rarr; Latest `₹23.35` | **Max LTP After:** `₹94.25` (**`+1.0%`**) &rarr; **FILTER SAVED LOSS (-75.0%)**

### Entry #38 — `13:17:01` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23225.6` (VWAP `23302.7`) | PCR `0.68` | 3m dOI `-633,815` (`LONG_UNWINDING`) | 15m PE dOI `-21,339,240` vs CE dOI `+13,161,135` | Vol Ratio `0.06x` | IV `17.9%` | Delta `-0.59` | Theta Bleed `33.4%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23225.6 vs VWAP 23302.7 (Basis -29.6))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +13,161,135 vs PE dOI -21,339,240, PE: LONG_UNWINDING, PCR 0.68)**
  - ✔️ **R5: IV Stability (PE IV 17.93% (3m dIV -0.20%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 120.90 vs VWAP 74.57 (3m dLTP -0.15))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.06x, BidQty 195 vs AskQty 130)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.59, Daily Theta Bleed 33.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹120.90` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.90` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-70.6%)**

### Entry #39 — `13:24:58` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23255.9` (VWAP `23299.6`) | PCR `0.67` | 3m dOI `+527,085` (`SHORT_BUILDUP`) | 15m PE dOI `-1,246,960` vs CE dOI `+13,222,495` | Vol Ratio `0.76x` | IV `17.5%` | Delta `-0.54` | Theta Bleed `40.5%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23255.9 vs VWAP 23299.6 (Basis -28.2))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +13,222,495 vs PE dOI -1,246,960, PE: SHORT_BUILDUP, PCR 0.67)**
  - ✔️ **R5: IV Stability (PE IV 17.53% (3m dIV +0.01%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 100.30 vs VWAP 75.62 (3m dLTP -2.15))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.76x, BidQty 2275 vs AskQty 1235)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.54, Daily Theta Bleed 40.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹100.30` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+20.4%`**) &rarr; **MISSED WINNER (+20.4% -> Tune Missing Rule!)**

### Entry #40 — `13:27:58` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23241.8` (VWAP `23298.4`) | PCR `0.69` | 3m dOI `+520,325` (`LONG_BUILDUP`) | 15m PE dOI `+2,135,575` vs CE dOI `+8,146,775` | Vol Ratio `1.01x` | IV `17.5%` | Delta `-0.57` | Theta Bleed `36.7%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23241.8 vs VWAP 23298.4 (Basis -30.4))**
  - ✔️ **R2: Option > VWAP (PE LTP 109.40 vs VWAP 76.12 (3m dLTP +9.10))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,146,775 vs PE dOI +2,135,575, PE: LONG_BUILDUP, PCR 0.69)**
  - ✔️ **R5: IV Stability (PE IV 17.51% (3m dIV -0.02%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.01x, BidQty 910 vs AskQty 390)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.57, Daily Theta Bleed 36.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹109.40` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+10.4%`**) &rarr; **TRACKING (Max +10.4%)**

### Entry #41 — `13:28:32` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23245.0` (VWAP `23297.3`) | PCR `0.69` | 3m dOI `+604,695` (`LONG_BUILDUP`) | 15m PE dOI `+2,466,620` vs CE dOI `+8,441,420` | Vol Ratio `0.11x` | IV `17.4%` | Delta `-0.55` | Theta Bleed `38.5%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23245.0 vs VWAP 23297.3 (Basis -25.9))**
  - ✔️ **R2: Option > VWAP (PE LTP 104.35 vs VWAP 76.17 (3m dLTP +4.05))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,441,420 vs PE dOI +2,466,620, PE: LONG_BUILDUP, PCR 0.69)**
  - ✔️ **R5: IV Stability (PE IV 17.43% (3m dIV -0.10%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.11x, BidQty 260 vs AskQty 1300)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.55, Daily Theta Bleed 38.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹104.35` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+15.7%`**) &rarr; **MISSED WINNER (+15.7% -> Tune Missing Rule!)**

### Entry #42 — `13:31:32` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23238.5` (VWAP `23296.2`) | PCR `0.70` | 3m dOI `-14,040` (`SHORT_COVERING`) | 15m PE dOI `+4,847,960` vs CE dOI `+4,693,520` | Vol Ratio `0.93x` | IV `17.5%` | Delta `-0.56` | Theta Bleed `37.7%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23238.5 vs VWAP 23296.2 (Basis -23.4))**
  - ✔️ **R2: Option > VWAP (PE LTP 106.80 vs VWAP 76.58 (3m dLTP +2.45))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +4,693,520 vs PE dOI +4,847,960, PE: SHORT_COVERING, PCR 0.70)**
  - ✔️ **R5: IV Stability (PE IV 17.50% (3m dIV +0.07%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.93x, BidQty 65 vs AskQty 2080)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 37.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹106.80` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+13.1%`**) &rarr; **MISSED WINNER (+13.1% -> Tune Missing Rule!)**

### Entry #43 — `13:34:34` | **NIFTY03NOV2623250CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23227.3` (VWAP `23294.8`) | PCR `0.68` | 3m dOI `+318,955` (`SHORT_BUILDUP`) | 15m PE dOI `+4,841,785` vs CE dOI `+3,017,950` | Vol Ratio `1.35x` | IV `17.6%` | Delta `0.42` | Theta Bleed `59.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +4,841,785 vs CE dOI +3,017,950, CE: SHORT_BUILDUP, PCR 0.68)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.35x, BidQty 2405 vs AskQty 1300)**
  - ✔️ **R5: IV Stability (CE IV 17.58% (3m dIV +0.08%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23227.3 vs VWAP 23294.8 (Basis -24.1))**
  - ❌ **R2: Option > VWAP (CE LTP 67.15 vs VWAP 111.72 (3m dLTP -4.80))**
  - ❌ **R6: Greeks & Theta (Delta 0.42, Daily Theta Bleed 59.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹67.15` &rarr; Latest `₹128.70` | **Max LTP After:** `₹140.65` (**`+109.5%`**) &rarr; **MISSED WINNER (+109.5% -> Tune Missing Rule!)**

### Entry #44 — `13:34:34` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23227.3` (VWAP `23294.8`) | PCR `0.68` | 3m dOI `-256,945` (`SHORT_COVERING`) | 15m PE dOI `+4,841,785` vs CE dOI `+3,017,950` | Vol Ratio `1.21x` | IV `17.6%` | Delta `-0.58` | Theta Bleed `35.2%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23227.3 vs VWAP 23294.8 (Basis -24.1))**
  - ✔️ **R2: Option > VWAP (PE LTP 113.95 vs VWAP 77.21 (3m dLTP +7.15))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,017,950 vs PE dOI +4,841,785, PE: SHORT_COVERING, PCR 0.68)**
  - ✔️ **R5: IV Stability (PE IV 17.58% (3m dIV +0.08%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.21x, BidQty 130 vs AskQty 1170)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.58, Daily Theta Bleed 35.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹113.95` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+6.0%`**) &rarr; **FILTER SAVED LOSS (-68.8%)**

### Entry #45 — `13:34:36` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23228.5` (VWAP `23293.6`) | PCR `0.68` | 3m dOI `-256,945` (`SHORT_COVERING`) | 15m PE dOI `+4,841,785` vs CE dOI `+3,017,950` | Vol Ratio `0.01x` | IV `17.6%` | Delta `-0.58` | Theta Bleed `35.1%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23228.5 vs VWAP 23293.6 (Basis -25.1))**
  - ✔️ **R2: Option > VWAP (PE LTP 113.90 vs VWAP 77.22 (3m dLTP +7.10))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,017,950 vs PE dOI +4,841,785, PE: SHORT_COVERING, PCR 0.68)**
  - ✔️ **R5: IV Stability (PE IV 17.55% (3m dIV +0.05%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.01x, BidQty 1235 vs AskQty 780)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.58, Daily Theta Bleed 35.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹113.90` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+6.0%`**) &rarr; **FILTER SAVED LOSS (-68.8%)**

### Entry #46 — `13:37:36` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23228.8` (VWAP `23292.4`) | PCR `0.66` | 3m dOI `-269,945` (`LONG_UNWINDING`) | 15m PE dOI `+3,992,105` vs CE dOI `+6,458,010` | Vol Ratio `1.05x` | IV `17.4%` | Delta `-0.58` | Theta Bleed `35.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23228.8 vs VWAP 23292.4 (Basis -25.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,458,010 vs PE dOI +3,992,105, PE: LONG_UNWINDING, PCR 0.66)**
  - ✔️ **R5: IV Stability (PE IV 17.40% (3m dIV -0.15%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 113.15 vs VWAP 77.73 (3m dLTP -0.75))**
  - ❌ **R4: Volume Burst (Vol Ratio 1.05x, BidQty 195 vs AskQty 65)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.58, Daily Theta Bleed 35.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹113.15` &rarr; Latest `₹35.55` | **Max LTP After:** `₹120.75` (**`+6.7%`**) &rarr; **FILTER SAVED LOSS (-68.6%)**

### Entry #47 — `13:38:14` | **NIFTY03NOV2623200PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23218.2` (VWAP `23291.0`) | PCR `0.81` | 3m dOI `-35,880` (`SHORT_COVERING`) | 15m PE dOI `+1,674,335` vs CE dOI `+4,337,385` | Vol Ratio `0.34x` | IV `17.6%` | Delta `-0.51` | Theta Bleed `44.1%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23218.2 vs VWAP 23291.0 (Basis -27.2))**
  - ✔️ **R2: Option > VWAP (PE LTP 92.85 vs VWAP 60.84 (3m dLTP +5.50))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +4,337,385 vs PE dOI +1,674,335, PE: SHORT_COVERING, PCR 0.81)**
  - ✔️ **R5: IV Stability (PE IV 17.57% (3m dIV -0.08%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.34x, BidQty 3640 vs AskQty 1885)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.51, Daily Theta Bleed 44.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹92.85` &rarr; Latest `₹23.35` | **Max LTP After:** `₹92.85` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-74.8%)**

### Entry #48 — `13:41:14` | **NIFTY03NOV2623200PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23222.2` (VWAP `23289.8`) | PCR `0.80` | 3m dOI `-92,560` (`LONG_UNWINDING`) | 15m PE dOI `-308,035` vs CE dOI `+5,227,365` | Vol Ratio `2.14x` | IV `17.4%` | Delta `-0.50` | Theta Bleed `46.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23222.2 vs VWAP 23289.8 (Basis -23.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +5,227,365 vs PE dOI -308,035, PE: LONG_UNWINDING, PCR 0.80)**
  - ✔️ **R5: IV Stability (PE IV 17.43% (3m dIV -0.14%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 88.40 vs VWAP 61.62 (3m dLTP -4.45))**
  - ❌ **R4: Volume Burst (Vol Ratio 2.14x, BidQty 715 vs AskQty 4030)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.50, Daily Theta Bleed 46.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹88.40` &rarr; Latest `₹23.35` | **Max LTP After:** `₹88.40` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-73.6%)**

### Entry #49 — `13:44:15` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23241.6` (VWAP `23289.0`) | PCR `0.64` | 3m dOI `-443,950` (`LONG_UNWINDING`) | 15m PE dOI `-2,836,665` vs CE dOI `+6,648,200` | Vol Ratio `0.80x` | IV `17.3%` | Delta `-0.56` | Theta Bleed `38.2%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23241.6 vs VWAP 23289.0 (Basis -24.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,648,200 vs PE dOI -2,836,665, PE: LONG_UNWINDING, PCR 0.64)**
  - ✔️ **R5: IV Stability (PE IV 17.29% (3m dIV -0.12%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 104.60 vs VWAP 78.83 (3m dLTP -11.20))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.80x, BidQty 325 vs AskQty 715)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 38.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹104.60` &rarr; Latest `₹35.55` | **Max LTP After:** `₹111.40` (**`+6.5%`**) &rarr; **FILTER SAVED LOSS (-66.0%)**

### Entry #50 — `13:47:16` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23243.2` (VWAP `23288.2`) | PCR `0.64` | 3m dOI `+137,150` (`SHORT_BUILDUP`) | 15m PE dOI `-3,130,335` vs CE dOI `+6,182,865` | Vol Ratio `0.71x` | IV `17.3%` | Delta `-0.55` | Theta Bleed `39.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23243.2 vs VWAP 23288.2 (Basis -23.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +6,182,865 vs PE dOI -3,130,335, PE: SHORT_BUILDUP, PCR 0.64)**
  - ✔️ **R5: IV Stability (PE IV 17.26% (3m dIV -0.03%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 102.60 vs VWAP 79.04 (3m dLTP -2.00))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.71x, BidQty 1300 vs AskQty 2925)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.55, Daily Theta Bleed 39.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹102.60` &rarr; Latest `₹35.55` | **Max LTP After:** `₹111.40` (**`+8.6%`**) &rarr; **TRACKING (Max +8.6%)**

### Entry #51 — `13:47:16` | **NIFTY03NOV2623250CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23243.2` (VWAP `23288.2`) | PCR `0.64` | 3m dOI `-21,775` (`SHORT_COVERING`) | 15m PE dOI `-3,130,335` vs CE dOI `+6,182,865` | Vol Ratio `1.75x` | IV `17.3%` | Delta `0.45` | Theta Bleed `55.3%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -3,130,335 vs CE dOI +6,182,865, CE: SHORT_COVERING, PCR 0.64)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.75x, BidQty 1235 vs AskQty 1105)**
  - ✔️ **R5: IV Stability (CE IV 17.26% (3m dIV -0.03%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23243.2 vs VWAP 23288.2 (Basis -23.4))**
  - ❌ **R2: Option > VWAP (CE LTP 72.40 vs VWAP 108.47 (3m dLTP +1.15))**
  - ❌ **R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 55.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹72.40` &rarr; Latest `₹128.70` | **Max LTP After:** `₹140.65` (**`+94.3%`**) &rarr; **MISSED WINNER (+94.3% -> Tune Missing Rule!)**

### Entry #52 — `13:49:28` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23230.5` (VWAP `23287.2`) | PCR `0.65` | 3m dOI `+343,915` (`LONG_BUILDUP`) | 15m PE dOI `-1,269,060` vs CE dOI `+5,760,950` | Vol Ratio `0.67x` | IV `17.3%` | Delta `-0.58` | Theta Bleed `35.6%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23230.5 vs VWAP 23287.2 (Basis -26.1))**
  - ✔️ **R2: Option > VWAP (PE LTP 111.40 vs VWAP 79.32 (3m dLTP +6.80))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +5,760,950 vs PE dOI -1,269,060, PE: LONG_BUILDUP, PCR 0.65)**
  - ✔️ **R5: IV Stability (PE IV 17.28% (3m dIV -0.01%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.67x, BidQty 715 vs AskQty 325)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.58, Daily Theta Bleed 35.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹111.40` &rarr; Latest `₹35.55` | **Max LTP After:** `₹111.40` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-68.1%)**

### Entry #53 — `13:52:29` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23240.8` (VWAP `23286.4`) | PCR `0.65` | 3m dOI `-190,580` (`LONG_UNWINDING`) | 15m PE dOI `-796,250` vs CE dOI `+2,367,755` | Vol Ratio `0.85x` | IV `17.2%` | Delta `-0.56` | Theta Bleed `38.5%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23240.8 vs VWAP 23286.4 (Basis -22.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +2,367,755 vs PE dOI -796,250, PE: LONG_UNWINDING, PCR 0.65)**
  - ✔️ **R5: IV Stability (PE IV 17.21% (3m dIV -0.07%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 103.55 vs VWAP 79.58 (3m dLTP -7.85))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.85x, BidQty 1690 vs AskQty 455)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 38.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹103.55` &rarr; Latest `₹35.55` | **Max LTP After:** `₹103.60` (**`+0.1%`**) &rarr; **FILTER SAVED LOSS (-65.7%)**

### Entry #54 — `13:53:32` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23240.9` (VWAP `23285.7`) | PCR `0.64` | 3m dOI `-64,155` (`LONG_UNWINDING`) | 15m PE dOI `-514,735` vs CE dOI `+3,559,010` | Vol Ratio `0.15x` | IV `17.2%` | Delta `-0.56` | Theta Bleed `38.6%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23240.9 vs VWAP 23285.7 (Basis -23.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,559,010 vs PE dOI -514,735, PE: LONG_UNWINDING, PCR 0.64)**
  - ✔️ **R5: IV Stability (PE IV 17.22% (3m dIV -0.06%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 103.55 vs VWAP 79.62 (3m dLTP -7.85))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.15x, BidQty 1495 vs AskQty 2795)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 38.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹103.55` &rarr; Latest `₹35.55` | **Max LTP After:** `₹103.60` (**`+0.1%`**) &rarr; **FILTER SAVED LOSS (-65.7%)**

### Entry #55 — `13:56:32` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23236.7` (VWAP `23284.9`) | PCR `0.65` | 3m dOI `+262,925` (`SHORT_BUILDUP`) | 15m PE dOI `+1,255,410` vs CE dOI `+2,933,580` | Vol Ratio `0.51x` | IV `17.2%` | Delta `-0.56` | Theta Bleed `38.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23236.7 vs VWAP 23284.9 (Basis -18.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +2,933,580 vs PE dOI +1,255,410, PE: SHORT_BUILDUP, PCR 0.65)**
  - ✔️ **R5: IV Stability (PE IV 17.17% (3m dIV -0.05%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 103.00 vs VWAP 79.77 (3m dLTP -0.55))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.51x, BidQty 650 vs AskQty 650)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 38.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹103.00` &rarr; Latest `₹35.55` | **Max LTP After:** `₹103.60` (**`+0.6%`**) &rarr; **FILTER SAVED LOSS (-65.5%)**

### Entry #56 — `13:56:50` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23238.5` (VWAP `23284.2`) | PCR `0.65` | 3m dOI `+273,650` (`LONG_BUILDUP`) | 15m PE dOI `+1,237,600` vs CE dOI `+2,819,180` | Vol Ratio `0.04x` | IV `17.2%` | Delta `-0.56` | Theta Bleed `38.6%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23238.5 vs VWAP 23284.2 (Basis -21.2))**
  - ✔️ **R2: Option > VWAP (PE LTP 103.60 vs VWAP 79.78 (3m dLTP +0.05))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +2,819,180 vs PE dOI +1,237,600, PE: LONG_BUILDUP, PCR 0.65)**
  - ✔️ **R5: IV Stability (PE IV 17.23% (3m dIV +0.01%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.04x, BidQty 2860 vs AskQty 1755)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 38.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹103.60` &rarr; Latest `₹35.55` | **Max LTP After:** `₹103.60` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-65.7%)**

### Entry #57 — `13:59:50` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23249.1` (VWAP `23283.6`) | PCR `0.63` | 3m dOI `-236,600` (`LONG_UNWINDING`) | 15m PE dOI `+1,461,005` vs CE dOI `+3,297,775` | Vol Ratio `0.84x` | IV `17.2%` | Delta `-0.54` | Theta Bleed `41.5%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23249.1 vs VWAP 23283.6 (Basis -20.2))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,297,775 vs PE dOI +1,461,005, PE: LONG_UNWINDING, PCR 0.63)**
  - ✔️ **R5: IV Stability (PE IV 17.18% (3m dIV -0.05%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 96.90 vs VWAP 79.95 (3m dLTP -6.70))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.84x, BidQty 4095 vs AskQty 910)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.54, Daily Theta Bleed 41.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹96.90` &rarr; Latest `₹35.55` | **Max LTP After:** `₹102.30` (**`+5.6%`**) &rarr; **FILTER SAVED LOSS (-63.3%)**

### Entry #58 — `14:02:51` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23244.3` (VWAP `23283.0`) | PCR `0.63` | 3m dOI `+305,695` (`LONG_BUILDUP`) | 15m PE dOI `+392,275` vs CE dOI `+3,274,180` | Vol Ratio `0.62x` | IV `17.1%` | Delta `-0.56` | Theta Bleed `39.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23244.3 vs VWAP 23283.0 (Basis -25.4))**
  - ✔️ **R2: Option > VWAP (PE LTP 102.30 vs VWAP 80.12 (3m dLTP +5.40))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,274,180 vs PE dOI +392,275, PE: LONG_BUILDUP, PCR 0.63)**
  - ✔️ **R5: IV Stability (PE IV 17.14% (3m dIV -0.04%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.62x, BidQty 715 vs AskQty 1755)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.56, Daily Theta Bleed 39.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹102.30` &rarr; Latest `₹35.55` | **Max LTP After:** `₹102.30` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-65.2%)**

### Entry #59 — `14:05:11` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23253.5` (VWAP `23282.6`) | PCR `0.62` | 3m dOI `+330,785` (`SHORT_BUILDUP`) | 15m PE dOI `+465,725` vs CE dOI `+4,142,710` | Vol Ratio `0.45x` | IV `17.1%` | Delta `-0.53` | Theta Bleed `42.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23253.5 vs VWAP 23282.6 (Basis -20.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +4,142,710 vs PE dOI +465,725, PE: SHORT_BUILDUP, PCR 0.62)**
  - ✔️ **R5: IV Stability (PE IV 17.09% (3m dIV -0.09%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 94.00 vs VWAP 80.19 (3m dLTP -2.90))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.45x, BidQty 1495 vs AskQty 2080)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.53, Daily Theta Bleed 42.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹94.00` &rarr; Latest `₹35.55` | **Max LTP After:** `₹96.75` (**`+2.9%`**) &rarr; **FILTER SAVED LOSS (-62.2%)**

### Entry #60 — `14:08:12` | **NIFTY03NOV2623250PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23250.6` (VWAP `23282.1`) | PCR `0.62` | 3m dOI `-102,050` (`SHORT_COVERING`) | 15m PE dOI `+615,680` vs CE dOI `+2,453,295` | Vol Ratio `0.98x` | IV `16.9%` | Delta `-0.54` | Theta Bleed `41.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23250.6 vs VWAP 23282.1 (Basis -24.2))**
  - ✔️ **R2: Option > VWAP (PE LTP 96.75 vs VWAP 80.37 (3m dLTP +2.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +2,453,295 vs PE dOI +615,680, PE: SHORT_COVERING, PCR 0.62)**
  - ✔️ **R5: IV Stability (PE IV 16.92% (3m dIV -0.17%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.98x, BidQty 2080 vs AskQty 1170)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.54, Daily Theta Bleed 41.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹96.75` &rarr; Latest `₹35.55` | **Max LTP After:** `₹96.75` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-63.3%)**

### Entry #61 — `14:11:13` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23257.0` (VWAP `23281.7`) | PCR `0.63` | 3m dOI `+397,150` (`SHORT_BUILDUP`) | 15m PE dOI `+94,055` vs CE dOI `+3,340,025` | Vol Ratio `0.85x` | IV `16.7%` | Delta `-0.52` | Theta Bleed `44.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23257.0 vs VWAP 23281.7 (Basis -18.7))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +3,340,025 vs PE dOI +94,055, PE: SHORT_BUILDUP, PCR 0.63)**
  - ✔️ **R5: IV Stability (PE IV 16.74% (3m dIV -0.18%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 89.45 vs VWAP 80.46 (3m dLTP -7.30))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.85x, BidQty 1820 vs AskQty 65)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.52, Daily Theta Bleed 44.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹89.45` &rarr; Latest `₹35.55` | **Max LTP After:** `₹89.45` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-60.3%)**

### Entry #62 — `14:14:14` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23264.9` (VWAP `23281.5`) | PCR `0.62` | 3m dOI `+125,710` (`SHORT_BUILDUP`) | 15m PE dOI `+1,503,190` vs CE dOI `+2,648,165` | Vol Ratio `0.70x` | IV `16.6%` | Delta `-0.51` | Theta Bleed `46.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23264.9 vs VWAP 23281.5 (Basis -19.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +2,648,165 vs PE dOI +1,503,190, PE: SHORT_BUILDUP, PCR 0.62)**
  - ✔️ **R5: IV Stability (PE IV 16.63% (3m dIV -0.11%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 85.35 vs VWAP 80.50 (3m dLTP -4.10))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.70x, BidQty 1950 vs AskQty 3380)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.51, Daily Theta Bleed 46.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹85.35` &rarr; Latest `₹35.55` | **Max LTP After:** `₹85.35` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-58.4%)**

### Entry #63 — `14:17:15` | **NIFTY03NOV2623250PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23274.4` (VWAP `23281.4`) | PCR `0.62` | 3m dOI `+14,170` (`SHORT_BUILDUP`) | 15m PE dOI `-98,020` vs CE dOI `-1,186,900` | Vol Ratio `1.38x` | IV `16.5%` | Delta `-0.48` | Theta Bleed `50.8%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23274.4 vs VWAP 23281.4 (Basis -13.6))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -1,186,900 vs PE dOI -98,020, PE: SHORT_BUILDUP, PCR 0.62)**
  - ✔️ **R5: IV Stability (PE IV 16.47% (3m dIV -0.16%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 76.70 vs VWAP 80.44 (3m dLTP -8.65))**
  - ❌ **R4: Volume Burst (Vol Ratio 1.38x, BidQty 2665 vs AskQty 5850)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.48, Daily Theta Bleed 50.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹76.70` &rarr; Latest `₹35.55` | **Max LTP After:** `₹77.45` (**`+1.0%`**) &rarr; **FILTER SAVED LOSS (-53.6%)**

### Entry #64 — `14:20:16` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23279.5` (VWAP `23281.3`) | PCR `0.51` | 3m dOI `+535,600` (`SHORT_BUILDUP`) | 15m PE dOI `+1,674,400` vs CE dOI `-4,472,325` | Vol Ratio `0.72x` | IV `16.2%` | Delta `-0.57` | Theta Bleed `37.8%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23279.5 vs VWAP 23281.3 (Basis -15.8))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -4,472,325 vs PE dOI +1,674,400, PE: SHORT_BUILDUP, PCR 0.51)**
  - ✔️ **R5: IV Stability (PE IV 16.25% (3m dIV -0.20%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 100.30 vs VWAP 97.40 (3m dLTP -2.75))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.72x, BidQty 2080 vs AskQty 520)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.57, Daily Theta Bleed 37.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹100.30` &rarr; Latest `₹52.60` | **Max LTP After:** `₹104.05` (**`+3.7%`**) &rarr; **FILTER SAVED LOSS (-47.6%)**

### Entry #65 — `14:23:17` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23283.3` (VWAP `23281.4`) | PCR `0.51` | 3m dOI `+302,900` (`LONG_BUILDUP`) | 15m PE dOI `+2,825,420` vs CE dOI `-3,573,700` | Vol Ratio `0.68x` | IV `16.2%` | Delta `-0.57` | Theta Bleed `37.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R2: Option > VWAP (PE LTP 100.45 vs VWAP 97.42 (3m dLTP +0.15))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -3,573,700 vs PE dOI +2,825,420, PE: LONG_BUILDUP, PCR 0.51)**
  - ✔️ **R5: IV Stability (PE IV 16.21% (3m dIV -0.04%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23283.3 vs VWAP 23281.4 (Basis -20.3))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.68x, BidQty 715 vs AskQty 2145)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.57, Daily Theta Bleed 37.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹100.45` &rarr; Latest `₹52.60` | **Max LTP After:** `₹104.05` (**`+3.6%`**) &rarr; **FILTER SAVED LOSS (-47.6%)**

### Entry #66 — `14:26:18` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23284.3` (VWAP `23281.4`) | PCR `0.53` | 3m dOI `+462,410` (`LONG_BUILDUP`) | 15m PE dOI `+4,243,720` vs CE dOI `-5,656,950` | Vol Ratio `0.62x` | IV `16.2%` | Delta `-0.58` | Theta Bleed `37.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R2: Option > VWAP (PE LTP 101.85 vs VWAP 97.45 (3m dLTP +1.40))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -5,656,950 vs PE dOI +4,243,720, PE: LONG_BUILDUP, PCR 0.53)**
  - ✔️ **R5: IV Stability (PE IV 16.22% (3m dIV +0.01%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23284.3 vs VWAP 23281.4 (Basis -23.9))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.62x, BidQty 2470 vs AskQty 520)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.58, Daily Theta Bleed 37.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹101.85` &rarr; Latest `₹52.60` | **Max LTP After:** `₹104.05` (**`+2.2%`**) &rarr; **FILTER SAVED LOSS (-48.4%)**

### Entry #67 — `14:29:18` | **NIFTY03NOV2623300PE** (PE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23280.7` (VWAP `23281.4`) | PCR `0.55` | 3m dOI `+501,670` (`LONG_BUILDUP`) | 15m PE dOI `+5,364,255` vs CE dOI `-8,634,210` | Vol Ratio `0.58x` | IV `16.1%` | Delta `-0.59` | Theta Bleed `35.9%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23280.7 vs VWAP 23281.4 (Basis -25.2))**
  - ✔️ **R2: Option > VWAP (PE LTP 104.05 vs VWAP 97.49 (3m dLTP +2.20))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -8,634,210 vs PE dOI +5,364,255, PE: LONG_BUILDUP, PCR 0.55)**
  - ✔️ **R5: IV Stability (PE IV 16.09% (3m dIV -0.13%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.58x, BidQty 325 vs AskQty 2015)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.59, Daily Theta Bleed 35.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹104.05` &rarr; Latest `₹52.60` | **Max LTP After:** `₹104.05` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-49.5%)**

### Entry #68 — `14:32:19` | **NIFTY03NOV2623300CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23284.9` (VWAP `23281.4`) | PCR `0.55` | 3m dOI `-689,065` (`SHORT_COVERING`) | 15m PE dOI `+5,151,315` vs CE dOI `-6,583,785` | Vol Ratio `1.51x` | IV `15.9%` | Delta `0.44` | Theta Bleed `57.9%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +5,151,315 vs CE dOI -6,583,785, CE: SHORT_COVERING, PCR 0.55)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.51x, BidQty 4160 vs AskQty 3055)**
  - ✔️ **R5: IV Stability (CE IV 15.94% (3m dIV -0.15%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23284.9 vs VWAP 23281.4 (Basis -15.1))**
  - ❌ **R2: Option > VWAP (CE LTP 64.85 vs VWAP 81.87 (3m dLTP +5.30))**
  - ❌ **R6: Greeks & Theta (Delta 0.44, Daily Theta Bleed 57.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹64.85` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+64.8%`**) &rarr; **MISSED WINNER (+64.8% -> Tune Missing Rule!)**

### Entry #69 — `14:38:26` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23320.0` (VWAP `23282.2`) | PCR `0.63` | 3m dOI `+1,083,485` (`SHORT_BUILDUP`) | 15m PE dOI `+4,740,580` vs CE dOI `-15,527,460` | Vol Ratio `1.55x` | IV `16.0%` | Delta `-0.48` | Theta Bleed `51.6%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -15,527,460 vs PE dOI +4,740,580, PE: SHORT_BUILDUP, PCR 0.63)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.55x, BidQty 2210 vs AskQty 1170)**
  - ✔️ **R5: IV Stability (PE IV 16.00% (3m dIV +0.22%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23320.0 vs VWAP 23282.2 (Basis -9.3))**
  - ❌ **R2: Option > VWAP (PE LTP 74.00 vs VWAP 97.04 (3m dLTP -14.15))**
  - ❌ **R6: Greeks & Theta (|Delta| 0.48, Daily Theta Bleed 51.6% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹74.00` &rarr; Latest `₹52.60` | **Max LTP After:** `₹83.00` (**`+12.2%`**) &rarr; **MISSED WINNER (+12.2% -> Tune Missing Rule!)**

### Entry #70 — `14:38:26` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23320.0` (VWAP `23282.2`) | PCR `0.63` | 3m dOI `-2,811,055` (`SHORT_COVERING`) | 15m PE dOI `+4,740,580` vs CE dOI `-15,527,460` | Vol Ratio `3.22x` | IV `16.0%` | Delta `0.52` | Theta Bleed `45.1%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23320.0 vs VWAP 23282.2 (Basis -9.3))**
  - ✔️ **R2: Option > VWAP (CE LTP 84.70 vs VWAP 81.81 (3m dLTP +15.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +4,740,580 vs CE dOI -15,527,460, CE: SHORT_COVERING, PCR 0.63)**
  - ✔️ **R5: IV Stability (CE IV 16.00% (3m dIV +0.22%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 3.22x, BidQty 910 vs AskQty 3900)**
  - ❌ **R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 45.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹84.70` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+26.2%`**) &rarr; **MISSED WINNER (+26.2% -> Tune Missing Rule!)**

### Entry #71 — `14:41:26` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23303.0` (VWAP `23282.5`) | PCR `0.65` | 3m dOI `-1,184,625` (`LONG_UNWINDING`) | 15m PE dOI `+5,398,900` vs CE dOI `-15,087,020` | Vol Ratio `1.37x` | IV `15.8%` | Delta `0.49` | Theta Bleed `49.8%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23303.0 vs VWAP 23282.5 (Basis -7.7))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +5,398,900 vs CE dOI -15,087,020, CE: LONG_UNWINDING, PCR 0.65)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.37x, BidQty 2275 vs AskQty 455)**
  - ✔️ **R5: IV Stability (CE IV 15.84% (3m dIV -0.16%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 76.00 vs VWAP 81.73 (3m dLTP -8.70))**
  - ❌ **R6: Greeks & Theta (Delta 0.49, Daily Theta Bleed 49.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹76.00` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+40.7%`**) &rarr; **MISSED WINNER (+40.7% -> Tune Missing Rule!)**

### Entry #72 — `14:44:27` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23318.4` (VWAP `23282.9`) | PCR `0.66` | 3m dOI `-480,220` (`SHORT_COVERING`) | 15m PE dOI `+3,365,505` vs CE dOI `-15,194,725` | Vol Ratio `1.70x` | IV `16.2%` | Delta `0.53` | Theta Bleed `45.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23318.4 vs VWAP 23282.9 (Basis -6.5))**
  - ✔️ **R2: Option > VWAP (CE LTP 86.35 vs VWAP 81.81 (3m dLTP +10.35))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +3,365,505 vs CE dOI -15,194,725, CE: SHORT_COVERING, PCR 0.66)**
  - ✔️ **R5: IV Stability (CE IV 16.24% (3m dIV +0.40%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.70x, BidQty 1755 vs AskQty 3315)**
  - ❌ **R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 45.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹86.35` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+23.8%`**) &rarr; **MISSED WINNER (+23.8% -> Tune Missing Rule!)**

### Entry #73 — `14:44:55` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23323.0` (VWAP `23283.4`) | PCR `0.68` | 3m dOI `-1,117,740` (`SHORT_COVERING`) | 15m PE dOI `+3,231,865` vs CE dOI `-18,237,700` | Vol Ratio `0.27x` | IV `16.2%` | Delta `0.53` | Theta Bleed `44.1%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23323.0 vs VWAP 23283.4 (Basis -8.2))**
  - ✔️ **R2: Option > VWAP (CE LTP 87.60 vs VWAP 81.82 (3m dLTP +11.60))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +3,231,865 vs CE dOI -18,237,700, CE: SHORT_COVERING, PCR 0.68)**
  - ✔️ **R5: IV Stability (CE IV 16.19% (3m dIV +0.35%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.27x, BidQty 2275 vs AskQty 390)**
  - ❌ **R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 44.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹87.60` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+22.0%`**) &rarr; **MISSED WINNER (+22.0% -> Tune Missing Rule!)**

### Entry #74 — `14:47:56` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23322.6` (VWAP `23283.9`) | PCR `0.71` | 3m dOI `-1,235,650` (`LONG_UNWINDING`) | 15m PE dOI `+5,514,925` vs CE dOI `-21,110,700` | Vol Ratio `1.40x` | IV `16.1%` | Delta `0.52` | Theta Bleed `45.8%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23322.6 vs VWAP 23283.9 (Basis -13.3))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +5,514,925 vs CE dOI -21,110,700, CE: LONG_UNWINDING, PCR 0.71)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.40x, BidQty 3185 vs AskQty 2860)**
  - ✔️ **R5: IV Stability (CE IV 16.09% (3m dIV -0.10%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 84.15 vs VWAP 81.85 (3m dLTP -3.45))**
  - ❌ **R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 45.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹84.15` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+27.0%`**) &rarr; **MISSED WINNER (+27.0% -> Tune Missing Rule!)**

### Entry #75 — `14:50:56` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23316.8` (VWAP `23284.3`) | PCR `0.75` | 3m dOI `-990,080` (`SHORT_COVERING`) | 15m PE dOI `+4,690,855` vs CE dOI `-22,510,995` | Vol Ratio `1.21x` | IV `16.2%` | Delta `0.52` | Theta Bleed `45.7%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23316.8 vs VWAP 23284.3 (Basis -7.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 85.05 vs VWAP 81.89 (3m dLTP +0.90))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +4,690,855 vs CE dOI -22,510,995, CE: SHORT_COVERING, PCR 0.75)**
  - ✔️ **R5: IV Stability (CE IV 16.22% (3m dIV +0.13%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.21x, BidQty 1365 vs AskQty 5785)**
  - ❌ **R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 45.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹85.05` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+25.7%`**) &rarr; **MISSED WINNER (+25.7% -> Tune Missing Rule!)**

### Entry #76 — `14:51:16` | **NIFTY03NOV2623300CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23315.7` (VWAP `23284.7`) | PCR `0.75` | 3m dOI `-990,080` (`LONG_UNWINDING`) | 15m PE dOI `+4,690,855` vs CE dOI `-22,510,995` | Vol Ratio `0.22x` | IV `16.1%` | Delta `0.51` | Theta Bleed `47.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23315.7 vs VWAP 23284.7 (Basis -10.1))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +4,690,855 vs CE dOI -22,510,995, CE: LONG_UNWINDING, PCR 0.75)**
  - ✔️ **R5: IV Stability (CE IV 16.12% (3m dIV +0.03%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 82.35 vs VWAP 81.89 (3m dLTP -1.80))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.22x, BidQty 2015 vs AskQty 325)**
  - ❌ **R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 47.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹82.35` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+29.8%`**) &rarr; **MISSED WINNER (+29.8% -> Tune Missing Rule!)**

### Entry #77 — `14:54:16` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23319.7` (VWAP `23285.1`) | PCR `0.75` | 3m dOI `-26,455` (`SHORT_COVERING`) | 15m PE dOI `+3,277,755` vs CE dOI `-13,018,135` | Vol Ratio `0.96x` | IV `16.4%` | Delta `0.52` | Theta Bleed `46.5%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23319.7 vs VWAP 23285.1 (Basis -12.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 84.85 vs VWAP 81.92 (3m dLTP +2.50))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +3,277,755 vs CE dOI -13,018,135, CE: SHORT_COVERING, PCR 0.75)**
  - ✔️ **R5: IV Stability (CE IV 16.44% (3m dIV +0.32%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.96x, BidQty 1560 vs AskQty 975)**
  - ❌ **R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 46.5% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹84.85` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+26.0%`**) &rarr; **MISSED WINNER (+26.0% -> Tune Missing Rule!)**

### Entry #78 — `14:57:17` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23324.5` (VWAP `23285.5`) | PCR `0.76` | 3m dOI `-373,100` (`SHORT_COVERING`) | 15m PE dOI `+580,710` vs CE dOI `-13,591,370` | Vol Ratio `0.63x` | IV `16.2%` | Delta `0.53` | Theta Bleed `45.3%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23324.5 vs VWAP 23285.5 (Basis -12.5))**
  - ✔️ **R2: Option > VWAP (CE LTP 86.10 vs VWAP 81.94 (3m dLTP +1.25))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +580,710 vs CE dOI -13,591,370, CE: SHORT_COVERING, PCR 0.76)**
  - ✔️ **R5: IV Stability (CE IV 16.25% (3m dIV -0.19%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.63x, BidQty 2405 vs AskQty 5070)**
  - ❌ **R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 45.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹86.10` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+24.2%`**) &rarr; **MISSED WINNER (+24.2% -> Tune Missing Rule!)**

### Entry #79 — `15:00:18` | **NIFTY03NOV2623300CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23316.3` (VWAP `23285.9`) | PCR `0.76` | 3m dOI `-183,950` (`LONG_UNWINDING`) | 15m PE dOI `+1,440,595` vs CE dOI `-8,808,800` | Vol Ratio `0.77x` | IV `16.1%` | Delta `0.51` | Theta Bleed `48.3%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23316.3 vs VWAP 23285.9 (Basis -14.1))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +1,440,595 vs CE dOI -8,808,800, CE: LONG_UNWINDING, PCR 0.76)**
  - ✔️ **R5: IV Stability (CE IV 16.12% (3m dIV -0.13%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 80.35 vs VWAP 81.93 (3m dLTP -5.75))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.77x, BidQty 1365 vs AskQty 2925)**
  - ❌ **R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 48.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹80.35` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+33.0%`**) &rarr; **MISSED WINNER (+33.0% -> Tune Missing Rule!)**

### Entry #80 — `15:03:19` | **NIFTY03NOV2623300PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23310.8` (VWAP `23286.2`) | PCR `0.78` | 3m dOI `+70,590` (`LONG_BUILDUP`) | 15m PE dOI `+190,060` vs CE dOI `-7,175,415` | Vol Ratio `1.66x` | IV `16.1%` | Delta `-0.51` | Theta Bleed `47.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -7,175,415 vs PE dOI +190,060, PE: LONG_BUILDUP, PCR 0.78)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.66x, BidQty 650 vs AskQty 845)**
  - ✔️ **R5: IV Stability (PE IV 16.08% (3m dIV -0.04%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23310.8 vs VWAP 23286.2 (Basis -17.1))**
  - ❌ **R2: Option > VWAP (PE LTP 82.10 vs VWAP 95.56 (3m dLTP +3.95))**
  - ❌ **R6: Greeks & Theta (|Delta| 0.51, Daily Theta Bleed 47.1% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹82.10` &rarr; Latest `₹52.60` | **Max LTP After:** `₹83.00` (**`+1.1%`**) &rarr; **FILTER SAVED LOSS (-35.9%)**

### Entry #81 — `15:09:21` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23313.8` (VWAP `23286.7`) | PCR `0.76` | 3m dOI `-224,835` (`SHORT_COVERING`) | 15m PE dOI `-3,359,655` vs CE dOI `-4,604,665` | Vol Ratio `0.80x` | IV `16.1%` | Delta `0.52` | Theta Bleed `47.2%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23313.8 vs VWAP 23286.7 (Basis -6.9))**
  - ✔️ **R2: Option > VWAP (CE LTP 82.10 vs VWAP 81.84 (3m dLTP +6.45))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -3,359,655 vs CE dOI -4,604,665, CE: SHORT_COVERING, PCR 0.76)**
  - ✔️ **R5: IV Stability (CE IV 16.05% (3m dIV -0.12%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.80x, BidQty 1105 vs AskQty 650)**
  - ❌ **R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 47.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹82.10` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+30.2%`**) &rarr; **MISSED WINNER (+30.2% -> Tune Missing Rule!)**

### Entry #82 — `15:10:55` | **NIFTY03NOV2623300CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23321.5` (VWAP `23287.1`) | PCR `0.75` | 3m dOI `-255,840` (`SHORT_COVERING`) | 15m PE dOI `-4,757,285` vs CE dOI `-3,582,475` | Vol Ratio `0.63x` | IV `16.1%` | Delta `0.53` | Theta Bleed `45.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23321.5 vs VWAP 23287.1 (Basis -7.3))**
  - ✔️ **R2: Option > VWAP (CE LTP 86.40 vs VWAP 81.86 (3m dLTP +10.75))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -4,757,285 vs CE dOI -3,582,475, CE: SHORT_COVERING, PCR 0.75)**
  - ✔️ **R5: IV Stability (CE IV 16.15% (3m dIV -0.02%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.63x, BidQty 2015 vs AskQty 260)**
  - ❌ **R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 45.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹86.40` &rarr; Latest `₹96.95` | **Max LTP After:** `₹106.90` (**`+23.7%`**) &rarr; **MISSED WINNER (+23.7% -> Tune Missing Rule!)**

### Entry #83 — `15:22:57` | **NIFTY03NOV2623350CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23331.1` (VWAP `23288.9`) | PCR `0.62` | 3m dOI `-945,880` (`SHORT_COVERING`) | 15m PE dOI `-6,311,955` vs CE dOI `-11,550,305` | Vol Ratio `1.15x` | IV `15.4%` | Delta `0.45` | Theta Bleed `59.2%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23331.1 vs VWAP 23288.9 (Basis -7.8))**
  - ✔️ **R2: Option > VWAP (CE LTP 62.45 vs VWAP 61.48 (3m dLTP +3.50))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -6,311,955 vs CE dOI -11,550,305, CE: SHORT_COVERING, PCR 0.62)**
  - ✔️ **R5: IV Stability (CE IV 15.36% (3m dIV -0.21%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.15x, BidQty 1495 vs AskQty 65)**
  - ❌ **R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 59.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹62.45` &rarr; Latest `₹70.00` | **Max LTP After:** `₹77.55` (**`+24.2%`**) &rarr; **MISSED WINNER (+24.2% -> Tune Missing Rule!)**

### Entry #84 — `15:25:58` | **NIFTY03NOV2623350CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23331.1` (VWAP `23289.3`) | PCR `0.63` | 3m dOI `-474,110` (`SHORT_COVERING`) | 15m PE dOI `-6,394,895` vs CE dOI `-13,523,250` | Vol Ratio `0.54x` | IV `15.3%` | Delta `0.45` | Theta Bleed `57.9%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23331.1 vs VWAP 23289.3 (Basis -4.2))**
  - ✔️ **R2: Option > VWAP (CE LTP 63.95 vs VWAP 61.49 (3m dLTP +1.50))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -6,394,895 vs CE dOI -13,523,250, CE: SHORT_COVERING, PCR 0.63)**
  - ✔️ **R5: IV Stability (CE IV 15.35% (3m dIV -0.01%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.54x, BidQty 1625 vs AskQty 195)**
  - ❌ **R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 57.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹63.95` &rarr; Latest `₹70.00` | **Max LTP After:** `₹77.55` (**`+21.3%`**) &rarr; **MISSED WINNER (+21.3% -> Tune Missing Rule!)**

### Entry #85 — `15:28:50` | **NIFTY03NOV2623350CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23331.1` (VWAP `23289.8`) | PCR `0.63` | 3m dOI `-717,860` (`SHORT_COVERING`) | 15m PE dOI `-6,438,575` vs CE dOI `-13,784,940` | Vol Ratio `0.54x` | IV `15.2%` | Delta `0.46` | Theta Bleed `57.3%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23331.1 vs VWAP 23289.8 (Basis -1.8))**
  - ✔️ **R2: Option > VWAP (CE LTP 64.20 vs VWAP 61.50 (3m dLTP +0.25))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -6,438,575 vs CE dOI -13,784,940, CE: SHORT_COVERING, PCR 0.63)**
  - ✔️ **R5: IV Stability (CE IV 15.20% (3m dIV -0.15%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 0.54x, BidQty 65 vs AskQty 520)**
  - ❌ **R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 57.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹64.20` &rarr; Latest `₹70.00` | **Max LTP After:** `₹77.55` (**`+20.8%`**) &rarr; **MISSED WINNER (+20.8% -> Tune Missing Rule!)**

### Entry #86 — `15:31:50` | **NIFTY03NOV2623450CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23440.8` (VWAP `23291.3`) | PCR `0.46` | 3m dOI `-256,425` (`SHORT_COVERING`) | 15m PE dOI `-2,764,385` vs CE dOI `-18,012,410` | Vol Ratio `2.07x` | IV `15.3%` | Delta `0.30` | Theta Bleed `92.9%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R2: Option > VWAP (CE LTP 34.85 vs VWAP 29.54 (3m dLTP +4.25))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -2,764,385 vs CE dOI -18,012,410, CE: SHORT_COVERING, PCR 0.46)**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.07x, BidQty 1170 vs AskQty 65)**
  - ✔️ **R5: IV Stability (CE IV 15.32% (3m dIV -0.28%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23291.3 (Basis -91.3))**
  - ❌ **R6: Greeks & Theta (Delta 0.30, Daily Theta Bleed 92.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹34.85` &rarr; Latest `₹34.20` | **Max LTP After:** `₹37.40` (**`+7.3%`**) &rarr; **TRACKING (Max +7.3%)**

### Entry #87 — `15:34:51` | **NIFTY03NOV2623450PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23440.8` (VWAP `23292.8`) | PCR `0.46` | 3m dOI `+36,920` (`SHORT_BUILDUP`) | 15m PE dOI `-2,806,895` vs CE dOI `-18,104,515` | Vol Ratio `0.86x` | IV `15.2%` | Delta `-0.69` | Theta Bleed `25.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -18,104,515 vs PE dOI -2,806,895, PE: SHORT_BUILDUP, PCR 0.46)**
  - ✔️ **R5: IV Stability (PE IV 15.24% (3m dIV -0.08%))**
  - ✔️ **R6: Greeks & Theta (|Delta| 0.69, Daily Theta Bleed 25.7% (Max 30%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23292.8 (Basis -82.2))**
  - ❌ **R2: Option > VWAP (PE LTP 128.85 vs VWAP 185.21 (3m dLTP -7.10))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.86x, BidQty 455 vs AskQty 390)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹128.85` &rarr; Latest `₹139.50` | **Max LTP After:** `₹139.50` (**`+8.3%`**) &rarr; **TRACKING (Max +8.3%)**

### Entry #88 — `15:34:51` | **NIFTY03NOV2623450CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23440.8` (VWAP `23292.8`) | PCR `0.46` | 3m dOI `-64,090` (`SHORT_COVERING`) | 15m PE dOI `-2,806,895` vs CE dOI `-18,104,515` | Vol Ratio `1.08x` | IV `15.2%` | Delta `0.31` | Theta Bleed `88.4%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R2: Option > VWAP (CE LTP 37.40 vs VWAP 29.61 (3m dLTP +2.55))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -2,806,895 vs CE dOI -18,104,515, CE: SHORT_COVERING, PCR 0.46)**
  - ✔️ **R5: IV Stability (CE IV 15.24% (3m dIV -0.08%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23292.8 (Basis -82.2))**
  - ❌ **R4: Volume Burst (Vol Ratio 1.08x, BidQty 1040 vs AskQty 65)**
  - ❌ **R6: Greeks & Theta (Delta 0.31, Daily Theta Bleed 88.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹37.40` &rarr; Latest `₹34.20` | **Max LTP After:** `₹37.40` (**`+0.0%`**) &rarr; **TRACKING (Max +0.0%)**

### Entry #89 — `15:37:52` | **NIFTY03NOV2623450PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23440.8` (VWAP `23294.3`) | PCR `0.47` | 3m dOI `+33,280` (`LONG_BUILDUP`) | 15m PE dOI `-3,004,040` vs CE dOI `-18,001,295` | Vol Ratio `0.83x` | IV `15.5%` | Delta `-0.70` | Theta Bleed `24.8%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI -18,001,295 vs PE dOI -3,004,040, PE: LONG_BUILDUP, PCR 0.47)**
  - ✔️ **R5: IV Stability (PE IV 15.53% (3m dIV +0.29%))**
  - ✔️ **R6: Greeks & Theta (|Delta| 0.70, Daily Theta Bleed 24.8% (Max 30%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23294.3 (Basis -88.6))**
  - ❌ **R2: Option > VWAP (PE LTP 134.40 vs VWAP 184.85 (3m dLTP +5.55))**
  - ❌ **R4: Volume Burst (Vol Ratio 0.83x, BidQty 130 vs AskQty 260)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹134.40` &rarr; Latest `₹139.50` | **Max LTP After:** `₹139.50` (**`+3.8%`**) &rarr; **TRACKING (Max +3.8%)**

---

## 3. Quick Comparison Table (`Score >= 3/6`)

| Time | Symbol | Side | Score | Entry LTP | Max LTP After | Max Gain % | Verdict | What Was Good (Passed) | Why It Missed 6/6 (Failed) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| `11:25:06` | **NIFTY03NOV2623350CE** | CE | **3/6** | ₹70.75 | ₹92.35 | **`+30.5%`** | **MISSED WINNER (+30.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23327.4 vs VWAP 23320.2 (Basis -12.7)) ;; R2: Option > VWAP (CE LTP 70.75 vs VWAP 69.69 (3m dLTP +2.00)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +14,037,725 vs CE dOI -4,103,645, CE: LONG_BUILDUP, PCR 0.89) | R4: Volume Burst (Vol Ratio 1.00x, BidQty 4095 vs AskQty 5070) ;; R5: IV Stability (CE IV 16.56% (3m dIV -0.37%)) ;; R6: Greeks & Theta (Delta 0.44, Daily Theta Bleed 52.0% (Max 30%)) |
| `11:28:21` | **NIFTY03NOV2623350CE** | CE | **3/6** | ₹70.30 | ₹92.35 | **`+31.4%`** | **MISSED WINNER (+31.4% -> Tune Missing Rule!)** | R2: Option > VWAP (CE LTP 70.30 vs VWAP 69.69 (3m dLTP +0.75)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +16,006,250 vs CE dOI -3,867,760, CE: LONG_BUILDUP, PCR 0.90) ;; R5: IV Stability (CE IV 16.63% (3m dIV +0.07%)) | R1: Spot/Basis Trend (Spot 23330.7 vs VWAP 23324.3 (Basis -17.6)) ;; R4: Volume Burst (Vol Ratio 0.04x, BidQty 975 vs AskQty 3120) ;; R6: Greeks & Theta (Delta 0.43, Daily Theta Bleed 52.6% (Max 30%)) |
| `11:31:21` | **NIFTY03NOV2623350CE** | CE | **4/6** | ₹74.70 | ₹92.35 | **`+23.6%`** | **MISSED WINNER (+23.6% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23338.0 vs VWAP 23327.1 (Basis -12.8)) ;; R2: Option > VWAP (CE LTP 74.70 vs VWAP 69.78 (3m dLTP +4.40)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +14,247,220 vs CE dOI -2,614,755, CE: LONG_BUILDUP, PCR 0.88) ;; R5: IV Stability (CE IV 16.45% (3m dIV -0.18%)) | R4: Volume Burst (Vol Ratio 0.12x, BidQty 3965 vs AskQty 5980) ;; R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 49.3% (Max 30%)) |
| `11:37:22` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹87.30 | ₹154.05 | **`+76.5%`** | **MISSED WINNER (+76.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23313.8 vs VWAP 23323.9 (Basis -13.3)) ;; R2: Option > VWAP (PE LTP 87.30 vs VWAP 86.91 (3m dLTP +1.70)) ;; R5: IV Stability (PE IV 16.76% (3m dIV -0.05%)) | R3: Trapped Writers / PCR / dOI (15m CE dOI -2,266,745 vs PE dOI +16,558,750, PE: LONG_BUILDUP, PCR 1.07) ;; R4: Volume Burst (Vol Ratio 0.33x, BidQty 260 vs AskQty 1625) ;; R6: Greeks & Theta (/Delta/ 0.50, Daily Theta Bleed 43.3% (Max 30%)) |
| `11:40:23` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹86.60 | ₹154.05 | **`+77.9%`** | **MISSED WINNER (+77.9% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23311.0 vs VWAP 23322.3 (Basis -9.2)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +2,891,005 vs PE dOI +1,055,535, PE: LONG_UNWINDING, PCR 1.05) ;; R5: IV Stability (PE IV 16.70% (3m dIV -0.06%)) | R2: Option > VWAP (PE LTP 86.60 vs VWAP 86.91 (3m dLTP -0.70)) ;; R4: Volume Burst (Vol Ratio 0.33x, BidQty 3445 vs AskQty 2535) ;; R6: Greeks & Theta (/Delta/ 0.49, Daily Theta Bleed 43.5% (Max 30%)) |
| `11:43:24` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹90.60 | ₹154.05 | **`+70.0%`** | **MISSED WINNER (+70.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23307.9 vs VWAP 23320.7 (Basis -13.9)) ;; R2: Option > VWAP (PE LTP 90.60 vs VWAP 86.99 (3m dLTP +4.00)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,198,520 vs PE dOI -238,810, PE: LONG_BUILDUP, PCR 1.04) ;; R5: IV Stability (PE IV 16.73% (3m dIV +0.03%)) | R4: Volume Burst (Vol Ratio 0.32x, BidQty 2405 vs AskQty 4225) ;; R6: Greeks & Theta (/Delta/ 0.51, Daily Theta Bleed 41.7% (Max 30%)) |
| `11:46:25` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹91.10 | ₹154.05 | **`+69.1%`** | **MISSED WINNER (+69.1% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23307.2 vs VWAP 23319.4 (Basis -14.8)) ;; R2: Option > VWAP (PE LTP 91.10 vs VWAP 87.10 (3m dLTP +0.50)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,661,450 vs PE dOI -58,890, PE: SHORT_COVERING, PCR 1.01) ;; R5: IV Stability (PE IV 16.69% (3m dIV -0.04%)) | R4: Volume Burst (Vol Ratio 0.47x, BidQty 2665 vs AskQty 1820) ;; R6: Greeks & Theta (/Delta/ 0.51, Daily Theta Bleed 41.4% (Max 30%)) |
| `11:49:26` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹96.55 | ₹154.05 | **`+59.5%`** | **MISSED WINNER (+59.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23294.5 vs VWAP 23317.1 (Basis -12.7)) ;; R2: Option > VWAP (PE LTP 96.55 vs VWAP 87.42 (3m dLTP +5.45)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +5,314,790 vs PE dOI -4,639,830, PE: SHORT_COVERING, PCR 0.97) ;; R5: IV Stability (PE IV 16.70% (3m dIV +0.01%)) | R4: Volume Burst (Vol Ratio 0.61x, BidQty 910 vs AskQty 10075) ;; R6: Greeks & Theta (/Delta/ 0.53, Daily Theta Bleed 39.0% (Max 30%)) |
| `11:52:27` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹100.90 | ₹154.05 | **`+52.7%`** | **MISSED WINNER (+52.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23288.8 vs VWAP 23314.7 (Basis -13.9)) ;; R2: Option > VWAP (PE LTP 100.90 vs VWAP 87.85 (3m dLTP +4.35)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +5,486,130 vs PE dOI -7,647,770, PE: SHORT_COVERING, PCR 0.93) ;; R5: IV Stability (PE IV 16.78% (3m dIV +0.08%)) | R4: Volume Burst (Vol Ratio 0.62x, BidQty 4745 vs AskQty 2210) ;; R6: Greeks & Theta (/Delta/ 0.54, Daily Theta Bleed 37.4% (Max 30%)) |
| `11:55:28` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹97.70 | ₹154.05 | **`+57.7%`** | **MISSED WINNER (+57.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23298.8 vs VWAP 23313.5 (Basis -17.5)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,062,405 vs PE dOI -10,776,675, PE: LONG_UNWINDING, PCR 0.86) ;; R5: IV Stability (PE IV 16.90% (3m dIV +0.12%)) | R2: Option > VWAP (PE LTP 97.70 vs VWAP 88.10 (3m dLTP -3.20)) ;; R4: Volume Burst (Vol Ratio 0.54x, BidQty 65 vs AskQty 1235) ;; R6: Greeks & Theta (/Delta/ 0.53, Daily Theta Bleed 39.1% (Max 30%)) |
| `11:58:29` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹94.70 | ₹154.05 | **`+62.7%`** | **MISSED WINNER (+62.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23309.3 vs VWAP 23313.2 (Basis -23.4)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +9,684,155 vs PE dOI -11,520,535, PE: SHORT_BUILDUP, PCR 0.84) ;; R5: IV Stability (PE IV 16.79% (3m dIV -0.11%)) | R2: Option > VWAP (PE LTP 94.70 vs VWAP 88.19 (3m dLTP -3.00)) ;; R4: Volume Burst (Vol Ratio 0.30x, BidQty 65 vs AskQty 65) ;; R6: Greeks & Theta (/Delta/ 0.52, Daily Theta Bleed 40.2% (Max 30%)) |
| `12:05:21` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹93.80 | ₹154.05 | **`+64.2%`** | **MISSED WINNER (+64.2% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23303.5 vs VWAP 23313.1 (Basis -17.1)) ;; R2: Option > VWAP (PE LTP 93.80 vs VWAP 88.36 (3m dLTP +5.45)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +7,816,380 vs PE dOI -7,329,270, PE: LONG_BUILDUP, PCR 0.82) ;; R5: IV Stability (PE IV 16.71% (3m dIV +0.07%)) | R4: Volume Burst (Vol Ratio 0.85x, BidQty 520 vs AskQty 2275) ;; R6: Greeks & Theta (/Delta/ 0.52, Daily Theta Bleed 40.4% (Max 30%)) |
| `12:06:14` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹91.95 | ₹154.05 | **`+67.5%`** | **MISSED WINNER (+67.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23304.8 vs VWAP 23312.6 (Basis -15.6)) ;; R2: Option > VWAP (PE LTP 91.95 vs VWAP 88.38 (3m dLTP +3.60)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,977,295 vs PE dOI -5,066,490, PE: LONG_BUILDUP, PCR 0.81) ;; R5: IV Stability (PE IV 16.64% (3m dIV +0.00%)) | R4: Volume Burst (Vol Ratio 0.13x, BidQty 650 vs AskQty 2600) ;; R6: Greeks & Theta (/Delta/ 0.52, Daily Theta Bleed 41.1% (Max 30%)) |
| `12:09:14` | **NIFTY03NOV2623300CE** | CE | **3/6** | ₹91.25 | ₹121.35 | **`+33.0%`** | **MISSED WINNER (+33.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23315.1 vs VWAP 23312.8 (Basis -9.6)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -711,555 vs CE dOI +791,570, CE: SHORT_COVERING, PCR 0.83) ;; R5: IV Stability (CE IV 17.03% (3m dIV +0.39%)) | R2: Option > VWAP (CE LTP 91.25 vs VWAP 92.09 (3m dLTP +10.10)) ;; R4: Volume Burst (Vol Ratio 0.84x, BidQty 2795 vs AskQty 1170) ;; R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 42.5% (Max 30%)) |
| `12:12:14` | **NIFTY03NOV2623350CE** | CE | **5/6** | ₹86.45 | ₹92.35 | **`+6.8%`** | **FILTER SAVED LOSS (-19.0%)** | R1: Spot/Basis Trend (Spot 23335.1 vs VWAP 23313.9 (Basis +7.7)) ;; R2: Option > VWAP (CE LTP 86.45 vs VWAP 68.88 (3m dLTP +19.65)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -615,095 vs CE dOI -9,068,085, CE: SHORT_COVERING, PCR 0.74) ;; R4: Volume Burst (Vol Ratio 1.61x, BidQty 1950 vs AskQty 715) ;; R5: IV Stability (CE IV 17.31% (3m dIV +0.53%)) | R6: Greeks & Theta (Delta 0.49, Daily Theta Bleed 45.7% (Max 30%)) |
| `12:13:30` | **NIFTY03NOV2623350CE** | CE | **4/6** | ₹80.05 | ₹92.35 | **`+15.4%`** | **MISSED WINNER (+15.4% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23331.7 vs VWAP 23314.7 (Basis +1.0)) ;; R2: Option > VWAP (CE LTP 80.05 vs VWAP 69.07 (3m dLTP +13.25)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -282,165 vs CE dOI -13,325,195, CE: SHORT_COVERING, PCR 0.77) ;; R5: IV Stability (CE IV 17.03% (3m dIV +0.25%)) | R4: Volume Burst (Vol Ratio 0.55x, BidQty 1170 vs AskQty 260) ;; R6: Greeks & Theta (Delta 0.47, Daily Theta Bleed 48.4% (Max 30%)) |
| `12:16:30` | **NIFTY03NOV2623350CE** | CE | **4/6** | ₹92.35 | ₹92.35 | **`+0.0%`** | **FILTER SAVED LOSS (-24.2%)** | R1: Spot/Basis Trend (Spot 23349.1 vs VWAP 23316.3 (Basis +4.0)) ;; R2: Option > VWAP (CE LTP 92.35 vs VWAP 69.81 (3m dLTP +12.30)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +1,831,895 vs CE dOI -15,841,150, CE: LONG_BUILDUP, PCR 0.77) ;; R5: IV Stability (CE IV 17.49% (3m dIV +0.46%)) | R4: Volume Burst (Vol Ratio 1.06x, BidQty 910 vs AskQty 2080) ;; R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 43.3% (Max 30%)) |
| `12:19:30` | **NIFTY03NOV2623350CE** | CE | **3/6** | ₹89.15 | ₹89.15 | **`+0.0%`** | **FILTER SAVED LOSS (-21.5%)** | R1: Spot/Basis Trend (Spot 23346.9 vs VWAP 23317.6 (Basis +2.8)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +3,315,975 vs CE dOI -18,391,490, CE: LONG_UNWINDING, PCR 0.82) ;; R5: IV Stability (CE IV 17.23% (3m dIV -0.26%)) | R2: Option > VWAP (CE LTP 89.15 vs VWAP 70.27 (3m dLTP -3.20)) ;; R4: Volume Burst (Vol Ratio 0.83x, BidQty 1755 vs AskQty 1820) ;; R6: Greeks & Theta (Delta 0.50, Daily Theta Bleed 44.3% (Max 30%)) |
| `12:25:31` | **NIFTY03NOV2623350CE** | CE | **3/6** | ₹80.00 | ₹80.00 | **`+0.0%`** | **FILTER SAVED LOSS (-12.5%)** | R1: Spot/Basis Trend (Spot 23336.0 vs VWAP 23319.7 (Basis -0.4)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +6,672,965 vs CE dOI -8,006,115, CE: SHORT_BUILDUP, PCR 0.86) ;; R5: IV Stability (CE IV 16.81% (3m dIV -0.05%)) | R2: Option > VWAP (CE LTP 80.00 vs VWAP 70.58 (3m dLTP -0.10)) ;; R4: Volume Burst (Vol Ratio 0.42x, BidQty 1950 vs AskQty 260) ;; R6: Greeks & Theta (Delta 0.48, Daily Theta Bleed 48.1% (Max 30%)) |
| `12:27:49` | **NIFTY03NOV2623350CE** | CE | **3/6** | ₹79.00 | ₹79.00 | **`+0.0%`** | **FILTER SAVED LOSS (-11.4%)** | R1: Spot/Basis Trend (Spot 23335.1 vs VWAP 23320.3 (Basis -0.9)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +6,866,535 vs CE dOI -2,904,850, CE: SHORT_BUILDUP, PCR 0.85) ;; R5: IV Stability (CE IV 16.76% (3m dIV -0.10%)) | R2: Option > VWAP (CE LTP 79.00 vs VWAP 70.63 (3m dLTP -1.10)) ;; R4: Volume Burst (Vol Ratio 0.25x, BidQty 325 vs AskQty 455) ;; R6: Greeks & Theta (Delta 0.47, Daily Theta Bleed 48.6% (Max 30%)) |
| `12:30:50` | **NIFTY03NOV2623350CE** | CE | **3/6** | ₹74.70 | ₹77.55 | **`+3.8%`** | **TRACKING (Max +3.8%)** | R1: Spot/Basis Trend (Spot 23327.0 vs VWAP 23320.5 (Basis -0.8)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +6,181,305 vs CE dOI -2,854,410, CE: SHORT_BUILDUP, PCR 0.85) ;; R5: IV Stability (CE IV 16.66% (3m dIV -0.10%)) | R2: Option > VWAP (CE LTP 74.70 vs VWAP 70.69 (3m dLTP -4.30)) ;; R4: Volume Burst (Vol Ratio 0.53x, BidQty 520 vs AskQty 2795) ;; R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 50.9% (Max 30%)) |
| `12:33:51` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹96.00 | ₹154.05 | **`+60.5%`** | **MISSED WINNER (+60.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23294.3 vs VWAP 23319.6 (Basis -9.6)) ;; R2: Option > VWAP (PE LTP 96.00 vs VWAP 87.06 (3m dLTP +20.75)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -2,161,965 vs PE dOI +3,494,270, PE: SHORT_COVERING, PCR 1.08) ;; R5: IV Stability (PE IV 17.11% (3m dIV +0.11%)) | R4: Volume Burst (Vol Ratio 1.79x, BidQty 715 vs AskQty 1950) ;; R6: Greeks & Theta (/Delta/ 0.53, Daily Theta Bleed 40.8% (Max 30%)) |
| `12:36:17` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹85.35 | ₹154.05 | **`+80.5%`** | **MISSED WINNER (+80.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23306.9 vs VWAP 23319.2 (Basis -2.1)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +1,843,985 vs PE dOI -3,652,805, PE: SHORT_COVERING, PCR 1.00) ;; R5: IV Stability (PE IV 17.03% (3m dIV +0.03%)) | R2: Option > VWAP (PE LTP 85.35 vs VWAP 87.03 (3m dLTP +10.10)) ;; R4: Volume Burst (Vol Ratio 0.97x, BidQty 4485 vs AskQty 650) ;; R6: Greeks & Theta (/Delta/ 0.49, Daily Theta Bleed 45.8% (Max 30%)) |
| `12:39:18` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹83.75 | ₹154.05 | **`+83.9%`** | **MISSED WINNER (+83.9% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23311.2 vs VWAP 23319.0 (Basis -6.5)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +1,907,230 vs PE dOI -4,305,340, PE: SHORT_BUILDUP, PCR 0.98) ;; R5: IV Stability (PE IV 16.83% (3m dIV -0.20%)) | R2: Option > VWAP (PE LTP 83.75 vs VWAP 86.99 (3m dLTP -1.60)) ;; R4: Volume Burst (Vol Ratio 0.50x, BidQty 65 vs AskQty 130) ;; R6: Greeks & Theta (/Delta/ 0.49, Daily Theta Bleed 46.2% (Max 30%)) |
| `12:42:19` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹91.90 | ₹154.05 | **`+67.6%`** | **MISSED WINNER (+67.6% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23298.7 vs VWAP 23318.3 (Basis -7.7)) ;; R2: Option > VWAP (PE LTP 91.90 vs VWAP 87.07 (3m dLTP +8.15)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +1,775,995 vs PE dOI -2,570,685, PE: LONG_BUILDUP, PCR 1.00) ;; R5: IV Stability (PE IV 16.99% (3m dIV +0.16%)) | R4: Volume Burst (Vol Ratio 0.77x, BidQty 975 vs AskQty 2275) ;; R6: Greeks & Theta (/Delta/ 0.51, Daily Theta Bleed 42.5% (Max 30%)) |
| `12:45:19` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹95.65 | ₹154.05 | **`+61.1%`** | **MISSED WINNER (+61.1% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23290.3 vs VWAP 23317.5 (Basis -6.1)) ;; R2: Option > VWAP (PE LTP 95.65 vs VWAP 87.24 (3m dLTP +3.75)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,229,135 vs PE dOI -3,545,620, PE: SHORT_COVERING, PCR 0.97) ;; R5: IV Stability (PE IV 17.06% (3m dIV +0.07%)) | R4: Volume Burst (Vol Ratio 0.92x, BidQty 195 vs AskQty 1105) ;; R6: Greeks & Theta (/Delta/ 0.53, Daily Theta Bleed 40.9% (Max 30%)) |
| `12:48:20` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹93.60 | ₹154.05 | **`+64.6%`** | **MISSED WINNER (+64.6% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23294.0 vs VWAP 23316.8 (Basis -7.5)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,993,855 vs PE dOI -4,790,825, PE: LONG_UNWINDING, PCR 0.92) ;; R5: IV Stability (PE IV 16.90% (3m dIV -0.16%)) | R2: Option > VWAP (PE LTP 93.60 vs VWAP 87.33 (3m dLTP -2.05)) ;; R4: Volume Burst (Vol Ratio 0.69x, BidQty 1885 vs AskQty 1430) ;; R6: Greeks & Theta (/Delta/ 0.52, Daily Theta Bleed 41.5% (Max 30%)) |
| `12:51:21` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹91.90 | ₹154.05 | **`+67.6%`** | **MISSED WINNER (+67.6% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23294.5 vs VWAP 23316.2 (Basis -7.0)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,505,185 vs PE dOI -1,427,335, PE: LONG_UNWINDING, PCR 0.89) ;; R5: IV Stability (PE IV 16.91% (3m dIV +0.01%)) | R2: Option > VWAP (PE LTP 91.90 vs VWAP 87.38 (3m dLTP -1.70)) ;; R4: Volume Burst (Vol Ratio 0.59x, BidQty 4355 vs AskQty 2015) ;; R6: Greeks & Theta (/Delta/ 0.52, Daily Theta Bleed 42.4% (Max 30%)) |
| `12:54:22` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹99.70 | ₹154.05 | **`+54.5%`** | **MISSED WINNER (+54.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23284.9 vs VWAP 23315.3 (Basis -8.3)) ;; R2: Option > VWAP (PE LTP 99.70 vs VWAP 87.59 (3m dLTP +7.80)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,732,050 vs PE dOI +48,425, PE: LONG_BUILDUP, PCR 0.92) ;; R5: IV Stability (PE IV 17.06% (3m dIV +0.15%)) | R4: Volume Burst (Vol Ratio 0.86x, BidQty 3380 vs AskQty 3315) ;; R6: Greeks & Theta (/Delta/ 0.54, Daily Theta Bleed 39.3% (Max 30%)) |
| `12:57:23` | **NIFTY03NOV2623300PE** | PE | **5/6** | ₹100.70 | ₹154.05 | **`+53.0%`** | **MISSED WINNER (+53.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23286.9 vs VWAP 23314.5 (Basis -12.4)) ;; R2: Option > VWAP (PE LTP 100.70 vs VWAP 88.13 (3m dLTP +1.00)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,070,530 vs PE dOI -10,732,800, PE: SHORT_COVERING, PCR 0.81) ;; R4: Volume Burst (Vol Ratio 2.19x, BidQty 910 vs AskQty 325) ;; R5: IV Stability (PE IV 17.08% (3m dIV +0.02%)) | R6: Greeks & Theta (/Delta/ 0.54, Daily Theta Bleed 38.9% (Max 30%)) |
| `13:00:24` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹107.05 | ₹154.05 | **`+43.9%`** | **MISSED WINNER (+43.9% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23281.7 vs VWAP 23313.7 (Basis -18.1)) ;; R2: Option > VWAP (PE LTP 107.05 vs VWAP 88.47 (3m dLTP +6.35)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +7,256,600 vs PE dOI -9,831,185, PE: SHORT_COVERING, PCR 0.80) ;; R5: IV Stability (PE IV 17.16% (3m dIV +0.08%)) | R4: Volume Burst (Vol Ratio 0.94x, BidQty 65 vs AskQty 585) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 36.6% (Max 30%)) |
| `13:02:47` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹108.55 | ₹154.05 | **`+41.9%`** | **MISSED WINNER (+41.9% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23275.7 vs VWAP 23312.7 (Basis -14.6)) ;; R2: Option > VWAP (PE LTP 108.55 vs VWAP 88.71 (3m dLTP +7.85)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,240,650 vs PE dOI -7,796,815, PE: SHORT_COVERING, PCR 0.79) ;; R5: IV Stability (PE IV 17.19% (3m dIV +0.11%)) | R4: Volume Burst (Vol Ratio 0.64x, BidQty 910 vs AskQty 2145) ;; R6: Greeks & Theta (/Delta/ 0.57, Daily Theta Bleed 36.1% (Max 30%)) |
| `13:05:48` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹91.20 | ₹121.05 | **`+32.7%`** | **MISSED WINNER (+32.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23262.2 vs VWAP 23311.4 (Basis -16.0)) ;; R2: Option > VWAP (PE LTP 91.20 vs VWAP 69.29 (3m dLTP +7.75)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +4,733,040 vs PE dOI -11,326,640, PE: SHORT_COVERING, PCR 0.95) ;; R5: IV Stability (PE IV 17.54% (3m dIV +0.10%)) | R4: Volume Burst (Vol Ratio 2.14x, BidQty 325 vs AskQty 2145) ;; R6: Greeks & Theta (/Delta/ 0.50, Daily Theta Bleed 44.5% (Max 30%)) |
| `13:08:48` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹99.35 | ₹121.05 | **`+21.8%`** | **MISSED WINNER (+21.8% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23251.0 vs VWAP 23309.9 (Basis -19.9)) ;; R2: Option > VWAP (PE LTP 99.35 vs VWAP 70.26 (3m dLTP +8.15)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,000,330 vs PE dOI -16,870,425, PE: SHORT_COVERING, PCR 0.89) ;; R5: IV Stability (PE IV 17.62% (3m dIV +0.08%)) | R4: Volume Burst (Vol Ratio 2.00x, BidQty 585 vs AskQty 1950) ;; R6: Greeks & Theta (/Delta/ 0.53, Daily Theta Bleed 40.9% (Max 30%)) |
| `13:10:41` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹111.15 | ₹121.05 | **`+8.9%`** | **TRACKING (Max +8.9%)** | R1: Spot/Basis Trend (Spot 23237.5 vs VWAP 23308.2 (Basis -24.6)) ;; R2: Option > VWAP (PE LTP 111.15 vs VWAP 71.98 (3m dLTP +19.95)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,187,025 vs PE dOI -18,401,890, PE: SHORT_COVERING, PCR 0.78) ;; R5: IV Stability (PE IV 17.99% (3m dIV +0.45%)) | R4: Volume Burst (Vol Ratio 2.66x, BidQty 650 vs AskQty 1495) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 37.0% (Max 30%)) |
| `13:13:41` | **NIFTY03NOV2623200PE** | PE | **4/6** | ₹94.05 | ₹94.25 | **`+0.2%`** | **FILTER SAVED LOSS (-75.2%)** | R1: Spot/Basis Trend (Spot 23223.9 vs VWAP 23306.2 (Basis -27.4)) ;; R2: Option > VWAP (PE LTP 94.05 vs VWAP 56.30 (3m dLTP +7.85)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +9,767,940 vs PE dOI -19,241,885, PE: LONG_BUILDUP, PCR 0.89) ;; R5: IV Stability (PE IV 18.23% (3m dIV +0.00%)) | R4: Volume Burst (Vol Ratio 2.55x, BidQty 260 vs AskQty 1170) ;; R6: Greeks & Theta (/Delta/ 0.50, Daily Theta Bleed 44.8% (Max 30%)) |
| `13:16:42` | **NIFTY03NOV2623200PE** | PE | **3/6** | ₹93.30 | ₹94.25 | **`+1.0%`** | **FILTER SAVED LOSS (-75.0%)** | R1: Spot/Basis Trend (Spot 23224.7 vs VWAP 23304.4 (Basis -28.5)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +12,769,835 vs PE dOI -20,094,360, PE: SHORT_BUILDUP, PCR 0.84) ;; R5: IV Stability (PE IV 18.10% (3m dIV -0.13%)) | R2: Option > VWAP (PE LTP 93.30 vs VWAP 57.64 (3m dLTP -0.75)) ;; R4: Volume Burst (Vol Ratio 2.29x, BidQty 260 vs AskQty 455) ;; R6: Greeks & Theta (/Delta/ 0.50, Daily Theta Bleed 44.9% (Max 30%)) |
| `13:17:01` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹120.90 | ₹120.90 | **`+0.0%`** | **FILTER SAVED LOSS (-70.6%)** | R1: Spot/Basis Trend (Spot 23225.6 vs VWAP 23302.7 (Basis -29.6)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +13,161,135 vs PE dOI -21,339,240, PE: LONG_UNWINDING, PCR 0.68) ;; R5: IV Stability (PE IV 17.93% (3m dIV -0.20%)) | R2: Option > VWAP (PE LTP 120.90 vs VWAP 74.57 (3m dLTP -0.15)) ;; R4: Volume Burst (Vol Ratio 0.06x, BidQty 195 vs AskQty 130) ;; R6: Greeks & Theta (/Delta/ 0.59, Daily Theta Bleed 33.4% (Max 30%)) |
| `13:24:58` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹100.30 | ₹120.75 | **`+20.4%`** | **MISSED WINNER (+20.4% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23255.9 vs VWAP 23299.6 (Basis -28.2)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +13,222,495 vs PE dOI -1,246,960, PE: SHORT_BUILDUP, PCR 0.67) ;; R5: IV Stability (PE IV 17.53% (3m dIV +0.01%)) | R2: Option > VWAP (PE LTP 100.30 vs VWAP 75.62 (3m dLTP -2.15)) ;; R4: Volume Burst (Vol Ratio 0.76x, BidQty 2275 vs AskQty 1235) ;; R6: Greeks & Theta (/Delta/ 0.54, Daily Theta Bleed 40.5% (Max 30%)) |
| `13:27:58` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹109.40 | ₹120.75 | **`+10.4%`** | **TRACKING (Max +10.4%)** | R1: Spot/Basis Trend (Spot 23241.8 vs VWAP 23298.4 (Basis -30.4)) ;; R2: Option > VWAP (PE LTP 109.40 vs VWAP 76.12 (3m dLTP +9.10)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,146,775 vs PE dOI +2,135,575, PE: LONG_BUILDUP, PCR 0.69) ;; R5: IV Stability (PE IV 17.51% (3m dIV -0.02%)) | R4: Volume Burst (Vol Ratio 1.01x, BidQty 910 vs AskQty 390) ;; R6: Greeks & Theta (/Delta/ 0.57, Daily Theta Bleed 36.7% (Max 30%)) |
| `13:28:32` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹104.35 | ₹120.75 | **`+15.7%`** | **MISSED WINNER (+15.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23245.0 vs VWAP 23297.3 (Basis -25.9)) ;; R2: Option > VWAP (PE LTP 104.35 vs VWAP 76.17 (3m dLTP +4.05)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +8,441,420 vs PE dOI +2,466,620, PE: LONG_BUILDUP, PCR 0.69) ;; R5: IV Stability (PE IV 17.43% (3m dIV -0.10%)) | R4: Volume Burst (Vol Ratio 0.11x, BidQty 260 vs AskQty 1300) ;; R6: Greeks & Theta (/Delta/ 0.55, Daily Theta Bleed 38.5% (Max 30%)) |
| `13:31:32` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹106.80 | ₹120.75 | **`+13.1%`** | **MISSED WINNER (+13.1% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23238.5 vs VWAP 23296.2 (Basis -23.4)) ;; R2: Option > VWAP (PE LTP 106.80 vs VWAP 76.58 (3m dLTP +2.45)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +4,693,520 vs PE dOI +4,847,960, PE: SHORT_COVERING, PCR 0.70) ;; R5: IV Stability (PE IV 17.50% (3m dIV +0.07%)) | R4: Volume Burst (Vol Ratio 0.93x, BidQty 65 vs AskQty 2080) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 37.7% (Max 30%)) |
| `13:34:34` | **NIFTY03NOV2623250CE** | CE | **3/6** | ₹67.15 | ₹140.65 | **`+109.5%`** | **MISSED WINNER (+109.5% -> Tune Missing Rule!)** | R3: Trapped Writers / PCR / dOI (15m PE dOI +4,841,785 vs CE dOI +3,017,950, CE: SHORT_BUILDUP, PCR 0.68) ;; R4: Volume Burst (Vol Ratio 1.35x, BidQty 2405 vs AskQty 1300) ;; R5: IV Stability (CE IV 17.58% (3m dIV +0.08%)) | R1: Spot/Basis Trend (Spot 23227.3 vs VWAP 23294.8 (Basis -24.1)) ;; R2: Option > VWAP (CE LTP 67.15 vs VWAP 111.72 (3m dLTP -4.80)) ;; R6: Greeks & Theta (Delta 0.42, Daily Theta Bleed 59.7% (Max 30%)) |
| `13:34:34` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹113.95 | ₹120.75 | **`+6.0%`** | **FILTER SAVED LOSS (-68.8%)** | R1: Spot/Basis Trend (Spot 23227.3 vs VWAP 23294.8 (Basis -24.1)) ;; R2: Option > VWAP (PE LTP 113.95 vs VWAP 77.21 (3m dLTP +7.15)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,017,950 vs PE dOI +4,841,785, PE: SHORT_COVERING, PCR 0.68) ;; R5: IV Stability (PE IV 17.58% (3m dIV +0.08%)) | R4: Volume Burst (Vol Ratio 1.21x, BidQty 130 vs AskQty 1170) ;; R6: Greeks & Theta (/Delta/ 0.58, Daily Theta Bleed 35.2% (Max 30%)) |
| `13:34:36` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹113.90 | ₹120.75 | **`+6.0%`** | **FILTER SAVED LOSS (-68.8%)** | R1: Spot/Basis Trend (Spot 23228.5 vs VWAP 23293.6 (Basis -25.1)) ;; R2: Option > VWAP (PE LTP 113.90 vs VWAP 77.22 (3m dLTP +7.10)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,017,950 vs PE dOI +4,841,785, PE: SHORT_COVERING, PCR 0.68) ;; R5: IV Stability (PE IV 17.55% (3m dIV +0.05%)) | R4: Volume Burst (Vol Ratio 0.01x, BidQty 1235 vs AskQty 780) ;; R6: Greeks & Theta (/Delta/ 0.58, Daily Theta Bleed 35.1% (Max 30%)) |
| `13:37:36` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹113.15 | ₹120.75 | **`+6.7%`** | **FILTER SAVED LOSS (-68.6%)** | R1: Spot/Basis Trend (Spot 23228.8 vs VWAP 23292.4 (Basis -25.9)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,458,010 vs PE dOI +3,992,105, PE: LONG_UNWINDING, PCR 0.66) ;; R5: IV Stability (PE IV 17.40% (3m dIV -0.15%)) | R2: Option > VWAP (PE LTP 113.15 vs VWAP 77.73 (3m dLTP -0.75)) ;; R4: Volume Burst (Vol Ratio 1.05x, BidQty 195 vs AskQty 65) ;; R6: Greeks & Theta (/Delta/ 0.58, Daily Theta Bleed 35.1% (Max 30%)) |
| `13:38:14` | **NIFTY03NOV2623200PE** | PE | **4/6** | ₹92.85 | ₹92.85 | **`+0.0%`** | **FILTER SAVED LOSS (-74.8%)** | R1: Spot/Basis Trend (Spot 23218.2 vs VWAP 23291.0 (Basis -27.2)) ;; R2: Option > VWAP (PE LTP 92.85 vs VWAP 60.84 (3m dLTP +5.50)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +4,337,385 vs PE dOI +1,674,335, PE: SHORT_COVERING, PCR 0.81) ;; R5: IV Stability (PE IV 17.57% (3m dIV -0.08%)) | R4: Volume Burst (Vol Ratio 0.34x, BidQty 3640 vs AskQty 1885) ;; R6: Greeks & Theta (/Delta/ 0.51, Daily Theta Bleed 44.1% (Max 30%)) |
| `13:41:14` | **NIFTY03NOV2623200PE** | PE | **3/6** | ₹88.40 | ₹88.40 | **`+0.0%`** | **FILTER SAVED LOSS (-73.6%)** | R1: Spot/Basis Trend (Spot 23222.2 vs VWAP 23289.8 (Basis -23.9)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +5,227,365 vs PE dOI -308,035, PE: LONG_UNWINDING, PCR 0.80) ;; R5: IV Stability (PE IV 17.43% (3m dIV -0.14%)) | R2: Option > VWAP (PE LTP 88.40 vs VWAP 61.62 (3m dLTP -4.45)) ;; R4: Volume Burst (Vol Ratio 2.14x, BidQty 715 vs AskQty 4030) ;; R6: Greeks & Theta (/Delta/ 0.50, Daily Theta Bleed 46.0% (Max 30%)) |
| `13:44:15` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹104.60 | ₹111.40 | **`+6.5%`** | **FILTER SAVED LOSS (-66.0%)** | R1: Spot/Basis Trend (Spot 23241.6 vs VWAP 23289.0 (Basis -24.4)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,648,200 vs PE dOI -2,836,665, PE: LONG_UNWINDING, PCR 0.64) ;; R5: IV Stability (PE IV 17.29% (3m dIV -0.12%)) | R2: Option > VWAP (PE LTP 104.60 vs VWAP 78.83 (3m dLTP -11.20)) ;; R4: Volume Burst (Vol Ratio 0.80x, BidQty 325 vs AskQty 715) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 38.2% (Max 30%)) |
| `13:47:16` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹102.60 | ₹111.40 | **`+8.6%`** | **TRACKING (Max +8.6%)** | R1: Spot/Basis Trend (Spot 23243.2 vs VWAP 23288.2 (Basis -23.4)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +6,182,865 vs PE dOI -3,130,335, PE: SHORT_BUILDUP, PCR 0.64) ;; R5: IV Stability (PE IV 17.26% (3m dIV -0.03%)) | R2: Option > VWAP (PE LTP 102.60 vs VWAP 79.04 (3m dLTP -2.00)) ;; R4: Volume Burst (Vol Ratio 0.71x, BidQty 1300 vs AskQty 2925) ;; R6: Greeks & Theta (/Delta/ 0.55, Daily Theta Bleed 39.0% (Max 30%)) |
| `13:47:16` | **NIFTY03NOV2623250CE** | CE | **3/6** | ₹72.40 | ₹140.65 | **`+94.3%`** | **MISSED WINNER (+94.3% -> Tune Missing Rule!)** | R3: Trapped Writers / PCR / dOI (15m PE dOI -3,130,335 vs CE dOI +6,182,865, CE: SHORT_COVERING, PCR 0.64) ;; R4: Volume Burst (Vol Ratio 1.75x, BidQty 1235 vs AskQty 1105) ;; R5: IV Stability (CE IV 17.26% (3m dIV -0.03%)) | R1: Spot/Basis Trend (Spot 23243.2 vs VWAP 23288.2 (Basis -23.4)) ;; R2: Option > VWAP (CE LTP 72.40 vs VWAP 108.47 (3m dLTP +1.15)) ;; R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 55.3% (Max 30%)) |
| `13:49:28` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹111.40 | ₹111.40 | **`+0.0%`** | **FILTER SAVED LOSS (-68.1%)** | R1: Spot/Basis Trend (Spot 23230.5 vs VWAP 23287.2 (Basis -26.1)) ;; R2: Option > VWAP (PE LTP 111.40 vs VWAP 79.32 (3m dLTP +6.80)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +5,760,950 vs PE dOI -1,269,060, PE: LONG_BUILDUP, PCR 0.65) ;; R5: IV Stability (PE IV 17.28% (3m dIV -0.01%)) | R4: Volume Burst (Vol Ratio 0.67x, BidQty 715 vs AskQty 325) ;; R6: Greeks & Theta (/Delta/ 0.58, Daily Theta Bleed 35.6% (Max 30%)) |
| `13:52:29` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹103.55 | ₹103.60 | **`+0.1%`** | **FILTER SAVED LOSS (-65.7%)** | R1: Spot/Basis Trend (Spot 23240.8 vs VWAP 23286.4 (Basis -22.9)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +2,367,755 vs PE dOI -796,250, PE: LONG_UNWINDING, PCR 0.65) ;; R5: IV Stability (PE IV 17.21% (3m dIV -0.07%)) | R2: Option > VWAP (PE LTP 103.55 vs VWAP 79.58 (3m dLTP -7.85)) ;; R4: Volume Burst (Vol Ratio 0.85x, BidQty 1690 vs AskQty 455) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 38.5% (Max 30%)) |
| `13:53:32` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹103.55 | ₹103.60 | **`+0.1%`** | **FILTER SAVED LOSS (-65.7%)** | R1: Spot/Basis Trend (Spot 23240.9 vs VWAP 23285.7 (Basis -23.4)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,559,010 vs PE dOI -514,735, PE: LONG_UNWINDING, PCR 0.64) ;; R5: IV Stability (PE IV 17.22% (3m dIV -0.06%)) | R2: Option > VWAP (PE LTP 103.55 vs VWAP 79.62 (3m dLTP -7.85)) ;; R4: Volume Burst (Vol Ratio 0.15x, BidQty 1495 vs AskQty 2795) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 38.6% (Max 30%)) |
| `13:56:32` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹103.00 | ₹103.60 | **`+0.6%`** | **FILTER SAVED LOSS (-65.5%)** | R1: Spot/Basis Trend (Spot 23236.7 vs VWAP 23284.9 (Basis -18.9)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +2,933,580 vs PE dOI +1,255,410, PE: SHORT_BUILDUP, PCR 0.65) ;; R5: IV Stability (PE IV 17.17% (3m dIV -0.05%)) | R2: Option > VWAP (PE LTP 103.00 vs VWAP 79.77 (3m dLTP -0.55)) ;; R4: Volume Burst (Vol Ratio 0.51x, BidQty 650 vs AskQty 650) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 38.7% (Max 30%)) |
| `13:56:50` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹103.60 | ₹103.60 | **`+0.0%`** | **FILTER SAVED LOSS (-65.7%)** | R1: Spot/Basis Trend (Spot 23238.5 vs VWAP 23284.2 (Basis -21.2)) ;; R2: Option > VWAP (PE LTP 103.60 vs VWAP 79.78 (3m dLTP +0.05)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +2,819,180 vs PE dOI +1,237,600, PE: LONG_BUILDUP, PCR 0.65) ;; R5: IV Stability (PE IV 17.23% (3m dIV +0.01%)) | R4: Volume Burst (Vol Ratio 0.04x, BidQty 2860 vs AskQty 1755) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 38.6% (Max 30%)) |
| `13:59:50` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹96.90 | ₹102.30 | **`+5.6%`** | **FILTER SAVED LOSS (-63.3%)** | R1: Spot/Basis Trend (Spot 23249.1 vs VWAP 23283.6 (Basis -20.2)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,297,775 vs PE dOI +1,461,005, PE: LONG_UNWINDING, PCR 0.63) ;; R5: IV Stability (PE IV 17.18% (3m dIV -0.05%)) | R2: Option > VWAP (PE LTP 96.90 vs VWAP 79.95 (3m dLTP -6.70)) ;; R4: Volume Burst (Vol Ratio 0.84x, BidQty 4095 vs AskQty 910) ;; R6: Greeks & Theta (/Delta/ 0.54, Daily Theta Bleed 41.5% (Max 30%)) |
| `14:02:51` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹102.30 | ₹102.30 | **`+0.0%`** | **FILTER SAVED LOSS (-65.2%)** | R1: Spot/Basis Trend (Spot 23244.3 vs VWAP 23283.0 (Basis -25.4)) ;; R2: Option > VWAP (PE LTP 102.30 vs VWAP 80.12 (3m dLTP +5.40)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,274,180 vs PE dOI +392,275, PE: LONG_BUILDUP, PCR 0.63) ;; R5: IV Stability (PE IV 17.14% (3m dIV -0.04%)) | R4: Volume Burst (Vol Ratio 0.62x, BidQty 715 vs AskQty 1755) ;; R6: Greeks & Theta (/Delta/ 0.56, Daily Theta Bleed 39.0% (Max 30%)) |
| `14:05:11` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹94.00 | ₹96.75 | **`+2.9%`** | **FILTER SAVED LOSS (-62.2%)** | R1: Spot/Basis Trend (Spot 23253.5 vs VWAP 23282.6 (Basis -20.4)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +4,142,710 vs PE dOI +465,725, PE: SHORT_BUILDUP, PCR 0.62) ;; R5: IV Stability (PE IV 17.09% (3m dIV -0.09%)) | R2: Option > VWAP (PE LTP 94.00 vs VWAP 80.19 (3m dLTP -2.90)) ;; R4: Volume Burst (Vol Ratio 0.45x, BidQty 1495 vs AskQty 2080) ;; R6: Greeks & Theta (/Delta/ 0.53, Daily Theta Bleed 42.7% (Max 30%)) |
| `14:08:12` | **NIFTY03NOV2623250PE** | PE | **4/6** | ₹96.75 | ₹96.75 | **`+0.0%`** | **FILTER SAVED LOSS (-63.3%)** | R1: Spot/Basis Trend (Spot 23250.6 vs VWAP 23282.1 (Basis -24.2)) ;; R2: Option > VWAP (PE LTP 96.75 vs VWAP 80.37 (3m dLTP +2.75)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +2,453,295 vs PE dOI +615,680, PE: SHORT_COVERING, PCR 0.62) ;; R5: IV Stability (PE IV 16.92% (3m dIV -0.17%)) | R4: Volume Burst (Vol Ratio 0.98x, BidQty 2080 vs AskQty 1170) ;; R6: Greeks & Theta (/Delta/ 0.54, Daily Theta Bleed 41.0% (Max 30%)) |
| `14:11:13` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹89.45 | ₹89.45 | **`+0.0%`** | **FILTER SAVED LOSS (-60.3%)** | R1: Spot/Basis Trend (Spot 23257.0 vs VWAP 23281.7 (Basis -18.7)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +3,340,025 vs PE dOI +94,055, PE: SHORT_BUILDUP, PCR 0.63) ;; R5: IV Stability (PE IV 16.74% (3m dIV -0.18%)) | R2: Option > VWAP (PE LTP 89.45 vs VWAP 80.46 (3m dLTP -7.30)) ;; R4: Volume Burst (Vol Ratio 0.85x, BidQty 1820 vs AskQty 65) ;; R6: Greeks & Theta (/Delta/ 0.52, Daily Theta Bleed 44.1% (Max 30%)) |
| `14:14:14` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹85.35 | ₹85.35 | **`+0.0%`** | **FILTER SAVED LOSS (-58.4%)** | R1: Spot/Basis Trend (Spot 23264.9 vs VWAP 23281.5 (Basis -19.9)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +2,648,165 vs PE dOI +1,503,190, PE: SHORT_BUILDUP, PCR 0.62) ;; R5: IV Stability (PE IV 16.63% (3m dIV -0.11%)) | R2: Option > VWAP (PE LTP 85.35 vs VWAP 80.50 (3m dLTP -4.10)) ;; R4: Volume Burst (Vol Ratio 0.70x, BidQty 1950 vs AskQty 3380) ;; R6: Greeks & Theta (/Delta/ 0.51, Daily Theta Bleed 46.1% (Max 30%)) |
| `14:17:15` | **NIFTY03NOV2623250PE** | PE | **3/6** | ₹76.70 | ₹77.45 | **`+1.0%`** | **FILTER SAVED LOSS (-53.6%)** | R1: Spot/Basis Trend (Spot 23274.4 vs VWAP 23281.4 (Basis -13.6)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -1,186,900 vs PE dOI -98,020, PE: SHORT_BUILDUP, PCR 0.62) ;; R5: IV Stability (PE IV 16.47% (3m dIV -0.16%)) | R2: Option > VWAP (PE LTP 76.70 vs VWAP 80.44 (3m dLTP -8.65)) ;; R4: Volume Burst (Vol Ratio 1.38x, BidQty 2665 vs AskQty 5850) ;; R6: Greeks & Theta (/Delta/ 0.48, Daily Theta Bleed 50.8% (Max 30%)) |
| `14:20:16` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹100.30 | ₹104.05 | **`+3.7%`** | **FILTER SAVED LOSS (-47.6%)** | R1: Spot/Basis Trend (Spot 23279.5 vs VWAP 23281.3 (Basis -15.8)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -4,472,325 vs PE dOI +1,674,400, PE: SHORT_BUILDUP, PCR 0.51) ;; R5: IV Stability (PE IV 16.25% (3m dIV -0.20%)) | R2: Option > VWAP (PE LTP 100.30 vs VWAP 97.40 (3m dLTP -2.75)) ;; R4: Volume Burst (Vol Ratio 0.72x, BidQty 2080 vs AskQty 520) ;; R6: Greeks & Theta (/Delta/ 0.57, Daily Theta Bleed 37.8% (Max 30%)) |
| `14:23:17` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹100.45 | ₹104.05 | **`+3.6%`** | **FILTER SAVED LOSS (-47.6%)** | R2: Option > VWAP (PE LTP 100.45 vs VWAP 97.42 (3m dLTP +0.15)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -3,573,700 vs PE dOI +2,825,420, PE: LONG_BUILDUP, PCR 0.51) ;; R5: IV Stability (PE IV 16.21% (3m dIV -0.04%)) | R1: Spot/Basis Trend (Spot 23283.3 vs VWAP 23281.4 (Basis -20.3)) ;; R4: Volume Burst (Vol Ratio 0.68x, BidQty 715 vs AskQty 2145) ;; R6: Greeks & Theta (/Delta/ 0.57, Daily Theta Bleed 37.7% (Max 30%)) |
| `14:26:18` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹101.85 | ₹104.05 | **`+2.2%`** | **FILTER SAVED LOSS (-48.4%)** | R2: Option > VWAP (PE LTP 101.85 vs VWAP 97.45 (3m dLTP +1.40)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -5,656,950 vs PE dOI +4,243,720, PE: LONG_BUILDUP, PCR 0.53) ;; R5: IV Stability (PE IV 16.22% (3m dIV +0.01%)) | R1: Spot/Basis Trend (Spot 23284.3 vs VWAP 23281.4 (Basis -23.9)) ;; R4: Volume Burst (Vol Ratio 0.62x, BidQty 2470 vs AskQty 520) ;; R6: Greeks & Theta (/Delta/ 0.58, Daily Theta Bleed 37.1% (Max 30%)) |
| `14:29:18` | **NIFTY03NOV2623300PE** | PE | **4/6** | ₹104.05 | ₹104.05 | **`+0.0%`** | **FILTER SAVED LOSS (-49.5%)** | R1: Spot/Basis Trend (Spot 23280.7 vs VWAP 23281.4 (Basis -25.2)) ;; R2: Option > VWAP (PE LTP 104.05 vs VWAP 97.49 (3m dLTP +2.20)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI -8,634,210 vs PE dOI +5,364,255, PE: LONG_BUILDUP, PCR 0.55) ;; R5: IV Stability (PE IV 16.09% (3m dIV -0.13%)) | R4: Volume Burst (Vol Ratio 0.58x, BidQty 325 vs AskQty 2015) ;; R6: Greeks & Theta (/Delta/ 0.59, Daily Theta Bleed 35.9% (Max 30%)) |
| `14:32:19` | **NIFTY03NOV2623300CE** | CE | **3/6** | ₹64.85 | ₹106.90 | **`+64.8%`** | **MISSED WINNER (+64.8% -> Tune Missing Rule!)** | R3: Trapped Writers / PCR / dOI (15m PE dOI +5,151,315 vs CE dOI -6,583,785, CE: SHORT_COVERING, PCR 0.55) ;; R4: Volume Burst (Vol Ratio 1.51x, BidQty 4160 vs AskQty 3055) ;; R5: IV Stability (CE IV 15.94% (3m dIV -0.15%)) | R1: Spot/Basis Trend (Spot 23284.9 vs VWAP 23281.4 (Basis -15.1)) ;; R2: Option > VWAP (CE LTP 64.85 vs VWAP 81.87 (3m dLTP +5.30)) ;; R6: Greeks & Theta (Delta 0.44, Daily Theta Bleed 57.9% (Max 30%)) |
| `14:38:26` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹74.00 | ₹83.00 | **`+12.2%`** | **MISSED WINNER (+12.2% -> Tune Missing Rule!)** | R3: Trapped Writers / PCR / dOI (15m CE dOI -15,527,460 vs PE dOI +4,740,580, PE: SHORT_BUILDUP, PCR 0.63) ;; R4: Volume Burst (Vol Ratio 1.55x, BidQty 2210 vs AskQty 1170) ;; R5: IV Stability (PE IV 16.00% (3m dIV +0.22%)) | R1: Spot/Basis Trend (Spot 23320.0 vs VWAP 23282.2 (Basis -9.3)) ;; R2: Option > VWAP (PE LTP 74.00 vs VWAP 97.04 (3m dLTP -14.15)) ;; R6: Greeks & Theta (/Delta/ 0.48, Daily Theta Bleed 51.6% (Max 30%)) |
| `14:38:26` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹84.70 | ₹106.90 | **`+26.2%`** | **MISSED WINNER (+26.2% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23320.0 vs VWAP 23282.2 (Basis -9.3)) ;; R2: Option > VWAP (CE LTP 84.70 vs VWAP 81.81 (3m dLTP +15.75)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +4,740,580 vs CE dOI -15,527,460, CE: SHORT_COVERING, PCR 0.63) ;; R5: IV Stability (CE IV 16.00% (3m dIV +0.22%)) | R4: Volume Burst (Vol Ratio 3.22x, BidQty 910 vs AskQty 3900) ;; R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 45.1% (Max 30%)) |
| `14:41:26` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹76.00 | ₹106.90 | **`+40.7%`** | **MISSED WINNER (+40.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23303.0 vs VWAP 23282.5 (Basis -7.7)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +5,398,900 vs CE dOI -15,087,020, CE: LONG_UNWINDING, PCR 0.65) ;; R4: Volume Burst (Vol Ratio 1.37x, BidQty 2275 vs AskQty 455) ;; R5: IV Stability (CE IV 15.84% (3m dIV -0.16%)) | R2: Option > VWAP (CE LTP 76.00 vs VWAP 81.73 (3m dLTP -8.70)) ;; R6: Greeks & Theta (Delta 0.49, Daily Theta Bleed 49.8% (Max 30%)) |
| `14:44:27` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹86.35 | ₹106.90 | **`+23.8%`** | **MISSED WINNER (+23.8% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23318.4 vs VWAP 23282.9 (Basis -6.5)) ;; R2: Option > VWAP (CE LTP 86.35 vs VWAP 81.81 (3m dLTP +10.35)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +3,365,505 vs CE dOI -15,194,725, CE: SHORT_COVERING, PCR 0.66) ;; R5: IV Stability (CE IV 16.24% (3m dIV +0.40%)) | R4: Volume Burst (Vol Ratio 1.70x, BidQty 1755 vs AskQty 3315) ;; R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 45.0% (Max 30%)) |
| `14:44:55` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹87.60 | ₹106.90 | **`+22.0%`** | **MISSED WINNER (+22.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23323.0 vs VWAP 23283.4 (Basis -8.2)) ;; R2: Option > VWAP (CE LTP 87.60 vs VWAP 81.82 (3m dLTP +11.60)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +3,231,865 vs CE dOI -18,237,700, CE: SHORT_COVERING, PCR 0.68) ;; R5: IV Stability (CE IV 16.19% (3m dIV +0.35%)) | R4: Volume Burst (Vol Ratio 0.27x, BidQty 2275 vs AskQty 390) ;; R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 44.1% (Max 30%)) |
| `14:47:56` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹84.15 | ₹106.90 | **`+27.0%`** | **MISSED WINNER (+27.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23322.6 vs VWAP 23283.9 (Basis -13.3)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +5,514,925 vs CE dOI -21,110,700, CE: LONG_UNWINDING, PCR 0.71) ;; R4: Volume Burst (Vol Ratio 1.40x, BidQty 3185 vs AskQty 2860) ;; R5: IV Stability (CE IV 16.09% (3m dIV -0.10%)) | R2: Option > VWAP (CE LTP 84.15 vs VWAP 81.85 (3m dLTP -3.45)) ;; R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 45.8% (Max 30%)) |
| `14:50:56` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹85.05 | ₹106.90 | **`+25.7%`** | **MISSED WINNER (+25.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23316.8 vs VWAP 23284.3 (Basis -7.0)) ;; R2: Option > VWAP (CE LTP 85.05 vs VWAP 81.89 (3m dLTP +0.90)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +4,690,855 vs CE dOI -22,510,995, CE: SHORT_COVERING, PCR 0.75) ;; R5: IV Stability (CE IV 16.22% (3m dIV +0.13%)) | R4: Volume Burst (Vol Ratio 1.21x, BidQty 1365 vs AskQty 5785) ;; R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 45.7% (Max 30%)) |
| `14:51:16` | **NIFTY03NOV2623300CE** | CE | **3/6** | ₹82.35 | ₹106.90 | **`+29.8%`** | **MISSED WINNER (+29.8% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23315.7 vs VWAP 23284.7 (Basis -10.1)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +4,690,855 vs CE dOI -22,510,995, CE: LONG_UNWINDING, PCR 0.75) ;; R5: IV Stability (CE IV 16.12% (3m dIV +0.03%)) | R2: Option > VWAP (CE LTP 82.35 vs VWAP 81.89 (3m dLTP -1.80)) ;; R4: Volume Burst (Vol Ratio 0.22x, BidQty 2015 vs AskQty 325) ;; R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 47.0% (Max 30%)) |
| `14:54:16` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹84.85 | ₹106.90 | **`+26.0%`** | **MISSED WINNER (+26.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23319.7 vs VWAP 23285.1 (Basis -12.0)) ;; R2: Option > VWAP (CE LTP 84.85 vs VWAP 81.92 (3m dLTP +2.50)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +3,277,755 vs CE dOI -13,018,135, CE: SHORT_COVERING, PCR 0.75) ;; R5: IV Stability (CE IV 16.44% (3m dIV +0.32%)) | R4: Volume Burst (Vol Ratio 0.96x, BidQty 1560 vs AskQty 975) ;; R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 46.5% (Max 30%)) |
| `14:57:17` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹86.10 | ₹106.90 | **`+24.2%`** | **MISSED WINNER (+24.2% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23324.5 vs VWAP 23285.5 (Basis -12.5)) ;; R2: Option > VWAP (CE LTP 86.10 vs VWAP 81.94 (3m dLTP +1.25)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +580,710 vs CE dOI -13,591,370, CE: SHORT_COVERING, PCR 0.76) ;; R5: IV Stability (CE IV 16.25% (3m dIV -0.19%)) | R4: Volume Burst (Vol Ratio 0.63x, BidQty 2405 vs AskQty 5070) ;; R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 45.3% (Max 30%)) |
| `15:00:18` | **NIFTY03NOV2623300CE** | CE | **3/6** | ₹80.35 | ₹106.90 | **`+33.0%`** | **MISSED WINNER (+33.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23316.3 vs VWAP 23285.9 (Basis -14.1)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +1,440,595 vs CE dOI -8,808,800, CE: LONG_UNWINDING, PCR 0.76) ;; R5: IV Stability (CE IV 16.12% (3m dIV -0.13%)) | R2: Option > VWAP (CE LTP 80.35 vs VWAP 81.93 (3m dLTP -5.75)) ;; R4: Volume Burst (Vol Ratio 0.77x, BidQty 1365 vs AskQty 2925) ;; R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 48.3% (Max 30%)) |
| `15:03:19` | **NIFTY03NOV2623300PE** | PE | **3/6** | ₹82.10 | ₹83.00 | **`+1.1%`** | **FILTER SAVED LOSS (-35.9%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI -7,175,415 vs PE dOI +190,060, PE: LONG_BUILDUP, PCR 0.78) ;; R4: Volume Burst (Vol Ratio 1.66x, BidQty 650 vs AskQty 845) ;; R5: IV Stability (PE IV 16.08% (3m dIV -0.04%)) | R1: Spot/Basis Trend (Spot 23310.8 vs VWAP 23286.2 (Basis -17.1)) ;; R2: Option > VWAP (PE LTP 82.10 vs VWAP 95.56 (3m dLTP +3.95)) ;; R6: Greeks & Theta (/Delta/ 0.51, Daily Theta Bleed 47.1% (Max 30%)) |
| `15:09:21` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹82.10 | ₹106.90 | **`+30.2%`** | **MISSED WINNER (+30.2% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23313.8 vs VWAP 23286.7 (Basis -6.9)) ;; R2: Option > VWAP (CE LTP 82.10 vs VWAP 81.84 (3m dLTP +6.45)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -3,359,655 vs CE dOI -4,604,665, CE: SHORT_COVERING, PCR 0.76) ;; R5: IV Stability (CE IV 16.05% (3m dIV -0.12%)) | R4: Volume Burst (Vol Ratio 0.80x, BidQty 1105 vs AskQty 650) ;; R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 47.2% (Max 30%)) |
| `15:10:55` | **NIFTY03NOV2623300CE** | CE | **4/6** | ₹86.40 | ₹106.90 | **`+23.7%`** | **MISSED WINNER (+23.7% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23321.5 vs VWAP 23287.1 (Basis -7.3)) ;; R2: Option > VWAP (CE LTP 86.40 vs VWAP 81.86 (3m dLTP +10.75)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -4,757,285 vs CE dOI -3,582,475, CE: SHORT_COVERING, PCR 0.75) ;; R5: IV Stability (CE IV 16.15% (3m dIV -0.02%)) | R4: Volume Burst (Vol Ratio 0.63x, BidQty 2015 vs AskQty 260) ;; R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 45.0% (Max 30%)) |
| `15:22:57` | **NIFTY03NOV2623350CE** | CE | **4/6** | ₹62.45 | ₹77.55 | **`+24.2%`** | **MISSED WINNER (+24.2% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23331.1 vs VWAP 23288.9 (Basis -7.8)) ;; R2: Option > VWAP (CE LTP 62.45 vs VWAP 61.48 (3m dLTP +3.50)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -6,311,955 vs CE dOI -11,550,305, CE: SHORT_COVERING, PCR 0.62) ;; R5: IV Stability (CE IV 15.36% (3m dIV -0.21%)) | R4: Volume Burst (Vol Ratio 1.15x, BidQty 1495 vs AskQty 65) ;; R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 59.2% (Max 30%)) |
| `15:25:58` | **NIFTY03NOV2623350CE** | CE | **4/6** | ₹63.95 | ₹77.55 | **`+21.3%`** | **MISSED WINNER (+21.3% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23331.1 vs VWAP 23289.3 (Basis -4.2)) ;; R2: Option > VWAP (CE LTP 63.95 vs VWAP 61.49 (3m dLTP +1.50)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -6,394,895 vs CE dOI -13,523,250, CE: SHORT_COVERING, PCR 0.63) ;; R5: IV Stability (CE IV 15.35% (3m dIV -0.01%)) | R4: Volume Burst (Vol Ratio 0.54x, BidQty 1625 vs AskQty 195) ;; R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 57.9% (Max 30%)) |
| `15:28:50` | **NIFTY03NOV2623350CE** | CE | **4/6** | ₹64.20 | ₹77.55 | **`+20.8%`** | **MISSED WINNER (+20.8% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23331.1 vs VWAP 23289.8 (Basis -1.8)) ;; R2: Option > VWAP (CE LTP 64.20 vs VWAP 61.50 (3m dLTP +0.25)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -6,438,575 vs CE dOI -13,784,940, CE: SHORT_COVERING, PCR 0.63) ;; R5: IV Stability (CE IV 15.20% (3m dIV -0.15%)) | R4: Volume Burst (Vol Ratio 0.54x, BidQty 65 vs AskQty 520) ;; R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 57.3% (Max 30%)) |
| `15:31:50` | **NIFTY03NOV2623450CE** | CE | **4/6** | ₹34.85 | ₹37.40 | **`+7.3%`** | **TRACKING (Max +7.3%)** | R2: Option > VWAP (CE LTP 34.85 vs VWAP 29.54 (3m dLTP +4.25)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -2,764,385 vs CE dOI -18,012,410, CE: SHORT_COVERING, PCR 0.46) ;; R4: Volume Burst (Vol Ratio 2.07x, BidQty 1170 vs AskQty 65) ;; R5: IV Stability (CE IV 15.32% (3m dIV -0.28%)) | R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23291.3 (Basis -91.3)) ;; R6: Greeks & Theta (Delta 0.30, Daily Theta Bleed 92.9% (Max 30%)) |
| `15:34:51` | **NIFTY03NOV2623450PE** | PE | **3/6** | ₹128.85 | ₹139.50 | **`+8.3%`** | **TRACKING (Max +8.3%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI -18,104,515 vs PE dOI -2,806,895, PE: SHORT_BUILDUP, PCR 0.46) ;; R5: IV Stability (PE IV 15.24% (3m dIV -0.08%)) ;; R6: Greeks & Theta (/Delta/ 0.69, Daily Theta Bleed 25.7% (Max 30%)) | R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23292.8 (Basis -82.2)) ;; R2: Option > VWAP (PE LTP 128.85 vs VWAP 185.21 (3m dLTP -7.10)) ;; R4: Volume Burst (Vol Ratio 0.86x, BidQty 455 vs AskQty 390) |
| `15:34:51` | **NIFTY03NOV2623450CE** | CE | **3/6** | ₹37.40 | ₹37.40 | **`+0.0%`** | **TRACKING (Max +0.0%)** | R2: Option > VWAP (CE LTP 37.40 vs VWAP 29.61 (3m dLTP +2.55)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -2,806,895 vs CE dOI -18,104,515, CE: SHORT_COVERING, PCR 0.46) ;; R5: IV Stability (CE IV 15.24% (3m dIV -0.08%)) | R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23292.8 (Basis -82.2)) ;; R4: Volume Burst (Vol Ratio 1.08x, BidQty 1040 vs AskQty 65) ;; R6: Greeks & Theta (Delta 0.31, Daily Theta Bleed 88.4% (Max 30%)) |
| `15:37:52` | **NIFTY03NOV2623450PE** | PE | **3/6** | ₹134.40 | ₹139.50 | **`+3.8%`** | **TRACKING (Max +3.8%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI -18,001,295 vs PE dOI -3,004,040, PE: LONG_BUILDUP, PCR 0.47) ;; R5: IV Stability (PE IV 15.53% (3m dIV +0.29%)) ;; R6: Greeks & Theta (/Delta/ 0.70, Daily Theta Bleed 24.8% (Max 30%)) | R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23294.3 (Basis -88.6)) ;; R2: Option > VWAP (PE LTP 134.40 vs VWAP 184.85 (3m dLTP +5.55)) ;; R4: Volume Burst (Vol Ratio 0.83x, BidQty 130 vs AskQty 260) |

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
