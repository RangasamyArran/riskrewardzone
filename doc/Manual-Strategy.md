# Manual Intraday Option Buying Strategy (Price Action + Option Chain Playbook)

> **Purpose:** Step-by-step manual execution guide for trading the **LearnOT 6-Point "Trapped Seller Gamma Blast" Strategy** using standard charting platforms (**TradingView / Zerodha Kite**) + an **NSE / Broker Option Chain**.

---

## 🖥️ 1. Screen Setup (Before 9:15 AM IST)

You only need **two charts side-by-side** and **one Option Chain tab**:

1. **Left Chart (Underlying Trend):**
   - **Instrument:** **Nifty 50 Futures** (or Nifty 50 Index Spot)
   - **Timeframes:** **15-Minute** (Big-picture structure) & **3-Minute** (Execution timing)
   - **Indicators:** **Session VWAP** + Horizontal lines for **Previous Day High (`PDH`)**, **Previous Day Low (`PDL`)**, and **Previous Day Close (`PDC`)**.

2. **Right Chart (Option Contract Execution):**
   - **Instrument:** Current **At-The-Money (`ATM`) Call (`CE`)** and **ATM Put (`PE`)**
   - **Timeframe:** **3-Minute**
   - **Indicators:**
     - **Session VWAP** (Most important filter for option buying!)
     - **Volume** with a **20-period Moving Average (`SMA 20`)** enabled on Volume.

3. **Option Chain Tab:**
   - **NSE / Zerodha / Sensibull / LearnOT Option Chain** filtered to **5 strikes above and 5 strikes below ATM** for the nearest weekly expiry.

---

## 🌅 2. Pre-Market Routine (8:45 AM – 9:15 AM IST)

Before the opening bell, check your **3-Stage Pre-Market Cues**:
1. **Global Cues:** GIFT Nifty Gap (`+` or `-` pts), US Market Close, Asian Markets (Nikkei / Hang Seng).
2. **Macro & Institutional Cues:** Previous day FII/DII net flow, Brent Crude, DXY & USD/INR.
3. **Domestic Cues (9:00–9:08 AM Pre-Open):**
   - **9:08 AM Equilibrium Spot Price** & **Advance-Decline Ratio**.
   - **Previous Day Closing PCR:**
     - $\text{PCR} \ge 1.45$: Market is **Overbought** &rarr; Watch for profit-booking / bearish reversal if a gap-up fails.
     - $\text{PCR} \le 0.65$: Market is **Oversold** &rarr; Watch for a short-covering bounce.
     - $\text{PCR } 0.90–1.30$: Healthy trend-following zone.
   - **India VIX Regime:**
     - **`13.5 – 16.5` (Goldilocks Zone):** Ideal for intraday option buying (`+25% / +45%` targets).
     - **`< 11.5` (Low Volatility):** Slow premiums; book profits early (`+15%–20%`).
     - **`> 19.5` (Extreme High IV):** High IV-Crush risk; reduce size by 50% or treat as a **No-Trade Day**.

---

## 🎯 3. The 5-Step Manual Intraday Routine (Every 3–15 Minutes After 9:30 AM)

### Step 1: Draw the Battlefield at 9:30 AM (`OI Walls` + `Opening Range`)
Let the first 15-minute candle (`9:15–9:30 AM`) complete without trading so opening volatility settles. At **9:30 AM**:
1. Mark the **First 15-Minute High & Low** on your Nifty chart.
2. Check the **Total Open Interest (`OI`)** column on the Option Chain:
   - Strike with **Highest Call (`CE`) OI** = **Intraday Resistance Wall (Ceiling)** (e.g., `23,500 CE`).
   - Strike with **Highest Put (`PE`) OI** = **Intraday Support Wall (Floor)** (e.g., `23,200 PE`).

---

### Step 2: Check Underlying Direction (`Rule 1` — Spot vs. Session VWAP)
Look at your **Left Chart (Nifty 3m/15m)**:
- **Bullish Regime:** Nifty is trading **ABOVE Session VWAP** (and Futures are not trading at a deep widening discount) &rarr; **Look ONLY to buy ATM Call (`CE`). Ignore Puts.**
- **Bearish Regime:** Nifty is trading **BELOW Session VWAP** &rarr; **Look ONLY to buy ATM Put (`PE`). Ignore Calls.**

> *Real Example (`2026-11-02` at `11:37 AM`):* Nifty broke below Session VWAP (`23,320`) &rarr; Mental focus shifted 100% to **ATM Put (`23,300 PE`)**.

---

### Step 3: Check Who Is Trapped on the Option Chain (`Rule 3` — 15m Change in OI)
Before buying an option, verify that **institutional option writers are fueling your move** by checking **Change in OI (`Chng in OI`)** over the last **15 minutes** around ATM:

- **For Buying ATM Call (`CE`):**
  1. **Trapped Call Writers (Short Covering — Best Signal):** Nifty crosses above a strike (e.g., `23,300`), and on `23,300 CE`, **Option Price is rising (`+dLTP`) while `CE OI` is falling (`-dOI`)**. Call writers are panic-buying back their shorts!
  2. **Put Writing Floor:** At the same time, **`23,300 PE` Change in OI is rising strongly (`+dOI`)** and faster than `CE OI` ($\Delta\text{OI}_{\text{PE}} > \Delta\text{OI}_{\text{CE}}$), or Near-ATM $\text{PCR} \ge 1.15$.

- **For Buying ATM Put (`PE`):**
  1. **Trapped Put Writers (Short Covering — Best Signal):** Nifty breaks below a strike (e.g., `23,300`), and on `23,300 PE`, **Option Price is rising (`+dLTP`) while `PE OI` is falling (`-dOI`)**. Put writers are running for cover!
  2. **Call Writing Ceiling:** At the same time, **`23,300 CE` Change in OI is rising strongly (`+dOI`)** and faster than `PE OI` ($\Delta\text{OI}_{\text{CE}} > \Delta\text{OI}_{\text{PE}}$), or Near-ATM $\text{PCR} \le 0.85$.

> *Real Example (`2026-11-02` at `11:46 AM`):* `23,300 CE` added `+3.66M` OI (heavy Call writing resistance) while `23,300 PE` shed `-187K` OI (`SHORT_COVERING`), fueling a **`+70.0%` surge in `23300PE` (`₹90.60 -> ₹154.05`)**!

---

### Step 4: Time the Exact Entry on the 3-Minute Option Chart (`Rule 2 + Rule 4`)
**Never buy an option just because Nifty Spot is moving.** Switch to your **Right Chart (3-Minute ATM Option Chart)** and verify two things:

1. **`Rule 2` — Option Price Above Option VWAP:**
   - The **3-minute Option candle MUST be trading ABOVE the Option's own Session VWAP** and closing green (`3m dLTP > 0`).
   - *Why this rule saves your capital:* On `2026-11-02` between `1:52 PM` and `2:20 PM`, traders who bought `23250PE` and `23300PE` lost `-55%` to `-65%`. Simply checking that **PE Price was BELOW PE VWAP** kept you out of all 31 losing setups!
2. **`Rule 4` — 3-Minute Volume Burst & Order Flow:**
   - The **3-minute Volume bar** on the Option chart spikes **above its 20-period Moving Average (`>= 1.2x` average volume)**, and Total `Bid Qty` on the market depth is healthy relative to `Ask Qty`.

---

### Step 5: Verify IV & Strike (`Rule 5 + Rule 6`), Then Manage with the 15-Minute Rule
1. **`Rule 5` — Anti-IV-Crush Check:**
   - Glance at **ATM IV** (or **India VIX**). Make sure IV is **flat or rising** (not dropping sharply by $> 0.30\%$ in 3 minutes).
2. **`Rule 6` — Strike Selection (`Delta` & `Theta`):**
   - Always buy the **ATM** or **1-strike ITM** contract where **$|\Delta|$ is between `0.45` and `0.70`** (typically priced around `₹80–₹150` on Nifty).
   - **Never** buy cheap far-OTM lottery tickets (`Delta < 0.30`) where Theta decay destroys the premium.
3. **Post-Entry Trade Management (Non-Negotiable):**
   - **Hard Stop-Loss:** Place your Stop-Loss **`15% to 20%` below Entry LTP** (e.g., Entry `₹90` &rarr; Stop-Loss `₹75`).
   - **⏱️ The 15-Minute Anti-Theta Time Stop:** Count **5 candles on the 3-minute chart (`15 minutes`)** after entry. If the option has **not gained at least `+5%`** within 15 minutes, **exit at market price immediately**. Real gamma blasts expand immediately; if it stalls for 15 minutes, Theta will bleed you.
   - **Profit Booking:**
     - **Target 1 (`+25%`):** Book 50% quantity and trail Stop-Loss on the remaining 50% to your Entry cost.
     - **Target 2 (`+45%+`):** Trail with the 3-minute Option VWAP or 9-EMA until the momentum wave ends.

---

## 📋 4. Desk Reference Cheat-Sheet (Print or Keep Next to Screen)

| # | Checklist Rule | Bullish Entry (`BUY ATM CE`) | Bearish Entry (`BUY ATM PE`) |
| :-: | :--- | :--- | :--- |
| **`R1`** | **Nifty Trend & Basis** | Nifty **$\ge$ Session VWAP** | Nifty **$\le$ Session VWAP** |
| **`R2`** | **3m Option VWAP** | **CE LTP $>$ CE VWAP** & Green 3m candle | **PE LTP $>$ PE VWAP** & Green 3m candle |
| **`R3`** | **15m OI & Trapped Writers** | `15m PE dOI > CE dOI` **OR** `CE Short Covering` **OR** `PCR >= 1.15` | `15m CE dOI > PE dOI` **OR** `PE Short Covering` **OR** `PCR <= 0.85` |
| **`R4`** | **3m Volume Burst** | 3m Option Volume **$\ge 1.2\times$ Avg Volume** & strong Bid Qty | 3m Option Volume **$\ge 1.2\times$ Avg Volume** & strong Bid Qty |
| **`R5`** | **IV Stability** | CE IV **Stable or Rising** (`3m dIV >= -0.30%`) | PE IV **Stable or Rising** (`3m dIV >= -0.30%`) |
| **`R6`** | **Strike & Greeks** | **ATM Strike** (`Delta 0.45–0.70`) | **ATM Strike** (`|Delta| 0.45–0.70`) |
| **🚫** | **Theta Trap Avoidance** | **NO TRADE** if ATM Straddle is decaying $> 2.5\%$ while both CE & PE OI rise in flat PCR (`0.88–1.12`) | **NO TRADE** if ATM Straddle is decaying $> 2.5\%$ while both CE & PE OI rise in flat PCR (`0.88–1.12`) |
| **⏱️** | **Exit Rules** | **SL:** `-15%` to `-20%` \| **Time Stop:** Exit if $< +5\%$ after `15 mins` \| **Targets:** `+25%` & `+45%` | **SL:** `-15%` to `-20%` \| **Time Stop:** Exit if $< +5\%$ after `15 mins` \| **Targets:** `+25%` & `+45%` |
