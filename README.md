# SupeRR Selector (Season 2)
### Professional IPL Player Pressure & Reliability Analytics Platform

A mathematically rigorous, reproducible cricket analytics platform quantifying match pressure and ranking player reliability in high-leverage situations across the **Indian Premier League (IPL Seasons 2022–2026)**.

---

## 1. Executive Summary & Core Results

**SupeRR Selector** evaluates player execution when matches are on the line. Moving beyond uncontextualized averages and strike rates, the platform models delivery-level leverage ($PI \in [0.0, 1.0]$), benchmarks performance via **Delivery Value Added (DVA)** against expected par, computes exposure-weighted success rates, applies **Empirical Bayes shrinkage** toward IPL cohort priors, and stabilizes rankings against match volatility ($\kappa$).

### Top 10 Most Reliable IPL Batters ($K = 50$, Prior $\mu_{\text{exp}} = 0.4303$)

| Rank | Player Name | IPL Franchise(s) | Pressure Balls | Qual Matches | Raw PSR | Exp PSR | Composite Reliability | Base SR | Press SR | Delta SR |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Rinku Singh** | Kolkata Knight Riders | 191 | 14 | 0.6429 | 0.8263 | **0.5583** | 136.72 | 198.43 | +61.71 |
| **2** | **Dhruv Jurel** | Rajasthan Royals | 92 | 8 | 0.6250 | 0.8090 | **0.5103** | 147.73 | 202.17 | +54.44 |
| **3** | **David Miller** | DC, GT, LSG | 109 | 12 | 0.7500 | 0.7619 | **0.4938** | 134.66 | 214.68 | +80.02 |
| **4** | **Ashutosh Sharma** | DC, PBKS | 116 | 13 | 0.6154 | 0.7193 | **0.4745** | 144.04 | 215.52 | +71.48 |
| **5** | **Tilak Varma** | Mumbai Indians | 81 | 9 | 0.6667 | 0.7500 | **0.4717** | 139.02 | 228.40 | +89.38 |
| **6** | **Tim David** | MI, RCB | 200 | 18 | 0.6111 | 0.6717 | **0.4679** | 174.27 | 185.50 | +11.23 |
| **7** | **Suryakumar Yadav** | Mumbai Indians | 56 | 8 | 0.5000 | 0.7778 | **0.4669** | 164.44 | 176.79 | +12.35 |
| **8** | **Shimron Hetmyer** | Rajasthan Royals | 96 | 11 | 0.5455 | 0.7188 | **0.4659** | 146.48 | 160.42 | +13.94 |
| **9** | **Ayush Badoni** | Lucknow Super Giants | 111 | 10 | 0.5000 | 0.6273 | **0.4252** | 136.69 | 168.47 | +31.78 |
| **10** | **Naman Dhir** | Mumbai Indians | 66 | 7 | 0.4286 | 0.6667 | **0.4244** | 159.95 | 186.36 | +26.42 |

### Top 10 Most Reliable IPL Bowlers ($K = 48$, Prior $\mu_{\text{exp}} = 0.6210$)

| Rank | Player Name | IPL Franchise(s) | Legal Balls | Qual Matches | Raw PSR | Exp PSR | Composite Reliability | Base Econ | Press Econ | Clutch Delta |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Jasprit Bumrah** | Mumbai Indians | 123 | 15 | 0.9333 | 0.9464 | **0.6477** | 7.29 | 5.90 | +1.38 |
| **2** | **Harshit Rana** | Kolkata Knight Riders | 98 | 11 | 0.9091 | 0.9053 | **0.6335** | 9.95 | 7.04 | +2.91 |
| **3** | **Sunil Narine** | Kolkata Knight Riders | 128 | 10 | 0.9000 | 0.8911 | **0.6203** | 6.94 | 5.86 | +1.08 |
| **4** | **Matheesha Pathirana** | CSK, KKR | 158 | 12 | 0.8333 | 0.8716 | **0.6160** | 8.64 | 7.97 | +0.67 |
| **5** | **Shardul Thakur** | CSK, DC, KKR, LSG, MI | 87 | 8 | 0.8750 | 0.8519 | **0.5948** | 10.64 | 8.69 | +1.95 |
| **6** | **Varun Chakravarthy** | Kolkata Knight Riders | 174 | 18 | 0.8333 | 0.8364 | **0.5945** | 8.32 | 7.14 | +1.18 |
| **7** | **Cameron Green** | KKR, MI, RCB | 57 | 6 | 0.8333 | 0.8909 | **0.5806** | 9.55 | 7.58 | +1.97 |
| **8** | **Yash Dayal** | GT, RCB | 78 | 9 | 0.7778 | 0.8182 | **0.5803** | 9.60 | 8.69 | +0.91 |
| **9** | **Suyash Sharma** | KKR, RCB | 124 | 9 | 0.6667 | 0.8257 | **0.5764** | 9.30 | 6.48 | +2.81 |
| **10** | **Lockie Ferguson** | GT, KKR, PBKS, RCB | 76 | 9 | 0.7778 | 0.8088 | **0.5657** | 10.16 | 8.53 | +1.63 |

---

## 2. Interactive Streamlit Dashboard

The platform includes a sports analytics web dashboard built with **Streamlit** and **Plotly**, adhering strictly to light-theme principles (clean white/light-grey backgrounds, dark navy typography, soft blue and muted purple accents, and zero emojis).

### Dashboard Sections:
1. **Overview**: Executive macro metrics (371 IPL matches, 87,687 deliveries, 8,630 high-pressure balls), distribution across pressure tiers, season trends, and showcase podiums for #1 ranked performers.
2. **Rankings**: Separate interactive leaderboards for batters and bowlers with multi-column sorting, franchise filters, toggle for all qualified players (45 batters, 53 bowlers), and instant CSV export.
3. **Player Search**: Complete directory covering all 601 evaluated IPL players. Displays qualification badges (with reasons for unqualification such as sample cutoffs), overall vs pressure statistics, and direct drill-downs.
4. **Batter Analysis**: Comprehensive 5-tab deep-dive studio for any batter:
   - *Tab 1 (Player Overview)*: Metric cards, reliability score gauge, and career vs high-pressure comparison.
   - *Tab 2 (Performance Analysis)*: Strike rate & average comparison, DVA breakdown, empirical delta summary table, phase splits (Powerplay, Middle, Death), and match timeline.
   - *Tab 3 (Player Comparison Studio)*: Side-by-side 2-way and 3-way evaluation across all 341 batters with grouped bars, 6D radar, exposure volume, and phase plots.
   - *Tab 4 (Match Pressure Explorer)*: Over-by-over pressure timeline, run chase progression, and delivery-level DVA inspection table across all 371 IPL matches.
   - *Tab 5 (Player Scouting Report)*: 14-section on-screen dossier with data-driven empirical strengths, tactical limitation audits, and on-demand downloadable 2-page PDF report.
5. **Bowler Analysis**: Symmetrical 5-tab deep-dive studio for any bowler (economy suppression, DVA suppressed, dot ball %, phase comparisons, 2/3-way comparison studio, match pressure explorer, and downloadable PDF scouting report).
6. **Pressure Analysis**: Macro distributions by innings (chase vs target setting), match phases, IPL season trends, team exposure, and top 10 tense death-overs climaxes.
7. **Methodology**: Transparent documentation of the 5-stage mathematical engine, formulas, Bayesian shrinkage parameters, and data limitations.

---

## 3. Running the Dashboard Locally

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### Installation & Launch
```bash
# 1. Clone repository and navigate to root directory
cd "Cricket Pressure Calculator"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit dashboard
streamlit run app/main.py
```
The application will open in your default browser at `http://localhost:8501`.

---

## 4. Deploying to Streamlit Community Cloud & GitHub

The repository is pre-configured for one-click deployment:
1. **Push to GitHub**:
   Ensure `data/processed/ipl_*.csv`, `data/processed/ipl_pressure_overview.json`, `app/`, `src/`, `.streamlit/`, and `requirements.txt` are committed.
2. **Streamlit Community Cloud**:
   - Log in to [share.streamlit.io](https://share.streamlit.io/).
   - Select your GitHub repository, branch (`main`), and set **Main file path** to:
     ```text
     app/main.py
     ```
   - Click **Deploy**.
3. **Configuration**:
   The custom `.streamlit/config.toml` automatically enforces the light theme, fonts, and primary colors in production.

---

## 5. Repository Structure

```text
Cricket_Pressure_Index/
├── .streamlit/
│   └── config.toml                           # Streamlit light-theme configuration
├── app/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py                         # Professional Plotly chart components (bars, radar, timelines)
│   │   ├── kpi_cards.py                      # Reusable KPI, comparison & match overview card components
│   │   └── scouting_report_pdf.py            # Professional 2-page PDF scouting report generator (FPDF2)
│   └── main.py                               # Multi-view Streamlit analytics dashboard (7 pages, 5 internal tabs)
├── data/
│   ├── raw/                                  # Frozen original datasets (6 files)
│   └── processed/                            # Validated pipeline datasets & caches
│       ├── clean_*.csv                       # Frozen standardized master datasets
│       ├── delivery_dva.csv                  # Delivery-level DVA dataset
│       ├── player_match_dva.csv              # Match-level player aggregates
│       ├── ipl_all_players.csv               # All 601 IPL players with stats & ranks
│       ├── ipl_all_player_scores.csv         # Complete Bayesian reliability scores
│       ├── ipl_final_rankings.csv            # Approved Top 10 + Top 10 rankings
│       ├── ipl_matches.csv                   # 371 IPL matches (2022-2026) metadata
│       ├── ipl_deliveries.parquet            # 87,687 ball-by-ball IPL deliveries cache
│       ├── ipl_player_match_history.csv      # Match-by-match history cache
│       ├── ipl_player_phase_breakdown.csv    # Powerplay, Middle, Death phase cache
│       └── ipl_pressure_overview.json        # Macro distributions cache
├── reports/
│   ├── ipl_top10_reliable_batters.csv        # Top 10 IPL Batters CSV
│   ├── ipl_top10_reliable_bowlers.csv        # Top 10 IPL Bowlers CSV
│   ├── ipl_rankings_audit_report.md          # Complete Phase 4 validation audit
│   └── phase5_advanced_scouting_integration_report.md # Phase 5 scouting integration dossier
├── src/
│   ├── dashboard_data.py                     # Cached data access layer for Streamlit
│   ├── ipl_rankings_pipeline.py              # Phase 4 IPL-only recalculation engine
│   ├── prepare_dashboard_data.py             # Dashboard cache generator script
│   ├── feature_engineering.py                # Phase 3B.1 delivery feature pipeline
│   ├── pressure_identification.py            # Phase 3B.2 pressure classifier
│   ├── dva_engine.py                         # Phase 3C DVA calculation engine
│   └── reliability_engine.py                 # Phase 3D reliability scoring engine
├── requirements.txt                          # Python dependencies
└── README.md                                 # Project documentation
```

---

## 6. Future Data Updates Workflow

When a new IPL season concludes:
1. Ingest new raw delivery records into `data/raw/` (or update processed tables).
2. Execute the verified pipeline:
   ```bash
   python src/ipl_rankings_pipeline.py
   python src/prepare_dashboard_data.py
   ```
3. The dashboard caches will refresh automatically without requiring manual UI code alterations. Historical baselines and priors remain versioned and documented.

---
*Developed for the SupeRR Selector Season 2 Competition under the approved Phase 3A Version 2.2 Master Specification.*
