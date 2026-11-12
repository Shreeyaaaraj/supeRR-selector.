# CRICKET PRESSURE INDEX — PHASE 3A (MASTER METHODOLOGY SPECIFICATION)
## Pressure Definition and Analytical Methodology

**Document Version:** 2.2 (Final Master Specification & Formal Sign-Off Specification)  
**Phase:** 3A (Methodology Specification & Analytical Architecture)  
**Status:** Approved Master Architecture Ready for Phase 3B Implementation  
**Author:** Antigravity (Data Science & Cricket Analytics Engineering)  
**Dataset Scope:** Frozen Clean Datasets (`clean_matches.csv`, `clean_ball_by_ball.csv`, `clean_playing_eleven.csv`, `clean_competitions.csv`, `clean_teams.csv`) covering IPL and Senior Men's T20I matches from 2022 onwards.

---

## Methodology Revision Log

| Version | Date | Key Changes, Investigations & Resolutions |
| :---: | :---: | :--- |
| **1.0** | 2026-11-10 | Initial formulation of continuous Pressure Index ($PI$), dual-innings models, Empirical Bayes shrinkage, and Phase 2 limitation audits. |
| **2.0** | 2026-11-10 | Comprehensive revision: Pre-delivery match state decoupling ($t-1$), three separate ball accounting definitions, empirical spectrum of `runs` ($0\text{--}6$ including 5s as overthrows), preliminary run-attribution matrix, and bounded 11 match scenarios. |
| **2.1** | 2026-11-11 | Forensic classification of the single penalty event (Match 16753, Inn 2, Over 6.4: full toss to Harry Tector, square drive, ball 4 of 6, helmet penalty under MCC Law 28.3). Audited 34 no-balls with `extras_2_runs > 0` against official scorecards (Yash Dayal 56 runs, Varun Chakravarthy 33 runs). |
| **2.2** | 2026-11-11 | **Final Correction Audit Resolutions:**<br>1. **No-Ball Extras Arithmetic Reconciled:** Fully decomposed all 35 records with `extras_2_runs > 0`: separated the 34 No-Ball records (18 one-run and 16 four-run records = 82 runs) from the 1 Leg-Bye record (Row 36854: 1 one-run record = 1 run), reconciling the exact total of 83 runs. Exact macro reconciliation confirmed: $272,672 - 3,254 = 269,418$ bowler runs with 0.00 discrepancy.<br>2. **Corrected Bowler DVA for Illegal Deliveries:** Eliminated the mathematical flaw that rewarded illegal deliveries with legal ball par budget. Set expected runs budget on illegal balls to $0.00$, ensuring no-balls and wides are properly penalized ($-1.0$ run). Verified spell-level reconciliation.<br>3. **Batter DVA Eligibility & Striker Wicket Accounting:** Restricted batter DVA strictly to balls faced (`is_batter_ball_faced == True`; wides excluded). Striker-specific dismissal penalty enforced (non-striker run-outs do not penalize the striker).<br>4. **Volatility Stabilizer Edge Cases:** Defined defensible fallbacks for $\text{IQR} \le 10^{-6}$ (fallback to league $\sigma$), insufficient qualified cohort ($N < 10$), and single-match players ($M_i < 2 \implies \kappa = 0.750$).<br>5. **PSR Exposure & Companion Measure:** Enforced single-match player aggregation with minimum pressure exposure cutoffs ($\ge 3$ balls or out for batters; $\ge 6$ balls for bowlers). Added Exposure-Weighted Success Rate ($PSR_{\text{exp}}$). |

---

## 1. Executive Summary & The Four-Level Hierarchy

A foundational principle of the **Cricket Pressure Index (CPI)** is the **strict separation between match pressure leverage and delivery outcome**. If a batter hits a six on ball $t$, that six cannot retroactively alter the pressure assigned to ball $t$. Similarly, if a bowler takes a wicket or bowls a wide on ball $t$, the pressure score of that ball must not be contaminated by the delivery's outcome.

To establish absolute mathematical integrity, CPI operates under a **Four-Level Analytical Architecture**:

```
[LEVEL A: Pre-Delivery Match Pressure State]
       │  (Evaluates match state strictly BEFORE delivery t is bowled)
       ▼
[LEVEL B: Batter Performance]       [LEVEL C: Bowler Performance]
       │  (Runs, Dots, Boundaries)         │  (Runs Conceded, Wickets, Dots)
       └─────────────────┬─────────────────┘
                         ▼
          [LEVEL D: Player Reliability]
             - Match-Level Aggregation & Success (PSR, PSR_exp)
             - Bounded Inter-Match Volatility Penalty (kappa)
             - Empirical Bayes Shrinkage (K)
             - Minimum Qualification Cutoffs
```

- **Level A: Pre-Delivery Match Pressure State:** Computed strictly at $t-1$ (prior to ball $t$ being bowled): $\text{cum\_runs}_{t-1}$, $W_{\text{lost}, t-1}$, $\text{legal\_balls}_{t-1}$, $B_{\text{rem}, t}^{\text{pre}}$, $R_{\text{req}, t}^{\text{pre}}$, $RRR_t^{\text{pre}}$, and $CRR_t^{\text{pre}}$. Delivery outcome data has **0.00% mathematical influence** on the pressure score of ball $t$.
- **Level B: Batter Performance Under Pressure:** Evaluates striker actions on delivery $t$ conditioned on Level A pressure ($PI_t \ge 0.65$).
- **Level C: Bowler Performance Under Pressure:** Evaluates bowler execution on delivery $t$ conditioned on Level A pressure ($PI_t \ge 0.65$).
- **Level D: Player Reliability Across Matches:** Aggregates individual performances across distinct matches, penalizes erratic variance, and regularizes sample sizes via Empirical Bayes shrinkage.

---

## 2. Task 1 & 4: Complete Pre-Delivery Pressure Equations & Validated Scenarios

Pressure is modeled on a continuous scale $[0, 1]$ denoted as $PI_t$:
- **High Pressure:** $PI_t \ge 0.65$ (Focal subset for clutch and reliability rankings)
- **Medium Pressure:** $0.40 \le PI_t < 0.65$
- **Low Pressure / Cruising / Settled:** $PI_t < 0.40$

---

### 2.1 Second-Innings Chasing Formula ($PI_{\text{chase}}$)

For delivery $t$ in Innings 2:
$$PI_{\text{chase}, t} = \Big[ 0.45 \cdot S(RRR_t^{\text{pre}}) + 0.35 \cdot W(W_{\text{lost}, t-1}) + 0.20 \cdot L(B_{\text{rem}, t}^{\text{pre}}) \Big] \times C(RRR_t^{\text{pre}}, B_{\text{rem}, t}^{\text{pre}}, W_{\text{lost}, t-1}) \times M_{\text{stage}}$$

#### 1. Rate Leverage: Bounded Logistic Sigmoid $S(RRR)$
$$S(RRR_t^{\text{pre}}) = \frac{1}{1 + \exp\left(-k_r (RRR_t^{\text{pre}} - RRR_0)\right)}$$
- **Input Range:** $RRR \in [0.0, \infty)$
- **Output Range:** $S \in (0.0, 1.0)$
- **Parameters:**
  - $RRR_0 = 9.60$ RPO: **Empirically Validated** from the median required run rate across all 91,934 second-innings deliveries. At $RRR = 9.60$, $S = 0.50$.
  - $k_r = 0.35$: Calibrated so normal cruising ($RRR = 6.0$) produces $S \approx 0.22$, elevated pressure ($RRR = 12.0$) produces $S \approx 0.69$, and extreme saturation ($RRR \ge 16.0$) produces $S \ge 0.90$.
- **Rationale:** A linear RRR diverges to infinity as $B_{\text{rem}} \to 0$ and causes wild instability from $\pm 1$ run score errors in death overs. The bounded sigmoid reflects tactical reality: requiring 20 RPO is virtually identical in human psychological pressure to requiring 25 RPO (both are near-impossible).

#### 2. Batting Resource Depletion Factor $W(W_{\text{lost}})$
$$W(W_{\text{lost}, t-1}) = 1.0 - \left(\frac{W_{\text{total}} - W_{\text{lost}, t-1}}{W_{\text{total}}}\right)^{1.25}$$
- **Parameters:** $W_{\text{total}} = 10.0$ for standard T20 matches; $W_{\text{total}} = 11.0$ for IPL 2023+ matches (**Impact Player Rule adjustment**).
- **Values:** 0 wkts down = 0.00; 3 down = 0.36; 5 down = 0.58; 7 down = 0.79; 9 down = 0.94.

#### 3. Climax Leverage Factor $L(B_{\text{rem}})$
$$L(B_{\text{rem}, t}^{\text{pre}}) = 1.0 - \left(\frac{B_{\text{rem}, t}^{\text{pre}}}{B_{\text{total}}}\right)^{0.80}$$
- **Values:** Powerplay ($B_{\text{rem}} = 100$): $L \approx 0.13$; Middle ($B_{\text{rem}} = 60$): $L \approx 0.43$; Death ($B_{\text{rem}} = 24$): $L \approx 0.73$; Final Over ($B_{\text{rem}} = 6$): $L \approx 0.91$.

#### 4. Contest Dampener $C(RRR, B_{\text{rem}}, W_{\text{lost}})$
$$C = \begin{cases}
1.0 & \text{if } 6.0 \le RRR \le 18.0 \\
\max\left(0.15, 1.0 - \dfrac{6.0 - RRR}{6.0}\right) & \text{if } RRR < 6.0 \quad (\text{Cruising / One-Sided}) \\
\max\left(0.20, 1.0 - \dfrac{RRR - 18.0}{16.0}\right) & \text{if } RRR > 18.0 \text{ and } B_{\text{rem}} \le 24 \text{ and } (W_{\text{total}} - W_{\text{lost}}) \le 3 \quad (\text{Lost Cause}) \\
1.0 & \text{otherwise}
\end{cases}$$
- **Rationale:** Scales down settled blowouts (needing 4 off 12 balls) or hopeless lost causes (needing 70 off 6 balls with 9 down).

#### 5. Weights & Knockout Multiplier
- $w_1 = 0.45$ (Rate), $w_2 = 0.35$ (Wickets), $w_3 = 0.20$ (Climax). Sum $= 1.00$. Unconditionally bounded in $[0.0, 1.0]$.
- $M_{\text{stage}} = 1.00$ for League stage; $1.15$ for Knockout / Playoff fixtures (capped at $1.0$).

---

### 2.2 First-Innings Target Setting Formula ($PI_{1\text{st}}$)

For delivery $t$ in Innings 1:
$$PI_{1\text{st}, t} = \Big[ 0.40 \cdot P_{\text{collapse}, t} + 0.35 \cdot P_{\text{phase}, t} + 0.25 \cdot P_{\text{pace}, t} \Big] \times M_{\text{stage}}$$
- **Early Collapse Crisis:** $P_{\text{collapse}, t} = \min\left(1.0, \max\left(0.0, \dfrac{W_{\text{lost}, t-1} - \text{Exp\_Wkts}(\text{overid}_t)}{3.0}\right)\right)$.
  - Empirical Expected Wickets: Over 6 = $1.80$; Over 15 = $3.80$; Over 20 = $6.20$.
- **Phase Stakes:** $P_{\text{phase}} = 0.40$ (Powerplay), $0.55$ (Middle), $0.85$ (Death).
- **Pace Deficit:** $P_{\text{pace}, t} = \min\left(1.0, \max\left(0.0, \dfrac{\text{Par\_RR}_{\mathcal{F}, \mathcal{P}} - CRR_t^{\text{pre}}}{3.5}\right)\right)$.
- **Super Over:** Fixed $PI = 1.00$ (isolated clutch supplement across all 26 historical deliveries).

---

### 2.3 Verification Across 11 Diverse Match Scenarios

The formulas were evaluated across 11 test scenarios representing diverse game states:

| Scenario | Game State | $RRR$ / $CRR$ | Dampener ($C$) | Computed $PI$ | Verification Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **1. Settled Blowout Win** | Chasing target 130: 126/1 in Over 18 (4 off 12) | $2.00$ | $0.333$ | **0.080** | Suppressed to Negligible by dampener |
| **2. Dominant Powerplay** | 1st Innings: 65/0 in Over 6 (IPL) | $10.83$ | N/A | **0.140** | Low Pressure (No wickets lost, high rate) |
| **3. Comfortable Chase** | Chasing target 140: 125/2 in Over 16 (15 off 24) | $3.75$ | $0.625$ | **0.176** | Low Pressure (Dampener scales down) |
| **4. Hopeless Defeat / Lost Cause** | Chasing target 210: 140/9 in Over 19 (70 off 6) | $70.00$ | $0.200$ | **0.192** | Suppressed (Eliminates garbage-time inflation) |
| **5. Death Consolidation** | 1st Innings: 155/3 in Over 18 (IPL) | $8.61$ | N/A | **0.447** | Medium Pressure (Wickets in hand) |
| **6. Large Target Early PP Crisis**| Chasing target 220: 28/3 in Over 4 (192 off 96) | $12.00$ | $1.000$ | **0.473** | Medium Pressure (Balanced by 16 overs left) |
| **7. 1st Innings Middle Struggle** | 1st Innings: 48/4 in Over 10 (IPL) | $4.80$ | N/A | **0.617** | Medium-High (Run deficit + 4 down) |
| **8. 1st Innings PP Collapse** | 1st Innings: 18/3 in Over 4 (IPL) | $4.50$ | N/A | **0.630** | Elevated Pressure (Severe early collapse) |
| **9. 1st Innings Death Crisis** | 1st Innings: 130/7 in Over 19 (IPL) | $6.84$ | N/A | **0.718** | High Pressure (Death crisis with tailenders) |
| **10. Difficult Chase** | Chasing target 195: 120/5 in Over 15 (75 off 30) | $15.00$ | $1.000$ | **0.728** | High Pressure (15 RPO with 5 down) |
| **11. Last-Over Close Chase** | Chasing target 170: 158/6 in Over 20 (12 off 6) | $12.00$ | $1.000$ | **0.735** | High Pressure (Peak climax leverage) |

---

## 3. Decoupled Ball Definitions & Penalty Event Classification

### 3.1 Three Decoupled Ball Accounting Rules
1. **Batter Balls Faced (`is_batter_ball_faced`):**
   $$\text{is\_batter\_ball\_faced} = (\text{extras\_type} \ne \text{'wide'})$$
   - *MCC Law Compliance:* Under Law 22.14, wides do not count as balls faced. Under Law 21.18, **no-balls count as balls faced by the striker**.
   - *Dataset Count:* **186,540 deliveries** ($96.15\%$).
2. **Bowler Legal Balls (`is_bowler_legal_ball`):**
   $$\text{is\_bowler\_legal\_ball} = \text{is\_legal\_delivery} = \sim \text{extras\_type}.\text{isin}([\text{'wide'}, \text{'Overstep'}, \text{'other'}])$$
   - *MCC Law Compliance:* Under Law 17.4, an over consists of 6 valid deliveries; wides and no-balls must be re-bowled.
   - *Dataset Count:* **185,715 deliveries** ($95.72\%$). Illegal deliveries (8,299 total) are excluded.
3. **Team Balls Remaining (`legal_balls_remaining_pre`):** Decreases by 1 **only when `is_bowler_legal_ball == True`**.

### 3.2 Classification of the Single Penalty Event
- **Incident:** Match 16753, Inn 2, Over 6.4 (Harry Tector vs Fareed Malik). Fareed bowled a full toss around the wicket; Tector played a square drive; the ball struck the spare helmet placed behind the wicket-keeper, awarding 5 penalty runs under **MCC Law 28.3**.
- **Statutory Classification:**
  - Batter Ball Faced: **`TRUE`** (Legitimately faced by Tector).
  - Bowler Legal Ball: **`TRUE`** (Ball 4 of 6; cumulative balls advanced 33 $\to$ 34).
  - Team Ball Consumed: **`TRUE`** (Balls remaining decreased 87 $\to$ 86).
  - Bowler Runs Conceded: **`0 RUNS`** (Helmet penalty runs are team extras; never debited to the bowler).

---

## 4. Batter Run Spectrum & Striker DVA Eligibility

### 4.1 Empirical Distribution of `runs`
Across all 194,014 deliveries, `runs` takes values in $\{0, 1, 2, 3, 4, 5, 6\}$ with **zero nulls, zero negatives, and zero values $> 6$**:
- 0: 76,463 ($39.41\%$) | 1: 69,628 ($35.89\%$) | 2: 12,183 ($6.28\%$) | 3: 638 ($0.33\%$)
- 4: 22,689 ($11.70\%$, boundary four) | **5: 23 ($0.01\%$)** | 6: 12,390 ($6.39\%$, boundary six)
- **All 23 occurrences of 5 runs:** Confirmed as authentic overthrows under **MCC Law 19.7**. They count fully towards batter runs and strike rate, but not towards boundary % ($B\%$).

### 4.2 Striker Delivery Value Added ($\text{DVA}_d^{\text{bat}}$)
Evaluated only when $\text{is\_batter\_ball\_faced} == \text{True}$ (wides excluded):
$$\text{DVA}_d^{\text{bat}} = \text{runs}_d - \left(\frac{\text{Par\_SR}_{\mathcal{F}, \mathcal{P}}}{100}\right) - \mathbb{I}(\text{dismissed\_player\_id} == \text{striker\_id}) \times \text{Wkt\_Penalty}_{\mathcal{P}}$$
- If the **non-striker is run out**, the striker was not dismissed and is **not penalized**.

---

## 5. Bowler Run Attribution & Corrected DVA for Illegal Deliveries

### 5.1 Reconciliation of All 35 Records with `extras_2_runs > 0`
- **Total records:** 35 records (19 one-run, 16 four-run, sum = 83 runs).
- **Statutory Partition:**
  - **34 No-Ball records** (`Overstep` / `other`): exactly **18 one-run** and **16 four-run** records (Sum = $\mathbf{82 \text{ runs}}$).
  - **1 Leg-Bye record** (Row 36854: Malan vs Rauf, Over 5.4): exactly **1 one-run** record (Sum = $\mathbf{1 \text{ run}}$).
  - Cross-check: $18 + 1 = 19$ one-run; $16 + 0 = 16$ four-run. Total sum $= 82 + 1 = 83$ runs.
- **Rule:** Under MCC Law 21.18, `extras_2_runs` on no-balls are untouched byes/leg-byes and are **never debited to the bowler** (reconciled against official scorecards: Yash Dayal 56 runs, Varun Chakravarthy 33 runs).
- **Macro Dataset Reconciliation:**
  $$\text{Total Delivery Runs (272,672)} - \text{Non-Bowler Extras (3,254)} = \mathbf{269,418 \text{ Bowler Runs Conceded (0.00 Error)}}$$

### 5.2 Corrected Bowler DVA Model
To eliminate the flaw that rewarded illegal deliveries with legal ball budget, expected runs budget is conditioned on bowling a **legal delivery**:
$$\text{Expected\_Runs\_Budget}_d = \begin{cases} \dfrac{\text{Par\_Econ}_{\mathcal{F}, \mathcal{P}}}{6.0} & \text{if } \text{is\_bowler\_legal\_ball}_d == \text{True} \\ 0.00 & \text{if } \text{is\_bowler\_legal\_ball}_d == \text{False} \end{cases}$$

$$\text{DVA}_d^{\text{bowl}} = \text{Expected\_Runs\_Budget}_d - \text{bowler\_runs\_conceded}_d + \mathbb{I}(\text{is\_bowler\_wicket}_d) \times \text{Wkt\_Bonus}_{\mathcal{P}}$$
- **Test:** On a no-ball/wide conceding 1 run: $\text{DVA} = 0.00 - 1.00 = \mathbf{-1.00 \text{ run}}$ (properly penalized).
- **Spell-level sum:** $\sum \text{DVA}_d^{\text{runs}} = (\text{Overs} \times \text{Par\_Econ}) - \text{Runs\_Conceded}$ (identically matches spell-level economy).

---

## 6. Mathematical Reliability, Shrinkage & Volatility Stabilizer

### 6.1 Empirical Bayes Shrinkage & Ranking Stability
$$\theta^*_i = \left(\frac{N_i}{N_i + K}\right) \hat{\theta}_i + \left(\frac{K}{N_i + K}\right) \mu_{\text{prior}}$$
- **Operational Baseline Anchors:** $K_{\text{batter}} = 50$ balls, $K_{\text{bowler}} = 48$ balls.
- **Variance Ratio Context:** Derived from match-level signal-to-noise ratios ($K \approx 4.36$ matches for batters, $7.56$ for bowlers). Framed as proposed operational anchors.
- **Ranking Stability:** Evaluating qualified players across $K \in [25, 100]$ yielded a **90% top-10 overlap (9 of 10 players identical)** between $K=25$, $K=50$, $K=75$, and $K=100$.

### 6.2 Mathematically Guaranteed Volatility Stabilizer ($\kappa$)
$$\kappa_i = 1.0 - 0.25 \cdot \tanh\left(\frac{\sigma_{i, \text{match}}}{\text{Denominator}}\right) \in (0.75, 1.00]$$

#### Edge Case Fallback Governance:
1. **Denominator Fallback ($\text{IQR}_{\text{league}} \le 10^{-6}$):** Fall back to league standard deviation $\sigma_{\text{league}}$ (or $1.00$).
2. **Insufficient Cohort ($N_{\text{qualified}} < 10$):** Fall back to global league historical $\text{IQR} = 0.42$.
3. **Single-Match Players ($M_i < 2$):** Assign $\kappa_i = 0.750$ (maximum volatility penalty for unproven consistency).
4. **Zero Volatility ($\sigma = 0.0$ with $M_i \ge 2$):** Assign $\kappa_i = 1.00$.

---

## 7. Player-Match Aggregation & Pressure Match Success Rate ($PSR$)

### 7.1 Single-Match Aggregation & Minimum Exposure
All pressure deliveries in a match are summed into a single player-match observation:
$$\text{Net\_Match\_DVA}_{i, m} = \sum_{d \in \text{MatchDeliveries}_{i, m} \text{ where } PI_d \ge 0.65} \text{DVA}_d$$
$$\text{Exposure}_{i, m} = \sum_{d \in \text{MatchDeliveries}_{i, m} \text{ where } PI_d \ge 0.65} \mathbb{I}(\text{is\_valid\_opportunity}_d)$$
- **Minimum Exposure Cutoffs:**
  - Batters: $\ge 3$ pressure balls faced OR dismissed under pressure.
  - Bowlers: $\ge 6$ legal pressure balls bowled (at least 1 full pressure over).

### 7.2 Dual Success Reporting
1. **Unweighted Match Win Rate ($PSR_i$):**
   $$PSR_i = \frac{1}{M_i} \sum_{m=1}^{M_i} \mathbb{I}(\text{Net\_Match\_DVA}_{i, m} > 0.0) \in [0.0, 1.0]$$
2. **Exposure-Weighted Pressure Success Index ($PSR_{\text{exp}, i}$):**
   $$PSR_{\text{exp}, i} = \frac{\sum_{m=1}^{M_i} \left( \text{Exposure}_{i, m} \times \mathbb{I}(\text{Net\_Match\_DVA}_{i, m} > 0.0) \right)}{\sum_{m=1}^{M_i} \text{Exposure}_{i, m}} \in [0.0, 1.0]$$

---

## 8. Final Unresolved Limitations & Governance Table

| # | Methodology Domain | Investigated Edge Case | Resolution Implemented | Remaining Analytical Limitation / Trade-Off |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **No-Ball Extras Accounting** | Untouched byes/leg-byes recorded in `extras_2_runs` on no-balls. | Decomposed 34 no-balls (82 runs) and 1 leg-bye (1 run) = 83 runs. Debited only $1 + \text{runs}$ to bowler under Law 21.18. | Match scorecards record team totals; delivery-level attribution reflects official ICC bowling debits but relies on reconstructed codes. |
| **2** | **Bowler DVA on Illegal Deliveries** | Bowlers were rewarded $+1.50$ runs budget on no-balls/wides under naive rate formulas. | Set expected runs budget to $0.00$ on illegal balls. DVA $= -\text{runs}$. Sum of DVA reconciles to spell-level runs saved against par. | Does not include an additional subjective free-hit penalty beyond the runs conceded on the free hit itself. |
| **3** | **Batter DVA Opportunities** | Wides and non-striker run-outs inflating/distorting batter metrics. | Excluded wides from batter DVA; charged dismissal penalties exclusively to striker when `dismissed_player_id == striker_id`. | Tactical run-outs sacrificed by a partner to keep a star batter on strike cannot be algorithmically distinguished from accidental run-outs. |
| **4** | **Bayesian Shrinkage Parameters** | $K_{\text{batter}} = 50$ and $K_{\text{bowler}} = 48$ converted from match-level variance ratios ($K \approx 4.36$ and $7.56$). | Framed $K$ as operational baseline anchors. Ranking stability proven (90% top-10 overlap across $K \in [25, 100]$). Sensitivity grid retained. | Assumes pseudo-i.i.d. ball outcomes within matches; sensitivity grid reporting is mandatory. |
| **5** | **Inter-Match Volatility Penalty** | Unbounded exponential dropped below $0.75$ for high $\sigma$; potential $\text{IQR} = 0$ division. | Adopted $\kappa = 1.0 - 0.25 \cdot \tanh(\sigma / \text{IQR}) \in (0.75, 1.00]$ with explicit fallbacks for $\text{IQR} = 0$, $N < 10$, and $M_i < 2$. | IQR is computed across the qualified cohort; fringe player volatility relies on cohort stabilization. |
| **6** | **Pressure Exposure Discrepancies** | 1-ball cameo appearances distorting binary match win rates. | Enforced minimum exposure ($\ge 3$ balls or out for batters; $\ge 6$ balls for bowlers) and dual reporting with $PSR_{\text{exp}}$. | Players right at the 3-ball threshold are given full match status if dismissed. |

---

## 9. Formal Sign-Off Specification

The Master Methodology Specification (Version 2.2) is complete, mathematically bounded, forensically audited, and verified against cricket statutory laws.

- [x] **No-Ball Extras Arithmetic:** Reconciled ($18 \times 1 + 16 \times 4 = 82$ on no-balls; $1$ on leg-bye; macro error = 0.00).
- [x] **Bowler DVA:** Conditioned on legal balls; zero reward for illegal balls; spell-level reconciliation verified.
- [x] **Batter DVA:** Restricted strictly to balls faced; non-striker run-outs separated.
- [x] **Volatility Edge Cases:** Robust fallbacks for $\text{IQR} = 0$ and $M_i < 2$; range guaranteed in $(0.75, 1.00]$.
- [x] **PSR Aggregation:** Single-match grouping; exposure thresholds; dual reporting with $PSR_{\text{exp}}$.
- [x] **Frozen Datasets:** 100% untouched and preserved.

**Methodology Version 2.2 is complete and frozen for formal sign-off.**
Upon approval, Phase 3B (Feature Engineering and Scoring Engine Implementation) will begin.
