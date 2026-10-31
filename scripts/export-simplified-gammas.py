#!/usr/bin/env python3
"""Export USXSUW tab.lis photon currents from the simplified scoring deck.

Usage: export-simplified-gammas.py OUTPUT.csv INPUT_tab.lis [INPUT_tab.lis ...]
Prompt values remain per incident proton; delayed values are already per second.
Only angle-integrated USXSUW tables are read, never double differential tables.
"""
import argparse
import csv
import math
import re
from pathlib import Path

TIMES = [0] + list(range(3600, 86401, 3600)) + list(range(172800, 864001, 86400))


def export(paths):
    seen = set()
    for path in paths:
        name = None
        for line in path.read_text().splitlines():
            match = re.match(r'\s*# Detector n:\s*\d+\s+(\w+)\s+\(integrated over solid angle\)', line)
            if match:
                name = match[1]
                if name in seen:
                    raise ValueError(f'Duplicate detector {name}; combine cycles with USXSUW first')
                seen.add(name)
                continue
            if 'double differential distributions' in line:
                name = None
            if name is None or not line.strip() or line.lstrip().startswith('#'):
                continue
            angular = re.fullmatch(r'A(\d{3})G(0[1-6])', name)
            total = re.fullmatch(r'G(\d{3})([LB])TOT', name)
            if name != 'PRGTOT' and not angular and not total:
                continue
            lo, hi, value, error = (float(v.replace('D', 'E')) for v in line.split())
            t = int((angular or total)[1]) if angular or total else 0
            prompt = t == 0
            omega = 4 * math.pi
            band = ''
            if angular:
                band = int(angular[2])
                omega = 2 * math.pi * (math.cos(math.radians((band-1)*30)) - math.cos(math.radians(band*30)))
            yield dict(detector=name, kind='prompt' if prompt else 'delayed',
                       cooling_s='' if prompt else TIMES[t-1],
                       grid=total[2] if total else 'B', band=band,
                       solid_angle_sr=omega, energy_low_MeV=lo*1000,
                       energy_high_MeV=hi*1000,
                       basis='per_primary' if prompt else 'per_second',
                       photons_per_MeV=value/1000,
                       photons_in_bin=value*(hi-lo),
                       photons_per_MeV_sr=value/1000/omega if angular else '',
                       error_percent=error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('inputs', type=Path, nargs='+')
    args = parser.parse_args()
    rows = list(export(args.inputs))
    if not rows:
        parser.error('No simplified-deck photon detectors found')
    with args.output.open('x', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} energy bins to {args.output}')


if __name__ == '__main__':
    main()
