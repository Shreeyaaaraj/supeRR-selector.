"""
Cricket Pressure Index — Phase 1 Inspection Launcher
====================================================
Runs the dynamic inspection module located in `src/data_inspection.py`.
"""
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.data_inspection import main

if __name__ == "__main__":
    main()
