"""
SupeRR Selector - Phase 5: Dashboard Data Access Layer
======================================================
Modular, high-performance cached data loaders for the Streamlit dashboard.
Ensures zero redundant calculation inside UI components.
"""

import json
import os
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed')
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')

@st.cache_data(show_spinner=False)
def load_pressure_overview():
    """Load high-level macro statistics and distributions."""
    json_path = os.path.join(DATA_DIR, 'ipl_pressure_overview.json')
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Overview data not found at {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_all_players():
    """Load all 601 evaluated IPL players with performance, qualification, and reliability metrics."""
    csv_path = os.path.join(DATA_DIR, 'ipl_all_players.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"All players data not found at {csv_path}")
    df = pd.read_csv(csv_path)
    # Ensure types
    df['player_id'] = df['player_id'].astype(int)
    if 'rank' in df.columns:
        df['rank'] = pd.to_numeric(df['rank'], errors='coerce')
    return df

@st.cache_data(show_spinner=False)
def load_top10_batters():
    """Load the approved Phase 4 Top 10 Most Reliable IPL Batters."""
    csv_path = os.path.join(REPORTS_DIR, 'ipl_top10_reliable_batters.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Top 10 batters data not found at {csv_path}")
    df = pd.read_csv(csv_path)
    df['rank'] = df['rank'].astype(int)
    df['player_id'] = df['player_id'].astype(int)
    return df

@st.cache_data(show_spinner=False)
def load_top10_bowlers():
    """Load the approved Phase 4 Top 10 Most Reliable IPL Bowlers."""
    csv_path = os.path.join(REPORTS_DIR, 'ipl_top10_reliable_bowlers.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Top 10 bowlers data not found at {csv_path}")
    df = pd.read_csv(csv_path)
    df['rank'] = df['rank'].astype(int)
    df['player_id'] = df['player_id'].astype(int)
    return df

@st.cache_data(show_spinner=False)
def load_player_match_history(player_id=None, role=None):
    """Load match-by-match performance history."""
    csv_path = os.path.join(DATA_DIR, 'ipl_player_match_history.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Player match history not found at {csv_path}")
    df = pd.read_csv(csv_path)
    df['player_id'] = df['player_id'].astype(int)
    if player_id is not None:
        df = df[df['player_id'] == int(player_id)]
    if role is not None:
        df = df[df['role'] == role]
    return df

@st.cache_data(show_spinner=False)
def load_player_phase_breakdown(player_id=None, role=None):
    """Load phase breakdowns (Powerplay, Middle, Death) for players."""
    csv_path = os.path.join(DATA_DIR, 'ipl_player_phase_breakdown.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Player phase breakdown not found at {csv_path}")
    df = pd.read_csv(csv_path)
    df['player_id'] = df['player_id'].astype(int)
    if player_id is not None:
        df = df[df['player_id'] == int(player_id)]
    if role is not None:
        df = df[df['role'] == role]
    return df

@st.cache_data(show_spinner=False)
def load_ipl_matches():
    """Load metadata for all 371 IPL matches (2022-2026)."""
    csv_path = os.path.join(DATA_DIR, 'ipl_matches.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"IPL matches data not found at {csv_path}")
    df = pd.read_csv(csv_path)
    df['match_id'] = df['match_id'].astype(int)
    df['season'] = df['season'].astype(str)
    return df

@st.cache_data(show_spinner=False)
def load_ipl_deliveries(match_id=None):
    """Load ball-by-ball delivery records for IPL matches."""
    parquet_path = os.path.join(DATA_DIR, 'ipl_deliveries.parquet')
    csv_path = os.path.join(DATA_DIR, 'ipl_deliveries.csv')
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path, low_memory=False)
    else:
        raise FileNotFoundError("IPL deliveries file not found in parquet or csv.")
    
    df['match_id'] = df['match_id'].astype(int)
    if match_id is not None:
        df = df[df['match_id'] == int(match_id)]
    return df

@st.cache_data(show_spinner=False)
def load_player_match_deliveries(player_id, match_id=None, role='batter'):
    """Load delivery records where the player was directly involved."""
    df = load_ipl_deliveries(match_id=match_id)
    p_id = int(player_id)
    if role == 'batter':
        df_player = df[df['striker_id'] == p_id].copy()
    else:
        df_player = df[df['bowler_id'] == p_id].copy()
    return df_player
