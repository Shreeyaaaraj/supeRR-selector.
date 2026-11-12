"""
Root-level forwarding proxy for dashboard_data.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_ROOT, 'src')

for _dir in [_ROOT, _SRC]:
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
    import importlib.util
    _src_dash = os.path.join(_SRC, 'dashboard_data.py')
    if os.path.exists(_src_dash):
        _spec = importlib.util.spec_from_file_location("dashboard_data", _src_dash)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        load_pressure_overview = _mod.load_pressure_overview
        load_all_players = _mod.load_all_players
        load_top10_batters = _mod.load_top10_batters
        load_top10_bowlers = _mod.load_top10_bowlers
        load_player_match_history = _mod.load_player_match_history
        load_player_phase_breakdown = _mod.load_player_phase_breakdown
        load_ipl_matches = _mod.load_ipl_matches
        load_ipl_deliveries = _mod.load_ipl_deliveries
        load_player_match_deliveries = _mod.load_player_match_deliveries
    else:
        raise

