"""Read processed RESNUCLEi tables with summary and geometry provenance.

No simulations or FLUKA processing utilities are executed. Standard library only.
"""
import argparse
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

__version__ = '1.0.0'
ELEMENTS = ('nn H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe '
            'Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb '
            'Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os '
            'Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md '
            'No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og').split()


def number(s):
    v = float(s.replace('D', 'E').replace('d', 'e'))
    if not math.isfinite(v):
        raise ValueError(f'Nonfinite value: {s}')
    return v


@dataclass
class Nuclide:
    z: int
    a: int
    m: int
    value: float
    relative_error_percent: float

    @property
    def label(self):
        return f'{ELEMENTS[self.z]}-{self.a}' + (f'-m{self.m}' if self.m else '')

    @property
    def absolute_error(self):
        return self.value * self.relative_error_percent / 100


@dataclass
class Detector:
    number: int
    name: str
    region_number: int
    normalization: float
    cooling_time_s: float | None
    value_unit: str
    total: float
    total_relative_error_percent: float
    beam_rate_per_s: float | None
    irradiation_s: float | None
    nuclides: list = field(default_factory=list)
    rounding_bound: float = 0.


def read_table(table, summary):
    """Return whole-region Bq or nuclei/primary, undoing WHAT(6) division.

    Times and numeric region IDs come from the summary, never detector suffixes.
    Ground and metastable states remain distinct, including the last table row.
    """
    text = Path(summary).read_text()
    headers = list(re.finditer(r'^\s*Detector n:\s*(\d+)\s+(\S+)', text, re.M))
    detectors = {}
    for i, h in enumerate(headers):
        block = text[h.end():headers[i+1].start() if i+1 < len(headers) else len(text)]
        region = re.search(r'Region\s+(\d+)\s+Volume:\s*(\S+)', block)
        total = re.search(r'Tot\. response\s*\(([^)]+)\)\s*(\S+)\s*\+/-\s*(\S+)', block)
        if not region or not total:
            raise ValueError(f'Missing summary metadata: {h[2]}')
        def prior(label):
            values = re.findall(label + r'\s*:\s*(\S+)', text[:h.start()])
            return number(values[-1]) if values else None
        unit = {'Bq/cmc': 'Bq', 'n/cmc/pr': 'nuclei/primary'}.get(total[1])
        if unit is None:
            raise ValueError(f'Unsupported summary unit: {total[1]}')
        norm = number(region[2])
        if norm <= 0:
            raise ValueError('Normalization must be positive')
        d = Detector(int(h[1]), h[2], int(region[1]), norm,
                     prior('Decay time') if unit == 'Bq' else None, unit,
                     number(total[2])*norm, number(total[3]),
                     prior('Beam intensity'), prior('Irradiation time'))
        if d.number in detectors or any(x.name == d.name for x in detectors.values()):
            raise ValueError('Duplicate summary detector')
        if unit == 'Bq' and d.cooling_time_s is None:
            raise ValueError('Activity detector lacks a decay time')
        detectors[d.number] = d
    if not detectors:
        raise ValueError('No RESNUCLEi summary detectors')

    active = None
    state = None
    seen_detectors = set()
    seen_nuclides = set()
    expect_name = False
    for line in Path(table).read_text().splitlines():
        if not line.strip():
            continue
        h = re.match(r'# Detector n:\s*(\d+)\s*$', line.strip())
        if h:
            n = int(h[1])
            if n not in detectors or n in seen_detectors:
                raise ValueError(f'Unknown/duplicate table detector: {n}')
            active = detectors[n]
            seen_detectors.add(n)
            seen_nuclides = set()
            state = None
            expect_name = True
        elif expect_name:
            if line.strip() != active.name:
                raise ValueError(f'Table/summary detector mismatch: {line}')
            expect_name = False
        elif line.strip() == '# A/Z Isotopes:':
            state = 0
        elif line.strip() == '# A/Z/m Isomers:':
            state = 1
        elif line.lstrip().startswith('#'):
            # Skip the redundant mass/charge projections in production tables.
            state = None
        elif state is not None:
            cols = line.split()
            if len(cols) != 4 + state:
                raise ValueError(f'Malformed nuclide row: {line}')
            a, z = map(int, cols[:2])
            m = int(cols[2]) if state else 0
            value, error = map(number, cols[-2:])
            if not (0 < z < len(ELEMENTS) and (a >= z or value == 0) and m >= state and value >= 0 and error >= 0):
                raise ValueError(f'Invalid nuclide row: {line}')
            key = (z, a, m)
            if key in seen_nuclides:
                raise ValueError(f'Duplicate nuclide state in {active.name}: {key}')
            seen_nuclides.add(key)
            if value:
                active.nuclides.append(Nuclide(z, a, m, value*active.normalization, error))
                # Bound the text rounding by half the last printed decimal place.
                exponent = Decimal(cols[-2].replace('D', 'E')).as_tuple().exponent
                active.rounding_bound += .5 * 10.**exponent * active.normalization
    if seen_detectors != set(detectors) or expect_name:
        raise ValueError('Incomplete table/summary detector coverage')
    for d in detectors.values():
        difference = abs(math.fsum(n.value for n in d.nuclides) - d.total)
        if difference > d.rounding_bound + abs(d.total)*2e-7:
            raise ValueError(f'Nuclide sum disagrees with summary total: {d.name} ({difference:g})')
    return list(detectors.values())


def read_geometry(path):
    """Read unconditional COMBNAME region order and single-region assignments.

    Refuse conditional/include geometry rather than silently misnumbering it.
    """
    text = Path(path).read_text()
    match = re.search(r'^GEOBEGIN[^\n]*COMBNAME.*?^END\s*\n(.*?)^END\s*$', text, re.M | re.S)
    if not match:
        raise ValueError('Expected an unconditional COMBNAME geometry')
    regions = {}
    for line in match[1].splitlines():
        if not line.strip() or line.startswith('*'):
            continue
        if line.startswith('#'):
            raise ValueError('Preprocess conditional geometry before reading')
        if line[0].isspace() or line.startswith('|'):
            continue
        name, neighbors, *_ = line.split()
        int(neighbors)
        if name in regions.values():
            raise ValueError(f'Duplicate geometry region: {name}')
        regions[len(regions)+1] = name
    if not regions:
        raise ValueError('No geometry regions')
    return regions


def validate_geometry(detectors, geometry, table):
    regions = read_geometry(geometry)
    unit_match = re.search(r'_(\d+)_tab\.lis$', str(table))
    if not unit_match:
        raise ValueError('Expected filename ending _UNIT_tab.lis')
    unit = int(unit_match[1])
    scoring = {}
    for line in Path(geometry).read_text().splitlines():
        if line[:10].strip() != 'RESNUCLE':
            continue
        if int(number(line[20:30].strip())) != -unit:
            continue
        name = line[70:80].strip()
        if name in scoring:
            raise ValueError(f'Duplicate input scoring name: {name}')
        scoring[name] = line[50:60].strip()
    if set(scoring) != {d.name for d in detectors}:
        raise ValueError('Input/table scoring detector coverage differs')
    for d in detectors:
        if d.region_number not in regions or scoring[d.name] != regions[d.region_number]:
            raise ValueError(f'Geometry/summary region mismatch: {d.name}')
    return regions


def write_csv(path, fields, rows):
    with path.open('x', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export(tables, geometry, output):
    if output.exists():
        raise ValueError(f'Output already exists: {output}')
    sources = [geometry]
    for table in tables:
        sources.extend([table, table.with_name(table.name.replace('_tab.lis', '_sum.lis'))])
    before = {str(p.resolve()): sha(p) for p in sources}
    datasets = {}
    regions = read_geometry(geometry)
    for table in tables:
        summary = table.with_name(table.name.replace('_tab.lis', '_sum.lis'))
        detectors = read_table(table, summary)
        validate_geometry(detectors, geometry, table)
        kind = 'activity' if detectors[0].value_unit == 'Bq' else 'production'
        if kind in datasets or any(d.value_unit != detectors[0].value_unit for d in detectors):
            raise ValueError('Duplicate or mixed dataset kinds')
        datasets[kind] = detectors
    metadata = dict(reader_version=__version__, sources_sha256=before,
                    regions=regions, current_scaling=1,
                    total_primaries={p.name: int(re.search(r'Total primaries run:\s*(\d+)', p.read_text())[1])
                                     for p in sources if p.name.endswith('_sum.lis')},
                    initial_inventory='Irradiation-induced products/daughters only; loaded Ra-226 and pre-existing daughters are not added.',
                    normalization='Whole-region values: printed values multiplied by RESNUCLEi WHAT(6), not physical geometry volume.',
                    summed_errors='Omitted: covariance between regions is unavailable.',
                    datasets={})
    pending = []
    for kind, detectors in datasets.items():
        unit = detectors[0].value_unit
        rows = []
        totals = []
        wide = defaultdict(dict)
        identities = set()
        times = sorted({d.cooling_time_s for d in detectors}) if kind == 'activity' else [None]
        scored_regions = sorted({d.region_number for d in detectors})
        for d in detectors:
            identity = d.region_number, d.cooling_time_s
            if identity in identities:
                raise ValueError('Duplicate region/cooling time')
            identities.add(identity)
            base = dict(detector=d.name, region_number=d.region_number, region=regions[d.region_number],
                        cooling_time_s=d.cooling_time_s, unit=unit)
            for n in sorted(d.nuclides, key=lambda n: (n.z, n.a, n.m)):
                rows.append(dict(base, isotope=n.label, z=n.z, a=n.a, m=n.m,
                                 value=n.value, relative_error_percent=n.relative_error_percent,
                                 absolute_statistical_error=n.absolute_error))
                wide[(d.region_number, n.z, n.a, n.m, n.label)][d.cooling_time_s] = n
            row_sum = math.fsum(n.value for n in d.nuclides)
            totals.append(dict(base, summary_total=d.total, table_sum=row_sum,
                               relative_error_percent=d.total_relative_error_percent,
                               difference=abs(row_sum-d.total), text_rounding_bound=d.rounding_bound,
                               normalization=d.normalization, nonzero_states=len(d.nuclides)))
        if identities != {(r, t) for r in scored_regions for t in times}:
            raise ValueError('Incomplete region/time grid')
        if kind == 'activity' and any(
            d.beam_rate_per_s != detectors[0].beam_rate_per_s or d.irradiation_s != detectors[0].irradiation_s
            for d in detectors
        ):
            raise ValueError('Inconsistent irradiation profiles')
        pending.append((f'{kind}-all-regions.csv', list(rows[0]), rows))
        pending.append((f'{kind}-regional-totals.csv', list(totals[0]), totals))
        value_cols = {t: f'activity_{t:g}s_Bq' if t is not None else 'yield_nuclei_per_primary' for t in times}
        wide_rows = []
        summed = {}
        for (r, z, a, m, label), values in sorted(wide.items()):
            row = dict(region_number=r, region=regions[r], isotope=label, z=z, a=a, m=m)
            key = z, a, m
            total_row = summed.setdefault(key, dict(isotope=label, z=z, a=a, m=m,
                                                    **{c: 0. for c in value_cols.values()}))
            for t, c in value_cols.items():
                row[c] = values[t].value if t in values else 0.
                total_row[c] += row[c]
            wide_rows.append(row)
        for r in scored_regions:
            pending.append((f'{kind}-{regions[r]}.csv', list(wide_rows[0]),
                            [row for row in wide_rows if row['region_number'] == r]))
        summed_rows = [summed[key] for key in sorted(summed)]
        pending.append((f'{kind}-all-components-summed.csv', list(summed_rows[0]), summed_rows))
        metadata['datasets'][kind] = dict(detectors=len(detectors), cooling_times_s=times,
                                          nonzero_rows=len(rows), unit=unit,
                                          beam_rate_per_s=detectors[0].beam_rate_per_s,
                                          irradiation_s=detectors[0].irradiation_s,
                                          current_microA=(detectors[0].beam_rate_per_s*1.602176634e-13
                                                          if detectors[0].beam_rate_per_s else None),
                                          max_total_difference=max(t['difference'] for t in totals))
    if any(sha(Path(p)) != digest for p, digest in before.items()):
        raise ValueError('A source changed during reading')
    output.mkdir(parents=True)
    for name, fields, rows in pending:
        write_csv(output / name, fields, rows)
    metadata['outputs'] = {p.name: sha(p) for p in sorted(output.glob('*.csv'))}
    (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (output / 'README.md').write_text('''# RESNUCLEi export

Region names/order are read from the supplied run input and checked against
each summary region number and input scoring card. Cooling times come from
the summaries, not the detector name suffix. No current scaling is applied.

`activity-REGION.csv` contains Bq at every available cooling time. The target
is `activity-TGT.csv`. `production-REGION.csv` contains nuclei per incident
primary, including stable products; it is a production yield, not the final
number of atoms after irradiation. Long `*-all-regions.csv` tables retain
per-state statistical errors (relative percent and absolute in the stated unit).
Ground states and metastable states (m1, m2, ...) are separate.

`*-regional-totals.csv` compares the nuclide sums against independently printed
summary totals within text-rounding bounds. A normalization of 1 means whole-region
scoring, even though FLUKA labels the printed result per cm3. Do not multiply
these exported values by physical region volumes or by current again.

Summed component tables omit combined statistical errors because regional
covariance is unavailable. Zero cells mean no nonzero entry was printed; they
do not establish physical absence. All printed nonzero states are retained.
These tables do not add the initially loaded Ra-226 or pre-existing daughters
and are not photon emission spectra. metadata.json records all source hashes,
irradiation conditions, cooling times, and output hashes. Sources are unchanged.
''')
    print(json.dumps(dict(output=str(output.resolve()), datasets=metadata['datasets']), indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tables', type=Path, nargs='+', help='Processed UNIT_tab.lis files')
    parser.add_argument('--input', type=Path, required=True, help='Matching run input (geometry/scoring)')
    parser.add_argument('-o', '--output', type=Path, required=True)
    parser.add_argument('--photon-tables', type=Path, nargs='+',
                        help='Also export outer-case USXSUW photon spectra into output/photons')
    args = parser.parse_args()
    try:
        export(args.tables, args.input, args.output)
        if args.photon_tables:
            from export_photons import export_photons
            export_photons(args.photon_tables, args.input, args.output / 'photons')
    except (OSError, ValueError) as error:
        parser.exit(2, f'Export refused: {error}\n')


if __name__ == '__main__':
    main()
