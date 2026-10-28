#!/usr/bin/env python3
"""Export a wide cooling-time activity table using the shared fluka-util parser.

Optional current scaling applies only to irradiation-induced activation in the
same fixed-material linear decay model. Sources and raw run products are unchanged.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'fluka-util'))
from process_rn_tab import read_table, __version__

REGIONS = {3: 'ALCASE', 4: 'HAV1', 5: 'WAT', 6: 'HAV2', 7: 'TGT'}
TIMES = (0, 3600, 86400, 604800)
E_CHARGE = 1.602176634e-19


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def writecsv(path, rows):
    with path.open('x', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def export(table, summary, out, source_current_ua, target_current_ua=None):
    table, summary = table.resolve(), summary.resolve()
    if out.exists():
        raise ValueError(f'Output already exists: {out}')
    target_current_ua = source_current_ua if target_current_ua is None else target_current_ua
    if not all(math.isfinite(v) and v > 0 for v in (source_current_ua, target_current_ua)):
        raise ValueError('Currents must be finite and positive')
    summary_text = summary.read_text()
    rates = set(map(float, re.findall(r'Beam intensity\s*:\s*([\d.Ee+-]+)\s+pr/s', summary_text)))
    durations = set(map(float, re.findall(r'Irradiation time\s*:\s*([\d.Ee+-]+)\s+s', summary_text)))
    if len(rates) != 1 or len(durations) != 1:
        raise ValueError('Expected one explicit irradiation rate and duration in summary')
    rate = next(iter(rates))
    observed_ua = rate * E_CHARGE * 1e6
    if not math.isclose(observed_ua, source_current_ua, rel_tol=1e-6):
        raise ValueError(f'Source current {source_current_ua} microA disagrees with summary ({observed_ua:.8g})')
    scale = target_current_ua / source_current_ua
    before = {str(p): sha(p) for p in (table, summary)}
    detectors = read_table(table, summary)
    if len(detectors) != 20:
        raise ValueError('Expected 5 regions at 4 cooling times')
    data = defaultdict(dict)
    identities = set()
    metadata = []
    expected_totals = defaultdict(float)
    for detector in detectors:
        if detector.value_unit != 'Bq' or detector.normalization != 1:
            raise ValueError(f'Expected whole-region Bq: {detector.name}')
        if detector.region_number not in REGIONS or detector.cooling_time_s not in TIMES:
            raise ValueError(f'Unexpected region/time: {detector.name}')
        region = REGIONS[detector.region_number]
        time = int(detector.cooling_time_s)
        if (region, time) in identities:
            raise ValueError('Duplicate region/time')
        identities.add((region, time))
        count = 0
        for nuclide in detector.nuclides:
            if not nuclide.value:
                continue
            key = (region, nuclide.z, nuclide.a, nuclide.m, nuclide.label)
            if time in data[key]:
                raise ValueError('Duplicate nuclide/state/time')
            value = nuclide.value * scale
            data[key][time] = (value, nuclide.relative_error_percent, nuclide.absolute_error * scale)
            expected_totals[(region, time)] += value
            count += 1
        metadata.append(dict(detector=detector.name, region=region, cooling_time_s=time, nonzero_rows=count))
    if identities != {(r, t) for r in REGIONS.values() for t in TIMES}:
        raise ValueError('Incomplete region/time coverage')

    by_region = []
    for (region, z, a, m, label), values in sorted(data.items()):
        row = dict(region=region, isotope=label, z=z, a=a, m=m)
        for time in TIMES:
            row[f'activity_{time}s'] = values.get(time, (0, None, None))[0]
        for time in TIMES:
            row[f'relative_error_{time}s_percent'] = values.get(time, (0, None, None))[1]
        for time in TIMES:
            row[f'absolute_statistical_error_{time}s_Bq'] = values.get(time, (0, None, None))[2]
        by_region.append(row)
    totals = {}
    for row in by_region:
        key = (row['z'], row['a'], row['m'], row['isotope'])
        if key not in totals:
            totals[key] = dict(isotope=row['isotope'], z=row['z'], a=row['a'], m=row['m'],
                               **{f'activity_{t}s': 0. for t in TIMES})
        for time in TIMES:
            totals[key][f'activity_{time}s'] += row[f'activity_{time}s']
    summed = [totals[k] for k in sorted(totals)]

    # Check every time/region and the intact-apparatus sum against the parsed input.
    for (region, time), expected in expected_totals.items():
        actual = sum(r[f'activity_{time}s'] for r in by_region if r['region'] == region)
        if not math.isclose(actual, expected, rel_tol=1e-12):
            raise ValueError(f'Activity conservation failed: {region}/{time}')
    for time in TIMES:
        if not math.isclose(sum(r[f'activity_{time}s'] for r in summed),
                            sum(r[f'activity_{time}s'] for r in by_region), rel_tol=1e-12):
            raise ValueError('Component summation failed')

    out.mkdir(parents=True)
    writecsv(out / 'all-components-by-region.csv', by_region)
    writecsv(out / 'all-components-summed.csv', summed)
    for region in REGIONS.values():
        writecsv(out / f'{region}.csv', [r for r in by_region if r['region'] == region])
    files = []
    for path in sorted(out.glob('*.csv')):
        with path.open() as stream:
            saved = list(csv.DictReader(stream))
        if not saved or any('upper_bound' in column for column in saved[0]):
            raise ValueError(f'Invalid export columns: {path}')
        if path.name == 'all-components-by-region.csv':
            if len(saved) != len(by_region):
                raise ValueError('Export row count mismatch')
            for original, written in zip(by_region, saved):
                if original['isotope'] != written['isotope'] or any(
                    original[f'activity_{t}s'] != float(written[f'activity_{t}s']) for t in TIMES
                ):
                    raise ValueError('Export changed identity or values')
        files.append(dict(file=path.name, rows=len(saved), sha256=sha(path)))
    meta = dict(schema_version=2, layout='one nuclide/state per row, all cooling times as columns',
                activity_columns_unit='Bq', parser='fluka-util.process_rn_tab', parser_version=__version__,
                source=str(table), source_sha256=before[str(table)], summary=str(summary),
                summary_sha256=before[str(summary)], source_beam_rate_per_s=rate,
                irradiation_s=next(iter(durations)), source_current_microA=source_current_ua,
                output_current_microA=target_current_ua, current_scale_factor=scale,
                result_origin='linear current rescaling of existing run; not a new simulation' if scale != 1 else 'existing simulation, no scaling',
                cooling_times_s=TIMES, summed_uncertainty='omitted; regional covariance unavailable',
                zero_cells='No nonzero entry at this time in processed table; not proof of physical absence',
                scope='Irradiation-induced nuclides and daughters; excludes initially loaded Ra-226 and pre-existing daughters',
                detectors=metadata, files=files)
    (out / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
    (out / 'README.md').write_text(f'''# Combined cooling-time product tables

Output current: **{target_current_ua:g} microA**, irradiation {next(iter(durations)):g} s.
Source simulation current: **{source_current_ua:g} microA**. Scale factor: **{scale:g}**.
Origin: **{meta['result_origin']}**.

Seven CSVs contain five individual components, all components with region identity,
and an isotope-summed intact-apparatus table. All files have activity_0s,
activity_3600s, activity_86400s and activity_604800s columns. **All activity values
are Bq**. Ground and metastable states are separate. Relative statistical errors
are percentages; absolute per-region statistical errors are Bq. Relative errors
are unchanged by current scaling; absolute errors scale with activity.
The summed table contains no statistical-upper-bound column or combined error.
Regional covariance is unavailable. Blank errors accompany zero/unprinted cells.

The scaling, when used, follows linear fixed-material activation/decay equations
with the identical irradiation duration, time profile, beam, geometry and material
properties. Decay constants, saturation and daughter ingrowth do not break that
linearity. This does not model heating/density changes, target burnup or irradiation
of the accumulated inventory. Initial Ra-226 and pre-existing daughters are excluded
and must not be multiplied by the beam-current factor. These are inventory tables,
not gamma emission lists or MCNP SDEF cards. No simulation is launched by this tool.

Source identities, hashes, parsed current, cooling times and output hashes are
in metadata.json. Original source files and prior export packages are preserved.
''')
    if any(sha(Path(p)) != digest for p, digest in before.items()):
        raise ValueError('Source changed during export')
    print(f'Exported 7 wide CSVs at {target_current_ua:g} microA (factor {scale:g}): {out}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table', type=Path)
    parser.add_argument('--summary', type=Path, required=True)
    parser.add_argument('--source-current-ua', type=float, required=True)
    parser.add_argument('--target-current-ua', type=float)
    parser.add_argument('-o', '--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        export(args.table, args.summary, args.output, args.source_current_ua, args.target_current_ua)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Export refused: {error}\n')


if __name__ == '__main__':
    main()
