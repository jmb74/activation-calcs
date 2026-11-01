"""Export outer-case photon leakage spectra from processed USXSUW results."""
import argparse
import csv
import json
import math
import re
from decimal import Decimal
from pathlib import Path

from process_rn_tab import number, read_geometry, sha, write_csv


def read_input(path, particle='PHOTON'):
    lines = path.read_text().splitlines()
    regions = read_geometry(path)
    defines = {}
    times = []
    detectors = {}
    associations = {}
    rate = duration = None
    active = None
    def value(token):
        return number(defines[token[1:]] if token.startswith('$') else token)
    for line in lines:
        if line.startswith('#define '):
            fields = line.split()
            if len(fields) == 3:
                defines[fields[1]] = fields[2]
        tag = line[:10].strip()
        fields = [line[i:i+10].strip() for i in range(10, 70, 10)]
        name = line[70:80].strip()
        if tag == 'DCYTIMES':
            times.extend(value(f) for f in fields if f)
        elif tag == 'IRRPROFI':
            if rate is not None or any(fields[2:]):
                raise ValueError('Expected a single constant irradiation interval')
            duration, rate = map(value, fields[:2])
        elif tag == 'USRBDX':
            if name == '&':
                if active is not None:
                    detectors[active]['grid'] = list(map(value, fields))
                active = None
            elif fields[1] == particle and fields[3:5] == ['ALCASE', 'VACREG']:
                if name in detectors:
                    raise ValueError(f'Duplicate photon detector: {name}')
                mode = int(value(fields[0]))
                if mode not in (1, -1):
                    raise ValueError('This exporter requires one-way current scoring')
                detectors[name] = dict(mode=mode, unit=int(abs(value(fields[2]))),
                                       divisor=value(fields[5]) if fields[5] else 1.)
                active = name
            else:
                active = None
        elif tag == 'DCYSCORE' and name == 'USRBDX':
            if fields[3] in detectors or fields[4] in detectors:
                if fields[3] != fields[4]:
                    raise ValueError('Expected explicit single-detector photon decay association')
                associations[fields[3]] = int(value(fields[0]))
    for name, d in detectors.items():
        if 'grid' not in d or d['divisor'] <= 0:
            raise ValueError(f'Incomplete photon detector: {name}')
        hi, lo, count, omega_hi, omega_lo, nangle = d['grid']
        if not (0 < lo < hi and count > 0 and count == int(count)
                and omega_lo == 0 and math.isclose(omega_hi, 2*math.pi, rel_tol=1e-7) and nangle == 1):
            raise ValueError('Expected positive energy grid covering the complete outward hemisphere')
        d['count'] = int(count)
        d['edges'] = [lo+(hi-lo)*i/int(count) if d['mode'] == 1
                      else lo*(hi/lo)**(i/int(count)) for i in range(int(count)+1)]
        index = associations.get(name)
        if index is not None and not 1 <= index <= len(times):
            raise ValueError('Invalid decay index')
        d['cooling_s'] = times[index-1] if index else None
    # Explicitly verify the full external surface used by this project's geometry.
    region_lines = {line.split()[0]: line.split()[2:] for line in lines
                    if re.match(r'^(ALCASE|VACREG)\s+\d+\s', line)}
    if region_lines != {'ALCASE': ['+outer', '-inner'], 'VACREG': ['+world', '-outer']}:
        raise ValueError('Cannot derive the full case surface from this geometry')
    body = next((line.split()[2:] for line in lines if re.match(r'^RCC\s+outer\s', line)), None)
    if body is None or len(body) != 7:
        raise ValueError('Expected a closed RCC outer case')
    x, y, z, dx, dy, dz, radius = map(value, body)
    length = math.sqrt(dx*dx+dy*dy+dz*dz)
    if length <= 0 or radius <= 0 or not rate or rate <= 0:
        raise ValueError('Invalid case dimensions or beam rate')
    area = 2*math.pi*radius*(radius+length)
    return dict(regions=regions, detectors=detectors, times=times, area_cm2=area,
                beam_rate_per_s=rate, irradiation_s=duration)


def read_summary(path):
    result = {}
    active = None
    with path.open() as stream:
        for line in stream:
            h = re.match(r'\s*Detector n:\s*\d+\s*\(\s*\d+\s*\)\s*(\S+)', line)
            if h:
                active = h[1]
                if active in result:
                    raise ValueError('Duplicate summary detector')
                result[active] = {}
            if active is None:
                continue
            d = result[active]
            area = re.search(r'Area:\s*(\S+)', line)
            boundary = re.search(r'from reg\.\s*(\d+)\s+to\s*(\d+)', line)
            total = re.search(r'Tot\. resp\.\s*\(Part/cmq/pr\)\s*(\S+)\s*\+/-\s*(\S+)', line)
            if area:
                d['divisor'] = number(area[1])
            if boundary:
                d['boundary'] = tuple(map(int, boundary.groups()))
            if 'one way scoring' in line:
                d['one_way'] = True
            if 'current scoring' in line:
                d['current'] = True
            if total:
                d['total'], d['error'] = map(number, total.groups())
    return result


def read_spectra(path):
    result = {}
    active = None
    with path.open() as stream:
        for line in stream:
            h = re.match(r'\s*# Detector n:\s*\d+\s+(\S+)\s+\(integrated over solid angle\)', line)
            if h:
                active = h[1]
                if active in result:
                    raise ValueError('Duplicate table detector')
                result[active] = []
            elif 'double differential distributions' in line:
                active = None
            elif active and line.strip() and not line.lstrip().startswith('#'):
                cols = line.split()
                if len(cols) != 4:
                    raise ValueError(f'Malformed photon bin: {line}')
                lo, hi, v, err = map(number, cols)
                if not (0 <= lo < hi and v >= 0 and err >= 0):
                    raise ValueError('Invalid photon bin')
                rounding = .5*10.**Decimal(cols[2].replace('D', 'E')).as_tuple().exponent if v else 0.
                result[active].append((lo, hi, v, err, rounding))
    return result


def export_particles(tables, geometry, output, particle='PHOTON'):
    if particle not in ('PHOTON', 'NEUTRON'):
        raise ValueError('Expected PHOTON or NEUTRON')
    species = particle.lower()
    particles = species + 's'
    if output.exists():
        raise ValueError(f'Output already exists: {output}')
    sources = [geometry] + [p for t in tables for p in (t, t.with_name(t.name.replace('_tab.lis', '_sum.lis')))]
    hashes = {str(p.resolve()): sha(p) for p in sources}
    config = read_input(geometry, particle)
    area = config['area_cm2']
    boundary = tuple(next(n for n, name in config['regions'].items() if name == r)
                     for r in ('ALCASE', 'VACREG'))
    selected_units = {int(re.search(r'_(\d+)_tab\.lis$', str(t))[1]) for t in tables}
    expected = {name for name, d in config['detectors'].items() if d['unit'] in selected_units}
    seen = set()
    rows = {'delayed': [], 'prompt': []}
    checks = []
    for table in tables:
        spectra = read_spectra(table)
        summary = read_summary(table.with_name(table.name.replace('_tab.lis', '_sum.lis')))
        for name in sorted(set(spectra) & expected):
            if name in seen:
                raise ValueError(f'Duplicate photon detector: {name}')
            seen.add(name)
            d, s = config['detectors'][name], summary[name]
            if not (s.get('one_way') and s.get('current') and s.get('boundary') == boundary
                    and s['divisor'] == d['divisor']):
                raise ValueError(f'Input/summary scoring mismatch: {name}')
            bins = spectra[name]
            if len(bins) != d['count']:
                raise ValueError(f'Wrong energy bin count: {name}')
            prompt = d['cooling_s'] is None
            if particle == 'NEUTRON' and not prompt:
                raise ValueError('The neutron exporter requires prompt detectors')
            kind = 'prompt' if prompt else 'delayed'
            integral = rounding = 0.
            for i, (printed_lo, printed_hi, value, err, bound) in enumerate(bins):
                lo, hi = d['edges'][i:i+2]
                if not (math.isclose(printed_lo, lo, rel_tol=.00051)
                        and math.isclose(printed_hi, hi, rel_tol=.00051)):
                    raise ValueError(f'Input/table energy grid mismatch: {name}')
                # Use unrounded input-defined bin edges; tables round their printed edges.
                differential = value*d['divisor']/1000
                count = value*d['divisor']*(hi-lo)
                integral += count
                rounding += bound*d['divisor']*(hi-lo)
                scale = config['beam_rate_per_s'] if prompt else 1.
                row = dict(detector=name, cooling_time_s=d['cooling_s'],
                           grid='linear_fine' if d['mode'] == 1 else 'log_broad',
                           energy_low_MeV=lo*1000, energy_high_MeV=hi*1000,
                           escaping_photons_per_s_per_MeV=differential*scale,
                           escaping_photons_per_s_in_bin=count*scale,
                           surface_average_outward_current_photons_per_cm2_s_MeV=differential*scale/area,
                           surface_average_outward_current_photons_per_cm2_s_in_bin=count*scale/area,
                           relative_statistical_error_percent=err,
                           absolute_statistical_error_photons_per_s_in_bin=count*scale*err/100)
                if prompt:
                    row.update(escaping_photons_per_primary_per_MeV=differential,
                               escaping_photons_per_primary_in_bin=count)
                rows[kind].append({key.replace('photons', particles): v for key, v in row.items()})
            total = s['total']*d['divisor']
            if abs(integral-total) > rounding+abs(total)*3e-7:
                raise ValueError(f'Integrated spectrum/summary disagreement: {name}')
            checks.append(dict(detector=name, cooling_time_s=d['cooling_s'],
                               basis=f'{particles}/primary' if prompt else f'{particles}/s',
                               table_integral=integral, summary_integral=total,
                               relative_difference=abs(integral-total)/total if total else 0.,
                               table_rounding_bound=rounding,
                               relative_statistical_error_percent=s['error']))
    if not seen or seen != expected:
        raise ValueError(f'Incomplete photon detector coverage: {expected-seen}')
    if any(sha(Path(p)) != digest for p, digest in hashes.items()):
        raise ValueError('A photon source changed during export')
    output.mkdir(parents=True)
    for kind, bins in rows.items():
        if bins:
            write_csv(output/f'{species}-escaping-{kind}.csv', list(bins[0]), bins)
    write_csv(output/f'{species}-detector-checks.csv', list(checks[0]), checks)
    metadata = dict(source_sha256=hashes, surface_area_cm2=area,
                    area_formula='2*pi*r*(r+length), complete closed RCC outer case',
                    beam_rate_per_s=config['beam_rate_per_s'], irradiation_s=config['irradiation_s'],
                    cooling_times_s=config['times'] if particle == 'PHOTON' else [],
                    source_current_microA=config['beam_rate_per_s']*1.602176634e-13,
                    scoring=f'one-way {species} current, ALCASE -> VACREG; not inverse-cosine-weighted fluence',
                    normalization='Undo scoring area divisor; delayed scores already photons/s; prompt rate scaled by source beam rate.',
                    overlapping_grids=('Fine and broad grids are alternatives. Never add them together.'
                                       if particle == 'PHOTON' else 'One prompt neutron energy grid.'),
                    energy_edges='Reconstructed from input linear/log grids to avoid rounded tab.lis boundaries.',
                    zero_bins='Preserved; zero scored photons does not establish physical absence.',
                    rows={kind: len(bins) for kind, bins in rows.items()},
                    files_sha256={p.name: sha(p) for p in output.glob('*.csv')})
    (output/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    (output/'README.md').write_text(f'''# Outer-case escaping photons

One-way ALCASE -> VACREG photon current across the complete outer case.
Case area: {area:.12g} cm², including the cylindrical side and both end caps.
Energy is MeV; cooling time is seconds after the end of irradiation.

The delayed CSV gives **photons/s/MeV** and **photons/s per energy bin**.
Surface-average outward-current columns give **photons/(cm² s MeV)** and
**photons/(cm² s) per energy bin**, averaged across the complete case surface.
They are current densities, not inverse-cosine-weighted scalar fluence rates.
The current scoring in this run cannot supply true scalar fluence. It would
require an additional fluence estimator in a future approved simulation.

The prompt CSV also retains **photons/incident proton/MeV** and
**photons/incident proton per bin**. Its per-second columns use the source beam
rate ({config['beam_rate_per_s']:.12g} protons/s); delayed rates already include
the irradiation/decay normalization and are not multiplied by current again.
Prompt emission occurs during irradiation and is not an extra post-irradiation
cooling-time point. Delayed values are instantaneous rates at each cooling time,
not time-integrated fluences over the intervals between samples.

The fine linear grid and broad logarithmic grid overlap: choose one; never add
them. Angle-integrated tables are used once, with no extra solid-angle factor.
Relative errors are percent; absolute bin-rate errors are photons/s. No errors
are combined across detectors or bins. No new simulation was launched.
Source/output hashes and normalization details are in metadata.json.
''')
    if particle == 'NEUTRON':
        (output/'README.md').write_text(f'''# Prompt neutrons exiting the outer case

Detector PRNTOT, USRBDX output unit 24, ALCASE -> VACREG, one-way current.
Energy is MeV. These are prompt emissions during irradiation, with no cooling
time assigned. The spectrum covers the input-defined energy range in 600
logarithmic bins for v6, from 1e-11 to 50 MeV.

`escaping_neutrons_per_s_per_MeV`: neutrons/(s MeV), whole case.
`escaping_neutrons_per_s_in_bin`: neutrons/s in each energy bin.
Surface-average columns: neutrons/(cm² s MeV) and neutrons/(cm² s) per bin.
Per-primary columns: neutrons/incident proton/MeV and neutrons/incident proton
per bin. Rates use the actual source beam rate, {config['beam_rate_per_s']:.12g}
protons/s (~{metadata['source_current_microA']:g} microA).
Case area is {area:.12g} cm², including both caps and the cylindrical side.

These are outward-current spectra, not inverse-cosine-weighted scalar fluence.
No irradiation-time multiplier is applied to a rate. All bins, including zeros,
are retained. Relative statistical errors are percent; absolute bin-rate errors
are neutrons/s. Angle-integrated data are used once, with no extra solid-angle
factor. Detector-total checks and source/output hashes accompany this export.
Original input and results are unchanged. No new simulation was launched.
''')
    print(f'Exported {particles}: {metadata["rows"]}; case area {area:.9g} cm²; {output}')


def export_photons(tables, geometry, output):
    return export_particles(tables, geometry, output, 'PHOTON')


def export_prompt_neutrons(table, geometry, output):
    return export_particles([table], geometry, output, 'NEUTRON')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table', type=Path)
    parser.add_argument('output', type=Path, help='New output directory')
    parser.add_argument('--input', type=Path, required=True, help='Matching run input')
    parser.add_argument('--prompt-table', type=Path, help='Optional unit-24 prompt table')
    args = parser.parse_args()
    try:
        export_photons([args.table]+([args.prompt_table] if args.prompt_table else []), args.input, args.output)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Photon export refused: {error}\n')


if __name__ == '__main__':
    main()
