"""
SupeRR Selector - Premium KPI Cards, Podiums & Visual Badges
============================================================
Modern, elegant sports analytics UI components adhering to the design system:
- Palette: #F8F8FC background, #FFFFFF cards, #ECEAF3 borders, #25233A text, #77758A secondary
- Accents: Primary purple (#7964B5), Bluish purple (#927CCB), Lavender (#DED6F2), Very light lavender (#F0ECF8), Soft pink (#F2DCE9), Rose (#D58DB5)
- Elegant SVG vector icons (strictly zero emojis)
- Smooth rounded corners (10px) and subtle depth shadows
- Uses st.html with indentation stripping to prevent raw HTML/CSS leakage
"""

import streamlit as st
import pandas as pd

__all__ = [
    'render_html',
    'render_hero_header',
    'metric_card',
    'status_badge',
    'player_header_card',
    'insight_box',
    'render_podium',
    'render_top10_table',
    'render_stats_summary_table',
    'render_scouting_card',
    'render_comparison_summary',
    'render_comparison_data_table',
    'render_match_overview_card'
]


def render_html(html_str: str):
    """Strip all leading line indentation and render HTML natively via st.html,
    preventing CommonMark 4-space code block interpretation and raw text leakage.
    If the content contains global CSS style tags, render via st.markdown(unsafe_allow_html=True)
    to guarantee reliable cascade across all Streamlit containers.
    """
    clean_lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    cleaned = "\n".join(clean_lines)
    if "<style" in cleaned.lower():
        st.markdown(cleaned, unsafe_allow_html=True)
    elif hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)


# SVG Geometric Icons (Zero Emojis)
SVG_ICONS = {
    'chart': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>''',
    'target': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="6" r="2"/></svg>''',
    'pulse': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>''',
    'users': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>''',
    'award': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>''',
    'shield': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>''',
    'activity': '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'''
}

VARIANT_STYLES = {
    'lavender': {
        'badge_bg': '#F0ECF8',
        'badge_color': '#7964B5',
        'border_top': '#927CCB',
        'icon': 'chart'
    },
    'pink': {
        'badge_bg': '#F2DCE9',
        'badge_color': '#D58DB5',
        'border_top': '#D58DB5',
        'icon': 'pulse'
    },
    'blue': {
        'badge_bg': '#F0ECF8',
        'badge_color': '#927CCB',
        'border_top': '#927CCB',
        'icon': 'shield'
    },
    'purple': {
        'badge_bg': '#F0ECF8',
        'badge_color': '#7964B5',
        'border_top': '#7964B5',
        'icon': 'award'
    },
    'rose': {
        'badge_bg': '#F2DCE9',
        'badge_color': '#D58DB5',
        'border_top': '#D58DB5',
        'icon': 'target'
    },
    'neutral': {
        'badge_bg': '#F8F8FC',
        'badge_color': '#77758A',
        'border_top': '#927CCB',
        'icon': 'activity'
    }
}


def render_hero_header(overview_data=None):
    """Render the flagship hero section with clean, sophisticated editorial studio layout."""
    if overview_data is not None and isinstance(overview_data, dict):
        total_m = overview_data.get('total_matches', 853)
        tag_str = "IPL & T20I 2022–2026" if total_m > 371 else "IPL 2022–2026"
        badge_str = f"{total_m:,} Matches · 5 Seasons"
    else:
        tag_str = "IPL 2022–2026"
        badge_str = "371 Matches · 5 Seasons"

    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-top: 3px solid #7964B5; border-radius: 10px; padding: 18px 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #7964B5; margin-bottom: 4px; font-family: 'Plus Jakarta Sans', sans-serif;">
                    CRICKET INTELLIGENCE STUDIO
                </div>
                <h1 style="margin: 0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 1.25; font-family: 'Plus Jakarta Sans', sans-serif;">
                    Read the pressure. Find the performers.
                </h1>
                <div style="font-size: 14.5px; color: #77758A; margin-top: 4px; line-height: 1.45; font-weight: 400; font-family: 'Plus Jakarta Sans', sans-serif;">
                    Discover reliable players when the game is on the line. A smarter way to evaluate cricket performance under pressure.
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: #F8F8FC; color: #77758A; border: 1px solid #ECEAF3; font-size: 12px; font-weight: 500; padding: 5px 12px; border-radius: 6px; font-family: 'Plus Jakarta Sans', sans-serif;">
                    {tag_str}
                </span>
                <span style="background: #F0ECF8; color: #7964B5; border: 1px solid #DED6F2; font-size: 12px; font-weight: 600; padding: 5px 12px; border-radius: 6px; font-family: 'Plus Jakarta Sans', sans-serif;">
                    {badge_str}
                </span>
            </div>
        </div>
    </div>
    """
    render_html(html)

def metric_card(title, value, subtitle=None, delta=None, delta_positive=True, variant='lavender', icon=None):
    """Render a compact, modern SaaS analytics metric card."""
    style = VARIANT_STYLES.get(variant, VARIANT_STYLES['lavender'])
    icon_key = icon if icon in SVG_ICONS else style['icon']
    icon_svg = SVG_ICONS.get(icon_key, SVG_ICONS['chart'])
    
    delta_html = ""
    if delta is not None:
        bg_col = "#EAF7EE" if delta_positive else "#FDF0F0"
        text_col = "#247C44" if delta_positive else "#C53030"
        border_col = "#C9ECCF" if delta_positive else "#F9CFD0"
        prefix = "+" if delta > 0 else ""
        delta_html = f"""
        <div style="display: inline-flex; align-items: center; padding: 2px 7px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; background: {bg_col}; color: {text_col}; border: 1px solid {border_col}; margin-top: 4px; font-family: 'Plus Jakarta Sans', sans-serif;">
            {prefix}{delta} vs Baseline
        </div>
        """
        
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div style="font-size: 0.75rem; color: #77758A; margin-top: 4px; font-weight: 500; font-family: \'Plus Jakarta Sans\', sans-serif;">{subtitle}</div>'
        
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03); min-height: 114px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; transition: transform 0.15s ease, box-shadow 0.15s ease;">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="font-size: 0.70rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #77758A; font-family: 'Plus Jakarta Sans', sans-serif;">
                    {title}
                </div>
                <div style="width: 28px; height: 28px; border-radius: 6px; background: {style['badge_bg']}; color: {style['badge_color']}; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    {icon_svg}
                </div>
            </div>
            <div style="font-size: 1.55rem; font-weight: 700; color: #25233A; margin-top: 4px; line-height: 1.15; letter-spacing: -0.02em; font-family: 'Plus Jakarta Sans', sans-serif;">
                {value}
            </div>
        </div>
        <div>
            {delta_html}
            {subtitle_html}
        </div>
    </div>
    """
    render_html(html)

def status_badge(is_qualified, rank=None, score=None, reasons=None, role=None):
    """Render an elegant qualification status card with pastel highlights."""
    if is_qualified:
        rank_str = f"Rank {int(rank)}" if rank and str(rank) != 'nan' else "Qualified"
        score_str = f"Reliability Score: {score:.4f}" if score and str(score) != 'nan' else ""
        badge_html = f"""
        <div style="background: #FFFFFF; border: 1px solid #D8F0E2; border-left: 4px solid #38A169; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #1F7A4A; background: #E8F7EE; padding: 4px 10px; border-radius: 6px; border: 1px solid #C4ECD4;">
                        Qualified for Reliability Ranking
                    </span>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #1B4D31; margin-top: 8px; letter-spacing: -0.01em;">
                        {rank_str} <span style="font-size: 0.95rem; font-weight: 500; color: #38A169; margin-left: 6px;">• {score_str}</span>
                    </div>
                </div>
                <div style="background: #F4FAF6; border: 1px solid #E1F2E8; border-radius: 6px; padding: 6px 12px; font-size: 0.78rem; color: #2F6F4C; font-weight: 500;">
                    Meets all 3 Phase 3A thresholds (Exposure, Matches, Career Volume)
                </div>
            </div>
        </div>
        """
    else:
        req_text = "40+ pressure balls, 6+ matches, 120+ career balls" if role == 'batter' else "36+ legal pressure balls, 6+ matches, 120+ career balls"
        reasons_clean = reasons if reasons else "Insufficient sample volume under high pressure"
        badge_html = f"""
        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #D58DB5; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #D58DB5; background: #F2DCE9; padding: 4px 10px; border-radius: 6px; border: 1px solid #F2DCE9;">
                        Not Qualified for Reliability Ranking
                    </span>
                    <div style="font-size: 0.92rem; font-weight: 600; color: #25233A; margin-top: 8px;">
                        {reasons_clean}
                    </div>
                </div>
                <div style="background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 6px; padding: 6px 12px; font-size: 0.78rem; color: #77758A; font-weight: 500;">
                    Required: {req_text}
                </div>
            </div>
        </div>
        """
    render_html(badge_html)

def player_header_card(p_row):
    """Render a premium sports player profile header card with pastel badge chips."""
    role_title = p_row['role'].capitalize()
    is_batter = p_row['role'] == 'batter'
    
    # Palette assignment
    role_bg = "#F2DCE9" if is_batter else "#F0ECF8"
    role_text = "#D58DB5" if is_batter else "#7964B5"
    role_border = "#F2DCE9" if is_batter else "#DED6F2"
    accent_bar = "#D58DB5" if is_batter else "#927CCB"
    
    teams = p_row.get('ipl_franchises', 'Unknown')
    seasons = p_row.get('seasons_played', '2022-2026')
    
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-top: 4px solid {accent_bar}; border-radius: 10px; padding: 20px 24px; margin-bottom: 18px; box-shadow: 0 1px 4px rgba(37, 35, 58, 0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="background: {role_bg}; color: {role_text}; border: 1px solid {role_border}; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; padding: 3px 10px; border-radius: 6px;">
                        {role_title} Analytics Profile
                    </span>
                    <span style="background: #F8F8FC; color: #77758A; border: 1px solid #ECEAF3; font-size: 0.72rem; font-weight: 600; padding: 3px 8px; border-radius: 6px;">
                        IPL Seasons: {seasons}
                    </span>
                </div>
                <h1 style="margin: 4px 0 6px 0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em;">
                    {p_row['player_name']}
                </h1>
                <div style="font-size: 0.9rem; color: #77758A; font-weight: 500;">
                    <strong style="color: #25233A;">Franchise(s):</strong> {teams}
                </div>
            </div>
            <div style="text-align: right; background: #F8F8FC; border: 1px solid #ECEAF3; padding: 10px 16px; border-radius: 8px;">
                <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #77758A;">
                    Player Registry ID
                </div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #7964B5; letter-spacing: -0.01em;">
                    ID {p_row['player_id']}
                </div>
            </div>
        </div>
    </div>
    """
    render_html(html)

def insight_box(title, items, variant='lavender'):
    """Render an automated insights card with soft pastel framing."""
    style = VARIANT_STYLES.get(variant, VARIANT_STYLES['lavender'])
    
    list_html = "".join([f'<li style="margin-bottom: 6px; color: #25233A; font-size: 0.88rem; line-height: 1.5;">{it}</li>' for it in items])
    
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid {style['border_top']}; border-radius: 10px; padding: 16px 20px; margin-top: 14px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(37, 35, 58, 0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            <div style="width: 24px; height: 24px; border-radius: 6px; background: {style['badge_bg']}; color: {style['badge_color']}; display: flex; align-items: center; justify-content: center;">
                {SVG_ICONS['chart']}
            </div>
            <h4 style="margin: 0; font-size: 0.98rem; font-weight: 700; color: #25233A;">
                {title}
            </h4>
        </div>
        <ul style="margin: 0; padding-left: 18px;">
            {list_html}
        </ul>
    </div>
    """
    render_html(html)

def render_podium(top3_df, role='batter'):
    """Render an Olympic/sports-style Top 3 podium widget with subtle pastel accents."""
    is_bat = (role == 'batter')
    accent_color = "#D58DB5" if is_bat else "#7964B5"
    pill_bg = "#F2DCE9" if is_bat else "#F0ECF8"
    pill_border = "#F2DCE9" if is_bat else "#DED6F2"
    
    # Sort by rank ascending
    sorted_df = top3_df.sort_values('rank', ascending=True)
    if len(sorted_df) < 3:
        return
        
    p1 = sorted_df.iloc[0]
    p2 = sorted_df.iloc[1]
    p3 = sorted_df.iloc[2]
    
    # Key stat for podium cards
    def get_stat_line(row):
        if is_bat:
            balls = int(row.get('pressure_exposure_balls', row.get('pressure_balls', 0)))
            sr = row.get('pressure_strike_rate', 0.0)
            return f"<strong>{balls}</strong> Balls · <strong>{sr:.1f}</strong> SR"
        else:
            balls = int(row.get('pressure_exposure_legal_balls', row.get('pressure_balls', 0)))
            econ = row.get('pressure_economy_rate', 0.0)
            return f"<strong>{balls}</strong> Balls · <strong>{econ:.2f}</strong> Econ"
            
    stat_p1 = get_stat_line(p1)
    stat_p2 = get_stat_line(p2)
    stat_p3 = get_stat_line(p3)
    
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-radius: 10px; padding: 18px 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(37,35,58,0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div style="font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {accent_color};">
                Top 3 Pressure Podium
            </div>
            <span style="background: {pill_bg}; color: {accent_color}; border: 1px solid {pill_border}; font-size: 0.70rem; font-weight: 700; padding: 2px 8px; border-radius: 6px;">
                {'Anchor K = 50' if is_bat else 'Anchor K = 48'}
            </span>
        </div>
        <div class="podium-grid-container" style="display: grid; grid-template-columns: 1fr 1.12fr 1fr; gap: 10px; align-items: end;">
            <!-- Step 2 (Left) -->
            <div style="background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 8px; padding: 12px 10px; text-align: center;">
                <div style="display: inline-block; background: #ECEAF3; color: #77758A; font-size: 0.68rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-bottom: 6px;">
                    RANK 2
                </div>
                <div style="font-size: 0.96rem; font-weight: 700; color: #25233A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {p2['player_name']}
                </div>
                <div style="font-size: 0.72rem; color: #77758A; margin-top: 2px;">
                    {p2['ipl_franchises'].split(',')[0]}
                </div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #25233A; margin-top: 6px;">
                    {p2['final_composite_score']:.4f}
                </div>
                <div style="font-size: 0.70rem; color: #77758A; margin-top: 4px;">
                    {stat_p2}
                </div>
            </div>
            
            <!-- Step 1 (Center - Elevated) -->
            <div style="background: {pill_bg}; border: 1.5px solid {pill_border}; border-radius: 10px; padding: 16px 12px; text-align: center; box-shadow: 0 2px 8px rgba(121,100,181,0.06); transform: translateY(-4px);">
                <div style="display: inline-block; background: {accent_color}; color: #FFFFFF; font-size: 0.70rem; font-weight: 700; padding: 3px 10px; border-radius: 6px; margin-bottom: 6px; letter-spacing: 0.04em;">
                    RANK 1
                </div>
                <div style="font-size: 1.10rem; font-weight: 700; color: #25233A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {p1['player_name']}
                </div>
                <div style="font-size: 0.75rem; color: #77758A; margin-top: 2px; font-weight: 500;">
                    {p1['ipl_franchises'].split(',')[0]}
                </div>
                <div style="font-size: 1.45rem; font-weight: 700; color: {accent_color}; margin-top: 6px;">
                    {p1['final_composite_score']:.4f}
                </div>
                <div style="font-size: 0.74rem; color: #25233A; margin-top: 4px;">
                    {stat_p1}
                </div>
            </div>
            
            <!-- Step 3 (Right) -->
            <div style="background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 8px; padding: 12px 10px; text-align: center;">
                <div style="display: inline-block; background: #ECEAF3; color: #77758A; font-size: 0.68rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-bottom: 6px;">
                    RANK 3
                </div>
                <div style="font-size: 0.96rem; font-weight: 700; color: #25233A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {p3['player_name']}
                </div>
                <div style="font-size: 0.72rem; color: #77758A; margin-top: 2px;">
                    {p3['ipl_franchises'].split(',')[0]}
                </div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #25233A; margin-top: 6px;">
                    {p3['final_composite_score']:.4f}
                </div>
                <div style="font-size: 0.70rem; color: #77758A; margin-top: 4px;">
                    {stat_p3}
                </div>
            </div>
        </div>
    </div>
    """
    render_html(html)

def render_top10_table(df_top, role):
    """Render a compact, elegant leaderboard table for the Top 10 Batters or Bowlers."""
    is_bat = (role == 'batter')
    primary_color = "#D58DB5" if is_bat else "#7964B5"
    badge_bg_1 = "#F2DCE9" if is_bat else "#F0ECF8"
    badge_col_1 = "#D58DB5" if is_bat else "#7964B5"
    badge_bor_1 = "#F2DCE9" if is_bat else "#DED6F2"
    row_bg_1 = "#FDF7FA" if is_bat else "#FAF8FD"
    metric_label = "Strike Rate" if is_bat else "Economy"
    balls_label = "Press Balls" if is_bat else "Legal Balls"
    
    rows_html = []
    for idx, r in df_top.sort_values('rank', ascending=True).iterrows():
        rank = int(r['rank'])
        name = r['player_name']
        team = str(r['ipl_franchises']).split(',')[0] if pd.notnull(r.get('ipl_franchises')) else "IPL"
        score = f"{r['final_composite_score']:.4f}"
        
        if is_bat:
            balls = int(r.get('pressure_exposure_balls', r.get('pressure_balls', 0)))
            perf = f"{r.get('pressure_strike_rate', 0.0):.1f}"
        else:
            balls = int(r.get('pressure_exposure_legal_balls', r.get('pressure_balls', 0)))
            perf = f"{r.get('pressure_economy_rate', 0.0):.2f}"
        
        if rank == 1:
            rank_cell = f'<span style="background: {badge_bg_1}; color: {badge_col_1}; border: 1px solid {badge_bor_1}; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 0.74rem;">Rank 1</span>'
            row_style = f'background: {row_bg_1}; border-bottom: 1px solid #ECEAF3;'
            score_cell = f'<strong style="color: {primary_color}; font-size: 0.92rem; font-weight: 700;">{score}</strong>'
            name_cell = f'<strong style="color: #25233A; font-size: 0.88rem;">{name}</strong>'
        elif rank == 2:
            rank_cell = '<span style="background: #F8F8FC; color: #7964B5; border: 1px solid #ECEAF3; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.74rem;">Rank 2</span>'
            row_style = 'background: #FAF8FE; border-bottom: 1px solid #ECEAF3;'
            score_cell = f'<strong style="color: #25233A; font-size: 0.88rem;">{score}</strong>'
            name_cell = f'<span style="font-weight: 600; color: #25233A; font-size: 0.86rem;">{name}</span>'
        elif rank == 3:
            rank_cell = '<span style="background: #F8F8FC; color: #77758A; border: 1px solid #ECEAF3; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.74rem;">Rank 3</span>'
            row_style = 'background: #FCFBFE; border-bottom: 1px solid #ECEAF3;'
            score_cell = f'<strong style="color: #25233A; font-size: 0.88rem;">{score}</strong>'
            name_cell = f'<span style="font-weight: 600; color: #25233A; font-size: 0.86rem;">{name}</span>'
        else:
            rank_cell = f'<span style="color: #77758A; font-weight: 500; font-size: 0.80rem; padding-left: 4px;">Rank {rank}</span>'
            row_style = 'background: #FFFFFF; border-bottom: 1px solid #F8F8FC;'
            score_cell = f'<span style="color: #25233A; font-weight: 600; font-size: 0.86rem;">{score}</span>'
            name_cell = f'<span style="color: #25233A; font-size: 0.85rem;">{name}</span>'
            
        rows_html.append(f"""
        <tr style="{row_style}">
            <td style="padding: 7px 8px; width: 44px; text-align: center;">{rank_cell}</td>
            <td style="padding: 7px 8px;">{name_cell}</td>
            <td style="padding: 7px 8px; font-size: 0.78rem; color: #77758A;">{team}</td>
            <td style="padding: 7px 8px; text-align: right; font-size: 0.82rem; color: #77758A;">{balls}</td>
            <td style="padding: 7px 8px; text-align: right; font-size: 0.82rem; color: #25233A; font-weight: 600;">{perf}</td>
            <td style="padding: 7px 10px; text-align: right;">{score_cell}</td>
        </tr>
        """)
        
    table_html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(37,35,58,0.03); margin-top: 6px; margin-bottom: 12px;">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-family: 'Plus Jakarta Sans', sans-serif;">
            <thead>
                <tr style="background: #F8F8FC; border-bottom: 1px solid #ECEAF3; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #77758A;">
                    <th style="padding: 8px 8px; text-align: center;">Rank</th>
                    <th style="padding: 8px 8px;">Player</th>
                    <th style="padding: 8px 8px;">Team</th>
                    <th style="padding: 8px 8px; text-align: right;">{balls_label}</th>
                    <th style="padding: 8px 8px; text-align: right;">{metric_label}</th>
                    <th style="padding: 8px 10px; text-align: right;">Score</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows_html)}
            </tbody>
        </table>
    </div>
    """
    render_html(table_html)

def render_stats_summary_table(stats_data, role='batter'):
    """Render a beautifully formatted HTML statistical summary table for player dossier."""
    rows = []
    num_metrics = len(stats_data['Metric'])
    for i in range(num_metrics):
        metric = stats_data['Metric'][i]
        baseline = stats_data['Baseline (Low / Non-Pressure)'][i]
        pressure = stats_data['High Pressure (PI >= 0.65)'][i]
        delta_key = 'Clutch Improvement' if 'Clutch Improvement' in stats_data else 'Delta / Impact'
        delta = stats_data[delta_key][i]
        
        # Color delta cell
        delta_style = "color: #77758A;"
        if delta.startswith("+"):
            delta_style = "color: #276749; font-weight: 700; background: #EAF7EE; padding: 2px 6px; border-radius: 4px;"
        elif delta.startswith("-") and delta != "-":
            delta_style = "color: #9B2C2C; font-weight: 700; background: #FDF0F0; padding: 2px 6px; border-radius: 4px;"
            
        bg = "#FFFFFF" if i % 2 == 0 else "#F8F8FC"
        rows.append(f"""
        <tr style="background: {bg}; border-bottom: 1px solid #ECEAF3;">
            <td style="padding: 8px 12px; font-weight: 600; color: #25233A; font-size: 0.86rem;">{metric}</td>
            <td style="padding: 8px 12px; font-size: 0.86rem; color: #77758A;">{baseline}</td>
            <td style="padding: 8px 12px; font-size: 0.86rem; font-weight: 600; color: #25233A;">{pressure}</td>
            <td style="padding: 8px 12px; font-size: 0.86rem;"><span style="{delta_style}">{delta}</span></td>
        </tr>
        """)
        
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-radius: 10px; overflow: hidden; margin-top: 8px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(37,35,58,0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="background: #F8F8FC; border-bottom: 1px solid #ECEAF3; font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #77758A;">
                    <th style="padding: 9px 12px;">Metric Dimension</th>
                    <th style="padding: 9px 12px;">Baseline (PI &lt; 0.65)</th>
                    <th style="padding: 9px 12px;">High Pressure (PI &ge; 0.65)</th>
                    <th style="padding: 9px 12px;">Clutch Delta / Impact</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
    </div>
    """
    render_html(html)

def render_scouting_card(p_row):
    """Render a compact scouting discovery card for Player Search page."""
    is_bat = (p_row['role'] == 'batter')
    role_color = "#D58DB5" if is_bat else "#7964B5"
    role_bg = "#F2DCE9" if is_bat else "#F0ECF8"
    role_border = "#F2DCE9" if is_bat else "#DED6F2"
    
    is_qual = p_row['is_qualified']
    rank_label = f"Rank {int(p_row['rank'])}" if is_qual and pd.notnull(p_row['rank']) else "Sample Gate"
    score_str = f"{p_row['final_composite_score']:.4f}" if is_qual and pd.notnull(p_row['final_composite_score']) else "N/A"
    
    status_color = "#276749" if is_qual else "#D58DB5"
    status_bg = "#EAF7EE" if is_qual else "#F2DCE9"
    
    balls = int(p_row['pressure_exposure_balls'])
    matches = int(p_row['pressure_matches'])
    
    if is_bat:
        metric_str = f"SR: <strong>{p_row['pressure_strike_rate']:.1f}</strong>" if pd.notnull(p_row['pressure_strike_rate']) else "SR: N/A"
    else:
        metric_str = f"Econ: <strong>{p_row['pressure_economy_rate']:.2f}</strong>" if pd.notnull(p_row['pressure_economy_rate']) else "Econ: N/A"
        
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-top: 3px solid {role_color}; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(37,35,58,0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span style="background: {role_bg}; color: {role_color}; border: 1px solid {role_border}; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; padding: 2px 7px; border-radius: 4px;">
                    {p_row['role'].upper()}
                </span>
                <span style="background: {status_bg}; color: {status_color}; font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 4px; margin-left: 4px;">
                    {rank_label}
                </span>
                <div style="font-size: 1.05rem; font-weight: 800; color: #25233A; margin-top: 6px;">
                    {p_row['player_name']}
                </div>
                <div style="font-size: 0.78rem; color: #77758A; margin-top: 2px;">
                    {p_row['ipl_franchises']}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.68rem; font-weight: 600; text-transform: uppercase; color: #77758A;">Reliability</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: {role_color if is_qual else '#77758A'};">
                    {score_str}
                </div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid #ECEAF3; font-size: 0.78rem; color: #77758A;">
            <div><strong>{balls}</strong> Pressure Balls · <strong>{matches}</strong> Matches</div>
            <div>{metric_str}</div>
        </div>
    </div>
    """
    render_html(html)

def render_comparison_summary(players_list, role='batter'):
    """Render side-by-side KPI comparison cards for 2 or 3 players.
    
    Zero emojis, clean pastel styling with exact metrics and qualification awareness.
    """
    if not players_list:
        return
        
    is_bat = (role == 'batter')
    accent = "#D58DB5" if is_bat else "#7964B5"
    n_cols = len(players_list)
    grid_cols = "1fr 1fr" if n_cols == 2 else "1fr 1fr 1fr"
    
    card_items_html = []
    for p in players_list:
        is_qual = bool(p.get('is_qualified', False))
        p_name = p.get('player_name', 'Unknown')
        franchises = p.get('ipl_franchises', 'IPL')
        rank = p.get('rank', None)
        
        if is_qual and pd.notnull(rank):
            rank_badge = f'<span style="background: #EAF7EE; color: #276749; border: 1px solid #C6E7D0; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Rank {int(rank)}</span>'
            score_val = f"{float(p.get('final_composite_score', 0.0)):.4f}"
            score_color = accent
            status_note = '<span style="color: #276749; font-size: 0.74rem; font-weight: 600;">Sample Qualified (Phase 3A gate met)</span>'
        else:
            rank_badge = '<span style="background: #F2DCE9; color: #D58DB5; border: 1px solid #F2DCE9; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Sample Gate</span>'
            score_val = 'N/A'
            score_color = '#77758A'
            reason = p.get('unqualified_reasons', 'Insufficient pressure exposure')
            status_note = f'<span style="color: #D58DB5; font-size: 0.72rem; font-weight: 500;">{reason}</span>'
            
        balls = int(p.get('pressure_exposure_balls', 0))
        career_balls = int(p.get('career_eligible_balls', 0))
        matches = int(p.get('psr_qualifying_matches', p.get('pressure_matches', 0)))
        
        # Primary metrics
        if is_bat:
            p_sr = p.get('pressure_strike_rate', None)
            c_sr = p.get('career_strike_rate', p.get('baseline_strike_rate', None))
            d_sr = p.get('delta_strike_rate', None)
            sr_str = f"{float(p_sr):.1f}" if pd.notnull(p_sr) else "N/A"
            c_sr_str = f"{float(c_sr):.1f}" if pd.notnull(c_sr) else "N/A"
            delta_str = f"{float(d_sr):+.1f}" if pd.notnull(d_sr) else "--"
            delta_color = "#276749" if (pd.notnull(d_sr) and float(d_sr) >= 0) else "#D58DB5"
            
            p_avg = p.get('pressure_average', None)
            avg_str = f"{float(p_avg):.1f}" if (pd.notnull(p_avg) and float(p_avg) > 0) else "N/A"
            
            metric1_label = "Pressure Strike Rate"
            metric1_val = f"<strong>{sr_str}</strong> <span style='font-size:0.75rem; color:#77758A;'>(Career: {c_sr_str})</span>"
            metric1_sub = f"<span style='color:{delta_color}; font-weight:700;'>{delta_str} Delta</span>"
            
            metric2_label = "Pressure Average"
            metric2_val = f"<strong>{avg_str}</strong>"
            metric2_sub = f"<span style='color:#77758A;'>Boundary: {float(p.get('pressure_boundary_pct', 0)):.1f}%</span>"
        else:
            p_econ = p.get('pressure_economy_rate', None)
            c_econ = p.get('career_economy_rate', p.get('baseline_economy_rate', None))
            supp = p.get('clutch_econ_suppression', None)
            econ_str = f"{float(p_econ):.2f}" if pd.notnull(p_econ) else "N/A"
            c_econ_str = f"{float(c_econ):.2f}" if pd.notnull(c_econ) else "N/A"
            supp_str = f"{float(supp):+.2f}" if pd.notnull(supp) else "--"
            supp_color = "#276749" if (pd.notnull(supp) and float(supp) <= 0) else "#D58DB5"
            
            metric1_label = "Pressure Economy"
            metric1_val = f"<strong>{econ_str}</strong> <span style='font-size:0.75rem; color:#77758A;'>(Career: {c_econ_str})</span>"
            metric1_sub = f"<span style='color:{supp_color}; font-weight:700;'>{supp_str} Suppression</span>"
            
            dot_pct = float(p.get('pressure_dot_pct', 0.0))
            metric2_label = "Pressure Dot Ball %"
            metric2_val = f"<strong>{dot_pct:.1f}%</strong>"
            metric2_sub = "<span style='color:#77758A;'>Dot Delivery Control</span>"
            
        raw_psr = p.get('raw_psr', None)
        psr_str = f"{float(raw_psr)*100:.1f}%" if pd.notnull(raw_psr) else "N/A"
        
        cum_dva = p.get('pressure_cumulative_dva', None)
        dva_pb = p.get('pressure_dva_per_ball', None)
        dva_str = f"{float(cum_dva):+.2f}" if pd.notnull(cum_dva) else "N/A"
        dva_pb_str = f"{float(dva_pb):+.3f}/b" if pd.notnull(dva_pb) else ""
        dva_color = "#276749" if (pd.notnull(cum_dva) and float(cum_dva) >= 0) else "#D58DB5"
        
        item_html = f"""
        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-top: 3px solid {accent}; border-radius: 10px; padding: 18px; box-shadow: 0 1px 3px rgba(37,35,58,0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div>
                    <span style="background: {'#F2DCE9' if is_bat else '#F0ECF8'}; color: {accent}; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; margin-right: 6px;">
                        {'BATTER' if is_bat else 'BOWLER'}
                    </span>
                    {rank_badge}
                    <div style="font-size: 1.15rem; font-weight: 800; color: #25233A; margin-top: 6px;">{p_name}</div>
                    <div style="font-size: 0.78rem; color: #77758A; margin-top: 2px;">{franchises}</div>
                </div>
            </div>
            
            <div style="background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: #77758A; letter-spacing: 0.5px;">Reliability Score</div>
                    <div style="font-size: 1.45rem; font-weight: 800; color: {score_color};">{score_val}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: #77758A;">Pressure Exposure</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25233A;">{balls} balls <span style="font-size:0.75rem; color:#77758A;">({matches} matches)</span></div>
                    <div style="font-size: 0.72rem; color: #77758A;">Career: {career_balls} balls</div>
                </div>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.82rem; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 6px; border-bottom: 1px solid #ECEAF3;">
                    <span style="color: #77758A;">{metric1_label}</span>
                    <span style="color: #25233A; text-align: right;">{metric1_val} &nbsp; {metric1_sub}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 6px; border-bottom: 1px solid #ECEAF3;">
                    <span style="color: #77758A;">{metric2_label}</span>
                    <span style="color: #25233A; text-align: right;">{metric2_val} &nbsp; {metric2_sub}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 6px; border-bottom: 1px solid #ECEAF3;">
                    <span style="color: #77758A;">Net Pressure DVA</span>
                    <span style="color: {dva_color}; font-weight: 700;">{dva_str} <span style="font-size:0.75rem; font-weight:500; color:#77758A;">({dva_pb_str})</span></span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 4px;">
                    <span style="color: #77758A;">PSR Execution Success</span>
                    <span style="color: #25233A; font-weight: 700;">{psr_str}</span>
                </div>
            </div>
            
            <div style="padding-top: 8px; border-top: 1px solid #ECEAF3; min-height: 24px;">
                {status_note}
            </div>
        </div>
        """
        card_items_html.append(item_html)
        
    full_html = f"""
    <div style="display: grid; grid-template-columns: {grid_cols}; gap: 16px; margin-bottom: 20px;">
        {''.join(card_items_html)}
    </div>
    """
    render_html(full_html)


def render_comparison_data_table(players_list, role='batter'):
    """Render a compact comparison table showing side-by-side exact metrics.
    
    Zero emojis, precise formatting with qualification status, strike rate / economy,
    boundary/dot rates, cumulative DVA, and sample sizes.
    """
    if not players_list:
        return
        
    is_bat = (role == 'batter')
    
    metrics = [
        "Qualification Status",
        "Official Reliability Rank",
        "Reliability Composite Score",
        "Pressure Deliveries",
        "Qualifying Matches",
        "Pressure Strike Rate" if is_bat else "Pressure Economy",
        "Baseline Strike Rate" if is_bat else "Baseline Economy",
        "Performance Delta" if is_bat else "Econ Suppression",
        "Boundary % (Pressure)",
        "Dot Ball % (Pressure)",
        "Cumulative Pressure DVA",
        "DVA per Ball",
        "Pressure Success Rate (PSR)"
    ]
    
    table_data = {"Metric": metrics}
    
    for idx, p in enumerate(players_list):
        p_name = p.get('player_name', f"Player {idx+1}")
        franchise = str(p.get('ipl_franchises', '')).split(',')[0].strip()
        col_header = f"{p_name} ({franchise})" if franchise else p_name
        
        is_qual = bool(p.get('is_qualified', False))
        rank = p.get('rank', None)
        score = p.get('final_composite_score', None)
        
        status_str = "Sample Qualified" if is_qual else "Sample Gate"
        rank_str = f"Rank {int(rank)}" if (is_qual and pd.notnull(rank)) else "Unranked"
        score_str = f"{float(score):.4f}" if (is_qual and pd.notnull(score)) else "N/A"
        
        press_balls = int(p.get('pressure_exposure_balls', 0))
        press_matches = int(p.get('psr_qualifying_matches', p.get('pressure_matches', 0)))
        
        if is_bat:
            p_metric = p.get('pressure_strike_rate', None)
            b_metric = p.get('baseline_strike_rate', None)
            d_metric = p.get('delta_strike_rate', None)
            p_metric_str = f"{float(p_metric):.1f}" if pd.notnull(p_metric) else "N/A"
            b_metric_str = f"{float(b_metric):.1f}" if pd.notnull(b_metric) else "N/A"
            d_metric_str = f"{float(d_metric):+.1f}" if pd.notnull(d_metric) else "--"
        else:
            p_metric = p.get('pressure_economy_rate', None)
            b_metric = p.get('baseline_economy_rate', None)
            d_metric = p.get('clutch_econ_suppression', None)
            p_metric_str = f"{float(p_metric):.2f}" if pd.notnull(p_metric) else "N/A"
            b_metric_str = f"{float(b_metric):.2f}" if pd.notnull(b_metric) else "N/A"
            d_metric_str = f"{float(d_metric):+.2f}" if pd.notnull(d_metric) else "--"
            
        bdry_pct = p.get('pressure_boundary_pct', None)
        dot_pct = p.get('pressure_dot_pct', None)
        cum_dva = p.get('pressure_cumulative_dva', None)
        dva_pb = p.get('pressure_dva_per_ball', None)
        psr = p.get('raw_psr', None)
        
        bdry_str = f"{float(bdry_pct):.1f}%" if pd.notnull(bdry_pct) else "N/A"
        dot_str = f"{float(dot_pct):.1f}%" if pd.notnull(dot_pct) else "N/A"
        dva_str = f"{float(cum_dva):+.2f} runs" if pd.notnull(cum_dva) else "0.00 runs"
        dva_pb_str = f"{float(dva_pb):+.3f}/b" if pd.notnull(dva_pb) else "0.000/b"
        psr_str = f"{float(psr)*100.0:.1f}%" if pd.notnull(psr) else "N/A"
        
        values = [
            status_str,
            rank_str,
            score_str,
            f"{press_balls:,} balls",
            f"{press_matches} matches",
            p_metric_str,
            b_metric_str,
            d_metric_str,
            bdry_str,
            dot_str,
            dva_str,
            dva_pb_str,
            psr_str
        ]
        table_data[col_header] = values
        
    df_comp = pd.DataFrame(table_data)
    
    st.markdown(
        "<h4 style='font-size: 1.05rem; margin: 20px 0 8px 0; color: #25233A; font-family: \"Plus Jakarta Sans\", sans-serif;'>Side-by-Side Exact Performance Table</h4>",
        unsafe_allow_html=True
    )
    st.dataframe(df_comp, use_container_width=True, hide_index=True)


def render_match_overview_card(match_row, match_deliveries, player_id=None, role='batter'):
    """Render comprehensive match summary card with leverage profile and player involvement."""
    m_id = match_row.get('match_id', '')
    season = match_row.get('season', '')
    m_date = match_row.get('match_date', '')
    home = match_row.get('home_team', 'Home')
    away = match_row.get('away_team', 'Away')
    result = match_row.get('result', '')
    target = match_row.get('target_runs', None)
    
    # Match deliveries macro stats
    total_balls = len(match_deliveries)
    if total_balls > 0:
        high_press_df = match_deliveries[match_deliveries['pressure_index'] >= 0.65]
        high_press_balls = len(high_press_df)
        high_press_pct = (high_press_balls / total_balls) * 100.0
        mean_pi = match_deliveries['pressure_index'].mean()
        max_pi = match_deliveries['pressure_index'].max()
        total_runs = int(match_deliveries['delivery_total_runs'].sum())
        total_wkts = int(match_deliveries['is_wicket'].sum())
    else:
        high_press_balls = 0
        high_press_pct = 0.0
        mean_pi = 0.0
        max_pi = 0.0
        total_runs = 0
        total_wkts = 0
        
    # Player involvement
    player_summary_html = ""
    if player_id is not None and total_balls > 0:
        p_id = int(player_id)
        is_bat = (role == 'batter')
        if is_bat:
            p_deliv = match_deliveries[match_deliveries['striker_id'] == p_id]
            if not p_deliv.empty:
                p_name = p_deliv['striker_name'].iloc[0] if 'striker_name' in p_deliv.columns else 'Player'
                p_balls = len(p_deliv)
                p_runs = int(p_deliv['runs'].sum())
                p_sr = (p_runs / p_balls * 100.0) if p_balls > 0 else 0.0
                p_fours = len(p_deliv[p_deliv['runs'] == 4])
                p_sixes = len(p_deliv[p_deliv['runs'] == 6])
                p_out = len(p_deliv[p_deliv['is_wicket'] == True])
                
                # High pressure subset
                p_hp = p_deliv[p_deliv['pressure_index'] >= 0.65]
                p_hp_balls = len(p_hp)
                p_hp_runs = int(p_hp['runs'].sum()) if p_hp_balls > 0 else 0
                p_hp_sr = (p_hp_runs / p_hp_balls * 100.0) if p_hp_balls > 0 else 0.0
                p_dva = p_deliv['dva_batter'].sum() if 'dva_batter' in p_deliv.columns else 0.0
                dva_color = "#276749" if p_dva >= 0 else "#D58DB5"
                
                out_str = "Dismissed" if p_out > 0 else "Not Out"
                
                player_summary_html = f"""
                <div style="background: #FDF7FA; border: 1px solid #F2DCE9; border-radius: 8px; padding: 12px 16px; margin-top: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #D58DB5; letter-spacing: 0.5px;">
                            Player Match Impact: {p_name}
                        </span>
                        <span style="font-size: 0.75rem; font-weight: 700; color: {'#D58DB5' if p_out > 0 else '#276749'};">
                            {out_str}
                        </span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 0.82rem;">
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">Total Runs</div>
                            <div style="font-weight: 800; color: #25233A; font-size: 1.05rem;">{p_runs} <span style="font-size:0.75rem; font-weight:500;">({p_balls}b)</span></div>
                            <div style="color: #77758A; font-size: 0.72rem;">SR {p_sr:.1f} • {p_fours}x4 {p_sixes}x6</div>
                        </div>
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">High Pressure Runs</div>
                            <div style="font-weight: 800; color: #D58DB5; font-size: 1.05rem;">{p_hp_runs} <span style="font-size:0.75rem; font-weight:500;">({p_hp_balls}b)</span></div>
                            <div style="color: #77758A; font-size: 0.72rem;">Pressure SR {p_hp_sr:.1f}</div>
                        </div>
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">Net Match DVA</div>
                            <div style="font-weight: 800; color: {dva_color}; font-size: 1.05rem;">{p_dva:+.2f}</div>
                            <div style="color: #77758A; font-size: 0.72rem;">Runs vs Expected</div>
                        </div>
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">Leverage Share</div>
                            <div style="font-weight: 800; color: #25233A; font-size: 1.05rem;">{(p_hp_balls/p_balls*100.0) if p_balls > 0 else 0.0:.0f}%</div>
                            <div style="color: #77758A; font-size: 0.72rem;">High Pressure Balls</div>
                        </div>
                    </div>
                </div>
                """
            else:
                player_summary_html = """
                <div style="background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 8px; padding: 10px 14px; margin-top: 12px; font-size: 0.78rem; color: #77758A;">
                    Player did not face any deliveries in this match.
                </div>
                """
        else:
            # Bowler
            p_deliv = match_deliveries[match_deliveries['bowler_id'] == p_id]
            if not p_deliv.empty:
                p_name = p_deliv['bowler_name'].iloc[0] if 'bowler_name' in p_deliv.columns else 'Player'
                p_balls = len(p_deliv)
                p_ov = f"{p_balls // 6}.{p_balls % 6}"
                p_runs = int(p_deliv['bowler_runs_conceded'].sum())
                p_wkts = int(p_deliv['is_wicket'].sum())
                p_econ = (p_runs / (p_balls / 6.0)) if p_balls > 0 else 0.0
                
                p_hp = p_deliv[p_deliv['pressure_index'] >= 0.65]
                p_hp_balls = len(p_hp)
                p_hp_runs = int(p_hp['bowler_runs_conceded'].sum()) if p_hp_balls > 0 else 0
                p_hp_wkts = int(p_hp['is_wicket'].sum()) if p_hp_balls > 0 else 0
                p_hp_econ = (p_hp_runs / (p_hp_balls / 6.0)) if p_hp_balls > 0 else 0.0
                p_dva = p_deliv['dva_bowler'].sum() if 'dva_bowler' in p_deliv.columns else 0.0
                dva_color = "#276749" if p_dva >= 0 else "#D58DB5"
                
                player_summary_html = f"""
                <div style="background: #F0ECF8; border: 1px solid #DED6F2; border-radius: 8px; padding: 12px 16px; margin-top: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #7964B5; letter-spacing: 0.5px;">
                            Player Match Impact: {p_name}
                        </span>
                        <span style="font-size: 0.75rem; font-weight: 700; color: #25233A;">
                            Figures: {p_wkts}/{p_runs} ({p_ov} ov)
                        </span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 0.82rem;">
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">Economy Rate</div>
                            <div style="font-weight: 800; color: #25233A; font-size: 1.05rem;">{p_econ:.2f}</div>
                            <div style="color: #77758A; font-size: 0.72rem;">{p_balls} Balls Bowled</div>
                        </div>
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">High Pressure Econ</div>
                            <div style="font-weight: 800; color: #7964B5; font-size: 1.05rem;">{p_hp_econ:.2f}</div>
                            <div style="color: #77758A; font-size: 0.72rem;">{p_hp_wkts} Wkts in {p_hp_balls}b</div>
                        </div>
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">Net Bowling DVA</div>
                            <div style="font-weight: 800; color: {dva_color}; font-size: 1.05rem;">{p_dva:+.2f}</div>
                            <div style="color: #77758A; font-size: 0.72rem;">Defended vs Expected</div>
                        </div>
                        <div>
                            <div style="color: #77758A; font-size: 0.70rem;">Pressure Share</div>
                            <div style="font-weight: 800; color: #25233A; font-size: 1.05rem;">{(p_hp_balls/p_balls*100.0) if p_balls > 0 else 0.0:.0f}%</div>
                            <div style="color: #77758A; font-size: 0.72rem;">High Pressure Balls</div>
                        </div>
                    </div>
                </div>
                """
            else:
                player_summary_html = """
                <div style="background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 8px; padding: 10px 14px; margin-top: 12px; font-size: 0.78rem; color: #77758A;">
                    Player did not bowl any deliveries in this match.
                </div>
                """
                
    target_str = f"Target: {int(target)} runs" if pd.notnull(target) else ""
    result_str = f"{result} • {target_str}" if target_str else f"{result}"
    
    html = f"""
    <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #7964B5; border-radius: 10px; padding: 18px; margin-bottom: 18px; box-shadow: 0 1px 3px rgba(37,35,58,0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <span style="background: #F0ECF8; color: #7964B5; font-size: 0.70rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; border: 1px solid #DED6F2;">
                    IPL {season}
                </span>
                <span style="color: #77758A; font-size: 0.78rem; margin-left: 6px;">
                    Match {m_id} • {m_date}
                </span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #25233A; margin-top: 4px;">
                    {home} vs {away}
                </div>
                <div style="font-size: 0.82rem; color: #77758A; margin-top: 2px;">
                    {result_str}
                </div>
            </div>
            
            <div style="display: flex; gap: 16px; background: #F8F8FC; border: 1px solid #ECEAF3; border-radius: 8px; padding: 10px 16px;">
                <div style="text-align: center;">
                    <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: #77758A;">Mean PI</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #7964B5;">{mean_pi:.2f}</div>
                </div>
                <div style="text-align: center; border-left: 1px solid #ECEAF3; padding-left: 14px;">
                    <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: #77758A;">Peak PI</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #D58DB5;">{max_pi:.2f}</div>
                </div>
                <div style="text-align: center; border-left: 1px solid #ECEAF3; padding-left: 14px;">
                    <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: #77758A;">High Press. Balls</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #25233A;">{high_press_balls} <span style="font-size:0.75rem; color:#77758A;">({high_press_pct:.0f}%)</span></div>
                </div>
                <div style="text-align: center; border-left: 1px solid #ECEAF3; padding-left: 14px;">
                    <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; color: #77758A;">Match Total</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #25233A;">{total_runs}/{total_wkts}</div>
                </div>
            </div>
        </div>
        
        {player_summary_html}
    </div>
    """
    render_html(html)

