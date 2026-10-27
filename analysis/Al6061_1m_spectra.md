# Al 6061 case and MCNP-style spectra at 1 metre

Use `working/cycloinv_6061_1m.flair`, which references the authoritative native
input `working/cycloinv_6061_1m.inp`. This supersedes the pure-aluminum working
candidate for future runs. The previous candidate, MCNP input and existing
results are preserved. No simulation was launched.

## Retained configuration

200 mg Ra-226 as anhydrous RaCl2, density 4.9 g/cm3, 1 cm target radius,
170.68 micrometre salt layer; 1.5875 mm case walls and back; the existing
Havar/water stack; centered uniform 1 cm radius 30 MeV proton beam;
40 microamperes for seven days; four cooling slots; all previous physics,
isotope, activity, apparatus-surface, penetration and spatial-map scores.

## Case alloy

ALCASE now uses AL6061 at 2.7 g/cm3, with the MCNP M4 mass fractions:

| Component | Mass fraction |
|---|---:|
| Al | 0.972000 |
| Mg | 0.010000 |
| Si | 0.006000 |
| Fe | 0.004088 |
| Cu | 0.002750 |
| Cr | 0.001950 |
| Zn | 0.001460 |
| Ti | 0.000876 |
| Mn | 0.000876 |

Fractions sum to 1. This is the specific reference-deck recipe, not a measured
certificate for the actual hardware. Existing elemental materials are reused;
ZINC is added. Natural elemental isotope compositions are used, consistent with
the existing FLUKA material approach. Aluminum remains the ALUMINUM constituent;
AL6061 is a separate compound, avoiding changes to the built-in elemental material.
The new material cards precede RACL2 so existing material-range production-cut
and photonuclear settings also cover the new alloy and zinc.

This changes case activation and can change radiation fields; old pure-aluminum
results are not results for the alloy. Case geometry and density are retained.

## Detector geometry

The MCNP 100 cm-radius sphere is rotated from the +x beam convention to +z:
centre (0, 0, 0.316495) cm. Keeping the reference centre allows direct geometric
comparison; it is approximately 20 micrometres upstream of the corrected salt
midpoint. Its exact 17 segmentation-plane coordinates are copied into XYP
planes to form 18 polar bands, approximately 0-10, 10-20, ..., 170-180 degrees
with respect to the forward beam axis. The reference planes are not all exact
10-degree boundaries; their actual angles and areas are recorded in
`analysis/detectors_1m_bands.json`.

The original 10 cm vacuum world is retained for existing apparatus-surface
scores. New vacuum regions DET01..DET18 fill the space from that sphere to the
100 cm sphere. OUTDET fills the 100-110 cm shell. Blackhole absorption is moved
outside 110 cm, with a 120 cm outer geometry envelope, allowing particles to
reach the new scoring sphere. No shielding or air was introduced. New vacuum
regions have the same explicit electron/photon transport cutoffs as existing
regions. Existing material regions retain their order and numerical indices.

Each USRBDX scores **outward** DETxx -> OUTDET crossings. Spatial polar bands
come from geometry, not the scorer's angular bins: its one angular bin includes
the full outgoing hemisphere relative to the local boundary normal. This is
appropriate for leakage into exterior vacuum. MCNP F1/F2 have no explicit
one-way restriction; in this exterior vacuum configuration there is no external
material to produce return crossings.

## Scores and processing

| Unit | Scores | Time |
|---|---|---|
| 32 | Neutron, proton, photon fluence and current; 18 bands each (108 detectors) | Prompt, per primary |
| 34 | Neutron/photon fluence and current; 18 bands each (72 detectors) | Cooling slot 1, EOI |
| 35 | Same | Slot 2, 1 h |
| 36 | Same | Slot 3, 1 d |
| 37 | Same | Slot 4, 7 d |

Names `M<t><s><q><bb>` identify the scores: t=0 prompt, 1..4 cooling index;
s=N neutron, P proton, G photon; q=F fluence or J current; bb=01..18 band.
Example: M0NF01 is prompt neutron fluence in the most forward band, M3GJ18 is
photon current in the backward band at cooling index 3. These delayed scores
use the same DCYTIMES slots as the existing inventory; changing a slot changes
both sets together. Proton delayed spectra are not added.

Use USXSUW on each new binary unit across independent cycles, as for the existing
USRBDX units. Output `_sum.lis` includes energy spectra integrated over the local
outgoing solid angle and cumulative results; `_tab.lis` also contains differential
data. Do not confuse an energy-integrated result with a differential ordinate.

- F detectors use the actual spherical-band area, A=2*pi*100*(z_high-z_low),
  in cm2. Energy/angle-integrated results are band-average fluence per primary
  (prompt), or fluence rate in cm^-2 s^-1 (cooling). The F estimator includes the
  inverse-cosine weight.
- J detectors use normalization area 1: after energy/angle integration these
  give crossings per primary (prompt), or crossings/s (cooling), corresponding
  to MCNP F1 flow rather than an area-average current density.
- Sum J across all 18 bands for the whole-sphere leakage. For whole-sphere
  average fluence, use sum(A_i*F_i)/(4*pi*100^2), not sum(F_i). Divide J_i by A_i
  if a band-average outward current density is wanted.
- Multiply prompt results by RATE=2.4966036e14 protons/s for irradiation rates.
  Cooling-linked results already include the irradiation history; do not multiply
  them by current again. These decay scores concern irradiation-produced nuclei,
  not an independently specified initial Ra-226/daughter source inventory.
- FLUKA energy is GeV. Convert energy axes to MeV by multiplying by 1000; convert
  densities per GeV to densities per MeV by dividing by 1000. Bin-integrated
  fluence or crossings need no energy-unit factor.

Each spectrum has 600 logarithmic energy bins:

| Particle | Energy limits (MeV) |
|---|---|
| Neutron | 1e-9 to 50 |
| Proton | 1e-5 to 30 |
| Photon | 0.01 to 30 |

These ranges cover the reference spectral ranges (the neutron low edge is the
first explicit reference energy boundary). Native USRBDX supports regular linear
or logarithmic energy grids, rather than the MCNP arbitrary E-card edges.
The fine logarithmic grid is therefore an intentional implementation difference.
For a binwise MCNP comparison, integrate/rebin the differential FLUKA spectrum to
the MCNP edges; overlapping-bin interpolation is an approximation when grids do
not coincide. Do not compare raw differential values with MCNP integrated bins.
No MCNP DE/DF dose coefficients are copied: this change adds the requested
spectra/current detectors. Dose conversion would use the resulting spectra and
a specified response quantity.

## Verification and remaining runtime check

Installed Flair 3.4-5.4 loads the new referenced project; preprocessing returns
no errors and all card fields validate. There are 26 regions and 438 total
USRBDX detectors, below the installed 1100-detector limit in
`/usr/local/fluka/include/usrbdx.inc:53`. Original scoring records are retained.
All alloy fractions sum to 1 and band areas sum to the full sphere area.
An independent analytic evaluation of the written body/region definitions found
exactly one region at each of 66,375 sampled points inside the outer envelope;
all 18 band midpoints cross from the intended DETxx region to OUTDET at 100 cm.
These checks are not FLUKA tracking or nuclear-data acceptance.

For a separately authorized pilot, the recommended executable remains the user's
selected `/usr/local/fluka/bin/flukadpm`. Its added DPMJET/RQMD models are not
needed for this 30 MeV proton beam; selection is retained for project consistency,
not as an accuracy upgrade. Use a fresh ignored results directory and inspect
loaded alloy isotope data, geometry diagnostics, score headers/normalization,
cooling associations and statistical errors. No run is authorized by this edit.

## References

FLUKA Manual 4-5.2, `/usr/local/fluka/doc/FLUKA_Manual.txt`:

- Section 7.22.8 COMPOUND, lines 7332-7487: mass proportions and normalization.
- Section 7.22.46 MATERIAL, lines 13888-14052: density and elemental/isotope definitions.
- Section 7.22.88 USRBDX, lines 20916-21232: one-way current/fluence, detector
  area, energy/angle grids, differential normalization and USXSUW processing.
- Section 8.2.4.10, lines 24159-24210: XYP inside means z below the plane.
- Section 7.22.64 RADDECAY and 7.22.66 RESNUCLEi: cooling scoring semantics,
  as documented in the existing inventory review.

MCNP M4, sphere 9 and polar planes 20..180 are taken directly from the unchanged
`reference/racl2_30MeV_good_flowandflux_fine.i`.
