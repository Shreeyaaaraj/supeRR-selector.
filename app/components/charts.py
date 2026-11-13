"""
SupeRR Selector - Premium Plotly Chart Components
=================================================
Designed with a modern pastel sports performance aesthetic:
- Palette: Soft Blue (#F0ECF8, #927CCB), Lavender (#F0ECF8, #927CCB), Deep Purple (#7964B5), Rose (#D58DB5, #F2DCE9)
- Pure white plot backgrounds with minimal gridlines (#ECEAF3)
- Strict compliance with Phase 3A v2.2 approved tiers (Low: < 0.40, Medium: 0.40–0.65, High: >= 0.65). Zero undefined categories.
- Zero emojis anywhere in labels, titles, tooltips, or legends.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

CHART_THEME = dict(
    font=dict(family="'Plus Jakarta Sans', sans-serif", size=12, color="#25233A"),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    margin=dict(l=65, r=25, t=75, b=55),
    title=dict(
        font=dict(family="'Plus Jakarta Sans', sans-serif", size=15, color="#25233A", weight=700),
        x=0.015,
        y=0.94,
        xref='container',
        yref='container',
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="#F0ECF8",
        linecolor="#ECEAF3",
        tickcolor="#ECEAF3",
        tickfont=dict(size=11, color="#77758A"),
        title_font=dict(size=12, color="#25233A", family="'Plus Jakarta Sans', sans-serif"),
        automargin=True
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#F0ECF8",
        linecolor="#ECEAF3",
        tickcolor="#ECEAF3",
        tickfont=dict(size=11, color="#77758A"),
        title_font=dict(size=12, color="#25233A", family="'Plus Jakarta Sans', sans-serif"),
        automargin=True
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=11, color="#77758A"),
        bgcolor="rgba(255,255,255,0.92)"
    )
)


def plot_pressure_tier_distribution(tier_counts, tier_pcts):
    """Bar chart showing delivery volume by approved 3 pressure tiers (Low, Medium, High)."""
    tiers = ['Low (PI < 0.40)', 'Medium (0.40–0.65)', 'High (PI >= 0.65)']
    tier_keys = ['Low', 'Medium', 'High']
    counts = [tier_counts.get(k, 0) for k in tier_keys]
    pcts = [tier_pcts.get(k, 0.0) for k in tier_keys]
    
    bar_colors = ['#F0ECF8', '#927CCB', '#7964B5']
    border_colors = ['#DED6F2', '#927CCB', '#7964B5']
    
    fig = go.Figure(data=[
        go.Bar(
            x=tiers,
            y=counts,
            text=[f"<b>{c:,}</b><br>({p:.1f}%)" for c, p in zip(counts, pcts)],
            textposition='outside',
            marker_color=bar_colors,
            marker_line_color=border_colors,
            marker_line_width=1.5,
            hoverinfo="x+y"
        )
    ])
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Delivery Volume Across Approved Pressure Tiers</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Total deliveries categorized into Low (PI < 0.40), Medium (0.40–0.65), and High (PI >= 0.65)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="Pressure Classification", automargin=True),
        yaxis=dict(title=dict(text="Total Deliveries", standoff=10), range=[0, max(counts) * 1.18], automargin=True),
        height=350,
        margin=dict(l=65, r=25, t=75, b=55)
    )
    return fig


def plot_top10_horizontal_bars(df_top, role):
    """Horizontal bar chart showing top reliable players (up to 15) by Reliability Score."""
    if df_top.empty:
        fig = go.Figure()
        fig.update_layout(CHART_THEME, title="<b>No Players Available to Display</b>")
        return fig

    # Take up to 15 players
    df_plot = df_top.head(15).copy() if len(df_top) > 15 else df_top.copy()
    df_sorted = df_plot.sort_values('final_composite_score', ascending=True).copy()
    n = len(df_sorted)

    is_bat = (role == 'batter')
    if is_bat:
        base_palette = [
            '#FCEEF5', '#F9E2EE', '#F6D4E6', '#F2C5DE', '#EEB5D4',
            '#E8A3C8', '#E190BC', '#D58DB5', '#CA73A1', '#D58DB5'
        ]
        base_borders = [
            '#F2DCE9', '#EDBBD6', '#E5A1C6', '#DC86B5', '#D26CA2',
            '#C55590', '#B7417E', '#A9316E', '#D58DB5', '#8C1B53'
        ]
        title_text = f"Top {n} Reliable Batters Under Pressure" if n != 10 else "Top 10 Reliable Batters Under Pressure"
    else:
        base_palette = [
            '#ECEAF8', '#E4E0F5', '#DAD4F1', '#CEC6EC', '#C0B6E6',
            '#B0A4DF', '#9F90D7', '#927CCB', '#8872C7', '#7964B5'
        ]
        base_borders = [
            '#DDD9F2', '#D1C9EB', '#C1B6E3', '#AF9FDC', '#9C88D3',
            '#8A72CA', '#785DC0', '#6C50B5', '#6044A8', '#54399B'
        ]
        title_text = f"Top {n} Reliable Bowlers Under Pressure" if n != 10 else "Top 10 Reliable Bowlers Under Pressure"

    # Sample n colors dynamically
    if n <= len(base_palette):
        idx_sample = np.linspace(0, len(base_palette) - 1, n, dtype=int)
        bar_colors = [base_palette[i] for i in idx_sample]
        border_colors = [base_borders[i] for i in idx_sample]
    else:
        bar_colors = [base_palette[-1]] * n
        border_colors = [base_borders[-1]] * n

    y_labels = []
    for _, r in df_sorted.iterrows():
        rk = f"Rank {int(r['rank'])}: " if ('rank' in r and pd.notnull(r['rank'])) else ""
        y_labels.append(f"{rk}{r['player_name']}")

    fig = go.Figure(go.Bar(
        y=y_labels,
        x=df_sorted['final_composite_score'],
        orientation='h',
        marker_color=bar_colors,
        marker_line_color=border_colors,
        marker_line_width=1.2,
        text=[f"  <b>{s:.4f}</b>" if pd.notnull(s) else "" for s in df_sorted['final_composite_score']],
        textposition='outside',
        textfont=dict(size=11, color="#25233A", family="'Plus Jakarta Sans', sans-serif"),
        hovertext=[
            f"<b>Rank:</b> {int(rank) if pd.notnull(rank) else 'N/A'}<br><b>Player:</b> {name}<br><b>Reliability Score:</b> {f'{score:.4f}' if pd.notnull(score) else 'N/A'}<br><b>Franchise:</b> {team}<br><b>Exp PSR:</b> {f'{psr*100:.1f}%' if pd.notnull(psr) else 'N/A'}"
            for name, rank, score, team, psr in zip(
                df_sorted['player_name'],
                df_sorted.get('rank', [None]*n),
                df_sorted['final_composite_score'],
                df_sorted.get('ipl_franchises', ['IPL']*n),
                df_sorted.get('exposure_weighted_psr', [None]*n)
            )
        ],
        hoverinfo="text"
    ))

    max_score = df_sorted['final_composite_score'].max() if not df_sorted['final_composite_score'].isna().all() else 0.70
    max_score = 0.70 if pd.isna(max_score) or max_score == 0 else max_score
    calc_height = max(360, 24 * n + 90)

    calc_height = max(380, 26 * n + 90)

    fig.update_layout(
        CHART_THEME,
        title=dict(
            text=f"<b>{title_text}</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Ranked by Final Composite Reliability Score under high-pressure conditions (PI >= 0.65)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis_title="",
        yaxis_title="",
        height=calc_height,
        margin=dict(l=150, r=60, t=75, b=50),
        xaxis=dict(
            range=[0, max_score * 1.18],
            showgrid=True,
            gridcolor="#F0ECF8",
            title=dict(text="Composite Reliability Score", standoff=16, font=dict(size=11.5, color="#4E4A62", family="'Plus Jakarta Sans', sans-serif")),
            automargin=True
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=600),
            automargin=True
        )
    )
    return fig


def plot_reliability_distribution(df_players):
    """Distribution comparison of Reliability Scores for qualified Batters vs Bowlers."""
    df_q = df_players[df_players['is_qualified'] & df_players['final_composite_score'].notnull()].copy()

    bat_scores = df_q[df_q['role'] == 'batter']['final_composite_score']
    bowl_scores = df_q[df_q['role'] == 'bowler']['final_composite_score']

    fig = go.Figure()

    n_bat = len(bat_scores)
    n_bowl = len(bowl_scores)

    fig.add_trace(go.Histogram(
        x=bat_scores,
        name=f"Qualified Batters (N={n_bat})",
        nbinsx=12,
        marker_color="#D58DB5",
        marker_line_color="#D58DB5",
        marker_line_width=1,
        opacity=0.75
    ))

    fig.add_trace(go.Histogram(
        x=bowl_scores,
        name=f"Qualified Bowlers (N={n_bowl})",
        nbinsx=12,
        marker_color="#7964B5",
        marker_line_color="#7964B5",
        marker_line_width=1,
        opacity=0.75
    ))

    fig.add_vline(x=0.4303, line_width=1.8, line_dash="dash", line_color="#D58DB5",
                  annotation_text="Batter Prior (0.4303)", annotation_position="top left",
                  annotation_font=dict(size=10, color="#D58DB5"))
    fig.add_vline(x=0.6210, line_width=1.8, line_dash="dash", line_color="#7964B5",
                  annotation_text="Bowler Prior (0.6210)", annotation_position="top right",
                  annotation_font=dict(size=10, color="#7964B5"))

    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Reliability Score Distribution: Batters vs Bowlers</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Composite Reliability Scores of qualified players compared against Bayesian priors</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis_title="Final Composite Reliability Score",
        yaxis_title="Player Count",
        barmode='overlay',
        height=350,
        margin=dict(l=55, r=25, t=75, b=50)
    )
    return fig

def plot_qualification_summary(overview_data):
    """Stacked bar chart comparing evaluated vs qualified player counts and sample gate attrition."""
    roles = ['IPL Bowlers', 'IPL Batters']
    qualified = [overview_data['qualified_bowlers'], overview_data['qualified_batters']]
    total = [overview_data['total_bowlers_evaluated'], overview_data['total_batters_evaluated']]
    unqualified = [t - q for t, q in zip(total, qualified)]
    rates = [(q / t) * 100 for q, t in zip(qualified, total)]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=roles,
        x=qualified,
        name="Qualified for Reliability Ranking",
        orientation='h',
        marker_color=['#7964B5', '#D58DB5'],
        marker_line_color=['#7964B5', '#D58DB5'],
        marker_line_width=1.2,
        text=[f"<b>{q} Qualified</b> ({r:.1f}%)" for q, r in zip(qualified, rates)],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color="#FFFFFF", size=11, family="'Plus Jakarta Sans', sans-serif")
    ))
    fig.add_trace(go.Bar(
        y=roles,
        x=unqualified,
        name="Insufficient Pressure Sample Volume",
        orientation='h',
        marker_color=['#F0ECF8', '#F2DCE9'],
        marker_line_color=['#DED6F2', '#F2DCE9'],
        marker_line_width=1.2,
        text=[f"<b>{u}</b> ({100-r:.1f}%)" for u, r in zip(unqualified, rates)],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color="#77758A", size=11, family="'Plus Jakarta Sans', sans-serif")
    ))
    
    fig.update_layout(
        CHART_THEME,
        barmode='stack',
        title=dict(
            text="<b>Player Qualification Summary (Phase 3A Sample Gates)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Evaluated vs qualified player counts and sample gate attrition</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis_title="Total Players Evaluated",
        yaxis_title="",
        height=350,
        margin=dict(l=110, r=30, t=75, b=50)
    )
    return fig


def plot_innings_comparison(innings_summary):
    """Grouped bar chart comparing 1st innings target setting vs 2nd innings run chasing."""
    categories = ['1st Innings (Setting Target)', '2nd Innings (Chasing Target)']
    hp_pcts = [innings_summary['1']['pct_high_pressure'], innings_summary['2']['pct_high_pressure']]
    hp_counts = [innings_summary['1']['high_pressure_deliveries'], innings_summary['2']['high_pressure_deliveries']]
    mean_pis = [innings_summary['1']['mean_pi'], innings_summary['2']['mean_pi']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=hp_pcts,
        name="High-Pressure Delivery %",
        marker_color="#927CCB",
        marker_line_color="#7964B5",
        marker_line_width=1.5,
        text=[f"<b>{p:.1f}%</b><br>({c:,} balls)" for p, c in zip(hp_pcts, hp_counts)],
        textposition='outside'
    ))
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>1st vs 2nd Innings High-Pressure Concentration</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Comparison of high-pressure delivery percentage between target setting and run chasing</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="", automargin=True),
        yaxis=dict(title=dict(text="High-Pressure Percentage (%)", standoff=12), range=[0, max(hp_pcts) * 1.30], automargin=True),
        height=350,
        margin=dict(l=65, r=25, t=75, b=55)
    )
    return fig


def plot_match_phase_distribution(phase_summary):
    """Bar chart showing delivery volume and pressure concentration across match phases."""
    phases = ['Powerplay\n(Overs 1–6)', 'Middle\n(Overs 7–15)', 'Death\n(Overs 16–20)']
    phase_keys = ['Powerplay', 'Middle', 'Death']
    
    hp_counts = [phase_summary[k]['high_pressure_deliveries'] for k in phase_keys]
    hp_pcts = [phase_summary[k]['pct_high_pressure'] for k in phase_keys]
    
    colors = ['#F0ECF8', '#927CCB', '#7964B5']
    borders = ['#DED6F2', '#927CCB', '#7964B5']
    
    fig = go.Figure(go.Bar(
        x=phases,
        y=hp_counts,
        marker_color=colors,
        marker_line_color=borders,
        marker_line_width=1.5,
        text=[f"<b>{c:,}</b><br>({p:.1f}%)" for c, p in zip(hp_counts, hp_pcts)],
        textposition='outside'
    ))
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>High-Pressure Deliveries by Match Phase</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>High-pressure delivery volume across Powerplay (1–6), Middle (7–15), and Death (16–20)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title=dict(text="Match Phase", standoff=12), automargin=True),
        yaxis=dict(title=dict(text="High-Pressure Deliveries", standoff=12), range=[0, max(hp_counts) * 1.25], automargin=True),
        height=350,
        margin=dict(l=65, r=25, t=75, b=60)
    )
    return fig


def plot_franchise_representation(df_qualified):
    """Bar chart showing franchise-wise representation of qualified players."""
    franchises = []
    for _, r in df_qualified.iterrows():
        teams = str(r['ipl_franchises']).split(', ')
        for t in teams:
            franchises.append({'franchise': t, 'role': r['role']})
            
    df_fr = pd.DataFrame(franchises)
    if df_fr.empty:
        fig = go.Figure()
        fig.update_layout(CHART_THEME, title="No Franchise Data Available", height=350)
        return fig
        
    counts = df_fr.groupby(['franchise', 'role']).size().unstack(fill_value=0)
    counts['Total'] = counts.sum(axis=1)
    counts = counts.sort_values('Total', ascending=True)
    
    fig = go.Figure()
    if 'batter' in counts.columns:
        fig.add_trace(go.Bar(
            y=counts.index,
            x=counts['batter'],
            name="Batters",
            orientation='h',
            marker_color="#F2DCE9",
            marker_line_color="#D58DB5",
            marker_line_width=1.2
        ))
    if 'bowler' in counts.columns:
        fig.add_trace(go.Bar(
            y=counts.index,
            x=counts['bowler'],
            name="Bowlers",
            orientation='h',
            marker_color="#7964B5",
            marker_line_color="#7964B5",
            marker_line_width=1.2
        ))
        
    fig.update_layout(
        CHART_THEME,
        barmode='stack',
        title=dict(
            text="<b>Franchise-Wise Qualified Players Representation</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Breakdown of qualified batters and bowlers across IPL franchises</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.95,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis_title="Number of Qualified Players",
        yaxis_title="",
        height=400,
        margin=dict(l=170, r=40, t=75, b=50)
    )
    return fig


def plot_phase_comparison(phase_df, role):
    """Grouped bar chart comparing baseline vs high pressure by match phase."""
    phases = ['Powerplay', 'Middle', 'Death']
    df_filtered = phase_df[phase_df['phase'].isin(phases)].copy()
    
    df_filtered['phase_order'] = df_filtered['phase'].map({'Powerplay': 1, 'Middle': 2, 'Death': 3})
    df_filtered = df_filtered.sort_values('phase_order')
    
    is_bat = (role == 'batter')
    metric_label = "Strike Rate" if is_bat else "Economy Rate"
    unit_str = "Runs / 100b" if is_bat else "Runs / Over (Lower is Better)"
    high_press_color = "#D58DB5" if is_bat else "#7964B5"
    high_press_border = "#BD759D" if is_bat else "#65529E"
    
    # Text with ball samples and small-sample flag
    base_texts = []
    base_hovers = []
    for _, r in df_filtered.iterrows():
        v = r.get('overall_metric')
        b = int(r.get('overall_balls', 0)) if pd.notnull(r.get('overall_balls')) else 0
        runs = int(r.get('overall_runs', 0)) if pd.notnull(r.get('overall_runs')) else 0
        if pd.notnull(v) and b > 0:
            base_texts.append(f"<b>{v:.1f}</b><br><span style='font-size:10px;'>({b}b)</span>")
            base_hovers.append(f"<b>Baseline Situation</b><br>Phase: <b>{r['phase']}</b><br>{metric_label}: <b>{v:.2f} {unit_str}</b><br>Runs: <b>{runs}</b><br>Deliveries: <b>{b} balls</b><extra></extra>")
        else:
            base_texts.append("")
            base_hovers.append(f"<b>Baseline Situation</b><br>Phase: <b>{r['phase']}</b><br>No Deliveries<extra></extra>")

    press_texts = []
    press_hovers = []
    for _, r in df_filtered.iterrows():
        v = r.get('pressure_metric')
        b = int(r.get('pressure_balls', 0)) if pd.notnull(r.get('pressure_balls')) else 0
        runs = int(r.get('pressure_runs', 0)) if pd.notnull(r.get('pressure_runs')) else 0
        if pd.notnull(v) and b > 0:
            is_small = (b < 10)
            flag = "*" if is_small else ""
            press_texts.append(f"<b>{v:.1f}{flag}</b><br><span style='font-size:10px;'>({b}b)</span>")
            warn = "<br><span style='color:#E53E3E;'>⚠️ Small sample (< 10 balls)</span>" if is_small else ""
            press_hovers.append(f"<b>High Pressure (PI >= 0.65)</b><br>Phase: <b>{r['phase']}</b><br>{metric_label}: <b>{v:.2f} {unit_str}</b><br>Runs: <b>{runs}</b><br>Deliveries: <b>{b} balls</b>{warn}<extra></extra>")
        else:
            press_texts.append("N/A")
            press_hovers.append(f"<b>High Pressure (PI >= 0.65)</b><br>Phase: <b>{r['phase']}</b><br>No Pressure Deliveries<extra></extra>")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtered['phase'],
        y=df_filtered['overall_metric'],
        name="Baseline Situation",
        marker_color="#F0ECF8",
        marker_line_color="#7964B5",
        marker_line_width=1.2,
        text=base_texts,
        hovertext=base_hovers,
        hoverinfo="text",
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        x=df_filtered['phase'],
        y=df_filtered['pressure_metric'],
        name="High Pressure (PI >= 0.65)",
        marker_color=high_press_color,
        marker_line_color=high_press_border,
        marker_line_width=1.2,
        text=press_texts,
        hovertext=press_hovers,
        hoverinfo="text",
        textposition='outside'
    ))
    
    max_val = max(
        df_filtered['overall_metric'].dropna().max() if not df_filtered['overall_metric'].dropna().empty else 100,
        df_filtered['pressure_metric'].dropna().max() if not df_filtered['pressure_metric'].dropna().empty else 100
    )
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        bargap=0.25,
        bargroupgap=0.10,
        title=dict(
            text=f"<b>{metric_label} Across Match Phases</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Baseline Situation vs High Pressure across Powerplay (1-6), Middle (7-15), and Death (16-20) overs</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(text="Match Phase", standoff=20, font=dict(size=11.5, color="#4E4A62", family="'Plus Jakarta Sans', sans-serif")),
            tickfont=dict(size=11.5, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=600),
            categoryorder='array',
            categoryarray=['Powerplay', 'Middle', 'Death'],
            automargin=True
        ),
        yaxis=dict(
            title=dict(text=f"{metric_label} ({unit_str})", standoff=20, font=dict(size=11.5, color="#25233A", family="'Plus Jakarta Sans', sans-serif")),
            range=[0, max_val * 1.35],
            gridcolor="#F0F1F6",
            linecolor="#ECEAF3",
            automargin=True
        ),
        height=420,
        margin=dict(l=95, r=35, t=130, b=65),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0.01,
            font=dict(size=11, color="#25233A", family="'Plus Jakarta Sans', sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="#ECEAF3",
            borderwidth=1
        )
    )
    return fig


def plot_match_timeline(history_df, role):
    """Timeline bar chart of player net pressure DVA per match with pastel indicator bars."""
    role_str = str(role).lower() if role else ''
    is_bat = (role_str == 'batter')
    is_bowl = (role_str == 'bowler')
    
    if is_bat:
        sub_text = "Net runs contributed under high-pressure deliveries per match"
        y_title = "Pressure DVA (Runs Added)"
        succ_label = "Positive Contribution (Runs Added)"
        fail_label = "Deficit (Runs Below Expectation)"
    elif is_bowl:
        sub_text = "Net runs defended under high-pressure deliveries per match"
        y_title = "Pressure DVA (Runs Defended)"
        succ_label = "Positive Contribution (Runs Defended)"
        fail_label = "Deficit (Runs Conceded Above Expectation)"
    else:
        sub_text = "Net runs contributed or defended under high-pressure deliveries per match"
        y_title = "Pressure DVA (Runs)"
        succ_label = "Positive Contribution"
        fail_label = "Deficit"

    if history_df.empty:
        fig = go.Figure()
        fig.update_layout(
            CHART_THEME,
            title=dict(
                text="<b>No High-Pressure Match Records</b>",
                font=dict(size=14, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
                x=0.02,
                y=0.90,
                xref='container',
                yref='container',
                xanchor='left',
                yanchor='top'
            ),
            height=300
        )
        return fig
        
    df_plot = history_df.sort_values('match_date').copy()
    
    colors = ['#38A169' if succ else '#E53E3E' for succ in df_plot['is_successful_pressure_match']]
    border_colors = ['#276749' if succ else '#9B2C2C' for succ in df_plot['is_successful_pressure_match']]
    
    fig = go.Figure()
    fig.add_hline(y=0, line_dash="solid", line_color="#ECEAF3", line_width=1.5)
    
    fig.add_trace(go.Bar(
        x=df_plot['match_date'],
        y=df_plot['pressure_dva'],
        marker_color=colors,
        marker_line_color=border_colors,
        marker_line_width=1,
        text=df_plot['pressure_dva'].apply(lambda x: f"{x:+.1f}"),
        textposition='outside',
        hovertext=[
            f"<b>Match ID:</b> {m}<br><b>Date:</b> {d}<br><b>Opponent:</b> {opp}<br><b>Pressure DVA:</b> {dva:+.2f}<br><b>Outcome:</b> {succ_label if succ else fail_label}"
            for m, d, opp, dva, succ in zip(df_plot['match_id'], df_plot['match_date'], df_plot['away_team'], df_plot['pressure_dva'], df_plot['is_successful_pressure_match'])
        ],
        hoverinfo="text"
    ))
    
    min_dva = df_plot['pressure_dva'].min()
    max_dva = df_plot['pressure_dva'].max()
    padding = max(abs(min_dva), abs(max_dva)) * 0.28 if max(abs(min_dva), abs(max_dva)) > 0 else 1.0
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text=f"<b>Match-by-Match Pressure Delivery Value Added (DVA)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>{sub_text}</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.02,
            y=0.92,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(
            title=dict(text="Match Date", standoff=10, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#25233A")),
            tickangle=-45,
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=10, color="#4E4A62"),
            automargin=True
        ),
        yaxis=dict(
            title=dict(text=y_title, standoff=14, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#25233A")),
            range=[min_dva - padding, max_dva + padding],
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=10, color="#4E4A62"),
            automargin=True
        ),
        height=360,
        margin=dict(l=80, r=25, t=85, b=65),
        showlegend=False
    )
    return fig


def plot_season_trends(season_summary):
    """Bar trend of high-pressure deliveries across IPL seasons."""
    seasons = sorted(list(season_summary.keys()))
    high_press = [season_summary[s]['high_pressure_deliveries'] for s in seasons]
    pcts = [season_summary[s]['pct_high_pressure'] for s in seasons]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=seasons,
        y=high_press,
        marker_color="#927CCB",
        marker_line_color="#7964B5",
        marker_line_width=1.5,
        text=[f"<b>{hp:,}</b><br>({p:.1f}%)" for hp, p in zip(high_press, pcts)],
        textposition='outside'
    ))
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>High-Pressure Deliveries by IPL Season (2022–2026)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Annual volume and proportion of deliveries bowled under high pressure (PI >= 0.65)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(type='category', title=dict(text="IPL Season", standoff=14), automargin=True),
        yaxis=dict(title=dict(text="High-Pressure Deliveries", standoff=12), range=[0, max(high_press) * 1.20], automargin=True),
        height=350,
        margin=dict(l=65, r=25, t=75, b=60)
    )
    return fig


def plot_team_pressure(team_summary):
    """Horizontal bar chart showing deliveries under pressure by franchise."""
    teams = list(team_summary.keys())
    high_press = [team_summary[t]['high_pressure_deliveries'] for t in teams]
    pcts = [team_summary[t]['pct_high_pressure'] for t in teams]
    
    df_t = pd.DataFrame({'team': teams, 'hp': high_press, 'pct': pcts}).sort_values('hp', ascending=True)
    
    fig = go.Figure(go.Bar(
        y=df_t['team'],
        x=df_t['hp'],
        orientation='h',
        marker_color="#7964B5",
        marker_line_color="#7964B5",
        marker_line_width=1.2,
        text=[f" <b>{h:,}</b> ({p:.1f}%)" for h, p in zip(df_t['hp'], df_t['pct'])],
        textposition='outside'
    ))
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>High-Pressure Deliveries Faced / Bowled by Franchise</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Volume and percentage of deliveries contested under high pressure (PI >= 0.65)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.95,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="Deliveries with PI >= 0.65", range=[0, df_t['hp'].max() * 1.25], automargin=True),
        yaxis=dict(automargin=True),
        height=390,
        margin=dict(l=160, r=40, t=75, b=45)
    )
    return fig


def plot_tense_match_dynamics(tense_situations):
    """Horizontal bar chart showing the highest leverage match finishes by mean death overs pressure."""
    if not tense_situations:
        fig = go.Figure()
        fig.update_layout(CHART_THEME, title="<b>No Tense Situations Recorded</b>")
        return fig
        
    df = pd.DataFrame(tense_situations).head(8).copy()
    df = df.sort_values('death_mean_pi', ascending=True)
    
    labels = [f"{r['home_team']} vs {r['away_team']} ({r['season']})" for _, r in df.iterrows()]
    means = df['death_mean_pi'].tolist()
    balls = df['death_high_press_balls'].tolist()
    
    fig = go.Figure(go.Bar(
        y=labels,
        x=means,
        orientation='h',
        marker_color="#D58DB5",
        marker_line_color="#D58DB5",
        marker_line_width=1.2,
        text=[f" <b>{m:.3f} PI</b> ({b} HP balls)" for m, b in zip(means, balls)],
        textposition='outside'
    ))
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Highest-Leverage Match Finishes (Death Overs Mean PI)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Top matches ranked by average pressure index in the final 5 overs (Overs 16–20)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.95,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="Mean Pressure Index in Death Overs (Overs 16–20)", range=[0, max(means) * 1.25], automargin=True),
        yaxis=dict(automargin=True),
        height=390,
        margin=dict(l=190, r=40, t=75, b=45)
    )
    return fig


def plot_top10_reliability_scatter(df_top, role='batter', highlighted_player_id=None, top_n_labels=5):
    """
    Modern scouting quadrant scatter plot of Pressure Exposure vs Reliability Score.
    ================================================================================
    - X-axis: Pressure Exposure (Balls)
    - Y-axis: Reliability Score
    - Dynamic vertical reference line at median exposure of currently displayed cohort
    - Horizontal reference line at approved Phase 3A cohort prior mean (0.4303 for batters, 0.6210 for bowlers)
    - Four analytical quadrants with subtle background shading:
      * Proven Under Pressure (High Exposure, High Reliability)
      * Promising, Limited Exposure (Low Exposure, High Reliability)
      * Experienced but Inconsistent (High Exposure, Low Reliability)
      * Developing Evidence (Low Exposure, Low Reliability)
    - Player label overlap prevention:
      * Displays text labels for top 5 players by Reliability Score (smart collision-free positioning)
      * Supports highlighting a selected player with an accent marker and bold label
      * All remaining players displayed via interactive rich hover tooltips
      * Small, consistent circular markers (no giant bubbles)
    """
    is_bat = (role == 'batter')
    if 'pressure_exposure_legal_balls' in df_top.columns and not is_bat:
        x_col = 'pressure_exposure_legal_balls'
    elif 'pressure_exposure_balls' in df_top.columns:
        x_col = 'pressure_exposure_balls'
    elif 'pressure_exposure' in df_top.columns:
        x_col = 'pressure_exposure'
    else:
        x_col = 'final_composite_score'
        
    y_col = 'final_composite_score'
    
    df_clean = df_top.dropna(subset=[x_col, y_col]).copy()
    if df_clean.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No player data available for the selected filters.",
            showarrow=False,
            font=dict(size=13, color="#77758A", family="'Plus Jakarta Sans', sans-serif")
        )
        fig.update_layout(
            CHART_THEME,
            height=450,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig
        
    prior_mean = 0.4303 if is_bat else 0.6210
    if len(df_clean) <= 70 and 'is_qualified' in df_clean.columns and df_clean['is_qualified'].sum() > 0:
        median_exposure = float(df_clean[df_clean['is_qualified']][x_col].median())
    else:
        median_exposure = float(df_clean[x_col].median())
    if median_exposure <= 0:
        median_exposure = 1.0

    x_min = 0.0
    x_max = float(max(df_clean[x_col].max() * 1.10, median_exposure * 1.45, 45.0))
    y_min = float(max(0.0, df_clean[y_col].min() * 0.90))
    y_max = float(min(1.0, max(df_clean[y_col].max() * 1.08, prior_mean + 0.16, 0.72)))

    fig = go.Figure()

    # Four subtle quadrant background fills (layer below data points)
    # 1. Promising, Limited Exposure (Top-Left): Soft pink tint
    fig.add_shape(
        type="rect",
        x0=x_min, x1=median_exposure,
        y0=prior_mean, y1=y_max,
        fillcolor="rgba(242, 220, 233, 0.35)",
        line=dict(width=0),
        layer="below"
    )
    # 2. Proven Under Pressure (Top-Right): Very light lavender tint
    fig.add_shape(
        type="rect",
        x0=median_exposure, x1=x_max,
        y0=prior_mean, y1=y_max,
        fillcolor="rgba(240, 236, 248, 0.40)",
        line=dict(width=0),
        layer="below"
    )
    # 3. Developing Evidence (Bottom-Left): Very soft neutral background
    fig.add_shape(
        type="rect",
        x0=x_min, x1=median_exposure,
        y0=y_min, y1=prior_mean,
        fillcolor="rgba(248, 248, 252, 0.50)",
        line=dict(width=0),
        layer="below"
    )
    # 4. Experienced but Inconsistent (Bottom-Right): Soft bluish-lavender tint
    fig.add_shape(
        type="rect",
        x0=median_exposure, x1=x_max,
        y0=y_min, y1=prior_mean,
        fillcolor="rgba(222, 214, 242, 0.30)",
        line=dict(width=0),
        layer="below"
    )

    # Reference Lines
    # Horizontal: Cohort Prior Mean
    fig.add_hline(
        y=prior_mean,
        line_dash="dash",
        line_color="#7964B5",
        line_width=1.5,
        annotation_text=f"Cohort Mean Reliability ({prior_mean:.4f})",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color="#77758A", family="'Plus Jakarta Sans', sans-serif")
    )
    # Vertical: Dynamic Median Exposure of displayed cohort
    fig.add_vline(
        x=median_exposure,
        line_dash="dash",
        line_color="#7964B5",
        line_width=1.5,
        annotation_text=f"Cohort Median Exposure ({median_exposure:.0f} balls)",
        annotation_position="top left",
        annotation_font=dict(size=10, color="#77758A", family="'Plus Jakarta Sans', sans-serif")
    )

    # Quadrant Title Watermarks in four corners
    quadrant_watermarks = [
        dict(
            x=0.02, y=0.97, xref="paper", yref="paper",
            text="<b style='color:#25233A; font-size:11px; letter-spacing:0.02em;'>PROMISING, LIMITED EXPOSURE</b><br><span style='color:#77758A; font-size:9.5px;'>Low Exposure · High Reliability</span>",
            showarrow=False, xanchor="left", yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.85)", bordercolor="#ECEAF3", borderwidth=1, borderpad=5
        ),
        dict(
            x=0.98, y=0.97, xref="paper", yref="paper",
            text="<b style='color:#25233A; font-size:11px; letter-spacing:0.02em;'>PROVEN UNDER PRESSURE</b><br><span style='color:#77758A; font-size:9.5px;'>High Exposure · High Reliability</span>",
            showarrow=False, xanchor="right", yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.85)", bordercolor="#ECEAF3", borderwidth=1, borderpad=5
        ),
        dict(
            x=0.02, y=0.03, xref="paper", yref="paper",
            text="<b style='color:#25233A; font-size:11px; letter-spacing:0.02em;'>DEVELOPING EVIDENCE</b><br><span style='color:#77758A; font-size:9.5px;'>Low Exposure · Low Reliability</span>",
            showarrow=False, xanchor="left", yanchor="bottom",
            bgcolor="rgba(255, 255, 255, 0.85)", bordercolor="#ECEAF3", borderwidth=1, borderpad=5
        ),
        dict(
            x=0.98, y=0.03, xref="paper", yref="paper",
            text="<b style='color:#25233A; font-size:11px; letter-spacing:0.02em;'>EXPERIENCED BUT INCONSISTENT</b><br><span style='color:#77758A; font-size:9.5px;'>High Exposure · Low Reliability</span>",
            showarrow=False, xanchor="right", yanchor="bottom",
            bgcolor="rgba(255, 255, 255, 0.85)", bordercolor="#ECEAF3", borderwidth=1, borderpad=5
        ),
    ]
    for wm in quadrant_watermarks:
        fig.add_annotation(wm)

    def create_hover_text(row):
        name = row['player_name']
        franchise = row.get('ipl_franchises', 'IPL')
        balls = int(row[x_col]) if pd.notnull(row.get(x_col)) else 0
        is_qual = bool(row.get('is_qualified', False))
        raw_score = row.get(y_col)
        rel_val = float(raw_score) if pd.notnull(raw_score) else 0.0

        # Calculate Quadrant
        if balls >= median_exposure and rel_val >= prior_mean:
            quad_name = "Proven Under Pressure"
        elif balls < median_exposure and rel_val >= prior_mean:
            quad_name = "Promising, Limited Exposure"
        elif balls >= median_exposure and rel_val < prior_mean:
            quad_name = "Experienced but Inconsistent"
        else:
            quad_name = "Developing Evidence"

        if pd.notnull(raw_score):
            rel = f"{rel_val:.4f}"
        else:
            rel = "— (Unavailable)"

        if is_qual:
            status_str = "Qualified"
            rank_str = f" • Rank #{int(row['rank'])}" if pd.notnull(row.get('rank')) else ""
        else:
            status_str = "Non-Qualified"
            rank_str = ""

        exp_psr = f"{row['exposure_weighted_psr']:.4f}" if 'exposure_weighted_psr' in row and pd.notnull(row.get('exposure_weighted_psr')) else "N/A"
        raw_psr = f"{row['raw_psr']:.4f}" if 'raw_psr' in row and pd.notnull(row.get('raw_psr')) else "N/A"
        qual_m = int(row['psr_qualifying_matches']) if 'psr_qualifying_matches' in row and pd.notnull(row.get('psr_qualifying_matches')) else int(row.get('pressure_matches', 0))

        return (
            f"<b>{name}</b> ({franchise})<br>"
            f"Qualification Status: <b>{status_str}</b>{rank_str}<br>"
            f"Quadrant: <b>{quad_name}</b><br>"
            f"Pressure Exposure: <b>{balls:,} balls</b><br>"
            f"Reliability Score: <b>{rel}</b><br>"
            f"Exposure-Weighted PSR: <b>{exp_psr}</b><br>"
            f"Unweighted PSR: <b>{raw_psr}</b><br>"
            f"Qualifying Pressure Matches: <b>{qual_m}</b>"
        )

    df_sorted = df_clean.sort_values(y_col, ascending=False).copy()
    top5_df = df_sorted.head(top_n_labels)
    top5_ids = set(top5_df['player_id'])
    
    has_highlight = (highlighted_player_id is not None and highlighted_player_id in df_clean['player_id'].values)
    highlight_row = df_clean[df_clean['player_id'] == highlighted_player_id].iloc[0] if has_highlight else None

    exclude_ids = set(top5_ids)
    if has_highlight:
        exclude_ids.add(highlighted_player_id)
        
    df_cohort_pts = df_clean[~df_clean['player_id'].isin(exclude_ids)].copy()

    # Trace 1: General Cohort Data Points (clean, small circular markers, no text labels)
    if not df_cohort_pts.empty:
        if has_highlight:
            cohort_colors = [
                ("rgba(192, 92, 142, 0.28)" if is_bat else "rgba(121, 100, 181, 0.28)") if q 
                else "rgba(160, 163, 189, 0.18)" 
                for q in df_cohort_pts.get('is_qualified', [True]*len(df_cohort_pts))
            ]
        else:
            cohort_colors = [
                ("rgba(192, 92, 142, 0.70)" if is_bat else "rgba(121, 100, 181, 0.70)") if q 
                else "rgba(160, 163, 189, 0.45)" 
                for q in df_cohort_pts.get('is_qualified', [True]*len(df_cohort_pts))
            ]
        cohort_hover = [create_hover_text(r) for _, r in df_cohort_pts.iterrows()]
        
        fig.add_trace(go.Scatter(
            x=df_cohort_pts[x_col],
            y=df_cohort_pts[y_col],
            mode='markers',
            marker=dict(
                size=7.5,
                color=cohort_colors,
                line=dict(width=1, color="#FFFFFF")
            ),
            hovertext=cohort_hover,
            hoverinfo='text',
            name="Cohort",
            showlegend=False
        ))

    # Trace 2: Top 5 Performers by Reliability (Circular markers + clean labels)
    if not top5_df.empty:
        t5_plot_df = top5_df[top5_df['player_id'] != highlighted_player_id] if has_highlight else top5_df
        if not t5_plot_df.empty:
            t5_hover = [create_hover_text(r) for _, r in t5_plot_df.iterrows()]
            
            label_positions = []
            for _, row in t5_plot_df.iterrows():
                x_val = row[x_col]
                y_val = row[y_col]
                if y_val >= y_max * 0.94:
                    pos = 'bottom right' if x_val < median_exposure else 'bottom left'
                elif x_val >= x_max * 0.85:
                    pos = 'top left'
                elif x_val <= median_exposure * 0.5:
                    pos = 'top right'
                else:
                    pos = 'top center'
                label_positions.append(pos)

            if has_highlight:
                # Keep top 5 visible with reduced opacity, labels suppressed in favor of highlighted player
                fig.add_trace(go.Scatter(
                    x=t5_plot_df[x_col],
                    y=t5_plot_df[y_col],
                    mode='markers',
                    marker=dict(
                        size=8.5,
                        color="rgba(213, 141, 181, 0.40)" if is_bat else "rgba(121, 100, 181, 0.40)",
                        line=dict(width=1, color="#FFFFFF")
                    ),
                    hovertext=t5_hover,
                    hoverinfo='text',
                    name="Top 5 Reliability",
                    showlegend=False
                ))
            else:
                # Default view: full opacity and top-5 labels restored
                fig.add_trace(go.Scatter(
                    x=t5_plot_df[x_col],
                    y=t5_plot_df[y_col],
                    mode='markers+text',
                    text=t5_plot_df['player_name'],
                    textposition=label_positions,
                    textfont=dict(size=11, color="#25233A", family="'Plus Jakarta Sans', sans-serif"),
                    marker=dict(
                        size=9,
                        color="#D58DB5" if is_bat else "#7964B5",
                        line=dict(width=1.5, color="#25233A")
                    ),
                    hovertext=t5_hover,
                    hoverinfo='text',
                    name="Top 5 Reliability",
                    showlegend=False
                ))

    # Trace 3: Selected / Highlighted Player
    if has_highlight and highlight_row is not None:
        hl_hover = [create_hover_text(highlight_row)]
        x_pt = highlight_row[x_col]
        y_pt = highlight_row[y_col]
        
        # Smart positioning for highlighted text
        if y_pt >= y_max * 0.92:
            hl_pos = 'bottom right' if x_pt < median_exposure else 'bottom left'
        elif x_pt >= x_max * 0.85:
            hl_pos = 'top left'
        elif x_pt <= median_exposure * 0.5:
            hl_pos = 'top right'
        else:
            hl_pos = 'top center'
            
        fig.add_trace(go.Scatter(
            x=[x_pt],
            y=[y_pt],
            mode='markers+text',
            text=[f"<b>{highlight_row['player_name']}</b>"],
            textposition=[hl_pos],
            textfont=dict(size=12.5, color="#7964B5", family="'Plus Jakarta Sans', sans-serif"),
            marker=dict(
                size=14,
                color="#F0ECF8",
                line=dict(width=3.5, color="#7964B5")
            ),
            hovertext=hl_hover,
            hoverinfo='text',
            name="Selected Player",
            showlegend=False
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>Scouting Quadrant: Pressure Exposure vs Reliability ({role.capitalize()}s)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Evaluating pressure ball volume against Bayesian-shrunk reliability scores across four performance quadrants</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(
                text="<b>Pressure Exposure (Balls)</b>",
                font=dict(size=12, color="#25233A", family="'Plus Jakarta Sans', sans-serif")
            ),
            range=[x_min, x_max],
            gridcolor="#F0F1F6",
            zeroline=False,
            showline=True,
            linecolor="#ECEAF3",
            tickfont=dict(size=10.5, color="#77758A", family="'Plus Jakarta Sans', sans-serif")
        ),
        yaxis=dict(
            title=dict(
                text="<b>Reliability Score</b>",
                font=dict(size=12, color="#25233A", family="'Plus Jakarta Sans', sans-serif")
            ),
            range=[y_min, y_max],
            gridcolor="#F0F1F6",
            zeroline=False,
            showline=True,
            linecolor="#ECEAF3",
            tickfont=dict(size=10.5, color="#77758A", family="'Plus Jakarta Sans', sans-serif")
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=520,
        margin=dict(l=65, r=40, t=80, b=55),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#ECEAF3",
            font=dict(size=12, color="#25233A", family="'Plus Jakarta Sans', sans-serif")
        )
    )
    return fig


# Alias for convenience and backward compatibility
plot_scouting_quadrant = plot_top10_reliability_scatter


def plot_career_vs_pressure_batter(p_row):
    """Bar comparison of Career/Baseline vs Pressure performance for batters with dual metric groups."""
    base_sr = p_row['baseline_strike_rate'] if pd.notnull(p_row.get('baseline_strike_rate')) else 0.0
    press_sr = p_row['pressure_strike_rate'] if pd.notnull(p_row.get('pressure_strike_rate')) else 0.0
    base_avg = p_row['career_average'] if pd.notnull(p_row.get('career_average')) else 0.0
    press_avg = p_row['pressure_average'] if pd.notnull(p_row.get('pressure_average')) else 0.0
    
    base_bdry = p_row.get('career_boundary_pct', 15.0) if pd.notnull(p_row.get('career_boundary_pct')) else 15.0
    press_bdry = p_row['pressure_boundary_pct'] if pd.notnull(p_row.get('pressure_boundary_pct')) else 0.0
    base_dot = p_row.get('career_dot_pct', 35.0) if pd.notnull(p_row.get('career_dot_pct')) else 35.0
    press_dot = p_row['pressure_dot_pct'] if pd.notnull(p_row.get('pressure_dot_pct')) else 0.0
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "<b>Scoring Pace & Average</b><br><span style='font-size:10.5px; color:#77758A;'>Strike Rate & Batting Average</span>",
            "<b>Ball Distribution & Control</b><br><span style='font-size:10.5px; color:#77758A;'>Boundary % & Dot Ball %</span>"
        ],
        horizontal_spacing=0.20
    )
    
    categories_run = ['Strike Rate', 'Average']
    categories_pct = ['Boundary %', 'Dot Ball %']
    
    fig.add_trace(go.Bar(
        x=categories_run,
        y=[base_sr, base_avg],
        name="Career Baseline",
        marker_color="#F0ECF8",
        marker_line_color="#7964B5",
        marker_line_width=1.2,
        text=[f"<b>{base_sr:.1f}</b>", f"<b>{base_avg:.1f}</b>"],
        textposition='outside',
        hovertemplate="<b>Career Baseline</b><br>%{x}: <b>%{y:.1f}</b><extra></extra>"
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=categories_run,
        y=[press_sr, press_avg],
        name="High Pressure (PI >= 0.65)",
        marker_color="#D58DB5",
        marker_line_color="#BD759D",
        marker_line_width=1.2,
        text=[f"<b>{press_sr:.1f}</b>", f"<b>{press_avg:.1f}</b>" if press_avg > 0 else "N/A"],
        textposition='outside',
        hovertemplate="<b>High Pressure</b><br>%{x}: <b>%{y:.1f}</b><extra></extra>"
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=categories_pct,
        y=[base_bdry, base_dot],
        name="Career Baseline",
        marker_color="#F0ECF8",
        marker_line_color="#7964B5",
        marker_line_width=1.2,
        text=[f"<b>{base_bdry:.1f}%</b>", f"<b>{base_dot:.1f}%</b>"],
        textposition='outside',
        showlegend=False,
        hovertemplate="<b>Career Baseline</b><br>%{x}: <b>%{y:.1f}%</b><extra></extra>"
    ), row=1, col=2)
    fig.add_trace(go.Bar(
        x=categories_pct,
        y=[press_bdry, press_dot],
        name="High Pressure (PI >= 0.65)",
        marker_color="#D58DB5",
        marker_line_color="#BD759D",
        marker_line_width=1.2,
        text=[f"<b>{press_bdry:.1f}%</b>", f"<b>{press_dot:.1f}%</b>"],
        textposition='outside',
        showlegend=False,
        hovertemplate="<b>High Pressure</b><br>%{x}: <b>%{y:.1f}%</b><extra></extra>"
    ), row=1, col=2)
    
    max_run = max(base_sr, press_sr, base_avg, press_avg, 50.0)
    max_pct = max(base_bdry, press_bdry, base_dot, press_dot, 40.0)
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        title=dict(
            text="<b>Career Baseline vs High-Pressure Performance (Batters)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Comparative evaluation across scoring metrics and ball distribution under high pressure (PI >= 0.65)</span>",
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=14.5, color="#25233A", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        height=440,
        margin=dict(l=75, r=35, t=155, b=55),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.18,
            xanchor="center",
            x=0.50,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#25233A"),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#ECEAF3",
            borderwidth=1
        )
    )
    fig.update_yaxes(title=dict(text="Runs (SR: /100b, Avg: /wkt)", standoff=16), range=[0, max_run * 1.30], row=1, col=1)
    fig.update_yaxes(title=dict(text="Percentage of Balls (%)", standoff=16), range=[0, min(100.0, max_pct * 1.30)], row=1, col=2)
    return fig

def plot_career_vs_pressure_bowler(p_row):
    """Bar comparison of Career/Baseline vs Pressure performance for bowlers with dual metric groups."""
    base_econ = p_row['baseline_economy_rate'] if pd.notnull(p_row.get('baseline_economy_rate')) else 0.0
    press_econ = p_row['pressure_economy_rate'] if pd.notnull(p_row.get('pressure_economy_rate')) else 0.0
    base_dot = p_row.get('career_dot_pct', 40.0) if pd.notnull(p_row.get('career_dot_pct')) else 40.0
    press_dot = p_row['pressure_dot_pct'] if pd.notnull(p_row.get('pressure_dot_pct')) else 0.0
    base_bdry = p_row.get('career_boundary_pct', 18.0) if pd.notnull(p_row.get('career_boundary_pct')) else 18.0
    press_bdry = p_row['pressure_boundary_pct'] if pd.notnull(p_row.get('pressure_boundary_pct')) else 0.0
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "<b>Run Restriction</b><br><span style='font-size:10.5px; color:#77758A;'>Economy Rate (Lower is Better)</span>",
            "<b>Delivery Distribution & Control</b><br><span style='font-size:10.5px; color:#77758A;'>Dot Ball % & Boundary % Conceded</span>"
        ],
        horizontal_spacing=0.22
    )
    
    categories_econ = ['Economy Rate']
    categories_pct = ['Dot Ball %', 'Boundary %']
    
    fig.add_trace(go.Bar(
        x=categories_econ,
        y=[base_econ],
        name="Career Baseline",
        marker_color="#F0ECF8",
        marker_line_color="#7964B5",
        marker_line_width=1.2,
        text=[f"<b>{base_econ:.2f}</b>"],
        textposition='outside',
        hovertemplate="<b>Career Baseline</b><br>%{x}: <b>%{y:.2f} RPO</b><extra></extra>"
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=categories_econ,
        y=[press_econ],
        name="High Pressure (PI >= 0.65)",
        marker_color="#7964B5",
        marker_line_color="#65529E",
        marker_line_width=1.2,
        text=[f"<b>{press_econ:.2f}</b>"],
        textposition='outside',
        hovertemplate="<b>High Pressure</b><br>%{x}: <b>%{y:.2f} RPO</b><extra></extra>"
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=categories_pct,
        y=[base_dot, base_bdry],
        name="Career Baseline",
        marker_color="#F0ECF8",
        marker_line_color="#7964B5",
        marker_line_width=1.2,
        text=[f"<b>{base_dot:.1f}%</b>", f"<b>{base_bdry:.1f}%</b>"],
        textposition='outside',
        showlegend=False,
        hovertemplate="<b>Career Baseline</b><br>%{x}: <b>%{y:.1f}%</b><extra></extra>"
    ), row=1, col=2)
    fig.add_trace(go.Bar(
        x=categories_pct,
        y=[press_dot, press_bdry],
        name="High Pressure (PI >= 0.65)",
        marker_color="#7964B5",
        marker_line_color="#65529E",
        marker_line_width=1.2,
        text=[f"<b>{press_dot:.1f}%</b>", f"<b>{press_bdry:.1f}%</b>"],
        textposition='outside',
        showlegend=False,
        hovertemplate="<b>High Pressure</b><br>%{x}: <b>%{y:.1f}%</b><extra></extra>"
    ), row=1, col=2)
    
    max_econ = max(base_econ, press_econ, 8.0)
    max_pct = max(base_dot, press_dot, base_bdry, press_bdry, 45.0)
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        title=dict(
            text="<b>Career Baseline vs High-Pressure Performance (Bowlers)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Comparative evaluation across run restriction and delivery distribution under high pressure (PI >= 0.65)</span>",
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=14.5, color="#25233A", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        height=440,
        margin=dict(l=75, r=35, t=155, b=55),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.18,
            xanchor="center",
            x=0.50,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#25233A"),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#ECEAF3",
            borderwidth=1
        )
    )
    fig.update_yaxes(title=dict(text="Runs / Over (RPO — Lower is Better)", standoff=16), range=[0, max_econ * 1.30], row=1, col=1)
    fig.update_yaxes(title=dict(text="Percentage of Balls (%)", standoff=16), range=[0, min(100.0, max_pct * 1.30)], row=1, col=2)
    return fig

def plot_reliability_gauge(score, rank, is_qualified, role):
    """Horizontal indicator gauge showing player reliability score relative to cohort prior."""
    prior_mean = 0.4303 if role == 'batter' else 0.6210
    
    if is_qualified and pd.notnull(score):
        val = float(score)
        rank_label = f"Rank {int(rank)}" if pd.notnull(rank) else "Qualified"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            number={'valueformat': '.4f', 'font': {'size': 26, 'color': '#25233A', 'family': "'Plus Jakarta Sans', sans-serif"}},
            title={'text': f"<b>Reliability Score ({rank_label})</b><br><span style='font-size:0.75rem; color:#4E4A62; font-weight:500;'>Cohort Prior: {prior_mean:.4f}</span>", 'font': {'size': 13, 'color': '#25233A', 'family': "'Plus Jakarta Sans', sans-serif"}},
            gauge={
                'axis': {'range': [0.0, 1.0], 'tickwidth': 1, 'tickcolor': "#ECEAF3"},
                'bar': {'color': "#7964B5", 'thickness': 0.28},
                'bgcolor': "#FFFFFF",
                'borderwidth': 1,
                'bordercolor': "#ECEAF3",
                'steps': [
                    {'range': [0, prior_mean], 'color': "#F8F8FC"},
                    {'range': [prior_mean, 1.0], 'color': "#F0ECF8"}
                ],
                'threshold': {
                    'line': {'color': "#D58DB5", 'width': 3},
                    'thickness': 0.75,
                    'value': prior_mean
                }
            }
        ))
    else:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=0.0,
            number={'valueformat': '.2f', 'font': {'size': 22, 'color': '#77758A'}},
            title={'text': "<b>Not Qualified for Reliability Ranking</b><br><span style='font-size:0.75rem; color:#D58DB5;'>Insufficient Sample Volume</span>", 'font': {'size': 13, 'color': '#25233A'}},
            gauge={
                'axis': {'range': [0.0, 1.0], 'tickwidth': 1, 'tickcolor': "#ECEAF3"},
                'bar': {'color': "#D58DB5", 'thickness': 0.2},
                'bgcolor': "#FFFFFF",
                'borderwidth': 1,
                'bordercolor': "#ECEAF3"
            }
        ))
        
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        font=dict(family="'Plus Jakarta Sans', sans-serif", color="#25233A"),
        height=220,
        margin=dict(l=30, r=30, t=50, b=20)
    )
    return fig


def plot_batter_strike_rate_chart(p_row):
    """Standalone independent container chart for Batting Strike Rate."""
    base_sr = p_row['baseline_strike_rate'] if pd.notnull(p_row.get('baseline_strike_rate')) else 0.0
    press_sr = p_row['pressure_strike_rate'] if pd.notnull(p_row.get('pressure_strike_rate')) else 0.0
    p_name = p_row.get('player_name', 'Batter')
    max_sr = max(base_sr, press_sr, 50.0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure (PI >= 0.65)"],
        y=[base_sr, press_sr],
        marker_color=["#F0ECF8", "#D58DB5"],
        marker_line_color=["#7964B5", "#BD759D"],
        marker_line_width=1.5,
        text=[f"<b>{base_sr:.1f}</b> SR", f"<b>{press_sr:.1f}</b> SR"],
        textposition="outside",
        hovertemplate=f"<b>{p_name}</b><br>Condition: <b>%{{x}}</b><br>Strike Rate: <b>%{{y:.2f}} Runs / 100 Balls</b><extra></extra>",
        showlegend=False
    ))
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Batting Strike Rate</b><br><span style='font-size: 12px; color: #4E4A62; font-weight: 500;'>Scoring pace: Career Baseline vs High Pressure (Runs per 100 Balls)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="", automargin=True),
        yaxis=dict(title=dict(text="Runs / 100 Balls (SR)", standoff=16), range=[0, max_sr * 1.30], automargin=True),
        height=360,
        margin=dict(l=85, r=35, t=85, b=55)
    )
    return fig

def plot_batter_average_chart(p_row):
    """Standalone independent container chart for Batting Average."""
    base_avg = p_row['career_average'] if pd.notnull(p_row.get('career_average')) else 0.0
    press_avg = p_row['pressure_average'] if pd.notnull(p_row.get('pressure_average')) else 0.0
    p_name = p_row.get('player_name', 'Batter')
    max_avg = max(base_avg, press_avg, 20.0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure (PI >= 0.65)"],
        y=[base_avg, press_avg],
        marker_color=["#F0ECF8", "#D58DB5"],
        marker_line_color=["#7964B5", "#BD759D"],
        marker_line_width=1.5,
        text=[f"<b>{base_avg:.1f}</b>", f"<b>{press_avg:.1f}</b>" if press_avg > 0 else "N/A"],
        textposition="outside",
        hovertemplate=f"<b>{p_name}</b><br>Condition: <b>%{{x}}</b><br>Batting Average: <b>%{{y:.2f}} Runs / Dismissal</b><extra></extra>",
        showlegend=False
    ))
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Batting Average</b><br><span style='font-size: 12px; color: #4E4A62; font-weight: 500;'>Dismissal resistance: Career Baseline vs High Pressure (Runs / Dismissal)</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="", automargin=True),
        yaxis=dict(title=dict(text="Runs / Dismissal (Avg)", standoff=16), range=[0, max_avg * 1.30], automargin=True),
        height=360,
        margin=dict(l=85, r=35, t=85, b=55)
    )
    return fig

def plot_batter_sr_avg_comparison(p_row):
    """Detailed comparison of Strike Rate and Batting Average with dedicated non-compressed axes."""
    base_sr = p_row['baseline_strike_rate'] if pd.notnull(p_row.get('baseline_strike_rate')) else 0.0
    press_sr = p_row['pressure_strike_rate'] if pd.notnull(p_row.get('pressure_strike_rate')) else 0.0
    base_avg = p_row['career_average'] if pd.notnull(p_row.get('career_average')) else 0.0
    press_avg = p_row['pressure_average'] if pd.notnull(p_row.get('pressure_average')) else 0.0
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "<b>Strike Rate</b><br><span style='font-size:10.5px; color:#77758A;'>Runs / 100 Balls</span>",
            "<b>Batting Average</b><br><span style='font-size:10.5px; color:#77758A;'>Runs / Dismissal</span>"
        ],
        horizontal_spacing=0.22
    )
    
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure"],
        y=[base_sr, press_sr],
        marker_color=["#F0ECF8", "#D58DB5"],
        marker_line_color=["#7964B5", "#BD759D"],
        marker_line_width=1.5,
        text=[f"<b>{base_sr:.1f}</b>", f"<b>{press_sr:.1f}</b>"],
        textposition="outside",
        name="Strike Rate",
        showlegend=False
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure"],
        y=[base_avg, press_avg],
        marker_color=["#F0ECF8", "#D58DB5"],
        marker_line_color=["#7964B5", "#BD759D"],
        marker_line_width=1.5,
        text=[f"<b>{base_avg:.1f}</b>", f"<b>{press_avg:.1f}</b>" if press_avg > 0 else "N/A"],
        textposition="outside",
        name="Batting Average",
        showlegend=False
    ), row=1, col=2)
    
    max_sr = max(base_sr, press_sr, 50.0)
    max_avg = max(base_avg, press_avg, 20.0)
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Batting Scoring Pace & Average: Baseline vs High Pressure</b>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        height=410,
        margin=dict(l=85, r=35, t=105, b=55)
    )
    fig.update_yaxes(title=dict(text="Runs / 100 Balls", standoff=16), range=[0, max_sr * 1.30], row=1, col=1)
    fig.update_yaxes(title=dict(text="Runs / Dismissal", standoff=16), range=[0, max_avg * 1.30], row=1, col=2)
    return fig

def plot_bowler_economy_chart(p_row):
    """Standalone independent container chart for Bowling Economy Rate."""
    base_econ = p_row['baseline_economy_rate'] if pd.notnull(p_row.get('baseline_economy_rate')) else 0.0
    press_econ = p_row['pressure_economy_rate'] if pd.notnull(p_row.get('pressure_economy_rate')) else 0.0
    p_name = p_row.get('player_name', 'Bowler')
    max_econ = max(base_econ, press_econ, 6.0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure (PI >= 0.65)"],
        y=[base_econ, press_econ],
        marker_color=["#F0ECF8", "#7964B5"],
        marker_line_color=["#7964B5", "#65529E"],
        marker_line_width=1.5,
        text=[f"<b>{base_econ:.2f}</b> RPO", f"<b>{press_econ:.2f}</b> RPO"],
        textposition="outside",
        hovertemplate=f"<b>{p_name}</b><br>Condition: <b>%{{x}}</b><br>Economy: <b>%{{y:.2f}} Runs / Over</b><br><span style='color:#7964B5;'>Lower is Better</span><extra></extra>",
        showlegend=False
    ))
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Bowling Economy Rate</b><br><span style='font-size: 12px; color: #4E4A62; font-weight: 500;'>Runs conceded per 6 legal balls (Runs / Over) · Lower is Better</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="", automargin=True),
        yaxis=dict(title=dict(text="Runs / Over (RPO — Lower is Better)", standoff=16), range=[0, max_econ * 1.30], automargin=True),
        height=360,
        margin=dict(l=85, r=35, t=85, b=55)
    )
    return fig

def plot_bowler_strike_rate_chart(p_row):
    """Standalone independent container chart for Bowling Strike Rate."""
    career_balls = p_row.get('career_eligible_balls', 0)
    career_wkts = p_row.get('career_dismissals', 0)
    base_sr = (career_balls / career_wkts) if career_wkts > 0 else 0.0
    press_sr = p_row['pressure_strike_rate'] if (pd.notnull(p_row.get('pressure_strike_rate')) and p_row.get('pressure_strike_rate', 0) > 0) else 0.0
    p_name = p_row.get('player_name', 'Bowler')
    max_sr = max(base_sr, press_sr, 15.0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure (PI >= 0.65)"],
        y=[base_sr, press_sr],
        marker_color=["#F0ECF8", "#7964B5"],
        marker_line_color=["#7964B5", "#65529E"],
        marker_line_width=1.5,
        text=[f"<b>{base_sr:.1f}</b> b/w" if base_sr > 0 else "N/A", f"<b>{press_sr:.1f}</b> b/w" if press_sr > 0 else "N/A"],
        textposition="outside",
        hovertemplate=f"<b>{p_name}</b><br>Condition: <b>%{{x}}</b><br>Strike Rate: <b>%{{y:.1f}} Balls / Wicket</b><br><span style='color:#7964B5;'>Lower is Better</span><extra></extra>",
        showlegend=False
    ))
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Bowling Strike Rate</b><br><span style='font-size: 12px; color: #4E4A62; font-weight: 500;'>Legal balls bowled per dismissal (Balls / Wicket) · Lower is Better</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(title="", automargin=True),
        yaxis=dict(title=dict(text="Balls / Wicket (Lower is Better)", standoff=16), range=[0, max_sr * 1.30], automargin=True),
        height=360,
        margin=dict(l=85, r=35, t=85, b=55)
    )
    return fig

def plot_bowler_econ_sr_comparison(p_row):
    """Detailed comparison of Economy Rate and Bowling Strike Rate with dedicated axes."""
    base_econ = p_row['baseline_economy_rate'] if pd.notnull(p_row.get('baseline_economy_rate')) else 0.0
    press_econ = p_row['pressure_economy_rate'] if pd.notnull(p_row.get('pressure_economy_rate')) else 0.0
    
    career_balls = p_row.get('career_eligible_balls', 0)
    career_wkts = p_row.get('career_dismissals', 0)
    base_sr = (career_balls / career_wkts) if career_wkts > 0 else 0.0
    press_sr = p_row['pressure_strike_rate'] if (pd.notnull(p_row.get('pressure_strike_rate')) and p_row.get('pressure_strike_rate', 0) > 0) else 0.0
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "<b>Economy Rate</b><br><span style='font-size:10.5px; color:#77758A;'>Runs / Over (Lower is Better)</span>",
            "<b>Bowling Strike Rate</b><br><span style='font-size:10.5px; color:#77758A;'>Balls / Wicket (Lower is Better)</span>"
        ],
        horizontal_spacing=0.22
    )
    
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure"],
        y=[base_econ, press_econ],
        marker_color=["#F0ECF8", "#7964B5"],
        marker_line_color=["#7964B5", "#65529E"],
        marker_line_width=1.5,
        text=[f"<b>{base_econ:.2f}</b>", f"<b>{press_econ:.2f}</b>"],
        textposition="outside",
        name="Economy Rate",
        showlegend=False
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=["Career Baseline", "High Pressure"],
        y=[base_sr, press_sr],
        marker_color=["#F0ECF8", "#7964B5"],
        marker_line_color=["#7964B5", "#65529E"],
        marker_line_width=1.5,
        text=[f"<b>{base_sr:.1f}</b>" if base_sr > 0 else "N/A", f"<b>{press_sr:.1f}</b>" if press_sr > 0 else "N/A"],
        textposition="outside",
        name="Strike Rate",
        showlegend=False
    ), row=1, col=2)
    
    max_econ = max(base_econ, press_econ, 6.0)
    max_sr = max(base_sr, press_sr, 15.0)
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Bowling Economy & Strike Rate: Baseline vs High Pressure</b>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        height=410,
        margin=dict(l=85, r=35, t=105, b=55)
    )
    fig.update_yaxes(title=dict(text="Runs / Over (RPO — Lower is Better)", standoff=16), range=[0, max_econ * 1.30], row=1, col=1)
    fig.update_yaxes(title=dict(text="Balls / Wicket (Lower is Better)", standoff=16), range=[0, max_sr * 1.30], row=1, col=2)
    return fig

def plot_dva_breakdown(p_row):
    """Visualization of net Delivery Value Added (DVA) in high pressure situations with dual axes."""
    cum_dva = p_row['pressure_cumulative_dva'] if pd.notnull(p_row.get('pressure_cumulative_dva')) else 0.0
    dva_per_ball = p_row['pressure_dva_per_ball'] if pd.notnull(p_row.get('pressure_dva_per_ball')) else 0.0
    
    role = str(p_row.get('role', '')).lower()
    is_bat = (role == 'batter')
    is_bowl = (role == 'bowler')
    
    ball_suffix = "Faced" if is_bat else ("Bowled" if is_bowl else "Faced / Bowled")
    impact_name = "Runs Added" if is_bat else ("Runs Defended" if is_bowl else "Net Runs Impact")
    
    color_cum = '#38A169' if cum_dva >= 0 else '#E53E3E'
    border_cum = '#276749' if cum_dva >= 0 else '#9B2C2C'
    
    color_pb = '#38A169' if dva_per_ball >= 0 else '#E53E3E'
    border_pb = '#276749' if dva_per_ball >= 0 else '#9B2C2C'
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            f"<b>Cumulative Match Pressure DVA ({impact_name})</b>",
            f"<b>DVA per Ball {ball_suffix}</b>"
        ],
        horizontal_spacing=0.16
    )
    
    fig.add_trace(go.Bar(
        x=["Cumulative DVA"],
        y=[cum_dva],
        marker_color=color_cum,
        marker_line_color=border_cum,
        marker_line_width=1.5,
        text=[f"<b>{cum_dva:+.2f} runs</b>"],
        textposition="outside",
        showlegend=False
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=["DVA per Ball"],
        y=[dva_per_ball],
        marker_color=color_pb,
        marker_line_color=border_pb,
        marker_line_width=1.5,
        text=[f"<b>{dva_per_ball:+.3f} / ball</b>"],
        textposition="outside",
        showlegend=False
    ), row=1, col=2)
    
    abs_cum = max(abs(cum_dva), 2.0)
    abs_pb = max(abs(dva_per_ball), 0.10)
    
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Delivery Value Added (DVA): Total Impact & Per-Ball Efficiency</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Cumulative run impact alongside per-ball value added in high-pressure situations</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.02,
            y=0.92,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        height=360,
        margin=dict(l=75, r=35, t=85, b=55)
    )
    fig.update_yaxes(title=dict(text=impact_name, standoff=12), range=[-abs_cum * 1.35, abs_cum * 1.35], row=1, col=1)
    fig.update_yaxes(title=dict(text=f"Runs / Ball {ball_suffix}", standoff=12), range=[-abs_pb * 1.35, abs_pb * 1.35], row=1, col=2)
    return fig

def plot_player_comparison_scoring(players_list, role='batter'):
    """Dedicated chart for Benchmark Section 1: Scoring Pace (Batters) or Run Restriction (Bowlers)."""
    is_bat = (role == 'batter')
    palette = [
        {'bar': '#8872C5', 'line': '#705CA8'},  # Player 1: Bluish purple
        {'bar': '#D58DB5', 'line': '#BD759D'},  # Player 2: Soft rose pink
        {'bar': '#5B4E7E', 'line': '#483D65'}   # Player 3: Deep indigo
    ]
    
    if is_bat:
        title_text = "<b>1. Scoring Pace</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Strike Rate under Baseline vs High-Pressure situations (Runs / 100 Balls)</span>"
        keys = [('Baseline SR', 'baseline_strike_rate', 'Runs / 100b'), ('Pressure SR', 'pressure_strike_rate', 'Runs / 100b')]
        x_title = "Strike Rate (Runs / 100 Balls)"
    else:
        title_text = "<b>1. Run Restriction</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Economy Rate under Baseline vs High-Pressure situations (Runs / Over · Lower is Better)</span>"
        keys = [('Baseline Economy', 'baseline_economy_rate', 'RPO'), ('Pressure Economy', 'pressure_economy_rate', 'RPO')]
        x_title = "Economy Rate (Runs / Over · Lower is Better)"
        
    fig = go.Figure()
    all_vals = []
    
    for idx, p in enumerate(players_list):
        style = palette[idx % len(palette)]
        p_name = p.get('player_name', 'Unknown')
        franchise = str(p.get('ipl_franchises', '')).split(',')[0].strip()
        label_name = f"{p_name} ({franchise})" if franchise else p_name
        
        cats = [k[0] for k in keys]
        vals = []
        texts = []
        hovers = []
        for cat_label, key, unit in keys:
            raw_v = p.get(key)
            if raw_v is not None and pd.notnull(raw_v):
                v = float(raw_v)
                vals.append(v)
                all_vals.append(v)
                fmt_str = f"<b>{v:.1f}</b>" if is_bat else f"<b>{v:.2f}</b>"
                texts.append(fmt_str)
                hovers.append(f"<b>{label_name}</b><br>{cat_label}: <b>{v:.2f} {unit}</b><extra></extra>")
            else:
                vals.append(0.0)
                texts.append("N/A")
                hovers.append(f"<b>{label_name}</b><br>{cat_label}: <b>N/A</b><extra></extra>")
                
        fig.add_trace(go.Bar(
            y=cats,
            x=vals,
            name=label_name,
            orientation='h',
            marker_color=style['bar'],
            marker_line_color=style['line'],
            marker_line_width=1.2,
            text=texts,
            hovertext=hovers,
            hoverinfo="text",
            textposition='outside',
            cliponaxis=False
        ))
        
    max_val = max(all_vals) if all_vals else 100.0
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        bargap=0.25,
        bargroupgap=0.10,
        title=dict(
            text=title_text,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=16, color="#25233A", weight=700),
            x=0.015,
            y=0.92,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(text=x_title, standoff=18, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#4E4A62", weight=600)),
            range=[0, max_val * 1.30],
            gridcolor="#F0F1F6",
            linecolor="#ECEAF3",
            automargin=True
        ),
        yaxis=dict(
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A", weight=600),
            linecolor="#ECEAF3"
        ),
        height=300,
        margin=dict(l=150, r=65, t=75, b=75),
        showlegend=False
    )
    return fig


def plot_player_comparison_control(players_list, role='batter'):
    """Dedicated chart for Benchmark Section 2: Boundary & Control (Batters) or Delivery Control (Bowlers)."""
    is_bat = (role == 'batter')
    palette = [
        {'bar': '#8872C5', 'line': '#705CA8'},  # Player 1: Bluish purple
        {'bar': '#D58DB5', 'line': '#BD759D'},  # Player 2: Soft rose pink
        {'bar': '#5B4E7E', 'line': '#483D65'}   # Player 3: Deep indigo
    ]
    
    if is_bat:
        title_text = "<b>2. Boundary & Control</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>High-Pressure Ball Distribution: Dot Ball % and Boundary %</span>"
        keys = [('Dot Ball %', 'pressure_dot_pct', '%'), ('Boundary %', 'pressure_boundary_pct', '%')]
        x_title = "Percentage of Balls Faced (%)"
    else:
        title_text = "<b>2. Delivery Control</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>High-Pressure Delivery Distribution: Dot Ball % and Boundary % Conceded</span>"
        keys = [('Dot Ball %', 'pressure_dot_pct', '%'), ('Boundary %', 'pressure_boundary_pct', '%')]
        x_title = "Percentage of Balls Bowled (%)"
        
    fig = go.Figure()
    
    for idx, p in enumerate(players_list):
        style = palette[idx % len(palette)]
        p_name = p.get('player_name', 'Unknown')
        franchise = str(p.get('ipl_franchises', '')).split(',')[0].strip()
        label_name = f"{p_name} ({franchise})" if franchise else p_name
        
        cats = [k[0] for k in keys]
        vals = []
        texts = []
        hovers = []
        for cat_label, key, unit in keys:
            raw_v = p.get(key)
            if raw_v is not None and pd.notnull(raw_v):
                v = float(raw_v)
                vals.append(v)
                texts.append(f"<b>{v:.1f}%</b>")
                hovers.append(f"<b>{label_name}</b><br>{cat_label}: <b>{v:.1f}%</b><extra></extra>")
            else:
                vals.append(0.0)
                texts.append("N/A")
                hovers.append(f"<b>{label_name}</b><br>{cat_label}: <b>N/A</b><extra></extra>")
                
        fig.add_trace(go.Bar(
            y=cats,
            x=vals,
            name=label_name,
            orientation='h',
            marker_color=style['bar'],
            marker_line_color=style['line'],
            marker_line_width=1.2,
            text=texts,
            hovertext=hovers,
            hoverinfo="text",
            textposition='outside',
            cliponaxis=False
        ))
        
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        bargap=0.25,
        bargroupgap=0.10,
        title=dict(
            text=title_text,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=16, color="#25233A", weight=700),
            x=0.015,
            y=0.92,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(text=x_title, standoff=18, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#4E4A62", weight=600)),
            range=[0, 100],
            gridcolor="#F0F1F6",
            linecolor="#ECEAF3",
            automargin=True
        ),
        yaxis=dict(
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A", weight=600),
            linecolor="#ECEAF3"
        ),
        height=300,
        margin=dict(l=150, r=65, t=75, b=75),
        showlegend=False
    )
    return fig


def plot_player_comparison_value(players_list, role='batter'):
    """Dedicated chart for Benchmark Section 3: Value Added (Cumulative DVA)."""
    is_bat = (role == 'batter')
    palette = [
        {'bar': '#8872C5', 'line': '#705CA8'},  # Player 1: Bluish purple
        {'bar': '#D58DB5', 'line': '#BD759D'},  # Player 2: Soft rose pink
        {'bar': '#5B4E7E', 'line': '#483D65'}   # Player 3: Deep indigo
    ]
    
    if is_bat:
        title_text = "<b>3. Value Added</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Cumulative Delivery Value Added (DVA) under High Pressure (Runs Added)</span>"
        x_title = "Cumulative Pressure DVA (Runs Added)"
    else:
        title_text = "<b>3. Value Added</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Cumulative Delivery Value Added (DVA) under High Pressure (Runs Defended)</span>"
        x_title = "Cumulative Pressure DVA (Runs Defended)"
        
    fig = go.Figure()
    all_vals = []
    
    for idx, p in enumerate(players_list):
        style = palette[idx % len(palette)]
        p_name = p.get('player_name', 'Unknown')
        franchise = str(p.get('ipl_franchises', '')).split(',')[0].strip()
        label_name = f"{p_name} ({franchise})" if franchise else p_name
        
        raw_v = p.get('pressure_cumulative_dva')
        if raw_v is not None and pd.notnull(raw_v):
            v = float(raw_v)
            val = [v]
            all_vals.append(v)
            text_val = [f"<b>{v:+.1f} r</b>"]
            hover_val = [f"<b>{label_name}</b><br>Cumulative DVA: <b>{v:+.2f} runs</b><extra></extra>"]
        else:
            val = [0.0]
            text_val = ["N/A"]
            hover_val = [f"<b>{label_name}</b><br>Cumulative DVA: <b>N/A</b><extra></extra>"]
            
        fig.add_trace(go.Bar(
            y=['Cumulative DVA'],
            x=val,
            name=label_name,
            orientation='h',
            marker_color=style['bar'],
            marker_line_color=style['line'],
            marker_line_width=1.2,
            text=text_val,
            hovertext=hover_val,
            hoverinfo="text",
            textposition='outside',
            cliponaxis=False
        ))
        
    max_abs = max([abs(v) for v in all_vals]) if all_vals else 15.0
    if max_abs == 0:
        max_abs = 15.0
    x_limit = max_abs * 1.45
    
    has_negative = any(v < 0 for v in all_vals)
    has_positive = any(v > 0 for v in all_vals)
    
    if has_negative and has_positive:
        x_range = [-x_limit, x_limit]
    elif has_negative:
        x_range = [-x_limit, x_limit * 0.12]
    else:
        x_range = [-x_limit * 0.12, x_limit]
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        bargap=0.25,
        bargroupgap=0.10,
        title=dict(
            text=title_text,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=16, color="#25233A", weight=700),
            x=0.015,
            y=0.92,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(text=x_title, standoff=18, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#4E4A62", weight=600)),
            range=x_range,
            zeroline=True,
            zerolinecolor="#25233A",
            zerolinewidth=1.5,
            gridcolor="#F0F1F6",
            linecolor="#ECEAF3",
            automargin=True
        ),
        yaxis=dict(
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A", weight=600),
            linecolor="#ECEAF3"
        ),
        height=300,
        margin=dict(l=150, r=65, t=75, b=75),
        showlegend=False
    )
    return fig


def plot_player_comparison_bars(players_list, role='batter'):
    """Multi-group horizontal bar comparison across 2 or 3 players.
    
    Stacks the 3 benchmark sections vertically into dedicated subplots:
    Row 1: Scoring Pace (Batters) or Run Restriction (Bowlers)
    Row 2: Boundary & Control (Batters) or Delivery Control (Bowlers)
    Row 3: Value Added (Cumulative DVA)
    
    This vertical structure guarantees adequate horizontal space for all axes,
    labels, and categories with zero overlap.
    """
    is_bat = (role == 'batter')
    palette = [
        {'bar': '#8872C5', 'line': '#705CA8'},  # Player 1: Bluish purple
        {'bar': '#D58DB5', 'line': '#BD759D'},  # Player 2: Soft rose pink
        {'bar': '#5B4E7E', 'line': '#483D65'}   # Player 3: Deep indigo
    ]
    
    if is_bat:
        main_title = "Batting Performance Benchmarks (Baseline vs High Pressure)"
        main_sub = "Multi-group comparative benchmark evaluating scoring pace, boundary control, and cumulative value added under pressure."
        sec1_title = "<b>1. Scoring Pace: Strike Rate (Runs / 100 Balls)</b>"
        sec2_title = "<b>2. Boundary & Control: Ball Distribution (%)</b>"
        sec3_title = "<b>3. Value Added: Cumulative DVA (Runs Added)</b>"
        g1_keys = [('Baseline SR', 'baseline_strike_rate', 'Runs / 100b'), ('Pressure SR', 'pressure_strike_rate', 'Runs / 100b')]
        g2_keys = [('Dot Ball %', 'pressure_dot_pct', '%'), ('Boundary %', 'pressure_boundary_pct', '%')]
        g3_keys = [('Cumulative DVA', 'pressure_cumulative_dva', 'runs')]
        x1_title = "Strike Rate (Runs / 100b)"
        x3_title = "Cumulative DVA (Runs Added)"
    else:
        main_title = "Bowling Performance Benchmarks (Baseline vs High Pressure)"
        main_sub = "Multi-group comparative benchmark evaluating run restriction, delivery control, and cumulative value added under pressure."
        sec1_title = "<b>1. Run Restriction: Economy Rate (Runs / Over · Lower is Better)</b>"
        sec2_title = "<b>2. Delivery Control: Dot % & Boundary % Conceded</b>"
        sec3_title = "<b>3. Value Added: Cumulative DVA (Runs Defended)</b>"
        g1_keys = [('Baseline Economy', 'baseline_economy_rate', 'RPO'), ('Pressure Economy', 'pressure_economy_rate', 'RPO')]
        g2_keys = [('Dot Ball %', 'pressure_dot_pct', '%'), ('Boundary %', 'pressure_boundary_pct', '%')]
        g3_keys = [('Cumulative DVA', 'pressure_cumulative_dva', 'runs')]
        x1_title = "Economy Rate (Runs / Over)"
        x3_title = "Cumulative DVA (Runs Defended)"

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=False,
        subplot_titles=[sec1_title, sec2_title, sec3_title],
        vertical_spacing=0.10
    )
    
    g1_vals_all = []
    g3_vals_all = []
    
    for idx, p in enumerate(players_list):
        style = palette[idx % len(palette)]
        p_name = p.get('player_name', 'Unknown')
        franchise = str(p.get('ipl_franchises', '')).split(',')[0].strip()
        label_name = f"{p_name} ({franchise})" if franchise else p_name
        
        # Subplot 1: Scoring / Economy Rates
        cats_1 = [k[0] for k in g1_keys]
        vals_1 = []
        texts_1 = []
        hovers_1 = []
        for cat_label, key, unit in g1_keys:
            raw_v = p.get(key)
            if raw_v is not None and pd.notnull(raw_v):
                v = float(raw_v)
                vals_1.append(v)
                g1_vals_all.append(v)
                fmt_str = f"<b>{v:.1f}</b>" if is_bat else f"<b>{v:.2f}</b>"
                texts_1.append(fmt_str)
                hovers_1.append(f"<b>{label_name}</b><br>{cat_label}: <b>{v:.2f} {unit}</b><extra></extra>")
            else:
                vals_1.append(0.0)
                texts_1.append("N/A")
                hovers_1.append(f"<b>{label_name}</b><br>{cat_label}: <b>N/A</b><extra></extra>")
                
        fig.add_trace(go.Bar(
            y=cats_1,
            x=vals_1,
            name=label_name,
            orientation='h',
            marker_color=style['bar'],
            marker_line_color=style['line'],
            marker_line_width=1.2,
            text=texts_1,
            hovertext=hovers_1,
            hoverinfo="text",
            textposition='outside',
            cliponaxis=False,
            showlegend=True
        ), row=1, col=1)

        # Subplot 2: Boundary & Dot Ball Percentages (%)
        cats_2 = [k[0] for k in g2_keys]
        vals_2 = []
        texts_2 = []
        hovers_2 = []
        for cat_label, key, unit in g2_keys:
            raw_v = p.get(key)
            if raw_v is not None and pd.notnull(raw_v):
                v = float(raw_v)
                vals_2.append(v)
                texts_2.append(f"<b>{v:.1f}%</b>")
                hovers_2.append(f"<b>{label_name}</b><br>{cat_label}: <b>{v:.1f}%</b><extra></extra>")
            else:
                vals_2.append(0.0)
                texts_2.append("N/A")
                hovers_2.append(f"<b>{label_name}</b><br>{cat_label}: <b>N/A</b><extra></extra>")
                
        fig.add_trace(go.Bar(
            y=cats_2,
            x=vals_2,
            name=label_name,
            orientation='h',
            marker_color=style['bar'],
            marker_line_color=style['line'],
            marker_line_width=1.2,
            text=texts_2,
            hovertext=hovers_2,
            hoverinfo="text",
            textposition='outside',
            cliponaxis=False,
            showlegend=False
        ), row=2, col=1)

        # Subplot 3: Cumulative DVA (Runs)
        cats_3 = [k[0] for k in g3_keys]
        vals_3 = []
        texts_3 = []
        hovers_3 = []
        for cat_label, key, unit in g3_keys:
            raw_v = p.get(key)
            if raw_v is not None and pd.notnull(raw_v):
                v = float(raw_v)
                vals_3.append(v)
                g3_vals_all.append(v)
                texts_3.append(f"<b>{v:+.1f} r</b>")
                hovers_3.append(f"<b>{label_name}</b><br>{cat_label}: <b>{v:+.2f} runs</b><extra></extra>")
            else:
                vals_3.append(0.0)
                texts_3.append("N/A")
                hovers_3.append(f"<b>{label_name}</b><br>{cat_label}: <b>N/A</b><extra></extra>")
                
        fig.add_trace(go.Bar(
            y=cats_3,
            x=vals_3,
            name=label_name,
            orientation='h',
            marker_color=style['bar'],
            marker_line_color=style['line'],
            marker_line_width=1.2,
            text=texts_3,
            hovertext=hovers_3,
            hoverinfo="text",
            textposition='outside',
            cliponaxis=False,
            showlegend=False
        ), row=3, col=1)

    max_g1 = max(g1_vals_all) if g1_vals_all else 100.0
    abs_g3 = max([abs(v) for v in g3_vals_all]) if g3_vals_all else 10.0

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        barmode='group',
        bargap=0.25,
        bargroupgap=0.10,
        title=dict(
            text=f"<b>{main_title}</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>{main_sub}</span>",
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=16, color="#25233A", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.01,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A"),
            bgcolor="rgba(255, 255, 255, 0.98)",
            bordercolor="#ECEAF3",
            borderwidth=1
        ),
        height=740,
        margin=dict(l=110, r=55, t=125, b=55)
    )
    
    fig.update_xaxes(
        title=dict(text=x1_title, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#77758A")),
        range=[0, max_g1 * 1.25],
        gridcolor="#F0F1F6", linecolor="#ECEAF3",
        tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=10, color="#77758A"),
        row=1, col=1
    )
    fig.update_xaxes(
        title=dict(text="Percentage of Balls (%)", font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#77758A")),
        range=[0, 105],
        gridcolor="#F0F1F6", linecolor="#ECEAF3",
        tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=10, color="#77758A"),
        row=2, col=1
    )
    fig.update_xaxes(
        title=dict(text=x3_title, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#77758A")),
        range=[-abs_g3 * 1.35, abs_g3 * 1.35],
        zeroline=True, zerolinecolor="#7964B5", zerolinewidth=1.5,
        gridcolor="#F0F1F6", linecolor="#ECEAF3",
        tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=10, color="#77758A"),
        row=3, col=1
    )

    for r in [1, 2, 3]:
        fig.update_yaxes(
            gridcolor="#F0F1F6", linecolor="#ECEAF3",
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=11, color="#25233A", weight=600),
            row=r, col=1
        )

    return fig


def plot_player_comparison_radar(players_list, role='batter'):
    """Radar chart comparing appropriately normalized skill dimensions (0 to 100)."""
    is_bat = (role == 'batter')
    fig = go.Figure()
    
    palette = [
        {'color': '#8872C5', 'fill': 'rgba(136, 114, 197, 0.20)'},  # Player 1
        {'color': '#D58DB5', 'fill': 'rgba(213, 141, 181, 0.20)'},  # Player 2
        {'color': '#5B4E7E', 'fill': 'rgba(91, 78, 126, 0.20)'}     # Player 3
    ]
    
    if is_bat:
        dimensions = [
            ('Pressure SR', 'pressure_strike_rate', 100.0, 200.0, False),
            ('Clutch Delta SR', 'delta_strike_rate', -30.0, 50.0, False),
            ('PSR Success %', 'raw_psr', 0.0, 1.0, False),
            ('DVA per Ball', 'pressure_dva_per_ball', -0.5, 0.5, False),
            ('Boundary %', 'pressure_boundary_pct', 5.0, 35.0, False),
            ('Reliability Score', 'final_composite_score', 0.25, 0.65, False)
        ]
    else:
        dimensions = [
            ('Econ Control', 'pressure_economy_rate', 6.0, 14.0, True),  # Inverted: lower economy is better
            ('Clutch Suppression', 'clutch_econ_suppression', -3.0, 3.0, False),
            ('PSR Success %', 'raw_psr', 0.0, 1.0, False),
            ('DVA per Ball', 'pressure_dva_per_ball', -0.5, 0.5, False),
            ('Dot Ball %', 'pressure_dot_pct', 20.0, 60.0, False),
            ('Reliability Score', 'final_composite_score', 0.35, 0.75, False)
        ]
        
    categories = [d[0] for d in dimensions]
    
    for idx, p in enumerate(players_list):
        style = palette[idx % len(palette)]
        p_name = p['player_name']
        scores = []
        for label, key, min_v, max_v, invert in dimensions:
            raw_v = p.get(key, None)
            if raw_v is None or pd.isna(raw_v):
                scores.append(25.0)  # Default neutral baseline for missing/unqualified metrics
            else:
                val = float(raw_v)
                norm = ((val - min_v) / (max_v - min_v)) * 100.0
                norm = max(5.0, min(100.0, norm))
                if invert:
                    norm = 100.0 - norm + 5.0
                scores.append(norm)
                
        # Close loop
        scores_closed = scores + [scores[0]]
        cat_closed = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=cat_closed,
            fill='toself',
            fillcolor=style['fill'],
            name=f"{p_name}",
            line=dict(color=style['color'], width=2)
        ))
        
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 105], showticklabels=False, linecolor="#ECEAF3", gridcolor="#F0ECF8"),
            angularaxis=dict(tickfont=dict(size=11, color="#25233A"), linecolor="#ECEAF3", gridcolor="#F0ECF8"),
            bgcolor="#FFFFFF"
        ),
        legend=dict(orientation="h", y=-0.15, xanchor="center", x=0.5, font=dict(size=11, color="#77758A")),
        title=dict(
            text="<b>Normalized Pressure Profile Radar (0–100 Benchmark)</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Multi-attribute percentile performance benchmark across core pressure metrics</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.95,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        height=380,
        margin=dict(t=75, b=45, l=40, r=40)
    )
    return fig


def plot_player_comparison_exposure(players_list, role='batter'):
    """Grouped horizontal bar chart comparing career sample vs pressure exposure."""
    is_bat = (role == 'batter')
    fig = go.Figure()
    
    names = [p['player_name'] for p in players_list]
    career_balls = [int(p.get('career_eligible_balls', 0)) for p in players_list]
    press_balls = [int(p.get('pressure_exposure_balls', 0)) for p in players_list]
    qual_matches = [int(p.get('psr_qualifying_matches', p.get('pressure_matches', 0))) for p in players_list]
    
    fig.add_trace(go.Bar(
        y=names,
        x=career_balls,
        name="Career IPL Balls",
        orientation='h',
        marker_color='#F0ECF8',
        marker_line_color='#7964B5',
        marker_line_width=1.2,
        text=[f"{b:,} balls" for b in career_balls],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        y=names,
        x=press_balls,
        name="Pressure Balls (PI >= 0.65)",
        orientation='h',
        marker_color='#8872C5',
        marker_line_color='#705CA8',
        marker_line_width=1.2,
        text=[f"{b:,} balls ({m} qual matches)" for b, m in zip(press_balls, qual_matches)],
        textposition='outside'
    ))
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        title=dict(
            text="<b>Sample Volume & Pressure Exposure Comparison</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Comparison of overall career deliveries faced/bowled versus high-pressure exposure</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis_title="Deliveries",
        yaxis_title="",
        height=300 + len(players_list) * 30,
        margin=dict(l=110, r=40, t=75, b=50)
    )
    return fig


def plot_player_comparison_phase(phase_dfs_dict, role='batter'):
    """Side-by-side phase performance across Powerplay, Middle, and Death."""
    is_bat = (role == 'batter')
    fig = go.Figure()
    
    # Distinct player palette: Player 1: #8872C5, Player 2: #D58DB5
    palette = [
        {'color': '#8872C5', 'border': '#705CA8'},  # Player 1
        {'color': '#D58DB5', 'border': '#BD759D'},  # Player 2
        {'color': '#5B4E7E', 'border': '#483D65'}   # Player 3
    ]
    
    phases = ['Powerplay', 'Middle', 'Death']
    metric_label = "Pressure Strike Rate" if is_bat else "Pressure Economy"
    unit_str = "Runs / 100b" if is_bat else "Runs / Over (Lower is Better)"
    
    all_y_vals = []
    
    for idx, (p_name, df_ph) in enumerate(phase_dfs_dict.items()):
        style = palette[idx % len(palette)]
        val_map = {}
        balls_map = {}
        runs_map = {}
        if not df_ph.empty:
            for _, r in df_ph.iterrows():
                ph = r.get('phase', '')
                val_map[ph] = r.get('pressure_metric')
                balls_map[ph] = int(r.get('pressure_balls', 0)) if pd.notnull(r.get('pressure_balls')) else 0
                runs_map[ph] = int(r.get('pressure_runs', 0)) if pd.notnull(r.get('pressure_runs')) else 0
                
        y_vals = []
        texts = []
        hovers = []
        for ph in phases:
            b = balls_map.get(ph, 0)
            raw_val = val_map.get(ph)
            runs = runs_map.get(ph, 0)
            if b > 0 and raw_val is not None and pd.notnull(raw_val):
                v = float(raw_val)
                y_vals.append(v)
                all_y_vals.append(v)
                is_small = (b < 10)
                flag = "*" if is_small else ""
                texts.append(f"<b>{v:.1f}{flag}</b><br><span style='font-size:10px;'>({b}b)</span>")
                warn_msg = "<br><span style='color:#E53E3E;'>⚠️ Small Sample (< 10 balls) — high variance</span>" if is_small else ""
                hovers.append(
                    f"<b>{p_name}</b><br>"
                    f"Phase: <b>{ph}</b><br>"
                    f"{metric_label}: <b>{v:.2f} {unit_str}</b><br>"
                    f"Pressure Runs: <b>{runs}</b><br>"
                    f"Pressure Balls: <b>{b} balls</b>"
                    f"{warn_msg}"
                    f"<extra></extra>"
                )
            else:
                y_vals.append(0.0)
                texts.append("<span style='font-size:10px; color:#77758A;'>No Sample</span>")
                hovers.append(f"<b>{p_name}</b><br>Phase: <b>{ph}</b><br>No pressure deliveries faced (0 balls)<extra></extra>")
        
        fig.add_trace(go.Bar(
            x=phases,
            y=y_vals,
            name=f"{p_name}",
            marker_color=style['color'],
            marker_line_color=style['border'],
            marker_line_width=1.2,
            text=texts,
            hovertext=hovers,
            hoverinfo="text",
            textposition='outside'
        ))
        
    metric_name = "Pressure Strike Rate" if is_bat else "Pressure Economy Rate"
    
    max_y = max(all_y_vals) if all_y_vals else 100.0
    
    fig.update_layout(
        CHART_THEME,
        barmode='group',
        bargap=0.25,
        bargroupgap=0.10,
        title=dict(
            text=f"<b>Match Phase Breakdown: {metric_name}</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Phase breakdown of high-pressure execution across Powerplay (1-6), Middle (7-15), and Death (16-20) overs</span>",
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=15, color="#25233A", weight=700),
            x=0.015,
            y=0.93,
            xref='container',
            yref='container',
            xanchor="left",
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(text="Match Phase", standoff=20, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#4E4A62")),
            tickfont=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A", weight=600),
            categoryorder='array',
            categoryarray=['Powerplay', 'Middle', 'Death'],
            automargin=True
        ),
        yaxis=dict(
            title=dict(text=f"{metric_label} ({unit_str})", standoff=20, font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A")),
            range=[0, max_y * 1.35],
            gridcolor="#F0F1F6",
            linecolor="#ECEAF3",
            automargin=True
        ),
        height=440,
        margin=dict(l=95, r=35, t=130, b=65),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0.01,
            font=dict(family="'Plus Jakarta Sans', sans-serif", size=11.5, color="#25233A"),
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="#ECEAF3",
            borderwidth=1
        )
    )
    return fig


def plot_match_over_pressure_timeline(df_match_deliveries, match_meta, player_id=None, role='batter'):
    """Over-by-over progression and pressure dynamics for Match Pressure Explorer."""
    if df_match_deliveries.empty:
        fig = go.Figure()
        fig.update_layout(CHART_THEME, title="No deliveries recorded for this match.", height=320)
        return fig
        
    # Aggregate by over and innings
    over_stats = df_match_deliveries.groupby(['innings', 'overid']).agg({
        'delivery_total_runs': 'sum',
        'is_wicket': 'sum',
        'pressure_index': 'mean'
    }).reset_index()
    
    # Check player involvement
    p_overs = set()
    if player_id is not None:
        p_id = int(player_id)
        if role == 'batter':
            p_deliv = df_match_deliveries[df_match_deliveries['striker_id'] == p_id]
        else:
            p_deliv = df_match_deliveries[df_match_deliveries['bowler_id'] == p_id]
        p_overs = set(zip(p_deliv['innings'], p_deliv['overid']))
        
    fig = go.Figure()
    
    # Plot Innings 1 and Innings 2 separately or combined
    innings_list = sorted(over_stats['innings'].unique())
    for inn in innings_list:
        sub = over_stats[over_stats['innings'] == inn].sort_values('overid')
        x_labels = [f"Inn {inn} Ov {ov}" for ov in sub['overid']]
        
        # Color bars by mean pressure tier
        colors = []
        for pi in sub['pressure_index']:
            if pi >= 0.65:
                colors.append('#7964B5')  # High pressure: deep purple
            elif pi >= 0.40:
                colors.append('#927CCB')  # Medium pressure: lavender
            else:
                colors.append('#F0ECF8')  # Low pressure: soft blue
                
        fig.add_trace(go.Bar(
            x=x_labels,
            y=sub['delivery_total_runs'],
            name=f"Innings {inn} Runs",
            marker_color=colors,
            marker_line_color='#25233A',
            marker_line_width=0.8,
            text=[f"{r}r" for r in sub['delivery_total_runs']],
            textposition='outside',
            yaxis='y1'
        ))
        
        # Pressure line on secondary y-axis
        fig.add_trace(go.Scatter(
            x=x_labels,
            y=sub['pressure_index'],
            name=f"Inn {inn} Mean PI",
            mode='lines+markers',
            line=dict(color='#D58DB5' if inn == 2 else '#7964B5', width=2.5),
            marker=dict(size=6),
            yaxis='y2'
        ))
        
        # Wicket markers
        wkt_overs = sub[sub['is_wicket'] > 0]
        if not wkt_overs.empty:
            wkt_x = [f"Inn {inn} Ov {ov}" for ov in wkt_overs['overid']]
            fig.add_trace(go.Scatter(
                x=wkt_x,
                y=wkt_overs['delivery_total_runs'],
                name=f"Inn {inn} Wickets",
                mode='markers',
                marker=dict(symbol='diamond', size=11, color='#E53E3E', line=dict(width=1.5, color='#9B2C2C')),
                text=[f"{int(w)} Wkts" for w in wkt_overs['is_wicket']],
                hoverinfo='text',
                yaxis='y1'
            ))
            
    # Add High Pressure threshold line on y2
    fig.add_hline(y=0.65, line_dash="dash", line_color="#D58DB5", line_width=1.5,
                  annotation_text="High Pressure Gate (PI >= 0.65)", annotation_position="top right", yref="y2")
    
    match_title = f"{match_meta.get('home_team', '')} vs {match_meta.get('away_team', '')} ({match_meta.get('match_date', '')})"
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        title=dict(
            text=f"<b>Over-by-Over Pressure Progression & Runs Scored</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>{match_title}</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.01,
            xref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(showgrid=True, gridcolor="#F0ECF8", tickfont=dict(size=10, color="#77758A"), automargin=True),
        yaxis=dict(title="Runs Scored in Over", showgrid=True, gridcolor="#F0ECF8", title_font=dict(size=12, color="#25233A"), automargin=True),
        yaxis2=dict(title="Mean Pressure Index (PI)", overlaying='y', side='right', range=[0, 1.05], showgrid=False, title_font=dict(size=12, color="#7964B5")),
        legend=dict(orientation="h", y=-0.22, xanchor="center", x=0.5, font=dict(size=10, color="#77758A")),
        height=380,
        margin=dict(l=50, r=50, t=75, b=60)
    )
    return fig


def plot_match_innings_chase_comparison(df_match_deliveries):
    """Cumulative run chase progression and required rate dynamics."""
    if df_match_deliveries.empty:
        fig = go.Figure()
        return fig
        
    fig = go.Figure()
    inn_1 = df_match_deliveries[df_match_deliveries['innings'] == 1].sort_values(['overid', 'over_ball_num'])
    inn_2 = df_match_deliveries[df_match_deliveries['innings'] == 2].sort_values(['overid', 'over_ball_num'])
    
    if not inn_1.empty:
        inn_1 = inn_1.reset_index(drop=True)
        inn_1['ball_seq'] = inn_1.index + 1
        fig.add_trace(go.Scatter(
            x=inn_1['ball_seq'],
            y=inn_1['cum_innings_runs_post'],
            name="1st Innings (Setting Target)",
            line=dict(color='#927CCB', width=2.5)
        ))
        
    if not inn_2.empty:
        inn_2 = inn_2.reset_index(drop=True)
        inn_2['ball_seq'] = inn_2.index + 1
        fig.add_trace(go.Scatter(
            x=inn_2['ball_seq'],
            y=inn_2['cum_innings_runs_post'],
            name="2nd Innings (Run Chase)",
            line=dict(color='#7964B5', width=2.5)
        ))
        
        # Target line
        target = inn_2['target_runs'].iloc[0] if 'target_runs' in inn_2.columns and pd.notnull(inn_2['target_runs'].iloc[0]) else None
        if target:
            fig.add_hline(y=target, line_dash="dash", line_color="#E53E3E", annotation_text=f"Target: {int(target)}", annotation_position="top left")
            
    fig.update_layout(
        CHART_THEME,
        title=dict(
            text="<b>Cumulative Innings Chase Progression</b><br><span style='font-size:12px; color:#4E4A62; font-weight:500;'>Comparative scoring trajectory between 1st innings target setting and 2nd innings run chase</span>",
            font=dict(size=15, color="#25233A", family="'Plus Jakarta Sans', sans-serif", weight=700),
            x=0.015,
            y=0.94,
            xref='container',
            yref='container',
            xanchor='left',
            yanchor='top'
        ),
        xaxis_title="Deliveries Bowled in Innings",
        yaxis_title="Total Runs",
        height=350,
        margin=dict(l=65, r=25, t=75, b=55)
    )
    return fig

