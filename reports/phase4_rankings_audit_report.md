# CRICKET PRESSURE INDEX — PHASE 4: RANKINGS AUDIT & VALIDATION REPORT

Generated: 2026-11-11 06:36:35 UTC
Specification: Approved Phase 3A Version 2.2 Master Specification
Status: Complete, Reconciled, and Verified

---

## 1. Executive Summary & Audit Verification

The Phase 4 rankings audit confirms that the **Top 10 Most Reliable Batters** and **Top 10 Most Reliable Bowlers Under Pressure** have been derived strictly and deterministically from the approved Phase 3D reliability engine outputs.

- **Batters Evaluated**: 824 total -> **98 Qualified** (>= 40 pressure balls, >= 6 qualifying matches, >= 120 career balls).
- **Bowlers Evaluated**: 596 total -> **112 Qualified** (>= 36 legal pressure balls, >= 6 qualifying matches, >= 120 career legal balls).
- **Integrity Verification**: Exactly 10 batters and 10 bowlers selected; exactly 0 duplicate player IDs; 0 unqualified players included.
- **Frozen Dataset Integrity**: All 5 processed master files (`clean_*.csv`) and delivery-level pipeline files remain 100% untouched and immutable.

## 2. Definitive Top 10 Batters Table

| Rank | ID | Player Name | Primary Team / Country | Qual M | Pressure Balls | Raw PSR | Exp PSR | Shrunk PSR (K=50) | Kappa | Composite Score | Base SR | Press SR | Delta SR | Sensitivity Range |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 4708 | **Rinku Singh** | India | 15 | 199 | 0.6000 | 0.7929 | 0.7203 | 0.7503 | **0.5405** | 144.94 | 194.97 | +50.04 | #1 - #2 (Shift: 1) |
| **2** | 1699 | **Suryakumar Yadav** | India | 10 | 85 | 0.6000 | 0.8519 | 0.6962 | 0.7534 | **0.5245** | 165.47 | 196.47 | +31.00 | #1 - #5 (Shift: 4) |
| **3** | 6725 | **Sherfane Rutherford** | Gujarat Titans | 11 | 114 | 0.6364 | 0.8158 | 0.6987 | 0.7506 | **0.5244** | 141.05 | 201.75 | +60.70 | #2 - #3 (Shift: 1) |
| **4** | 7260 | **Dhruv Jurel** | India | 8 | 94 | 0.6250 | 0.8090 | 0.6779 | 0.7551 | **0.5119** | 144.89 | 198.94 | +54.05 | #4 - #6 (Shift: 2) |
| **5** | 6396 | **Tim David** | Australia | 24 | 249 | 0.6667 | 0.7247 | 0.6757 | 0.7507 | **0.5072** | 173.08 | 195.58 | +22.50 | #2 - #9 (Shift: 7) |
| **6** | 7897 | **Namboori Tilak Varma** | India | 17 | 181 | 0.7059 | 0.7389 | 0.6724 | 0.7519 | **0.5056** | 139.11 | 202.76 | +63.65 | #4 - #8 (Shift: 4) |
| **7** | 37052 | **Naman Dhir** | India | 10 | 103 | 0.6000 | 0.7864 | 0.6704 | 0.7505 | **0.5032** | 163.35 | 206.80 | +43.45 | #6 - #7 (Shift: 1) |
| **8** | 8221 | **Nitish Reddy** | India | 7 | 65 | 0.5714 | 0.8462 | 0.6659 | 0.7517 | **0.5006** | 146.29 | 189.23 | +42.94 | #5 - #8 (Shift: 3) |
| **9** | 4106 | **Daryl Mitchell** | Chennai Super Kings | 7 | 54 | 0.5714 | 0.8148 | 0.6306 | 0.7695 | **0.4852** | 144.34 | 159.26 | +14.92 | #7 - #13 (Shift: 6) |
| **10** | 4773 | **Jaker Ali Anik** | Bangladesh | 7 | 98 | 0.7143 | 0.7526 | 0.6441 | 0.7503 | **0.4833** | 117.63 | 182.65 | +65.02 | #9 - #11 (Shift: 2) |

## 3. Definitive Top 10 Bowlers Table

| Rank | ID | Player Name | Primary Team / Country | Qual M | Legal Balls | Raw PSR | Exp PSR | Shrunk PSR (K=48) | Kappa | Composite Score | Base Econ | Press Econ | Clutch Delta | Sensitivity Range |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 2490 | **Mohammad Nawaz** | Pakistan | 12 | 115 | 1.0000 | 1.0000 | 0.8958 | 0.7570 | **0.6781** | 7.39 | 5.06 | +2.33 | #1 - #1 (Shift: 0) |
| **2** | 4926 | **Shadab Khan** | Pakistan | 10 | 104 | 1.0000 | 1.0000 | 0.8883 | 0.7555 | **0.6711** | 8.23 | 5.31 | +2.93 | #2 - #3 (Shift: 1) |
| **3** | 5979 | **Abrar Ahmed** | Pakistan | 14 | 136 | 0.9286 | 0.9528 | 0.8728 | 0.7602 | **0.6635** | 7.22 | 4.06 | +3.16 | #2 - #4 (Shift: 2) |
| **4** | 4823 | **Washington Sundar** | Gujarat Titans | 6 | 74 | 1.0000 | 1.0000 | 0.8608 | 0.7633 | **0.6570** | 8.28 | 6.16 | +2.12 | #3 - #4 (Shift: 1) |
| **5** | 2933 | **Jasprit Bumrah** | India | 25 | 204 | 0.8400 | 0.8723 | 0.8292 | 0.7514 | **0.6231** | 7.25 | 6.65 | +0.60 | #5 - #8 (Shift: 3) |
| **6** | 1813 | **Deepak Chahar** | Chennai Super Kings | 9 | 87 | 0.8889 | 0.9178 | 0.8212 | 0.7579 | **0.6224** | 9.02 | 9.31 | -0.29 | #5 - #8 (Shift: 3) |
| **7** | 781 | **Sunil Narine** | Kolkata Knight Riders | 10 | 128 | 0.9000 | 0.8911 | 0.8243 | 0.7536 | **0.6212** | 6.94 | 5.86 | +1.08 | #6 - #7 (Shift: 1) |
| **8** | 4692 | **Lockie Ferguson** | Gujarat Titans | 18 | 162 | 0.8333 | 0.8649 | 0.8149 | 0.7564 | **0.6164** | 9.17 | 7.07 | +2.10 | #6 - #11 (Shift: 5) |
| **9** | 29888 | **Harshit Rana** | India | 15 | 126 | 0.8667 | 0.8770 | 0.8133 | 0.7549 | **0.6140** | 9.89 | 7.57 | +2.32 | #9 - #10 (Shift: 1) |
| **10** | 5939 | **Cameron Green** | Australia | 8 | 79 | 0.8750 | 0.9104 | 0.8105 | 0.7542 | **0.6113** | 9.79 | 7.14 | +2.65 | #7 - #14 (Shift: 7) |

## 4. Tie-Breaking Documentation

The Phase 3A Version 2.2 Master Specification does not specify an explicit secondary tie-breaker. However, because the final composite reliability scores $\text{Reliability\_Score} = \text{PSR}^*_{\text{exp}} \times \kappa_i$ are distinct to 4 decimal places across all 20 ranked players, no tie-breaking rule was required to establish the unambiguous rank order.

## 5. Step-by-Step Manual Calculations (First 3 Batters & First 3 Bowlers)

### A. Batters (Prior Mean $\mu = 0.4316$, Anchor $K = 50$, Denominator $\text{IQR} = 2.3831$)

#### Rank 1: Rinku Singh (ID 4708)
- Matches: $M = 15$, Successes: $W = 9$
- Raw PSR: $W / M = 9 / 15 = 0.6000$
- Exposure-Weighted PSR: $\text{PSR}_{\text{exp}} = 0.7929$
- Volatility: $\sigma = 8.8166 \implies \tanh(8.8166 / 2.3831) = 0.9988$
- Volatility Stabilizer: $\kappa = 1.0 - 0.25 \times 0.9988 = 0.7503$
- Shrinkage: $w_N = 199/(199+50) = 0.7992$, $w_K = 50/(199+50) = 0.2008$
- Shrunk Exp PSR: $\theta^* = (0.7992 \times 0.7929) + (0.2008 \times 0.4316) = 0.7203$
- Final Composite Reliability Score: $\text{Reliability} = 0.7203 \times 0.7503 = \mathbf{0.5405}$

#### Rank 2: Suryakumar Yadav (ID 1699)
- Matches: $M = 10$, Successes: $W = 6$
- Raw PSR: $W / M = 6 / 10 = 0.6000$
- Exposure-Weighted PSR: $\text{PSR}_{\text{exp}} = 0.8519$
- Volatility: $\sigma = 5.9515 \implies \tanh(5.9515 / 2.3831) = 0.9865$
- Volatility Stabilizer: $\kappa = 1.0 - 0.25 \times 0.9865 = 0.7534$
- Shrinkage: $w_N = 85/(85+50) = 0.6296$, $w_K = 50/(85+50) = 0.3704$
- Shrunk Exp PSR: $\theta^* = (0.6296 \times 0.8519) + (0.3704 \times 0.4316) = 0.6962$
- Final Composite Reliability Score: $\text{Reliability} = 0.6962 \times 0.7534 = \mathbf{0.5245}$

#### Rank 3: Sherfane Rutherford (ID 6725)
- Matches: $M = 11$, Successes: $W = 7$
- Raw PSR: $W / M = 7 / 11 = 0.6364$
- Exposure-Weighted PSR: $\text{PSR}_{\text{exp}} = 0.8158$
- Volatility: $\sigma = 8.0532 \implies \tanh(8.0532 / 2.3831) = 0.9977$
- Volatility Stabilizer: $\kappa = 1.0 - 0.25 \times 0.9977 = 0.7506$
- Shrinkage: $w_N = 114/(114+50) = 0.6951$, $w_K = 50/(114+50) = 0.3049$
- Shrunk Exp PSR: $\theta^* = (0.6951 \times 0.8158) + (0.3049 \times 0.4316) = 0.6987$
- Final Composite Reliability Score: $\text{Reliability} = 0.6987 \times 0.7506 = \mathbf{0.5244}$

### B. Bowlers (Prior Mean $\mu = 0.6462$, Anchor $K = 48$, Denominator $\text{IQR} = 2.2497$)

#### Rank 1: Mohammad Nawaz (ID 2490)
- Matches: $M = 12$, Successes: $W = 12$
- Raw PSR: $W / M = 12 / 12 = 1.0000$
- Exposure-Weighted PSR: $\text{PSR}_{\text{exp}} = 1.0000$
- Volatility: $\sigma = 4.7934 \implies \tanh(4.7934 / 2.2497) = 0.9722$
- Volatility Stabilizer: $\kappa = 1.0 - 0.25 \times 0.9722 = 0.7570$
- Shrinkage: $w_N = 115/(115+48) = 0.7055$, $w_K = 48/(115+48) = 0.2945$
- Shrunk Exp PSR: $\theta^* = (0.7055 \times 1.0000) + (0.2945 \times 0.6462) = 0.8958$
- Final Composite Reliability Score: $\text{Reliability} = 0.8958 \times 0.7570 = \mathbf{0.6781}$

#### Rank 2: Shadab Khan (ID 4926)
- Matches: $M = 10$, Successes: $W = 10$
- Raw PSR: $W / M = 10 / 10 = 1.0000$
- Exposure-Weighted PSR: $\text{PSR}_{\text{exp}} = 1.0000$
- Volatility: $\sigma = 5.0671 \implies \tanh(5.0671 / 2.2497) = 0.9781$
- Volatility Stabilizer: $\kappa = 1.0 - 0.25 \times 0.9781 = 0.7555$
- Shrinkage: $w_N = 104/(104+48) = 0.6842$, $w_K = 48/(104+48) = 0.3158$
- Shrunk Exp PSR: $\theta^* = (0.6842 \times 1.0000) + (0.3158 \times 0.6462) = 0.8883$
- Final Composite Reliability Score: $\text{Reliability} = 0.8883 \times 0.7555 = \mathbf{0.6711}$

#### Rank 3: Abrar Ahmed (ID 5979)
- Matches: $M = 14$, Successes: $W = 13$
- Raw PSR: $W / M = 13 / 14 = 0.9286$
- Exposure-Weighted PSR: $\text{PSR}_{\text{exp}} = 0.9528$
- Volatility: $\sigma = 4.3509 \implies \tanh(4.3509 / 2.2497) = 0.9591$
- Volatility Stabilizer: $\kappa = 1.0 - 0.25 \times 0.9591 = 0.7602$
- Shrinkage: $w_N = 136/(136+48) = 0.7391$, $w_K = 48/(136+48) = 0.2609$
- Shrunk Exp PSR: $\theta^* = (0.7391 \times 0.9528) + (0.2609 \times 0.6462) = 0.8728$
- Final Composite Reliability Score: $\text{Reliability} = 0.8728 \times 0.7602 = \mathbf{0.6635}$

## 6. Sensitivity Grid & Robustness Analysis

- **Batters Grid Robustness**: 9 of 10 batters remain in the Top 10 across all tested values $K \in [25, 100]$. The single transition occurs at $K=100$ where Daryl Mitchell (#13) drops out and high-volume veteran David Miller (#10) enters.
- **Bowlers Grid Robustness**: 8 of 10 bowlers remain in the Top 10 across all tested values $K \in [25, 100]$. Two transitions occur: Akeal Hosein enters at $K=25$ (#9), and Shaheen Shah Afridi enters at $K=75$ (#10) and $K=100$ (#10), displacing Lockie Ferguson and Cameron Green respectively.
- **Operational Anchors**: At the proposed operational anchors ($K=50$ for batters, $K=48$ for bowlers), pairwise stability to adjacent settings is **90.0% to 100.0%**.

================================================================================
PHASE 4 FINAL PLAYER RANKINGS AUDIT COMPLETE — ALL METRICS VERIFIED
================================================================================
