# Target #2 geometry troubleshooting and simplification

Use **`working/cycloinv_target2_clean.inp`**. This is a new working copy of the
current on-disk `cycloinv_target2_graphite.inp`, which remains untouched.
This note supersedes the geometry/scoring portions of `target2_graphite_setup.md`.

## Confirmed problem in the inspected input

The sphere called `world` was centered at (0,0,-28.255) cm with radius 10 cm,
while the target occupies z=0 to 1.755 cm. The region expression
`OUTVAC = +det100 -world` therefore includes the target itself: at
(x,y,z)=(0,0,0.255), both **TGT and OUTVAC** are selected. Meanwhile
`VACREG = +world -outer` describes a disconnected upstream sphere, rather than
vacuum surrounding the apparatus. The radius-100 cm `det100` sphere was centered
at z=-28 cm, so it also protrudes beyond the radius-110 cm `far` sphere centered
at z=0.255 cm. These are real overlapping/non-nested regions, not a plot
colouring issue. Earlier static checks described a previous version of the deck;
they do not validate these subsequently changed sphere positions.

## Simplified geometry

Seven bodies remain: one world sphere, two RCCs and four interface planes.
Every body is used. Removed the extra concentric scoring/black-hole spheres,
the six angular-sector regions and five angular cut planes, and the separate
front-plate plane/region. The four remaining planes are required to distinguish
water, Ta, target, Cu and rear water.

```text
SPH world   0 0 0.255 110
RCC outer   0 0 0    0 0 1.755 1.2
RCC inner   0 0 0.05 0 0 1.505 1

BLKHOLE = -world
VACREG  = +world -outer
ALCASE  = +outer -inner
```

The cavity starts at z=0.05 and ends at z=1.555 cm. ALCASE is one connected
Al6061 region comprising the 0.05 cm front plate, 0.2 cm radial wall and 0.2 cm
rear plate. Its volume is 3.21133601 cm3 (derived as outer-cylinder volume minus
cavity volume). External cylinder area is 22.28017510 cm2. The full cavity
contains WAT, TAWIN, TGT, CUBACK and COOL, with unchanged material dimensions,
densities and composition. No vacuum lies inside the housing.

The current source card is retained exactly: Gaussian x/y FWHM 0.68 cm, 23.5 MeV,
z=-5 cm. The old uniform-disk comment was corrected. Beam current, duration,
inventory physics, cooling times, target-face proton scores and loading parameters
are retained. Front/side/rear aluminum isotope inventories are combined into
ALCASE; the separate FRONTAL inventory detectors are removed. Each cooling-time
inventory range now contains six material regions.

## Gamma source boundary

Prompt total currents (unit 24) and all 34 cooling-time delayed photon spectra
(unit 38) now score **ALCASE -> VACREG**, over the whole external housing.
Area divisor remains 1: results describe total escaping current rather than
current density averaged over the housing area. The L and B spectra overlap
in energy and must not be added. Existing proton PIN/POUT/PSIDE/PBACK spectra
remain on unit 31.

This boundary includes photons produced anywhere inside the assembly that
escape through its aluminum envelope; it does not restrict production to Al.
It is a suitable boundary for an escaping gamma energy source spectrum. A full
surface source for transport elsewhere also needs emission positions and
outgoing directions, including their correlations with energy. The retained
energy histograms alone do not supply that phase-space distribution. No custom
source routine or boundary-crossing event writer has been introduced.

Legacy 1 m angular-sector spectra (unit 39) are removed along with the geometry
that defined them. Unit 24/38 spectra have changed scoring surface from a remote
sphere to the Al exterior; do not silently combine them with previous results
or use the old sector-based postprocessing. New scan cases use the corrected
input by default through `scripts/make-target2-cases.py`.

## Verification and limits

- Installed Flair 3.4-5.4 loaded/preprocessed the corrected input: no preprocessing
  errors and no invalid card fields. Evaluated source energy is -0.0235 GeV and
  baseline mixture density is 1.9731 g/cm3.
- Independent analytic evaluation of the actual SPH/RCC/XYP body definitions
  and region expressions found the old overlap at the target center. The clean
  deck selected exactly one region for each of 120,000 reproducibly sampled
  points over target, near-field and full-world scales, including exterior
  black-hole points. Layer midpoint checks passed.
- All retained bodies are referenced, all USRBDX regions exist, and each
  decay-linked RESNUCLE range includes six material regions.
- Four energy/loading cases were generated in a temporary directory, including
  zero graphite; the zero-graphite case also passed Flair card validation.
- `analysis/target2_clean_geometry.png` is an analytic section of the **actual
  parsed corrected input**, y=0, with materials labelled. It is not a screenshot
  of Flair or a FLUKA runtime geometry check.

No simulation or GUI launch was performed. Runtime geometry acceptance and
physical scoring results remain untested. Retain the recommended executable
`/usr/local/fluka/bin/flukadpm` for a separately authorized run; additional
DPMJET/RQMD linkage is unnecessary for the current low-energy proton beam.

Syntax/scoring references: installed **FLUKA Manual 4-5.2**, §8.2.4.4 RCC,
`/usr/local/fluka/doc/FLUKA_Manual.txt:23855–23896`; §7.22.88 USRBDX,
lines 20920–21231 (one-way region crossing, area normalization and spectrum
integration); §7.22.4 BEAM, lines 6369–6421 (Gaussian beam width interpretation).
These define card semantics; overlap findings and cylinder measures above are
independent geometric deductions from the inspected input.
