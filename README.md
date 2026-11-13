# SupeRR Selector | Season 2
### Cricket Intelligence Studio — IPL & Senior Men's T20I Recruitment Analytics

**SupeRR Selector** is a cricket analytics and player recruitment platform designed to evaluate player reliability, performance under pressure, and consistency in high-leverage match situations.

The platform combines ball-by-ball data from the **Indian Premier League (IPL Seasons 2022–2026)** and **Senior Men's T20 Internationals (T20Is)** to identify and compare players across three experience categories:

- IPL-only players
- Senior Men's T20I-only players
- Players with experience in both formats

It uses pressure identification, Delivery Value Added (DVA), Pressure Success Rate (PSR), Empirical Bayes shrinkage, and reliability adjustments to support evidence-based player evaluation.

---

## 1. Project Overview

Traditional cricket statistics such as batting average, strike rate and bowling economy do not fully explain how players perform under pressure.

SupeRR Selector addresses this by evaluating player performance in high-leverage situations and comparing execution against format-specific expectations.

The platform provides three complementary analytical models:

| Model | Data used | Purpose |
|---|---|---|
| **Model A — IPL Reference** | IPL performances only | Preserves the original IPL-only V1 baseline |
| **Model B — Pooled Model** | IPL + Senior Men's T20I | Evaluates performance using combined-format evidence |
| **Model C — Recruitment Model** | IPL-primary + T20I-auxiliary | Prioritises IPL evidence while incorporating T20I experience |

**Important:** Model A is the frozen original IPL reference. Players with both IPL and T20I experience are evaluated using their IPL performances only. T20I-only players remain visible in the overall candidate pool but receive N/A for Model A IPL scores.

Model B and Model C expand the evaluation to include T20I-only candidates.

---

## 2. Dataset & Player Coverage

The platform uses processed ball-by-ball cricket data from IPL and Senior Men's T20I competitions.

### Dataset coverage

| Dataset | Match records | Matches with ball-by-ball data | Deliveries |
|---|---:|---:|---:|
| IPL | 371 | 367 | 87,687 |
| Senior Men's T20I | 482 | 470 | 106,327 |
| **Combined** | **853** | **837** | **194,014** |

### Candidate pool

<escape> | Player category | Player-role evaluations |
|---|---:|
| IPL-only | 267 |
| Both IPL and T20I | 353 |
| Senior Men's T20I-only | 715 |
| **Total** | **1,335** |</escape>

**838 unique players** are represented in the combined candidate pool.

Player-role evaluations are calculated independently for batting and bowling. A player can therefore appear in both role categories.

### Candidate eligibility

Model C uses role-specific qualification requirements, including:

- Minimum career ball volume.
- Minimum effective pressure-ball exposure.
- Minimum effective qualifying matches.

The qualification process distinguishes between batting and bowling evaluations. Players can qualify independently in either or both roles.

Pakistani players are excluded from candidate evaluation and rankings using verified player metadata. Performances by eligible non-Pakistani players against Pakistani opposition are retained.

---

## 3. Three Recruitment Models

### Model A — Original IPL Reference Model

Model A preserves the original IPL-only V1 methodology and results.

- Uses IPL performance data only.
- Includes IPL-only and dual-format players who have IPL records.
- Does not assign IPL scores to T20I-only players.
- Keeps original IPL priors, qualification rules, reliability adjustments and scores unchanged.

The original V1 parameters are:

| Parameter | Batters | Bowlers |
|---|---:|---:|
| Shrinkage constant (K) | 50 | 48 |
| IPL prior (μ) | 0.4303 | 0.6210 |

Model A acts as the historical reference against which the expanded recruitment models can be compared.

### Model B — Combined IPL + T20I Model

Model B evaluates players using pooled IPL and Senior Men's T20I evidence.

- Uses verified IPL and Senior Men's T20I records.
- Includes players with experience in either or both formats.
- Uses equal format exposure weighting (λ = 1.00).
- Applies pooled cohort priors and empirical shrinkage.

This model provides a combined-format performance comparison.

### Model C — IPL-Primary Recruitment Model

Model C is the primary recruitment evaluation model.

It gives greater importance to IPL evidence while incorporating T20I performance as additional supporting evidence.

**T20I weighting: λ = 0.50**

Effective exposure:

`N_eff = N_IPL + λ × N_T20I`

Effective success:

`S_eff = N_IPL × PSR_IPL + λ × N_T20I × PSR_T20I`

Effective Pressure Success Rate:

`PSR_eff = S_eff / N_eff`

The resulting rate is shrunk towards the original IPL cohort prior and adjusted for player-match volatility.

This allows T20I-only players to be evaluated without treating their T20I exposure as equivalent to the same volume of IPL exposure.

### Model C qualification requirements

| Requirement | Batters | Bowlers |
|---|---:|---:|
| Minimum career balls | 120 faced | 120 legal balls bowled |
| Minimum effective pressure balls | 40 | 36 |
| Minimum effective qualifying matches | 6 | 6 |

Effective exposure and qualifying matches account for the 0.50 T20I weighting.

---

## 4. Analytical Methodology

### 4.1 Pressure Index (PI)

Each delivery receives a Pressure Index between 0 and 1.

The pressure engine considers:

- Required Run Rate (RRR).
- Wickets remaining.
- Balls remaining.
- Match phase and stage.
- Match situation, including chase and first-innings context.

Pressure categories:

| Category | Pressure Index |
|---|---|
| High Pressure | PI ≥ 0.65 |
| Medium Pressure | 0.40 ≤ PI < 0.65 |
| Low Pressure | PI < 0.40 |

### 4.2 Delivery Value Added (DVA)

DVA measures how much value a player adds or suppresses compared with the expected par performance for the format and match phase.

**Batter DVA**

Evaluates batter runs against expected par scoring, with a dismissal penalty.

**Bowler DVA**

Evaluates runs conceded against expected par economy, with a bonus for bowler-credited wickets.

Format-specific and phase-specific par benchmarks are used.

### 4.3 Pressure Success Rate (PSR)

PSR measures the proportion of qualifying player-match pressure performances that produce positive net DVA.

Pressure exposure is used to weight the success rate, rather than treating every appearance as an identical sample.

### 4.4 Empirical Bayes Shrinkage

Player results are adjusted towards an appropriate cohort prior to reduce the influence of small samples.

This helps avoid overrating players based on a limited number of pressure situations.

### 4.5 Reliability Adjustment

A volatility-based reliability multiplier (κ) adjusts the final score to account for variation in match-level performance.

The purpose is to reward repeatable execution rather than isolated high-pressure performances.

---

## 5. Dashboard Features

The Streamlit dashboard provides an interactive scouting and analytics environment.

### Overview
- Combined tournament context.
- Match and delivery coverage.
- Pressure distributions.
- Player performance highlights.
- Dynamic KPI summaries.

### Rankings
- Batter reliability leaderboard.
- Bowler reliability leaderboard.
- Player rankings and qualification information.
- Search and franchise filters.
- CSV downloads.

### Player Search
- Search across the combined candidate pool.
- IPL-only, T20I-only and dual-format player coverage.
- Player-role evaluation information.
- Qualification and performance details.

### Batter Analysis
- Player performance overview.
- Career versus pressure statistics.
- Strike-rate and average comparisons.
- DVA breakdown.
- Powerplay, middle-overs and death-overs analysis.
- Match-by-match performance history.
- Player scouting dossier and PDF export.

### Bowler Analysis
- Economy and pressure-performance analysis.
- DVA and wicket contributions.
- Phase-wise bowling performance.
- Match history and delivery-level exploration.
- Player comparison and scouting dossier.
- Downloadable PDF report.

### Player Comparison
- Multi-player performance comparison.
- Radar charts.
- Scoring and control metrics.
- Exposure and phase comparisons.

### Pressure Analysis
- Innings-level pressure distributions.
- Match phase analysis.
- Team pressure exposure.
- High-pressure match situations.
- Over-by-over pressure timelines.

### Methodology
- Pressure Index methodology.
- DVA calculations.
- PSR methodology.
- Empirical Bayes shrinkage.
- Reliability adjustment.
- Qualification criteria and model assumptions.

---

## 6. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Analytics | Statistical modelling, Empirical Bayes |
| Visualisation | Plotly |
| Dashboard | Streamlit |
| Data Formats | CSV, JSON, Parquet |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |
| PDF Reporting | Python PDF generation tools |

---

## 7. Repository Structure

```text
supeRR-selector/
│
├── .streamlit/
│   └── config.toml
│
├── app/
│   ├── components/
│   │   ├── charts.py
│   │   ├── kpi_cards.py
│   │   └── scouting_report_pdf.py
│   │
│   └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── clean_*.csv
│       ├── delivery_dva.csv
│       ├── player_match_dva.csv
│       ├── ipl_*.csv
│       ├── model_b_all_player_scores.csv
│       ├── model_b_rankings.csv
│       ├── recruitment_all_player_scores.csv
│       ├── recruitment_all_players.csv
│       ├── recruitment_deliveries.parquet
│       ├── recruitment_final_rankings.csv
│       ├── recruitment_matches.csv
│       ├── recruitment_player_match_history.csv
│       ├── recruitment_player_phase_breakdown.csv
│       └── recruitment_pressure_overview.json
│
├── reports/
│   ├── recruitment_top10_reliable_batters.csv
│   └── recruitment_top10_reliable_bowlers.csv
│
├── src/
│   ├── dashboard_data.py
│   ├── recruitment_pipeline.py
│   ├── ipl_rankings_pipeline.py
│   ├── prepare_dashboard_data.py
│   ├── feature_engineering.py
│   ├── pressure_identification.py
│   ├── dva_engine.py
│   └── reliability_engine.py
│
├── test_implementation.py
├── requirements.txt
└── README.md
```

---

## 8. Run the Dashboard Locally

### Prerequisites
- Python 3.10 or above.
- Git.
- Virtual environment (recommended).

### Installation

Clone the repository:

```bash
git clone https://github.com/Shreeyaaaraj/supeRR-selector.git
cd supeRR-selector
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app/main.py
```

The application will open in your browser, usually at:

`http://localhost:8501`

### Run validation tests

```bash
python test_implementation.py
```

---

## 9. Deployment

The application is deployed through Streamlit Community Cloud.

**GitHub Repository:**  
https://github.com/Shreeyaaaraj/supeRR-selector

**Main branch:** `main`

**Main application file:** `app/main.py`

For future updates:

1. Make and test the changes locally.
2. Run the validation tests.
3. Commit the changes to Git.
4. Push to the `main` branch.
5. Allow Streamlit Community Cloud to redeploy the application.
6. Verify the live dashboard.

---

## 10. Model Governance & Data Integrity

The project maintains separate IPL reference and combined-format recruitment outputs.

Key safeguards include:

- Original Model A V1 results are preserved.
- Model A scores are calculated from IPL data only.
- T20I-only candidates receive N/A for Model A IPL scores.
- Model B and Model C use explicitly verified competition flags.
- Pakistani player IDs are excluded from candidate rankings.
- Eligible non-Pakistani performances against Pakistan are retained.
- Batting and bowling evaluations are maintained independently.
- Automated implementation tests are included in the repository.

---

## 11. Future Scope

Potential future improvements include:

- Additional international T20 competition coverage.
- Enhanced player-role and all-rounder evaluation.
- More advanced player comparison and squad-building tools.
- Tactical matchup and opposition analysis.
- Expanded scouting reports and recruitment insights.
- Automated data ingestion for future seasons.

---

## About the Project

**SupeRR Selector — Season 2** is a cricket intelligence and recruitment analytics project focused on identifying players who consistently deliver when match pressure is highest.

By combining IPL and Senior Men's T20I evidence while preserving an IPL-only reference model, the platform provides a structured approach to pressure-performance evaluation and player recruitment.

**Built with Python, Streamlit, Pandas and Plotly.**

**Repository:** https://github.com/Shreeyaaaraj/supeRR-selector
