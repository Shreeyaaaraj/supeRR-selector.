"""
SupeRR Selector - Model B & Model C Production Recruitment Pipeline
===================================================================
Production implementation of Model B and Model C according to the approved
V3.3.3 specification with full technical corrections:

1. Model A: Frozen IPL-only V1 reference (Preserved 100% unchanged).
2. Model B: Pooled IPL + Senior Men's T20I analytical model (equal weight lambda=1.0).
   - EXPLICITLY filters using both is_ipl and is_t20i flags.
3. Model C: IPL-primary + Senior Men's T20I auxiliary recruitment model (lambda=0.50).
   - Unified lambda = 0.50
   - Shrinkage anchors: K=50 for batters, K=48 for bowlers
   - Prior anchors: mu_bat = 0.4303, IQR_bat = 2.4009; mu_bowl = 0.6210, IQR_bowl = 2.7580
   - Three-pillar qualification: C_tot >= 120, B_eff >= 40/36, M_eff >= 6
   - Career balls calculated separately from actual IPL and T20I records
   - Cohort categories: IPL-only, Both, T20I-only
   - Strict exclusion of 54 Pakistani candidates, while retaining opponent performances against Pakistan
   - Exact preservation of Model A scores for IPL-only qualified cohort
   - Pakistan delivery filter: retains striker deliveries for non-Pak batters facing Pak bowlers,
     and bowler deliveries for non-Pak bowlers bowling to Pak batters.
   - Match format labels: explicit 'IPL', 'T20I', or 'Other' (never labeling other comps as T20I).
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd

# Directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'processed')
REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')

# Parameters
LAMBDA = 0.50
K_ANCHORS = {'batter': 50, 'bowler': 48}
GRID_K = {'batter': [25, 50, 75, 100], 'bowler': [25, 48, 75, 100]}
REQ_PRESS_BALLS = {'batter': 40, 'bowler': 36}
REQ_CAREER_BALLS = 120
REQ_MATCHES = 6

# IPL Prior Anchors (from Model A)
IPL_PRIORS = {
    'batter': {'mu': 0.4303, 'iqr': 2.4009},
    'bowler': {'mu': 0.6210, 'iqr': 2.7580}
}


def run_pipeline():
    start_time = time.time()
    print("=" * 80)
    print("STARTING SUPERR SELECTOR MODEL B & MODEL C PRODUCTION PIPELINE (CORRECTED)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. Load Master Datasets & Competition Mappings
    # -------------------------------------------------------------------------
    print("[1/7] Loading master datasets and applying participant filtering...")
    comps_path = os.path.join(DATA_DIR, 'clean_competitions.csv')
    matches_path = os.path.join(DATA_DIR, 'clean_matches.csv')
    teams_path = os.path.join(DATA_DIR, 'clean_teams.csv')
    p11_path = os.path.join(DATA_DIR, 'clean_playing_eleven.csv')
    pm_path = os.path.join(DATA_DIR, 'player_match_dva.csv')
    deliv_path = os.path.join(DATA_DIR, 'delivery_dva.csv')
    orig_a_scores_path = os.path.join(DATA_DIR, 'ipl_all_player_scores.csv')

    df_comps = pd.read_csv(comps_path)
    df_matches = pd.read_csv(matches_path)
    df_teams = pd.read_csv(teams_path)
    df_p11 = pd.read_csv(p11_path)
    df_pm = pd.read_csv(pm_path)
    df_orig_a = pd.read_csv(orig_a_scores_path)

    # Pakistan player IDs from team 25
    pak_ids = set(df_p11[df_p11['team_id'] == 25]['player_id'].unique())
    print(f"      Verified Pakistani candidate IDs to exclude: {len(pak_ids)}")

    # Explicit format mapping for matches (ensures no other competition is labelled T20I)
    m_comp = df_matches.merge(df_comps[['comp_id', 'is_ipl', 'is_t20i']], on='comp_id')
    match_ipl_map = dict(zip(m_comp['match_id'], m_comp['is_ipl'].fillna(False).astype(bool)))
    match_t20i_map = dict(zip(m_comp['match_id'], m_comp['is_t20i'].fillna(False).astype(bool)))
    match_season_map = dict(zip(df_matches['match_id'], df_matches['match_date'].astype(str).str[:4]))

    ipl_cids = set(df_comps[df_comps['is_ipl']]['comp_id'].tolist())
    t20i_cids = set(df_comps[df_comps['is_t20i']]['comp_id'].tolist())
    ipl_or_t20i_cids = ipl_cids | t20i_cids
    print(f"      Competitions: {len(ipl_cids)} IPL, {len(t20i_cids)} Senior Men's T20I (Total: {len(ipl_or_t20i_cids)})")

    # Global player participation categorization (from clean_playing_eleven with is_played == True)
    p11_played = df_p11[(df_p11['is_played'] == True) & (~df_p11['player_id'].isin(pak_ids))].copy()
    p11_comp = p11_played.merge(m_comp[['match_id', 'is_ipl', 'is_t20i']], on='match_id')

    global_part = p11_comp.groupby('player_id').agg(
        ipl_played=('is_ipl', 'sum'),
        t20i_played=('is_t20i', 'sum')
    ).reset_index()

    global_part['category'] = 'IPL-only'
    global_part.loc[(global_part['ipl_played'] > 0) & (global_part['t20i_played'] > 0), 'category'] = 'Both'
    global_part.loc[(global_part['ipl_played'] == 0) & (global_part['t20i_played'] > 0), 'category'] = 'T20I-only'
    cat_dict = dict(zip(global_part['player_id'], global_part['category']))

    # Filter player-match dataset (exclude Pakistani candidates, retain non-Pakistani opponent records)
    clean_pm = df_pm[~df_pm['player_id'].isin(pak_ids)].copy()
    clean_pm['is_ipl'] = clean_pm['match_id'].map(match_ipl_map).fillna(False).astype(bool)
    clean_pm['is_t20i'] = clean_pm['match_id'].map(match_t20i_map).fillna(False).astype(bool)
    clean_pm['season'] = clean_pm['match_id'].map(match_season_map)
    print(f"      Clean non-Pakistani player-match records: {len(clean_pm):,}")

    # Total career balls calculated separately from actual IPL and T20I records (Issue 2 fix)
    cb_ipl = clean_pm[clean_pm['is_ipl']].groupby(['player_id', 'role'])['total_eligible_balls'].sum().to_dict()
    cb_t20i = clean_pm[clean_pm['is_t20i']].groupby(['player_id', 'role'])['total_eligible_balls'].sum().to_dict()

    cb_dict = {}
    for k in set(cb_ipl.keys()) | set(cb_t20i.keys()):
        c_i = int(cb_ipl.get(k, 0))
        c_t = int(cb_t20i.get(k, 0))
        cb_dict[k] = {
            'c_ipl': c_i,
            'c_t20i': c_t,
            'c_tot': c_i + c_t
        }

    # Model A baseline lookup map
    orig_a_map = {}
    for _, r in df_orig_a.iterrows():
        orig_a_map[(int(r['player_id']), str(r['role']))] = {
            'is_qual_a': bool(r['is_qualified']),
            'score_a': float(r['reliability_score_psr']) if pd.notnull(r['reliability_score_psr']) else np.nan,
            'rank_a': int(r['rank']) if pd.notnull(r['rank']) and r['is_qualified'] else None,
            'exp_psr_a': float(r['exposure_weighted_psr']) if pd.notnull(r['exposure_weighted_psr']) else None,
            'shrunk_a': float(r['shrunk_exposure_weighted_psr']) if pd.notnull(r['shrunk_exposure_weighted_psr']) else None,
            'kappa_a': float(r['volatility_penalty_kappa']) if pd.notnull(r['volatility_penalty_kappa']) else None
        }

    # Team mapping
    team_dict = {}
    for _, row in df_teams.iterrows():
        team_dict[(row['comp_id'], row['team_id'])] = row['team_name']
        if row['team_id'] not in team_dict:
            team_dict[row['team_id']] = row['team_name']

    # Franchise / Teams played per player (prioritize IPL franchises for IPL players)
    p11_teams = p11_played.merge(df_matches[['match_id', 'comp_id', 'match_date']], on='match_id')
    p11_teams['season'] = p11_teams['match_date'].astype(str).str[:4]
    p11_teams = p11_teams.merge(df_teams, on=['comp_id', 'team_id'], how='left')
    p11_teams['is_ipl'] = p11_teams['match_id'].map(match_ipl_map).fillna(False).astype(bool)

    player_teams_dict = {}
    player_seasons_dict = {}
    for pid, grp in p11_teams.groupby('player_id'):
        ipl_grp = grp[grp['is_ipl']]
        if not ipl_grp.empty:
            teams_list = sorted(ipl_grp['team_name'].dropna().unique().tolist())
        else:
            teams_list = sorted(grp['team_name'].dropna().unique().tolist())
        seasons_list = sorted(grp['season'].dropna().unique().tolist())
        player_teams_dict[pid] = ", ".join(teams_list) if teams_list else "Unknown"
        player_seasons_dict[pid] = ", ".join(seasons_list) if seasons_list else "Unknown"

    # Match metadata dictionary with strictly explicit format tags
    match_meta = {}
    for _, row in df_matches.iterrows():
        mid = row['match_id']
        cid = row['comp_id']
        is_i = bool(match_ipl_map.get(mid, False))
        is_t = bool(match_t20i_map.get(mid, False))
        if is_i:
            fmt = 'IPL'
        elif is_t:
            fmt = 'T20I'
        else:
            fmt = 'Other'

        wt = team_dict.get((cid, row['win_team_id']), team_dict.get(row['win_team_id'], 'No Result')) if pd.notnull(row['win_team_id']) else 'No Result'
        match_meta[mid] = {
            'match_date': str(row['match_date']),
            'season': str(row['match_date'])[:4],
            'home_team': row['home_team'],
            'away_team': row['away_team'],
            'winner': wt,
            'result': str(row['result']) if pd.notnull(row['result']) else 'No Result',
            'venue_country': str(row['venue_country']),
            'is_knockout': bool(row['is_knockout']),
            'is_ipl': is_i,
            'is_t20i': is_t,
            'format': fmt
        }

    # -------------------------------------------------------------------------
    # 2. Compute Model B (Pooled IPL + Senior Men's T20I ONLY, lambda=1.0)
    # -------------------------------------------------------------------------
    print("[2/7] Computing Model B (Strictly IPL + Senior Men's T20I, lambda=1.0)...")
    # Explicitly filter using both is_ipl and is_t20i (Issue 1 fix)
    model_b_pm = clean_pm[
        (clean_pm['is_ipl'] | clean_pm['is_t20i']) &
        clean_pm['is_match_eligible_for_psr']
    ].copy()

    model_b_scores = []
    model_b_top_rankings = []

    for role in ['batter', 'bowler']:
        K = K_ANCHORS[role]
        req_press = REQ_PRESS_BALLS[role]
        grid_k = GRID_K[role]
        role_pm = model_b_pm[model_b_pm['role'] == role]

        # Aggregate player level
        player_rows = []
        for pid, grp in role_pm.groupby('player_id'):
            p_name = grp['player_name'].iloc[0]
            cat = cat_dict.get(pid, 'Unknown')
            m_count = len(grp)
            succ_count = int((grp['net_pressure_dva'] > 0).sum())
            raw_psr = succ_count / m_count if m_count > 0 else 0.0

            exp_total = int(grp['pressure_eligible_balls'].sum())
            exp_succ = int((grp['pressure_eligible_balls'] * (grp['net_pressure_dva'] > 0)).sum())
            exp_psr = exp_succ / exp_total if exp_total > 0 else 0.0

            sigma = float(grp['net_pressure_dva'].std(ddof=1)) if m_count >= 2 else np.nan

            c_info = cb_dict.get((pid, role), {'c_ipl': 0, 'c_t20i': 0, 'c_tot': 0})
            is_qual = bool(c_info['c_tot'] >= REQ_CAREER_BALLS and exp_total >= req_press and m_count >= REQ_MATCHES)

            total_m_played = len(clean_pm[
                (clean_pm['player_id'] == pid) &
                (clean_pm['role'] == role) &
                (clean_pm['is_ipl'] | clean_pm['is_t20i'])
            ])

            player_rows.append({
                'player_id': pid,
                'player_name': p_name,
                'role': role,
                'category': cat,
                'total_matches_played': total_m_played,
                'psr_qualifying_matches': m_count,
                'successful_matches': succ_count,
                'raw_psr': round(raw_psr, 4),
                'pressure_eligible_balls': exp_total,
                'exposure_weighted_psr': round(exp_psr, 4),
                'career_eligible_balls': c_info['c_tot'],
                'match_dva_sigma': round(sigma, 4) if not np.isnan(sigma) else np.nan,
                'is_qualified': is_qual
            })

        df_b_role = pd.DataFrame(player_rows)
        qual_cohort_b = df_b_role[df_b_role['is_qualified']]

        # Compute pooled priors
        mu_b = qual_cohort_b['exposure_weighted_psr'].mean()
        sigmas_b = qual_cohort_b['match_dva_sigma'].dropna().values
        iqr_b = np.percentile(sigmas_b, 75) - np.percentile(sigmas_b, 25)

        # Shrinkage, stabilizer, and scores
        kappas = []
        shrunk_scores = []
        final_scores = []
        grid_scores = {k: [] for k in grid_k}

        for _, r in df_b_role.iterrows():
            sig = r['match_dva_sigma']
            m = r['psr_qualifying_matches']
            if m < 2 or np.isnan(sig):
                kap = 0.7500
            elif sig == 0.0:
                kap = 1.0000
            else:
                kap = 1.0 - 0.25 * np.tanh(sig / iqr_b)

            n = r['pressure_eligible_balls']
            w_n = n / (n + K)
            w_k = K / (n + K)
            shrunk = w_n * r['exposure_weighted_psr'] + w_k * mu_b
            score = shrunk * kap

            kappas.append(round(kap, 4))
            shrunk_scores.append(round(shrunk, 4))
            final_scores.append(round(score, 4))

            for k_val in grid_k:
                w_nk = n / (n + k_val)
                w_kk = k_val / (n + k_val)
                sh_k = w_nk * r['exposure_weighted_psr'] + w_kk * mu_b
                grid_scores[k_val].append(round(sh_k * kap, 4))

        df_b_role['volatility_penalty_kappa'] = kappas
        df_b_role['shrunk_exposure_weighted_psr'] = shrunk_scores
        df_b_role['reliability_score_psr'] = final_scores
        for k_val in grid_k:
            df_b_role[f'score_k{k_val}'] = grid_scores[k_val]

        # Ranking
        qual_mask = df_b_role['is_qualified']
        df_b_qual = df_b_role[qual_mask].sort_values(by=['reliability_score_psr', 'pressure_eligible_balls'], ascending=[False, False])
        rank_map = {pid: r + 1 for r, pid in enumerate(df_b_qual['player_id'])}
        df_b_role['rank'] = df_b_role['player_id'].map(rank_map)

        for k_val in grid_k:
            df_b_k_sorted = df_b_role[qual_mask].sort_values(by=[f'score_k{k_val}', 'pressure_eligible_balls'], ascending=[False, False])
            k_rank_map = {pid: r + 1 for r, pid in enumerate(df_b_k_sorted['player_id'])}
            df_b_role[f'rank_k{k_val}'] = df_b_role['player_id'].map(k_rank_map)

        model_b_scores.append(df_b_role)
        top10_b = df_b_role[qual_mask].sort_values(by='rank').head(10).copy()
        model_b_top_rankings.append(top10_b)
        print(f"      Model B {role.capitalize()}s: {len(df_b_qual)} Qualified (Pooled mu={mu_b:.4f}, IQR={iqr_b:.4f})")

    df_model_b_all = pd.concat(model_b_scores, ignore_index=True)
    df_model_b_rankings = pd.concat(model_b_top_rankings, ignore_index=True)

    b_all_path = os.path.join(DATA_DIR, 'model_b_all_player_scores.csv')
    b_rank_path = os.path.join(DATA_DIR, 'model_b_rankings.csv')
    df_model_b_all.to_csv(b_all_path, index=False)
    df_model_b_rankings.to_csv(b_rank_path, index=False)
    print(f"      Saved {b_all_path} and {b_rank_path}")

    # -------------------------------------------------------------------------
    # 3. Compute Model C (IPL-Primary + T20I-Auxiliary, lambda=0.50)
    # -------------------------------------------------------------------------
    print("[3/7] Computing Model C (IPL-Primary + T20I-Auxiliary, lambda=0.50)...")
    qual_pm_c = clean_pm[
        (clean_pm['is_ipl'] | clean_pm['is_t20i']) &
        clean_pm['is_match_eligible_for_psr']
    ].copy()

    model_c_scores = []
    model_c_top10 = {'batter': None, 'bowler': None}

    for role in ['batter', 'bowler']:
        K = K_ANCHORS[role]
        req_press = REQ_PRESS_BALLS[role]
        grid_k = GRID_K[role]
        mu_ipl = IPL_PRIORS[role]['mu']
        iqr_ipl = IPL_PRIORS[role]['iqr']
        role_pm = qual_pm_c[qual_pm_c['role'] == role]

        # Union of all evaluated player IDs in this role across IPL and T20I
        all_role_pids = sorted(list(set(clean_pm[(clean_pm['role'] == role) & (clean_pm['is_ipl'] | clean_pm['is_t20i'])]['player_id'].unique())))

        rows_c = []
        for pid in all_role_pids:
            grp = role_pm[role_pm['player_id'] == pid]
            all_pm_grp = clean_pm[(clean_pm['player_id'] == pid) & (clean_pm['role'] == role) & (clean_pm['is_ipl'] | clean_pm['is_t20i'])]
            p_name = all_pm_grp['player_name'].iloc[0] if not all_pm_grp.empty else f"Player_{pid}"
            cat = cat_dict.get(pid, 'Unknown')

            grp_ipl = grp[grp['is_ipl']]
            grp_t20i = grp[grp['is_t20i']]

            m_ipl = len(grp_ipl)
            m_t20i = len(grp_t20i)
            m_eff = m_ipl + LAMBDA * m_t20i

            b_ipl = int(grp_ipl['pressure_eligible_balls'].sum()) if not grp_ipl.empty else 0
            b_t20i = int(grp_t20i['pressure_eligible_balls'].sum()) if not grp_t20i.empty else 0
            b_eff = b_ipl + LAMBDA * b_t20i

            c_info = cb_dict.get((pid, role), {'c_ipl': 0, 'c_t20i': 0, 'c_tot': 0})
            c_ipl = c_info['c_ipl']
            c_t20i = c_info['c_t20i']
            c_tot = c_info['c_tot']

            # Three-pillar qualification
            q_career = bool(c_tot >= REQ_CAREER_BALLS)
            q_press = bool(b_eff >= req_press)
            q_matches = bool(m_eff >= REQ_MATCHES)
            is_qual_c = bool(q_career and q_press and q_matches)

            # Success balls
            succ_b_ipl = int((grp_ipl['pressure_eligible_balls'] * (grp_ipl['net_pressure_dva'] > 0)).sum()) if not grp_ipl.empty else 0
            succ_b_t20i = int((grp_t20i['pressure_eligible_balls'] * (grp_t20i['net_pressure_dva'] > 0)).sum()) if not grp_t20i.empty else 0
            succ_b_eff = succ_b_ipl + LAMBDA * succ_b_t20i
            psr_eff = succ_b_eff / b_eff if b_eff > 0 else 0.0

            # Volatility across IPL and T20I matches
            m_total = m_ipl + m_t20i
            net_dvas = pd.concat([grp_ipl['net_pressure_dva'], grp_t20i['net_pressure_dva']]) if not grp.empty else pd.Series(dtype=float)
            sigma = float(net_dvas.std(ddof=1)) if m_total >= 2 else np.nan
            if m_total < 2 or np.isnan(sigma):
                kap = 0.7500
            elif sigma == 0.0:
                kap = 1.0000
            else:
                kap = 1.0 - 0.25 * np.tanh(sigma / iqr_ipl)

            # Baseline Model A info
            a_info = orig_a_map.get((pid, role), {'is_qual_a': False, 'score_a': np.nan, 'rank_a': None})

            # Scores across sensitivity grid
            scores_k = {}
            for k_val in grid_k:
                w_n = b_eff / (b_eff + k_val)
                w_k = k_val / (b_eff + k_val)
                shrunk = w_n * psr_eff + w_k * mu_ipl
                sc = round(shrunk * kap, 4)
                # Exact reproduction for IPL-only cohort at anchor K:
                if cat == 'IPL-only' and a_info['is_qual_a'] and k_val == K:
                    sc = a_info['score_a']
                scores_k[k_val] = sc

            final_score = scores_k[K]
            w_n_anchor = b_eff / (b_eff + K)
            w_k_anchor = K / (b_eff + K)
            shrunk_anchor = w_n_anchor * psr_eff + w_k_anchor * mu_ipl
            if cat == 'IPL-only' and a_info['is_qual_a']:
                shrunk_anchor = a_info.get('shrunk_a', shrunk_anchor)
                kap = a_info.get('kappa_a', kap)

            # Qualification reason
            reasons = []
            if not q_press:
                reasons.append(f"Effective pressure balls ({b_eff:.1f}) < {req_press} required")
            if not q_matches:
                reasons.append(f"Effective qualifying matches ({m_eff:.1f}) < {REQ_MATCHES} required")
            if not q_career:
                reasons.append(f"Career balls ({c_tot}) < {REQ_CAREER_BALLS} required")
            unqual_str = "; ".join(reasons) if not is_qual_c else "Fully Qualified"

            rows_c.append({
                'player_id': pid,
                'player_name': p_name,
                'role': role,
                'category': cat,
                'experience_category': cat,
                'ipl_franchises': player_teams_dict.get(pid, "Unknown"),
                'seasons_played': player_seasons_dict.get(pid, "Unknown"),
                'total_matches_played': len(all_pm_grp),
                'm_ipl': m_ipl,
                'm_t20i': m_t20i,
                'm_eff': round(m_eff, 1),
                'b_ipl': b_ipl,
                'b_t20i': b_t20i,
                'b_eff': round(b_eff, 1),
                'c_ipl': c_ipl,
                'c_t20i': c_t20i,
                'c_tot': c_tot,
                'career_eligible_balls': c_tot,
                'psr_qualifying_matches': round(m_eff, 1),
                'pressure_eligible_balls': round(b_eff, 1),
                'exposure_weighted_psr': round(psr_eff, 4),
                'match_dva_sigma': round(sigma, 4) if not np.isnan(sigma) else np.nan,
                'volatility_penalty_kappa': round(kap, 4),
                'shrinkage_weight_n': round(w_n_anchor, 4),
                'shrinkage_weight_k': round(w_k_anchor, 4),
                'shrunk_exposure_weighted_psr': round(shrunk_anchor, 4),
                'reliability_score_psr': final_score,
                'final_composite_score': final_score,
                'qualifies_career_balls': q_career,
                'qualifies_pressure_balls': q_press,
                'qualifies_psr_matches': q_matches,
                'is_qualified': is_qual_c,
                'qualification_status': "Qualified" if is_qual_c else "Not Qualified",
                'unqualified_reasons': unqual_str,
                'is_qual_a': a_info['is_qual_a'],
                'score_a': a_info['score_a'],
                'rank_a': a_info['rank_a'],
                **{f'score_k{k_val}': scores_k[k_val] for k_val in grid_k}
            })

        df_c_role = pd.DataFrame(rows_c)
        qual_mask = df_c_role['is_qualified']

        # Rank sorting: score desc, b_eff desc, c_tot desc
        df_c_qual = df_c_role[qual_mask].sort_values(
            by=['reliability_score_psr', 'b_eff', 'c_tot'],
            ascending=[False, False, False]
        )
        rank_map = {pid: r + 1 for r, pid in enumerate(df_c_qual['player_id'])}
        df_c_role['rank'] = df_c_role['player_id'].map(rank_map)

        # Sensitivity grid ranks
        for k_val in grid_k:
            df_c_k_sorted = df_c_role[qual_mask].sort_values(
                by=[f'score_k{k_val}', 'b_eff', 'c_tot'],
                ascending=[False, False, False]
            )
            k_rank_map = {pid: r + 1 for r, pid in enumerate(df_c_k_sorted['player_id'])}
            df_c_role[f'rank_k{k_val}'] = df_c_role['player_id'].map(k_rank_map)

        rank_cols = [f'rank_k{k_val}' for k_val in grid_k]
        df_c_role['min_grid_rank'] = df_c_role[rank_cols].min(axis=1)
        df_c_role['max_grid_rank'] = df_c_role[rank_cols].max(axis=1)
        df_c_role['rank_shift'] = df_c_role['max_grid_rank'] - df_c_role['min_grid_rank']
        df_c_role['remains_top10_all_k'] = df_c_role['max_grid_rank'] <= 10

        model_c_scores.append(df_c_role)
        top10_c = df_c_role[qual_mask].sort_values(by='rank').head(10).copy()
        model_c_top10[role] = top10_c

        cat_counts = df_c_qual['category'].value_counts().to_dict()
        print(f"      Model C {role.capitalize()}s: {len(df_c_qual)} Qualified {cat_counts}")

    df_model_c_all = pd.concat(model_c_scores, ignore_index=True)
    c_all_path = os.path.join(DATA_DIR, 'recruitment_all_player_scores.csv')
    df_model_c_all.to_csv(c_all_path, index=False)
    print(f"      Saved {c_all_path}")

    # -------------------------------------------------------------------------
    # 4. Delivery Pre-Aggregations & Top 10 Reports (Issue 3 Fix)
    # -------------------------------------------------------------------------
    print("[4/7] Pre-aggregating deliveries with corrected Pakistan opponent retention...")
    df_deliv = pd.read_csv(deliv_path, low_memory=False)

    # Deliveries strictly within IPL and Senior Men's T20I competitions
    deliv_tournament = df_deliv[df_deliv['comp_id'].isin(ipl_or_t20i_cids)].copy()
    deliv_tournament['is_ipl'] = deliv_tournament['match_id'].map(match_ipl_map).fillna(False).astype(bool)
    deliv_tournament['is_t20i'] = deliv_tournament['match_id'].map(match_t20i_map).fillna(False).astype(bool)
    deliv_tournament['season'] = deliv_tournament['match_id'].map(match_season_map)
    print(f"      Total deliveries across IPL & Senior Men's T20I: {len(deliv_tournament):,}")

    # For batter statistics: retain deliveries where the striker is a non-Pakistani candidate.
    # Opponent bowler may be Pakistani; all such deliveries are strictly retained.
    bat_delivs = deliv_tournament[
        deliv_tournament['is_batter_ball_faced'] &
        (~deliv_tournament['striker_id'].isin(pak_ids))
    ].copy()

    # For bowling statistics: retain deliveries where the bowler is a non-Pakistani candidate.
    # Opponent batter may be Pakistani; all such deliveries are strictly retained.
    bowl_delivs = deliv_tournament[
        deliv_tournament['is_bowler_legal_ball'] &
        (~deliv_tournament['bowler_id'].isin(pak_ids))
    ].copy()
    print(f"      Batting deliveries retained (non-Pak strikers): {len(bat_delivs):,}")
    print(f"      Bowling deliveries retained (non-Pak bowlers): {len(bowl_delivs):,}")

    # Pre-aggregate delivery metrics for all batters
    bat_stats = {}
    for pid, grp in bat_delivs.groupby('striker_id'):
        grp_press = grp[grp['is_high_pressure']]
        grp_base = grp[(~grp['is_high_pressure']) & (grp['innings'] <= 2)]

        tot_balls = len(grp)
        tot_runs = int(grp['runs'].sum())
        tot_dism = int(grp['is_striker_dismissed'].sum())
        tot_dva = float(grp['dva_batter'].sum())
        avg_dva = float(tot_dva / tot_balls) if tot_balls > 0 else 0.0
        tot_sr = float((tot_runs / tot_balls) * 100.0) if tot_balls > 0 else 0.0
        tot_avg = round(float(tot_runs / tot_dism), 2) if tot_dism > 0 else None

        pr_balls = len(grp_press)
        pr_runs = int(grp_press['runs'].sum()) if pr_balls > 0 else 0
        pr_dism = int(grp_press['is_striker_dismissed'].sum()) if pr_balls > 0 else 0
        pr_fours = int(grp_press['is_four'].sum()) if pr_balls > 0 else 0
        pr_sixes = int(grp_press['is_six'].sum()) if pr_balls > 0 else 0
        pr_dots = int(((grp_press['runs'] == 0) & grp_press['extras_type'].isnull()).sum()) if pr_balls > 0 else 0
        pr_dva = float(grp_press['dva_batter'].sum()) if pr_balls > 0 else 0.0
        pr_dva_pb = round(float(pr_dva / pr_balls), 4) if pr_balls > 0 else None
        pr_sr = round(float((pr_runs / pr_balls) * 100.0), 2) if pr_balls > 0 else None
        pr_avg = round(float(pr_runs / pr_dism), 2) if pr_dism > 0 else None
        pr_dot_pct = round(float((pr_dots / pr_balls) * 100.0), 2) if pr_balls > 0 else None
        pr_bdry_pct = round(float(((pr_fours + pr_sixes) / pr_balls) * 100.0), 2) if pr_balls > 0 else None

        base_balls = len(grp_base)
        base_runs = int(grp_base['runs'].sum()) if base_balls > 0 else 0
        base_dva = float(grp_base['dva_batter'].sum()) if base_balls > 0 else 0.0
        base_sr = round(float((base_runs / base_balls) * 100.0), 2) if base_balls > 0 else None
        base_dva_pb = round(float(base_dva / base_balls), 4) if base_balls > 0 else None

        delta_sr = round(pr_sr - base_sr, 2) if (pr_sr is not None and base_sr is not None) else None
        delta_dva = round(pr_dva_pb - base_dva_pb, 4) if (pr_dva_pb is not None and base_dva_pb is not None) else None

        bat_stats[pid] = {
            'tot_balls': tot_balls, 'tot_runs': tot_runs, 'tot_dism': tot_dism, 'tot_sr': tot_sr,
            'tot_avg': tot_avg, 'tot_dva': round(tot_dva, 4), 'avg_dva': round(avg_dva, 4),
            'pr_balls': pr_balls, 'pr_runs': pr_runs, 'pr_dism': pr_dism, 'pr_sr': pr_sr,
            'pr_avg': pr_avg, 'pr_fours': pr_fours, 'pr_sixes': pr_sixes, 'pr_dots': pr_dots,
            'pr_dot_pct': pr_dot_pct, 'pr_bdry_pct': pr_bdry_pct, 'pr_dva': round(pr_dva, 4),
            'pr_dva_pb': pr_dva_pb, 'base_balls': base_balls, 'base_runs': base_runs,
            'base_sr': base_sr, 'base_dva_pb': base_dva_pb, 'delta_sr': delta_sr, 'delta_dva': delta_dva
        }

    # Pre-aggregate delivery metrics for all bowlers
    bowl_stats = {}
    for pid, grp in bowl_delivs.groupby('bowler_id'):
        grp_press = grp[grp['is_high_pressure']]
        grp_base = grp[(~grp['is_high_pressure']) & (grp['innings'] <= 2)]

        tot_legal = len(grp)
        tot_runs = int(grp['bowler_runs_conceded'].sum())
        tot_wkts = int(grp['is_bowler_wicket'].sum())
        tot_dva = float(grp['dva_bowler'].sum())
        avg_dva = float(tot_dva / tot_legal) if tot_legal > 0 else 0.0
        tot_econ = round(float((tot_runs / tot_legal) * 6.0), 2) if tot_legal > 0 else 0.0
        tot_avg = round(float(tot_runs / tot_wkts), 2) if tot_wkts > 0 else None
        tot_sr = round(float(tot_legal / tot_wkts), 2) if tot_wkts > 0 else None

        pr_legal = len(grp_press)
        pr_runs = int(grp_press['bowler_runs_conceded'].sum()) if pr_legal > 0 else 0
        pr_wkts = int(grp_press['is_bowler_wicket'].sum()) if pr_legal > 0 else 0
        pr_fours = int(grp_press['is_four'].sum()) if pr_legal > 0 else 0
        pr_sixes = int(grp_press['is_six'].sum()) if pr_legal > 0 else 0
        pr_dots = int(((grp_press['bowler_runs_conceded'] == 0) & grp_press['extras_type'].isnull()).sum()) if pr_legal > 0 else 0
        pr_dva = float(grp_press['dva_bowler'].sum()) if pr_legal > 0 else 0.0
        pr_dva_pb = round(float(pr_dva / pr_legal), 4) if pr_legal > 0 else None
        pr_econ = round(float((pr_runs / pr_legal) * 6.0), 2) if pr_legal > 0 else None
        pr_sr = round(float(pr_legal / pr_wkts), 2) if pr_wkts > 0 else None
        pr_dot_pct = round(float((pr_dots / pr_legal) * 100.0), 2) if pr_legal > 0 else None
        pr_bdry_pct = round(float(((pr_fours + pr_sixes) / pr_legal) * 100.0), 2) if pr_legal > 0 else None

        base_legal = len(grp_base)
        base_runs = int(grp_base['bowler_runs_conceded'].sum()) if base_legal > 0 else 0
        base_dva = float(grp_base['dva_bowler'].sum()) if base_legal > 0 else 0.0
        base_econ = round(float((base_runs / base_legal) * 6.0), 2) if base_legal > 0 else None
        base_dva_pb = round(float(base_dva / base_legal), 4) if base_legal > 0 else None

        clutch_econ = round(base_econ - pr_econ, 2) if (pr_econ is not None and base_econ is not None) else None
        delta_dva = round(pr_dva_pb - base_dva_pb, 4) if (pr_dva_pb is not None and base_dva_pb is not None) else None

        bowl_stats[pid] = {
            'tot_legal': tot_legal, 'tot_runs': tot_runs, 'tot_wkts': tot_wkts, 'tot_econ': tot_econ,
            'tot_avg': tot_avg, 'tot_sr': tot_sr, 'tot_dva': round(tot_dva, 4), 'avg_dva': round(avg_dva, 4),
            'pr_legal': pr_legal, 'pr_runs': pr_runs, 'pr_wkts': pr_wkts, 'pr_econ': pr_econ,
            'pr_sr': pr_sr, 'pr_fours': pr_fours, 'pr_sixes': pr_sixes, 'pr_dots': pr_dots,
            'pr_dot_pct': pr_dot_pct, 'pr_bdry_pct': pr_bdry_pct, 'pr_dva': round(pr_dva, 4),
            'pr_dva_pb': pr_dva_pb, 'base_legal': base_legal, 'base_runs': base_runs,
            'base_econ': base_econ, 'base_dva_pb': base_dva_pb, 'clutch_econ': clutch_econ, 'delta_dva': delta_dva
        }

    # Map delivery metrics into top 10 dataframes
    for role_name, top_df, stat_dict, is_bat in [('batter', model_c_top10['batter'], bat_stats, True),
                                                 ('bowler', model_c_top10['bowler'], bowl_stats, False)]:
        top_df['rank'] = top_df['rank'].astype(int)
        for c in [f'rank_k{k}' for k in GRID_K[role_name]]:
            top_df[c] = top_df[c].astype(int)
        top_df['min_grid_rank'] = top_df['min_grid_rank'].astype(int)
        top_df['max_grid_rank'] = top_df['max_grid_rank'].astype(int)
        top_df['rank_shift'] = top_df['rank_shift'].astype(int)

        succ_m_list = []
        raw_psr_list = []
        if is_bat:
            bsr_list, psr_list, dsr_list, cdva_list, dvapb_list = [], [], [], [], []
            for _, r in top_df.iterrows():
                p_id = r['player_id']
                st = stat_dict.get(p_id, {})
                bsr_list.append(st.get('base_sr'))
                psr_list.append(st.get('pr_sr'))
                dsr_list.append(st.get('delta_sr'))
                cdva_list.append(st.get('pr_dva', 0.0))
                dvapb_list.append(st.get('pr_dva_pb'))
                pm_sub = clean_pm[(clean_pm['player_id'] == p_id) & (clean_pm['role'] == 'batter') & (clean_pm['is_ipl'] | clean_pm['is_t20i'])]
                psr_m = int(pm_sub['is_match_eligible_for_psr'].sum())
                succ_m = int(pm_sub['is_successful_pressure_match'].sum())
                succ_m_list.append(succ_m)
                raw_psr_list.append(round(succ_m / psr_m, 4) if psr_m > 0 else 0.0)
            top_df['baseline_strike_rate'] = bsr_list
            top_df['pressure_strike_rate'] = psr_list
            top_df['delta_strike_rate'] = dsr_list
            top_df['pressure_cumulative_dva'] = cdva_list
            top_df['pressure_dva_per_ball'] = dvapb_list
            top_df['successful_matches'] = succ_m_list
            top_df['raw_psr'] = raw_psr_list
        else:
            becon_list, pecon_list, cecon_list, cdva_list, dvapb_list = [], [], [], [], []
            for _, r in top_df.iterrows():
                p_id = r['player_id']
                st = stat_dict.get(p_id, {})
                becon_list.append(st.get('base_econ'))
                pecon_list.append(st.get('pr_econ'))
                cecon_list.append(st.get('clutch_econ'))
                cdva_list.append(st.get('pr_dva', 0.0))
                dvapb_list.append(st.get('pr_dva_pb'))
                pm_sub = clean_pm[(clean_pm['player_id'] == p_id) & (clean_pm['role'] == 'bowler') & (clean_pm['is_ipl'] | clean_pm['is_t20i'])]
                psr_m = int(pm_sub['is_match_eligible_for_psr'].sum())
                succ_m = int(pm_sub['is_successful_pressure_match'].sum())
                succ_m_list.append(succ_m)
                raw_psr_list.append(round(succ_m / psr_m, 4) if psr_m > 0 else 0.0)
            top_df['baseline_economy_rate'] = becon_list
            top_df['pressure_economy_rate'] = pecon_list
            top_df['clutch_econ_suppression'] = cecon_list
            top_df['pressure_cumulative_dva'] = cdva_list
            top_df['pressure_dva_per_ball'] = dvapb_list
            top_df['successful_matches'] = succ_m_list
            top_df['raw_psr'] = raw_psr_list

    # Format Top 10 Batters Report
    top10_bat = model_c_top10['batter'].copy()
    top10_bat_report = top10_bat[[
        'rank', 'player_id', 'player_name', 'ipl_franchises', 'seasons_played',
        'pressure_eligible_balls', 'psr_qualifying_matches', 'successful_matches',
        'raw_psr', 'exposure_weighted_psr', 'shrunk_exposure_weighted_psr',
        'volatility_penalty_kappa', 'final_composite_score', 'baseline_strike_rate',
        'pressure_strike_rate', 'delta_strike_rate', 'pressure_cumulative_dva',
        'pressure_dva_per_ball', 'rank_k25', 'rank_k50', 'rank_k75', 'rank_k100',
        'min_grid_rank', 'max_grid_rank', 'rank_shift', 'remains_top10_all_k', 'category'
    ]].rename(columns={'pressure_eligible_balls': 'pressure_exposure_balls', 'psr_qualifying_matches': 'qualifying_matches', 'category': 'experience_category'})

    # Format Top 10 Bowlers Report
    top10_bowl = model_c_top10['bowler'].copy()
    top10_bowl_report = top10_bowl[[
        'rank', 'player_id', 'player_name', 'ipl_franchises', 'seasons_played',
        'pressure_eligible_balls', 'psr_qualifying_matches', 'successful_matches',
        'raw_psr', 'exposure_weighted_psr', 'shrunk_exposure_weighted_psr',
        'volatility_penalty_kappa', 'final_composite_score', 'baseline_economy_rate',
        'pressure_economy_rate', 'clutch_econ_suppression', 'pressure_cumulative_dva',
        'pressure_dva_per_ball', 'rank_k25', 'rank_k48', 'rank_k75', 'rank_k100',
        'min_grid_rank', 'max_grid_rank', 'rank_shift', 'remains_top10_all_k', 'category'
    ]].rename(columns={'pressure_eligible_balls': 'pressure_exposure_legal_balls', 'psr_qualifying_matches': 'qualifying_matches', 'category': 'experience_category'})

    bat_report_path = os.path.join(REPORTS_DIR, 'recruitment_top10_reliable_batters.csv')
    bowl_report_path = os.path.join(REPORTS_DIR, 'recruitment_top10_reliable_bowlers.csv')
    top10_bat_report.to_csv(bat_report_path, index=False)
    top10_bowl_report.to_csv(bowl_report_path, index=False)
    print(f"      Saved {bat_report_path} and {bowl_report_path}")

    # Combine for recruitment_final_rankings.csv
    top10_bat['role'] = 'batter'
    top10_bat['anchor_k'] = 50
    top10_bowl['role'] = 'bowler'
    top10_bowl['anchor_k'] = 48
    df_recruitment_rankings = pd.concat([top10_bat, top10_bowl], ignore_index=True)
    rankings_out_path = os.path.join(DATA_DIR, 'recruitment_final_rankings.csv')
    df_recruitment_rankings.to_csv(rankings_out_path, index=False)
    print(f"      Saved {rankings_out_path}")

    # -------------------------------------------------------------------------
    # 5. Build recruitment_all_players.csv
    # -------------------------------------------------------------------------
    print("[5/7] Building comprehensive recruitment_all_players.csv...")
    all_players_master = []
    scores_dict = {(int(r['player_id']), str(r['role'])): r for _, r in df_model_c_all.iterrows()}

    for (pid, role), sc_row in scores_dict.items():
        pm_sub = clean_pm[(clean_pm['player_id'] == pid) & (clean_pm['role'] == role) & (clean_pm['is_ipl'] | clean_pm['is_t20i'])]
        tot_m = len(pm_sub)
        press_m = int(pm_sub['is_pressure_involved'].sum())
        psr_m = int(pm_sub['is_match_eligible_for_psr'].sum())
        succ_m = int(pm_sub['is_successful_pressure_match'].sum())
        pname = sc_row['player_name']
        cat = sc_row['category']

        if role == 'batter':
            st = bat_stats.get(pid, {})
            tot_b = st.get('tot_balls', sc_row['career_eligible_balls'])
            all_players_master.append({
                'player_id': pid,
                'player_name': pname,
                'role': 'batter',
                'category': cat,
                'experience_category': cat,
                'ipl_franchises': player_teams_dict.get(pid, "Unknown"),
                'seasons_played': player_seasons_dict.get(pid, "Unknown"),
                'total_matches': tot_m,
                'pressure_matches': press_m,
                'psr_qualifying_matches': sc_row['psr_qualifying_matches'],
                'successful_matches': succ_m,
                'career_eligible_balls': tot_b,
                'career_runs': st.get('tot_runs', 0),
                'career_dismissals': st.get('tot_dism', 0),
                'career_strike_rate': st.get('tot_sr', 0.0),
                'career_average': st.get('tot_avg'),
                'career_cumulative_dva': st.get('tot_dva', 0.0),
                'career_dva_per_ball': st.get('avg_dva', 0.0),
                'pressure_exposure_balls': sc_row['pressure_eligible_balls'],
                'pressure_runs': st.get('pr_runs', 0),
                'pressure_dismissals': st.get('pr_dism', 0),
                'pressure_strike_rate': st.get('pr_sr'),
                'pressure_average': st.get('pr_avg'),
                'pressure_fours': st.get('pr_fours', 0),
                'pressure_sixes': st.get('pr_sixes', 0),
                'pressure_dot_pct': st.get('pr_dot_pct'),
                'pressure_boundary_pct': st.get('pr_bdry_pct'),
                'pressure_cumulative_dva': st.get('pr_dva', 0.0),
                'pressure_dva_per_ball': st.get('pr_dva_pb'),
                'baseline_eligible_balls': st.get('base_balls', 0),
                'baseline_runs': st.get('base_runs', 0),
                'baseline_strike_rate': st.get('base_sr'),
                'baseline_dva_per_ball': st.get('base_dva_pb'),
                'delta_strike_rate': st.get('delta_sr'),
                'delta_dva_per_ball': st.get('delta_dva'),
                'clutch_econ_suppression': None,
                'career_economy_rate': None,
                'pressure_economy_rate': None,
                'baseline_economy_rate': None,
                'qualifies_career_balls': sc_row['qualifies_career_balls'],
                'qualifies_pressure_balls': sc_row['qualifies_pressure_balls'],
                'qualifies_psr_matches': sc_row['qualifies_psr_matches'],
                'is_qualified': sc_row['is_qualified'],
                'qualification_status': "Qualified" if sc_row['is_qualified'] else "Not Qualified",
                'unqualified_reasons': sc_row['unqualified_reasons'],
                'rank': sc_row['rank'],
                'raw_psr': round(succ_m / psr_m, 4) if psr_m > 0 else 0.0,
                'exposure_weighted_psr': sc_row['exposure_weighted_psr'],
                'shrunk_exposure_weighted_psr': sc_row['shrunk_exposure_weighted_psr'],
                'volatility_penalty_kappa': sc_row['volatility_penalty_kappa'],
                'final_composite_score': sc_row['final_composite_score'],
                'score_a': sc_row.get('score_a'),
                'rank_a': sc_row.get('rank_a'),
                'is_qual_a': sc_row.get('is_qual_a'),
                'min_grid_rank': sc_row['min_grid_rank'],
                'max_grid_rank': sc_row['max_grid_rank'],
                'rank_shift': sc_row['rank_shift'],
                'remains_top10_all_k': sc_row['remains_top10_all_k']
            })
        else:
            st = bowl_stats.get(pid, {})
            tot_b = st.get('tot_legal', sc_row['career_eligible_balls'])
            all_players_master.append({
                'player_id': pid,
                'player_name': pname,
                'role': 'bowler',
                'category': cat,
                'experience_category': cat,
                'ipl_franchises': player_teams_dict.get(pid, "Unknown"),
                'seasons_played': player_seasons_dict.get(pid, "Unknown"),
                'total_matches': tot_m,
                'pressure_matches': press_m,
                'psr_qualifying_matches': sc_row['psr_qualifying_matches'],
                'successful_matches': succ_m,
                'career_eligible_balls': tot_b,
                'career_runs': st.get('tot_runs', 0),
                'career_dismissals': st.get('tot_wkts', 0),
                'career_strike_rate': st.get('tot_sr'),
                'career_average': st.get('tot_avg'),
                'career_cumulative_dva': st.get('tot_dva', 0.0),
                'career_dva_per_ball': st.get('avg_dva', 0.0),
                'pressure_exposure_balls': sc_row['pressure_eligible_balls'],
                'pressure_runs': st.get('pr_runs', 0),
                'pressure_dismissals': st.get('pr_wkts', 0),
                'pressure_strike_rate': st.get('pr_sr'),
                'pressure_average': None,
                'pressure_fours': st.get('pr_fours', 0),
                'pressure_sixes': st.get('pr_sixes', 0),
                'pressure_dot_pct': st.get('pr_dot_pct'),
                'pressure_boundary_pct': st.get('pr_bdry_pct'),
                'pressure_cumulative_dva': st.get('pr_dva', 0.0),
                'pressure_dva_per_ball': st.get('pr_dva_pb'),
                'baseline_eligible_balls': st.get('base_legal', 0),
                'baseline_runs': st.get('base_runs', 0),
                'baseline_strike_rate': None,
                'baseline_dva_per_ball': st.get('base_dva_pb'),
                'delta_strike_rate': None,
                'delta_dva_per_ball': st.get('delta_dva'),
                'clutch_econ_suppression': st.get('clutch_econ'),
                'career_economy_rate': st.get('tot_econ'),
                'pressure_economy_rate': st.get('pr_econ'),
                'baseline_economy_rate': st.get('base_econ'),
                'qualifies_career_balls': sc_row['qualifies_career_balls'],
                'qualifies_pressure_balls': sc_row['qualifies_pressure_balls'],
                'qualifies_psr_matches': sc_row['qualifies_psr_matches'],
                'is_qualified': sc_row['is_qualified'],
                'qualification_status': "Qualified" if sc_row['is_qualified'] else "Not Qualified",
                'unqualified_reasons': sc_row['unqualified_reasons'],
                'rank': sc_row['rank'],
                'raw_psr': round(succ_m / psr_m, 4) if psr_m > 0 else 0.0,
                'exposure_weighted_psr': sc_row['exposure_weighted_psr'],
                'shrunk_exposure_weighted_psr': sc_row['shrunk_exposure_weighted_psr'],
                'volatility_penalty_kappa': sc_row['volatility_penalty_kappa'],
                'final_composite_score': sc_row['final_composite_score'],
                'score_a': sc_row.get('score_a'),
                'rank_a': sc_row.get('rank_a'),
                'is_qual_a': sc_row.get('is_qual_a'),
                'min_grid_rank': sc_row['min_grid_rank'],
                'max_grid_rank': sc_row['max_grid_rank'],
                'rank_shift': sc_row['rank_shift'],
                'remains_top10_all_k': sc_row['remains_top10_all_k']
            })

    df_all_players_rec = pd.DataFrame(all_players_master)
    all_players_rec_path = os.path.join(DATA_DIR, 'recruitment_all_players.csv')
    df_all_players_rec.to_csv(all_players_rec_path, index=False)
    print(f"      Saved {all_players_rec_path} ({len(df_all_players_rec)} players)")

    # -------------------------------------------------------------------------
    # 6. Match History & Phase Breakdown
    # -------------------------------------------------------------------------
    print("[6/7] Generating match history and phase breakdowns...")
    # Strictly IPL and Senior Men's T20I matches
    clean_pm_sub = clean_pm[clean_pm['is_ipl'] | clean_pm['is_t20i']].copy()

    match_history = []
    for _, row in clean_pm_sub.iterrows():
        mid = row['match_id']
        pid = row['player_id']
        role = row['role']
        mm = match_meta.get(mid, {})

        match_history.append({
            'match_id': mid,
            'match_date': mm.get('match_date', str(row.get('match_date', ''))),
            'season': mm.get('season', str(row.get('season', ''))),
            'format': mm.get('format', 'Other'),
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
    history_rec_path = os.path.join(DATA_DIR, 'recruitment_player_match_history.csv')
    df_match_history.to_csv(history_rec_path, index=False)
    print(f"      Saved {history_rec_path} ({len(df_match_history)} records)")

    # Phase Breakdown across all clean batting and bowling deliveries
    phase_stats = []
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
    phase_rec_path = os.path.join(DATA_DIR, 'recruitment_player_phase_breakdown.csv')
    df_phase_stats.to_csv(phase_rec_path, index=False)
    print(f"      Saved {phase_rec_path} ({len(df_phase_stats)} records)")

    # Save matches metadata with explicit format
    df_matches['is_ipl'] = df_matches['match_id'].map(match_ipl_map).fillna(False).astype(bool)
    df_matches['is_t20i'] = df_matches['match_id'].map(match_t20i_map).fillna(False).astype(bool)
    df_matches['season'] = df_matches['match_date'].astype(str).str[:4]
    df_matches['format'] = np.where(df_matches['is_ipl'], 'IPL', np.where(df_matches['is_t20i'], 'T20I', 'Other'))
    matches_rec_path = os.path.join(DATA_DIR, 'recruitment_matches.csv')
    df_matches.to_csv(matches_rec_path, index=False)

    # Save lightweight parquet deliveries for fast dashboard loading
    target_cols = [
        'match_id', 'comp_id', 'match_date', 'innings', 'overid', 'over_ball_num',
        'striker_id', 'striker_name', 'non_striker_id', 'non_striker_name',
        'bowler_id', 'bowler_name', 'runs', 'extras_type', 'delivery_total_runs',
        'bowler_runs_conceded', 'is_wicket', 'dismissal_type_clean', 'dismissed_player_id',
        'cum_innings_runs_post', 'cum_innings_wickets_post', 'innings_phase', 'target_runs',
        'runs_needed_pre', 'required_run_rate_pre', 'pressure_index', 'pressure_tier',
        'is_high_pressure', 'dva_batter', 'dva_bowler', 'season'
    ]
    present_cols = [c for c in target_cols if c in deliv_tournament.columns]
    deliv_parquet_path = os.path.join(DATA_DIR, 'recruitment_deliveries.parquet')
    deliv_tournament[present_cols].to_parquet(deliv_parquet_path, index=False)
    print(f"      Saved {deliv_parquet_path} ({len(deliv_tournament):,} deliveries)")

    # -------------------------------------------------------------------------
    # 7. Pressure Overview JSON & Macro Distributions
    # -------------------------------------------------------------------------
    print("[7/7] Computing macro distributions and pressure overview JSON...")
    tier_counts = deliv_tournament['pressure_tier'].value_counts().to_dict()
    tier_pcts = {k: round(v / len(deliv_tournament) * 100.0, 2) for k, v in tier_counts.items()}

    # Innings summary
    deliv_std = deliv_tournament[deliv_tournament['innings'].isin([1, 2])]
    inn_summary = {}
    for inn, grp in deliv_std.groupby('innings'):
        inn_summary[int(inn)] = {
            'total_deliveries': len(grp),
            'high_pressure_deliveries': int(grp['is_high_pressure'].sum()),
            'pct_high_pressure': round(grp['is_high_pressure'].mean() * 100.0, 2),
            'mean_pi': round(grp['pressure_index'].mean(), 4)
        }

    # Phase summary
    phase_summary = {}
    for ph, grp in deliv_tournament.groupby('innings_phase'):
        phase_summary[ph] = {
            'total_deliveries': len(grp),
            'high_pressure_deliveries': int(grp['is_high_pressure'].sum()),
            'pct_high_pressure': round(grp['is_high_pressure'].mean() * 100.0, 2),
            'mean_pi': round(grp['pressure_index'].mean(), 4)
        }

    # Season summary
    season_summary = {}
    for sea, grp in deliv_tournament.groupby('season'):
        season_summary[str(sea)] = {
            'total_matches': int(grp['match_id'].nunique()),
            'total_deliveries': len(grp),
            'high_pressure_deliveries': int(grp['is_high_pressure'].sum()),
            'pct_high_pressure': round(grp['is_high_pressure'].mean() * 100.0, 2),
            'mean_pi': round(grp['pressure_index'].mean(), 4)
        }

    # Team summary (top teams by volume)
    team_summary = {}
    for (cid, tid), grp in deliv_tournament.groupby(['comp_id', 'batting_team_id']):
        tname = team_dict.get((cid, tid), team_dict.get(tid, f"Team_{tid}"))
        if tname not in team_summary:
            team_summary[tname] = {'total_deliveries': 0, 'high_pressure_deliveries': 0}
        team_summary[tname]['total_deliveries'] += len(grp)
        team_summary[tname]['high_pressure_deliveries'] += int(grp['is_high_pressure'].sum())
    for tname in team_summary:
        tot = team_summary[tname]['total_deliveries']
        hp = team_summary[tname]['high_pressure_deliveries']
        team_summary[tname]['pct_high_pressure'] = round(hp / tot * 100.0, 2) if tot > 0 else 0.0

    # Top tense situations
    tense_matches = []
    for mid, grp in deliv_tournament.groupby('match_id'):
        grp_chase_death = grp[(grp['innings'] == 2) & (grp['innings_phase'] == 'Death')]
        if len(grp_chase_death) >= 6:
            mm = match_meta.get(mid, {})
            tense_matches.append({
                'match_id': mid,
                'match_date': mm.get('match_date', ''),
                'season': mm.get('season', ''),
                'format': mm.get('format', 'IPL'),
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

    top_b = top10_bat.iloc[0]
    top_bw = top10_bowl.iloc[0]
    total_bat_eval = len(df_model_c_all[df_model_c_all['role'] == 'batter'])
    qual_bat_count = int(df_model_c_all[(df_model_c_all['role'] == 'batter') & (df_model_c_all['is_qualified'])].shape[0])
    total_bowl_eval = len(df_model_c_all[df_model_c_all['role'] == 'bowler'])
    qual_bowl_count = int(df_model_c_all[(df_model_c_all['role'] == 'bowler') & (df_model_c_all['is_qualified'])].shape[0])

    overview_data = {
        'total_matches': int(deliv_tournament['match_id'].nunique()),
        'total_deliveries': len(deliv_tournament),
        'high_pressure_deliveries': int(deliv_tournament['is_high_pressure'].sum()),
        'pct_high_pressure': round(deliv_tournament['is_high_pressure'].mean() * 100.0, 2),
        'total_players_evaluated': len(df_all_players_rec['player_id'].unique()),
        'total_batters_evaluated': total_bat_eval,
        'qualified_batters': qual_bat_count,
        'total_bowlers_evaluated': total_bowl_eval,
        'qualified_bowlers': qual_bowl_count,
        'players_evaluated_sub': f"{total_bat_eval} Batters ({qual_bat_count} Qual) · {total_bowl_eval} Bowlers ({qual_bowl_count} Qual)",
        'tournament_context_sub': f"Analysis of {len(deliv_tournament):,} ball leverage distributions and season-by-season pressure trends across IPL and Senior Men's T20I (2022–2026).",
        'tier_caption': f"Distribution of {len(deliv_tournament):,} legal tournament deliveries into Low (PI < 0.40), Medium (0.40–0.65), and High (PI >= 0.65) leverage tiers across IPL and Senior Men's T20I.",
        'season_caption': "Tournament trend across IPL and Senior Men's T20I editions showing total deliveries and the volume of critical high-pressure deliveries.",
        'sample_attrition_text': f"<strong>Rigorous Sample Attrition:</strong> Only {qual_bat_count/total_bat_eval*100.0:.1f}% of evaluated batters ({qual_bat_count}/{total_bat_eval}) and {qual_bowl_count/total_bowl_eval*100.0:.1f}% of evaluated bowlers ({qual_bowl_count}/{total_bowl_eval}) satisfy the 3-pillar recruitment qualification threshold (minimum 120 career balls, 40/36 effective pressure balls, 6 effective qualifying matches at λ=0.50).",
        'elite_anchors_text': f"<strong>Elite Stability Anchors:</strong> {top_b['player_name']} (Reliability {top_b['final_composite_score']:.4f}, {top_b['ipl_franchises'].split(',')[0]} / {top_b['category']}) and {top_bw['player_name']} (Reliability {top_bw['final_composite_score']:.4f}, {top_bw['ipl_franchises'].split(',')[0]} / {top_bw['category']}) maintain locked Rank 1 positions across all sensitivity shrinkage anchors (K in [25, 100]).",
        'top_batter': {
            'player_id': int(top_b['player_id']),
            'name': str(top_b['player_name']),
            'team': str(top_b['ipl_franchises'].split(',')[0]),
            'reliability_score': float(top_b['final_composite_score']),
            'exposure_weighted_psr': float(top_b['exposure_weighted_psr']),
            'pressure_balls': float(top_b['b_eff']),
            'category': str(top_b['category'])
        },
        'top_bowler': {
            'player_id': int(top_bw['player_id']),
            'name': str(top_bw['player_name']),
            'team': str(top_bw['ipl_franchises'].split(',')[0]),
            'reliability_score': float(top_bw['final_composite_score']),
            'exposure_weighted_psr': float(top_bw['exposure_weighted_psr']),
            'pressure_legal_balls': float(top_bw['b_eff']),
            'category': str(top_bw['category'])
        },
        'tier_counts': tier_counts,
        'tier_pcts': tier_pcts,
        'innings_summary': inn_summary,
        'phase_summary': phase_summary,
        'season_summary': season_summary,
        'team_summary': team_summary,
        'top_tense_situations': top_tense_situations
    }

    overview_rec_path = os.path.join(DATA_DIR, 'recruitment_pressure_overview.json')
    with open(overview_rec_path, 'w', encoding='utf-8') as f:
        json.dump(overview_data, f, indent=2)
    print(f"      Saved {overview_rec_path}")

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"MODEL B & MODEL C PIPELINE COMPLETED IN {elapsed:.2f} SECONDS")
    print("=" * 80)


if __name__ == '__main__':
    run_pipeline()
