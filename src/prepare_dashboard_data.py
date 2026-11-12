"""
Cricket Pressure Index - Phase 5: Dashboard Data Preparation
============================================================
Prepares high-performance cached datasets for the Streamlit dashboard:
1. data/processed/ipl_all_players.csv (All 601 players with qualification & reliability scores)
2. data/processed/ipl_player_match_history.csv (Match-by-match breakdowns)
3. data/processed/ipl_player_phase_breakdown.csv (Powerplay, Middle, Death breakdowns)
4. data/processed/ipl_pressure_overview.json (Macro distributions, season/team/phase breakdowns)

Strictly uses approved Phase 3A Version 2.2 methodology and Phase 4 validated rankings.
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd

def run_data_preparation():
    start_time = time.time()
    print("=" * 80)
    print("STARTING DASHBOARD DATA PREPARATION FOR STREAMLIT APPLICATION")
    print("=" * 80)
    
    # 1. Load Datasets
    print("[1/5] Loading master datasets...")
    comps_path = 'data/processed/clean_competitions.csv'
    matches_path = 'data/processed/clean_matches.csv'
    teams_path = 'data/processed/clean_teams.csv'
    p11_path = 'data/processed/clean_playing_eleven.csv'
    deliv_path = 'data/processed/delivery_dva.csv'
    pm_path = 'data/processed/player_match_dva.csv'
    
    df_comps = pd.read_csv(comps_path)
    df_matches = pd.read_csv(matches_path)
    df_teams = pd.read_csv(teams_path)
    df_p11 = pd.read_csv(p11_path)
    
    ipl_comp_ids = set(df_comps[df_comps['is_ipl']]['comp_id'].tolist())
    print(f"      Identified {len(ipl_comp_ids)} IPL Competitions: {sorted(list(ipl_comp_ids))}")
    
    df_matches_ipl = df_matches[df_matches['comp_id'].isin(ipl_comp_ids)].copy()
    df_matches_ipl['season'] = df_matches_ipl['match_date'].astype(str).str[:4]
    
    # Team dictionary mapping (comp_id, team_id) -> team_name
    team_dict = {}
    for _, row in df_teams[df_teams['comp_id'].isin(ipl_comp_ids)].iterrows():
        team_dict[(row['comp_id'], row['team_id'])] = row['team_name']
        team_dict[row['team_id']] = row['team_name']  # fallback
        
    match_meta = {}
    for _, row in df_matches_ipl.iterrows():
        mid = row['match_id']
        cid = row['comp_id']
        ht = row['home_team']
        at = row['away_team']
        wt = team_dict.get(row['win_team_id'], 'No Result') if pd.notnull(row['win_team_id']) else 'No Result'
        match_meta[mid] = {
            'match_date': str(row['match_date']),
            'season': str(row['season']),
            'home_team': ht,
            'away_team': at,
            'winner': wt,
            'result': str(row['result']) if pd.notnull(row['result']) else 'No Result',
            'venue_country': str(row['venue_country']),
            'is_knockout': bool(row['is_knockout'])
        }

    # Load delivery & player-match datasets filtered to IPL
    print("[2/5] Filtering delivery and player-match datasets to IPL...")
    df_deliv = pd.read_csv(deliv_path, low_memory=False)
    deliv_ipl = df_deliv[df_deliv['comp_id'].isin(ipl_comp_ids)].copy()
    del df_deliv  # free memory
    
    df_pm = pd.read_csv(pm_path)
    pm_ipl = df_pm[df_pm['comp_id'].isin(ipl_comp_ids)].copy()
    del df_pm  # free memory
    
    print(f"      Filtered Deliveries: {len(deliv_ipl):,}")
    print(f"      Filtered Player-Matches: {len(pm_ipl):,}")
    
    # Player Franchise Map
    p11_ipl = df_p11[df_p11['match_id'].isin(df_matches_ipl['match_id'])].merge(
        df_matches_ipl[['match_id', 'comp_id', 'season']], on='match_id'
    )
    p11_ipl = p11_ipl.merge(df_teams, on=['comp_id', 'team_id'], how='left')
    
    player_franchises = {}
    player_seasons = {}
    for pid, grp in p11_ipl.groupby('player_id'):
        fr_list = sorted(grp['team_name'].dropna().unique().tolist())
        se_list = sorted(grp['season'].dropna().unique().tolist())
        player_franchises[pid] = ", ".join(fr_list) if fr_list else "Unknown"
        player_seasons[pid] = ", ".join([str(s) for s in se_list]) if se_list else "Unknown"

    # 2. Player Aggregation & Scores
    print("[3/5] Computing all-player career, pressure, qualification, and reliability metrics...")
    
    # Read existing Phase 4 final rankings and all-player scores
    df_final_ipl = pd.read_csv('data/processed/ipl_final_rankings.csv')
    top_bat_dict = {row['player_id']: row for _, row in df_final_ipl[df_final_ipl['role'] == 'batter'].iterrows()}
    top_bowl_dict = {row['player_id']: row for _, row in df_final_ipl[df_final_ipl['role'] == 'bowler'].iterrows()}
    
    df_all_scores = pd.read_csv('data/processed/ipl_all_player_scores.csv')
    scores_dict = {(int(r['player_id']), str(r['role'])): r for _, r in df_all_scores.iterrows()}
    
    all_players = []
    
    # A. Batters
    bat_delivs = deliv_ipl[deliv_ipl['is_batter_ball_faced']].copy()
    for pid, grp in bat_delivs.groupby('striker_id'):
        pname = grp['striker_name'].iloc[0]
        match_grp = pm_ipl[(pm_ipl['player_id'] == pid) & (pm_ipl['role'] == 'batter')]
        
        grp_press = grp[grp['is_high_pressure']]
        grp_base = grp[(~grp['is_high_pressure']) & (grp['innings'] <= 2)]
        
        tot_balls = len(grp)
        tot_runs = int(grp['runs'].sum())
        tot_dismissals = int(grp['is_striker_dismissed'].sum())
        tot_fours = int(grp['is_four'].sum())
        tot_sixes = int(grp['is_six'].sum())
        tot_dots = int(((grp['runs'] == 0) & grp['extras_type'].isnull()).sum())
        tot_dva = float(grp['dva_batter'].sum())
        avg_dva = float(tot_dva / tot_balls) if tot_balls > 0 else 0.0
        tot_sr = float((tot_runs / tot_balls) * 100.0) if tot_balls > 0 else 0.0
        tot_avg = round(float(tot_runs / tot_dismissals), 2) if tot_dismissals > 0 else None
        
        press_balls = len(grp_press)
        press_runs = int(grp_press['runs'].sum()) if press_balls > 0 else 0
        press_dismissals = int(grp_press['is_striker_dismissed'].sum()) if press_balls > 0 else 0
        press_fours = int(grp_press['is_four'].sum()) if press_balls > 0 else 0
        press_sixes = int(grp_press['is_six'].sum()) if press_balls > 0 else 0
        press_dots = int(((grp_press['runs'] == 0) & grp_press['extras_type'].isnull()).sum()) if press_balls > 0 else 0
        press_dva = float(grp_press['dva_batter'].sum()) if press_balls > 0 else 0.0
        press_dva_per_ball = round(float(press_dva / press_balls), 4) if press_balls > 0 else None
        press_sr = round(float((press_runs / press_balls) * 100.0), 2) if press_balls > 0 else None
        press_avg = round(float(press_runs / press_dismissals), 2) if press_dismissals > 0 else None
        press_dot_pct = round(float((press_dots / press_balls) * 100.0), 2) if press_balls > 0 else None
        press_bdry_pct = round(float(((press_fours + press_sixes) / press_balls) * 100.0), 2) if press_balls > 0 else None
        
        base_balls = len(grp_base)
        base_runs = int(grp_base['runs'].sum()) if base_balls > 0 else 0
        base_dismissals = int(grp_base['is_striker_dismissed'].sum()) if base_balls > 0 else 0
        base_dva = float(grp_base['dva_batter'].sum()) if base_balls > 0 else 0.0
        base_sr = round(float((base_runs / base_balls) * 100.0), 2) if base_balls > 0 else None
        base_dva_per_ball = round(float(base_dva / base_balls), 4) if base_balls > 0 else None
        
        delta_sr = round(press_sr - base_sr, 2) if (press_sr is not None and base_sr is not None) else None
        delta_dva = round(press_dva_per_ball - base_dva_per_ball, 4) if (press_dva_per_ball is not None and base_dva_per_ball is not None) else None
        
        tot_matches = len(match_grp)
        press_matches = int(match_grp['is_pressure_involved'].sum())
        psr_matches = int(match_grp['is_match_eligible_for_psr'].sum())
        successful_matches = int(match_grp['is_successful_pressure_match'].sum())
        
        # Qualification check
        q_career = bool(tot_balls >= 120)
        q_press = bool(press_balls >= 40)
        q_psr = bool(psr_matches >= 6)
        is_qual = bool(q_career and q_press and q_psr)
        
        reasons = []
        if not q_press:
            reasons.append(f"Pressure balls faced ({press_balls}) < 40 required")
        if not q_psr:
            reasons.append(f"Qualifying PSR matches ({psr_matches}) < 6 required")
        if not q_career:
            reasons.append(f"Career IPL balls faced ({tot_balls}) < 120 required")
        unqual_str = "; ".join(reasons) if not is_qual else "Fully Qualified"
        
        # Score and rank info from all_scores and top_info
        score_info = scores_dict.get((pid, 'batter'), {})
        top_info = top_bat_dict.get(pid, None)
        
        p_rank = int(top_info['rank']) if top_info is not None else (int(score_info['rank']) if pd.notnull(score_info.get('rank')) else None)
        p_raw_psr = round(float(score_info['raw_psr']), 4) if pd.notnull(score_info.get('raw_psr')) else (round(successful_matches / psr_matches, 4) if psr_matches > 0 else 0.0)
        p_exp_psr = round(float(score_info['exposure_weighted_psr']), 4) if pd.notnull(score_info.get('exposure_weighted_psr')) else None
        p_shrunk_psr = round(float(score_info['shrunk_exposure_weighted_psr']), 4) if pd.notnull(score_info.get('shrunk_exposure_weighted_psr')) else None
        p_kappa = round(float(score_info['volatility_penalty_kappa']), 4) if pd.notnull(score_info.get('volatility_penalty_kappa')) else None
        p_final_score = round(float(score_info['reliability_score_psr']), 4) if pd.notnull(score_info.get('reliability_score_psr')) else None
        
        all_players.append({
            'player_id': pid,
            'player_name': pname,
            'role': 'batter',
            'ipl_franchises': player_franchises.get(pid, "Unknown"),
            'seasons_played': player_seasons.get(pid, "Unknown"),
            'total_matches': tot_matches,
            'pressure_matches': press_matches,
            'psr_qualifying_matches': psr_matches,
            'successful_matches': successful_matches,
            'career_eligible_balls': tot_balls,
            'career_runs': tot_runs,
            'career_dismissals': tot_dismissals,
            'career_strike_rate': tot_sr,
            'career_average': tot_avg,
            'career_cumulative_dva': round(tot_dva, 4),
            'career_dva_per_ball': round(avg_dva, 4),
            'pressure_exposure_balls': press_balls,
            'pressure_runs': press_runs,
            'pressure_dismissals': press_dismissals,
            'pressure_strike_rate': press_sr,
            'pressure_average': press_avg,
            'pressure_fours': press_fours,
            'pressure_sixes': press_sixes,
            'pressure_dot_pct': press_dot_pct,
            'pressure_boundary_pct': press_bdry_pct,
            'pressure_cumulative_dva': round(press_dva, 4),
            'pressure_dva_per_ball': press_dva_per_ball,
            'baseline_eligible_balls': base_balls,
            'baseline_runs': base_runs,
            'baseline_strike_rate': base_sr,
            'baseline_dva_per_ball': base_dva_per_ball,
            'delta_strike_rate': delta_sr,
            'delta_dva_per_ball': delta_dva,
            'clutch_econ_suppression': None,
            'career_economy_rate': None,
            'pressure_economy_rate': None,
            'baseline_economy_rate': None,
            'qualifies_career_balls': q_career,
            'qualifies_pressure_balls': q_press,
            'qualifies_psr_matches': q_psr,
            'is_qualified': is_qual,
            'qualification_status': "Qualified" if is_qual else "Not Qualified",
            'unqualified_reasons': unqual_str,
            'rank': p_rank,
            'raw_psr': p_raw_psr,
            'exposure_weighted_psr': p_exp_psr,
            'shrunk_exposure_weighted_psr': p_shrunk_psr,
            'volatility_penalty_kappa': p_kappa,
            'final_composite_score': p_final_score,
            'min_grid_rank': int(top_info['min_grid_rank']) if top_info is not None else None,
            'max_grid_rank': int(top_info['max_grid_rank']) if top_info is not None else None,
            'rank_shift': int(top_info['rank_shift']) if top_info is not None else None,
            'remains_top10_all_k': bool(top_info['remains_top10_all_k']) if top_info is not None else False
        })
        
    # B. Bowlers
    for pid, grp in deliv_ipl.groupby('bowler_id'):
        pname = grp['bowler_name'].iloc[0]
        match_grp = pm_ipl[(pm_ipl['player_id'] == pid) & (pm_ipl['role'] == 'bowler')]
        
        grp_press = grp[grp['is_high_pressure']]
        grp_base = grp[(~grp['is_high_pressure']) & (grp['innings'] <= 2)]
        
        tot_legal = int(grp['is_bowler_legal_ball'].sum())
        tot_runs = int(grp['bowler_runs_conceded'].sum())
        tot_wkts = int(grp['is_bowler_wicket'].sum())
        tot_fours = int(grp['is_four'].sum())
        tot_sixes = int(grp['is_six'].sum())
        tot_dots = int(((grp['bowler_runs_conceded'] == 0) & grp['is_bowler_legal_ball']).sum())
        tot_dva = float(grp['dva_bowler'].sum())
        avg_dva = float(tot_dva / tot_legal) if tot_legal > 0 else 0.0
        tot_econ = round(float((tot_runs / tot_legal) * 6.0), 2) if tot_legal > 0 else None
        tot_bowl_sr = round(float(tot_legal / tot_wkts), 2) if tot_wkts > 0 else None
        tot_bowl_avg = round(float(tot_runs / tot_wkts), 2) if tot_wkts > 0 else None
        
        press_legal = int(grp_press['is_bowler_legal_ball'].sum())
        press_runs = int(grp_press['bowler_runs_conceded'].sum()) if press_legal > 0 else 0
        press_wkts = int(grp_press['is_bowler_wicket'].sum()) if press_legal > 0 else 0
        press_fours = int(grp_press['is_four'].sum()) if press_legal > 0 else 0
        press_sixes = int(grp_press['is_six'].sum()) if press_legal > 0 else 0
        press_dots = int(((grp_press['bowler_runs_conceded'] == 0) & grp_press['is_bowler_legal_ball']).sum()) if press_legal > 0 else 0
        press_dva = float(grp_press['dva_bowler'].sum()) if press_legal > 0 else 0.0
        press_dva_per_ball = round(float(press_dva / press_legal), 4) if press_legal > 0 else None
        press_econ = round(float((press_runs / press_legal) * 6.0), 2) if press_legal > 0 else None
        press_bowl_sr = round(float(press_legal / press_wkts), 2) if press_wkts > 0 else None
        press_dot_pct = round(float((press_dots / press_legal) * 100.0), 2) if press_legal > 0 else None
        press_bdry_pct = round(float(((press_fours + press_sixes) / press_legal) * 100.0), 2) if press_legal > 0 else None
        
        base_legal = int(grp_base['is_bowler_legal_ball'].sum())
        base_runs = int(grp_base['bowler_runs_conceded'].sum()) if base_legal > 0 else 0
        base_wkts = int(grp_base['is_bowler_wicket'].sum()) if base_legal > 0 else 0
        base_dva = float(grp_base['dva_bowler'].sum()) if base_legal > 0 else 0.0
        base_econ = round(float((base_runs / base_legal) * 6.0), 2) if base_legal > 0 else None
        base_dva_per_ball = round(float(base_dva / base_legal), 4) if base_legal > 0 else None
        
        clutch_econ = round(base_econ - press_econ, 2) if (base_econ is not None and press_econ is not None) else None
        delta_dva = round(press_dva_per_ball - base_dva_per_ball, 4) if (press_dva_per_ball is not None and base_dva_per_ball is not None) else None
        
        tot_matches = len(match_grp)
        press_matches = int(match_grp['is_pressure_involved'].sum())
        psr_matches = int(match_grp['is_match_eligible_for_psr'].sum())
        successful_matches = int(match_grp['is_successful_pressure_match'].sum())
        
        # Qualification check
        q_career = bool(tot_legal >= 120)
        q_press = bool(press_legal >= 36)
        q_psr = bool(psr_matches >= 6)
        is_qual = bool(q_career and q_press and q_psr)
        
        reasons = []
        if not q_press:
            reasons.append(f"Pressure legal balls bowled ({press_legal}) < 36 required")
        if not q_psr:
            reasons.append(f"Qualifying PSR matches ({psr_matches}) < 6 required")
        if not q_career:
            reasons.append(f"Career IPL legal balls bowled ({tot_legal}) < 120 required")
        unqual_str = "; ".join(reasons) if not is_qual else "Fully Qualified"
        
        # Score and rank info from all_scores and top_info
        score_info = scores_dict.get((pid, 'bowler'), {})
        top_info = top_bowl_dict.get(pid, None)
        
        p_rank = int(top_info['rank']) if top_info is not None else (int(score_info['rank']) if pd.notnull(score_info.get('rank')) else None)
        p_raw_psr = round(float(score_info['raw_psr']), 4) if pd.notnull(score_info.get('raw_psr')) else (round(successful_matches / psr_matches, 4) if psr_matches > 0 else 0.0)
        p_exp_psr = round(float(score_info['exposure_weighted_psr']), 4) if pd.notnull(score_info.get('exposure_weighted_psr')) else None
        p_shrunk_psr = round(float(score_info['shrunk_exposure_weighted_psr']), 4) if pd.notnull(score_info.get('shrunk_exposure_weighted_psr')) else None
        p_kappa = round(float(score_info['volatility_penalty_kappa']), 4) if pd.notnull(score_info.get('volatility_penalty_kappa')) else None
        p_final_score = round(float(score_info['reliability_score_psr']), 4) if pd.notnull(score_info.get('reliability_score_psr')) else None
        
        all_players.append({
            'player_id': pid,
            'player_name': pname,
            'role': 'bowler',
            'ipl_franchises': player_franchises.get(pid, "Unknown"),
            'seasons_played': player_seasons.get(pid, "Unknown"),
            'total_matches': tot_matches,
            'pressure_matches': press_matches,
            'psr_qualifying_matches': psr_matches,
            'successful_matches': successful_matches,
            'career_eligible_balls': tot_legal,
            'career_runs': tot_runs,
            'career_dismissals': tot_wkts,
            'career_strike_rate': tot_bowl_sr,
            'career_average': tot_bowl_avg,
            'career_cumulative_dva': round(tot_dva, 4),
            'career_dva_per_ball': round(avg_dva, 4),
            'pressure_exposure_balls': press_legal,
            'pressure_runs': press_runs,
            'pressure_dismissals': press_wkts,
            'pressure_strike_rate': press_bowl_sr,
            'pressure_average': None,
            'pressure_fours': press_fours,
            'pressure_sixes': press_sixes,
            'pressure_dot_pct': press_dot_pct,
            'pressure_boundary_pct': press_bdry_pct,
            'pressure_cumulative_dva': round(press_dva, 4),
            'pressure_dva_per_ball': press_dva_per_ball,
            'baseline_eligible_balls': base_legal,
            'baseline_runs': base_runs,
            'baseline_strike_rate': None,
            'baseline_dva_per_ball': base_dva_per_ball,
            'delta_strike_rate': None,
            'delta_dva_per_ball': delta_dva,
            'clutch_econ_suppression': clutch_econ,
            'career_economy_rate': tot_econ,
            'pressure_economy_rate': press_econ,
            'baseline_economy_rate': base_econ,
            'qualifies_career_balls': q_career,
            'qualifies_pressure_balls': q_press,
            'qualifies_psr_matches': q_psr,
            'is_qualified': is_qual,
            'qualification_status': "Qualified" if is_qual else "Not Qualified",
            'unqualified_reasons': unqual_str,
            'rank': p_rank,
            'raw_psr': p_raw_psr,
            'exposure_weighted_psr': p_exp_psr,
            'shrunk_exposure_weighted_psr': p_shrunk_psr,
            'volatility_penalty_kappa': p_kappa,
            'final_composite_score': p_final_score,
            'min_grid_rank': int(top_info['min_grid_rank']) if top_info is not None else None,
            'max_grid_rank': int(top_info['max_grid_rank']) if top_info is not None else None,
            'rank_shift': int(top_info['rank_shift']) if top_info is not None else None,
            'remains_top10_all_k': bool(top_info['remains_top10_all_k']) if top_info is not None else False
        })
        
    df_all_players = pd.DataFrame(all_players)
    players_out_path = 'data/processed/ipl_all_players.csv'
    df_all_players.to_csv(players_out_path, index=False)
    print(f"      Saved {players_out_path} ({len(df_all_players)} players)")

    # 3. Match-by-match Player Breakdown
    print("[4/5] Preparing match history and phase breakdowns...")
    match_history = []
    for _, row in pm_ipl.iterrows():
        mid = row['match_id']
        pid = row['player_id']
        role = row['role']
        mm = match_meta.get(mid, {})
        
        match_history.append({
            'match_id': mid,
            'match_date': mm.get('match_date', str(row.get('match_date', ''))),
            'season': mm.get('season', str(row.get('season', ''))),
            'home_team': mm.get('home_team', ''),
            'away_team': mm.get('away_team', ''),
            'winner': mm.get('winner', ''),
            'result': mm.get('result', ''),
            'player_id': pid,
            'player_name': row['player_name'],
            'role': role,
            'is_pressure_involved': bool(row['is_pressure_involved']),
            'is_match_eligible_for_psr': bool(row['is_match_eligible_for_psr']),
            'pressure_eligible_balls': int(row['pressure_eligible_balls']),
            'pressure_runs': int(row['pressure_runs']),
            'pressure_wickets_or_dismissals': int(row['pressure_wickets_or_dismissals']),
            'pressure_dva': round(float(row['pressure_dva']), 4),
            'pressure_metric': round(float(row['pressure_sr']), 2) if role == 'batter' and pd.notnull(row['pressure_sr']) else (round(float(row['pressure_econ']), 2) if role == 'bowler' and pd.notnull(row['pressure_econ']) else None),
            'is_successful_pressure_match': bool(row['is_successful_pressure_match']),
            'total_eligible_balls': int(row['total_eligible_balls']),
            'total_runs': int(row['total_runs']),
            'total_wickets_or_dismissals': int(row['total_wickets_or_dismissals']),
            'total_dva': round(float(row['match_total_dva']), 4)
        })
    df_match_history = pd.DataFrame(match_history)
    history_out_path = 'data/processed/ipl_player_match_history.csv'
    df_match_history.to_csv(history_out_path, index=False)
    print(f"      Saved {history_out_path} ({len(df_match_history)} records)")

    # 4. Phase Breakdown (Powerplay 1-6, Middle 7-15, Death 16-20)
    # Using deliv_ipl['innings_phase']
    phase_stats = []
    
    # Batters phase stats
    for (pid, phase), grp in bat_delivs.groupby(['striker_id', 'innings_phase']):
        grp_press = grp[grp['is_high_pressure']]
        b_all = len(grp)
        r_all = int(grp['runs'].sum())
        w_all = int(grp['is_striker_dismissed'].sum())
        sr_all = round((r_all / b_all) * 100.0, 2) if b_all > 0 else 0.0
        dva_all = round(float(grp['dva_batter'].sum()), 4)
        
        b_pr = len(grp_press)
        r_pr = int(grp_press['runs'].sum()) if b_pr > 0 else 0
        w_pr = int(grp_press['is_striker_dismissed'].sum()) if b_pr > 0 else 0
        sr_pr = round((r_pr / b_pr) * 100.0, 2) if b_pr > 0 else None
        dva_pr = round(float(grp_press['dva_batter'].sum()), 4) if b_pr > 0 else 0.0
        
        phase_stats.append({
            'player_id': pid,
            'role': 'batter',
            'phase': phase,
            'overall_balls': b_all,
            'overall_runs': r_all,
            'overall_wickets': w_all,
            'overall_metric': sr_all,
            'overall_dva': dva_all,
            'pressure_balls': b_pr,
            'pressure_runs': r_pr,
            'pressure_wickets': w_pr,
            'pressure_metric': sr_pr,
            'pressure_dva': dva_pr
        })
        
    # Bowlers phase stats
    bowl_delivs = deliv_ipl[deliv_ipl['is_bowler_legal_ball']].copy()
    for (pid, phase), grp in bowl_delivs.groupby(['bowler_id', 'innings_phase']):
        grp_press = grp[grp['is_high_pressure']]
        b_all = len(grp)
        r_all = int(grp['bowler_runs_conceded'].sum())
        w_all = int(grp['is_bowler_wicket'].sum())
        econ_all = round((r_all / b_all) * 6.0, 2) if b_all > 0 else 0.0
        dva_all = round(float(grp['dva_bowler'].sum()), 4)
        
        b_pr = len(grp_press)
        r_pr = int(grp_press['bowler_runs_conceded'].sum()) if b_pr > 0 else 0
        w_pr = int(grp_press['is_bowler_wicket'].sum()) if b_pr > 0 else 0
        econ_pr = round((r_pr / b_pr) * 6.0, 2) if b_pr > 0 else None
        dva_pr = round(float(grp_press['dva_bowler'].sum()), 4) if b_pr > 0 else 0.0
        
        phase_stats.append({
            'player_id': pid,
            'role': 'bowler',
            'phase': phase,
            'overall_balls': b_all,
            'overall_runs': r_all,
            'overall_wickets': w_all,
            'overall_metric': econ_all,
            'overall_dva': dva_all,
            'pressure_balls': b_pr,
            'pressure_runs': r_pr,
            'pressure_wickets': w_pr,
            'pressure_metric': econ_pr,
            'pressure_dva': dva_pr
        })
    df_phase_stats = pd.DataFrame(phase_stats)
    phase_out_path = 'data/processed/ipl_player_phase_breakdown.csv'
    df_phase_stats.to_csv(phase_out_path, index=False)
    print(f"      Saved {phase_out_path} ({len(df_phase_stats)} records)")

    # 5. Macro Distributions & Pressure Overview
    print("[5/5] Computing macro pressure distributions...")
    
    # Tier breakdown
    tier_counts = deliv_ipl['pressure_tier'].value_counts().to_dict()
    tier_pcts = {k: round(v / len(deliv_ipl) * 100.0, 2) for k, v in tier_counts.items()}
    
    # Innings breakdown
    deliv_ipl_std = deliv_ipl[deliv_ipl['innings'].isin([1, 2])]
    inn_grp = deliv_ipl_std.groupby('innings')
    inn_summary = {}
    for inn, grp in inn_grp:
        inn_summary[int(inn)] = {
            'total_deliveries': len(grp),
            'high_pressure_deliveries': int(grp['is_high_pressure'].sum()),
            'pct_high_pressure': round(grp['is_high_pressure'].mean() * 100.0, 2),
            'mean_pi': round(grp['pressure_index'].mean(), 4)
        }
        
    # Phase breakdown
    phase_grp = deliv_ipl.groupby('innings_phase')
    phase_summary = {}
    for ph, grp in phase_grp:
        phase_summary[ph] = {
            'total_deliveries': len(grp),
            'high_pressure_deliveries': int(grp['is_high_pressure'].sum()),
            'pct_high_pressure': round(grp['is_high_pressure'].mean() * 100.0, 2),
            'mean_pi': round(grp['pressure_index'].mean(), 4)
        }
        
    # Season breakdown
    deliv_ipl['season_str'] = deliv_ipl['match_date'].astype(str).str[:4]
    season_grp = deliv_ipl.groupby('season_str')
    season_summary = {}
    for sea, grp in season_grp:
        season_summary[sea] = {
            'total_matches': int(grp['match_id'].nunique()),
            'total_deliveries': len(grp),
            'high_pressure_deliveries': int(grp['is_high_pressure'].sum()),
            'pct_high_pressure': round(grp['is_high_pressure'].mean() * 100.0, 2),
            'mean_pi': round(grp['pressure_index'].mean(), 4)
        }
        
    # Team breakdown (by batting team)
    team_summary = {}
    for (cid, tid), grp in deliv_ipl.groupby(['comp_id', 'batting_team_id']):
        tname = team_dict.get((cid, tid), team_dict.get(tid, f"Team_{tid}"))
        if tname not in team_summary:
            team_summary[tname] = {'total_deliveries': 0, 'high_pressure_deliveries': 0}
        team_summary[tname]['total_deliveries'] += len(grp)
        team_summary[tname]['high_pressure_deliveries'] += int(grp['is_high_pressure'].sum())
    for tname in team_summary:
        tot = team_summary[tname]['total_deliveries']
        hp = team_summary[tname]['high_pressure_deliveries']
        team_summary[tname]['pct_high_pressure'] = round(hp / tot * 100.0, 2) if tot > 0 else 0.0

    # Top 10 high-pressure match situations (highest mean PI in 2nd innings death overs)
    tense_matches = []
    for mid, grp in deliv_ipl.groupby('match_id'):
        grp_chase_death = grp[(grp['innings'] == 2) & (grp['innings_phase'] == 'Death')]
        if len(grp_chase_death) >= 6:
            mm = match_meta.get(mid, {})
            tense_matches.append({
                'match_id': mid,
                'match_date': mm.get('match_date', ''),
                'season': mm.get('season', ''),
                'home_team': mm.get('home_team', ''),
                'away_team': mm.get('away_team', ''),
                'result': mm.get('result', ''),
                'death_balls': len(grp_chase_death),
                'death_high_press_balls': int(grp_chase_death['is_high_pressure'].sum()),
                'death_mean_pi': round(grp_chase_death['pressure_index'].mean(), 4),
                'max_pi': round(grp['pressure_index'].max(), 4)
            })
    df_tense = pd.DataFrame(tense_matches).sort_values(by='death_mean_pi', ascending=False).head(10)
    top_tense_situations = df_tense.to_dict(orient='records')
    
    overview_data = {
        'total_matches': 371,
        'total_deliveries': len(deliv_ipl),
        'high_pressure_deliveries': int(deliv_ipl['is_high_pressure'].sum()),
        'pct_high_pressure': round(deliv_ipl['is_high_pressure'].mean() * 100.0, 2),
        'total_batters_evaluated': 341,
        'qualified_batters': 45,
        'total_bowlers_evaluated': 260,
        'qualified_bowlers': 53,
        'top_batter': {
            'player_id': 4708,
            'name': 'Rinku Singh',
            'team': 'Kolkata Knight Riders',
            'reliability_score': 0.5583,
            'exposure_weighted_psr': 0.8263,
            'pressure_balls': 191
        },
        'top_bowler': {
            'player_id': 2933,
            'name': 'Jasprit Bumrah',
            'team': 'Mumbai Indians',
            'reliability_score': 0.6477,
            'exposure_weighted_psr': 0.9464,
            'pressure_legal_balls': 123
        },
        'tier_counts': tier_counts,
        'tier_pcts': tier_pcts,
        'innings_summary': inn_summary,
        'phase_summary': phase_summary,
        'season_summary': season_summary,
        'team_summary': team_summary,
        'top_tense_situations': top_tense_situations
    }
    
    overview_out_path = 'data/processed/ipl_pressure_overview.json'
    with open(overview_out_path, 'w', encoding='utf-8') as f:
        json.dump(overview_data, f, indent=2)
    print(f"      Saved {overview_out_path}")
    
    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"DASHBOARD DATA PREPARATION COMPLETED IN {elapsed:.2f} SECONDS")
    print("=" * 80)

if __name__ == '__main__':
    run_data_preparation()
