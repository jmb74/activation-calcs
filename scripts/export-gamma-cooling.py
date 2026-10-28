#!/usr/bin/env python3
"""Export unit-38 USXSUW angle-integrated gamma spectra; never runs FLUKA."""
import argparse
import csv
import math
import re
from pathlib import Path


def read_spectra(path):
    spectra = {}
    active = None
    for line in path.read_text().splitlines():
        header = re.match(r'\s*# Detector n:\s*\d+\s+(\w+)\s+\(integrated over solid angle\)', line)
        if header:
            active = header[1]
            if active in spectra:
                raise ValueError(f'Duplicate detector {active}')
            spectra[active] = []
            continue
        if 'double differential distributions' in line:
            active = None
        if active and line.strip() and not line.lstrip().startswith('#'):
            values = [float(v.replace('D', 'E')) for v in line.split()]
            if len(values) != 4 or not all(math.isfinite(v) for v in values):
                raise ValueError(f'Invalid spectrum row: {line}')
            lo, hi, value, error = values
            if not 0 <= lo < hi or value < 0 or error < 0:
                raise ValueError(f'Invalid bin: {line}')
            spectra[active].append(values)
    return spectra


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table', type=Path, help='unit 38 USXSUW *_tab.lis')
    parser.add_argument('output', type=Path, help='new output CSV')
    args = parser.parse_args()
    spectra = read_spectra(args.table)
    times = list(range(0, 86401, 3600)) + [d*86400 for d in range(2, 11)]
    expected = {f'G{i:03}{kind}{face}' for i in range(1, 35)
                for kind in ('L', 'B') for face in ('A', 'H')}
    if set(spectra) != expected:
        raise ValueError(f'Detector mismatch: missing={expected-set(spectra)}, extra={set(spectra)-expected}')
    rows = []
    for i, time in enumerate(times, 1):
        for kind, count in [('L', 3000), ('B', 600)]:
            a, h = (spectra[f'G{i:03}{kind}{f}'] for f in ('A', 'H'))
            if len(a) != count or len(h) != count:
                raise ValueError('Unexpected number of energy bins')
            for left, right in zip(a, h):
                if left[:2] != right[:2]:
                    raise ValueError('Surface energy grids differ')
                lo, hi = left[:2]
                # USXSUW angle-integrated tables are differential per GeV.
                rate = left[2] + right[2]
                rows.append([time, kind, lo*1e3, hi*1e3,
                             rate/1e3, rate*(hi-lo), left[3], right[3]])
    with args.output.open('x', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['cooling_time_s', 'grid', 'energy_low_MeV', 'energy_high_MeV',
                         'escaping_photons_per_s_per_MeV', 'escaping_photons_per_s_in_bin',
                         'case_relative_error_percent', 'front_relative_error_percent'])
        writer.writerows(rows)
    print(f'Wrote {len(rows)} bins to {args.output}')


if __name__ == '__main__':
    main()
