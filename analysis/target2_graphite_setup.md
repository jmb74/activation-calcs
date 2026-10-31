> Geometry update: use `working/cycloinv_target2_clean.inp` and see
> `analysis/target2_geometry_troubleshooting.md`. The old spherical/sector
> scoring geometry described below has been superseded. The case generator
> now defaults to the cleaned input.

# Target #2: RaCl2 dispersed in graphite

Authoritative new working input: `working/cycloinv_target2_graphite.inp`, copied
from the supplied/latest `working/cycloinv_target2.inp`. Both that source and all
older inputs/results are preserved. No simulation was launched.

## Geometry and operating conditions

The supplied MCNP beam axis x is mapped to FLUKA z. All lengths below are cm.

| Region | z front | z back | Material |
|---|---:|---:|---|
| FRONTAL | 0 | 0.05 | Al6061, 2.7 g/cm3 |
| WAT | 0.05 | 0.15 | Water, 1 g/cm3 |
| TAWIN | 0.15 | 0.155 | Ta181, 16.654 g/cm3 |
| TGT | 0.155 | 0.355 | Ra226 / natural C / natural Cl mixture |
| CUBACK | 0.355 | 0.555 | Cu63/Cu65, atom fractions 0.6917/0.3083, 8.96 g/cm3 |
| COOL | 0.555 | 1.555 | Water, 1 g/cm3 |

Inner radius is 1 cm. The Al6061 housing has radius 1.2 cm and ends at
z=1.755 cm, giving 2 mm side and back walls. The RCC lengths, rather than the
supplied comment saying the inner cylinder ends at copper, determine the 10 mm
rear water extent. Entrance water is now **1 mm**, superseding the old 3 mm.
Beam starts at z=-5 cm with a uniform radius-1-cm disk, +z direction and
**23.5 MeV** source kinetic energy. The 100/110 cm spheres are centered at
z=0.255 cm. Existing six angular bands are retained and recentered; the supplied
MCNP angular-cut planes do not define tallies and were not substituted for the
existing six-band scoring. The old extra 120 cm black-hole outer body is retained.
Cartesian maps are enlarged to enclose the entire new assembly.

Retained irradiation is 400 microA for seven days, RATE=2.4966036e15 protons/s,
IRRT=604800 s. Inventory physics (PRECISIO, evaporation, coalescence,
JEFF-3.3 pointwise neutrons, photonuclear switch, decay and transport cutoffs)
are inherited. Havar is replaced by the supplied Al and Ta. All original target
inventory/cooling detectors are retained; Cu and rear water inventory detectors
are added at each cooling time, inside each DCYSCORE detector range. Regional
scorers also include these new regions. No new physics-model setting was added.

## Graphite loading convention

The baseline exactly reproduces supplied density 1.9731 g/cm3 and mass fractions
Ra226=0.1623, C=0.7868, Cl=0.0509. Define partial densities, in g of constituent
per cm3 of the whole mixture:

- RARHO = 0.32023413; CLRHO = 0.10043079 (fixed).
- CRHO = 1.55243508 (variable graphite loading).
- RHOM = RARHO + CLRHO + CRHO (baseline 1.9731).

COMPOUND uses negative relative mass proportions; FLUKA normalizes these to
mass fractions. MATERIAL RHOM supplies the total bulk density. This represents a
homogeneous mixture; CRHO is not the microscopic density of a graphite grain.
In the fixed pi*1^2*0.2 = 0.628318531 cm3 target volume, baseline masses are
201.209038 mg Ra226, 63.102526 mg Cl and 975.423729 mg carbon. The supplied
rounded Ra/Cl ratio is retained, including its small deviation from exact RaCl2
stoichiometry. The Ra loading is therefore about **201.2 mg**, rather than an
imposed exact 200 mg. Changing CRHO leaves Ra/Cl masses and geometry fixed.
Changing only total density at fixed mass fractions would change the Ra loading
and would be a different experiment. No density/porosity or thermal scattering
benchmark has been performed for this homogenized material.

Use the generator below, which updates CRHO and RHOM together. For manual edits,
keep their sum consistent. EBEAM is GeV, CRHO/RHOM are g/cm3. Avoid a source
energy at or above EMAX (baseline scoring ceiling 60 MeV).

```sh
python3 scripts/make-target2-cases.py \
  --energies-mev 22 23.5 25 27 30 \
  --graphite-rho 1.2 1.4 1.55243508 \
  --output-dir /private/tmp/target2-study
```

These illustrative values create 15 separate `e##_g##/target2.inp` files and a
`cases.csv` manifest with energy, densities, masses, executable and input hashes.
They do not launch FLUKA. Output directory must be new; existing cases cannot be
overwritten. Zero graphite is also supported. Select the actual scan grid before
production work; the example grid is not an optimization result. Generated
simulation products belong in isolated directories outside Git.

## Proton energies at the target faces

Unit 31 contains four prompt, one-way USRBDX **current** energy spectra:

| Detector | Crossing | Interpretation |
|---|---|---|
| PIN | TAWIN -> TGT | Incoming protons at front face |
| POUT | TGT -> CUBACK | Outgoing protons at rear face only |
| PSIDE | TGT -> ALCASE | Lateral leakage, separate from rear exit |
| PBACK | TGT -> TAWIN | Backscatter through front face |

All use 1200 linear bins from 0 to 0.06 GeV (50 keV/bin), full outgoing
hemisphere and area divisor 1. These include all crossing protons, including
secondary protons and repeated crossings; they do not identify individual
primary trajectories. No delayed DCYSCORE is applied to these detectors.

Process unit 31 across independent cycles with installed `usxsuw` (or Flair's
USRBDX processing). For the **solid-angle-integrated single differential**
spectrum f_i in the processed output, set w_i=f_i*(Ehi_i-Elo_i).
Then sum(w_i) is crossings per source proton, and
mean E = sum(w_i*(Ehi_i+Elo_i)/2)/sum(w_i). Multiply GeV energies by 1000 for MeV.
This bin-midpoint mean is an approximation at the selected bin resolution.
If sum(w_i)=0, report no crossings; the mean energy is undefined.
Divide the per-GeV differential spectrum by 1000 for a per-MeV spectrum.
For raw double differential data, also multiply by the angular bin width
2*pi sr before integrating. Do not apply that factor again to the processed
single differential spectrum.

Compare PIN/POUT spectra and their integrated crossing yields for each case.
POUT/PIN is a rear-crossing yield ratio, not an exact primary survival fraction.
The difference of the two mean energies describes different crossing populations,
so it is not a paired mean energy loss for individual protons. Report the energy
spread and exiting yield alongside the means; a zero rear yield can indicate
that protons range out before reaching copper. Current and duration scale
inventory/activity; they do not change the per-crossing mean energy.

## Executable and validation

Recommend and retain `/usr/local/fluka/bin/flukadpm` for each separately approved
run. Its additional DPMJET/RQMD linkage is not required for 23.5 MeV primary
protons and does not itself improve this inventory calculation. Reassess if the
projectile or energy regime changes. No simulation, compilation or GUI launch
was performed for this update.

Static validation with installed Flair 3.4-5.4: baseline plus nine generated
combinations (23.5/25/30 MeV x CRHO=0/1.2/1.55243508) preprocess without errors
and have zero invalid card fields. Evaluated baseline BEAM energy is -0.0235 GeV
and mixture density is 1.9731 g/cm3. An independent analytic SPH/RCC/XYP check
sampled 45,000 points across three spatial scales (requiring one region for each
point inside the outer black-hole body), checked layer midpoints, and verified
all decay-linked inventory ranges include seven regions. These checks do not
establish FLUKA runtime geometry acceptance, nuclear-model accuracy, scoring
statistics or scientific validation. An approved isolated pilot run remains the
next validation step.

References checked against installed **FLUKA Manual 4-5.2**,
`/usr/local/fluka/doc/FLUKA_Manual.txt`:

- §6.1 preprocessor, lines 3904–4048 (numeric constants and substitutions).
- §7.22.4 BEAM, lines 6305 onward, especially 6369–6421 (circular spot).
- §7.22.8 COMPOUND, lines 7332–7487 (negative mass proportions and normalization).
- §7.22.46 MATERIAL, lines 13888–14052 (density and isotope mass number).
- §7.22.59 PHYSICS/DPMTHRES, lines 16932–17005 (extra-model thresholds).
- §7.22.88 USRBDX, lines 20920–21231 (one-way current, units, areas,
  energy bins and processing; especially 21097–21112 for integration).
- §8.2.4.4 RCC, lines 23855–23896 (base, height vector and radius).
