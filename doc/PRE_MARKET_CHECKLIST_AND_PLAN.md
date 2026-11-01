# LearnOT Daily Pre-Market Checklist & Game Plan (08:50 AM – 09:15 AM)

Just as [`doc/TRADING_JOURNAL.md`](TRADING_JOURNAL.md) reviews your setups *after* they happen, this **Pre-Market Game Plan** prepares you **before 09:15 AM** so you already know **where Option Sellers are trapped** before the market even opens.

---

## 1. The 6 Pre-Market Pillars to Track Every Morning (`08:55 AM – 09:14 AM`)

### Pillar 1: Pre-Open Gap & Opening Regime (`09:07 AM – 09:08 AM` NSE Pre-Open)
At `09:08 AM`, NSE settles the exact opening price of **NIFTY / BANKNIFTY**. Compare the Opening Spot Price with Yesterday's Close (`PDC`):

| Opening Type | Nifty Points | BankNifty Points | What Happens to Option Sellers? | Your Option Buying Pre-Plan |
| :--- | :---: | :---: | :--- | :--- |
| **1. Flat Open** | $\pm 0 \text{ to } 50$ pts | $\pm 0 \text{ to } 120$ pts | Overnight writers are comfortable; premiums are cheap. | **Best Setup Day:** Wait for `09:30 AM` range breakout + `6/6` Gamma Blast signal. |
| **2. Moderate Gap** | $\pm 50 \text{ to } 130$ pts | $\pm 120 \text{ to } 300$ pts | Writers on the gap side are immediately under pressure! | **Watch Trapped Strike:** If gap opens near a major round strike (e.g., `24500`), watch for `SHORT_COVERING` on that strike at `09:20–09:35 AM`. |
| **3. Huge Gap** | $> 150$ pts | $> 350$ pts | Morning IV spikes artificially at `09:15 AM` and then **crashes** (`IV Crush`). | **DO NOT CHASE AT 09:15 AM:** Wait until `10:00 AM` for IV to settle and Spot to retest Session VWAP. |

---

### Pillar 2: Yesterday's 3 Institutional Levels (`PDH`, `PDL`, `PDC`)
Mark these 3 lines on your Spot chart before `09:15 AM`:
1. **Previous Day High (`PDH`):** Where yesterday's Call Sellers placed their stop-losses.
   * *Pre-Plan:* If Spot breaks above `PDH` + ATM CE shows `SHORT_COVERING` $\rightarrow$ **High-Probability `BUY_ATM_CE`**.
2. **Previous Day Low (`PDL`):** Where yesterday's Put Sellers placed their stop-losses.
   * *Pre-Plan:* If Spot breaks below `PDL` + ATM PE shows `SHORT_COVERING` $\rightarrow$ **High-Probability `BUY_ATM_PE`**.
3. **Previous Day Close (`PDC`):** Acts as a magnet if the market opens with a weak gap and fails to hold the first 15-minute candle.

---

### Pillar 3: Overnight OI Walls & "Pre-Trapped Seller" Strike Detection
Before `09:15 AM`, look at yesterday's closing Option Chain (or run `uv run option_chain_analyzer.py --once` at `09:10 AM`):
* **Call OI Wall (Resistance):** Strike with Highest Call OI (e.g., `24500 CE` or `24600 CE`).
* **Put OI Wall (Support):** Strike with Highest Put OI (e.g., `24400 PE` or `24300 PE`).

> [!IMPORTANT]
> **The #1 Morning Jackpot Setup ("Overnight Trapped Writers"):**
> * Suppose yesterday's **Highest Call OI** was at **`24500 CE`**, and today at `09:08 AM` Pre-Open, Nifty opens at **`24525`** (above the Call Wall!).
> * Everyone who sold `24500 CE` yesterday is **instantly in a heavy loss at 09:15 AM**.
> * If Nifty holds above `24500` during the first 15 minutes (`09:15–09:30 AM`), those trapped Call Sellers will panic-buy back their Calls (`SHORT_COVERING`), triggering a massive rally toward `24600`!
> * Same in reverse if Nifty gaps down *below* the **Highest Put OI strike**.

---

### Pillar 4: India VIX (Volatility Thermometer)
Check **India VIX** before the open to set your profit-booking expectation:
* **India VIX $< 11.5$ (Low Volatility):** Expect slower option moves and faster Theta decay. Book $75\%$ of your position at **Target 1 ($+20\%\text{ to }+25\%$)**.
* **India VIX $12.0 \text{ – } 18.0$ (Normal / Ideal):** Best environment for Option Buying; follow standard **Target 1 ($+25\%$)** and **Target 2 ($+45\%$)**.
* **India VIX $> 20.0$ (High Event Volatility):** Option premiums are expensive and prone to sudden **IV Crush**. Cut lot size by $50\%$ and never buy OTM options.

---

### Pillar 5: Days to Expiry (`DTE`) & Strike Selection Rule
Check how many days remain until the nearest weekly expiry:
* **3 to 5 Days to Expiry:** Trade **ATM** strike ($\text{Delta} \approx 0.50\text{–}0.55$).
* **1 to 2 Days to Expiry:** Trade **ATM or 1-Strike ITM (`ITM1`)** ($\text{Delta} \approx 0.55\text{–}0.65$) to reduce Theta bleed.
* **0 DTE (Expiry Day):**
  * Morning (`09:25 AM – 11:15 AM`): Strictly trade **`ITM1`** ($\text{Delta} \ge 0.60$).
  * Afternoon (`01:30 PM – 02:45 PM`): Watch for **Pin-Break Gamma Squeeze** where ATM Call or Put OI drops sharply (`SHORT_COVERING`).

---

### Pillar 6: System & Risk Guardrail Check (`09:10 AM`)
1. OpenAlgo running at `http://127.0.0.1:5000` and logged into Zerodha?
2. OpenAlgo **Analyze Mode = ON** (if practicing) or Live Lot Size verified?
3. LearnOT Web UI (`http://127.0.0.1:8080`) launched with Auto-Poll set to **`180s (3m NSE OI Cycle ★)`**?

---

## 2. Daily Pre-Market Worksheet (Copy & Fill in 2 Minutes at 09:08 AM)

```markdown
### 📅 Date: YYYY-MM-DD | Index: NIFTY / BANKNIFTY | Expiry: ________ (DTE: __d)

1. **Yesterday's Key Spot Levels:**
   - PDH (Prev Day High)  : ________
   - PDL (Prev Day Low)   : ________
   - PDC (Prev Day Close) : ________

2. **09:08 AM Pre-Open Settlement:**
   - Pre-Open Spot        : ________ (Gap: ____ pts -> [ ] Flat  [ ] Moderate Gap  [ ] Huge Gap)
   - India VIX            : ________ ([ ] <11.5 Low  [ ] 12-18 Ideal  [ ] >20 High)

3. **Overnight Option Chain Walls:**
   - Major Call Resistance (Max CE OI) : ________ CE
   - Major Put Support (Max PE OI)     : ________ PE
   - Are Overnight Writers Trapped by the Gap? : [ ] Yes (Strike: ______)  [ ] No

4. **My Pre-Planned Scenarios for Today:**
   - 🟢 **Bullish Plan (`BUY_ATM_CE`):** Only if Spot holds above ________ (VWAP / PDH / Put Wall) AND `____ CE` shows `SHORT_COVERING` + `6/6` Checklist.
   - 🔴 **Bearish Plan (`BUY_ATM_PE`):** Only if Spot breaks below ________ (VWAP / PDL / Call Wall) AND `____ PE` shows `SHORT_COVERING` + `6/6` Checklist.
   - ⚪ **No-Trade Zone (Theta Trap):** If Spot stays chopped between ________ and ________ with decaying ATM Straddle.

5. **Risk Commitment:**
   - Mode: [ ] Practice (Analyze Mode ON)  [ ] Live (Lots: __)
   - Hard Stop-Loss: -18% | Time-Stop: 15 Minutes | Max Trades Today: 3
```
