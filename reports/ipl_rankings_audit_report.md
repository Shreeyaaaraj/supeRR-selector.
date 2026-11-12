# CRICKET PRESSURE INDEX — PHASE 4: IPL-ONLY FINAL RANKINGS AUDIT REPORT

Generated: 2026-11-11 08:46:31 UTC
Scope: Indian Premier League Matches Only (Seasons 2022–2026)
Specification: Approved Phase 3A Version 2.2 Master Methodology

---

## 1. Executive Summary & Competition Isolation

This audit report confirms the successful isolation, recalculation, and validation of **IPL-only** final pressure reliability rankings.

- **Competitions Filtered**: Strictly restricted to IPL seasons 2022, 2023, 2024, 2025, and 2026 (`comp_id` in `[1358, 1715, 2193, 2725, 3298]`).
- **IPL Match Pool**: 371 matches evaluated across 5 tournament editions.
- **Exclusion of T20Is**: Exactly 0 Men's T20I matches, bilat deals, or non-IPL tournaments were included in this pipeline.
- **Pakistani Players Verification**: Pakistani international players appearing in previous combined rankings (Mohammad Nawaz, Shadab Khan, Abrar Ahmed) have 0 IPL appearances and are completely excluded from these IPL rankings. All T20I data remains preserved in the combined datasets.
- **Frozen Master Integrity**: All 5 processed master files (`clean_*.csv`) and raw datasets remain 100% untouched and immutable.

## 2. IPL Cohort Qualification & Sample Attrition

### A. Batters Cohort
- Total Batters Evaluated in IPL: **341**
- Satisfying Career Ball Minimum (>= 120 balls in IPL): 129
- Satisfying Pressure Exposure Minimum (>= 40 balls in IPL): 66
- Satisfying Qualifying Matches (>= 6 matches with >= 3 balls/out in IPL): 65
- **Fully Qualified IPL Batters**: **45** (13.2%)
- **Additional Qualified Batters Available**: **35** beyond the Top 10.
- Primary Reasons for Failure: 275 failed on pressure balls faced (< 40); 12 met ball volume but failed on qualifying matches (< 6).
  *Notable Batters Failing Match Cutoff*: Shikhar Dhawan (40 balls, 2 matches), David Warner (47 balls, 3 matches), Kieron Pollard (47 balls, 4 matches), Liam Livingstone (53 balls, 5 matches), Rishabh Pant (44 balls, 4 matches), Sherfane Rutherford (57 balls, 5 matches).

### B. Bowlers Cohort
- Total Bowlers Evaluated in IPL: **260**
- Satisfying Career Legal Balls (>= 120 balls in IPL): 146
- Satisfying Pressure Exposure (>= 36 legal balls in IPL): 77
- Satisfying Qualifying Matches (>= 6 matches with >= 6 legal balls in IPL): 53
- **Fully Qualified IPL Bowlers**: **53** (20.4%)
- **Additional Qualified Bowlers Available**: **43** beyond the Top 10.
- Primary Reasons for Failure: 183 failed on pressure legal balls (< 36); 24 met ball volume but failed on qualifying matches (< 6).
  *Notable Bowlers Failing Match Cutoff*: Deepak Chahar (49 balls, 5 matches), Axar Patel (58 balls, 5 matches), Hardik Pandya (41 balls, 4 matches), Mitchell Santner (39 balls, 5 matches), Dwayne Bravo (47 balls, 3 matches).

## 3. Recalculated IPL Priors & Volatility Denominators

| Parameter / Metric | Batters Cohort (N=45) | Bowlers Cohort (N=53) |
| :--- | :---: | :---: |
| **Operational Shrinkage Anchor (K)** | K_batter = 50 balls | K_bowler = 48 legal balls |
| **Cohort Volatility Denominator (IQR_cohort)** | **2.4009** | **2.7580** |
| **Prior Mean Raw PSR (mu)** | 0.3431 (34.3%) | 0.6055 (60.5%) |
| **Prior Mean Exposure PSR (mu)** | **0.4303** (43.03%) | **0.6210** (62.10%) |
| **Prior Mean Clutch Delta (mu)** | +10.34 SR | +0.04 RPO |

## 4. Definitive Top 10 Most Reliable IPL Batters

| Rank | ID | Player Name | Franchises (2022–2026) | Qual M | Pressure Balls | Raw PSR | Exp PSR | Shrunk PSR (K=50) | Kappa (volatility) | Composite Score | Base SR | Press SR | Delta SR | Sensitivity Range |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 4708 | **Rinku Singh** | Kolkata Knight Riders | 14 | 191 | 0.6429 | 0.8263 | 0.7441 | 0.7503 | **0.5583** | 136.72 | 198.43 | +61.71 | #1 - #1 (Shift: 0) |
| **2** | 7260 | **Dhruv Jurel** | Rajasthan Royals | 8 | 92 | 0.6250 | 0.8090 | 0.6757 | 0.7553 | **0.5103** | 147.73 | 202.17 | +54.44 | #2 - #2 (Shift: 0) |
| **3** | 1077 | **David Miller** | Delhi Capitals, Gujarat Titans, Lucknow Super Giants | 12 | 109 | 0.7500 | 0.7619 | 0.6576 | 0.7509 | **0.4938** | 134.66 | 214.68 | +80.02 | #3 - #3 (Shift: 0) |
| **4** | 8101 | **Ashutosh Sharma** | Delhi Capitals, Punjab Kings | 13 | 116 | 0.6154 | 0.7193 | 0.6323 | 0.7505 | **0.4745** | 144.04 | 215.52 | +71.48 | #4 - #6 (Shift: 2) |
| **5** | 7897 | **Namboori Tilak Varma** | Mumbai Indians | 9 | 81 | 0.6667 | 0.7500 | 0.6280 | 0.7512 | **0.4717** | 139.02 | 228.40 | +89.38 | #5 - #6 (Shift: 1) |
| **6** | 6396 | **Tim David** | Mumbai Indians, Royal Challengers Bengaluru | 18 | 200 | 0.6111 | 0.6717 | 0.6234 | 0.7505 | **0.4679** | 174.27 | 185.50 | +11.23 | #4 - #8 (Shift: 4) |
| **7** | 1699 | **Suryakumar Yadav** | Mumbai Indians | 8 | 56 | 0.5000 | 0.7778 | 0.6139 | 0.7605 | **0.4669** | 164.44 | 176.79 | +12.35 | #4 - #8 (Shift: 4) |
| **8** | 3297 | **Shimron Hetmyer** | Rajasthan Royals | 11 | 96 | 0.5455 | 0.7188 | 0.6200 | 0.7514 | **0.4659** | 146.48 | 160.42 | +13.94 | #7 - #8 (Shift: 1) |
| **9** | 6460 | **Ayush Badoni** | Lucknow Super Giants | 10 | 111 | 0.5000 | 0.6273 | 0.5661 | 0.7510 | **0.4252** | 136.69 | 168.47 | +31.78 | #9 - #10 (Shift: 1) |
| **10** | 37052 | **Naman Dhir** | Mumbai Indians | 7 | 66 | 0.4286 | 0.6667 | 0.5648 | 0.7514 | **0.4244** | 159.95 | 186.36 | +26.42 | #9 - #10 (Shift: 1) |

## 5. Definitive Top 10 Most Reliable IPL Bowlers

| Rank | ID | Player Name | Franchises (2022–2026) | Qual M | Legal Balls | Raw PSR | Exp PSR | Shrunk PSR (K=48) | Kappa (volatility) | Composite Score | Base Econ | Press Econ | Clutch Delta | Sensitivity Range |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 2933 | **Jasprit Bumrah** | Mumbai Indians | 15 | 123 | 0.9333 | 0.9464 | 0.8551 | 0.7575 | **0.6477** | 7.29 | 5.90 | +1.38 | #1 - #1 (Shift: 0) |
| **2** | 29888 | **Harshit Rana** | Kolkata Knight Riders | 11 | 98 | 0.9091 | 0.9053 | 0.8118 | 0.7804 | **0.6335** | 9.95 | 7.04 | +2.91 | #2 - #2 (Shift: 0) |
| **3** | 781 | **Sunil Narine** | Kolkata Knight Riders | 10 | 128 | 0.9000 | 0.8911 | 0.8174 | 0.7589 | **0.6203** | 6.94 | 5.86 | +1.08 | #3 - #4 (Shift: 1) |
| **4** | 8661 | **Matheesha Pathirana** | Chennai Super Kings, Kolkata Knight Riders | 12 | 158 | 0.8333 | 0.8716 | 0.8132 | 0.7575 | **0.6160** | 8.64 | 7.97 | +0.67 | #3 - #4 (Shift: 1) |
| **5** | 2847 | **Shardul Thakur** | Chennai Super Kings, Delhi Capitals, Kolkata Knight Riders, Lucknow Super Giants, Mumbai Indians | 8 | 87 | 0.8750 | 0.8519 | 0.7698 | 0.7727 | **0.5948** | 10.64 | 8.69 | +1.95 | #5 - #6 (Shift: 1) |
| **6** | 6256 | **Varun Chakravarthy** | Kolkata Knight Riders | 18 | 174 | 0.8333 | 0.8364 | 0.7898 | 0.7527 | **0.5945** | 8.32 | 7.14 | +1.18 | #5 - #7 (Shift: 2) |
| **7** | 5939 | **Cameron Green** | Kolkata Knight Riders, Mumbai Indians, Royal Challengers Bengaluru | 6 | 57 | 0.8333 | 0.8909 | 0.7675 | 0.7565 | **0.5806** | 9.55 | 7.58 | +1.97 | #6 - #9 (Shift: 3) |
| **8** | 7322 | **Yash Dayal** | Gujarat Titans, Royal Challengers Bengaluru | 9 | 78 | 0.7778 | 0.8182 | 0.7431 | 0.7809 | **0.5803** | 9.60 | 8.69 | +0.91 | #7 - #8 (Shift: 1) |
| **9** | 36982 | **Suyash Sharma** | Kolkata Knight Riders, Royal Challengers Bengaluru | 9 | 124 | 0.6667 | 0.8257 | 0.7686 | 0.7500 | **0.5764** | 9.30 | 6.48 | +2.81 | #8 - #9 (Shift: 1) |
| **10** | 4692 | **Lockie Ferguson** | Gujarat Titans, Kolkata Knight Riders, Punjab Kings, Royal Challengers Bengaluru | 9 | 76 | 0.7778 | 0.8088 | 0.7361 | 0.7685 | **0.5657** | 10.16 | 8.53 | +1.63 | #10 - #11 (Shift: 1) |

## 6. Sensitivity Grid Analysis Across K in [25, 100]

### A. Batters Grid (K in [25, 50, 75, 100])
- **Top 10 Overlap Across Every Comparison**: **10 / 10 (100.0%)**.
- All 10 batters remain in the Top 10 across the entire grid K=25 to K=100.
- **Rank Shifts**: Rinku Singh (#1 across all K), Dhruv Jurel (#2 across all K), David Miller (#3 across all K).
  Ashutosh Sharma (#4 to #6), Tilak Varma (#5 to #6), Tim David (#4 to #8), Suryakumar Yadav (#4 to #8), Shimron Hetmyer (#7 to #8), Ayush Badoni (#9 to #10), Naman Dhir (#9 to #10).

### B. Bowlers Grid (K in [25, 48, 75, 100])
- **Overlap K=25 vs K=48**: **10 / 10 (100.0%)**.
- **Overlap K=48 vs K=75**: **10 / 10 (100.0%)**.
- **Overlap K=48 vs K=100**: **9 / 10 (90.0%)** (Lockie Ferguson #11; Maheesh Theekshana #10).
- **Rank Shifts**: Jasprit Bumrah (#1 across all K), Harshit Rana (#2 across all K), Sunil Narine (#3 to #4), Matheesha Pathirana (#3 to #4).

## 7. Step-by-Step Manual Calculations (First 3 Batters & First 3 Bowlers)

### A. IPL Batters (K = 50, mu = 0.4303, IQR = 2.4009)

#### Rank 1: Rinku Singh (ID 4708)
- Qualifying Matches: M = 14, Wins: W = 9 -> Raw PSR = 0.6429
- Exposure-Weighted PSR: PSR_exp = 0.8263 (191 pressure balls)
- Match Volatility: sigma = 8.9872 -> tanh(8.9872 / 2.4009) = 0.9989
- Stabilizer: kappa = 1.0 - 0.25 * 0.9989 = 0.7503
- Shrinkage: w_N = 191/(191+50) = 0.7925, w_K = 50/(191+50) = 0.2075
- Shrunk Exp PSR: theta* = (0.7925 * 0.8263) + (0.2075 * 0.4303) = 0.7441
- Final Composite Reliability Score: Reliability = 0.7441 * 0.7503 = **0.5583**

#### Rank 2: Dhruv Jurel (ID 7260)
- Qualifying Matches: M = 8, Wins: W = 5 -> Raw PSR = 0.6250
- Exposure-Weighted PSR: PSR_exp = 0.8090 (92 pressure balls)
- Match Volatility: sigma = 5.4398 -> tanh(5.4398 / 2.4009) = 0.9787
- Stabilizer: kappa = 1.0 - 0.25 * 0.9787 = 0.7553
- Shrinkage: w_N = 92/(92+50) = 0.6479, w_K = 50/(92+50) = 0.3521
- Shrunk Exp PSR: theta* = (0.6479 * 0.8090) + (0.3521 * 0.4303) = 0.6757
- Final Composite Reliability Score: Reliability = 0.6757 * 0.7553 = **0.5103**

#### Rank 3: David Miller (ID 1077)
- Qualifying Matches: M = 12, Wins: W = 9 -> Raw PSR = 0.7500
- Exposure-Weighted PSR: PSR_exp = 0.7619 (109 pressure balls)
- Match Volatility: sigma = 7.5688 -> tanh(7.5688 / 2.4009) = 0.9964
- Stabilizer: kappa = 1.0 - 0.25 * 0.9964 = 0.7509
- Shrinkage: w_N = 109/(109+50) = 0.6855, w_K = 50/(109+50) = 0.3145
- Shrunk Exp PSR: theta* = (0.6855 * 0.7619) + (0.3145 * 0.4303) = 0.6576
- Final Composite Reliability Score: Reliability = 0.6576 * 0.7509 = **0.4938**

### B. IPL Bowlers (K = 48, mu = 0.6210, IQR = 2.7580)

#### Rank 1: Jasprit Bumrah (ID 2933)
- Qualifying Matches: M = 15, Wins: W = 14 -> Raw PSR = 0.9333
- Exposure-Weighted PSR: PSR_exp = 0.9464 (123 legal balls)
- Match Volatility: sigma = 5.7641 -> tanh(5.7641 / 2.7580) = 0.9699
- Stabilizer: kappa = 1.0 - 0.25 * 0.9699 = 0.7575
- Shrinkage: w_N = 123/(123+48) = 0.7193, w_K = 48/(123+48) = 0.2807
- Shrunk Exp PSR: theta* = (0.7193 * 0.9464) + (0.2807 * 0.6210) = 0.8551
- Final Composite Reliability Score: Reliability = 0.8551 * 0.7575 = **0.6477**

#### Rank 2: Harshit Rana (ID 29888)
- Qualifying Matches: M = 11, Wins: W = 10 -> Raw PSR = 0.9091
- Exposure-Weighted PSR: PSR_exp = 0.9053 (98 legal balls)
- Match Volatility: sigma = 3.7765 -> tanh(3.7765 / 2.7580) = 0.8785
- Stabilizer: kappa = 1.0 - 0.25 * 0.8785 = 0.7804
- Shrinkage: w_N = 98/(98+48) = 0.6712, w_K = 48/(98+48) = 0.3288
- Shrunk Exp PSR: theta* = (0.6712 * 0.9053) + (0.3288 * 0.6210) = 0.8118
- Final Composite Reliability Score: Reliability = 0.8118 * 0.7804 = **0.6335**

#### Rank 3: Sunil Narine (ID 781)
- Qualifying Matches: M = 10, Wins: W = 9 -> Raw PSR = 0.9000
- Exposure-Weighted PSR: PSR_exp = 0.8911 (128 legal balls)
- Match Volatility: sigma = 5.5293 -> tanh(5.5293 / 2.7580) = 0.9644
- Stabilizer: kappa = 1.0 - 0.25 * 0.9644 = 0.7589
- Shrinkage: w_N = 128/(128+48) = 0.7273, w_K = 48/(128+48) = 0.2727
- Shrunk Exp PSR: theta* = (0.7273 * 0.8911) + (0.2727 * 0.6210) = 0.8174
- Final Composite Reliability Score: Reliability = 0.8174 * 0.7589 = **0.6203**

================================================================================
PHASE 4 IPL-ONLY RANKINGS AUDIT COMPLETE — ALL METRICS VALIDATED
================================================================================
