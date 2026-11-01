# Nifty & BankNifty Option Buying: Strategy Blueprint & Daily Rulebook
**Platform:** OpenAlgo (`http://127.0.0.1:5000`) + Zerodha Kite  
**Focus:** Intraday Momentum Option Buying (Defeating Theta Decay & Volatility Crush)  
**Instruments:** `NIFTY` & `BANKNIFTY` (`NSE_INDEX` / `NFO`)

---

## 1. The Core Philosophy: Defeating the Two Enemies of Option Buyers

As an Option Buyer in Nifty and BankNifty, you are fighting two mathematical headwinds every second you hold a trade:
1. **Theta ($\Theta$) — Time Decay:** Option premiums melt away every minute the index stays sideways. Near expiry, Theta accelerates exponentially.
2. **Vega ($\nu$) — Volatility (IV) Crush:** When fear spikes, Implied Volatility (IV) inflates option premiums. Once the panic pauses—even if Nifty moves in your direction—IV drops ("IV Crush") and your option premium stalls or falls.

### Your Trading Edge: "Trapped Seller Gamma Blast"
Retail traders use the Option Chain to *predict* support and resistance. Institutional prop desks and FIIs dominate **Option Selling (Writing)**. 
* **Our Edge:** We do **not** buy options in a slow, grinding market. We wait for institutional Option Writers to build a massive wall of Open Interest (OI) at a strike, and we **only buy when that wall cracks**—forcing trapped writers to cover their shorts in panic (**Short Covering**) while opposing writers pile in aggressively (**Put/Call Writing Support**).
* When trapped sellers cover, **Delta ($\Delta$) expands via Gamma ($\Gamma$)** and **IV expands**, turning Vega and Gamma into your allies and overwhelming Theta decay.

---

## 2. System Architecture on OpenAlgo (`http://127.0.0.1:5000`)

Your local OpenAlgo server connected to Zerodha provides all the endpoints required to run this strategy scientifically:

```
+-------------------------------------------------------------------------+
|                 Zerodha Kite (Live Tick & Order Routing)                |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                OpenAlgo Server (http://127.0.0.1:5000)                  |
|  - /api/v1/analyzer        -> Confirms Analyze (Simulator) vs Live Mode |
|  - /api/v1/expiry          -> Auto-discovers nearest NFO expiry         |
|  - /api/v1/optionchain     -> Strikes, LTP, OI, Volume, Bid/Ask, Greeks |
|  - /api/v1/syntheticfuture -> Fair value & Cost-of-Carry Basis          |
|  - /api/v1/optionsorder    -> Dynamic ATM / ITM1 order execution        |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|          LearnOT Option Chain Analyzer (option_chain_analyzer.py)       |
|  1. Polls Option Chain every 60s & stores snapshots in SQLite           |
|  2. Computes 5m & 15m Change in OI (dOI), Intraday dPCR, Session VWAP   |
|  3. Tracks ATM Straddle Decay vs Expansion & IV Crush Guardrails        |
|  4. Evaluates 6-Point Entry Checklist + 15-Minute Theta Time-Stop       |
+-------------------------------------------------------------------------+
```

---

## 3. The 4-Quadrant Price + OI Matrix (Strike Level)

In our analyzer, every Call (CE) and Put (PE) strike is classified over rolling **5-minute** and **15-minute** lookback windows by comparing **Price Change ($\Delta\text{Price}$)** and **OI Change ($\Delta\text{OI}$)**:

| Option Price ($\Delta\text{LTP}$) | Open Interest ($\Delta\text{OI}$) | Quadrant Classification | Who is in Control? |
| :--- | :--- | :--- | :--- |
| **LTP $\uparrow$** | **OI $\uparrow$** | **Long Buildup (LB)** | Fresh Option Buyers entering aggressively |
| **LTP $\downarrow$** | **OI $\uparrow$** | **Short Buildup (SB)** | Fresh Option Writers (Sellers) eating premium |
| **LTP $\uparrow$** | **OI $\downarrow$** | **Short Covering (SC)** | **Trapped Option Writers panicking & exiting (HIGHEST EDGE)** |
| **LTP $\downarrow$** | **OI $\downarrow$** | **Long Unwinding (LU)** | Option Buyers booking profit or hitting stop-loss |

---

## 4. Quantitative Entry Rules (100% Mechanical Checklist)

A trade signal (`BUY CE` or `BUY PE`) is valid **ONLY** when all 6 rules align simultaneously.

### Time Window Filter
* **9:15 AM – 9:45 AM (No-Trade Discovery Zone):** Do **not** place trades. Let our analyzer record the baseline OI walls, ATM Straddle premium, and Session VWAP.
* **9:45 AM – 11:30 AM (Prime Morning Momentum Window):** Highest probability for breakout + writer trapping.
* **11:30 AM – 1:15 PM (Theta Trap Zone):** Avoid fresh option buying unless a major intraday breakout occurs with $2\times$ volume.
* **1:15 PM – 2:55 PM (Afternoon Short-Covering Window):** Second prime window when trapped intraday writers square off.
* **After 3:00 PM:** No new intraday option buying entries; square off all open intraday positions by **3:15 PM**.

---

### Setup A: Bullish Momentum Entry (`BUY ATM CE` or `ITM1 CE`)

Trigger `BUY CE` when:
1. **Underlying & Synthetic Basis Filter:**
   * `Underlying LTP > Session VWAP`
   * **Synthetic Future Basis** ($\text{Synthetic Future} - \text{Spot}$) is stable or rising (not in deep backwardation/panic selling).
2. **Option Price > Option VWAP:**
   * Target Call Option (`ATM` or `ITM1` CE) `LTP > Option Session VWAP` and trading near its 15-minute high.
3. **OI Wall & Trapped Call Writers ($\Delta\text{OI}$ Edge):**
   * **Put Writer Support:** Aggregate Put OI change across `ATM ± 3` strikes over the last 15 minutes is strongly positive ($\sum \Delta\text{OI}_{\text{PE, 15m}} > 0$) with Put strikes showing **Short Buildup** ($\text{PE LTP}\downarrow, \text{PE OI}\uparrow$).
   * **Call Writer Unwinding / Panic:** Either ATM/OTM1 Call OI is unwinding ($\Delta\text{OI}_{\text{CE, 5m}} < 0$ while $\text{CE LTP}\uparrow$ = **Short Covering**) **OR** Intraday Rolling Put-Call Ratio ($\Delta\text{PCR}_{15m} = \frac{\sum \Delta\text{OI}_{\text{PE}}}{\sum \Delta\text{OI}_{\text{CE}}}$) is **$> 1.35$** (or Total Near-ATM PCR $> 1.15$ and rising).
4. **Volume & Order Flow Velocity:**
   * Current 5-minute CE Volume change is $> 1.5\times$ the rolling average 5-minute volume, **AND** `bid_qty >= 0.8 * ask_qty` (no massive wall of sellers sitting on the ask).
5. **Anti-IV-Crush Guardrail (Vega Protection):**
   * Call Implied Volatility ($\text{IV}_{\text{CE}}$) is **stable or rising** over the last 5–15 minutes ($\Delta\text{IV}_{5m} \ge -0.3\%$).
   * *Never buy a Call if IV is crashing sharply, even if Spot is ticking up slowly.*
6. **Greeks & Strike Selection Filter (Theta Protection):**
   * Select `ATM` or `ITM1` Call where **Delta ($\Delta$) is between $0.50$ and $0.65$**.
   * **Daily Theta Bleed Ratio:** $|\Theta| / \text{LTP} < 18\%$ on regular days (or $< 30\%$ on expiry day). Never buy far OTM options ($\Delta < 0.35$) where Theta eats the entire premium.

---

### Setup B: Bearish Momentum Entry (`BUY ATM PE` or `ITM1 PE`)

Trigger `BUY PE` when:
1. **Underlying & Synthetic Basis Filter:**
   * `Underlying LTP < Session VWAP`
   * Synthetic Future Basis is flat or negative/falling.
2. **Option Price > Option VWAP:**
   * Target Put Option (`ATM` or `ITM1` PE) `LTP > Option Session VWAP` and breaking above its 15-minute high.
3. **OI Wall & Trapped Put Writers ($\Delta\text{OI}$ Edge):**
   * **Call Writer Resistance:** Aggregate Call OI change across `ATM ± 3` strikes over the last 15 minutes is strongly positive ($\sum \Delta\text{OI}_{\text{CE, 15m}} > 0$) with Call strikes showing **Short Buildup** ($\text{CE LTP}\downarrow, \text{CE OI}\uparrow$).
   * **Put Writer Unwinding / Panic:** Either ATM/OTM1 Put OI is unwinding ($\Delta\text{OI}_{\text{PE, 5m}} < 0$ while $\text{PE LTP}\uparrow$ = **Short Covering**) **OR** Intraday Rolling $\Delta\text{PCR}_{15m} < 0.70$ (or Total Near-ATM PCR $< 0.85$ and falling).
4. **Volume & Order Flow Velocity:**
   * Current 5-minute PE Volume burst $> 1.5\times$ rolling average, and `bid_qty >= 0.8 * ask_qty`.
5. **Anti-IV-Crush Guardrail (Vega Protection):**
   * Put Implied Volatility ($\text{IV}_{\text{PE}}$) is **stable or rising** ($\Delta\text{IV}_{5m} \ge -0.3\%$). *(Bearish moves typically spike IV, giving Put buyers a double boost from Delta + Vega!)*
6. **Greeks & Strike Selection Filter:**
   * Select `ATM` or `ITM1` Put where **$|\Delta|$ is between $0.50$ and $0.65$**.

---

### Setup C: The "No-Trade / Theta Trap" Filter (When to Sit Out)
Our analyzer will explicitly flag **`THETA TRAP - DO NOT BUY`** when:
* **ATM Straddle Premium ($\text{ATM CE LTP} + \text{ATM PE LTP}$) is decaying** steadily while **both** ATM Call OI and ATM Put OI are rising ($\Delta\text{OI}_{\text{CE}} \uparrow$ and $\Delta\text{OI}_{\text{PE}} \uparrow$).
* Near-ATM PCR is stuck between **$0.88$ and $1.12$**.
* **Meaning:** Institutional straddle sellers are in full control. Option buyers will get chopped up by Theta and IV crush. Stay in cash!

---

## 5. Exit, Risk Management & Anti-Theta Rules

Every entry generated by the analyzer immediately computes four exit parameters:

| Rule | Parameter | Why It Protects You |
| :--- | :--- | :--- |
| **1. Initial Hard Stop-Loss** | **$-18\%$ of Entry Premium** (15% on Expiry Day) | Caps maximum loss per trade before a reversal compounds. |
| **2. The 15-Minute Time-Stop** | **Exit if PnL $< +5\%$ after 15 mins** | **Your #1 weapon against Theta.** Option buying requires *immediate* momentum. If trapped writers haven't panicked within 15 minutes, the thesis failed—exit at cost/tiny loss. |
| **3. Target 1 (Scale Out / Trail)** | **$+25\%$ of Entry Premium** (1:1.4 R:R) | Book 50% lots (or trail Stop-Loss to Entry Cost + 2% brokerage buffer). |
| **4. Target 2 (Gamma Runner)** | **$+45\%$ of Entry Premium** or $\Delta\text{OI}$ reversal | Captures the full short-covering blast; trail SL below each 5-minute candle low. |
| **5. Daily Kill Switch** | **Max 3 Trades/Day OR 2 Consecutive Losses** | Prevents revenge trading on choppy days. |

---

## 6. Why 3-Minute (`180s`) Polling + Instant Gmail Setup Alerts

### Why 3 Minutes (`180s`) is the Gold Standard for NSE/Zerodha OI
* On NSE/Zerodha Kite, **Price (LTP)** and **Volume** update every tick, but **Exchange Open Interest (OI) snapshots refresh on a 3-minute cycle (`180 seconds`)**.
* Polling OI every 10 or 30 seconds often compares identical OI numbers (`dOI = 0`), masking the real institutional buildup.
* Therefore, our analyzer defaults to **`POLL_INTERVAL_SECONDS=180` (3 minutes)** and compares:
  * **Short-Term Velocity (`3m dOI`, `3m dLTP`, `3m dIV`):** 1 full NSE OI broadcast cycle.
  * **Intraday Trend (`15m dOI`):** 5 full NSE OI broadcast cycles.

### Instant Gmail Alert When 6/6 Rules Satisfy
Whenever all 6 rules align (`BUY_ATM_CE` or `BUY_ATM_PE`), `WhatsAppNotifier` automatically sends a high-priority, mobile-friendly **HTML + Plain-Text Trade Card** to your Gmail with:
* Subject Line: `🚀 [GAMMA BLAST 6/6] BUY_ATM_CE: NIFTY05NOV2624500CE @ ₹126.50`
* **Entry LTP**, **Hard Stop-Loss ($-18\%$)**, **Target 1 ($+25\%$)**, **Target 2 ($+45\%$)**, and **15m Anti-Theta Stop Price**
* **3-Min Option Chain Edge Metrics:** Spot vs VWAP, ATM Straddle %, Strike Quadrant (`SHORT_COVERING`), 3m & 15m $\Delta\text{OI}$, PCR, Volume Burst, IV, Delta, and Theta bleed %.

#### How to Activate Official Gmail Alerts in 60 Seconds (100% Free & Direct from Your Mac):
1. Open your Google Account App Passwords page: **[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)**
   *(Note: 2-Step Verification must be enabled on your Google account to create an App Password).*
2. Type **`LearnOT`** as the App Name and click **Create**.
3. Google will show a **16-character App Password** (e.g., `abcd efgh ijkl mnop`).
4. Paste your Gmail address and that 16-character App Password into your `.env` file (or directly into the **Gmail Alert Card** in the Web UI at `http://127.0.0.1:8080`):
   ```ini
   WHATSAPP_ENABLED=true
   WHATSAPP_PROVIDER=gmail
   GMAIL_USER=your_email@gmail.com
   GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
   ```

---

## 7. Your Daily Practice Routine with OpenAlgo & `uv`

Follow this exact 4-step routine every market day (`9:10 AM – 3:30 PM`):

1. **9:10 AM — Start OpenAlgo & Confirm Analyze Mode**
   * Log in to your local OpenAlgo instance (`http://127.0.0.1:5000`) connected to Zerodha.
   * Keep **Analyze Mode = ON** (Simulator Mode) while practicing for your first 20–30 sessions.
2. **9:15 AM — Launch the Web UI or Terminal Analyzer (`180s` = 3-Min Cycle)**
   * **Web UI Desk:**
     ```bash
     uv run dashboard_ui.py --port 8080
     ```
     Open `http://127.0.0.1:8080` and set **Auto-Poll: `180s (3m NSE OI Cycle ★)`**.
   * **Or Terminal Analyzer:**
     ```bash
     uv run option_chain_analyzer.py --underlying NIFTY --interval 180 --auto-paper
     ```
3. **9:45 AM Onward — Wait for Your Gmail Setup Alert**
   * Whenever all 6 rules pass on a 3-minute snapshot, you receive the high-priority Gmail alert with exact Entry, Stop-Loss, Target, and 15-minute Theta Time-Stop levels so you can review and take the call calmly.
4. **Test Anytime Outside Market Hours**
   * Run:
     ```bash
     uv run option_chain_analyzer.py --test-email
     ```

