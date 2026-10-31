#!/usr/bin/env python3
"""Write isolated target #2 inputs for an energy/graphite-density grid; never run FLUKA."""
import argparse
import csv
import hashlib
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def define(text, name, value):
    text, count = re.subn(rf'(?m)^#define {name}\s+[^\n]*$', f'#define {name} {value:.12g}', text)
    if count != 1:
        raise ValueError(f'Expected one definition of {name}, found {count}')
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--energies-mev', type=float, nargs='+', required=True)
    parser.add_argument('--graphite-rho', type=float, nargs='+', required=True,
                        help='g carbon per cm3 of target mixture; fixed Ra/Cl partial densities')
    parser.add_argument('--output-dir', type=Path, required=True, help='New directory; must not exist')
    parser.add_argument('--template', type=Path, default=ROOT / 'working/cycloinv_target2_clean.inp')
    args = parser.parse_args()
    if any(not math.isfinite(e) or e <= 0 for e in args.energies_mev):
        parser.error('Energies must be finite and positive')
    if any(not math.isfinite(r) or r < 0 for r in args.graphite_rho):
        parser.error('Graphite partial densities must be finite and nonnegative')
    template = args.template.read_text()
    fixed = {}
    for name in ('RARHO', 'CLRHO', 'EMAX'):
        fixed[name] = float(re.search(rf'(?m)^#define {name}\s+(\S+)', template)[1])
    if max(args.energies_mev) / 1000 >= fixed['EMAX']:
        parser.error('Raise template EMAX above all requested source energies before generating cases')
    args.output_dir.mkdir(parents=True, exist_ok=False)
    rows = []
    volume = math.pi * 0.2  # 1 cm radius, 2 mm thickness
    for i, energy in enumerate(dict.fromkeys(args.energies_mev), 1):
        for j, carbon in enumerate(dict.fromkeys(args.graphite_rho), 1):
            case = args.output_dir / f'e{i:02d}_g{j:02d}'
            case.mkdir()
            rho = carbon + fixed['RARHO'] + fixed['CLRHO']
            text = define(template, 'EBEAM', energy / 1000)
            text = define(text, 'CRHO', carbon)
            text = define(text, 'RHOM', rho)
            # A zero carbon weight is removed explicitly, avoiding a negative-zero field.
            if carbon == 0:
                text = text.replace('    -$CRHO    CARBON', '                    ')
            text = text.replace('RaCl2 graphite target: enclosed Al housing, variable energy/loading',
                                f'RaCl2 graphite target: {energy:g} MeV, carbon {carbon:g} g/cm3')
            inp = case / 'target2.inp'
            inp.write_text(text)
            rows.append(dict(case=case.name, energy_MeV=energy, graphite_g_cm3=carbon,
                             mixture_g_cm3=rho, graphite_mass_g=carbon * volume,
                             Ra226_mass_g=fixed['RARHO'] * volume,
                             Cl_mass_g=fixed['CLRHO'] * volume,
                             graphite_mass_fraction=carbon / rho,
                             executable='/usr/local/fluka/bin/flukadpm',
                             input_sha256=hashlib.sha256(inp.read_bytes()).hexdigest()))
    with (args.output_dir / 'cases.csv').open('w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    print(f'Created {len(rows)} input cases in {args.output_dir}; no simulations launched.')

if __name__ == '__main__':
    main()
