"""
SupeRR Selector - Premium Sports Performance Analytics Dashboard
================================================================
Season 2: IPL Pressure & Performance Analytics Platform
- Palette: #F8F8FC background, #FFFFFF cards/surfaces, #ECEAF3 borders, #25233A primary text, #77758A secondary text
- Accent System: Primary Purple (#7964B5), Bluish Purple (#927CCB), Lavender (#DED6F2), Very Light Lavender (#F0ECF8), Soft Pink (#F2DCE9), Rose Accent (#D58DB5)
- Strict adherence to Phase 3A Version 2.2 approved tiers (Low: < 0.40, Medium: 0.40–0.65, High: >= 0.65). Zero undefined categories.
- Zero emojis anywhere in the application. Fully validated Phase 3A Version 2.2 methodology.
- Uses st.html / render_html everywhere to eliminate raw HTML/CSS leakage.
"""

import os
import sys
import time
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# Comprehensive path resolution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
COMPONENTS_DIR = os.path.join(CURRENT_DIR, 'components')

for _dir in [ROOT_DIR, SRC_DIR, CURRENT_DIR, COMPONENTS_DIR]:
    if _dir not in sys.path:
        sys.path.insert(0, _dir)

try:
    from src.dashboard_data import (
        load_pressure_overview,
        load_all_players,
        load_top10_batters,
        load_top10_bowlers,
        load_player_match_history,
        load_player_phase_breakdown,
        load_ipl_matches,
        load_ipl_deliveries,
        load_player_match_deliveries
    )
except ImportError:
    from dashboard_data import (
        load_pressure_overview,
        load_all_players,
        load_top10_batters,
        load_top10_bowlers,
        load_player_match_history,
        load_player_phase_breakdown,
        load_ipl_matches,
        load_ipl_deliveries,
        load_player_match_deliveries
    )

try:
    from app.components.kpi_cards import (
        metric_card,
        status_badge,
        player_header_card,
        insight_box,
        render_hero_header,
        render_podium,
        render_top10_table,
        render_stats_summary_table,
        render_scouting_card,
        render_comparison_summary,
        render_comparison_data_table,
        render_match_overview_card,
        render_html
    )
except ImportError:
    from components.kpi_cards import (
        metric_card,
        status_badge,
        player_header_card,
        insight_box,
        render_hero_header,
        render_podium,
        render_top10_table,
        render_stats_summary_table,
        render_scouting_card,
        render_comparison_summary,
        render_comparison_data_table,
        render_match_overview_card,
        render_html
    )

try:
    from app.components.charts import (
        plot_pressure_tier_distribution,
        plot_phase_comparison,
        plot_match_timeline,
        plot_season_trends,
        plot_team_pressure,
        plot_top10_reliability_scatter,
        plot_top10_horizontal_bars,
        plot_qualification_summary,
        plot_innings_comparison,
        plot_match_phase_distribution,
        plot_franchise_representation,
        plot_career_vs_pressure_batter,
        plot_career_vs_pressure_bowler,
        plot_reliability_gauge,
        plot_batter_sr_avg_comparison,
        plot_bowler_econ_sr_comparison,
        plot_batter_strike_rate_chart,
        plot_batter_average_chart,
        plot_bowler_economy_chart,
        plot_bowler_strike_rate_chart,
        plot_dva_breakdown,
        plot_player_comparison_bars,
        plot_player_comparison_scoring,
        plot_player_comparison_control,
        plot_player_comparison_value,
        plot_player_comparison_radar,
        plot_player_comparison_exposure,
        plot_player_comparison_phase,
        plot_match_over_pressure_timeline,
        plot_match_innings_chase_comparison,
        plot_reliability_distribution,
        plot_tense_match_dynamics
    )
except ImportError:
    from components.charts import (
        plot_pressure_tier_distribution,
        plot_phase_comparison,
        plot_match_timeline,
        plot_season_trends,
        plot_team_pressure,
        plot_top10_reliability_scatter,
        plot_top10_horizontal_bars,
        plot_qualification_summary,
        plot_innings_comparison,
        plot_match_phase_distribution,
        plot_franchise_representation,
        plot_career_vs_pressure_batter,
        plot_career_vs_pressure_bowler,
        plot_reliability_gauge,
        plot_batter_sr_avg_comparison,
        plot_bowler_econ_sr_comparison,
        plot_batter_strike_rate_chart,
        plot_batter_average_chart,
        plot_bowler_economy_chart,
        plot_bowler_strike_rate_chart,
        plot_dva_breakdown,
        plot_player_comparison_bars,
        plot_player_comparison_scoring,
        plot_player_comparison_control,
        plot_player_comparison_value,
        plot_player_comparison_radar,
        plot_player_comparison_exposure,
        plot_player_comparison_phase,
        plot_match_over_pressure_timeline,
        plot_match_innings_chase_comparison,
        plot_reliability_distribution,
        plot_tense_match_dynamics
    )

try:
    from app.components.scouting_report_pdf import generate_scouting_pdf
except ImportError:
    from components.scouting_report_pdf import generate_scouting_pdf

# Page Setup
st.set_page_config(
    page_title="SupeRR Selector | IPL Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Modern SaaS Analytics Styling (Zero Emojis)
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* ------------------------------------------------------------- */
    /* Streamlit Chrome & Default Decoration Suppression */
    /* ------------------------------------------------------------- */
    [data-testid="stDecoration"],
    header[data-testid="stHeader"]::before,
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Keep header transparent so sidebar collapse arrow remains usable */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        background: transparent !important;
        border-bottom: none !important;
        color: #25233A !important;
    }
    
    /* Global App Background & Clean Plus Jakarta Sans Typography */
    html, body, .stApp, [data-testid="stApp"], [data-testid="stAppViewContainer"], section[data-testid="stMain"], [data-testid="stMainBlockContainer"], .main {
        background-color: #F8F8FC !important;
        background: #F8F8FC !important;
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* ------------------------------------------------------------- */
    /* Sidebar Light Surface (#FFFFFF) */
    /* ------------------------------------------------------------- */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border-right: 1px solid #ECEAF3 !important;
        box-shadow: 1px 0 4px rgba(37, 35, 58, 0.03) !important;
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Sidebar collapse / expand toggle icon styling (seamless light theme) */
    [data-testid="stSidebarCollapseButton"] button {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 6px !important;
        color: #77758A !important;
        transition: all 0.15s ease-in-out !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        background-color: #F8F8FC !important;
        border: 1px solid #ECEAF3 !important;
        color: #25233A !important;
    }
    [data-testid="stSidebarCollapseButton"] svg {
        color: #77758A !important;
        stroke: #77758A !important;
        fill: #77758A !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover svg {
        color: #25233A !important;
        stroke: #25233A !important;
        fill: #25233A !important;
    }
    
    [data-testid="collapsedControl"] button {
        background-color: #FFFFFF !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 6px !important;
        box-shadow: 0 1px 3px rgba(37, 35, 58, 0.05) !important;
        color: #77758A !important;
        transition: all 0.15s ease-in-out !important;
    }
    [data-testid="collapsedControl"] button:hover {
        background-color: #F0ECFA !important;
        border-color: #E3DCF6 !important;
        color: #7964B5 !important;
    }
    [data-testid="collapsedControl"] svg {
        color: #77758A !important;
        stroke: #77758A !important;
        fill: #77758A !important;
    }
    [data-testid="collapsedControl"] button:hover svg {
        color: #7964B5 !important;
        stroke: #7964B5 !important;
        fill: #7964B5 !important;
    }
    
    /* Layout width optimization & whitespace reduction */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 96% !important;
    }
    
    @media (max-width: 1200px) {
        .block-container {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 98% !important;
        }
    }
    
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1rem !important;
            max-width: 100% !important;
        }
        .comp-grid-container {
            grid-template-columns: 1fr !important;
        }
        .podium-grid-container {
            grid-template-columns: 1fr !important;
            align-items: stretch !important;
        }
    }
    
    /* ------------------------------------------------------------- */
    /* Strict Typography Scale & Hierarchy */
    /* Page titles: 28-32px bold | Section headings: 19-21px semibold */
    /* KPI values: 28-32px bold | Body text: 14-15px | Supporting text: 12-13px */
    /* ------------------------------------------------------------- */
    h1, [data-testid="stHeader"] h1 {
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.25 !important;
    }
    
    h2 {
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.3 !important;
    }
    
    h3 {
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.35 !important;
    }
    
    h4, h5, h6 {
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0 !important;
    }
    
    p, li, .stMarkdown p {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14.5px !important;
        font-weight: 400 !important;
        color: #25233A !important;
        line-height: 1.55 !important;
    }
    
    caption, .stCaption, [data-testid="stCaptionContainer"] p, small {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        color: #77758A !important;
        line-height: 1.4 !important;
    }
    
    /* Widget Labels */
    [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        color: #25233A !important;
        margin-bottom: 5px !important;
        letter-spacing: 0.02em !important;
    }
    
    /* ------------------------------------------------------------- */
    /* Compact, Left-Aligned Sidebar Navigation */
    /* ------------------------------------------------------------- */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.15rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] {
        width: 100% !important;
        margin: 1px 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] button {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
        padding: 8px 12px !important;
        border-radius: 6px !important;
        font-size: 0.88rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        line-height: 1.35 !important;
        box-shadow: none !important;
        outline: none !important;
        border: 1px solid transparent !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    
    /* Inactive text navigation item */
    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"] {
        background-color: transparent !important;
        background: transparent !important;
        color: #77758A !important;
        border: 1px solid transparent !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #F8F8FC !important;
        background: #F8F8FC !important;
        color: #25233A !important;
        border: 1px solid #ECEAF3 !important;
    }
    
    /* Active navigation item: pale lavender background and purple text */
    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
        background-color: #F0ECFA !important;
        background: #F0ECFA !important;
        color: #7964B5 !important;
        border: 1px solid #E3DCF6 !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
        background-color: #EAE3F7 !important;
        background: #EAE3F7 !important;
        color: #7964B5 !important;
        border: 1px solid #E3DCF6 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] button p,
    [data-testid="stSidebar"] [data-testid="stButton"] button span,
    [data-testid="stSidebar"] [data-testid="stButton"] button div {
        color: inherit !important;
        font-weight: inherit !important;
        font-size: inherit !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        margin: 0 !important;
        text-align: left !important;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"] p {
        color: #77758A !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover p {
        color: #25233A !important;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"] p {
        color: #7964B5 !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover p {
        color: #7964B5 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] button:focus,
    [data-testid="stSidebar"] [data-testid="stButton"] button:focus:not(:focus-visible) {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Suppress radio buttons in sidebar */
    [data-testid="stSidebar"] div[data-testid="stRadio"] {
        display: none !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* ------------------------------------------------------------- */
    /* Refined Dropdowns & Selectboxes (Consistent 40px, #ECEAF3 border) */
    /* ------------------------------------------------------------- */
    div[data-testid="stSelectbox"] {
        margin-bottom: 8px !important;
    }
    
    div[data-baseweb="select"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        width: 100% !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 8px !important;
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        padding: 0 12px !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #7964B5 !important;
        background-color: #F8F8FC !important;
    }
    
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="select"][aria-expanded="true"] > div {
        border-color: #7964B5 !important;
        box-shadow: 0 0 0 2px rgba(121, 100, 181, 0.18) !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[aria-selected="true"],
    div[data-baseweb="select"] div[class*="ValueContainer"] {
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        line-height: 40px !important;
    }
    
    div[data-baseweb="select"] svg {
        color: #77758A !important;
        fill: #77758A !important;
        transition: transform 0.15s ease !important;
    }
    
    /* Popover Listbox */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0 4px 16px rgba(37, 35, 58, 0.08) !important;
    }
    
    li[role="option"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        color: #25233A !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        margin: 1px 0 !important;
        transition: all 0.12s ease-in-out !important;
        cursor: pointer !important;
    }
    
    li[role="option"][aria-selected="true"] {
        background-color: #F0ECF8 !important;
        background: #F0ECF8 !important;
        color: #7964B5 !important;
        font-weight: 600 !important;
    }
    
    li[role="option"]:hover:not([aria-selected="true"]) {
        background-color: #F8F8FC !important;
        background: #F8F8FC !important;
        color: #25233A !important;
    }
    
    /* ------------------------------------------------------------- */
    /* Refined Search Fields & Text Inputs (Matches Dropdown Styling) */
    /* ------------------------------------------------------------- */
    div[data-testid="stTextInput"] {
        margin-bottom: 8px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 8px !important;
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-shadow: none !important;
        padding: 0 10px !important;
        transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    
    div[data-baseweb="input"]:hover {
        border-color: #7964B5 !important;
        background-color: #F8F8FC !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #7964B5 !important;
        box-shadow: 0 0 0 2px rgba(121, 100, 181, 0.18) !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-baseweb="input"] input {
        color: #25233A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        height: 38px !important;
        padding: 0 4px !important;
        background: transparent !important;
    }
    
    div[data-baseweb="input"] input::placeholder {
        color: #77758A !important;
        font-weight: 400 !important;
    }
    
    /* ------------------------------------------------------------- */
    /* Main Content Area Buttons (Consistent 40px Height, 8px Radius) */
    /* ------------------------------------------------------------- */
    [data-testid="stMain"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
        background: #7964B5 !important;
        background-color: #7964B5 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        height: 40px !important;
        min-height: 40px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0 16px !important;
        box-shadow: 0 1px 2px rgba(121, 100, 181, 0.18) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    
    [data-testid="stMain"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
        background: #6853A3 !important;
        background-color: #6853A3 !important;
        box-shadow: 0 2px 5px rgba(121, 100, 181, 0.28) !important;
    }
    
    [data-testid="stMain"] [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:focus {
        box-shadow: 0 0 0 2px rgba(121, 100, 181, 0.28) !important;
    }
    
    /* Secondary/Action button outline & download buttons in main area */
    [data-testid="stMain"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"],
    [data-testid="stMain"] [data-testid="stDownloadButton"] button {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #25233A !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 8px !important;
        height: 40px !important;
        min-height: 40px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0 16px !important;
        box-shadow: 0 1px 2px rgba(37, 35, 58, 0.02) !important;
        transition: all 0.15s ease-in-out !important;
        cursor: pointer !important;
    }
    
    [data-testid="stMain"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover {
        background-color: #F8F8FC !important;
        background: #F8F8FC !important;
        border-color: #7964B5 !important;
        color: #7964B5 !important;
    }
    
    [data-testid="stMain"] [data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:focus,
    [data-testid="stMain"] [data-testid="stDownloadButton"] button:focus {
        border-color: #7964B5 !important;
        box-shadow: 0 0 0 2px rgba(121, 100, 181, 0.18) !important;
    }
    
    /* Plotly Charts & Visual Containers */
    div.stPlotlyChart, [data-testid="stPlotlyChart"] {
        background: #FFFFFF !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03) !important;
        padding: 0 !important;
        margin-bottom: 20px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        width: 100% !important;
    }
    
    div.stPlotlyChart > div, [data-testid="stPlotlyChart"] > div,
    div.stPlotlyChart .js-plotly-plot, [data-testid="stPlotlyChart"] .js-plotly-plot,
    div.stPlotlyChart .plot-container, [data-testid="stPlotlyChart"] .plot-container {
        box-sizing: border-box !important;
        overflow: hidden !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    div.stPlotlyChart iframe, [data-testid="stPlotlyChart"] iframe {
        border: none !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        width: 100% !important;
    }
    
    /* Dataframe and Tables */
    div[data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid #ECEAF3 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03) !important;
        overflow: hidden !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid #ECEAF3;
        padding-bottom: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 6px 14px;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
        font-size: 0.88rem;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #77758A;
        background-color: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: #7964B5 !important;
        border-bottom: 2px solid #7964B5 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Scroll management helpers */
    div[data-testid="stHtml"]:has(#supeRR-scroll-anchor),
    iframe[title="st.components.v1.html"],
    div[data-testid="stCustomComponentV1"]:has(iframe[title="st.components.v1.html"]) {
        display: none !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
"""
st.html(CUSTOM_CSS)


# -----------------------------------------------------------------------------
# Navigation & State Setup
# -----------------------------------------------------------------------------
PAGES = [
    "Overview",
    "Rankings",
    "Player Search",
    "Batter Analysis",
    "Bowler Analysis",
    "Pressure Analysis",
    "Methodology"
]

# Sync with URL query parameters to support Browser Back / Forward buttons seamlessly
qp = st.query_params
query_page = qp.get("page", None)

if "page" not in st.session_state:
    st.session_state.page = query_page if (query_page in PAGES) else "Overview"
    st.session_state._last_synced_page = st.session_state.page
    st.query_params["page"] = st.session_state.page
elif query_page and query_page in PAGES and query_page != st.session_state.get("_last_synced_page"):
    # Browser Back or Forward button changed the URL
    if query_page != st.session_state.page:
        st.session_state.previous_page = st.session_state.page
        st.session_state.page = query_page
    st.session_state._last_synced_page = query_page

if "previous_page" not in st.session_state:
    st.session_state.previous_page = "Overview"

if "selected_batter_id" not in st.session_state:
    st.session_state.selected_batter_id = 4708  # Default: Rinku Singh

if "selected_bowler_id" not in st.session_state:
    st.session_state.selected_bowler_id = 2933  # Default: Jasprit Bumrah

# -----------------------------------------------------------------------------
# Decoupled Comparison State Variables (Isolated from individual analysis navigation)
# 1. Active Page: st.session_state.page
# 2. Current Analysis Player: st.session_state.selected_batter_id / selected_bowler_id
# 3. Comparison Player 1: st.session_state.comp_player_1_id
# 4. Comparison Player 2: st.session_state.comp_player_2_id
# 5. Optional Comparison Player 3: st.session_state.comp_player_3_id, comp_enable_p3
# 6. Current Comparison Role: st.session_state.comp_role
# -----------------------------------------------------------------------------
if "comp_role" not in st.session_state:
    st.session_state.comp_role = "batter"

if "comp_bat_p1_id" not in st.session_state:
    st.session_state.comp_bat_p1_id = 4708  # Default: Rinku Singh

if "comp_bat_p2_id" not in st.session_state:
    st.session_state.comp_bat_p2_id = 4016  # Default: Shivam Dube

if "comp_bat_p3_id" not in st.session_state:
    st.session_state.comp_bat_p3_id = None

if "comp_bat_enable_p3" not in st.session_state:
    st.session_state.comp_bat_enable_p3 = False

if "comp_bowl_p1_id" not in st.session_state:
    st.session_state.comp_bowl_p1_id = 2933  # Default: Jasprit Bumrah

if "comp_bowl_p2_id" not in st.session_state:
    st.session_state.comp_bowl_p2_id = 4220  # Default: Arshdeep Singh

if "comp_bowl_p3_id" not in st.session_state:
    st.session_state.comp_bowl_p3_id = None

if "comp_bowl_enable_p3" not in st.session_state:
    st.session_state.comp_bowl_enable_p3 = False

# Unified aliases
if "comp_player_1_id" not in st.session_state:
    st.session_state.comp_player_1_id = 4708

if "comp_player_2_id" not in st.session_state:
    st.session_state.comp_player_2_id = 4016

if "comp_player_3_id" not in st.session_state:
    st.session_state.comp_player_3_id = None

if "comp_enable_p3" not in st.session_state:
    st.session_state.comp_enable_p3 = False

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "nav_stack" not in st.session_state:
    st.session_state.nav_stack = []

if "batter_active_tab" not in st.session_state:
    st.session_state.batter_active_tab = "Player Overview"

if "bowler_active_tab" not in st.session_state:
    st.session_state.bowler_active_tab = "Player Overview"

def set_batter_active_tab(tab_name):
    st.session_state.batter_active_tab = tab_name

def set_bowler_active_tab(tab_name):
    st.session_state.bowler_active_tab = tab_name

# -----------------------------------------------------------------------------
# Load Datasets (Early load for dynamic sidebar & dashboard components)
# -----------------------------------------------------------------------------
try:
    overview_data = load_pressure_overview()
    df_players = load_all_players()
    df_top_bat = load_top10_batters()
    df_top_bowl = load_top10_bowlers()
except Exception as e:
    st.error(f"Error loading dashboard datasets: {str(e)}")
    st.stop()

# Derive dynamic cohort counts and labels
n_qual_bat = int(((df_players['role'] == 'batter') & df_players['is_qualified']).sum())
n_tot_bat = int((df_players['role'] == 'batter').sum())
n_qual_bowl = int(((df_players['role'] == 'bowler') & df_players['is_qualified']).sum())
n_tot_bowl = int((df_players['role'] == 'bowler').sum())

opt_qual_bat = f"Qualified Only (N={n_qual_bat})"
opt_all_bat = f"All Batters (N={n_tot_bat})"
opt_qual_bowl = f"Qualified Only (N={n_qual_bowl})"
opt_all_bowl = f"All Bowlers (N={n_tot_bowl})"

opt_sq_bat = f"Qualified Batters Only (N={n_qual_bat})"
opt_sq_all_bat = f"All Batters (N={n_tot_bat})"
opt_sq_bowl = f"Qualified Bowlers Only (N={n_qual_bowl})"
opt_sq_all_bowl = f"All Bowlers (N={n_tot_bowl})"

def reset_rank_bat_filters():
    st.session_state.rank_bat_search_input = ""
    st.session_state.rank_team_bat = "All Franchises"
    st.session_state.rank_qual_bat = opt_qual_bat

def reset_rank_bowl_filters():
    st.session_state.rank_bowl_search_input = ""
    st.session_state.rank_team_bowl = "All Franchises"
    st.session_state.rank_qual_bowl = opt_qual_bowl

def reset_player_search_filters():
    st.session_state.search_query = ""
    st.session_state.ps_search_box = ""
    st.session_state.ps_role_box = "All Roles"
    st.session_state.ps_franchise_box = "All Franchises"
    st.session_state.ps_qual_box = "All Players"

if "rankings_active_tab" not in st.session_state:
    st.session_state.rankings_active_tab = "Batters Leaderboard"

if "rank_bat_search_input" not in st.session_state:
    st.session_state.rank_bat_search_input = ""

if "rank_team_bat" not in st.session_state:
    st.session_state.rank_team_bat = "All Franchises"

if "rank_qual_bat" not in st.session_state or not str(st.session_state.rank_qual_bat).startswith("Qualified"):
    st.session_state.rank_qual_bat = opt_qual_bat
else:
    st.session_state.rank_qual_bat = opt_qual_bat

if "rank_bowl_search_input" not in st.session_state:
    st.session_state.rank_bowl_search_input = ""

if "rank_team_bowl" not in st.session_state:
    st.session_state.rank_team_bowl = "All Franchises"

if "rank_qual_bowl" not in st.session_state or not str(st.session_state.rank_qual_bowl).startswith("Qualified"):
    st.session_state.rank_qual_bowl = opt_qual_bowl
else:
    st.session_state.rank_qual_bowl = opt_qual_bowl

if "ps_search_box" not in st.session_state:
    st.session_state.ps_search_box = ""

if "ps_role_box" not in st.session_state:
    st.session_state.ps_role_box = "All Roles"

if "ps_franchise_box" not in st.session_state:
    st.session_state.ps_franchise_box = "All Franchises"

if "ps_qual_box" not in st.session_state:
    st.session_state.ps_qual_box = "All Players"

if "ps_selected_idx" not in st.session_state:
    st.session_state.ps_selected_idx = 0

if "rank_bat_sel_box" not in st.session_state:
    st.session_state.rank_bat_sel_box = 4708

if "rank_bowl_sel_box" not in st.session_state:
    st.session_state.rank_bowl_sel_box = 2933

if "ps_select_player_box" not in st.session_state:
    st.session_state.ps_select_player_box = 0

if "sq_bat_cohort_select" not in st.session_state or not str(st.session_state.sq_bat_cohort_select).startswith("Qualified"):
    st.session_state.sq_bat_cohort_select = opt_sq_bat
else:
    st.session_state.sq_bat_cohort_select = opt_sq_bat

if "sq_bat_cohort_val" not in st.session_state or not str(st.session_state.sq_bat_cohort_val).startswith("Qualified"):
    st.session_state.sq_bat_cohort_val = opt_sq_bat
else:
    st.session_state.sq_bat_cohort_val = opt_sq_bat

if "sq_bat_hl_select" not in st.session_state:
    st.session_state.sq_bat_hl_select = "(None)"

if "sq_bowl_cohort_select" not in st.session_state or not str(st.session_state.sq_bowl_cohort_select).startswith("Qualified"):
    st.session_state.sq_bowl_cohort_select = opt_sq_bowl
else:
    st.session_state.sq_bowl_cohort_select = opt_sq_bowl

if "sq_bowl_cohort_val" not in st.session_state or not str(st.session_state.sq_bowl_cohort_val).startswith("Qualified"):
    st.session_state.sq_bowl_cohort_val = opt_sq_bowl
else:
    st.session_state.sq_bowl_cohort_val = opt_sq_bowl

if "sq_bowl_hl_select" not in st.session_state:
    st.session_state.sq_bowl_hl_select = "(None)"


def navigate_to(page_name, player_id=None, role=None, from_tab=None, origin_page=None):
    """
    Seamless router between dashboard views preserving analytics state and full history stack.
    """
    current_page = st.session_state.get("page", "Overview")
    actual_origin = origin_page or current_page

    # Determine origin active tab if leaving an analysis or rankings page
    current_tab = from_tab
    if current_tab is None:
        if actual_origin == "Batter Analysis":
            current_tab = st.session_state.get("batter_active_tab", "Player Overview")
        elif actual_origin == "Bowler Analysis":
            current_tab = st.session_state.get("bowler_active_tab", "Player Overview")
        elif actual_origin == "Rankings":
            current_tab = st.session_state.get("rankings_active_tab", "Batters Leaderboard")

    history_entry = {
        "page": actual_origin,
        "tab": current_tab,
        "selected_batter_id": st.session_state.get("selected_batter_id", 4708),
        "selected_bowler_id": st.session_state.get("selected_bowler_id", 2933),
        "search_query": st.session_state.get("search_query", ""),
        "ps_search_box": st.session_state.get("ps_search_box", ""),
        "ps_role_box": st.session_state.get("ps_role_box", "All Roles"),
        "ps_franchise_box": st.session_state.get("ps_franchise_box", "All Franchises"),
        "ps_qual_box": st.session_state.get("ps_qual_box", "All Players"),
        "ps_selected_idx": st.session_state.get("ps_selected_idx", 0),
        "ps_select_player_box": st.session_state.get("ps_selected_idx", 0),
        "rank_bat_search_input": st.session_state.get("rank_bat_search_input", ""),
        "rank_team_bat": st.session_state.get("rank_team_bat", "All Franchises"),
        "rank_qual_bat": st.session_state.get("rank_qual_bat", opt_qual_bat),
        "rank_bat_sel_box": st.session_state.get("rank_bat_sel_box", None),
        "rank_bowl_search_input": st.session_state.get("rank_bowl_search_input", ""),
        "rank_team_bowl": st.session_state.get("rank_team_bowl", "All Franchises"),
        "rank_qual_bowl": st.session_state.get("rank_qual_bowl", opt_qual_bowl),
        "rank_bowl_sel_box": st.session_state.get("rank_bowl_sel_box", None),
        "ov_select_bat": st.session_state.get("ov_select_bat", None),
        "ov_select_bowl": st.session_state.get("ov_select_bowl", None),
        "comp_bat_p1_id": st.session_state.get("comp_bat_p1_id", 4708),
        "comp_bat_p2_id": st.session_state.get("comp_bat_p2_id", 4016),
        "comp_bat_p3_id": st.session_state.get("comp_bat_p3_id", None),
        "comp_bat_enable_p3": st.session_state.get("comp_bat_enable_p3", False),
        "comp_bowl_p1_id": st.session_state.get("comp_bowl_p1_id", 2933),
        "comp_bowl_p2_id": st.session_state.get("comp_bowl_p2_id", 4220),
        "comp_bowl_p3_id": st.session_state.get("comp_bowl_p3_id", None),
        "comp_bowl_enable_p3": st.session_state.get("comp_bowl_enable_p3", False),
    }

    if "nav_stack" not in st.session_state:
        st.session_state.nav_stack = []

    # Record history if not redundant identical top
    if st.session_state.nav_stack:
        top = st.session_state.nav_stack[-1]
        if not (top.get("page") == actual_origin and top.get("tab") == current_tab and actual_origin == page_name):
            st.session_state.nav_stack.append(history_entry)
    else:
        st.session_state.nav_stack.append(history_entry)

    # Cap stack size
    if len(st.session_state.nav_stack) > 25:
        st.session_state.nav_stack.pop(0)

    st.session_state.previous_page = actual_origin
    st.session_state.page = page_name
    st.session_state._last_synced_page = page_name

    if player_id is not None:
        if role == 'bowler':
            st.session_state.selected_bowler_id = int(player_id)
        else:
            st.session_state.selected_batter_id = int(player_id)

    # Default to Player Overview when inspecting an individual player profile
    if page_name == "Batter Analysis":
        st.session_state.batter_active_tab = "Player Overview"
    if page_name == "Bowler Analysis":
        st.session_state.bowler_active_tab = "Player Overview"

    st.query_params["page"] = page_name
    st.rerun()


def navigate_back(fallback_page=None):
    """
    Pops the previous view state from nav_stack and restores page, tab, selected player, and filters.
    Prevents navigation loops and guarantees immediate single-click response.
    """
    current_page = st.session_state.get("page", "Overview")
    if "nav_stack" not in st.session_state:
        st.session_state.nav_stack = []

    # Clean stack: remove redundant top entries matching current page and active tab
    while st.session_state.nav_stack:
        cand = st.session_state.nav_stack[-1]
        cand_p = cand.get("page")
        cand_t = cand.get("tab")

        if cand_p == current_page:
            if current_page == "Batter Analysis":
                curr_tab = st.session_state.get("batter_active_tab")
            elif current_page == "Bowler Analysis":
                curr_tab = st.session_state.get("bowler_active_tab")
            elif current_page == "Rankings":
                curr_tab = st.session_state.get("rankings_active_tab")
            else:
                curr_tab = None

            if cand_t == curr_tab or cand_t is None:
                st.session_state.nav_stack.pop()
                continue
        break

    if st.session_state.nav_stack:
        target_state = st.session_state.nav_stack.pop()
        target_page = target_state.get("page", fallback_page or "Overview")
        target_tab = target_state.get("tab")

        st.session_state.previous_page = current_page
        st.session_state.page = target_page

        # Restore player selections
        if "selected_batter_id" in target_state:
            st.session_state.selected_batter_id = target_state["selected_batter_id"]
        if "selected_bowler_id" in target_state:
            st.session_state.selected_bowler_id = target_state["selected_bowler_id"]

        # Restore comparison players
        for k in ["comp_bat_p1_id", "comp_bat_p2_id", "comp_bat_p3_id", "comp_bat_enable_p3",
                  "comp_bowl_p1_id", "comp_bowl_p2_id", "comp_bowl_p3_id", "comp_bowl_enable_p3"]:
            if k in target_state and target_state[k] is not None:
                st.session_state[k] = target_state[k]

        # Restore tabs
        if target_page == "Batter Analysis" and target_tab:
            st.session_state.batter_active_tab = target_tab
        elif target_page == "Bowler Analysis" and target_tab:
            st.session_state.bowler_active_tab = target_tab
        elif target_page == "Rankings" and target_tab:
            st.session_state.rankings_active_tab = target_tab

        # Restore Player Search state
        if target_page == "Player Search":
            for k in ["search_query", "ps_search_box", "ps_role_box", "ps_franchise_box", "ps_qual_box", "ps_selected_idx", "ps_select_player_box"]:
                if k in target_state and target_state[k] is not None:
                    st.session_state[k] = target_state[k]

        # Restore Rankings state
        if target_page == "Rankings":
            for k in ["rank_bat_search_input", "rank_team_bat", "rank_qual_bat", "rank_bat_sel_box",
                      "rank_bowl_search_input", "rank_team_bowl", "rank_qual_bowl", "rank_bowl_sel_box"]:
                if k in target_state and target_state[k] is not None:
                    st.session_state[k] = target_state[k]

        # Restore Overview state
        if target_page == "Overview":
            for k in ["ov_select_bat", "ov_select_bowl"]:
                if k in target_state and target_state[k] is not None:
                    st.session_state[k] = target_state[k]
    else:
        # Fallback if stack is empty
        cand_fallback = st.session_state.get("previous_page")
        if cand_fallback and cand_fallback != current_page and cand_fallback in PAGES:
            target_page = cand_fallback
        else:
            target_page = fallback_page if (fallback_page and fallback_page != current_page) else "Overview"

        st.session_state.previous_page = current_page
        st.session_state.page = target_page

    st.session_state._last_synced_page = st.session_state.page
    st.query_params["page"] = st.session_state.page
    st.rerun()


def render_player_comparison_benchmarks(players_list, role='batter'):
    """Renders Performance Benchmarks across 3 separate Plotly containers with dedicated vertical space."""
    is_bat = (role == 'batter')
    main_title = "Batting Performance Benchmarks (Baseline vs High Pressure)" if is_bat else "Bowling Performance Benchmarks (Baseline vs High Pressure)"
    main_sub = (
        "Multi-group comparative benchmark evaluating scoring pace, boundary control, and cumulative value added under pressure."
        if is_bat else
        "Multi-group comparative benchmark evaluating run restriction, delivery control, and cumulative value added under pressure."
    )
    
    # 1. Main Title & Supporting Description Header Card with Player Legend Badges
    palette = ['#8872C5', '#D58DB5', '#5B4E7E']
    legend_chips = []
    for idx, p in enumerate(players_list):
        c = palette[idx % len(palette)]
        p_name = p.get('player_name', 'Unknown')
        fr = str(p.get('ipl_franchises', '')).split(',')[0].strip()
        label = f"{p_name} ({fr})" if fr else p_name
        legend_chips.append(
            f"<div style='display:inline-flex; align-items:center; gap:8px; padding:6px 14px; background:#F8F7FC; border:1px solid #ECEAF3; border-radius:20px; font-size:12.5px; font-weight:600; color:#25233A;'>"
            f"<span style='display:inline-block; width:12px; height:12px; background:{c}; border-radius:3px;'></span>"
            f"{label}"
            f"</div>"
        )
    chips_html = " ".join(legend_chips)
    
    header_html = (
        f"<div style='background:#FFFFFF; border:1px solid #ECEAF3; border-radius:12px; padding:20px 24px; margin-bottom:16px; box-shadow:0 1px 3px rgba(37,35,58,0.03);'>"
        f"<div style='font-size:17px; font-weight:700; color:#25233A; margin-bottom:4px; font-family: Plus Jakarta Sans, sans-serif;'>{main_title}</div>"
        f"<div style='font-size:12.5px; color:#4E4A62; font-weight:500; margin-bottom:14px; font-family: Plus Jakarta Sans, sans-serif;'>{main_sub}</div>"
        f"<div style='display:flex; flex-wrap:wrap; gap:10px; align-items:center;'>"
        f"<span style='font-size:11.5px; font-weight:600; color:#4E4A62; text-transform:uppercase; letter-spacing:0.5px;'>Players:</span>"
        f"{chips_html}"
        f"</div>"
        f"</div>"
    )
    render_html(header_html)
    
    # 2. Section 1 — Scoring Pace / Run Restriction
    fig_sec1 = plot_player_comparison_scoring(players_list, role=role)
    st.plotly_chart(fig_sec1, use_container_width=True)
    
    # 3. Section 2 — Boundary & Control / Delivery Control
    fig_sec2 = plot_player_comparison_control(players_list, role=role)
    st.plotly_chart(fig_sec2, use_container_width=True)
    
    # 4. Section 3 — Value Added
    fig_sec3 = plot_player_comparison_value(players_list, role=role)
    st.plotly_chart(fig_sec3, use_container_width=True)


# -----------------------------------------------------------------------------
# Sidebar Navigation & Branding
# -----------------------------------------------------------------------------
with st.sidebar:
    # Studio Branding: Light Theme with Soft Lavender SR Monogram
    render_html("""
        <div style="padding: 6px 4px 14px 4px; border-bottom: 1px solid #ECEAF3; margin-bottom: 14px; font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 32px; height: 32px; border-radius: 6px; background: #F0ECFA; border: 1px solid #E3DCF6; color: #7964B5; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.84rem; letter-spacing: -0.02em; flex-shrink: 0; font-family: 'Plus Jakarta Sans', sans-serif;">
                    SR
                </div>
                <div>
                    <div style="font-size: 1.02rem; font-weight: 700; color: #25233A; line-height: 1.15; letter-spacing: -0.01em; font-family: 'Plus Jakarta Sans', sans-serif;">
                        SupeRR Selector
                    </div>
                    <div style="font-size: 0.72rem; color: #77758A; font-weight: 500; margin-top: 2px; font-family: 'Plus Jakarta Sans', sans-serif;">
                        Cricket Intelligence Studio
                    </div>
                </div>
            </div>
        </div>
        <div style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #77758A; padding: 0 4px 8px 6px; font-family: 'Plus Jakarta Sans', sans-serif;">
            WORKSPACE
        </div>
    """)
    
    # Exactly Seven compact, left-aligned text-only navigation links
    for p in PAGES:
        is_active = (st.session_state.page == p)
        if st.button(
            p,
            key=f"nav_link_{p}",
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            if st.session_state.page != p:
                navigate_to(p, origin_page=st.session_state.page)
    
    # Subtle Light Studio Footer
    render_html(f"""
        <div style="padding: 14px 6px 6px 6px; border-top: 1px solid #ECEAF3; margin-top: 24px; font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="font-size: 0.78rem; font-weight: 600; color: #25233A; margin-bottom: 2px;">
                SupeRR Selector Studio
            </div>
            <div style="font-size: 0.70rem; color: #77758A; line-height: 1.45; font-weight: 500;">
                Seasons 2022–2026<br>
                {overview_data.get('total_matches', 853):,} Matches · {overview_data.get('total_deliveries', 173315):,} Deliveries
            </div>
        </div>
    """)


# -----------------------------------------------------------------------------
# Scroll Position Management (Automatic Scroll-to-Top on Page Navigation)
# -----------------------------------------------------------------------------
if "last_scrolled_page" not in st.session_state:
    st.session_state.last_scrolled_page = None

is_page_navigation = (st.session_state.last_scrolled_page != st.session_state.page)
if is_page_navigation:
    st.session_state.last_scrolled_page = st.session_state.page
    nav_token = f"{st.session_state.page}_{int(time.time() * 1000)}"
    
    # 1. Primary host-level reset: executes directly in the main window (no iframe restrictions)
    st.html(f"""
        <div id="supeRR-scroll-anchor" data-page="{st.session_state.page}" data-token="{nav_token}" style="position: absolute; top: 0; left: 0; width: 1px; height: 1px; pointer-events: none; opacity: 0; margin: 0; padding: 0;"></div>
        <script>
        (function() {{
            function resetScrollContainer() {{
                try {{
                    if ('scrollRestoration' in history) {{
                        history.scrollRestoration = 'manual';
                    }}
                }} catch(e) {{}}

                var doc = document;
                var parentDoc = null;
                if (window.parent && window.parent !== window) {{
                    try {{ parentDoc = window.parent.document; }} catch(e) {{}}
                }}

                // Target the actual scrolling container in Streamlit: section[data-testid="stMain"]
                var targets = [
                    doc.querySelector('section[data-testid="stMain"]'),
                    doc.querySelector('[data-testid="stMain"]'),
                    doc.querySelector('.stMain'),
                    doc.querySelector('section.main'),
                    doc.querySelector('.main'),
                    doc.querySelector('[data-testid="stAppViewContainer"]'),
                    doc.documentElement,
                    doc.body
                ];

                if (parentDoc) {{
                    try {{
                        targets.push(
                            parentDoc.querySelector('section[data-testid="stMain"]'),
                            parentDoc.querySelector('[data-testid="stMain"]'),
                            parentDoc.querySelector('.stMain'),
                            parentDoc.querySelector('section.main'),
                            parentDoc.querySelector('.main'),
                            parentDoc.querySelector('[data-testid="stAppViewContainer"]'),
                            parentDoc.documentElement,
                            parentDoc.body
                        );
                    }} catch(e) {{}}
                }}

                targets.forEach(function(el) {{
                    if (el) {{
                        el.scrollTop = 0;
                        if (typeof el.scrollTo === 'function') {{
                            try {{
                                el.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
                            }} catch(err) {{
                                el.scrollTop = 0;
                            }}
                        }}
                    }}
                }});

                try {{ window.scrollTo({{ top: 0, left: 0, behavior: 'instant' }}); }} catch(e) {{ window.scrollTo(0, 0); }}
                if (window.parent && window.parent !== window) {{
                    try {{ window.parent.scrollTo({{ top: 0, left: 0, behavior: 'instant' }}); }} catch(e) {{}}
                }}

                var anchor = doc.getElementById('supeRR-scroll-anchor') || (parentDoc && parentDoc.getElementById('supeRR-scroll-anchor'));
                if (anchor && typeof anchor.scrollIntoView === 'function') {{
                    try {{
                        anchor.scrollIntoView({{ behavior: 'instant', block: 'start' }});
                    }} catch(e) {{
                        try {{ anchor.scrollIntoView(true); }} catch(err) {{}}
                    }}
                }}
            }}

            resetScrollContainer();
            if (window.requestAnimationFrame) {{
                window.requestAnimationFrame(resetScrollContainer);
            }}
            setTimeout(resetScrollContainer, 15);
            setTimeout(resetScrollContainer, 50);
            setTimeout(resetScrollContainer, 120);
            setTimeout(resetScrollContainer, 250);
            setTimeout(resetScrollContainer, 500);
        }})();
        </script>
        <style>
            div[data-testid="stHtml"]:has(#supeRR-scroll-anchor) {{
                display: none !important;
                height: 0px !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        </style>
        <!-- supeRR_nav_reset: {nav_token} -->
    """, unsafe_allow_javascript=True)

    # 2. Secondary custom component iframe fallback (targets parent document)
    components.html(f"""
        <div id="supeRR-scroll-anchor-iframe" style="display:none;"></div>
        <script>
        (function() {{
            function resetParentScrollContainer() {{
                try {{
                    var p = window.parent;
                    if (!p || !p.document) return;
                    var doc = p.document;
                    var targets = [
                        doc.querySelector('section[data-testid="stMain"]'),
                        doc.querySelector('[data-testid="stMain"]'),
                        doc.querySelector('.stMain'),
                        doc.querySelector('section.main'),
                        doc.querySelector('.main'),
                        doc.querySelector('[data-testid="stAppViewContainer"]'),
                        doc.documentElement,
                        doc.body
                    ];
                    targets.forEach(function(el) {{
                        if (el) {{
                            el.scrollTop = 0;
                            if (el.scrollTo) {{
                                try {{ el.scrollTo({{ top: 0, left: 0, behavior: 'instant' }}); }} catch(e) {{ el.scrollTop = 0; }}
                            }}
                        }}
                    }});
                    try {{ p.scrollTo({{ top: 0, left: 0, behavior: 'instant' }}); }} catch(e) {{}}
                    var anchor = doc.getElementById('supeRR-scroll-anchor');
                    if (anchor && anchor.scrollIntoView) {{
                        try {{ anchor.scrollIntoView({{ behavior: 'instant', block: 'start' }}); }} catch(e) {{}}
                    }}
                }} catch(e) {{}}
            }}
            resetParentScrollContainer();
            if (window.requestAnimationFrame) window.requestAnimationFrame(resetParentScrollContainer);
            setTimeout(resetParentScrollContainer, 15);
            setTimeout(resetParentScrollContainer, 50);
            setTimeout(resetParentScrollContainer, 120);
            setTimeout(resetParentScrollContainer, 250);
            setTimeout(resetParentScrollContainer, 500);
        }})();
        </script>
    """, height=0, width=0)


# -----------------------------------------------------------------------------
# PAGE 1: OVERVIEW
# -----------------------------------------------------------------------------
if st.session_state.page == "Overview":
    # Clean Editorial Hero Section
    render_hero_header(overview_data)
    
    # Exactly 4 Polished Overview KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Matches Analysed", f"{overview_data['total_matches']:,}", "Seasons 2022–2026 analysed", variant='lavender', icon='chart')
    with col2:
        metric_card("Deliveries Analysed", f"{overview_data['total_deliveries']:,}", "Ball-by-ball leverage evaluated", variant='blue', icon='activity')
    with col3:
        players_sub = overview_data.get('players_evaluated_sub', f"{overview_data.get('total_batters_evaluated', 341)} Batters ({overview_data.get('qualified_batters', 45)} Qual) · {overview_data.get('total_bowlers_evaluated', 260)} Bowlers ({overview_data.get('qualified_bowlers', 53)} Qual)")
        metric_card("Players Evaluated", f"{overview_data.get('total_players_evaluated', 601):,}", players_sub, variant='purple', icon='users')
    with col4:
        metric_card("High-Pressure Deliveries", f"{overview_data['high_pressure_deliveries']:,}", f"{overview_data['pct_high_pressure']}% with PI >= 0.65", variant='pink', icon='pulse')
    
    # Section A & B: TOP 10 PLAYERS UNDER PRESSURE
    render_html("""
        <div style="margin-top: 24px; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid #ECEAF3; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 10px; font-family: 'Plus Jakarta Sans', sans-serif;">
            <div>
                <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #7964B5; margin-bottom: 4px;">
                    IPL Empirical Leaderboards
                </div>
                <h2 style="margin: 0; font-size: 20px; font-weight: 600; color: #25233A; letter-spacing: -0.01em;">
                    Top Reliable Players Under Pressure
                </h2>
            </div>
            <div style="display: flex; gap: 8px;">
                <span style="background: #F2DCE9; color: #D58DB5; border: 1px solid #F2DCE9; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
                    Batters Anchor K = 50
                </span>
                <span style="background: #F0ECF8; color: #7964B5; border: 1px solid #DED6F2; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
                    Bowlers Anchor K = 48
                </span>
            </div>
        </div>
    """)

    col_top_bat, col_top_bowl = st.columns(2)
    
    with col_top_bat:
        render_html("""
            <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 1.05rem; font-weight: 600; color: #25233A; letter-spacing: -0.01em;">
                        Top 10 Reliable Batters
                    </div>
                    <span style="background: #F2DCE9; color: #D58DB5; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 8px; border-radius: 6px; border: 1px solid #F2DCE9;">
                        40+ Pressure Balls · 6+ Matches
                    </span>
                </div>
                <div style="font-size: 0.82rem; color: #4E4A62; font-weight: 500; margin-top: 3px;">
                    Ranked by shrunk exposure-weighted PSR and volatility penalty kappa.
                </div>
            </div>
        """)
        
        # Horizontal Bar Chart (Pink/Rose Theme)
        fig_top_bat = plot_top10_horizontal_bars(df_top_bat, 'batter')
        st.plotly_chart(fig_top_bat, use_container_width=True)
        
        # Leaderboard Table
        render_top10_table(df_top_bat, 'batter')
        
        # Interactive selector to view detailed Batter Analysis
        render_html("<div style='font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #4E4A62; margin-top: 10px; margin-bottom: 6px;'>Inspect Detailed Batter Analysis</div>")
        col_sel_bat, col_btn_bat = st.columns([3, 1], vertical_alignment="bottom")
        with col_sel_bat:
            bat_names = df_top_bat['player_name'].tolist()
            selected_bat_name = st.selectbox(
                "Select Batter to Inspect Profile",
                options=bat_names,
                format_func=lambda name: f"Rank {int(df_top_bat.loc[df_top_bat['player_name']==name, 'rank'].values[0])} - {name} ({df_top_bat.loc[df_top_bat['player_name']==name, 'final_composite_score'].values[0]:.4f})",
                label_visibility="collapsed",
                key="ov_select_bat"
            )
        with col_btn_bat:
            if st.button("Inspect", key="btn_inspect_bat", use_container_width=True):
                p_id = df_top_bat.loc[df_top_bat['player_name'] == selected_bat_name, 'player_id'].values[0]
                navigate_to("Batter Analysis", player_id=p_id, role='batter', origin_page="Overview")
                
    with col_top_bowl:
        render_html("""
            <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.03); font-family: 'Plus Jakarta Sans', sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 1.05rem; font-weight: 600; color: #25233A; letter-spacing: -0.01em;">
                        Top 10 Reliable Bowlers
                    </div>
                    <span style="background: #F0ECF8; color: #7964B5; font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 8px; border-radius: 6px; border: 1px solid #DED6F2;">
                        36+ Legal Balls · 6+ Matches
                    </span>
                </div>
                <div style="font-size: 0.82rem; color: #4E4A62; font-weight: 500; margin-top: 3px;">
                    Ranked by shrunk exposure-weighted PSR and volatility penalty kappa.
                </div>
            </div>
        """)
        
        # Horizontal Bar Chart (Lavender/Purple Theme)
        fig_top_bowl = plot_top10_horizontal_bars(df_top_bowl, 'bowler')
        st.plotly_chart(fig_top_bowl, use_container_width=True)
        
        # Leaderboard Table
        render_top10_table(df_top_bowl, 'bowler')
        
        # Interactive selector to view detailed Bowler Analysis
        render_html("<div style='font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #4E4A62; margin-top: 10px; margin-bottom: 6px; font-family: \"Plus Jakarta Sans\", sans-serif;'>Inspect Detailed Bowler Analysis</div>")
        col_sel_bowl, col_btn_bowl = st.columns([3, 1], vertical_alignment="bottom")
        with col_sel_bowl:
            bowl_names = df_top_bowl['player_name'].tolist()
            selected_bowl_name = st.selectbox(
                "Select Bowler to Inspect Profile",
                options=bowl_names,
                format_func=lambda name: f"Rank {int(df_top_bowl.loc[df_top_bowl['player_name']==name, 'rank'].values[0])} - {name} ({df_top_bowl.loc[df_top_bowl['player_name']==name, 'final_composite_score'].values[0]:.4f})",
                label_visibility="collapsed",
                key="ov_select_bowl"
            )
        with col_btn_bowl:
            if st.button("Inspect", key="btn_inspect_bowl", use_container_width=True):
                p_id = df_top_bowl.loc[df_top_bowl['player_name'] == selected_bowl_name, 'player_id'].values[0]
                navigate_to("Bowler Analysis", player_id=p_id, role='bowler', origin_page="Overview")

    render_html("<div style='margin-top: 24px;'></div>")

    # Section C & D: PRESSURE OVERVIEW & SEASON TRENDS
    tournament_sub = overview_data.get('tournament_context_sub', f"Analysis of {overview_data['total_deliveries']:,} ball leverage distributions and season-by-season pressure trends across IPL 2022–2026.")
    render_html(f"""
        <div style="margin-top: 16px; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid #ECEAF3; font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #7964B5; margin-bottom: 4px;">
                Tournament Empirical Context
            </div>
            <h2 style="margin: 0; font-size: 20px; font-weight: 600; color: #25233A; letter-spacing: -0.01em;">
                Pressure Overview & Season Trends
            </h2>
            <div style="font-size: 0.86rem; color: #4E4A62; font-weight: 500; margin-top: 2px;">
                {tournament_sub}
            </div>
        </div>
    """)

    # Streamlined Tournament Context Visualizations:
    # 1) Delivery Volume by Pressure Tiers (Low, Med, High)
    # 2) Season-by-Season Pressure Trend
    col_ov_ch1, col_ov_ch2 = st.columns(2)
    with col_ov_ch1:
        fig_tiers = plot_pressure_tier_distribution(overview_data['tier_counts'], overview_data['tier_pcts'])
        st.plotly_chart(fig_tiers, use_container_width=True)
        tier_cap = overview_data.get('tier_caption', f"Distribution of {overview_data['total_deliveries']:,} legal tournament deliveries into Low (PI < 0.40), Medium (0.40–0.65), and High (PI >= 0.65) leverage tiers.")
        st.caption(tier_cap)
    with col_ov_ch2:
        fig_seasons = plot_season_trends(overview_data['season_summary'])
        st.plotly_chart(fig_seasons, use_container_width=True)
        season_cap = overview_data.get('season_caption', "Tournament trend across IPL editions showing total deliveries and the volume of critical high-pressure deliveries.")
        st.caption(season_cap)
    render_html("<div style='margin-top: 18px;'></div>")

    top_b = overview_data.get('top_batter', {})
    top_bw = overview_data.get('top_bowler', {})
    default_attrition = "<strong>Rigorous Sample Attrition:</strong> Only 13.2% of evaluated batters (45/341) and 20.4% of evaluated bowlers (53/260) satisfy the 3-tier sample threshold (minimum 40/36 pressure balls, 6 qualifying matches, 120 career balls)."
    default_anchors = f"<strong>Elite Stability Anchors:</strong> {top_b.get('name', 'Rinku Singh')} (Reliability {top_b.get('reliability_score', 0.5583):.4f}, {top_b.get('team', 'KKR')}) and {top_bw.get('name', 'Jasprit Bumrah')} (Reliability {top_bw.get('reliability_score', 0.6477):.4f}, {top_bw.get('team', 'MI')}) maintain locked Rank 1 positions across all sensitivity shrinkage anchors (K in [25, 100])."

    insights = [
        "<strong>Run-Chase Pressure Concentration:</strong> Chasing targets in the 2nd innings produces 2.4x higher pressure ball concentration (14.1% vs 5.9%) than 1st innings target setting, driven by terminal balls remaining and dynamic required run rates.",
        "<strong>Death-Overs Climax Leverage:</strong> The Death Phase (overs 16–20) concentrates over 72% of all match-deciding high-pressure deliveries across the tournament editions.",
        overview_data.get('sample_attrition_text', default_attrition),
        overview_data.get('elite_anchors_text', default_anchors)
    ]
    insight_box("Key Empirical Insights & Strategic Observations", insights, variant='lavender')


# -----------------------------------------------------------------------------
# PAGE 2: RANKINGS
# -----------------------------------------------------------------------------
elif st.session_state.page == "Rankings":
    col_nav_r1, col_nav_r2 = st.columns([1, 7], vertical_alignment="center")
    with col_nav_r1:
        if st.button("Back", key="back_btn_rank", use_container_width=True):
            navigate_back(fallback_page="Overview")
    with col_nav_r2:
        render_html("""
            <div style="display: inline-block; background: #F0ECF8; color: #7964B5; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; padding: 3px 10px; border-radius: 14px; margin-bottom: 2px;">
                Approved Phase 3A Version 2.2 Leaderboards
            </div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 1.2;">
                SupeRR Selector Reliability Rankings
            </h1>
        """)
    render_html("""
        <p style="color: #77758A; font-size: 0.94rem; margin-top: 6px; margin-bottom: 16px;">
            Definitive leaderboards for qualified IPL players. Scores combine empirical bayes shrinkage toward cohort priors with match-to-match volatility stabilization.
        </p>
        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #7964B5; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(37, 35, 58, 0.04);">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #7964B5; margin-bottom: 2px;">
                Ranking Methodology & Qualification Framework
            </div>
            <div style="font-size: 0.86rem; color: #37324B; line-height: 1.5;">
                Reliability Scores synthesize high-leverage performance (DVA), logarithmic match exposure weighting, and Empirical Bayes shrinkage toward cohort priors (Batters: &mu; = 0.4303, K = 50 balls; Bowlers: &mu; = 0.6210, K = 48 legal balls). Inconsistency is penalized via volatility stabilizer &kappa;. 
                <strong>Sample Qualification Gate:</strong> Minimum 40 pressure balls (batters) / 36 legal pressure balls (bowlers) across &ge; 6 qualifying matches and &ge; 120 career tournament deliveries.
            </div>
        </div>
    """)
    
    rankings_tab_list = ["Batters Leaderboard", "Bowlers Leaderboard", "Franchise Clutch Distribution"]
    rank_def_tab = st.session_state.get("rankings_active_tab", "Batters Leaderboard")
    if rank_def_tab not in rankings_tab_list:
        rank_def_tab = "Batters Leaderboard"
    role_tab1, role_tab2, role_tab3 = st.tabs(rankings_tab_list, default=rank_def_tab, key="rankings_tabs_container")
    
    # BATTERS LEADERBOARD TAB
    with role_tab1:
        render_html("<div style='margin-bottom: 12px;'></div>")

        # Complete Filter Bar: Search, Franchise, Qualification, Clear
        col_ctl1, col_ctl2, col_ctl3, col_ctl4 = st.columns([3, 2.5, 2.5, 1.2], vertical_alignment="bottom")
        with col_ctl1:
            search_bat = st.text_input("Search Batter by Name", placeholder="e.g. Rinku, Miller, Pooran...", key="rank_bat_search_input")
        with col_ctl2:
            all_bat_teams = ["All Franchises"] + sorted(list(set([t for teams in df_players[df_players['role'] == 'batter']['ipl_franchises'].dropna() for t in teams.split(", ")])))
            team_filter_bat = st.selectbox("Franchise", all_bat_teams, key="rank_team_bat")
        with col_ctl3:
            qual_filter_bat = st.selectbox("Qualification Status", [opt_qual_bat, opt_all_bat, "Non-Qualified Only"], key="rank_qual_bat")
        with col_ctl4:
            st.button("Clear", key="rank_clear_bat_btn", on_click=reset_rank_bat_filters, use_container_width=True)

        # Filter dataset
        if qual_filter_bat.startswith("Qualified"):
            bat_display = df_players[(df_players['role'] == 'batter') & df_players['is_qualified']].sort_values('final_composite_score', ascending=False).copy()
        elif qual_filter_bat.startswith("Non-Qualified"):
            bat_display = df_players[(df_players['role'] == 'batter') & (~df_players['is_qualified'])].sort_values('pressure_exposure_balls', ascending=False).copy()
        else:
            bat_display = df_players[df_players['role'] == 'batter'].sort_values(['is_qualified', 'final_composite_score', 'pressure_exposure_balls'], ascending=[False, False, False]).copy()

        if search_bat:
            bat_display = bat_display[bat_display['player_name'].str.contains(search_bat, case=False, na=False)]

        if team_filter_bat != "All Franchises":
            bat_display = bat_display[bat_display['ipl_franchises'].str.contains(team_filter_bat, na=False)]

        # Status & Export Bar
        col_st_b, col_ex_b = st.columns([3, 1])
        with col_st_b:
            render_html(f"<div style='font-size: 0.86rem; color: #77758A; padding-top: 6px;'>Showing <strong>{len(bat_display)}</strong> matching batters.</div>")
        with col_ex_b:
            csv_bat = bat_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                csv_bat,
                "supeRR_selector_batters_rankings.csv",
                "text/csv",
                use_container_width=True,
                key="dl_bat_csv_btn"
            )

        if bat_display.empty:
            st.info("No batters match the selected filter criteria.")
        else:
            # Subtle visual distinction for podium toppers when viewing qualified roster
            if qual_filter_bat.startswith("Qualified") and not search_bat and team_filter_bat == "All Franchises":
                render_podium(df_top_bat, role='batter')

            cols_to_show_bat = [
                'rank', 'player_name', 'ipl_franchises', 'final_composite_score',
                'exposure_weighted_psr', 'raw_psr', 'pressure_exposure_balls',
                'psr_qualifying_matches' if 'psr_qualifying_matches' in bat_display.columns else 'qualifying_matches',
                'delta_strike_rate'
            ]

            display_rename_bat = {
                'rank': 'Rank',
                'player_name': 'Player Name',
                'ipl_franchises': 'Franchise(s)',
                'final_composite_score': 'Reliability Score',
                'exposure_weighted_psr': 'Exp PSR',
                'raw_psr': 'Raw PSR',
                'pressure_exposure_balls': 'Pressure Balls',
                'psr_qualifying_matches': 'Qual Matches',
                'qualifying_matches': 'Qual Matches',
                'delta_strike_rate': 'Delta SR'
            }

            table_bat = bat_display[[c for c in cols_to_show_bat if c in bat_display.columns]].rename(columns=display_rename_bat)

            def highlight_top3(row):
                rank_val = row.get('Rank')
                if pd.notnull(rank_val):
                    try:
                        r = int(rank_val)
                        if r == 1:
                            return ['background-color: #F0ECF8; font-weight: 600;'] * len(row)
                        elif r in (2, 3):
                            return ['background-color: #F8F8FC; font-weight: 500;'] * len(row)
                    except (ValueError, TypeError):
                        pass
                return [''] * len(row)

            st.dataframe(
                table_bat.style.apply(highlight_top3, axis=1).format({
                    'Rank': lambda x: f"{int(x)}" if pd.notnull(x) else "-",
                    'Reliability Score': lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A",
                    'Exp PSR': lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A",
                    'Raw PSR': lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A",
                    'Pressure Balls': '{:.0f}',
                    'Qual Matches': '{:.0f}',
                    'Delta SR': lambda x: f"{x:+.2f}" if pd.notnull(x) else "N/A"
                }),
                use_container_width=True,
                hide_index=True
            )

            # Profile Inspection Selector
            col_act1, col_act2 = st.columns([3, 1], vertical_alignment="bottom")
            with col_act1:
                bat_options = bat_display['player_id'].tolist()
                if "rank_bat_sel_box" in st.session_state and bat_options:
                    if st.session_state.rank_bat_sel_box not in bat_options:
                        st.session_state.rank_bat_sel_box = bat_options[0]
                bat_select = st.selectbox(
                    "Select a batter to inspect analytics dossier:",
                    options=bat_options,
                    format_func=lambda x: f"Rank {int(bat_display[bat_display['player_id']==x]['rank'].values[0]) if 'rank' in bat_display.columns and pd.notnull(bat_display[bat_display['player_id']==x]['rank'].values[0]) else 'Gate'} - {bat_display[bat_display['player_id']==x]['player_name'].values[0]} ({bat_display[bat_display['player_id']==x]['ipl_franchises'].values[0]})",
                    key="rank_bat_sel_box"
                )
            with col_act2:
                if st.button("Inspect Profile", key="btn_rank_bat", use_container_width=True):
                    navigate_to("Batter Analysis", player_id=bat_select, role='batter', from_tab="Batters Leaderboard", origin_page="Rankings")

            render_html("<div style='margin-top: 20px;'></div>")
            
            # Top 10 Batters Horizontal Bar Chart
            chart_data_bat = bat_display if not bat_display.empty else df_top_bat
            fig_top_b = plot_top10_horizontal_bars(chart_data_bat, 'batter')
            st.plotly_chart(fig_top_b, use_container_width=True)

            # Scouting Quadrant Studio (Dedicated Interactive Tool)
            render_html("""
                <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #D58DB5; border-radius: 12px; padding: 16px 20px; margin-top: 24px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(36, 38, 59, 0.04);">
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #D58DB5; margin-bottom: 3px;">
                        Scouting Quadrant Studio
                    </div>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #25233A; letter-spacing: -0.01em;">
                        Pressure Exposure vs Reliability (Batters)
                    </h3>
                    <div style="font-size: 0.86rem; color: #77758A; margin-top: 4px; line-height: 1.45;">
                        Categorizes batters across four analytical quadrants against cohort median exposure and benchmark prior reliability (&mu; = 0.4303):
                        <strong>Proven Under Pressure</strong>, <strong>Promising (Limited Exposure)</strong>, 
                        <strong>Experienced but Inconsistent</strong>, and <strong>Developing Evidence</strong>.
                    </div>
                </div>
            """)

            # Handle Reset or Pending Cohort triggers before widget instantiation
            if st.session_state.get("sq_bat_do_reset", False):
                st.session_state.sq_bat_cohort_select = opt_sq_bat
                st.session_state.sq_bat_cohort_val = opt_sq_bat
                st.session_state.sq_bat_hl_select = 0
                st.session_state.sq_bat_highlight_id = None
                st.session_state.sq_bat_do_reset = False

            if st.session_state.get("sq_bat_pending_cohort", None):
                st.session_state.sq_bat_cohort_select = st.session_state.sq_bat_pending_cohort
                st.session_state.sq_bat_cohort_val = st.session_state.sq_bat_pending_cohort
                st.session_state.sq_bat_pending_cohort = None

            # State initialization for Quadrant interactive controls
            if "sq_bat_cohort_val" not in st.session_state:
                st.session_state.sq_bat_cohort_val = opt_sq_bat
            if "sq_bat_highlight_id" not in st.session_state:
                st.session_state.sq_bat_highlight_id = None

            # Interactive Quadrant Filter Bar - ONE searchable player selector
            col_q1, col_q2, col_q3 = st.columns([2.8, 5.8, 1.4], vertical_alignment="bottom")
            
            with col_q1:
                cohort_options = [opt_sq_bat, opt_sq_all_bat]
                cohort_idx = cohort_options.index(st.session_state.sq_bat_cohort_val) if st.session_state.sq_bat_cohort_val in cohort_options else 0
                sel_cohort_bat = st.selectbox(
                    "Quadrant Cohort",
                    options=cohort_options,
                    index=cohort_idx,
                    key="sq_bat_cohort_select"
                )
                st.session_state.sq_bat_cohort_val = sel_cohort_bat

            # Resolve base datasets
            bat_pool = df_players[df_players['role'] == 'batter'].sort_values('player_name').copy()
            if sel_cohort_bat.startswith("Qualified"):
                sq_cohort_bat = bat_pool[bat_pool['is_qualified']].sort_values('final_composite_score', ascending=False).copy()
            else:
                sq_cohort_bat = bat_pool.sort_values(['is_qualified', 'final_composite_score'], ascending=[False, False]).copy()

            with col_q2:
                # Complete batter dataset options for searching & selecting
                hl_options = [0] + bat_pool['player_id'].tolist()
                cur_hl_id = st.session_state.sq_bat_highlight_id or 0
                hl_pos = hl_options.index(cur_hl_id) if cur_hl_id in hl_options else 0
                
                def fmt_bat_search_hl(pid):
                    if pid == 0:
                        return "None (Top 5 Labels Only)"
                    matches = bat_pool[bat_pool['player_id'] == pid]
                    if not matches.empty:
                        r = matches.iloc[0]
                        q_tag = "Qualified" if r['is_qualified'] else "Non-Qualified"
                        return f"{r['player_name']} ({r['ipl_franchises']}) • {q_tag}"
                    return f"ID {pid}"

                sel_hl_bat = st.selectbox(
                    "Find and Highlight Batter",
                    options=hl_options,
                    index=hl_pos,
                    format_func=fmt_bat_search_hl,
                    key="sq_bat_hl_select"
                )
                st.session_state.sq_bat_highlight_id = sel_hl_bat if sel_hl_bat != 0 else None

            with col_q3:
                if st.button("Reset", key="sq_bat_reset_btn", use_container_width=True):
                    st.session_state.sq_bat_do_reset = True
                    st.rerun()

            # Data Flow: Resolve chart plotting DataFrame and Selected Batter Highlighting
            chart_bat_df = sq_cohort_bat.copy()
            highlight_id_to_plot = None

            if st.session_state.sq_bat_highlight_id:
                selected_bat_matches = bat_pool[bat_pool['player_id'] == st.session_state.sq_bat_highlight_id]
                if not selected_bat_matches.empty:
                    bat_row = selected_bat_matches.iloc[0]
                    bat_balls = int(bat_row['pressure_exposure_balls'])
                    bat_is_qual = bool(bat_row['is_qualified'])
                    raw_score = bat_row.get('final_composite_score')
                    has_chart_coords = (bat_balls > 0 and pd.notnull(raw_score))

                    if has_chart_coords:
                        bat_score = float(raw_score)
                        
                        # Dynamically append selected batter to chart data if outside currently displayed cohort
                        # This enables instant plotting and highlighting on the scatter plot without altering baseline cohort filters
                        if st.session_state.sq_bat_highlight_id not in chart_bat_df['player_id'].values:
                            chart_bat_df = pd.concat([chart_bat_df, selected_bat_matches], ignore_index=True)
                            
                        highlight_id_to_plot = st.session_state.sq_bat_highlight_id
                        
                        # Determine Quadrant relative to cohort median and Phase 3A prior mean (mu = 0.4303)
                        if len(chart_bat_df) <= 70 and 'is_qualified' in chart_bat_df.columns and chart_bat_df['is_qualified'].sum() > 0:
                            bat_med = float(chart_bat_df[chart_bat_df['is_qualified']]['pressure_exposure_balls'].median())
                        else:
                            bat_med = float(chart_bat_df['pressure_exposure_balls'].median())
                        prior_mean_bat = 0.4303
                        
                        if bat_balls >= bat_med and bat_score >= prior_mean_bat:
                            bat_quadrant = "Proven Under Pressure"
                            bat_quad_desc = "High Exposure · High Reliability"
                            bat_quad_color = "#7964B5"
                            bat_quad_bg = "#F0ECF8"
                        elif bat_balls < bat_med and bat_score >= prior_mean_bat:
                            bat_quadrant = "Promising, Limited Exposure"
                            bat_quad_desc = "Low Exposure · High Reliability"
                            bat_quad_color = "#927CCB"
                            bat_quad_bg = "#F2DCE9"
                        elif bat_balls >= bat_med and bat_score < prior_mean_bat:
                            bat_quadrant = "Experienced but Inconsistent"
                            bat_quad_desc = "High Exposure · Low Reliability"
                            bat_quad_color = "#77758A"
                            bat_quad_bg = "#ECEAF3"
                        else:
                            bat_quadrant = "Developing Evidence"
                            bat_quad_desc = "Low Exposure · Low Reliability"
                            bat_quad_color = "#77758A"
                            bat_quad_bg = "#F8F8FC"

                        if bat_is_qual:
                            bat_qual_badge = f"Qualified • Rank #{int(bat_row['rank'])}" if pd.notnull(bat_row.get('rank')) else "Qualified"
                            bat_rel_text = f"{bat_score:.4f}"
                            qual_context_html = ""
                        else:
                            bat_qual_badge = "Non-Qualified"
                            bat_rel_text = f"{bat_score:.4f}"
                            unqual_reason = bat_row.get('unqualified_reasons', 'Did not meet minimum qualification threshold')
                            qual_context_html = f"""
                            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #ECEAF3; font-size: 12px; color: #77758A;">
                                <strong style="color: #555368;">Qualification Context:</strong> {unqual_reason}
                            </div>
                            """

                        # Badge indicating whether overlaid or native to the selected cohort
                        is_overlaid = (st.session_state.sq_bat_highlight_id not in sq_cohort_bat['player_id'].values)
                        overlay_badge = '<span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #F2DCE9; color: #927CCB; padding: 2px 8px; border-radius: 10px;">Overlaid on Cohort</span>' if is_overlaid else ''

                        render_html(f"""
                        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #7964B5; border-radius: 8px; padding: 12px 18px; margin: 12px 0 14px 0; box-shadow: 0 1px 3px rgba(37,35,58,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                                <div>
                                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 3px;">
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #F0ECF8; color: #7964B5; padding: 2px 8px; border-radius: 10px;">
                                            {bat_qual_badge}
                                        </span>
                                        {overlay_badge}
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: {bat_quad_bg}; color: {bat_quad_color}; padding: 2px 8px; border-radius: 10px;">
                                            {bat_quadrant}
                                        </span>
                                    </div>
                                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #25233A;">
                                        {bat_row['player_name']} <span style="font-size: 13px; font-weight: 500; color: #77758A;">({bat_row['ipl_franchises']})</span>
                                    </h4>
                                    <div style="font-size: 12px; color: #77758A; margin-top: 2px;">{bat_quad_desc}</div>
                                </div>
                                <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                                    <div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #77758A;">Pressure Exposure</div>
                                        <div style="font-size: 15px; font-weight: 700; color: #25233A;">{bat_balls:,} balls</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #77758A;">Reliability Score</div>
                                        <div style="font-size: 15px; font-weight: 700; color: #7964B5;">{bat_rel_text}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #77758A;">Chart Coordinates</div>
                                        <div style="font-size: 13px; font-weight: 600; color: #555368;">X: {bat_balls}b &nbsp;|&nbsp; Y: {bat_score:.4f}</div>
                                    </div>
                                </div>
                            </div>
                            {qual_context_html}
                        </div>
                        """)
                    else:
                        # Player has zero pressure exposure balls (or missing reliability metrics)
                        # Do NOT plot on the scatter plot and do NOT assign arbitrary 0 coordinates
                        highlight_id_to_plot = None
                        unqual_reason = bat_row.get('unqualified_reasons', 'No pressure deliveries faced (Pressure Index >= 0.65)')
                        c_matches = int(bat_row['total_matches']) if pd.notnull(bat_row.get('total_matches')) else 0
                        c_balls = int(bat_row['career_eligible_balls']) if pd.notnull(bat_row.get('career_eligible_balls')) else 0
                        c_runs = int(bat_row['career_runs']) if pd.notnull(bat_row.get('career_runs')) else 0
                        c_sr = f"{float(bat_row['career_strike_rate']):.2f}" if pd.notnull(bat_row.get('career_strike_rate')) else "—"
                        c_avg = f"{float(bat_row['career_average']):.2f}" if pd.notnull(bat_row.get('career_average')) else "—"
                        c_dva = f"{float(bat_row['career_cumulative_dva']):+.2f}" if pd.notnull(bat_row.get('career_cumulative_dva')) else "—"

                        render_html(f"""
                        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #77758A; border-radius: 8px; padding: 14px 18px; margin: 12px 0 14px 0; box-shadow: 0 1px 3px rgba(37,35,58,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                                <div>
                                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #ECEAF3; color: #77758A; padding: 2px 8px; border-radius: 10px;">
                                            Non-Qualified • Zero Pressure Exposure
                                        </span>
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #F8F8FC; color: #77758A; padding: 2px 8px; border-radius: 10px; border: 1px solid #ECEAF3;">
                                            Cannot Plot on Pressure Chart
                                        </span>
                                    </div>
                                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #25233A;">
                                        {bat_row['player_name']} <span style="font-size: 13px; font-weight: 500; color: #77758A;">({bat_row['ipl_franchises']})</span>
                                    </h4>
                                    <div style="font-size: 13px; color: #555368; margin-top: 6px; line-height: 1.45;">
                                        This batter has faced <strong>0 pressure deliveries</strong> (PI &ge; 0.65) in the evaluated IPL dataset. 
                                        Because reliability under pressure requires pressure exposure to measure, this player cannot be plotted on the two-axis pressure scatter plot without introducing misleading coordinates.
                                    </div>
                                    <div style="margin-top: 8px; font-size: 12px; color: #77758A;">
                                        <strong style="color: #555368;">Qualification Reason:</strong> {unqual_reason}
                                    </div>
                                </div>
                                <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap; background: #F8F8FC; padding: 10px 14px; border-radius: 6px; border: 1px solid #ECEAF3;">
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Matches</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_matches}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Career Balls</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_balls:,}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Career Runs</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_runs:,}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Strike Rate</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_sr}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Average</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_avg}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Net DVA</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #7964B5;">{c_dva}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """)

            # Render the Scouting Quadrant
            fig_bat_scatter = plot_top10_reliability_scatter(
                chart_bat_df,
                role='batter',
                highlighted_player_id=highlight_id_to_plot,
                top_n_labels=5
            )
            st.plotly_chart(fig_bat_scatter, use_container_width=True)

    # BOWLERS LEADERBOARD TAB
    with role_tab2:
        render_html("<div style='margin-bottom: 12px;'></div>")

        # Complete Filter Bar: Search, Franchise, Qualification, Clear
        col_ctl_bw1, col_ctl_bw2, col_ctl_bw3, col_ctl_bw4 = st.columns([3, 2.5, 2.5, 1.2], vertical_alignment="bottom")
        with col_ctl_bw1:
            search_bowl = st.text_input("Search Bowler by Name", placeholder="e.g. Bumrah, Mohit, Sandeep...", key="rank_bowl_search_input")
        with col_ctl_bw2:
            all_bowl_teams = ["All Franchises"] + sorted(list(set([t for teams in df_players[df_players['role'] == 'bowler']['ipl_franchises'].dropna() for t in teams.split(", ")])))
            team_filter_bowl = st.selectbox("Franchise", all_bowl_teams, key="rank_team_bowl")
        with col_ctl_bw3:
            qual_filter_bowl = st.selectbox("Qualification Status", [opt_qual_bowl, opt_all_bowl, "Non-Qualified Only"], key="rank_qual_bowl")
        with col_ctl_bw4:
            st.button("Clear", key="rank_clear_bowl_btn", on_click=reset_rank_bowl_filters, use_container_width=True)

        # Filter dataset
        if qual_filter_bowl.startswith("Qualified"):
            bowl_display = df_players[(df_players['role'] == 'bowler') & df_players['is_qualified']].sort_values('final_composite_score', ascending=False).copy()
        elif qual_filter_bowl.startswith("Non-Qualified"):
            bowl_display = df_players[(df_players['role'] == 'bowler') & (~df_players['is_qualified'])].sort_values('pressure_exposure_balls', ascending=False).copy()
        else:
            bowl_display = df_players[df_players['role'] == 'bowler'].sort_values(['is_qualified', 'final_composite_score', 'pressure_exposure_balls'], ascending=[False, False, False]).copy()

        if search_bowl:
            bowl_display = bowl_display[bowl_display['player_name'].str.contains(search_bowl, case=False, na=False)]

        if team_filter_bowl != "All Franchises":
            bowl_display = bowl_display[bowl_display['ipl_franchises'].str.contains(team_filter_bowl, na=False)]

        # Status & Export Bar
        col_st_bw, col_ex_bw = st.columns([3, 1])
        with col_st_bw:
            render_html(f"<div style='font-size: 0.86rem; color: #77758A; padding-top: 6px;'>Showing <strong>{len(bowl_display)}</strong> matching bowlers.</div>")
        with col_ex_bw:
            csv_bowl = bowl_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                csv_bowl,
                "supeRR_selector_bowlers_rankings.csv",
                "text/csv",
                use_container_width=True,
                key="dl_bowl_csv_btn"
            )

        if bowl_display.empty:
            st.info("No bowlers match the selected filter criteria.")
        else:
            # Subtle visual distinction for podium toppers when viewing qualified roster
            if qual_filter_bowl.startswith("Qualified") and not search_bowl and team_filter_bowl == "All Franchises":
                render_podium(df_top_bowl, role='bowler')

            cols_to_show_bowl = [
                'rank', 'player_name', 'ipl_franchises', 'final_composite_score',
                'exposure_weighted_psr', 'raw_psr',
                'pressure_exposure_legal_balls' if 'pressure_exposure_legal_balls' in bowl_display.columns else 'pressure_exposure_balls',
                'psr_qualifying_matches' if 'psr_qualifying_matches' in bowl_display.columns else 'qualifying_matches',
                'clutch_econ_suppression'
            ]

            display_rename_bowl = {
                'rank': 'Rank',
                'player_name': 'Player Name',
                'ipl_franchises': 'Franchise(s)',
                'final_composite_score': 'Reliability Score',
                'exposure_weighted_psr': 'Exp PSR',
                'raw_psr': 'Raw PSR',
                'pressure_exposure_legal_balls': 'Legal Balls',
                'pressure_exposure_balls': 'Legal Balls',
                'psr_qualifying_matches': 'Qual Matches',
                'qualifying_matches': 'Qual Matches',
                'clutch_econ_suppression': 'Econ Suppression'
            }

            table_bowl = bowl_display[[c for c in cols_to_show_bowl if c in bowl_display.columns]].rename(columns=display_rename_bowl)

            def highlight_top3_bowl(row):
                rank_val = row.get('Rank')
                if pd.notnull(rank_val):
                    try:
                        r = int(rank_val)
                        if r == 1:
                            return ['background-color: #F0ECF8; font-weight: 600;'] * len(row)
                        elif r in (2, 3):
                            return ['background-color: #F8F8FC; font-weight: 500;'] * len(row)
                    except (ValueError, TypeError):
                        pass
                return [''] * len(row)

            st.dataframe(
                table_bowl.style.apply(highlight_top3_bowl, axis=1).format({
                    'Rank': lambda x: f"{int(x)}" if pd.notnull(x) else "-",
                    'Reliability Score': lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A",
                    'Exp PSR': lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A",
                    'Raw PSR': lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A",
                    'Legal Balls': '{:.0f}',
                    'Qual Matches': '{:.0f}',
                    'Econ Suppression': lambda x: f"{x:+.2f}" if pd.notnull(x) else "N/A"
                }),
                use_container_width=True,
                hide_index=True
            )

            col_act_bw1, col_act_bw2 = st.columns([3, 1], vertical_alignment="bottom")
            with col_act_bw1:
                bowl_options = bowl_display['player_id'].tolist()
                if "rank_bowl_sel_box" in st.session_state and bowl_options:
                    if st.session_state.rank_bowl_sel_box not in bowl_options:
                        st.session_state.rank_bowl_sel_box = bowl_options[0]
                bowl_select = st.selectbox(
                    "Select a bowler to inspect analytics dossier:",
                    options=bowl_options,
                    format_func=lambda x: f"Rank {int(bowl_display[bowl_display['player_id']==x]['rank'].values[0]) if 'rank' in bowl_display.columns and pd.notnull(bowl_display[bowl_display['player_id']==x]['rank'].values[0]) else 'Gate'} - {bowl_display[bowl_display['player_id']==x]['player_name'].values[0]} ({bowl_display[bowl_display['player_id']==x]['ipl_franchises'].values[0]})",
                    key="rank_bowl_sel_box"
                )
            with col_act_bw2:
                if st.button("Inspect Profile", key="btn_rank_bowl", use_container_width=True):
                    navigate_to("Bowler Analysis", player_id=bowl_select, role='bowler', from_tab="Bowlers Leaderboard", origin_page="Rankings")

            render_html("<div style='margin-top: 20px;'></div>")
            
            # Top 10 Bowlers Horizontal Bar Chart
            chart_data_bowl = bowl_display if not bowl_display.empty else df_top_bowl
            fig_top_bw = plot_top10_horizontal_bars(chart_data_bowl, 'bowler')
            st.plotly_chart(fig_top_bw, use_container_width=True)

            # Scouting Quadrant Studio (Bowlers)
            render_html("""
                <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #7964B5; border-radius: 12px; padding: 16px 20px; margin-top: 24px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(36, 38, 59, 0.04);">
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #7964B5; margin-bottom: 3px;">
                        Scouting Quadrant Studio
                    </div>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #25233A; letter-spacing: -0.01em;">
                        Pressure Exposure vs Reliability (Bowlers)
                    </h3>
                    <div style="font-size: 0.86rem; color: #77758A; margin-top: 4px; line-height: 1.45;">
                        Categorizes bowlers across four analytical quadrants against cohort median exposure and benchmark prior reliability (&mu; = 0.6210):
                        <strong>Proven Under Pressure</strong>, <strong>Promising (Limited Exposure)</strong>, 
                        <strong>Experienced but Inconsistent</strong>, and <strong>Developing Evidence</strong>.
                    </div>
                </div>
            """)

            # Handle Reset or Pending Cohort triggers before widget instantiation
            if st.session_state.get("sq_bowl_do_reset", False):
                st.session_state.sq_bowl_cohort_select = opt_sq_bowl
                st.session_state.sq_bowl_cohort_val = opt_sq_bowl
                st.session_state.sq_bowl_hl_select = 0
                st.session_state.sq_bowl_highlight_id = None
                st.session_state.sq_bowl_do_reset = False

            if st.session_state.get("sq_bowl_pending_cohort", None):
                st.session_state.sq_bowl_cohort_select = st.session_state.sq_bowl_pending_cohort
                st.session_state.sq_bowl_cohort_val = st.session_state.sq_bowl_pending_cohort
                st.session_state.sq_bowl_pending_cohort = None

            # State initialization for Bowler Quadrant controls
            if "sq_bowl_cohort_val" not in st.session_state:
                st.session_state.sq_bowl_cohort_val = opt_sq_bowl
            if "sq_bowl_highlight_id" not in st.session_state:
                st.session_state.sq_bowl_highlight_id = None

            # Interactive Quadrant Filter Bar - ONE searchable player selector
            col_q_bw1, col_q_bw2, col_q_bw3 = st.columns([2.8, 5.8, 1.4], vertical_alignment="bottom")
            
            with col_q_bw1:
                cohort_bw_options = [opt_sq_bowl, opt_sq_all_bowl]
                cohort_bw_idx = cohort_bw_options.index(st.session_state.sq_bowl_cohort_val) if st.session_state.sq_bowl_cohort_val in cohort_bw_options else 0
                sel_cohort_bowl = st.selectbox(
                    "Quadrant Cohort",
                    options=cohort_bw_options,
                    index=cohort_bw_idx,
                    key="sq_bowl_cohort_select"
                )
                st.session_state.sq_bowl_cohort_val = sel_cohort_bowl

            # Resolve base cohort dataset
            bowl_pool = df_players[df_players['role'] == 'bowler'].sort_values('player_name').copy()
            if sel_cohort_bowl.startswith("Qualified"):
                sq_cohort_bowl = bowl_pool[bowl_pool['is_qualified']].sort_values('final_composite_score', ascending=False).copy()
            else:
                sq_cohort_bowl = bowl_pool.sort_values(['is_qualified', 'final_composite_score'], ascending=[False, False]).copy()

            with col_q_bw2:
                # Complete bowler dataset options for searching & selecting
                hl_bw_options = [0] + bowl_pool['player_id'].tolist()
                cur_hl_bw_id = st.session_state.sq_bowl_highlight_id or 0
                hl_bw_pos = hl_bw_options.index(cur_hl_bw_id) if cur_hl_bw_id in hl_bw_options else 0
                
                def fmt_bowl_search_hl(pid):
                    if pid == 0:
                        return "None (Top 5 Labels Only)"
                    matches = bowl_pool[bowl_pool['player_id'] == pid]
                    if not matches.empty:
                        r = matches.iloc[0]
                        q_tag = "Qualified" if r['is_qualified'] else "Non-Qualified"
                        return f"{r['player_name']} ({r['ipl_franchises']}) • {q_tag}"
                    return f"ID {pid}"

                sel_hl_bowl = st.selectbox(
                    "Find and Highlight Bowler",
                    options=hl_bw_options,
                    index=hl_bw_pos,
                    format_func=fmt_bowl_search_hl,
                    key="sq_bowl_hl_select"
                )
                st.session_state.sq_bowl_highlight_id = sel_hl_bowl if sel_hl_bowl != 0 else None

            with col_q_bw3:
                if st.button("Reset", key="sq_bowl_reset_btn", use_container_width=True):
                    st.session_state.sq_bowl_do_reset = True
                    st.rerun()

            # Data Flow: Resolve chart plotting DataFrame and Selected Bowler Highlighting
            chart_bowl_df = sq_cohort_bowl.copy()
            highlight_id_to_plot_bw = None

            if st.session_state.sq_bowl_highlight_id:
                selected_bowl_matches = bowl_pool[bowl_pool['player_id'] == st.session_state.sq_bowl_highlight_id]
                if not selected_bowl_matches.empty:
                    bowl_row = selected_bowl_matches.iloc[0]
                    bowl_balls = int(bowl_row.get('pressure_exposure_legal_balls', bowl_row.get('pressure_exposure_balls', 0)))
                    bowl_is_qual = bool(bowl_row['is_qualified'])
                    raw_score_bw = bowl_row.get('final_composite_score')
                    has_chart_coords_bw = (bowl_balls > 0 and pd.notnull(raw_score_bw))

                    if has_chart_coords_bw:
                        bowl_score = float(raw_score_bw)
                        
                        # Dynamically append selected bowler to chart data if outside currently displayed cohort
                        # This enables instant plotting and highlighting on the scatter plot without altering baseline cohort filters
                        if st.session_state.sq_bowl_highlight_id not in chart_bowl_df['player_id'].values:
                            chart_bowl_df = pd.concat([chart_bowl_df, selected_bowl_matches], ignore_index=True)
                            
                        highlight_id_to_plot_bw = st.session_state.sq_bowl_highlight_id
                        
                        # Determine Quadrant relative to cohort median and Phase 3A prior mean (mu = 0.6210)
                        bowl_med_col = 'pressure_exposure_legal_balls' if 'pressure_exposure_legal_balls' in chart_bowl_df.columns else 'pressure_exposure_balls'
                        if len(chart_bowl_df) <= 70 and 'is_qualified' in chart_bowl_df.columns and chart_bowl_df['is_qualified'].sum() > 0:
                            bowl_med = float(chart_bowl_df[chart_bowl_df['is_qualified']][bowl_med_col].median())
                        else:
                            bowl_med = float(chart_bowl_df[bowl_med_col].median())
                        prior_mean_bowl = 0.6210
                        
                        if bowl_balls >= bowl_med and bowl_score >= prior_mean_bowl:
                            bowl_quadrant = "Proven Under Pressure"
                            bowl_quad_desc = "High Exposure · High Reliability"
                            bowl_quad_color = "#7964B5"
                            bowl_quad_bg = "#F0ECF8"
                        elif bowl_balls < bowl_med and bowl_score >= prior_mean_bowl:
                            bowl_quadrant = "Promising, Limited Exposure"
                            bowl_quad_desc = "Low Exposure · High Reliability"
                            bowl_quad_color = "#927CCB"
                            bowl_quad_bg = "#F2DCE9"
                        elif bowl_balls >= bowl_med and bowl_score < prior_mean_bowl:
                            bowl_quadrant = "Experienced but Inconsistent"
                            bowl_quad_desc = "High Exposure · Low Reliability"
                            bowl_quad_color = "#77758A"
                            bowl_quad_bg = "#ECEAF3"
                        else:
                            bowl_quadrant = "Developing Evidence"
                            bowl_quad_desc = "Low Exposure · Low Reliability"
                            bowl_quad_color = "#77758A"
                            bowl_quad_bg = "#F8F8FC"

                        if bowl_is_qual:
                            bowl_qual_badge = f"Qualified • Rank #{int(bowl_row['rank'])}" if pd.notnull(bowl_row.get('rank')) else "Qualified"
                            bowl_rel_text = f"{bowl_score:.4f}"
                            qual_context_bw_html = ""
                        else:
                            bowl_qual_badge = "Non-Qualified"
                            bowl_rel_text = f"{bowl_score:.4f}"
                            unqual_reason_bw = bowl_row.get('unqualified_reasons', 'Did not meet minimum qualification threshold')
                            qual_context_bw_html = f"""
                            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #ECEAF3; font-size: 12px; color: #77758A;">
                                <strong style="color: #555368;">Qualification Context:</strong> {unqual_reason_bw}
                            </div>
                            """

                        # Badge indicating whether overlaid or native to the selected cohort
                        is_overlaid_bw = (st.session_state.sq_bowl_highlight_id not in sq_cohort_bowl['player_id'].values)
                        overlay_badge_bw = '<span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #F2DCE9; color: #927CCB; padding: 2px 8px; border-radius: 10px;">Overlaid on Cohort</span>' if is_overlaid_bw else ''

                        render_html(f"""
                        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #7964B5; border-radius: 8px; padding: 12px 18px; margin: 12px 0 14px 0; box-shadow: 0 1px 3px rgba(37,35,58,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                                <div>
                                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 3px;">
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #F0ECF8; color: #7964B5; padding: 2px 8px; border-radius: 10px;">
                                            {bowl_qual_badge}
                                        </span>
                                        {overlay_badge_bw}
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: {bowl_quad_bg}; color: {bowl_quad_color}; padding: 2px 8px; border-radius: 10px;">
                                            {bowl_quadrant}
                                        </span>
                                    </div>
                                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #25233A;">
                                        {bowl_row['player_name']} <span style="font-size: 13px; font-weight: 500; color: #77758A;">({bowl_row['ipl_franchises']})</span>
                                    </h4>
                                    <div style="font-size: 12px; color: #77758A; margin-top: 2px;">{bowl_quad_desc}</div>
                                </div>
                                <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                                    <div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #77758A;">Pressure Exposure</div>
                                        <div style="font-size: 15px; font-weight: 700; color: #25233A;">{bowl_balls:,} balls</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #77758A;">Reliability Score</div>
                                        <div style="font-size: 15px; font-weight: 700; color: #7964B5;">{bowl_rel_text}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #77758A;">Chart Coordinates</div>
                                        <div style="font-size: 13px; font-weight: 600; color: #555368;">X: {bowl_balls}b &nbsp;|&nbsp; Y: {bowl_score:.4f}</div>
                                    </div>
                                </div>
                            </div>
                            {qual_context_bw_html}
                        </div>
                        """)
                    else:
                        # Bowler has zero pressure exposure balls (or missing reliability metrics)
                        # Do NOT plot on the scatter plot and do NOT assign arbitrary 0 coordinates
                        highlight_id_to_plot_bw = None
                        unqual_reason_bw = bowl_row.get('unqualified_reasons', 'No pressure deliveries bowled (Pressure Index >= 0.65)')
                        c_matches_bw = int(bowl_row['total_matches']) if pd.notnull(bowl_row.get('total_matches')) else 0
                        c_balls_bw = int(bowl_row['career_eligible_balls']) if pd.notnull(bowl_row.get('career_eligible_balls')) else 0
                        c_runs_bw = int(bowl_row['career_runs']) if pd.notnull(bowl_row.get('career_runs')) else 0
                        c_econ_bw = f"{float(bowl_row['career_economy_rate']):.2f}" if pd.notnull(bowl_row.get('career_economy_rate')) else "—"
                        c_avg_bw = f"{float(bowl_row['career_average']):.2f}" if pd.notnull(bowl_row.get('career_average')) else "—"
                        c_dva_bw = f"{float(bowl_row['career_cumulative_dva']):+.2f}" if pd.notnull(bowl_row.get('career_cumulative_dva')) else "—"

                        render_html(f"""
                        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-left: 4px solid #77758A; border-radius: 8px; padding: 14px 18px; margin: 12px 0 14px 0; box-shadow: 0 1px 3px rgba(37,35,58,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                                <div>
                                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #ECEAF3; color: #77758A; padding: 2px 8px; border-radius: 10px;">
                                            Non-Qualified • Zero Pressure Exposure
                                        </span>
                                        <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background: #F8F8FC; color: #77758A; padding: 2px 8px; border-radius: 10px; border: 1px solid #ECEAF3;">
                                            Cannot Plot on Pressure Chart
                                        </span>
                                    </div>
                                    <h4 style="margin: 0; font-size: 16px; font-weight: 700; color: #25233A;">
                                        {bowl_row['player_name']} <span style="font-size: 13px; font-weight: 500; color: #77758A;">({bowl_row['ipl_franchises']})</span>
                                    </h4>
                                    <div style="font-size: 13px; color: #555368; margin-top: 6px; line-height: 1.45;">
                                        This bowler has bowled <strong>0 pressure deliveries</strong> (PI &ge; 0.65) in the evaluated IPL dataset. 
                                        Because reliability under pressure requires pressure exposure to measure, this player cannot be plotted on the two-axis pressure scatter plot without introducing misleading coordinates.
                                    </div>
                                    <div style="margin-top: 8px; font-size: 12px; color: #77758A;">
                                        <strong style="color: #555368;">Qualification Reason:</strong> {unqual_reason_bw}
                                    </div>
                                </div>
                                <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap; background: #F8F8FC; padding: 10px 14px; border-radius: 6px; border: 1px solid #ECEAF3;">
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Matches</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_matches_bw}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Career Balls</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_balls_bw:,}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Runs Conceded</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_runs_bw:,}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Economy Rate</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_econ_bw}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Average</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #25233A;">{c_avg_bw}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10.5px; font-weight: 600; text-transform: uppercase; color: #77758A;">Net DVA</div>
                                        <div style="font-size: 14px; font-weight: 700; color: #7964B5;">{c_dva_bw}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """)

            # Render the Scouting Quadrant
            fig_bowl_scatter = plot_top10_reliability_scatter(
                chart_bowl_df,
                role='bowler',
                highlighted_player_id=highlight_id_to_plot_bw,
                top_n_labels=5
            )
            st.plotly_chart(fig_bowl_scatter, use_container_width=True)

    # FRANCHISE CLUTCH DISTRIBUTION TAB
    with role_tab3:
        render_html("<div style='margin-bottom: 10px;'></div>")
        qual_all = df_players[df_players['is_qualified']].copy()
        fig_fr = plot_franchise_representation(qual_all)
        st.plotly_chart(fig_fr, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 3: PLAYER SEARCH
# -----------------------------------------------------------------------------
elif st.session_state.page == "Player Search":
    col_nav_s1, col_nav_s2 = st.columns([1, 7], vertical_alignment="center")
    with col_nav_s1:
        if st.button("Back", key="back_btn_search", use_container_width=True):
            navigate_back(fallback_page="Overview")
    with col_nav_s2:
        render_html("""
            <div style="display: inline-block; background: #F0ECF8; color: #7964B5; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; padding: 3px 10px; border-radius: 14px; margin-bottom: 2px;">
                Complete IPL Talent Registry
            </div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 1.2;">
                SupeRR Selector Scouting Directory
            </h1>
        """)
    render_html("""
        <p style="color: #77758A; font-size: 0.94rem; margin-top: 6px; margin-bottom: 16px;">
            Search all 601 players evaluated in IPL 2022–2026. Inspect qualification statuses, sample volumes, and individual performance benchmarks.
        </p>
    """)

    # 5-Column Filter Bar with Clear Filters button
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns([3, 2, 2, 2, 1.2], vertical_alignment="bottom")
    with col_s1:
        search_term = st.text_input("Search Player by Name", placeholder="e.g. Virat Kohli, Bumrah, Dhoni, Russell...", key="ps_search_box")
        st.session_state.search_query = search_term
    with col_s2:
        filter_role = st.selectbox("Role", ["All Roles", "Batters Only", "Bowlers Only"], key="ps_role_box")
    with col_s3:
        all_unique_franchises = sorted(list(set([t for teams in df_players['ipl_franchises'].dropna() for t in teams.split(", ")])))
        filter_franchise = st.selectbox("Franchise", ["All Franchises"] + all_unique_franchises, key="ps_franchise_box")
    with col_s4:
        filter_qual = st.selectbox("Qualification Status", ["All Players", "Qualified Only", "Not Qualified Only"], key="ps_qual_box")
    with col_s5:
        st.button("Clear", key="ps_clear_all_btn", on_click=reset_player_search_filters, use_container_width=True)

    df_filtered_search = df_players.copy()
    if search_term:
        df_filtered_search = df_filtered_search[df_filtered_search['player_name'].str.contains(search_term, case=False, na=False)]
    if filter_role == "Batters Only":
        df_filtered_search = df_filtered_search[df_filtered_search['role'] == 'batter']
    elif filter_role == "Bowlers Only":
        df_filtered_search = df_filtered_search[df_filtered_search['role'] == 'bowler']

    if filter_franchise != "All Franchises":
        df_filtered_search = df_filtered_search[df_filtered_search['ipl_franchises'].str.contains(filter_franchise, na=False)]

    if filter_qual == "Qualified Only":
        df_filtered_search = df_filtered_search[df_filtered_search['is_qualified']]
    elif filter_qual == "Not Qualified Only":
        df_filtered_search = df_filtered_search[~df_filtered_search['is_qualified']]

    # Results Count and Export
    col_cnt_s, col_exp_s = st.columns([3, 1])
    with col_cnt_s:
        render_html(f"<div style='font-size: 0.88rem; color: #77758A; padding-top: 6px;'>Showing <strong>{len(df_filtered_search)}</strong> of 601 players in registry.</div>")
    with col_exp_s:
        csv_search = df_filtered_search.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv_search,
            "supeRR_selector_player_search.csv",
            "text/csv",
            use_container_width=True,
            key="dl_search_csv_btn"
        )

    if df_filtered_search.empty:
        st.info("No players matched the selected search filters.")
    else:
        # Quick Scouting Discovery Cards (Top matching results)
        if search_term or len(df_filtered_search) <= 6:
            render_html("<div style='font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #7964B5; margin-bottom: 8px;'>Scouting Talent Cards</div>")
            sc_cards = df_filtered_search.head(6)
            n_cards = len(sc_cards)
            sc_cols = st.columns(min(n_cards, 3))
            for i, (_, row_item) in enumerate(sc_cards.iterrows()):
                with sc_cols[i % len(sc_cols)]:
                    render_scouting_card(row_item)
            render_html("<div style='margin-top: 12px;'></div>")

        # Avoid duplicate index issues: index each unique entry cleanly
        options_indices = df_filtered_search.index.tolist()
        if "ps_select_player_box" in st.session_state and options_indices:
            if st.session_state.ps_select_player_box not in options_indices:
                st.session_state.ps_select_player_box = options_indices[0]
        saved_ps_idx = st.session_state.get("ps_selected_idx", options_indices[0] if options_indices else 0)
        idx_pos = options_indices.index(saved_ps_idx) if saved_ps_idx in options_indices else 0
        selected_idx = st.selectbox(
            "Select player to inspect complete analytics dossier:",
            options=options_indices,
            index=idx_pos,
            format_func=lambda idx: f"{df_filtered_search.loc[idx if idx in df_filtered_search.index else options_indices[0], 'player_name']} ({df_filtered_search.loc[idx if idx in df_filtered_search.index else options_indices[0], 'role'].capitalize()} • {df_filtered_search.loc[idx if idx in df_filtered_search.index else options_indices[0], 'ipl_franchises']})" if options_indices else "",
            key="ps_select_player_box"
        )
        st.session_state.ps_selected_idx = selected_idx

        p_row = df_filtered_search.loc[selected_idx] if selected_idx in df_filtered_search.index else df_filtered_search.iloc[0]

        player_header_card(p_row)
        status_badge(
            p_row['is_qualified'],
            rank=p_row['rank'],
            score=p_row['final_composite_score'],
            reasons=p_row['unqualified_reasons'],
            role=p_row['role']
        )

        col_st1, col_st2, col_st3, col_st4 = st.columns(4)
        if p_row['role'] == 'batter':
            with col_st1:
                metric_card("Career IPL Balls", f"{int(p_row['career_eligible_balls']):,}", f"{int(p_row['career_runs']):,} runs (SR: {p_row['career_strike_rate']:.1f})", variant='blue', icon='activity')
            with col_st2:
                metric_card("Pressure Balls Faced", f"{int(p_row['pressure_exposure_balls']):,}", f"{int(p_row['pressure_runs']):,} runs in {int(p_row['pressure_matches'])} matches", variant='pink', icon='pulse')
            with col_st3:
                sr_val = f"{p_row['pressure_strike_rate']:.1f}" if pd.notnull(p_row['pressure_strike_rate']) else "N/A"
                metric_card("Pressure Strike Rate", sr_val, delta=p_row['delta_strike_rate'], delta_positive=(p_row['delta_strike_rate'] or 0) > 0, variant='lavender', icon='target')
            with col_st4:
                psr_val = f"{p_row['raw_psr']*100:.1f}%" if pd.notnull(p_row['raw_psr']) else "0.0%"
                metric_card("Pressure Success Rate", psr_val, f"{int(p_row['successful_matches'])} wins in {int(p_row['psr_qualifying_matches'])} qual matches", variant='purple', icon='award')
        else:
            with col_st1:
                metric_card("Career Legal Balls", f"{int(p_row['career_eligible_balls']):,}", f"{int(p_row['career_dismissals'])} wkts (Econ: {p_row['career_economy_rate']:.2f})", variant='blue', icon='activity')
            with col_st2:
                metric_card("Pressure Legal Balls", f"{int(p_row['pressure_exposure_balls']):,}", f"{int(p_row['pressure_dismissals'])} wkts in {int(p_row['pressure_matches'])} matches", variant='pink', icon='pulse')
            with col_st3:
                econ_val = f"{p_row['pressure_economy_rate']:.2f}" if pd.notnull(p_row['pressure_economy_rate']) else "N/A"
                metric_card("Pressure Economy", econ_val, delta=p_row['clutch_econ_suppression'], delta_positive=(p_row['clutch_econ_suppression'] or 0) > 0, variant='lavender', icon='target')
            with col_st4:
                psr_val = f"{p_row['raw_psr']*100:.1f}%" if pd.notnull(p_row['raw_psr']) else "0.0%"
                metric_card("Pressure Success Rate", psr_val, f"{int(p_row['successful_matches'])} wins in {int(p_row['psr_qualifying_matches'])} qual matches", variant='purple', icon='award')

        # Visualizations for Player Search Page
        render_html("<div style='margin-top: 14px;'></div>")
        col_ps_chart1, col_ps_chart2 = st.columns([1, 2])
        with col_ps_chart1:
            fig_gauge = plot_reliability_gauge(p_row['final_composite_score'], p_row['rank'], p_row['is_qualified'], p_row['role'])
            st.plotly_chart(fig_gauge, use_container_width=True)
        with col_ps_chart2:
            if p_row['role'] == 'batter':
                fig_comp = plot_career_vs_pressure_batter(p_row)
            else:
                fig_comp = plot_career_vs_pressure_bowler(p_row)
            st.plotly_chart(fig_comp, use_container_width=True)

        # Match Timeline
        df_hist_search = load_player_match_history(player_id=p_row['player_id'], role=p_row['role'])
        if not df_hist_search.empty:
            df_hist_search_press = df_hist_search[df_hist_search['is_pressure_involved']].copy()
            if not df_hist_search_press.empty:
                fig_timeline_s = plot_match_timeline(df_hist_search_press, p_row['role'])
                st.plotly_chart(fig_timeline_s, use_container_width=True)

        render_html("<div style='margin-top: 14px;'></div>")
        target_page = "Batter Analysis" if p_row['role'] == 'batter' else "Bowler Analysis"
        if st.button(f"Open Complete Analytics Dossier for {p_row['player_name']}", use_container_width=True, key=f"btn_open_dossier_{p_row['player_id']}"):
            navigate_to(target_page, player_id=p_row['player_id'], role=p_row['role'], origin_page="Player Search")


# -----------------------------------------------------------------------------
# PAGE 4: BATTER ANALYSIS
# -----------------------------------------------------------------------------
elif st.session_state.page == "Batter Analysis":
    col_nav_b1, col_nav_b2 = st.columns([1, 7], vertical_alignment="center")
    with col_nav_b1:
        if st.button("Back", key="back_btn_bat", use_container_width=True):
            navigate_back(fallback_page="Overview")
    with col_nav_b2:
        render_html("<h1 style='margin:0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 40px;'>Deep-Dive Batter Analysis</h1>")
        
    batters_list = df_players[df_players['role'] == 'batter'].sort_values('player_name').copy()
    cur_bat_id = st.session_state.selected_batter_id
    if cur_bat_id not in batters_list['player_id'].values:
        cur_bat_id = 4708  # Rinku Singh fallback
        st.session_state.selected_batter_id = 4708
        
    selected_batter_idx = int(batters_list['player_id'].tolist().index(cur_bat_id))
    selected_b_id = st.selectbox(
        "Select Batter to Inspect:",
        options=batters_list['player_id'].tolist(),
        index=selected_batter_idx,
        format_func=lambda x: f"{batters_list[batters_list['player_id']==x]['player_name'].values[0]} ({batters_list[batters_list['player_id']==x]['ipl_franchises'].values[0]})"
    )
    if selected_b_id != cur_bat_id:
        st.session_state.selected_batter_id = selected_b_id
        st.rerun()
        
    p_row = batters_list[batters_list['player_id'] == selected_b_id].iloc[0]
    
    # Preload player phase and match history
    df_phase = load_player_phase_breakdown(player_id=selected_b_id, role='batter')
    df_hist = load_player_match_history(player_id=selected_b_id, role='batter')
    df_hist_press = df_hist[df_hist['is_pressure_involved']].copy() if not df_hist.empty else pd.DataFrame()
    
    # Statistical summary data dictionary
    stats_data_batter = {
        "Metric": [
            "Balls Faced", "Runs Scored", "Dismissals", "Batting Average", 
            "Strike Rate", "Fours", "Sixes", "Boundary %", "Dot Ball %", 
            "Cumulative DVA", "DVA per Ball"
        ],
        "Baseline (Low / Non-Pressure)": [
            f"{int(p_row.get('baseline_eligible_balls', 0)):,}",
            f"{int(p_row.get('baseline_runs', 0)):,}",
            "-", "-",
            f"{p_row['baseline_strike_rate']:.2f}" if pd.notnull(p_row.get('baseline_strike_rate')) else "N/A",
            "-", "-", "-", "-", "-",
            f"{p_row['baseline_dva_per_ball']:+.4f}" if pd.notnull(p_row.get('baseline_dva_per_ball')) else "N/A"
        ],
        "High Pressure (PI >= 0.65)": [
            f"{int(p_row.get('pressure_exposure_balls', 0)):,}",
            f"{int(p_row.get('pressure_runs', 0)):,}",
            f"{int(p_row.get('pressure_dismissals', 0))}",
            f"{p_row['pressure_average']:.2f}" if pd.notnull(p_row.get('pressure_average')) else ("Not Dismissed" if p_row.get('pressure_dismissals', 0) == 0 else "N/A"),
            f"{p_row['pressure_strike_rate']:.2f}" if pd.notnull(p_row.get('pressure_strike_rate')) else "N/A",
            f"{int(p_row.get('pressure_fours', 0))}",
            f"{int(p_row.get('pressure_sixes', 0))}",
            f"{p_row['pressure_boundary_pct']:.2f}%" if pd.notnull(p_row.get('pressure_boundary_pct')) else "N/A",
            f"{p_row['pressure_dot_pct']:.2f}%" if pd.notnull(p_row.get('pressure_dot_pct')) else "N/A",
            f"{p_row['pressure_cumulative_dva']:+.4f}" if pd.notnull(p_row.get('pressure_cumulative_dva')) else "N/A",
            f"{p_row['pressure_dva_per_ball']:+.4f}" if pd.notnull(p_row.get('pressure_dva_per_ball')) else "N/A"
        ],
        "Delta / Impact": [
            "-", "-", "-", "-",
            f"{p_row['delta_strike_rate']:+.2f}" if pd.notnull(p_row.get('delta_strike_rate')) else "N/A",
            "-", "-", "-", "-", "-",
            f"{p_row['delta_dva_per_ball']:+.4f}" if pd.notnull(p_row.get('delta_dva_per_ball')) else "N/A"
        ]
    }
    
    # Top Player Header Card & Status Badge
    player_header_card(p_row)
    status_badge(
        p_row['is_qualified'],
        rank=p_row['rank'],
        score=p_row['final_composite_score'],
        reasons=p_row['unqualified_reasons'],
        role='batter'
    )
    
    # Five Unified Tabs
    batter_tab_list = [
        "Player Overview",
        "Performance Analysis",
        "Player Comparison Studio",
        "Match Pressure Explorer",
        "Player Scouting Report"
    ]
    bat_def_tab = st.session_state.get("batter_active_tab", "Player Overview")
    if bat_def_tab not in batter_tab_list:
        bat_def_tab = "Player Overview"
    tab_overview, tab_perf, tab_comp, tab_match, tab_scout = st.tabs(
        batter_tab_list,
        default=bat_def_tab,
        key="batter_analysis_tabs_container"
    )
    
    # ---------------- TAB 1: PLAYER OVERVIEW ----------------
    with tab_overview:
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            sr_val = f"{p_row['pressure_strike_rate']:.1f}" if pd.notnull(p_row.get('pressure_strike_rate')) else "N/A"
            metric_card("Pressure Strike Rate", sr_val, delta=p_row.get('delta_strike_rate'), delta_positive=(p_row.get('delta_strike_rate') or 0) > 0, variant='pink', icon='pulse')
        with col_k2:
            dva_val = f"{p_row['pressure_cumulative_dva']:+.1f}" if pd.notnull(p_row.get('pressure_cumulative_dva')) else "0.0"
            dva_sub = f"{p_row['pressure_dva_per_ball']:+.2f} per ball" if pd.notnull(p_row.get('pressure_dva_per_ball')) else ""
            metric_card("Pressure DVA Contributed", dva_val, dva_sub, variant='lavender', icon='chart')
        with col_k3:
            psr_val = f"{p_row['raw_psr']*100:.1f}%" if pd.notnull(p_row.get('raw_psr')) else "0.0%"
            exp_sub = f"Exposure PSR: {p_row['exposure_weighted_psr']*100:.1f}%" if pd.notnull(p_row.get('exposure_weighted_psr')) else "Not Qualified"
            metric_card("Pressure Success Rate", psr_val, exp_sub, variant='rose', icon='award')
        with col_k4:
            bdry_val = f"{p_row['pressure_boundary_pct']:.1f}%" if pd.notnull(p_row.get('pressure_boundary_pct')) else "N/A"
            dot_sub = f"Dot Ball Rate: {p_row['pressure_dot_pct']:.1f}%" if pd.notnull(p_row.get('pressure_dot_pct')) else ""
            metric_card("Pressure Boundary %", bdry_val, dot_sub, variant='purple', icon='target')

        render_html("<div style='margin-top: 14px;'></div>")
        col_ov_c1, col_ov_c2 = st.columns([1, 2])
        with col_ov_c1:
            fig_gauge = plot_reliability_gauge(p_row.get('final_composite_score'), p_row.get('rank'), p_row.get('is_qualified'), 'batter')
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.caption("Shrunk Bayesian composite reliability score with empirical penalty adjustment.")
        with col_ov_c2:
            fig_career = plot_career_vs_pressure_batter(p_row)
            st.plotly_chart(fig_career, use_container_width=True)
            st.caption("Career Baseline vs High-Pressure (PI >= 0.65) strike rate and delivery sample volume.")
            
        if p_row.get('is_qualified'):
            insight_box(
                "Phase 3A Analytical Assessment",
                [
                    f"Overall Reliability Index: {p_row['final_composite_score']:.4f} (Rank {int(p_row['rank'])}) across {int(p_row['pressure_exposure_balls'])} high-pressure deliveries.",
                    f"Clutch Acceleration: Pressure SR {p_row['pressure_strike_rate']:.1f} representing a {p_row['delta_strike_rate']:+.1f} surge over career baseline.",
                    f"Winning Inning Conversion: {int(p_row['successful_matches'])} pressure-successful matches out of {int(p_row['psr_qualifying_matches'])} qualifying outings (PSR: {p_row['raw_psr']*100:.1f}%)."
                ],
                variant='lavender'
            )
        else:
            insight_box(
                "Sample Gate Status & Observational Audit",
                [
                    f"Qualification Status: Player is currently unranked ({p_row.get('unqualified_reasons', 'Insufficient sample size')}).",
                    f"Current Exposure: {int(p_row.get('pressure_exposure_balls', 0))} pressure balls faced across {int(p_row.get('psr_qualifying_matches', p_row.get('pressure_matches', 0)))} qualifying matches (Minimum required: 60 balls & 6 matches).",
                    "Data Integrity Guard: Statistics are recorded purely on empirical deliveries without prior shrinkage distortion."
                ],
                variant='pink'
            )

    # ---------------- TAB 2: PERFORMANCE ANALYSIS ----------------
    with tab_perf:
        col_bv1, col_bv2 = st.columns(2)
        with col_bv1:
            fig_sr = plot_batter_strike_rate_chart(p_row)
            st.plotly_chart(fig_sr, use_container_width=True)
            st.caption("Batting Strike Rate: Baseline vs High-Pressure scoring pace (Runs per 100 Balls).")
        with col_bv2:
            fig_avg = plot_batter_average_chart(p_row)
            st.plotly_chart(fig_avg, use_container_width=True)
            st.caption("Batting Average: Baseline vs High-Pressure dismissal resistance (Runs per Dismissal).")

        render_html("<div style='margin-top: 14px;'></div>")
        fig_dva_b = plot_dva_breakdown(p_row)
        st.plotly_chart(fig_dva_b, use_container_width=True)
        st.caption("Delivery Value Added (DVA): Net runs scored above expected value per ball and cumulative match impact.")

        render_html("<h4 style='font-size: 1.05rem; margin-top: 18px; color: #25233A;'>Statistical Summary: Baseline vs High Pressure</h4>")
        render_stats_summary_table(stats_data_batter, role='batter')

        render_html("<h4 style='font-size: 1.05rem; margin-top: 18px; color: #25233A;'>Match Phase Performance Breakdown</h4>")
        if not df_phase.empty:
            col_ph1, col_ph2 = st.columns([3, 2])
            with col_ph1:
                fig_ph = plot_phase_comparison(df_phase, 'batter')
                st.plotly_chart(fig_ph, use_container_width=True)
                st.caption("Strike rate and ball volume breakdown across Powerplay (1-6), Middle (7-15), and Death (16-20) overs.")
            with col_ph2:
                tbl_phase = df_phase[['phase', 'overall_balls', 'overall_metric', 'pressure_balls', 'pressure_metric', 'pressure_dva']].rename(columns={
                    'phase': 'Phase',
                    'overall_balls': 'Total Balls',
                    'overall_metric': 'Base SR',
                    'pressure_balls': 'Press Balls',
                    'pressure_metric': 'Press SR',
                    'pressure_dva': 'Press DVA'
                })
                st.dataframe(tbl_phase.style.format({
                    'Total Balls': '{:.0f}',
                    'Base SR': '{:.1f}',
                    'Press Balls': '{:.0f}',
                    'Press SR': '{:.1f}',
                    'Press DVA': '{:+.2f}'
                }), use_container_width=True, hide_index=True)
        else:
            st.info("No phase breakdown recorded for this player.")

        render_html("<h4 style='font-size: 1.05rem; margin-top: 18px; color: #25233A;'>Match-by-Match Pressure Performance Timeline</h4>")
        if not df_hist.empty:
            if not df_hist_press.empty:
                fig_time = plot_match_timeline(df_hist_press, 'batter')
                st.plotly_chart(fig_time, use_container_width=True)
                st.caption("Chronological match progression showing strike rate and binary PSR qualification outcome.")
                
                cols_hist = [
                    'match_date', 'season', 'away_team', 'pressure_eligible_balls', 
                    'pressure_runs', 'pressure_wickets_or_dismissals', 
                    'pressure_metric', 'pressure_dva', 'is_successful_pressure_match'
                ]
                tbl_hist = df_hist_press[cols_hist].rename(columns={
                    'match_date': 'Date',
                    'season': 'Season',
                    'away_team': 'Opponent',
                    'pressure_eligible_balls': 'Balls Faced',
                    'pressure_runs': 'Runs',
                    'pressure_wickets_or_dismissals': 'Dismissed',
                    'pressure_metric': 'Strike Rate',
                    'pressure_dva': 'Net DVA',
                    'is_successful_pressure_match': 'Success'
                }).sort_values('Date', ascending=False)
                
                st.dataframe(
                    tbl_hist.style.format({
                        'Balls Faced': '{:.0f}',
                        'Runs': '{:.0f}',
                        'Dismissed': '{:.0f}',
                        'Strike Rate': '{:.1f}',
                        'Net DVA': '{:+.2f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Player has participated in matches, but faced 0 high-pressure deliveries.")
        else:
            st.info("No match history available.")

    # ---------------- TAB 3: PLAYER COMPARISON STUDIO ----------------
    with tab_comp:
        render_html("<h2 style='margin:0 0 6px 0; font-size: 20px; font-weight: 600; color:#25233A;'>Side-by-Side Batter Comparison Studio</h2>")
        st.markdown(
            "<div style='font-size:0.84rem; color:#77758A; margin-bottom:14px;'>"
            "Independent comparison workspace. Benchmarking 2 or 3 batters updates the view in place without redirecting or altering individual player profiles."
            "</div>",
            unsafe_allow_html=True
        )
        
        # Format map for robust display across comparisons
        batters_format_map = {
            int(row['player_id']): f"{row['player_name']} ({str(row.get('ipl_franchises', '')).split(',')[0].strip()})"
            for _, row in batters_list.iterrows()
        }
        bat_name_to_id = {v: k for k, v in batters_format_map.items()}
        def format_batter(x):
            if isinstance(x, str):
                return x
            return batters_format_map.get(int(x), f"Player {x}")
        
        # State variables for comparison
        b_p1_id = st.session_state.get('comp_bat_p1_id', 4708)
        if b_p1_id not in batters_list['player_id'].values:
            b_p1_id = int(batters_list['player_id'].iloc[0])
            st.session_state.comp_bat_p1_id = b_p1_id
            
        p1_idx = int(batters_list['player_id'].tolist().index(b_p1_id))
        
        comp_col1, comp_col2, comp_col3 = st.columns([3, 3, 2], vertical_alignment="bottom")
        with comp_col1:
            raw_b_p1 = st.selectbox(
                "Player 1:",
                options=batters_list['player_id'].tolist(),
                index=p1_idx,
                format_func=format_batter,
                key="comp_bat_p1_select",
                on_change=set_batter_active_tab,
                args=("Player Comparison Studio",)
            )
            new_b_p1 = bat_name_to_id.get(raw_b_p1, raw_b_p1) if isinstance(raw_b_p1, str) else int(raw_b_p1)
            if new_b_p1 != b_p1_id:
                st.session_state.comp_bat_p1_id = new_b_p1
                st.session_state.comp_player_1_id = new_b_p1
                st.session_state.batter_active_tab = "Player Comparison Studio"
                b_p1_id = new_b_p1
                
        p1_row = batters_list[batters_list['player_id'] == b_p1_id].iloc[0]
        
        other_batters = batters_list[batters_list['player_id'] != b_p1_id].copy()
        b_p2_id = st.session_state.get('comp_bat_p2_id', 4016)
        if b_p2_id not in other_batters['player_id'].values:
            qual_peers = other_batters[other_batters['is_qualified']]['player_id'].tolist()
            b_p2_id = qual_peers[0] if qual_peers else int(other_batters['player_id'].iloc[0])
            st.session_state.comp_bat_p2_id = b_p2_id
            
        p2_idx = int(other_batters['player_id'].tolist().index(b_p2_id))
        with comp_col2:
            raw_b_p2 = st.selectbox(
                "Compare with Player 2:",
                options=other_batters['player_id'].tolist(),
                index=p2_idx,
                format_func=format_batter,
                key="comp_bat_p2_select",
                on_change=set_batter_active_tab,
                args=("Player Comparison Studio",)
            )
            new_b_p2 = bat_name_to_id.get(raw_b_p2, raw_b_p2) if isinstance(raw_b_p2, str) else int(raw_b_p2)
            if new_b_p2 != b_p2_id:
                st.session_state.comp_bat_p2_id = new_b_p2
                st.session_state.comp_player_2_id = new_b_p2
                st.session_state.batter_active_tab = "Player Comparison Studio"
                b_p2_id = new_b_p2
                
        p2_row = other_batters[other_batters['player_id'] == b_p2_id].iloc[0]
        
        with comp_col3:
            add_p3 = st.checkbox(
                "Add 3rd Batter",
                value=st.session_state.get("comp_bat_enable_p3", False),
                key="comp_bat_p3_toggle",
                on_change=set_batter_active_tab,
                args=("Player Comparison Studio",)
            )
            st.session_state.comp_bat_enable_p3 = add_p3
            st.session_state.comp_enable_p3 = add_p3
            st.session_state.batter_active_tab = "Player Comparison Studio"
            p3_row = None
            if add_p3:
                p3_candidates = other_batters[other_batters['player_id'] != b_p2_id].copy()
                b_p3_id = st.session_state.get('comp_bat_p3_id', None)
                if b_p3_id not in p3_candidates['player_id'].values:
                    b_p3_id = int(p3_candidates['player_id'].iloc[0])
                    st.session_state.comp_bat_p3_id = b_p3_id
                p3_idx = int(p3_candidates['player_id'].tolist().index(b_p3_id))
                raw_b_p3 = st.selectbox(
                    "Player 3:",
                    options=p3_candidates['player_id'].tolist(),
                    index=p3_idx,
                    format_func=format_batter,
                    key="comp_bat_p3_select",
                    on_change=set_batter_active_tab,
                    args=("Player Comparison Studio",)
                )
                new_b_p3 = bat_name_to_id.get(raw_b_p3, raw_b_p3) if isinstance(raw_b_p3, str) else int(raw_b_p3)
                if new_b_p3 != b_p3_id:
                    st.session_state.comp_bat_p3_id = new_b_p3
                    st.session_state.comp_player_3_id = new_b_p3
                    st.session_state.batter_active_tab = "Player Comparison Studio"
                    b_p3_id = new_b_p3
                p3_row = p3_candidates[p3_candidates['player_id'] == b_p3_id].iloc[0]

        players_comp_list = [p1_row, p2_row]
        if p3_row is not None:
            players_comp_list.append(p3_row)
            
        # Action buttons: Open Player Profile explicitly
        act_cols = st.columns(len(players_comp_list))
        for idx_p, p_item in enumerate(players_comp_list):
            with act_cols[idx_p]:
                if st.button(
                    f"Open Profile: {p_item['player_name']}",
                    key=f"btn_open_prof_bat_{p_item['player_id']}",
                    use_container_width=True
                ):
                    navigate_to("Batter Analysis", player_id=p_item['player_id'], role='batter', from_tab="Player Comparison Studio", origin_page="Batter Analysis")

        # Comparison KPI Summary Cards
        render_comparison_summary(players_comp_list, role='batter')
        
        # 1) Rebuilt Benchmark Comparison across 3 dedicated vertical containers
        render_player_comparison_benchmarks(players_comp_list, role='batter')
        
        # 2) One compact comparison table showing exact values
        render_comparison_data_table(players_comp_list, role='batter')
        
        # 3) One phase-wise comparison chart where data is available
        phase_dict_b = {}
        for p in players_comp_list:
            df_ph_p = load_player_phase_breakdown(p['player_id'], 'batter')
            phase_dict_b[p['player_name']] = df_ph_p
        fig_cp_ph = plot_player_comparison_phase(phase_dict_b, role='batter')
        st.plotly_chart(fig_cp_ph, use_container_width=True)
        st.caption("Phase breakdown of pressure strike rate across Powerplay (1-6), Middle (7-15), and Death (16-20) overs. Parentheses show balls faced (b); asterisk (*) marks sample < 10 balls.")

    # ---------------- TAB 4: MATCH PRESSURE EXPLORER ----------------
    with tab_match:
        render_html("<h2 style='margin:0 0 12px 0; font-size: 20px; font-weight: 600; color:#25233A;'>Match Pressure Dynamics & Delivery Inspector</h2>")
        
        df_all_matches = load_ipl_matches()
        
        col_mf1, col_mf2 = st.columns([1, 2])
        with col_mf1:
            filter_mode = st.radio(
                "Match Scope:",
                ["Matches with " + p_row['player_name'], "All IPL Matches (2022-2026)"],
                index=0,
                key="bat_match_scope",
                on_change=set_batter_active_tab,
                args=("Match Pressure Explorer",)
            )
        with col_mf2:
            seasons_avail = ["All Seasons"] + sorted(df_all_matches['season'].astype(str).unique().tolist())
            sel_season = st.selectbox(
                "Filter Season:",
                options=seasons_avail,
                index=0,
                key="bat_match_season",
                on_change=set_batter_active_tab,
                args=("Match Pressure Explorer",)
            )
            
        if filter_mode.startswith("Matches with"):
            if not df_hist.empty and 'match_id' in df_hist.columns:
                player_mids = set(df_hist['match_id'].unique().tolist())
            else:
                p_delivs = load_player_match_deliveries(selected_b_id, role='batter')
                player_mids = set(p_delivs['match_id'].unique().tolist()) if not p_delivs.empty else set()
                
            filtered_matches = df_all_matches[df_all_matches['match_id'].isin(player_mids)].copy()
            if filtered_matches.empty:
                filtered_matches = df_all_matches.copy()
        else:
            filtered_matches = df_all_matches.copy()
            
        if sel_season != "All Seasons":
            filtered_matches = filtered_matches[filtered_matches['season'].astype(str) == sel_season]
            
        if filtered_matches.empty:
            st.warning("No matches found matching the selected filters.")
        else:
            filtered_matches = filtered_matches.sort_values('match_date', ascending=False)
            match_options = filtered_matches['match_id'].tolist()
            
            sel_match_id = st.selectbox(
                "Select Match to Explore:",
                options=match_options,
                format_func=lambda x: f"{filtered_matches[filtered_matches['match_id']==x]['match_date'].values[0]} - {filtered_matches[filtered_matches['match_id']==x]['home_team'].values[0]} vs {filtered_matches[filtered_matches['match_id']==x]['away_team'].values[0]} (IPL {filtered_matches[filtered_matches['match_id']==x]['season'].values[0]}, Match {x})",
                key="bat_sel_match",
                on_change=set_batter_active_tab,
                args=("Match Pressure Explorer",)
            )
            
            selected_match_row = filtered_matches[filtered_matches['match_id'] == sel_match_id].iloc[0]
            df_match_delivs = load_ipl_deliveries(match_id=sel_match_id)
            
            # Match Overview & Player Impact Card
            render_match_overview_card(selected_match_row, df_match_delivs, player_id=selected_b_id, role='batter')
            
            # Over-by-Over Timeline
            fig_match_over = plot_match_over_pressure_timeline(df_match_delivs, selected_match_row, player_id=selected_b_id, role='batter')
            st.plotly_chart(fig_match_over, use_container_width=True)
            st.caption("Over-by-over leverage timeline showing run progression, wickets, and delivery pressure index.")
            
            # Ball-by-Ball Inspection
            render_html("<h4 style='font-size:1.05rem; margin-top:16px; color:#25233A;'>Delivery-Level Leverage & Value Added Inspection</h4>")
            deliv_filter = st.radio(
                "Filter Deliveries:",
                ["High Pressure Deliveries Only (PI >= 0.65)", f"{p_row['player_name']} Deliveries Only", "All Deliveries in Match"],
                horizontal=True,
                key="bat_deliv_filter",
                on_change=set_batter_active_tab,
                args=("Match Pressure Explorer",)
            )
            
            df_table_delivs = df_match_delivs.copy()
            if deliv_filter.startswith("High Pressure"):
                df_table_delivs = df_table_delivs[df_table_delivs['pressure_index'] >= 0.65]
            elif deliv_filter.startswith(p_row['player_name']):
                df_table_delivs = df_table_delivs[df_table_delivs['striker_id'] == selected_b_id]
                
            if df_table_delivs.empty:
                st.info("No deliveries match the selected delivery filter.")
            else:
                cols_to_show = [
                    'innings', 'overid', 'over_ball_num', 'striker_name', 'bowler_name', 
                    'runs', 'delivery_total_runs', 'is_wicket', 'pressure_index', 'pressure_tier', 'dva_batter'
                ]
                df_disp_delivs = df_table_delivs[cols_to_show].rename(columns={
                    'innings': 'Inn',
                    'overid': 'Over',
                    'over_ball_num': 'Ball',
                    'striker_name': 'Striker',
                    'bowler_name': 'Bowler',
                    'runs': 'Runs',
                    'delivery_total_runs': 'Total',
                    'is_wicket': 'Wkt',
                    'pressure_index': 'PI',
                    'pressure_tier': 'Tier',
                    'dva_batter': 'Batter DVA'
                }).sort_values(['Inn', 'Over', 'Ball'])
                
                st.dataframe(
                    df_disp_delivs.style.format({
                        'Inn': '{:.0f}',
                        'Over': '{:.0f}',
                        'Ball': '{:.0f}',
                        'Runs': '{:.0f}',
                        'Total': '{:.0f}',
                        'PI': '{:.3f}',
                        'Batter DVA': '{:+.3f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )

    # ---------------- TAB 5: PLAYER SCOUTING REPORT ----------------
    with tab_scout:
        col_sc_h1, col_sc_h2 = st.columns([3, 1], vertical_alignment="center")
        with col_sc_h1:
            render_html(f"""
            <div>
                <span style="background: #F2DCE9; color: #D58DB5; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; padding: 2px 8px; border-radius: 6px;">
                    Confidential Scouting Intelligence
                </span>
                <h2 style="margin: 4px 0 0 0; font-size: 20px; font-weight: 600; color: #25233A;">
                    {p_row['player_name']} - Executive Scouting Dossier
                </h2>
                <div style="font-size: 0.82rem; color: #77758A;">
                    Complete 14-Section Performance Evaluation | IPL 2022-2026 Coverage
                </div>
            </div>
            """)
        with col_sc_h2:
            pdf_bytes = generate_scouting_pdf(
                p_row,
                stats_data=stats_data_batter,
                phase_df=df_phase,
                match_history_df=df_hist,
                role='batter'
            )
            safe_player_file = p_row['player_name'].replace(' ', '_')
            st.download_button(
                label="Download Executive PDF Dossier",
                data=pdf_bytes,
                file_name=f"SupeRR_Scouting_Report_{safe_player_file}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="bat_scout_pdf_btn"
            )
            
        render_html("<div style='margin-top: 14px;'></div>")
        
        # Section 1: Executive Summary & Reliability Rating
        render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-top: 3px solid #D58DB5; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #D58DB5;">Section 1: Executive Reliability Summary</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #25233A; margin: 4px 0 8px 0;">
                {'Rank ' + str(int(p_row['rank'])) + ' Reliable IPL Batter' if p_row['is_qualified'] else 'Sample Gate Unranked Batter'}
            </div>
            <div style="font-size: 0.86rem; color: #37324B; line-height: 1.5;">
                {p_row['player_name']} has accumulated <strong>{int(p_row.get('career_eligible_balls', 0)):,}</strong> career IPL deliveries across <strong>{int(p_row.get('total_matches', 0))}</strong> matches for {p_row.get('ipl_franchises', 'IPL')}.
                Under Phase 3A high-pressure conditions (PI &ge; 0.65), the batter recorded <strong>{int(p_row.get('pressure_exposure_balls', 0))}</strong> deliveries across <strong>{int(p_row.get('psr_qualifying_matches', p_row.get('pressure_matches', 0)))}</strong> qualifying match situations.
                Official Reliability Index: <strong>{f"{p_row['final_composite_score']:.4f}" if p_row['is_qualified'] else "Withheld (Sample Gate)"}</strong>.
            </div>
        </div>
        """)
        
        # Section 2 & 3: Four Core Benchmarks Grid
        col_sc_b1, col_sc_b2, col_sc_b3, col_sc_b4 = st.columns(4)
        with col_sc_b1:
            metric_card("Pressure Strike Rate", f"{p_row['pressure_strike_rate']:.1f}" if pd.notnull(p_row.get('pressure_strike_rate')) else "N/A", f"Career: {p_row.get('career_strike_rate', 0.0):.1f}", delta=p_row.get('delta_strike_rate'), delta_positive=(p_row.get('delta_strike_rate') or 0) > 0, variant='pink')
        with col_sc_b2:
            metric_card("Pressure Average", f"{p_row['pressure_average']:.1f}" if (pd.notnull(p_row.get('pressure_average')) and p_row.get('pressure_average', 0) > 0) else "N/A", f"{int(p_row.get('pressure_dismissals', 0))} Dismissals", variant='lavender')
        with col_sc_b3:
            metric_card("Net Pressure DVA", f"{p_row.get('pressure_cumulative_dva', 0.0):+.2f}", f"{p_row.get('pressure_dva_per_ball', 0.0):+.3f}/ball", delta_positive=(p_row.get('pressure_cumulative_dva') or 0) >= 0, variant='rose')
        with col_sc_b4:
            metric_card("PSR Execution Rate", f"{p_row.get('raw_psr', 0.0)*100:.1f}%", f"{int(p_row.get('successful_matches', 0))} of {int(p_row.get('psr_qualifying_matches', 0))} wins", variant='purple')
            
        render_html("<div style='margin-top: 14px;'></div>")
        
        # Section 4: Performance Dimension Breakdown
        render_html("<h4 style='font-size: 1.05rem; margin-top: 10px; color: #25233A;'>Section 4: Baseline vs Pressure Empirical Breakdown</h4>")
        render_stats_summary_table(stats_data_batter, role='batter')
        
        # Section 5 & 6: Phase & Tactical Strengths
        col_sc_ph1, col_sc_ph2 = st.columns(2)
        with col_sc_ph1:
            render_html("<h4 style='font-size: 1.05rem; margin-top: 10px; color: #25233A;'>Section 5: Phase Leverage Distribution</h4>")
            if not df_phase.empty:
                st.dataframe(df_phase[['phase', 'overall_balls', 'overall_metric', 'pressure_balls', 'pressure_metric', 'pressure_dva']].rename(columns={
                    'phase': 'Phase', 'overall_balls': 'Total Balls', 'overall_metric': 'Career SR', 'pressure_balls': 'Press Balls', 'pressure_metric': 'Press SR', 'pressure_dva': 'Press DVA'
                }), use_container_width=True, hide_index=True)
            else:
                st.info("No phase breakdown recorded.")
        with col_sc_ph2:
            render_html("<h4 style='font-size: 1.05rem; margin-top: 10px; color: #25233A;'>Section 6: Grounded Empirical Strengths</h4>")
            strengths = []
            if pd.notnull(p_row.get('delta_strike_rate')) and p_row.get('delta_strike_rate', 0) > 0:
                strengths.append(f"Clutch Acceleration: Generates a positive strike rate delta of {p_row['delta_strike_rate']:+.1f} under PI >= 0.65.")
            if pd.notnull(p_row.get('pressure_cumulative_dva')) and p_row.get('pressure_cumulative_dva', 0) > 0:
                strengths.append(f"Positive Run Value: Contributed {p_row['pressure_cumulative_dva']:+.2f} net runs above expected par under pressure.")
            if pd.notnull(p_row.get('raw_psr')) and p_row.get('raw_psr', 0) >= 0.50:
                strengths.append(f"Winning Match Execution: Achieved a {p_row['raw_psr']*100:.1f}% positive match execution rate.")
            if not strengths:
                strengths.append("Baseline Competency: Displays consistent execution in non-leverage phases of play.")
            insight_box("Empirical Strengths", strengths, variant='lavender')

        # Section 7: Limitations & Sample Integrity Audit
        render_html("<h4 style='font-size: 1.05rem; margin-top: 14px; color: #25233A;'>Section 7: Limitations & Sample Integrity Audit</h4>")
        limits = []
        if not p_row['is_qualified']:
            limits.append(f"Disqualification Audit: {p_row.get('unqualified_reasons', 'Did not meet minimum sample requirements')}.")
            limits.append("Reliability Rating Withheld: Official prior shrinkage is gated until 60 pressure balls and 6 qualifying matches are recorded.")
        else:
            if pd.notnull(p_row.get('pressure_dot_pct')) and p_row.get('pressure_dot_pct', 0) > 35.0:
                limits.append(f"Dot Ball Vulnerability: High dot ball frequency under pressure ({p_row['pressure_dot_pct']:.1f}%).")
            if pd.notnull(p_row.get('delta_strike_rate')) and p_row.get('delta_strike_rate', 0) < 0:
                limits.append(f"Strike Rate Deceleration: Strike rate slows by {p_row['delta_strike_rate']:.1f} in high pressure compared to career baseline.")
            limits.append("Cohort Prior Shrinkage: PSR is stabilized against the IPL batter cohort prior (mu = 0.4303, K = 50 balls).")
        insight_box("Tactical Audit & Limitations", limits, variant='pink')


# -----------------------------------------------------------------------------
# PAGE 5: BOWLER ANALYSIS
# -----------------------------------------------------------------------------
elif st.session_state.page == "Bowler Analysis":
    col_nav_bw1, col_nav_bw2 = st.columns([1, 7], vertical_alignment="center")
    with col_nav_bw1:
        if st.button("Back", key="back_btn_bowl", use_container_width=True):
            navigate_back(fallback_page="Overview")
    with col_nav_bw2:
        render_html("<h1 style='margin:0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 40px;'>Deep-Dive Bowler Analysis</h1>")
        
    bowlers_list = df_players[df_players['role'] == 'bowler'].sort_values('player_name').copy()
    cur_bowl_id = st.session_state.selected_bowler_id
    if cur_bowl_id not in bowlers_list['player_id'].values:
        cur_bowl_id = 2933  # Jasprit Bumrah fallback
        st.session_state.selected_bowler_id = 2933
        
    selected_bowler_idx = int(bowlers_list['player_id'].tolist().index(cur_bowl_id))
    selected_bw_id = st.selectbox(
        "Select Bowler to Inspect:",
        options=bowlers_list['player_id'].tolist(),
        index=selected_bowler_idx,
        format_func=lambda x: f"{bowlers_list[bowlers_list['player_id']==x]['player_name'].values[0]} ({bowlers_list[bowlers_list['player_id']==x]['ipl_franchises'].values[0]})"
    )
    if selected_bw_id != cur_bowl_id:
        st.session_state.selected_bowler_id = selected_bw_id
        st.rerun()
        
    p_row = bowlers_list[bowlers_list['player_id'] == selected_bw_id].iloc[0]
    
    # Preload phase and history data
    df_phase_bw = load_player_phase_breakdown(player_id=selected_bw_id, role='bowler')
    df_hist_bw = load_player_match_history(player_id=selected_bw_id, role='bowler')
    df_hist_press_bw = df_hist_bw[df_hist_bw['is_pressure_involved']].copy() if not df_hist_bw.empty else pd.DataFrame()
    
    # Statistical Summary Dictionary
    press_overs = f"{int(p_row.get('pressure_exposure_balls', 0)) // 6}.{int(p_row.get('pressure_exposure_balls', 0)) % 6}"
    base_overs = f"{int(p_row.get('baseline_eligible_balls', 0)) // 6}.{int(p_row.get('baseline_eligible_balls', 0)) % 6}"
    
    stats_data_bowler = {
        "Metric": [
            "Legal Balls Bowled", "Overs", "Runs Conceded", "Wickets", 
            "Economy Rate", "Bowling Strike Rate", "Boundary % Conceded", 
            "Dot Ball %", "Cumulative DVA", "DVA per Ball"
        ],
        "Baseline (Low / Non-Pressure)": [
            f"{int(p_row.get('baseline_eligible_balls', 0)):,}",
            base_overs,
            f"{int(p_row.get('baseline_runs', 0)):,}",
            "-",
            f"{p_row['baseline_economy_rate']:.2f}" if pd.notnull(p_row.get('baseline_economy_rate')) else "N/A",
            "-", "-", "-", "-",
            f"{p_row['baseline_dva_per_ball']:+.4f}" if pd.notnull(p_row.get('baseline_dva_per_ball')) else "N/A"
        ],
        "High Pressure (PI >= 0.65)": [
            f"{int(p_row.get('pressure_exposure_balls', 0)):,}",
            press_overs,
            f"{int(p_row.get('pressure_runs', 0)):,}",
            f"{int(p_row.get('pressure_dismissals', 0))}",
            f"{p_row['pressure_economy_rate']:.2f}" if pd.notnull(p_row.get('pressure_economy_rate')) else "N/A",
            f"{p_row['pressure_strike_rate']:.1f}" if pd.notnull(p_row.get('pressure_strike_rate')) else "N/A",
            f"{p_row['pressure_boundary_pct']:.2f}%" if pd.notnull(p_row.get('pressure_boundary_pct')) else "N/A",
            f"{p_row['pressure_dot_pct']:.2f}%" if pd.notnull(p_row.get('pressure_dot_pct')) else "N/A",
            f"{p_row['pressure_cumulative_dva']:+.4f}" if pd.notnull(p_row.get('pressure_cumulative_dva')) else "N/A",
            f"{p_row['pressure_dva_per_ball']:+.4f}" if pd.notnull(p_row.get('pressure_dva_per_ball')) else "N/A"
        ],
        "Clutch Improvement": [
            "-", "-", "-", "-",
            f"{p_row['clutch_econ_suppression']:+.2f}" if pd.notnull(p_row.get('clutch_econ_suppression')) else "N/A",
            "-", "-", "-", "-",
            f"{p_row['delta_dva_per_ball']:+.4f}" if pd.notnull(p_row.get('delta_dva_per_ball')) else "N/A"
        ]
    }
    
    # Top Level Header Card & Status Badge
    player_header_card(p_row)
    status_badge(
        p_row['is_qualified'],
        rank=p_row['rank'],
        score=p_row['final_composite_score'],
        reasons=p_row['unqualified_reasons'],
        role='bowler'
    )
    
    # Five Unified Tabs
    bowler_tab_list = [
        "Player Overview",
        "Performance Analysis",
        "Player Comparison Studio",
        "Match Pressure Explorer",
        "Player Scouting Report"
    ]
    bowl_def_tab = st.session_state.get("bowler_active_tab", "Player Overview")
    if bowl_def_tab not in bowler_tab_list:
        bowl_def_tab = "Player Overview"
    tab_overview_bw, tab_perf_bw, tab_comp_bw, tab_match_bw, tab_scout_bw = st.tabs(
        bowler_tab_list,
        default=bowl_def_tab,
        key="bowler_analysis_tabs_container"
    )
    
    # ---------------- TAB 1: PLAYER OVERVIEW ----------------
    with tab_overview_bw:
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            econ_val = f"{p_row['pressure_economy_rate']:.2f}" if pd.notnull(p_row.get('pressure_economy_rate')) else "N/A"
            metric_card("Pressure Economy", econ_val, delta=p_row.get('clutch_econ_suppression'), delta_positive=(p_row.get('clutch_econ_suppression') or 0) > 0, variant='blue', icon='shield')
        with col_k2:
            dva_val = f"{p_row['pressure_cumulative_dva']:+.1f}" if pd.notnull(p_row.get('pressure_cumulative_dva')) else "0.0"
            dva_sub = f"{p_row['pressure_dva_per_ball']:+.2f} per ball" if pd.notnull(p_row.get('pressure_dva_per_ball')) else ""
            metric_card("Pressure DVA Suppressed", dva_val, dva_sub, variant='purple', icon='chart')
        with col_k3:
            psr_val = f"{p_row['raw_psr']*100:.1f}%" if pd.notnull(p_row.get('raw_psr')) else "0.0%"
            exp_sub = f"Exposure PSR: {p_row['exposure_weighted_psr']*100:.1f}%" if pd.notnull(p_row.get('exposure_weighted_psr')) else "Not Qualified"
            metric_card("Pressure Success Rate", psr_val, exp_sub, variant='lavender', icon='award')
        with col_k4:
            dot_val = f"{p_row['pressure_dot_pct']:.1f}%" if pd.notnull(p_row.get('pressure_dot_pct')) else "N/A"
            bdry_sub = f"Boundary Rate: {p_row['pressure_boundary_pct']:.1f}%" if pd.notnull(p_row.get('pressure_boundary_pct')) else ""
            metric_card("Pressure Dot Ball %", dot_val, bdry_sub, variant='neutral', icon='target')

        render_html("<div style='margin-top: 14px;'></div>")
        col_ov_bw1, col_ov_bw2 = st.columns([1, 2])
        with col_ov_bw1:
            fig_gauge_bw = plot_reliability_gauge(p_row.get('final_composite_score'), p_row.get('rank'), p_row.get('is_qualified'), 'bowler')
            st.plotly_chart(fig_gauge_bw, use_container_width=True)
            st.caption("Shrunk Bayesian composite reliability score with empirical penalty adjustment.")
        with col_ov_bw2:
            fig_career_bw = plot_career_vs_pressure_bowler(p_row)
            st.plotly_chart(fig_career_bw, use_container_width=True)
            st.caption("Career Baseline vs High-Pressure (PI >= 0.65) economy rate and delivery sample volume.")
            
        if p_row.get('is_qualified'):
            insight_box(
                "Phase 3A Analytical Assessment",
                [
                    f"Overall Reliability Index: {p_row['final_composite_score']:.4f} (Rank {int(p_row['rank'])}) across {int(p_row['pressure_exposure_balls'])} high-pressure deliveries.",
                    f"Clutch Suppression: Economy rate improves by {p_row['clutch_econ_suppression']:+.2f} RPO under intense pressure situations.",
                    f"Defense Execution Rate: Defended target or suppressed run rate in {int(p_row['successful_matches'])} of {int(p_row['psr_qualifying_matches'])} qualifying matches (PSR: {p_row['raw_psr']*100:.1f}%)."
                ],
                variant='lavender'
            )
        else:
            insight_box(
                "Sample Gate Status & Observational Audit",
                [
                    f"Qualification Status: Player is currently unranked ({p_row.get('unqualified_reasons', 'Insufficient sample size')}).",
                    f"Current Exposure: {int(p_row.get('pressure_exposure_balls', 0))} pressure balls bowled across {int(p_row.get('psr_qualifying_matches', p_row.get('pressure_matches', 0)))} qualifying matches (Minimum required: 60 balls & 6 matches).",
                    "Data Integrity Guard: Statistics are recorded purely on empirical deliveries without prior shrinkage distortion."
                ],
                variant='blue'
            )

    # ---------------- TAB 2: PERFORMANCE ANALYSIS ----------------
    with tab_perf_bw:
        col_bw_e1, col_bw_e2 = st.columns(2)
        with col_bw_e1:
            fig_econ = plot_bowler_economy_chart(p_row)
            st.plotly_chart(fig_econ, use_container_width=True)
            st.caption("Economy Rate: Baseline vs High-Pressure run restriction (Runs per Over). Lower is better.")
        with col_bw_e2:
            fig_bw_sr = plot_bowler_strike_rate_chart(p_row)
            st.plotly_chart(fig_bw_sr, use_container_width=True)
            st.caption("Bowling Strike Rate: Balls bowled per dismissal. Lower is better.")

        render_html("<div style='margin-top: 14px;'></div>")
        fig_dva_bw = plot_dva_breakdown(p_row)
        st.plotly_chart(fig_dva_bw, use_container_width=True)
        st.caption("Delivery Value Added (DVA): Net runs suppressed relative to baseline expectation per ball and cumulative match impact.")

        render_html("<h4 style='font-size: 1.05rem; margin-top: 18px; color: #25233A;'>Statistical Summary: Baseline vs High Pressure</h4>")
        render_stats_summary_table(stats_data_bowler, role='bowler')

        render_html("<h4 style='font-size: 1.05rem; margin-top: 18px; color: #25233A;'>Match Phase Performance Breakdown</h4>")
        if not df_phase_bw.empty:
            col_ph_bw1, col_ph_bw2 = st.columns([3, 2])
            with col_ph_bw1:
                fig_ph_bw = plot_phase_comparison(df_phase_bw, 'bowler')
                st.plotly_chart(fig_ph_bw, use_container_width=True)
                st.caption("Economy rate and legal ball volume breakdown across Powerplay (1-6), Middle (7-15), and Death (16-20) overs.")
            with col_ph_bw2:
                tbl_phase_bw = df_phase_bw[['phase', 'overall_balls', 'overall_metric', 'pressure_balls', 'pressure_metric', 'pressure_dva']].rename(columns={
                    'phase': 'Phase',
                    'overall_balls': 'Total Legal',
                    'overall_metric': 'Base Econ',
                    'pressure_balls': 'Press Legal',
                    'pressure_metric': 'Press Econ',
                    'pressure_dva': 'Press DVA'
                })
                st.dataframe(tbl_phase_bw.style.format({
                    'Total Legal': '{:.0f}',
                    'Base Econ': '{:.2f}',
                    'Press Legal': '{:.0f}',
                    'Press Econ': '{:.2f}',
                    'Press DVA': '{:+.2f}'
                }), use_container_width=True, hide_index=True)
        else:
            st.info("No phase breakdown recorded for this bowler.")

        render_html("<h4 style='font-size: 1.05rem; margin-top: 18px; color: #25233A;'>Match-by-Match Pressure Performance Timeline</h4>")
        if not df_hist_bw.empty:
            if not df_hist_press_bw.empty:
                fig_time_bw = plot_match_timeline(df_hist_press_bw, 'bowler')
                st.plotly_chart(fig_time_bw, use_container_width=True)
                st.caption("Chronological match progression showing economy rate and binary PSR qualification outcome.")
                
                cols_hist_bw = [
                    'match_date', 'season', 'away_team', 'pressure_eligible_balls', 
                    'pressure_runs', 'pressure_wickets_or_dismissals', 
                    'pressure_metric', 'pressure_dva', 'is_successful_pressure_match'
                ]
                tbl_hist_bw = df_hist_press_bw[cols_hist_bw].rename(columns={
                    'match_date': 'Date',
                    'season': 'Season',
                    'away_team': 'Opponent',
                    'pressure_eligible_balls': 'Legal Balls',
                    'pressure_runs': 'Runs Conceded',
                    'pressure_wickets_or_dismissals': 'Wickets',
                    'pressure_metric': 'Economy Rate',
                    'pressure_dva': 'Net DVA',
                    'is_successful_pressure_match': 'Success'
                }).sort_values('Date', ascending=False)
                
                st.dataframe(
                    tbl_hist_bw.style.format({
                        'Legal Balls': '{:.0f}',
                        'Runs Conceded': '{:.0f}',
                        'Wickets': '{:.0f}',
                        'Economy Rate': '{:.2f}',
                        'Net DVA': '{:+.2f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Player has bowled in matches, but bowled 0 high-pressure deliveries.")
        else:
            st.info("No match history available.")

    # ---------------- TAB 3: PLAYER COMPARISON STUDIO ----------------
    with tab_comp_bw:
        render_html("<h2 style='margin:0 0 6px 0; font-size: 20px; font-weight: 600; color:#25233A;'>Side-by-Side Bowler Comparison Studio</h2>")
        st.markdown(
            "<div style='font-size:0.84rem; color:#77758A; margin-bottom:14px;'>"
            "Independent comparison workspace. Benchmarking 2 or 3 bowlers updates the view in place without redirecting or altering individual player profiles."
            "</div>",
            unsafe_allow_html=True
        )
        
        # Format map for robust display across bowler comparisons
        bowlers_format_map = {
            int(row['player_id']): f"{row['player_name']} ({str(row.get('ipl_franchises', '')).split(',')[0].strip()})"
            for _, row in bowlers_list.iterrows()
        }
        bowl_name_to_id = {v: k for k, v in bowlers_format_map.items()}
        def format_bowler(x):
            if isinstance(x, str):
                return x
            return bowlers_format_map.get(int(x), f"Player {x}")
        
        # State variables for bowler comparison
        bw_p1_id = st.session_state.get('comp_bowl_p1_id', 2933)
        if bw_p1_id not in bowlers_list['player_id'].values:
            bw_p1_id = int(bowlers_list['player_id'].iloc[0])
            st.session_state.comp_bowl_p1_id = bw_p1_id
            
        p1_idx_bw = int(bowlers_list['player_id'].tolist().index(bw_p1_id))
        
        comp_col1, comp_col2, comp_col3 = st.columns([3, 3, 2], vertical_alignment="bottom")
        with comp_col1:
            raw_bw_p1 = st.selectbox(
                "Player 1:",
                options=bowlers_list['player_id'].tolist(),
                index=p1_idx_bw,
                format_func=format_bowler,
                key="comp_bowl_p1_select",
                on_change=set_bowler_active_tab,
                args=("Player Comparison Studio",)
            )
            new_bw_p1 = bowl_name_to_id.get(raw_bw_p1, raw_bw_p1) if isinstance(raw_bw_p1, str) else int(raw_bw_p1)
            if new_bw_p1 != bw_p1_id:
                st.session_state.comp_bowl_p1_id = new_bw_p1
                st.session_state.comp_player_1_id = new_bw_p1
                st.session_state.bowler_active_tab = "Player Comparison Studio"
                bw_p1_id = new_bw_p1
                
        p1_row_bw = bowlers_list[bowlers_list['player_id'] == bw_p1_id].iloc[0]
        
        other_bowlers = bowlers_list[bowlers_list['player_id'] != bw_p1_id].copy()
        bw_p2_id = st.session_state.get('comp_bowl_p2_id', 4220)
        if bw_p2_id not in other_bowlers['player_id'].values:
            qual_peers_bw = other_bowlers[other_bowlers['is_qualified']]['player_id'].tolist()
            bw_p2_id = qual_peers_bw[0] if qual_peers_bw else int(other_bowlers['player_id'].iloc[0])
            st.session_state.comp_bowl_p2_id = bw_p2_id
            
        p2_idx_bw = int(other_bowlers['player_id'].tolist().index(bw_p2_id))
        with comp_col2:
            raw_bw_p2 = st.selectbox(
                "Compare with Player 2:",
                options=other_bowlers['player_id'].tolist(),
                index=p2_idx_bw,
                format_func=format_bowler,
                key="comp_bowl_p2_select",
                on_change=set_bowler_active_tab,
                args=("Player Comparison Studio",)
            )
            new_bw_p2 = bowl_name_to_id.get(raw_bw_p2, raw_bw_p2) if isinstance(raw_bw_p2, str) else int(raw_bw_p2)
            if new_bw_p2 != bw_p2_id:
                st.session_state.comp_bowl_p2_id = new_bw_p2
                st.session_state.comp_player_2_id = new_bw_p2
                st.session_state.bowler_active_tab = "Player Comparison Studio"
                bw_p2_id = new_bw_p2
                
        p2_row_bw = other_bowlers[other_bowlers['player_id'] == bw_p2_id].iloc[0]
        
        with comp_col3:
            add_p3_bw = st.checkbox(
                "Add 3rd Bowler",
                value=st.session_state.get("comp_bowl_enable_p3", False),
                key="comp_bowl_p3_toggle",
                on_change=set_bowler_active_tab,
                args=("Player Comparison Studio",)
            )
            st.session_state.comp_bowl_enable_p3 = add_p3_bw
            st.session_state.comp_enable_p3 = add_p3_bw
            st.session_state.bowler_active_tab = "Player Comparison Studio"
            p3_row_bw = None
            if add_p3_bw:
                p3_candidates_bw = other_bowlers[other_bowlers['player_id'] != bw_p2_id].copy()
                bw_p3_id = st.session_state.get('comp_bowl_p3_id', None)
                if bw_p3_id not in p3_candidates_bw['player_id'].values:
                    bw_p3_id = int(p3_candidates_bw['player_id'].iloc[0])
                    st.session_state.comp_bowl_p3_id = bw_p3_id
                p3_idx_bw = int(p3_candidates_bw['player_id'].tolist().index(bw_p3_id))
                raw_bw_p3 = st.selectbox(
                    "Player 3:",
                    options=p3_candidates_bw['player_id'].tolist(),
                    index=p3_idx_bw,
                    format_func=format_bowler,
                    key="comp_bowl_p3_select",
                    on_change=set_bowler_active_tab,
                    args=("Player Comparison Studio",)
                )
                new_bw_p3 = bowl_name_to_id.get(raw_bw_p3, raw_bw_p3) if isinstance(raw_bw_p3, str) else int(raw_bw_p3)
                if new_bw_p3 != bw_p3_id:
                    st.session_state.comp_bowl_p3_id = new_bw_p3
                    st.session_state.comp_player_3_id = new_bw_p3
                    st.session_state.bowler_active_tab = "Player Comparison Studio"
                    bw_p3_id = new_bw_p3
                p3_row_bw = p3_candidates_bw[p3_candidates_bw['player_id'] == bw_p3_id].iloc[0]

        players_comp_list_bw = [p1_row_bw, p2_row_bw]
        if p3_row_bw is not None:
            players_comp_list_bw.append(p3_row_bw)
            
        # Action buttons: Open Player Profile explicitly
        act_cols_bw = st.columns(len(players_comp_list_bw))
        for idx_p, p_item in enumerate(players_comp_list_bw):
            with act_cols_bw[idx_p]:
                if st.button(
                    f"Open Profile: {p_item['player_name']}",
                    key=f"btn_open_prof_bw_{p_item['player_id']}",
                    use_container_width=True
                ):
                    navigate_to("Bowler Analysis", player_id=p_item['player_id'], role='bowler', from_tab="Player Comparison Studio", origin_page="Bowler Analysis")

        # Comparison KPI Summary Cards
        render_comparison_summary(players_comp_list_bw, role='bowler')
        
        # 1) Rebuilt Benchmark Comparison across 3 dedicated vertical containers
        render_player_comparison_benchmarks(players_comp_list_bw, role='bowler')
        
        # 2) One compact comparison table showing exact values
        render_comparison_data_table(players_comp_list_bw, role='bowler')
        
        # 3) One phase-wise comparison chart where data is available
        phase_dict_bw = {}
        for p in players_comp_list_bw:
            df_ph_p = load_player_phase_breakdown(p['player_id'], 'bowler')
            phase_dict_bw[p['player_name']] = df_ph_p
        fig_cp_ph_bw = plot_player_comparison_phase(phase_dict_bw, role='bowler')
        st.plotly_chart(fig_cp_ph_bw, use_container_width=True)
        st.caption("Phase breakdown of pressure economy rate across Powerplay (1-6), Middle (7-15), and Death (16-20) overs. Parentheses show legal balls bowled (b); asterisk (*) marks sample < 10 balls.")

    # ---------------- TAB 4: MATCH PRESSURE EXPLORER ----------------
    with tab_match_bw:
        render_html("<h2 style='margin:0 0 12px 0; font-size: 20px; font-weight: 600; color:#25233A;'>Match Pressure Dynamics & Delivery Inspector</h2>")
        
        df_all_matches = load_ipl_matches()
        
        col_mf1, col_mf2 = st.columns([1, 2])
        with col_mf1:
            filter_mode_bw = st.radio(
                "Match Scope:",
                ["Matches with " + p_row['player_name'], "All IPL Matches (2022-2026)"],
                index=0,
                key="bw_match_scope",
                on_change=set_bowler_active_tab,
                args=("Match Pressure Explorer",)
            )
        with col_mf2:
            seasons_avail = ["All Seasons"] + sorted(df_all_matches['season'].astype(str).unique().tolist())
            sel_season_bw = st.selectbox(
                "Filter Season:",
                options=seasons_avail,
                index=0,
                key="bw_match_season",
                on_change=set_bowler_active_tab,
                args=("Match Pressure Explorer",)
            )
            
        if filter_mode_bw.startswith("Matches with"):
            if not df_hist_bw.empty and 'match_id' in df_hist_bw.columns:
                player_mids_bw = set(df_hist_bw['match_id'].unique().tolist())
            else:
                p_delivs_bw = load_player_match_deliveries(selected_bw_id, role='bowler')
                player_mids_bw = set(p_delivs_bw['match_id'].unique().tolist()) if not p_delivs_bw.empty else set()
                
            filtered_matches_bw = df_all_matches[df_all_matches['match_id'].isin(player_mids_bw)].copy()
            if filtered_matches_bw.empty:
                filtered_matches_bw = df_all_matches.copy()
        else:
            filtered_matches_bw = df_all_matches.copy()
            
        if sel_season_bw != "All Seasons":
            filtered_matches_bw = filtered_matches_bw[filtered_matches_bw['season'].astype(str) == sel_season_bw]
            
        if filtered_matches_bw.empty:
            st.warning("No matches found matching the selected filters.")
        else:
            filtered_matches_bw = filtered_matches_bw.sort_values('match_date', ascending=False)
            match_options_bw = filtered_matches_bw['match_id'].tolist()
            
            sel_match_id_bw = st.selectbox(
                "Select Match to Explore:",
                options=match_options_bw,
                format_func=lambda x: f"{filtered_matches_bw[filtered_matches_bw['match_id']==x]['match_date'].values[0]} - {filtered_matches_bw[filtered_matches_bw['match_id']==x]['home_team'].values[0]} vs {filtered_matches_bw[filtered_matches_bw['match_id']==x]['away_team'].values[0]} (IPL {filtered_matches_bw[filtered_matches_bw['match_id']==x]['season'].values[0]}, Match {x})",
                key="bw_sel_match",
                on_change=set_bowler_active_tab,
                args=("Match Pressure Explorer",)
            )
            
            selected_match_row_bw = filtered_matches_bw[filtered_matches_bw['match_id'] == sel_match_id_bw].iloc[0]
            df_match_delivs_bw = load_ipl_deliveries(match_id=sel_match_id_bw)
            
            # Match Overview & Player Impact Card
            render_match_overview_card(selected_match_row_bw, df_match_delivs_bw, player_id=selected_bw_id, role='bowler')
            
            # Over-by-Over Timeline
            fig_match_over_bw = plot_match_over_pressure_timeline(df_match_delivs_bw, selected_match_row_bw, player_id=selected_bw_id, role='bowler')
            st.plotly_chart(fig_match_over_bw, use_container_width=True)
            st.caption("Over-by-over leverage timeline showing run progression, wickets, and delivery pressure index.")
            
            # Ball-by-Ball Inspection
            render_html("<h4 style='font-size:1.05rem; margin-top:16px; color:#25233A;'>Delivery-Level Leverage & Value Added Inspection</h4>")
            deliv_filter_bw = st.radio(
                "Filter Deliveries:",
                ["High Pressure Deliveries Only (PI >= 0.65)", f"{p_row['player_name']} Deliveries Only", "All Deliveries in Match"],
                horizontal=True,
                key="bw_deliv_filter",
                on_change=set_bowler_active_tab,
                args=("Match Pressure Explorer",)
            )
            
            df_table_delivs_bw = df_match_delivs_bw.copy()
            if deliv_filter_bw.startswith("High Pressure"):
                df_table_delivs_bw = df_table_delivs_bw[df_table_delivs_bw['pressure_index'] >= 0.65]
            elif deliv_filter_bw.startswith(p_row['player_name']):
                df_table_delivs_bw = df_table_delivs_bw[df_table_delivs_bw['bowler_id'] == selected_bw_id]
                
            if df_table_delivs_bw.empty:
                st.info("No deliveries match the selected delivery filter.")
            else:
                cols_to_show_bw = [
                    'innings', 'overid', 'over_ball_num', 'striker_name', 'bowler_name', 
                    'runs', 'bowler_runs_conceded', 'is_wicket', 'pressure_index', 'pressure_tier', 'dva_bowler'
                ]
                df_disp_delivs_bw = df_table_delivs_bw[cols_to_show_bw].rename(columns={
                    'innings': 'Inn',
                    'overid': 'Over',
                    'over_ball_num': 'Ball',
                    'striker_name': 'Striker',
                    'bowler_name': 'Bowler',
                    'runs': 'Runs',
                    'bowler_runs_conceded': 'Conceded',
                    'is_wicket': 'Wkt',
                    'pressure_index': 'PI',
                    'pressure_tier': 'Tier',
                    'dva_bowler': 'Bowler DVA'
                }).sort_values(['Inn', 'Over', 'Ball'])
                
                st.dataframe(
                    df_disp_delivs_bw.style.format({
                        'Inn': '{:.0f}',
                        'Over': '{:.0f}',
                        'Ball': '{:.0f}',
                        'Runs': '{:.0f}',
                        'Conceded': '{:.0f}',
                        'PI': '{:.3f}',
                        'Bowler DVA': '{:+.3f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )

    # ---------------- TAB 5: PLAYER SCOUTING REPORT ----------------
    with tab_scout_bw:
        col_sc_h1, col_sc_h2 = st.columns([3, 1], vertical_alignment="center")
        with col_sc_h1:
            render_html(f"""
            <div>
                <span style="background: #F0ECF8; color: #7964B5; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; padding: 2px 8px; border-radius: 6px;">
                    Confidential Scouting Intelligence
                </span>
                <h2 style="margin: 4px 0 0 0; font-size: 20px; font-weight: 600; color: #25233A;">
                    {p_row['player_name']} - Executive Scouting Dossier
                </h2>
                <div style="font-size: 0.82rem; color: #77758A;">
                    Complete 14-Section Performance Evaluation | IPL 2022-2026 Coverage
                </div>
            </div>
            """)
        with col_sc_h2:
            pdf_bytes_bw = generate_scouting_pdf(
                p_row,
                stats_data=stats_data_bowler,
                phase_df=df_phase_bw,
                match_history_df=df_hist_bw,
                role='bowler'
            )
            safe_player_file = p_row['player_name'].replace(' ', '_')
            st.download_button(
                label="Download Executive PDF Dossier",
                data=pdf_bytes_bw,
                file_name=f"SupeRR_Scouting_Report_{safe_player_file}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="bw_scout_pdf_btn"
            )
            
        render_html("<div style='margin-top: 14px;'></div>")
        
        # Section 1: Executive Summary & Reliability Rating
        render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #ECEAF3; border-top: 3px solid #7964B5; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #7964B5;">Section 1: Executive Reliability Summary</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #25233A; margin: 4px 0 8px 0;">
                {'Rank ' + str(int(p_row['rank'])) + ' Reliable IPL Bowler' if p_row['is_qualified'] else 'Sample Gate Unranked Bowler'}
            </div>
            <div style="font-size: 0.86rem; color: #37324B; line-height: 1.5;">
                {p_row['player_name']} has delivered <strong>{int(p_row.get('career_eligible_balls', 0)):,}</strong> career IPL legal deliveries across <strong>{int(p_row.get('total_matches', 0))}</strong> matches for {p_row.get('ipl_franchises', 'IPL')}.
                Under Phase 3A high-pressure conditions (PI &ge; 0.65), the bowler delivered <strong>{int(p_row.get('pressure_exposure_balls', 0))}</strong> deliveries across <strong>{int(p_row.get('psr_qualifying_matches', p_row.get('pressure_matches', 0)))}</strong> qualifying match situations.
                Official Reliability Index: <strong>{f"{p_row['final_composite_score']:.4f}" if p_row['is_qualified'] else "Withheld (Sample Gate)"}</strong>.
            </div>
        </div>
        """)
        
        # Section 2 & 3: Four Core Benchmarks Grid
        col_sc_b1, col_sc_b2, col_sc_b3, col_sc_b4 = st.columns(4)
        with col_sc_b1:
            metric_card("Pressure Economy", f"{p_row['pressure_economy_rate']:.2f}" if pd.notnull(p_row.get('pressure_economy_rate')) else "N/A", f"Career: {p_row.get('career_economy_rate', 0.0):.2f}", delta=p_row.get('clutch_econ_suppression'), delta_positive=(p_row.get('clutch_econ_suppression') or 0) > 0, variant='blue')
        with col_sc_b2:
            metric_card("Pressure Bowling SR", f"{p_row['pressure_strike_rate']:.1f}" if (pd.notnull(p_row.get('pressure_strike_rate')) and p_row.get('pressure_strike_rate', 0) > 0) else "N/A", f"{int(p_row.get('pressure_dismissals', 0))} Wickets", variant='lavender')
        with col_sc_b3:
            metric_card("Net Pressure DVA", f"{p_row.get('pressure_cumulative_dva', 0.0):+.2f}", f"{p_row.get('pressure_dva_per_ball', 0.0):+.3f}/ball", delta_positive=(p_row.get('pressure_cumulative_dva') or 0) >= 0, variant='purple')
        with col_sc_b4:
            metric_card("PSR Execution Rate", f"{p_row.get('raw_psr', 0.0)*100:.1f}%", f"{int(p_row.get('successful_matches', 0))} of {int(p_row.get('psr_qualifying_matches', 0))} wins", variant='rose')
            
        render_html("<div style='margin-top: 14px;'></div>")
        
        # Section 4: Performance Dimension Breakdown
        render_html("<h4 style='font-size: 1.05rem; margin-top: 10px; color: #25233A;'>Section 4: Baseline vs Pressure Empirical Breakdown</h4>")
        render_stats_summary_table(stats_data_bowler, role='bowler')
        
        # Section 5 & 6: Phase & Tactical Strengths
        col_sc_ph1, col_sc_ph2 = st.columns(2)
        with col_sc_ph1:
            render_html("<h4 style='font-size: 1.05rem; margin-top: 10px; color: #25233A;'>Section 5: Phase Leverage Distribution</h4>")
            if not df_phase_bw.empty:
                st.dataframe(df_phase_bw[['phase', 'overall_balls', 'overall_metric', 'pressure_balls', 'pressure_metric', 'pressure_dva']].rename(columns={
                    'phase': 'Phase', 'overall_balls': 'Total Legal', 'overall_metric': 'Career Econ', 'pressure_balls': 'Press Legal', 'pressure_metric': 'Press Econ', 'pressure_dva': 'Press DVA'
                }), use_container_width=True, hide_index=True)
            else:
                st.info("No phase breakdown recorded.")
        with col_sc_ph2:
            render_html("<h4 style='font-size: 1.05rem; margin-top: 10px; color: #25233A;'>Section 6: Grounded Empirical Strengths</h4>")
            strengths_bw = []
            if pd.notnull(p_row.get('clutch_econ_suppression')) and p_row.get('clutch_econ_suppression', 0) > 0:
                strengths_bw.append(f"Clutch Run Suppression: Economy improves by {p_row['clutch_econ_suppression']:+.2f} RPO under intense pressure.")
            if pd.notnull(p_row.get('pressure_cumulative_dva')) and p_row.get('pressure_cumulative_dva', 0) > 0:
                strengths_bw.append(f"Defended Run Value: Prevented {p_row['pressure_cumulative_dva']:+.2f} net runs relative to expected match par.")
            if pd.notnull(p_row.get('raw_psr')) and p_row.get('raw_psr', 0) >= 0.50:
                strengths_bw.append(f"Match Winning Control: Successfully contained opponent scoring in {p_row['raw_psr']*100:.1f}% of qualifying outings.")
            if not strengths_bw:
                strengths_bw.append("Baseline Competency: Delivers reliable control in early and mid-innings baseline overs.")
            insight_box("Empirical Strengths", strengths_bw, variant='lavender')

        # Section 7: Limitations & Sample Integrity Audit
        render_html("<h4 style='font-size: 1.05rem; margin-top: 14px; color: #25233A;'>Section 7: Limitations & Sample Integrity Audit</h4>")
        limits_bw = []
        if not p_row['is_qualified']:
            limits_bw.append(f"Disqualification Audit: {p_row.get('unqualified_reasons', 'Did not meet minimum sample requirements')}.")
            limits_bw.append("Reliability Rating Withheld: Official prior shrinkage is gated until 60 pressure balls and 6 qualifying matches are recorded.")
        else:
            if pd.notnull(p_row.get('pressure_boundary_pct')) and p_row.get('pressure_boundary_pct', 0) > 20.0:
                limits_bw.append(f"Boundary Concession Risk: Boundary concession rate increases under pressure ({p_row['pressure_boundary_pct']:.1f}%).")
            if pd.notnull(p_row.get('clutch_econ_suppression')) and p_row.get('clutch_econ_suppression', 0) < 0:
                limits_bw.append(f"Economy Expansion: Economy rate inflates by {abs(p_row['clutch_econ_suppression']):.2f} RPO in high pressure.")
            limits_bw.append("Cohort Prior Shrinkage: PSR is stabilized against the IPL bowler cohort prior (mu = 0.6210, K = 48 balls).")
        insight_box("Tactical Audit & Limitations", limits_bw, variant='blue')


# -----------------------------------------------------------------------------
# PAGE 6: PRESSURE ANALYSIS
# -----------------------------------------------------------------------------
elif st.session_state.page == "Pressure Analysis":
    col_nav_p1, col_nav_p2 = st.columns([1, 7], vertical_alignment="center")
    with col_nav_p1:
        if st.button("Back", key="back_btn_pressure", use_container_width=True):
            navigate_back(fallback_page="Overview")
    with col_nav_p2:
        render_html("""
            <div style="display: inline-block; background: #F0ECF8; color: #7964B5; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; padding: 3px 10px; border-radius: 14px; margin-bottom: 2px;">
                Macro Dynamics & Environmental Factors
            </div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 1.2;">
                SupeRR Selector Pressure Dynamics
            </h1>
        """)
    render_html("""
        <p style="color: #77758A; font-size: 0.94rem; margin-top: 6px; margin-bottom: 16px;">
            Examine how pressure concentrates across IPL match phases, run chases, tournament editions, and team dynamics under the approved methodology.
        </p>
    """)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        render_html("<h3 style='margin: 0 0 10px 0; font-size: 20px; font-weight: 600; color: #25233A;'>Pressure Distribution by Innings</h3>")
        inn_data = overview_data['innings_summary']
        inn_df = pd.DataFrame([
            {'Innings': '1st Innings (Setting Target)', 'Deliveries': inn_data['1']['total_deliveries'], 'High Pressure': inn_data['1']['high_pressure_deliveries'], 'High Pressure %': inn_data['1']['pct_high_pressure'], 'Mean PI': inn_data['1']['mean_pi']},
            {'Innings': '2nd Innings (Chasing Target)', 'Deliveries': inn_data['2']['total_deliveries'], 'High Pressure': inn_data['2']['high_pressure_deliveries'], 'High Pressure %': inn_data['2']['pct_high_pressure'], 'Mean PI': inn_data['2']['mean_pi']}
        ])
        st.dataframe(inn_df.style.format({
            'Deliveries': '{:,}',
            'High Pressure': '{:,}',
            'High Pressure %': '{:.2f}%',
            'Mean PI': '{:.4f}'
        }), use_container_width=True, hide_index=True)
        
        fig_inn_p = plot_innings_comparison(overview_data['innings_summary'])
        st.plotly_chart(fig_inn_p, use_container_width=True)
        
        render_html("""
            <div style="font-size: 0.84rem; color: #77758A; line-height: 1.5; margin-top: 8px;">
                <strong>Strategic Takeaway:</strong> High-pressure situations are strongly asymmetric, concentrating in the <strong>2nd innings run chase (14.1% vs 5.9%)</strong>, where required run rate escalating against finite balls creates acute climax leverage.
            </div>
        """)

    with col_p2:
        render_html("<h3 style='margin: 0 0 10px 0; font-size: 20px; font-weight: 600; color: #25233A;'>Pressure Distribution by Match Phase</h3>")
        ph_data = overview_data['phase_summary']
        ph_df = pd.DataFrame([
            {'Phase': 'Powerplay (Overs 1–6)', 'Deliveries': ph_data['Powerplay']['total_deliveries'], 'High Pressure': ph_data['Powerplay']['high_pressure_deliveries'], 'High Pressure %': ph_data['Powerplay']['pct_high_pressure'], 'Mean PI': ph_data['Powerplay']['mean_pi']},
            {'Phase': 'Middle (Overs 7–15)', 'Deliveries': ph_data['Middle']['total_deliveries'], 'High Pressure': ph_data['Middle']['high_pressure_deliveries'], 'High Pressure %': ph_data['Middle']['pct_high_pressure'], 'Mean PI': ph_data['Middle']['mean_pi']},
            {'Phase': 'Death (Overs 16–20)', 'Deliveries': ph_data['Death']['total_deliveries'], 'High Pressure': ph_data['Death']['high_pressure_deliveries'], 'High Pressure %': ph_data['Death']['pct_high_pressure'], 'Mean PI': ph_data['Death']['mean_pi']}
        ])
        st.dataframe(ph_df.style.format({
            'Deliveries': '{:,}',
            'High Pressure': '{:,}',
            'High Pressure %': '{:.2f}%',
            'Mean PI': '{:.4f}'
        }), use_container_width=True, hide_index=True)
        
        fig_ph_p = plot_match_phase_distribution(overview_data['phase_summary'])
        st.plotly_chart(fig_ph_p, use_container_width=True)
        
        render_html("""
            <div style="font-size: 0.84rem; color: #77758A; line-height: 1.5; margin-top: 8px;">
                <strong>Strategic Takeaway:</strong> The <strong>Death phase (overs 16–20)</strong> accounts for over 72% of all high-pressure deliveries across the tournament, reflecting terminal ball scarcity.
            </div>
        """)

    render_html("<div style='margin-top: 20px;'></div>")
    
    col_tm1, col_tm2 = st.columns([3, 2])
    with col_tm1:
        fig_team = plot_team_pressure(overview_data['team_summary'])
        st.plotly_chart(fig_team, use_container_width=True)
    with col_tm2:
        render_html("<h3 style='margin: 0 0 10px 0; font-size: 20px; font-weight: 600; color: #25233A;'>Franchise Pressure Exposure Table</h3>")
        team_list = []
        for t, d in overview_data['team_summary'].items():
            team_list.append({
                'Franchise': t,
                'Total Deliveries': d['total_deliveries'],
                'High Pressure Balls': d['high_pressure_deliveries'],
                'Pressure %': d['pct_high_pressure']
            })
        df_team_tbl = pd.DataFrame(team_list).sort_values('High Pressure Balls', ascending=False)
        st.dataframe(df_team_tbl.style.format({
            'Total Deliveries': '{:,}',
            'High Pressure Balls': '{:,}',
            'Pressure %': '{:.2f}%'
        }), use_container_width=True, hide_index=True)

    render_html("<div style='margin-top: 24px;'></div>")
    col_tns1, col_tns2 = st.columns([3, 2])
    with col_tns1:
        fig_tense = plot_tense_match_dynamics(overview_data['top_tense_situations'])
        st.plotly_chart(fig_tense, use_container_width=True)
    with col_tns2:
        render_html("<h3 style='margin: 0 0 10px 0; font-size: 20px; font-weight: 600; color: #25233A;'>Top 10 High-Pressure Match Finishes</h3>")
        tense_df = pd.DataFrame(overview_data['top_tense_situations'])
        tense_table = tense_df[['season', 'match_date', 'home_team', 'away_team', 'result', 'death_high_press_balls', 'death_mean_pi']].rename(columns={
            'season': 'Season',
            'match_date': 'Date',
            'home_team': 'Team 1',
            'away_team': 'Team 2',
            'result': 'Match Result',
            'death_high_press_balls': 'Death HP Balls',
            'death_mean_pi': 'Death Mean PI'
        })
        st.dataframe(tense_table.style.format({
            'Death HP Balls': '{:.0f}',
            'Death Mean PI': '{:.4f}'
        }), use_container_width=True, hide_index=True)
        
    render_html("""
        <div style="font-size: 0.84rem; color: #77758A; line-height: 1.5; margin-top: 8px;">
            <strong>Strategic Takeaway:</strong> Matches with the highest mean pressure in death overs consistently feature razor-thin run chases decided in the final 6 balls (often requiring > 12 RPO with <= 3 wickets in hand), creating extreme leverage where single deliveries swing expected win probabilities by > 35%.
        </div>
    """)


# -----------------------------------------------------------------------------
# PAGE 7: METHODOLOGY
# -----------------------------------------------------------------------------
elif st.session_state.page == "Methodology":
    col_nav_m1, col_nav_m2 = st.columns([1, 7], vertical_alignment="center")
    with col_nav_m1:
        if st.button("Back", key="back_btn_methodology", use_container_width=True):
            navigate_back(fallback_page="Overview")
    with col_nav_m2:
        render_html("""
            <div style="display: inline-block; background: #F0ECF8; color: #7964B5; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; padding: 3px 10px; border-radius: 14px; margin-bottom: 2px;">
                Mathematical Rigor & Transparency
            </div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 700; color: #25233A; letter-spacing: -0.02em; line-height: 1.2;">
                SupeRR Selector Methodology Specification
            </h1>
        """)
    render_html("""
        <p style="color: #77758A; font-size: 0.94rem; margin-top: 6px; margin-bottom: 16px;">
            Complete technical specification for the approved Phase 3A Version 2.2 SupeRR Selector and reliability scoring engine.
        </p>
    """)
    
    with st.expander("1. Delivery-Level Pressure Index (PI)", expanded=True):
        st.markdown("""
            Every legal delivery receives a continuous Pressure Index $PI \\in [0.0, 1.0]$. Deliveries with $PI \\ge 0.65$ are classified as **High Pressure**.
            
            **Approved Tier Boundaries (Phase 3A Version 2.2):**
            - **Low Pressure**: $PI < 0.40$
            - **Medium Pressure**: $0.40 \\le PI < 0.65$
            - **High Pressure**: $PI \\ge 0.65$
            
            **2nd Innings Formulation (Run Chases):**
            $$PI_{\\text{2nd}} = f(RRR) \\times WicketsFactor \\times Leverage \\times ContestedDampener \\times Stakes$$
            - **Sigmoid RRR Curve**: Centers around format par ($RRR_0 = 9.0$), smoothly scaling up to 1.0 for extreme chase rates.
            - **Wickets in Hand**: Scales as $(1.0 - 0.08 \\times WicketsDown)$ to reflect batting depth and bowler opportunity.
            - **Climax Leverage**: Escalates inversely with balls remaining, peaking in overs 16–20.
            
            **1st Innings Formulation (Target Setting):**
            $$PI_{\\text{1st}} = (0.50 \\times CollapseFactor + 0.30 \\times PhaseStakes + 0.20 \\times PaceDeficit) \\times Stakes$$
            Accounts for early top-order collapse, death-overs acceleration, and pacing behind par run rates.
        """)
        
    with st.expander("2. Delivery Value Added (DVA)", expanded=False):
        st.markdown("""
            Delivery Value Added measures the net run contribution of a batter or bowler relative to the format par baseline:
            
            - **Batter DVA**:
              $$\\text{DVA}_{\\text{batter}} = \\text{Runs} - \\text{ParSR}(\\text{Phase}, \\text{Innings}) - (2.50 \\times I_{\\text{wicket}})$$
            - **Bowler DVA**:
              $$\\text{DVA}_{\\text{bowler}} = \\text{ParEcon}(\\text{Phase}, \\text{Innings}) - \\text{RunsConceded} + (2.50 \\times I_{\\text{wicket}})$$
              *Illegal deliveries (wides, no-balls) receive an additional penalty equal to the penalty run.*
        """)
        
    with st.expander("3. Pressure Success Rate (PSR) & Exposure Weighting", expanded=False):
        st.markdown("""
            A player's match pressure contribution is aggregated as:
            $$\\text{NetMatchDVA} = \\sum_{d \\in \\text{PressureDeliveries}} \\text{DVA}_d$$
            A match is deemed a **Pressure Success** ($I_i = 1$) if $\\text{NetMatchDVA} > 0$.
            
            To account for delivery volume within each match, matches are weighted by logarithmic exposure:
            $$w_{ij} = \\ln(1 + B_{ij})$$
            $$\\text{PSR}_{\\text{exp}} = \\frac{\\sum_j w_{ij} I_{ij}}{\\sum_j w_{ij}}$$
        """)
        
    with st.expander("4. Empirical Bayes Shrinkage Toward IPL Cohort Priors", expanded=False):
        st.markdown("""
            To prevent small-sample distortion, observed exposure PSR is shrunk toward the empirical prior mean $\\mu_{\\text{exp}}$ of the qualified IPL cohort:
            $$\\theta^* = \\left(\\frac{N}{N + K}\\right) \\text{PSR}_{\\text{exp}} + \\left(\\frac{K}{N + K}\\right) \\mu_{\\text{exp}}$$
            
            **Approved Operational Anchors:**
            - **Batters**: $K_{\\text{batter}} = 50$ pressure balls faced ($\mu_{\\text{exp}} = 0.4303$)
            - **Bowlers**: $K_{\\text{bowler}} = 48$ legal pressure balls bowled ($\mu_{\\text{exp}} = 0.6210$)
        """)
        
    with st.expander("5. Volatility Stabilizer (\\kappa) & Final Composite Score", expanded=False):
        st.markdown("""
            To penalize inconsistent 'one-hit wonders' who fluctuate erratically, match-to-match standard deviation $\\sigma_{\\text{match}}$ is stabilized against the cohort interquartile range ($\\text{IQR}_{\\text{cohort}}$):
            
            $$\\kappa_i = 1.0 - 0.25 \\times \\tanh\\left(\\frac{\\sigma_i}{\\text{IQR}_{\\text{cohort}}}\\right)$$
            
            **Final Composite Reliability Score:**
            $$\\text{ReliabilityScore}_i = \\theta^*_i \\times \\kappa_i$$
            The score rewards both high success rates and reliable consistency across appearances.
        """)
        
    with st.expander("6. Qualification Criteria & Sample Attrition", expanded=False):
        st.markdown("""
            | Cohort | Pressure Exposure | Qualifying Matches | Career IPL Sample | Qualified Count |
            | :--- | :---: | :---: | :---: | :---: |
            | **IPL Batters** | $\\ge 40$ pressure balls faced | $\\ge 6$ matches ($\ge 3$ balls or out) | $\\ge 120$ career IPL balls | **45** / 341 (13.2%) |
            | **IPL Bowlers** | $\\ge 36$ legal pressure balls | $\\ge 6$ matches ($\ge 6$ legal balls) | $\\ge 120$ career IPL balls | **53** / 260 (20.4%) |
        """)
        
    with st.expander("7. Data Scope & Limitations", expanded=False):
        st.markdown("""
            - **Strict Competition Isolation**: Filtered strictly to IPL seasons 2022–2026. Exactly 0 Men's T20I matches are included in the IPL rankings.
            - **Tracking Data Limitations**: Advanced optical trajectory systems (e.g. 3D high-frame rate coordinate cameras) are proprietary broadcast feeds not present in standard scorecard delivery feeds, and are not fabricated.
            - **Pakistani International Players**: Players such as Mohammad Nawaz, Shadab Khan, and Abrar Ahmed appear in T20Is but have 0 IPL matches, and are naturally excluded from IPL rankings.
        """)

    render_html("""
        <div style="margin-top: 24px; margin-bottom: 14px;">
            <h2 style="margin: 0; font-size: 20px; font-weight: 600; color: #25233A;">
                Methodology Summary: Standard vs SupeRR Selector Metrics
            </h2>
            <p style="color: #77758A; font-size: 0.88rem; margin-top: 2px;">
                Direct architectural comparison of classical cricket box score metrics against Phase 3A Version 2.2 pressure formulations.
            </p>
        </div>
    """)

    methodology_summary_data = pd.DataFrame([
        {
            "Analytical Dimension": "Batting Acceleration",
            "Standard Box-Score Metric": "Career Strike Rate (SR)",
            "SupeRR Selector Metric": "Delta Strike Rate (Delta SR)",
            "Mathematical Formula": "SR_pressure - SR_baseline",
            "Scouting Rationale": "Isolates rapid run acceleration under intense match pressure from low-stakes pacing."
        },
        {
            "Analytical Dimension": "Bowling Run Restriction",
            "Standard Box-Score Metric": "Career Economy Rate",
            "SupeRR Selector Metric": "Clutch Economy Suppression",
            "Mathematical Formula": "Econ_baseline - Econ_pressure",
            "Scouting Rationale": "Rewards bowlers who actively suppress scoring rates under high chase and death leverage."
        },
        {
            "Analytical Dimension": "Net Delivery Contribution",
            "Standard Box-Score Metric": "Total Runs / Wickets",
            "SupeRR Selector Metric": "Delivery Value Added (DVA)",
            "Mathematical Formula": "Runs_actual - Par(Phase, Inn) +/- Wicket_Credit",
            "Scouting Rationale": "Calibrates every single ball against historical format par baselines for that exact match situation."
        },
        {
            "Analytical Dimension": "Match Success Aggregation",
            "Standard Box-Score Metric": "Win-Loss Records",
            "SupeRR Selector Metric": "Exposure-Weighted PSR",
            "Mathematical Formula": "Sum(w_i * I_i) / Sum(w_i), where w_i = ln(1 + B_i)",
            "Scouting Rationale": "Weights high-delivery clutch appearances more heavily than incidental 1-ball cameos."
        },
        {
            "Analytical Dimension": "Small-Sample Noise Control",
            "Standard Box-Score Metric": "Raw PSR / Win Rate",
            "SupeRR Selector Metric": "Empirical Bayes Shrunk PSR (theta*)",
            "Mathematical Formula": "(N / (N + K)) * PSR_exp + (K / (N + K)) * mu_exp",
            "Scouting Rationale": "Regresses unproven players toward the validated IPL cohort prior (mu=0.4303 bat, mu=0.6210 bowl)."
        },
        {
            "Analytical Dimension": "Consistency Stabilization",
            "Standard Box-Score Metric": "Standard Deviation",
            "SupeRR Selector Metric": "Volatility Penalty (kappa)",
            "Mathematical Formula": "1.0 - 0.25 * tanh(sigma_i / IQR_cohort)",
            "Scouting Rationale": "Penalizes erratic boom-or-bust performers, rewarding repeatable high-leverage execution."
        },
        {
            "Analytical Dimension": "Definitive Reliability Index",
            "Standard Box-Score Metric": "Unweighted Leaderboard",
            "SupeRR Selector Metric": "Final Composite Reliability Score",
            "Mathematical Formula": "theta* * kappa",
            "Scouting Rationale": "Unifies Bayesian shrunk execution rate with match consistency into a single bounded score."
        }
    ])

    st.dataframe(methodology_summary_data, use_container_width=True, hide_index=True)

