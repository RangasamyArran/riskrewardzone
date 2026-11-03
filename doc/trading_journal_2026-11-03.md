# LearnOT Daily Trading & Fine-Tuning Journal (2026-11-03 — NIFTY)

> **How to Use This Journal:**
> 1. **🌅 Section 0 (Pre-Market Sentiment Signal vs. Post-Market Deviation):** Synthesizes GIFT/SGX Nifty, Global Sentiment, Prev Day PCR (Reversal vs Trend), and India VIX (`13.5–16.5` Goldilocks vs High-IV No-Trade) into a Pre-Market Signal and audits how your trades matched or deviated.
> 2. **✅ What Was Good Today (`Score >= 3/6`):** Which conditions aligned in your favor (with exact numbers).
> 3. **❌ Why It Did Not Meet 6/6:** Which specific rule(s) failed (e.g., PCR, 15m dOI, Volume Burst, or Option VWAP) with exact live numbers.
> 4. **📈 What Happened Next (Outcome Tracking):** How high the option premium moved *after* that snapshot (`Max LTP After` & `Max Gain %`) so you can decide whether to fine-tune a strict condition or keep it.

---

## 0. Pre-Market Sentiment Signal vs. Post-Market Deviation Review

| Metric | Morning Pre-Market Sentiment (`06:30 AM – 09:08 AM`) | Actual Intraday Outcome (`09:15 AM – 03:30 PM`) | System Signal & Deviation Verdict |
| :--- | :--- | :--- | :--- |
| **🌍 Global Indicators (`6:30–8:00 AM`)** | GIFT Gap: `+22.0` pts / US Close: `MILD_BULLISH` / Asia (Nikkei/HangSeng): `POSITIVE_MOMENTUM` | Open `23440.8` / High `24495.0` / Low `23440.8` / Close `24495.0` | **`BULLISH CONFLUENCE OPEN (+22 pts / 7/8 Bullish Cues)`** |
| **📊 Macro & Institutional Triggers** | FII/DII: `FII_NET_LONG` / Brent Crude: `COOLING_BULLISH` / DXY & USDINR: `COOLING_INR_STRONG` | Intraday Range: `1054.2` pts (Walls: `23200 PE` – `23500 CE`) | Bull Cues: `7/8` / Bear Cues: `0/8` |
| **🇮🇳 Domestic (`9:00–9:08 AM`) & VIX/PCR** | 09:08 Adv/Dec: `MODERATE_ADVANCES` / India VIX: **`14.4`** / Prev PCR: **`1.18`** | `✅ Bull Trigger (23453) CROSSED (High 24495.0) ;; 🛡️ Bear Trigger (23421) held (Low 23440.8) ;; Broke PDH (23466)` | `🟢 GOLDILOCKS OPTION BUYING DAY (VIX 14.4 in 13.5–16.5 Sweet Spot: Steady IV, no crush, ideal for +25% / +45% Gamma Blast targets!)` |
| **🧠 System Pre-Market Signal** | **`🚀 BULLISH CONTINUATION SIGNAL (7/8 Pre-Market Cues Bullish + VIX 14.4 -> Buy ATM CE above Bull Trigger)`** | PDH `23466` / PDL `23376` / PDC `23419` | 09:08 Equilibrium: `23440.8` |
| **🎯 Planned Bias & Triggers** | Bias: **`BULLISH_ABOVE_TRIGGER`** (Bull `>23453` / Bear `<23421`) | Trades Taken: **`0/2`** (PnL: `₹+0.00`) | **`PLAN ALIGNED (100% Discipline)`** |
| **📓 Execution vs. Pre-Plan** | *Morning Note:* VIX 14.4 (Goldilocks 14-16 zone) + Prev PCR 1.18 Bullish -> Buy ATM CE above 23453. | *Post-Market Note:* Add reflection in Web UI Portal | ✔️ Trade Count Discipline (0/2 max) |

---

## 1. Fine-Tuning Rule Blocker Summary (Which Condition Held Back Good Trades Today?)

| Condition That Failed | Times Failed (at >=3/6) | Missed Winners (>= +12% Move) | Avg Max Gain After | Fine-Tuning Action |
| :--- | :---: | :---: | :---: | :--- |
| **R6: Greeks & Theta** | 18 | **9** | `+46.9%` | TUNING CANDIDATE: Blocked 9 winning move(s) (Avg Max +46.9%). Consider relaxing R6: Greeks & Theta threshold. |
| **R4: Volume Burst** | 7 | **4** | `+55.5%` | TUNING CANDIDATE: Blocked 4 winning move(s) (Avg Max +55.5%). Consider relaxing R4: Volume Burst threshold. |
| **R2: Option > VWAP** | 11 | **2** | `+16.1%` | TUNING CANDIDATE: Blocked 2 winning move(s) (Avg Max +16.1%). Consider relaxing R2: Option > VWAP threshold. |
| **R1: Spot/Basis Trend** | 6 | **2** | `+56.9%` | TUNING CANDIDATE: Blocked 2 winning move(s) (Avg Max +56.9%). Consider relaxing R1: Spot/Basis Trend threshold. |
| **R5: IV Stability** | 2 | **1** | `+41.3%` | TUNING CANDIDATE: Blocked 1 winning move(s) (Avg Max +41.3%). Consider relaxing R5: IV Stability threshold. |
| **R3: Trapped Writers / PCR / dOI** | 3 | **0** | `+2.0%` | GOOD GUARDRAIL: Blocked 3 setup(s) (Avg Max +2.0%). |

---

## 2. Setup-by-Setup Breakdown: What Was Good vs. Why It Missed 6/6

### Entry #1 — `06:21:05` | **NIFTY03NOV2623450PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23440.8` (VWAP `23440.8`) | PCR `0.47` | 3m dOI `+0` (`NEUTRAL`) | 15m PE dOI `+0` vs CE dOI `+0` | Vol Ratio `1.00x` | IV `25.0%` | Delta `-0.71` | Theta Bleed `60.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23440.8 (Basis -96.1))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +0 vs PE dOI +0, PE: NEUTRAL, PCR 0.47)**
  - ✔️ **R5: IV Stability (PE IV 25.02% (3m dIV +0.00%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 139.50 vs VWAP 139.50 (3m dLTP +0.00))**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 195 vs AskQty 845)**
  - ❌ **R6: Greeks & Theta (|Delta| 0.71, Daily Theta Bleed 60.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹139.50` &rarr; Latest `₹0.40` | **Max LTP After:** `₹139.50` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-99.7%)**

### Entry #2 — `09:17:40` | **NIFTY03NOV2623550CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23568.8` (VWAP `23535.1`) | PCR `0.51` | 3m dOI `+4,268,485` (`LONG_BUILDUP`) | 15m PE dOI `+23,942,620` vs CE dOI `+10,114,585` | Vol Ratio `1.00x` | IV `27.1%` | Delta `0.49` | Theta Bleed `197.9%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R2: Option > VWAP (CE LTP 66.30 vs VWAP 22.72 (3m dLTP +22.05))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +23,942,620 vs CE dOI +10,114,585, CE: LONG_BUILDUP, PCR 0.51)**
  - ✔️ **R5: IV Stability (CE IV 27.14% (3m dIV +1.68%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23568.8 vs VWAP 23535.1 (Basis -21.9))**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 1365 vs AskQty 780)**
  - ❌ **R6: Greeks & Theta (Delta 0.49, Daily Theta Bleed 197.9% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹66.30` &rarr; Latest `₹177.10` | **Max LTP After:** `₹183.15` (**`+176.2%`**) &rarr; **MISSED WINNER (+176.2% -> Tune Missing Rule!)**

### Entry #3 — `09:23:40` | **NIFTY03NOV2623600PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23588.8` (VWAP `23555.6`) | PCR `0.69` | 3m dOI `+4,246,905` (`SHORT_BUILDUP`) | 15m PE dOI `+56,385,225` vs CE dOI `+33,739,550` | Vol Ratio `2.00x` | IV `26.2%` | Delta `-0.57` | Theta Bleed `155.3%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +33,739,550 vs PE dOI +56,385,225, PE: SHORT_BUILDUP, PCR 0.69)**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.00x, BidQty 715 vs AskQty 325)**
  - ✔️ **R5: IV Stability (PE IV 26.25% (3m dIV -0.22%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23588.8 vs VWAP 23555.6 (Basis -18.5))**
  - ❌ **R2: Option > VWAP (PE LTP 81.15 vs VWAP 125.19 (3m dLTP -4.60))**
  - ❌ **R6: Greeks & Theta (|Delta| 0.57, Daily Theta Bleed 155.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹81.15` &rarr; Latest `₹1.50` | **Max LTP After:** `₹81.15` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-98.2%)**

### Entry #4 — `09:23:40` | **NIFTY03NOV2623600CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23588.8` (VWAP `23555.6`) | PCR `0.69` | 3m dOI `+2,549,170` (`LONG_BUILDUP`) | 15m PE dOI `+56,385,225` vs CE dOI `+33,739,550` | Vol Ratio `1.29x` | IV `26.2%` | Delta `0.43` | Theta Bleed `245.2%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R2: Option > VWAP (CE LTP 51.40 vs VWAP 21.17 (3m dLTP +1.95))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +56,385,225 vs CE dOI +33,739,550, CE: LONG_BUILDUP, PCR 0.69)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.29x, BidQty 4875 vs AskQty 4095)**
  - ✔️ **R5: IV Stability (CE IV 26.25% (3m dIV -0.22%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23588.8 vs VWAP 23555.6 (Basis -18.5))**
  - ❌ **R6: Greeks & Theta (Delta 0.43, Daily Theta Bleed 245.2% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹51.40` &rarr; Latest `₹127.70` | **Max LTP After:** `₹136.20` (**`+165.0%`**) &rarr; **MISSED WINNER (+165.0% -> Tune Missing Rule!)**

### Entry #5 — `09:35:42` | **NIFTY03NOV2623600CE** (CE) — **5/6** [🟡 NEAR-MISS (5/6)]
* **Option Chain Context:** Spot `23617.1` (VWAP `23565.9`) | PCR `0.96` | 3m dOI `+1,043,965` (`LONG_BUILDUP`) | 15m PE dOI `+53,664,520` vs CE dOI `+13,706,875` | Vol Ratio `3.69x` | IV `27.2%` | Delta `0.53` | Theta Bleed `188.3%`
* **✅ What Was Good Today (5 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23617.1 vs VWAP 23565.9 (Basis -7.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 71.70 vs VWAP 31.73 (3m dLTP +20.30))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +53,664,520 vs CE dOI +13,706,875, CE: LONG_BUILDUP, PCR 0.96)**
  - ✔️ **R4: Volume Burst (Vol Ratio 3.69x, BidQty 2860 vs AskQty 1560)**
  - ✔️ **R5: IV Stability (CE IV 27.22% (3m dIV +0.97%))**
* **❌ Why It Did Not Meet 6/6 (1 Condition(s) Missing):**
  - ❌ **R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 188.3% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹71.70` &rarr; Latest `₹127.70` | **Max LTP After:** `₹136.20` (**`+90.0%`**) &rarr; **MISSED WINNER (+90.0% -> Tune Missing Rule!)**

### Entry #6 — `10:09:01` | **NIFTY03NOV2623600CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23618.2` (VWAP `23573.3`) | PCR `1.04` | 3m dOI `+2,430,740` (`SHORT_BUILDUP`) | 15m PE dOI `+31,325,775` vs CE dOI `+19,042,335` | Vol Ratio `3.76x` | IV `27.4%` | Delta `0.51` | Theta Bleed `216.4%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23618.2 vs VWAP 23573.3 (Basis -13.7))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +31,325,775 vs CE dOI +19,042,335, CE: SHORT_BUILDUP, PCR 1.04)**
  - ✔️ **R5: IV Stability (CE IV 27.38% (3m dIV +0.16%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 66.00 vs VWAP 40.18 (3m dLTP -5.70))**
  - ❌ **R4: Volume Burst (Vol Ratio 3.76x, BidQty 390 vs AskQty 1170)**
  - ❌ **R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 216.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹66.00` &rarr; Latest `₹127.70` | **Max LTP After:** `₹136.20` (**`+106.4%`**) &rarr; **MISSED WINNER (+106.4% -> Tune Missing Rule!)**

### Entry #7 — `10:25:48` | **NIFTY03NOV2623650CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23645.5` (VWAP `23582.3`) | PCR `0.97` | 3m dOI `+1,638,455` (`LONG_BUILDUP`) | 15m PE dOI `+10,095,800` vs CE dOI `+3,074,630` | Vol Ratio `1.48x` | IV `26.0%` | Delta `0.46` | Theta Bleed `271.7%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23645.5 vs VWAP 23582.3 (Basis -12.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 51.00 vs VWAP 32.83 (3m dLTP +8.25))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +10,095,800 vs CE dOI +3,074,630, CE: LONG_BUILDUP, PCR 0.97)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.48x, BidQty 6370 vs AskQty 780)**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R5: IV Stability (CE IV 25.96% (3m dIV -1.04%))**
  - ❌ **R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 271.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹51.00` &rarr; Latest `₹81.10` | **Max LTP After:** `₹93.10` (**`+82.5%`**) &rarr; **MISSED WINNER (+82.5% -> Tune Missing Rule!)**

### Entry #8 — `11:43:44` | **NIFTY03NOV2623650CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23666.7` (VWAP `23591.7`) | PCR `1.17` | 3m dOI `-1,794,325` (`SHORT_COVERING`) | 15m PE dOI `+29,520,335` vs CE dOI `-3,065,660` | Vol Ratio `6.78x` | IV `26.4%` | Delta `0.52` | Theta Bleed `304.0%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23666.7 vs VWAP 23591.7 (Basis -12.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 54.15 vs VWAP 41.45 (3m dLTP +3.15))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +29,520,335 vs CE dOI -3,065,660, CE: SHORT_COVERING, PCR 1.17)**
  - ✔️ **R5: IV Stability (CE IV 26.44% (3m dIV +0.48%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 6.78x, BidQty 585 vs AskQty 1820)**
  - ❌ **R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 304.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹54.15` &rarr; Latest `₹81.10` | **Max LTP After:** `₹93.10` (**`+71.9%`**) &rarr; **MISSED WINNER (+71.9% -> Tune Missing Rule!)**

### Entry #9 — `11:59:27` | **NIFTY03NOV2623700CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23689.6` (VWAP `23601.5`) | PCR `1.25` | 3m dOI `-1,927,770` (`SHORT_COVERING`) | 15m PE dOI `+13,963,755` vs CE dOI `-14,272,960` | Vol Ratio `1.41x` | IV `26.6%` | Delta `0.45` | Theta Bleed `401.4%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23689.6 vs VWAP 23601.5 (Basis -6.1))**
  - ✔️ **R2: Option > VWAP (CE LTP 42.50 vs VWAP 26.79 (3m dLTP +10.95))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +13,963,755 vs CE dOI -14,272,960, CE: SHORT_COVERING, PCR 1.25)**
  - ✔️ **R5: IV Stability (CE IV 26.60% (3m dIV +0.56%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R4: Volume Burst (Vol Ratio 1.41x, BidQty 3835 vs AskQty 5980)**
  - ❌ **R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 401.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹42.50` &rarr; Latest `₹41.70` | **Max LTP After:** `₹57.00` (**`+34.1%`**) &rarr; **MISSED WINNER (+34.1% -> Tune Missing Rule!)**

### Entry #10 — `12:30:33` | **NIFTY03NOV2623650PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23673.5` (VWAP `23608.0`) | PCR `1.19` | 3m dOI `-1,469,780` (`SHORT_COVERING`) | 15m PE dOI `-11,691,615` vs CE dOI `+10,075,325` | Vol Ratio `3.17x` | IV `28.4%` | Delta `-0.46` | Theta Bleed `456.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +10,075,325 vs PE dOI -11,691,615, PE: SHORT_COVERING, PCR 1.19)**
  - ✔️ **R4: Volume Burst (Vol Ratio 3.17x, BidQty 4680 vs AskQty 2015)**
  - ✔️ **R5: IV Stability (PE IV 28.39% (3m dIV +1.12%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23673.5 vs VWAP 23608.0 (Basis -10.4))**
  - ❌ **R2: Option > VWAP (PE LTP 43.25 vs VWAP 54.80 (3m dLTP +6.75))**
  - ❌ **R6: Greeks & Theta (|Delta| 0.46, Daily Theta Bleed 456.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹43.25` &rarr; Latest `₹4.45` | **Max LTP After:** `₹43.25` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-89.7%)**

### Entry #11 — `12:30:33` | **NIFTY03NOV2623650CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23673.5` (VWAP `23608.0`) | PCR `1.19` | 3m dOI `+3,730,740` (`SHORT_BUILDUP`) | 15m PE dOI `-11,691,615` vs CE dOI `+10,075,325` | Vol Ratio `1.57x` | IV `28.4%` | Delta `0.54` | Theta Bleed `350.8%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23673.5 vs VWAP 23608.0 (Basis -10.4))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -11,691,615 vs CE dOI +10,075,325, CE: SHORT_BUILDUP, PCR 1.19)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.57x, BidQty 4355 vs AskQty 195)**
  - ✔️ **R5: IV Stability (CE IV 28.39% (3m dIV +1.18%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 56.30 vs VWAP 45.47 (3m dLTP -13.60))**
  - ❌ **R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 350.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹56.30` &rarr; Latest `₹81.10` | **Max LTP After:** `₹93.10` (**`+65.4%`**) &rarr; **MISSED WINNER (+65.4% -> Tune Missing Rule!)**

### Entry #12 — `13:02:11` | **NIFTY03NOV2623700CE** (CE) — **5/6** [🟡 NEAR-MISS (5/6)]
* **Option Chain Context:** Spot `23692.8` (VWAP `23615.1`) | PCR `1.19` | 3m dOI `+213,590` (`LONG_BUILDUP`) | 15m PE dOI `+15,796,625` vs CE dOI `-417,235` | Vol Ratio `1.73x` | IV `28.0%` | Delta `0.46` | Theta Bleed `551.4%`
* **✅ What Was Good Today (5 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23692.8 vs VWAP 23615.1 (Basis -4.0))**
  - ✔️ **R2: Option > VWAP (CE LTP 39.05 vs VWAP 29.30 (3m dLTP +6.05))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +15,796,625 vs CE dOI -417,235, CE: LONG_BUILDUP, PCR 1.19)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.73x, BidQty 3055 vs AskQty 195)**
  - ✔️ **R5: IV Stability (CE IV 28.03% (3m dIV -0.21%))**
* **❌ Why It Did Not Meet 6/6 (1 Condition(s) Missing):**
  - ❌ **R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 551.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹39.05` &rarr; Latest `₹41.70` | **Max LTP After:** `₹57.00` (**`+46.0%`**) &rarr; **MISSED WINNER (+46.0% -> Tune Missing Rule!)**

### Entry #13 — `13:34:34` | **NIFTY03NOV2623750CE** (CE) — **5/6** [🟡 NEAR-MISS (5/6)]
* **Option Chain Context:** Spot `23730.8` (VWAP `23624.0`) | PCR `1.10` | 3m dOI `+2,929,550` (`LONG_BUILDUP`) | 15m PE dOI `+17,197,960` vs CE dOI `-3,985,800` | Vol Ratio `2.81x` | IV `28.6%` | Delta `0.42` | Theta Bleed `798.7%`
* **✅ What Was Good Today (5 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23730.8 vs VWAP 23624.0 (Basis -1.4))**
  - ✔️ **R2: Option > VWAP (CE LTP 30.70 vs VWAP 20.17 (3m dLTP +11.10))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +17,197,960 vs CE dOI -3,985,800, CE: LONG_BUILDUP, PCR 1.10)**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.81x, BidQty 8450 vs AskQty 11505)**
  - ✔️ **R5: IV Stability (CE IV 28.60% (3m dIV +1.17%))**
* **❌ Why It Did Not Meet 6/6 (1 Condition(s) Missing):**
  - ❌ **R6: Greeks & Theta (Delta 0.42, Daily Theta Bleed 798.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹30.70` &rarr; Latest `₹15.60` | **Max LTP After:** `₹30.70` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-49.2%)**

### Entry #14 — `14:08:53` | **NIFTY03NOV2623700PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23708.5` (VWAP `23630.0`) | PCR `1.23` | 3m dOI `+4,091,945` (`LONG_BUILDUP`) | 15m PE dOI `+3,607,240` vs CE dOI `+4,122,690` | Vol Ratio `5.05x` | IV `33.2%` | Delta `-0.46` | Theta Bleed `1005.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +4,122,690 vs PE dOI +3,607,240, PE: LONG_BUILDUP, PCR 1.23)**
  - ✔️ **R4: Volume Burst (Vol Ratio 5.05x, BidQty 3835 vs AskQty 585)**
  - ✔️ **R5: IV Stability (PE IV 33.22% (3m dIV +3.97%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23708.5 vs VWAP 23630.0 (Basis +1.9))**
  - ❌ **R2: Option > VWAP (PE LTP 34.30 vs VWAP 56.06 (3m dLTP +6.35))**
  - ❌ **R6: Greeks & Theta (|Delta| 0.46, Daily Theta Bleed 1005.0% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹34.30` &rarr; Latest `₹14.75` | **Max LTP After:** `₹34.30` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-57.0%)**

### Entry #15 — `14:08:53` | **NIFTY03NOV2623700CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23708.5` (VWAP `23630.0`) | PCR `1.23` | 3m dOI `-1,119,690` (`LONG_UNWINDING`) | 15m PE dOI `+3,607,240` vs CE dOI `+4,122,690` | Vol Ratio `1.77x` | IV `33.2%` | Delta `0.54` | Theta Bleed `780.8%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23708.5 vs VWAP 23630.0 (Basis +1.9))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI +3,607,240 vs CE dOI +4,122,690, CE: LONG_UNWINDING, PCR 1.23)**
  - ✔️ **R4: Volume Burst (Vol Ratio 1.77x, BidQty 2600 vs AskQty 2275)**
  - ✔️ **R5: IV Stability (CE IV 33.22% (3m dIV +4.27%))**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 44.15 vs VWAP 34.44 (3m dLTP -12.85))**
  - ❌ **R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 780.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹44.15` &rarr; Latest `₹41.70` | **Max LTP After:** `₹44.15` (**`+0.0%`**) &rarr; **TRACKING (Max +0.0%)**

### Entry #16 — `14:37:46` | **NIFTY03NOV2623700PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23709.2` (VWAP `23635.3`) | PCR `1.03` | 3m dOI `-9,453,730` (`LONG_UNWINDING`) | 15m PE dOI `-17,996,095` vs CE dOI `+8,897,850` | Vol Ratio `4.04x` | IV `33.6%` | Delta `-0.43` | Theta Bleed `1701.8%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m CE dOI +8,897,850 vs PE dOI -17,996,095, PE: LONG_UNWINDING, PCR 1.03)**
  - ✔️ **R4: Volume Burst (Vol Ratio 4.04x, BidQty 3315 vs AskQty 130)**
  - ✔️ **R5: IV Stability (PE IV 33.57% (3m dIV +0.35%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R1: Spot/Basis Trend (Spot 23709.2 vs VWAP 23635.3 (Basis +4.8))**
  - ❌ **R2: Option > VWAP (PE LTP 25.15 vs VWAP 48.74 (3m dLTP -9.15))**
  - ❌ **R6: Greeks & Theta (|Delta| 0.43, Daily Theta Bleed 1701.8% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹25.15` &rarr; Latest `₹14.75` | **Max LTP After:** `₹25.15` (**`+0.0%`**) &rarr; **FILTER SAVED LOSS (-41.4%)**

### Entry #17 — `14:37:46` | **NIFTY03NOV2623700CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `23709.2` (VWAP `23635.3`) | PCR `1.03` | 3m dOI `+7,748,910` (`SHORT_BUILDUP`) | 15m PE dOI `-17,996,095` vs CE dOI `+8,897,850` | Vol Ratio `2.14x` | IV `33.6%` | Delta `0.57` | Theta Bleed `1087.7%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23709.2 vs VWAP 23635.3 (Basis +4.8))**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.14x, BidQty 6825 vs AskQty 4810)**
  - ✔️ **R5: IV Stability (CE IV 33.57% (3m dIV +0.35%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 39.35 vs VWAP 35.08 (3m dLTP -4.80))**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m PE dOI -17,996,095 vs CE dOI +8,897,850, CE: SHORT_BUILDUP, PCR 1.03)**
  - ❌ **R6: Greeks & Theta (Delta 0.57, Daily Theta Bleed 1087.7% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹39.35` &rarr; Latest `₹41.70` | **Max LTP After:** `₹41.70` (**`+6.0%`**) &rarr; **TRACKING (Max +6.0%)**

### Entry #18 — `15:11:34` | **NIFTY03NOV2623700CE** (CE) — **4/6** [🔵 WATCH (4/6)]
* **Option Chain Context:** Spot `23713.0` (VWAP `23640.2`) | PCR `0.97` | 3m dOI `-2,009,670` (`SHORT_COVERING`) | 15m PE dOI `-13,895,245` vs CE dOI `-5,388,955` | Vol Ratio `2.14x` | IV `27.5%` | Delta `0.66` | Theta Bleed `785.4%`
* **✅ What Was Good Today (4 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 23713.0 vs VWAP 23640.2 (Basis +13.7))**
  - ✔️ **R2: Option > VWAP (CE LTP 41.70 vs VWAP 35.90 (3m dLTP +2.35))**
  - ✔️ **R3: Trapped Writers / PCR / dOI (15m PE dOI -13,895,245 vs CE dOI -5,388,955, CE: SHORT_COVERING, PCR 0.97)**
  - ✔️ **R4: Volume Burst (Vol Ratio 2.14x, BidQty 5070 vs AskQty 4095)**
* **❌ Why It Did Not Meet 6/6 (2 Condition(s) Missing):**
  - ❌ **R5: IV Stability (CE IV 27.52% (3m dIV -6.05%))**
  - ❌ **R6: Greeks & Theta (Delta 0.66, Daily Theta Bleed 785.4% (Max 30%))**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹41.70` &rarr; Latest `₹41.70` | **Max LTP After:** `₹41.70` (**`+0.0%`**) &rarr; **NEW ENTRY (Tracking...)**

### Entry #19 — `18:09:57` | **NIFTY07NOV2624500PE** (PE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `24495.0` (VWAP `24495.0`) | PCR `0.89` | 3m dOI `+0` (`NEUTRAL`) | 15m PE dOI `+0` vs CE dOI `+0` | Vol Ratio `1.00x` | IV `13.2%` | Delta `-0.46` | Theta Bleed `11.0%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0))**
  - ✔️ **R5: IV Stability (PE IV 13.20% (3m dIV +0.00%))**
  - ✔️ **R6: Greeks & Theta (|Delta| 0.46, Daily Theta Bleed 11.0% (Max 18%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (PE LTP 98.00 vs VWAP 98.00 (3m dLTP +0.00))**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m CE dOI +0 vs PE dOI +0, PE: NEUTRAL, PCR 0.89)**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 1625 vs AskQty 1450)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹98.00` &rarr; Latest `₹98.00` | **Max LTP After:** `₹98.00` (**`+0.0%`**) &rarr; **NEW ENTRY (Tracking...)**

### Entry #20 — `18:09:57` | **NIFTY07NOV2624500CE** (CE) — **3/6** [🔵 WATCH (3/6)]
* **Option Chain Context:** Spot `24495.0` (VWAP `24495.0`) | PCR `0.89` | 3m dOI `+0` (`NEUTRAL`) | 15m PE dOI `+0` vs CE dOI `+0` | Vol Ratio `1.00x` | IV `12.8%` | Delta `0.54` | Theta Bleed `11.1%`
* **✅ What Was Good Today (3 Conditions Met):**
  - ✔️ **R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0))**
  - ✔️ **R5: IV Stability (CE IV 12.80% (3m dIV +0.00%))**
  - ✔️ **R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 11.1% (Max 18%))**
* **❌ Why It Did Not Meet 6/6 (3 Condition(s) Missing):**
  - ❌ **R2: Option > VWAP (CE LTP 104.00 vs VWAP 104.00 (3m dLTP +0.00))**
  - ❌ **R3: Trapped Writers / PCR / dOI (15m PE dOI +0 vs CE dOI +0, CE: NEUTRAL, PCR 0.89)**
  - ❌ **R4: Volume Burst (Vol Ratio 1.00x, BidQty 1950 vs AskQty 1300)**
* **📈 Forward Outcome & Verdict:** Entry LTP `₹104.00` &rarr; Latest `₹104.00` | **Max LTP After:** `₹104.00` (**`+0.0%`**) &rarr; **NEW ENTRY (Tracking...)**

---

## 3. Quick Comparison Table (`Score >= 3/6`)

| Time | Symbol | Side | Score | Entry LTP | Max LTP After | Max Gain % | Verdict | What Was Good (Passed) | Why It Missed 6/6 (Failed) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| `06:21:05` | **NIFTY03NOV2623450PE** | PE | **3/6** | ₹139.50 | ₹139.50 | **`+0.0%`** | **FILTER SAVED LOSS (-99.7%)** | R1: Spot/Basis Trend (Spot 23440.8 vs VWAP 23440.8 (Basis -96.1)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +0 vs PE dOI +0, PE: NEUTRAL, PCR 0.47) ;; R5: IV Stability (PE IV 25.02% (3m dIV +0.00%)) | R2: Option > VWAP (PE LTP 139.50 vs VWAP 139.50 (3m dLTP +0.00)) ;; R4: Volume Burst (Vol Ratio 1.00x, BidQty 195 vs AskQty 845) ;; R6: Greeks & Theta (/Delta/ 0.71, Daily Theta Bleed 60.7% (Max 30%)) |
| `09:17:40` | **NIFTY03NOV2623550CE** | CE | **3/6** | ₹66.30 | ₹183.15 | **`+176.2%`** | **MISSED WINNER (+176.2% -> Tune Missing Rule!)** | R2: Option > VWAP (CE LTP 66.30 vs VWAP 22.72 (3m dLTP +22.05)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +23,942,620 vs CE dOI +10,114,585, CE: LONG_BUILDUP, PCR 0.51) ;; R5: IV Stability (CE IV 27.14% (3m dIV +1.68%)) | R1: Spot/Basis Trend (Spot 23568.8 vs VWAP 23535.1 (Basis -21.9)) ;; R4: Volume Burst (Vol Ratio 1.00x, BidQty 1365 vs AskQty 780) ;; R6: Greeks & Theta (Delta 0.49, Daily Theta Bleed 197.9% (Max 30%)) |
| `09:23:40` | **NIFTY03NOV2623600PE** | PE | **3/6** | ₹81.15 | ₹81.15 | **`+0.0%`** | **FILTER SAVED LOSS (-98.2%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI +33,739,550 vs PE dOI +56,385,225, PE: SHORT_BUILDUP, PCR 0.69) ;; R4: Volume Burst (Vol Ratio 2.00x, BidQty 715 vs AskQty 325) ;; R5: IV Stability (PE IV 26.25% (3m dIV -0.22%)) | R1: Spot/Basis Trend (Spot 23588.8 vs VWAP 23555.6 (Basis -18.5)) ;; R2: Option > VWAP (PE LTP 81.15 vs VWAP 125.19 (3m dLTP -4.60)) ;; R6: Greeks & Theta (/Delta/ 0.57, Daily Theta Bleed 155.3% (Max 30%)) |
| `09:23:40` | **NIFTY03NOV2623600CE** | CE | **4/6** | ₹51.40 | ₹136.20 | **`+165.0%`** | **MISSED WINNER (+165.0% -> Tune Missing Rule!)** | R2: Option > VWAP (CE LTP 51.40 vs VWAP 21.17 (3m dLTP +1.95)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +56,385,225 vs CE dOI +33,739,550, CE: LONG_BUILDUP, PCR 0.69) ;; R4: Volume Burst (Vol Ratio 1.29x, BidQty 4875 vs AskQty 4095) ;; R5: IV Stability (CE IV 26.25% (3m dIV -0.22%)) | R1: Spot/Basis Trend (Spot 23588.8 vs VWAP 23555.6 (Basis -18.5)) ;; R6: Greeks & Theta (Delta 0.43, Daily Theta Bleed 245.2% (Max 30%)) |
| `09:35:42` | **NIFTY03NOV2623600CE** | CE | **5/6** | ₹71.70 | ₹136.20 | **`+90.0%`** | **MISSED WINNER (+90.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23617.1 vs VWAP 23565.9 (Basis -7.0)) ;; R2: Option > VWAP (CE LTP 71.70 vs VWAP 31.73 (3m dLTP +20.30)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +53,664,520 vs CE dOI +13,706,875, CE: LONG_BUILDUP, PCR 0.96) ;; R4: Volume Burst (Vol Ratio 3.69x, BidQty 2860 vs AskQty 1560) ;; R5: IV Stability (CE IV 27.22% (3m dIV +0.97%)) | R6: Greeks & Theta (Delta 0.53, Daily Theta Bleed 188.3% (Max 30%)) |
| `10:09:01` | **NIFTY03NOV2623600CE** | CE | **3/6** | ₹66.00 | ₹136.20 | **`+106.4%`** | **MISSED WINNER (+106.4% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23618.2 vs VWAP 23573.3 (Basis -13.7)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +31,325,775 vs CE dOI +19,042,335, CE: SHORT_BUILDUP, PCR 1.04) ;; R5: IV Stability (CE IV 27.38% (3m dIV +0.16%)) | R2: Option > VWAP (CE LTP 66.00 vs VWAP 40.18 (3m dLTP -5.70)) ;; R4: Volume Burst (Vol Ratio 3.76x, BidQty 390 vs AskQty 1170) ;; R6: Greeks & Theta (Delta 0.51, Daily Theta Bleed 216.4% (Max 30%)) |
| `10:25:48` | **NIFTY03NOV2623650CE** | CE | **4/6** | ₹51.00 | ₹93.10 | **`+82.5%`** | **MISSED WINNER (+82.5% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23645.5 vs VWAP 23582.3 (Basis -12.0)) ;; R2: Option > VWAP (CE LTP 51.00 vs VWAP 32.83 (3m dLTP +8.25)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +10,095,800 vs CE dOI +3,074,630, CE: LONG_BUILDUP, PCR 0.97) ;; R4: Volume Burst (Vol Ratio 1.48x, BidQty 6370 vs AskQty 780) | R5: IV Stability (CE IV 25.96% (3m dIV -1.04%)) ;; R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 271.7% (Max 30%)) |
| `11:43:44` | **NIFTY03NOV2623650CE** | CE | **4/6** | ₹54.15 | ₹93.10 | **`+71.9%`** | **MISSED WINNER (+71.9% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23666.7 vs VWAP 23591.7 (Basis -12.0)) ;; R2: Option > VWAP (CE LTP 54.15 vs VWAP 41.45 (3m dLTP +3.15)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +29,520,335 vs CE dOI -3,065,660, CE: SHORT_COVERING, PCR 1.17) ;; R5: IV Stability (CE IV 26.44% (3m dIV +0.48%)) | R4: Volume Burst (Vol Ratio 6.78x, BidQty 585 vs AskQty 1820) ;; R6: Greeks & Theta (Delta 0.52, Daily Theta Bleed 304.0% (Max 30%)) |
| `11:59:27` | **NIFTY03NOV2623700CE** | CE | **4/6** | ₹42.50 | ₹57.00 | **`+34.1%`** | **MISSED WINNER (+34.1% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23689.6 vs VWAP 23601.5 (Basis -6.1)) ;; R2: Option > VWAP (CE LTP 42.50 vs VWAP 26.79 (3m dLTP +10.95)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +13,963,755 vs CE dOI -14,272,960, CE: SHORT_COVERING, PCR 1.25) ;; R5: IV Stability (CE IV 26.60% (3m dIV +0.56%)) | R4: Volume Burst (Vol Ratio 1.41x, BidQty 3835 vs AskQty 5980) ;; R6: Greeks & Theta (Delta 0.45, Daily Theta Bleed 401.4% (Max 30%)) |
| `12:30:33` | **NIFTY03NOV2623650PE** | PE | **3/6** | ₹43.25 | ₹43.25 | **`+0.0%`** | **FILTER SAVED LOSS (-89.7%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI +10,075,325 vs PE dOI -11,691,615, PE: SHORT_COVERING, PCR 1.19) ;; R4: Volume Burst (Vol Ratio 3.17x, BidQty 4680 vs AskQty 2015) ;; R5: IV Stability (PE IV 28.39% (3m dIV +1.12%)) | R1: Spot/Basis Trend (Spot 23673.5 vs VWAP 23608.0 (Basis -10.4)) ;; R2: Option > VWAP (PE LTP 43.25 vs VWAP 54.80 (3m dLTP +6.75)) ;; R6: Greeks & Theta (/Delta/ 0.46, Daily Theta Bleed 456.7% (Max 30%)) |
| `12:30:33` | **NIFTY03NOV2623650CE** | CE | **4/6** | ₹56.30 | ₹93.10 | **`+65.4%`** | **MISSED WINNER (+65.4% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23673.5 vs VWAP 23608.0 (Basis -10.4)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -11,691,615 vs CE dOI +10,075,325, CE: SHORT_BUILDUP, PCR 1.19) ;; R4: Volume Burst (Vol Ratio 1.57x, BidQty 4355 vs AskQty 195) ;; R5: IV Stability (CE IV 28.39% (3m dIV +1.18%)) | R2: Option > VWAP (CE LTP 56.30 vs VWAP 45.47 (3m dLTP -13.60)) ;; R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 350.8% (Max 30%)) |
| `13:02:11` | **NIFTY03NOV2623700CE** | CE | **5/6** | ₹39.05 | ₹57.00 | **`+46.0%`** | **MISSED WINNER (+46.0% -> Tune Missing Rule!)** | R1: Spot/Basis Trend (Spot 23692.8 vs VWAP 23615.1 (Basis -4.0)) ;; R2: Option > VWAP (CE LTP 39.05 vs VWAP 29.30 (3m dLTP +6.05)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +15,796,625 vs CE dOI -417,235, CE: LONG_BUILDUP, PCR 1.19) ;; R4: Volume Burst (Vol Ratio 1.73x, BidQty 3055 vs AskQty 195) ;; R5: IV Stability (CE IV 28.03% (3m dIV -0.21%)) | R6: Greeks & Theta (Delta 0.46, Daily Theta Bleed 551.4% (Max 30%)) |
| `13:34:34` | **NIFTY03NOV2623750CE** | CE | **5/6** | ₹30.70 | ₹30.70 | **`+0.0%`** | **FILTER SAVED LOSS (-49.2%)** | R1: Spot/Basis Trend (Spot 23730.8 vs VWAP 23624.0 (Basis -1.4)) ;; R2: Option > VWAP (CE LTP 30.70 vs VWAP 20.17 (3m dLTP +11.10)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +17,197,960 vs CE dOI -3,985,800, CE: LONG_BUILDUP, PCR 1.10) ;; R4: Volume Burst (Vol Ratio 2.81x, BidQty 8450 vs AskQty 11505) ;; R5: IV Stability (CE IV 28.60% (3m dIV +1.17%)) | R6: Greeks & Theta (Delta 0.42, Daily Theta Bleed 798.7% (Max 30%)) |
| `14:08:53` | **NIFTY03NOV2623700PE** | PE | **3/6** | ₹34.30 | ₹34.30 | **`+0.0%`** | **FILTER SAVED LOSS (-57.0%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI +4,122,690 vs PE dOI +3,607,240, PE: LONG_BUILDUP, PCR 1.23) ;; R4: Volume Burst (Vol Ratio 5.05x, BidQty 3835 vs AskQty 585) ;; R5: IV Stability (PE IV 33.22% (3m dIV +3.97%)) | R1: Spot/Basis Trend (Spot 23708.5 vs VWAP 23630.0 (Basis +1.9)) ;; R2: Option > VWAP (PE LTP 34.30 vs VWAP 56.06 (3m dLTP +6.35)) ;; R6: Greeks & Theta (/Delta/ 0.46, Daily Theta Bleed 1005.0% (Max 30%)) |
| `14:08:53` | **NIFTY03NOV2623700CE** | CE | **4/6** | ₹44.15 | ₹44.15 | **`+0.0%`** | **TRACKING (Max +0.0%)** | R1: Spot/Basis Trend (Spot 23708.5 vs VWAP 23630.0 (Basis +1.9)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +3,607,240 vs CE dOI +4,122,690, CE: LONG_UNWINDING, PCR 1.23) ;; R4: Volume Burst (Vol Ratio 1.77x, BidQty 2600 vs AskQty 2275) ;; R5: IV Stability (CE IV 33.22% (3m dIV +4.27%)) | R2: Option > VWAP (CE LTP 44.15 vs VWAP 34.44 (3m dLTP -12.85)) ;; R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 780.8% (Max 30%)) |
| `14:37:46` | **NIFTY03NOV2623700PE** | PE | **3/6** | ₹25.15 | ₹25.15 | **`+0.0%`** | **FILTER SAVED LOSS (-41.4%)** | R3: Trapped Writers / PCR / dOI (15m CE dOI +8,897,850 vs PE dOI -17,996,095, PE: LONG_UNWINDING, PCR 1.03) ;; R4: Volume Burst (Vol Ratio 4.04x, BidQty 3315 vs AskQty 130) ;; R5: IV Stability (PE IV 33.57% (3m dIV +0.35%)) | R1: Spot/Basis Trend (Spot 23709.2 vs VWAP 23635.3 (Basis +4.8)) ;; R2: Option > VWAP (PE LTP 25.15 vs VWAP 48.74 (3m dLTP -9.15)) ;; R6: Greeks & Theta (/Delta/ 0.43, Daily Theta Bleed 1701.8% (Max 30%)) |
| `14:37:46` | **NIFTY03NOV2623700CE** | CE | **3/6** | ₹39.35 | ₹41.70 | **`+6.0%`** | **TRACKING (Max +6.0%)** | R1: Spot/Basis Trend (Spot 23709.2 vs VWAP 23635.3 (Basis +4.8)) ;; R4: Volume Burst (Vol Ratio 2.14x, BidQty 6825 vs AskQty 4810) ;; R5: IV Stability (CE IV 33.57% (3m dIV +0.35%)) | R2: Option > VWAP (CE LTP 39.35 vs VWAP 35.08 (3m dLTP -4.80)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -17,996,095 vs CE dOI +8,897,850, CE: SHORT_BUILDUP, PCR 1.03) ;; R6: Greeks & Theta (Delta 0.57, Daily Theta Bleed 1087.7% (Max 30%)) |
| `15:11:34` | **NIFTY03NOV2623700CE** | CE | **4/6** | ₹41.70 | ₹41.70 | **`+0.0%`** | **NEW ENTRY (Tracking...)** | R1: Spot/Basis Trend (Spot 23713.0 vs VWAP 23640.2 (Basis +13.7)) ;; R2: Option > VWAP (CE LTP 41.70 vs VWAP 35.90 (3m dLTP +2.35)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI -13,895,245 vs CE dOI -5,388,955, CE: SHORT_COVERING, PCR 0.97) ;; R4: Volume Burst (Vol Ratio 2.14x, BidQty 5070 vs AskQty 4095) | R5: IV Stability (CE IV 27.52% (3m dIV -6.05%)) ;; R6: Greeks & Theta (Delta 0.66, Daily Theta Bleed 785.4% (Max 30%)) |
| `18:09:57` | **NIFTY07NOV2624500PE** | PE | **3/6** | ₹98.00 | ₹98.00 | **`+0.0%`** | **NEW ENTRY (Tracking...)** | R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0)) ;; R5: IV Stability (PE IV 13.20% (3m dIV +0.00%)) ;; R6: Greeks & Theta (/Delta/ 0.46, Daily Theta Bleed 11.0% (Max 18%)) | R2: Option > VWAP (PE LTP 98.00 vs VWAP 98.00 (3m dLTP +0.00)) ;; R3: Trapped Writers / PCR / dOI (15m CE dOI +0 vs PE dOI +0, PE: NEUTRAL, PCR 0.89) ;; R4: Volume Burst (Vol Ratio 1.00x, BidQty 1625 vs AskQty 1450) |
| `18:09:57` | **NIFTY07NOV2624500CE** | CE | **3/6** | ₹104.00 | ₹104.00 | **`+0.0%`** | **NEW ENTRY (Tracking...)** | R1: Spot/Basis Trend (Spot 24495.0 vs VWAP 24495.0 (Basis +7.0)) ;; R5: IV Stability (CE IV 12.80% (3m dIV +0.00%)) ;; R6: Greeks & Theta (Delta 0.54, Daily Theta Bleed 11.1% (Max 18%)) | R2: Option > VWAP (CE LTP 104.00 vs VWAP 104.00 (3m dLTP +0.00)) ;; R3: Trapped Writers / PCR / dOI (15m PE dOI +0 vs CE dOI +0, CE: NEUTRAL, PCR 0.89) ;; R4: Volume Burst (Vol Ratio 1.00x, BidQty 1950 vs AskQty 1300) |

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
