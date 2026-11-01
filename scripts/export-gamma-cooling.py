#!/usr/bin/env python3
"""Export geometry-checked outer-case photon currents by energy and cooling time.

Usage: export-gamma-cooling.py TABLE OUTPUT_DIR --input RUN.inp
       [--prompt-table UNIT24_tab.lis]
Units and normalization are recorded in each export README and metadata.json.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'working' / 'readers'))
from export_photons import main

if __name__ == '__main__':
    main()
