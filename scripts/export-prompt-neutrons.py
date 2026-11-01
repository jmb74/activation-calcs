#!/usr/bin/env python3
"""Export outer-case prompt neutron currents by energy; never starts FLUKA."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'working/readers'))
from export_photons import export_prompt_neutrons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table', type=Path, help='Unit-24 processed *_tab.lis')
    parser.add_argument('output', type=Path, help='New output directory')
    parser.add_argument('--input', type=Path, required=True, help='Matching run input')
    args = parser.parse_args()
    try:
        export_prompt_neutrons(args.table, args.input, args.output)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Neutron export refused: {error}\n')


if __name__ == '__main__':
    main()
