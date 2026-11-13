# SupeRR Selector (Season 2)
### Professional IPL & Senior Men's T20I Player Pressure & Reliability Analytics Platform

A mathematically rigorous, reproducible cricket analytics platform quantifying match pressure and ranking player reliability in high-leverage situations across the **Indian Premier League (IPL Seasons 2022–2026)** and **Senior Men's T20 Internationals (T20Is)**.

---

## 1. Executive Summary & Core Results

**SupeRR Selector** evaluates player execution when matches are on the line. Moving beyond uncontextualized averages and strike rates, the platform models delivery-level leverage (\(PI \in [0.0, 1.0]\)), benchmarks performance via **Delivery Value Added (DVA)** against expected par, computes exposure-weighted success rates, applies empirical shrinkage to account for sample size, and stabilizes rankings against match volatility (\(\kappa\)).

The recruitment evaluation covers **838 unique players and 1,335 player-role evaluations**, combining IPL-only, Senior Men's T20I-only, and players with experience in both formats. The final qualified pool contains **69 batters and 75 bowlers**.

Top 10 Most Reliable Batters — Combined IPL & T20I Rankings
Rank	Player Name	IPL Franchise(s)	Pressure Balls	Qual Matches	Raw PSR	Exp PSR	Composite Reliability	Base SR	Press SR	Delta SR
1	Rinku Singh	Kolkata Knight Riders	194.0	14.5	0.6000	0.8093	0.5490	144.94	194.97	+50.03
2	Sherfane Rutherford	Gujarat Titans, Mumbai Indians, Royal Challengers Bengaluru	85.5	8.0	0.6364	0.8713	0.5319	141.05	201.75	+60.70
3	Dhruv Jurel	Rajasthan Royals	89.0	8.0	0.6250	0.8090	0.5082	144.89	198.94	+54.05
4	Suryakumar Yadav	Mumbai Indians	67.5	9.0	0.6000	0.8222	0.4939	165.47	196.47	+31.00
5	Namboori Tilak Varma	Mumbai Indians	130.0	13.0	0.7059	0.7423	0.4930	139.11	202.76	+63.65
6	Tim David	Mumbai Indians, Royal Challengers Bengaluru	222.5	21.0	0.6667	0.7011	0.4890	173.08	195.58	+22.50
7	Liam Livingstone	Punjab Kings, Royal Challengers Bengaluru, Sunrisers Hyderabad	65.5	7.0	0.6667	0.7939	0.4792	151.09	187.18	+36.09
8	David Miller	Delhi Capitals, Gujarat Titans, Lucknow Super Giants	143.0	15.5	0.5789	0.7063	0.4762	141.00	198.38	+57.38
9	Ashutosh Sharma	Delhi Capitals, Punjab Kings	114.0	13.0	0.6154	0.7193	0.4745	144.04	215.52	+71.48
10	Naman Dhir	Mumbai Indians	84.5	8.5	0.6000	0.7396	0.4688	163.35	206.80	+43.45

Top 10 Most Reliable Bowlers — Combined IPL & T20I Rankings
Rank	Player Name	IPL Franchise(s)	Legal Balls	Qual Matches	Raw PSR	Exp PSR	Composite Reliability	Base Econ	Press Econ	Clutch Delta
1	Jasprit Bumrah	Mumbai Indians	150.0	20.0	0.8400	0.9000	0.6277	6.89	6.47	+0.42
2	Sunil Narine	Kolkata Knight Riders	101.0	10.0	0.9000	0.8911	0.6203	6.85	5.81	+1.04
3	Harshit Rana	Kolkata Knight Riders	108.5	13.0	0.8667	0.8894	0.6144	9.52	7.33	+2.19
4	Shardul Thakur	Chennai Super Kings, Delhi Capitals, Kolkata Knight Riders, Lucknow Super Giants, Mumbai Indians	85.0	8.5	0.8889	0.8588	0.6008	9.93	8.27	+1.66
5	Matheesha Pathirana	Chennai Super Kings, Kolkata Knight Riders	179.0	14.5	0.7647	0.8464	0.5997	8.08	6.62	+1.46
6	Lockie Ferguson	Gujarat Titans, Kolkata Knight Riders, Punjab Kings, Royal Challengers Bengaluru	108.0	13.5	0.8333	0.8472	0.5941	8.63	6.89	+1.74
7	Nathan Ellis	Chennai Super Kings, Punjab Kings	106.5	11.0	0.8235	0.8498	0.5925	7.97	7.70	+0.27
8	Cameron Green	Kolkata Knight Riders, Mumbai Indians, Royal Challengers Bengaluru	61.0	7.0	0.8750	0.9016	0.5913	9.38	6.84	+2.54
9	Varun Chakravarthy	Kolkata Knight Riders	241.0	25.5	0.8182	0.8091	0.5849	7.99	6.85	+1.14
10	Deepak Chahar	Chennai Super Kings, Mumbai Indians	54.0	7.0	0.8889	0.8889	0.5849	8.68	8.83	-0.15

Table Notes
Metric	Explanation
Pressure Balls	Effective batting exposure in high-pressure situations.
Legal Balls	Effective legal bowling exposure in high-pressure situations.
Qual Matches	Effective number of qualifying matches.
Raw PSR	Raw Pressure Success Rate before exposure adjustment.
Exp PSR	Exposure-weighted Pressure Success Rate.
Composite Reliability	Final reliability score used to rank players.
Base SR	Baseline batting strike rate.
Press SR	Batting strike rate in high-pressure situations.
Delta SR	Difference between pressure strike rate and baseline strike rate.
Base Econ	Baseline bowling economy rate.
Press Econ	Bowling economy rate in high-pressure situations.
Clutch Delta	Reduction in economy rate under pressure. A positive value indicates improved economy.
- Pressure Balls / Legal Balls and Qual Matches are effective exposure values. Fractional values can occur because T20I exposure receives a reduced contribution in the combined evaluation.
- Exp PSR represents the exposure-weighted PSR.
- Composite Reliability is the final ranking score.
- For batters, a positive Delta SR indicates a higher strike rate in pressure situations than the baseline.
- For bowlers, Clutch Delta is the reduction in economy rate under pressure. A positive value indicates economy suppression; a negative value indicates a higher pressure economy rate.
- IPL Franchise(s) lists IPL team history, not T20I teams.
- Rankings indicate measured pressure reliability, not current player availability, auction status, price, or guaranteed squad suitability.

---

## 2. Interactive Streamlit Dashboard

The platform includes a sports analytics web dashboard built with **Streamlit** and **Plotly**, adhering to light-theme principles (clean white/light-grey backgrounds, dark navy typography, soft blue and muted purple accents, and no emojis).

### Dashboard Sections:

1. **Overview**: Executive macro metrics, match and delivery coverage, distribution across pressure tiers, season trends, and showcase podiums for top-ranked performers.

2. **Rankings**: Separate interactive leaderboards for batters and bowlers with multi-column sorting, franchise filters, qualified-player views, and CSV export. Rankings use the combined IPL and Senior Men's T20I recruitment evaluation.

3. **Player Search**: Player directory covering the evaluated recruitment pool. Displays qualification status, experience category (IPL-only, T20I-only, or Both), overall versus pressure statistics, and player drill-downs.

4. **Batter Analysis**: Deep-dive analysis for individual batters, including:
   - *Player Overview*: Metric cards, reliability score, and career versus high-pressure comparison.
   - *Performance Analysis*: Strike rate and average comparison, DVA breakdown, empirical delta summary, phase splits (Powerplay, Middle, Death), and match timeline.
   - *Player Comparison Studio*: Side-by-side player evaluation, exposure volume, and phase comparisons.
   - *Match Pressure Explorer*: Over-by-over pressure timeline, run-chase progression, and delivery-level DVA inspection.
   - *Player Scouting Report*: Data-driven strengths, tactical limitation analysis, and downloadable PDF scouting report.

5. **Bowler Analysis**: Deep-dive analysis for individual bowlers, including economy suppression, DVA, dot-ball performance, phase comparisons, player comparison, match pressure exploration, and downloadable PDF scouting reports.

6. **Pressure Analysis**: Macro distributions by innings (chase versus setting a target), match phases, season trends, team exposure, and high-pressure match situations.

7. **Methodology**: Transparent documentation of the pressure identification process, DVA calculation, reliability scoring, shrinkage parameters, qualification criteria, and data limitations.

---

## 3. Running the Dashboard Locally

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### Installation & Launch

```bash
# 1. Clone repository and navigate to the project root
cd "superRR-selector"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit dashboard
streamlit run app/main.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 4. Deploying to Streamlit Community Cloud & GitHub

The repository is configured for deployment through Streamlit Community Cloud.

1. **Push to GitHub**:
   Ensure the application, source code, configuration, requirements, and required processed datasets are committed.

2. **Streamlit Community Cloud**:
   - Log in to [share.streamlit.io](https://share.streamlit.io/).
   - Select your GitHub repository and branch (`main`).
   - Set **Main file path** to:

   ```text
   app/main.py
   ```

   - Click **Deploy**.

3. **Configuration**:
   The `.streamlit/config.toml` file controls the dashboard theme and visual configuration in production.

---

## 5. Repository Structure

```text
superRR-selector/
├── .streamlit/
│   └── config.toml
├── app/
│   ├── components/
│   │   ├── charts.py
│   │   ├── kpi_cards.py
│   │   └── scouting_report_pdf.py
│   └── main.py
├── data/
│   ├── raw/                                  # Original source datasets
│   └── processed/
│       ├── clean_*.csv                       # Standardized master datasets
│       ├── clean_ball_by_ball.csv
│       ├── clean_competitions.csv
│       ├── clean_matches.csv
│       ├── clean_playing_eleven.csv
│       ├── clean_teams.csv
│       ├── delivery_dva.csv
│       ├── engineered_deliveries.csv
│       ├── final_rankings.csv
│       ├── ipl_all_player_scores.csv          # Frozen IPL-only player scores
│       ├── ipl_final_rankings.csv             # Frozen IPL-only rankings
│       ├── model_b_all_player_scores.csv
│       ├── model_b_rankings.csv
│       ├── player_match_dva.csv
│       ├── player_match_pressure.csv
│       ├── player_performance_summary.csv
│       ├── player_reliability_scores.csv
│       ├── pressure_deliveries.csv
│       ├── recruitment_all_players.csv
│       ├── recruitment_all_player_scores.csv  # Combined recruitment player-role scores
│       ├── recruitment_deliveries.parquet
│       ├── recruitment_final_rankings.csv     # Combined recruitment Top 10 rankings
│       ├── recruitment_matches.csv
│       ├── recruitment_player_match_history.csv
│       ├── recruitment_player_phase_breakdown.csv
│       ├── recruitment_pressure_overview.json
│       └── reliability_sensitivity_analysis.csv
├── reports/
│   └──                                      # Analysis and validation reports
├── src/
│   ├── recruitment_pipeline.py
│   └── prepare_dashboard_data.py
├── requirements.txt
└── README.md
```

*The structure above highlights the principal application and processed-data files. Additional source files and generated outputs may be present in the repository.*

---

## 6. Future Data Updates Workflow

When new IPL or Senior Men's T20I data becomes available:

1. Ingest the new raw match and delivery records into the appropriate source-data location.
2. Validate player identifiers, match formats, team metadata, and delivery records.
3. Ensure IPL and T20I records are classified explicitly. Do not treat other competition formats as T20I data.
4. Apply the eligibility and player-exclusion rules consistently before calculating rankings.
5. Execute the verified recruitment pipeline:

   ```bash
   python src/recruitment_pipeline.py
   python src/prepare_dashboard_data.py
   ```

6. Review the generated recruitment rankings, player scores, qualification counts, and dashboard outputs.
7. Test the dashboard locally before committing and pushing changes to GitHub.

The original IPL-only ranking outputs are retained as a frozen historical reference. New combined-format recruitment results are generated separately so that historical IPL-only results are not overwritten.

---

*Developed for the SupeRR Selector Season 2 Competition under the approved Phase 3A Version 2.2 Master Specification.*
