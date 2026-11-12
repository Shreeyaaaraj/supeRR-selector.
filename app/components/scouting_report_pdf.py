"""
SupeRR Selector - Player Scouting Report PDF Generator
======================================================
Generates high-resolution, professional PDF scouting dossiers for any IPL player
(qualified or non-qualified) using the approved Phase 3A Version 2.2 methodology.

Palette:
- Navy: #1C1A2F (Headers, primary accents)
- Pink/Rose: #D58DB5, #F2DCE9 (Batting accents)
- Lavender/Purple: #7964B5, #E9E4FA (Bowling accents)
- Light gray table stripes: #FAF9FE
"""

import os
import datetime
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos


def _safe_str(val):
    """Sanitize strings to avoid fpdf latin-1 encoding issues."""
    if val is None or pd.isna(val):
        return "-"
    s = str(val)
    # Replace common unicode typographic characters with ASCII equivalents
    replacements = {
        '\u2014': '-',   # em-dash
        '\u2013': '-',   # en-dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '*',   # bullet
        '\u2265': '>=',  # greater or equal
        '\u2264': '<=',  # less or equal
        '\u00d7': 'x',   # multiplication
        '\u03ba': 'kappa', # kappa
        '\u03bc': 'mu',    # mu
        '\u03b8': 'theta'  # theta
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    # Encode to latin-1 compatible ascii
    return s.encode('latin-1', 'replace').decode('latin-1')


class ScoutingReportPDF(FPDF):
    def __init__(self, player_name, role):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.player_name = player_name
        self.role = role
        self.set_auto_page_break(auto=True, margin=15)
        
        # Load Arial font if available on Windows, else Helvetica
        font_path = "C:/Windows/Fonts/arial.ttf"
        font_bold = "C:/Windows/Fonts/arialbd.ttf"
        if os.path.exists(font_path) and os.path.exists(font_bold):
            self.add_font("Arial", "", font_path)
            self.add_font("Arial", "B", font_bold)
            self.main_font = "Arial"
        else:
            self.main_font = "Helvetica"

    def header(self):
        # Flagship Navy Header Banner
        self.set_fill_color(28, 26, 47)  # #1C1A2F
        self.rect(0, 0, 210, 26, style='F')
        
        # Accent line at bottom of header banner
        if self.role == 'batter':
            self.set_fill_color(213, 141, 181)  # #D58DB5 (Rose)
        else:
            self.set_fill_color(121, 100, 181)  # #7964B5 (Purple)
        self.rect(0, 25, 210, 1.5, style='F')
        
        # Title
        self.set_text_color(255, 255, 255)
        self.set_font(self.main_font, 'B', 14)
        self.set_xy(12, 5)
        self.cell(0, 7, text="SupeRR Selector - IPL Scouting Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Subtitle
        self.set_font(self.main_font, '', 8)
        self.set_text_color(220, 231, 250)
        self.set_xy(12, 14)
        self.cell(0, 5, text="Season 2: IPL Pressure & Performance Platform (2022-2026) | Approved Phase 3A v2.2", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font(self.main_font, '', 8)
        self.set_text_color(120, 117, 138)
        self.cell(0, 8, text=f"SupeRR Selector Confidential Scouting Intelligence | Page {self.page_no()}", align='C')


def generate_scouting_pdf(p_row, stats_data=None, phase_df=None, match_history_df=None, role='batter'):
    """Generate a 2-page executive scouting dossier as raw PDF bytes."""
    # Allow flexible calling: generate_scouting_pdf(p_row, phase_df, match_history_df, role)
    if isinstance(stats_data, pd.DataFrame):
        actual_match_history = phase_df
        actual_phase_df = stats_data
        actual_role = match_history_df if isinstance(match_history_df, str) else p_row.get('role', role)
        stats_data = None
        phase_df = actual_phase_df
        match_history_df = actual_match_history
        role = actual_role
    elif role == 'batter' and p_row.get('role') in ['batter', 'bowler']:
        role = p_row.get('role')

    is_bat = (role == 'batter')
    name = _safe_str(p_row['player_name'])
    teams = _safe_str(p_row.get('ipl_franchises', 'IPL Franchise'))
    seasons = _safe_str(p_row.get('seasons_played', '2022-2026'))
    pid = int(p_row['player_id'])
    is_qual = bool(p_row['is_qualified'])
    score_val = p_row.get('final_composite_score', None)
    rank_val = p_row.get('rank', None)
    
    if phase_df is None:
        phase_df = pd.DataFrame()
    if match_history_df is None:
        match_history_df = pd.DataFrame()
        
    if stats_data is None:
        if is_bat:
            stats_data = {
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
        else:
            press_overs = f"{int(p_row.get('pressure_exposure_balls', 0)) // 6}.{int(p_row.get('pressure_exposure_balls', 0)) % 6}"
            base_overs = f"{int(p_row.get('baseline_eligible_balls', 0)) // 6}.{int(p_row.get('baseline_eligible_balls', 0)) % 6}"
            stats_data = {
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
    
    pdf = ScoutingReportPDF(name, role)
    pdf.add_page()
    
    # --- SECTION 1: PLAYER PROFILE & QUALIFICATION ---
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(236, 234, 243)
    pdf.set_line_width(0.4)
    pdf.rect(12, 32, 186, 32, style='FD')
    
    # Left: Player Name & Teams
    pdf.set_xy(16, 35)
    pdf.set_font(pdf.main_font, 'B', 15)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(110, 7, text=name, new_x=XPos.RIGHT, new_y=YPos.TOP)
    
    # Right: ID & Generation Date
    gen_date = datetime.date.today().strftime("%d %b %Y")
    pdf.set_xy(125, 35)
    pdf.set_font(pdf.main_font, 'B', 9)
    pdf.set_text_color(121, 100, 181 if not is_bat else 192)
    pdf.cell(68, 6, text=f"Player ID: {pid} | Date: {gen_date}", align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_xy(16, 43)
    pdf.set_font(pdf.main_font, '', 9)
    pdf.set_text_color(94, 88, 115)
    pdf.cell(110, 5, text=f"Role: {role.capitalize()} | Franchise(s): {teams}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_xy(16, 49)
    pdf.cell(110, 5, text=f"IPL Coverage: Seasons {seasons} | Total Evaluated Matches: {int(p_row.get('total_matches', 0))}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Qualification Chip
    pdf.set_xy(16, 56)
    if is_qual:
        pdf.set_fill_color(232, 247, 238)  # #E8F7EE
        pdf.set_text_color(31, 122, 74)     # #1F7A4A
        pdf.set_font(pdf.main_font, 'B', 8.5)
        rank_str = f"Rank {int(rank_val)}" if pd.notnull(rank_val) else "Qualified"
        score_str = f"Reliability Score: {score_val:.4f}" if pd.notnull(score_val) else ""
        pdf.cell(178, 6, text=f"  STATUS: QUALIFIED  |  {rank_str}  |  {score_str} (Approved Phase 3A Anchor)", fill=True)
    else:
        pdf.set_fill_color(242, 220, 233)  # #F2DCE9
        pdf.set_text_color(140, 71, 110)   # #8C476E
        pdf.set_font(pdf.main_font, 'B', 8.5)
        reason = _safe_str(p_row.get('unqualified_reasons', 'Insufficient pressure sample volume'))
        pdf.cell(178, 6, text=f"  STATUS: NOT QUALIFIED  |  Reason: {reason}", fill=True)
        
    pdf.ln(14)
    
    # --- SECTION 2: KEY PERFORMANCE BENCHMARKS (4 CARDS) ---
    pdf.set_font(pdf.main_font, 'B', 10.5)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(0, 6, text="Key Empirical Performance Benchmarks (Baseline vs High Pressure PI >= 0.65)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    
    # 4 metrics cards
    card_w = 44.5
    card_h = 22
    y_cards = pdf.get_y()
    
    metrics_summary = []
    if is_bat:
        sr_p = f"{p_row['pressure_strike_rate']:.1f}" if pd.notnull(p_row.get('pressure_strike_rate')) else "N/A"
        sr_d = f"{p_row['delta_strike_rate']:+.1f}" if pd.notnull(p_row.get('delta_strike_rate')) else "-"
        metrics_summary = [
            ("PRESSURE STRIKE RATE", sr_p, f"Delta: {sr_d}"),
            ("PRESSURE EXPOSURE", f"{int(p_row.get('pressure_exposure_balls', 0)):,} Balls", f"{int(p_row.get('pressure_runs', 0)):,} Runs"),
            ("PRESSURE SUCCESS (PSR)", f"{p_row.get('raw_psr', 0.0)*100:.1f}%", f"{int(p_row.get('successful_matches', 0))}/{int(p_row.get('psr_qualifying_matches', 0))} matches"),
            ("NET PRESSURE DVA", f"{p_row.get('pressure_cumulative_dva', 0.0):+.1f} Runs", f"{p_row.get('pressure_dva_per_ball', 0.0):+.2f}/ball")
        ]
    else:
        ec_p = f"{p_row['pressure_economy_rate']:.2f}" if pd.notnull(p_row.get('pressure_economy_rate')) else "N/A"
        ec_d = f"{p_row['clutch_econ_suppression']:+.2f}" if pd.notnull(p_row.get('clutch_econ_suppression')) else "-"
        metrics_summary = [
            ("PRESSURE ECONOMY", ec_p, f"Suppression: {ec_d}"),
            ("PRESSURE LEGAL BALLS", f"{int(p_row.get('pressure_exposure_balls', 0)):,} Balls", f"{int(p_row.get('pressure_dismissals', 0))} Wickets"),
            ("PRESSURE SUCCESS (PSR)", f"{p_row.get('raw_psr', 0.0)*100:.1f}%", f"{int(p_row.get('successful_matches', 0))}/{int(p_row.get('psr_qualifying_matches', 0))} matches"),
            ("NET PRESSURE DVA", f"{p_row.get('pressure_cumulative_dva', 0.0):+.1f} Runs", f"{p_row.get('pressure_dva_per_ball', 0.0):+.2f}/ball")
        ]
        
    for i, (m_title, m_val, m_sub) in enumerate(metrics_summary):
        x = 12 + i * (card_w + 2.5)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(236, 234, 243)
        pdf.rect(x, y_cards, card_w, card_h, style='FD')
        
        # Color top border
        if is_bat:
            pdf.set_fill_color(192, 92, 142)
        else:
            pdf.set_fill_color(121, 100, 181)
        pdf.rect(x, y_cards, card_w, 1.2, style='F')
        
        pdf.set_xy(x + 2, y_cards + 3)
        pdf.set_font(pdf.main_font, '', 6.5)
        pdf.set_text_color(94, 88, 115)
        pdf.cell(card_w - 4, 4, text=m_title)
        
        pdf.set_xy(x + 2, y_cards + 8)
        pdf.set_font(pdf.main_font, 'B', 12)
        pdf.set_text_color(37, 35, 58)
        pdf.cell(card_w - 4, 6, text=_safe_str(m_val))
        
        pdf.set_xy(x + 2, y_cards + 15)
        pdf.set_font(pdf.main_font, '', 7)
        pdf.set_text_color(121, 100, 181 if not is_bat else 192)
        pdf.cell(card_w - 4, 4, text=_safe_str(m_sub))
        
    pdf.set_y(y_cards + card_h + 6)
    
    # --- SECTION 3: DETAILED STATISTICAL COMPARISON TABLE ---
    pdf.set_font(pdf.main_font, 'B', 10.5)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(0, 6, text="Performance Dimension Breakdown (Baseline vs High Pressure)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    
    col_w = [56, 44, 44, 42]
    # Header row
    pdf.set_fill_color(244, 242, 250)
    pdf.set_text_color(94, 88, 115)
    pdf.set_font(pdf.main_font, 'B', 7.5)
    headers = ["Metric Dimension", "Baseline (PI < 0.65)", "High Pressure (PI >= 0.65)", "Clutch Delta / Impact"]
    for w, h in zip(col_w, headers):
        pdf.cell(w, 6, text=h, border=1, fill=True, align='C')
    pdf.ln()
    
    # Table rows
    pdf.set_font(pdf.main_font, '', 8)
    num_metrics = len(stats_data['Metric'])
    delta_col_key = 'Clutch Improvement' if 'Clutch Improvement' in stats_data else 'Delta / Impact'
    for idx in range(num_metrics):
        m = _safe_str(stats_data['Metric'][idx])
        base_v = _safe_str(stats_data['Baseline (Low / Non-Pressure)'][idx])
        press_v = _safe_str(stats_data['High Pressure (PI >= 0.65)'][idx])
        delta_v = _safe_str(stats_data[delta_col_key][idx])
        
        fill = (idx % 2 == 1)
        if fill:
            pdf.set_fill_color(250, 249, 254)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        pdf.set_text_color(37, 35, 58)
        pdf.cell(col_w[0], 5.2, text=f"  {m}", border=1, fill=fill)
        pdf.set_text_color(94, 88, 115)
        pdf.cell(col_w[1], 5.2, text=base_v, border=1, fill=fill, align='C')
        pdf.set_text_color(37, 35, 58)
        pdf.cell(col_w[2], 5.2, text=press_v, border=1, fill=fill, align='C')
        
        # Colorize delta cell
        if delta_v.startswith("+"):
            pdf.set_text_color(39, 103, 73)
        elif delta_v.startswith("-") and delta_v != "-":
            pdf.set_text_color(155, 44, 44)
        else:
            pdf.set_text_color(94, 88, 115)
        pdf.cell(col_w[3], 5.2, text=delta_v, border=1, fill=fill, align='C')
        pdf.ln()
        
    pdf.ln(4)
    
    # --- SECTION 4: MATCH PHASE BREAKDOWN TABLE ---
    pdf.set_font(pdf.main_font, 'B', 10.5)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(0, 6, text="Match Phase Performance Breakdown (Powerplay, Middle, Death)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    
    col_w_ph = [36, 30, 30, 30, 30, 30]
    ph_headers = [
        "Phase", 
        "Total Balls", 
        "Base Metric" if is_bat else "Base Econ", 
        "Press Balls", 
        "Press Metric" if is_bat else "Press Econ", 
        "Press DVA"
    ]
    pdf.set_fill_color(244, 242, 250)
    pdf.set_text_color(94, 88, 115)
    pdf.set_font(pdf.main_font, 'B', 7.5)
    for w, h in zip(col_w_ph, ph_headers):
        pdf.cell(w, 6, text=h, border=1, fill=True, align='C')
    pdf.ln()
    
    pdf.set_font(pdf.main_font, '', 8)
    if not phase_df.empty:
        for idx, r in phase_df.iterrows():
            ph_name = _safe_str(r.get('phase', ''))
            tot_b = f"{int(r.get('overall_balls', 0)):,}"
            base_m = f"{r.get('overall_metric', 0.0):.1f}"
            pr_b = f"{int(r.get('pressure_balls', 0)):,}"
            pr_m = f"{r.get('pressure_metric', 0.0):.1f}"
            pr_dva = f"{r.get('pressure_dva', 0.0):+.2f}"
            
            pdf.set_text_color(37, 35, 58)
            pdf.cell(col_w_ph[0], 5.2, text=f"  {ph_name}", border=1)
            pdf.set_text_color(94, 88, 115)
            pdf.cell(col_w_ph[1], 5.2, text=tot_b, border=1, align='C')
            pdf.cell(col_w_ph[2], 5.2, text=base_m, border=1, align='C')
            pdf.set_text_color(37, 35, 58)
            pdf.cell(col_w_ph[3], 5.2, text=pr_b, border=1, align='C')
            pdf.cell(col_w_ph[4], 5.2, text=pr_m, border=1, align='C')
            pdf.cell(col_w_ph[5], 5.2, text=pr_dva, border=1, align='C')
            pdf.ln()
    else:
        pdf.cell(186, 6, text="No match phase breakdown recorded for this player.", border=1, align='C')
        pdf.ln()
        
    # ================= PAGE 2: MATCH TIMELINE, STRENGTHS & LIMITATIONS =================
    pdf.add_page()
    
    # --- SECTION 5: RECENT HIGH-PRESSURE MATCH TIMELINE ---
    pdf.set_font(pdf.main_font, 'B', 10.5)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(0, 6, text="Recent High-Pressure Match Involvements (Sample History)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    
    col_w_m = [24, 18, 48, 22, 22, 26, 26]
    m_headers = ["Date", "Season", "Opponent Team", "Balls", "Runs/Wkts", "Strike Rate" if is_bat else "Economy", "Net DVA"]
    pdf.set_fill_color(244, 242, 250)
    pdf.set_text_color(94, 88, 115)
    pdf.set_font(pdf.main_font, 'B', 7.5)
    for w, h in zip(col_w_m, m_headers):
        pdf.cell(w, 6, text=h, border=1, fill=True, align='C')
    pdf.ln()
    
    pdf.set_font(pdf.main_font, '', 7.5)
    if not match_history_df.empty:
        df_press_m = match_history_df[match_history_df['is_pressure_involved']].sort_values('match_date', ascending=False).head(8)
        if not df_press_m.empty:
            for idx, r in df_press_m.iterrows():
                m_date = _safe_str(r.get('match_date', ''))
                m_seas = _safe_str(r.get('season', ''))
                m_opp = _safe_str(r.get('away_team', ''))
                m_b = f"{int(r.get('pressure_eligible_balls', 0))}"
                m_rw = f"{int(r.get('pressure_runs', 0))}" if is_bat else f"{int(r.get('pressure_wickets_or_dismissals', 0))} wkt"
                m_met = f"{r.get('pressure_metric', 0.0):.1f}"
                m_dva = f"{r.get('pressure_dva', 0.0):+.2f}"
                
                pdf.set_text_color(37, 35, 58)
                pdf.cell(col_w_m[0], 5, text=m_date, border=1, align='C')
                pdf.set_text_color(94, 88, 115)
                pdf.cell(col_w_m[1], 5, text=m_seas, border=1, align='C')
                pdf.cell(col_w_m[2], 5, text=m_opp[:24], border=1)
                pdf.set_text_color(37, 35, 58)
                pdf.cell(col_w_m[3], 5, text=m_b, border=1, align='C')
                pdf.cell(col_w_m[4], 5, text=m_rw, border=1, align='C')
                pdf.cell(col_w_m[5], 5, text=m_met, border=1, align='C')
                pdf.cell(col_w_m[6], 5, text=m_dva, border=1, align='C')
                pdf.ln()
        else:
            pdf.cell(186, 6, text="Player has 0 high-pressure match involvements in sample.", border=1, align='C')
            pdf.ln()
    else:
        pdf.cell(186, 6, text="No match history available.", border=1, align='C')
        pdf.ln()
        
    pdf.ln(4)
    
    # --- SECTION 6: DATA-GROUNDED SCOUTING STRENGTHS ---
    pdf.set_font(pdf.main_font, 'B', 10.5)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(0, 6, text="Data-Grounded Strengths & Empirical Observations", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    
    strengths = []
    # Derive factual strengths directly from player stats (zero hallucinations)
    press_balls = int(p_row.get('pressure_exposure_balls', 0))
    dva_total = p_row.get('pressure_cumulative_dva', 0.0)
    psr_val = p_row.get('raw_psr', 0.0)
    
    if is_bat:
        sr_diff = p_row.get('delta_strike_rate', 0.0) or 0.0
        if sr_diff > 0:
            strengths.append(f"Clutch Acceleration: Pressure strike rate ({p_row['pressure_strike_rate']:.1f}) exceeds baseline ({p_row['baseline_strike_rate']:.1f}) by {sr_diff:+.1f} points.")
        if dva_total > 0:
            strengths.append(f"Positive Value Added: Generated {dva_total:+.1f} net runs of Delivery Value Added (DVA) under high leverage.")
        if psr_val >= 0.50:
            strengths.append(f"Favorable Pressure Success: Achieved a {psr_val*100:.1f}% raw Pressure Success Rate (PSR) across qualifying match appearances.")
        if not phase_df.empty:
            death_row = phase_df[phase_df['phase'] == 'Death']
            if not death_row.empty and death_row.iloc[0]['pressure_balls'] >= 15:
                strengths.append(f"Death Phase Proven: Faced {int(death_row.iloc[0]['pressure_balls'])} pressure balls in overs 16-20 with a {death_row.iloc[0]['pressure_metric']:.1f} strike rate.")
    else:
        econ_diff = p_row.get('clutch_econ_suppression', 0.0) or 0.0
        if econ_diff > 0:
            strengths.append(f"Economy Suppression: Pressure economy ({p_row['pressure_economy_rate']:.2f}) suppresses baseline scoring by {econ_diff:+.2f} runs/over.")
        if dva_total > 0:
            strengths.append(f"Defensive Run Value: Saved {dva_total:+.1f} net runs of Delivery Value Added (DVA) under high leverage.")
        if psr_val >= 0.50:
            strengths.append(f"Match Winning Rate: Produced a {psr_val*100:.1f}% raw Pressure Success Rate (PSR) across qualifying bowling matches.")
            
    if not strengths:
        strengths.append("Limited high-pressure sample volume observed in the 2022-2026 IPL tournament window.")
        
    pdf.set_font(pdf.main_font, '', 8.5)
    pdf.set_text_color(55, 50, 75)
    for st_text in strengths:
        pdf.cell(5, 5, text="*", align='C')
        pdf.multi_cell(181, 5, text=_safe_str(st_text))
        pdf.ln(1)
        
    pdf.ln(3)
    
    # --- SECTION 7: LIMITATIONS, SAMPLE DEFICITS & QUALIFICATION AUDIT ---
    pdf.set_font(pdf.main_font, 'B', 10.5)
    pdf.set_text_color(37, 35, 58)
    pdf.cell(0, 6, text="Performance Limitations & Qualification Sample Audit", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    
    limitations = []
    if is_qual:
        k_anchor = 50 if is_bat else 48
        prior_mean = 0.4303 if is_bat else 0.6210
        limitations.append(f"Sample Shrinkage Stabilization: Evaluated against cohort prior (mu = {prior_mean}) with anchor K = {k_anchor} pressure deliveries.")
        limitations.append(f"Reliability Volatility Penalty: Match-to-match standard deviation stabilized via tanh kappa factor ({p_row.get('volatility_factor', 0.95):.4f}).")
    else:
        limitations.append(f"Sample Gate Restriction: {_safe_str(p_row.get('unqualified_reasons', 'Did not meet sample minimums'))}.")
        limitations.append("Shrunk Reliability Score Withheld: To maintain statistical rigor, raw PSR is not converted into an official rank without satisfying all 3 Phase 3A sample gates.")
        
    pdf.set_font(pdf.main_font, '', 8.5)
    pdf.set_text_color(55, 50, 75)
    for lim_text in limitations:
        pdf.cell(5, 5, text="*", align='C')
        pdf.multi_cell(181, 5, text=_safe_str(lim_text))
        pdf.ln(1)
        
    pdf.ln(4)
    
    # --- SECTION 8: METHODOLOGICAL TRANSPARENCY NOTES ---
    pdf.set_fill_color(248, 248, 252)
    pdf.set_draw_color(220, 218, 230)
    pdf.rect(12, pdf.get_y(), 186, 26, style='FD')
    
    pdf.set_xy(15, pdf.get_y() + 2)
    pdf.set_font(pdf.main_font, 'B', 7.5)
    pdf.set_text_color(94, 88, 115)
    pdf.cell(180, 4, text="METHODOLOGICAL SPECIFICATION & DATA INTEGRITY NOTES (PHASE 3A VERSION 2.2):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_xy(15, pdf.get_y() + 1)
    pdf.set_font(pdf.main_font, '', 7)
    pdf.set_text_color(120, 117, 138)
    notes_text = (
        "1. Pressure Index (PI): Continuous metric in [0, 1]. Deliveries with PI >= 0.65 represent high-pressure leverage situations.\n"
        "2. Delivery Value Added (DVA): Net run value generated relative to phase and innings par baseline, including wicket adjustments.\n"
        "3. Shrinkage & Volatility: Exposure-weighted PSR is shrunk toward the IPL cohort prior and penalized by match-to-match volatility kappa.\n"
        "4. Data Isolation: Evaluated strictly across IPL 2022-2026 ball-by-ball tournament records. Exactly 0 T20I matches included in IPL ratings."
    )
    pdf.multi_cell(180, 3.8, text=_safe_str(notes_text))
    
    return bytes(pdf.output())
