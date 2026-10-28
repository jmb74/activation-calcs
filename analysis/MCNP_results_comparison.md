# Numerical comparison: supplied MCNP run and current FLUKA run

Compared 2026-10-26. Inputs, reference spreadsheets, MCNP output and original
FLUKA results are unchanged. No simulation was launched. The pure-radium plated
and graphite alternatives in the packet are outside this comparison, consistent
with the supplied project note asking to hold those designs for later.

## Sources and matching

The primary MCNP evidence is `reference/racl2_30MeV_good_flowandflux_fine.io`:
MCNP **6.3.0**, 500,000,000 completed histories, 2026-08-30 final output. Its echoed
input is the old 30 MeV salt case, including the original M3 composition and target
thickness. `racl2_30MeV_good_flowandflux_fine-1.i` and the previously supplied input
are identical. We use the completed output rather than assuming every workbook
represents the same calculation: `latest_08242026.xlsx`, nucleonics!A4, identifies
an earlier 205,282,281-history tally. The workbook can contain earlier/rearranged
results and is not the numerical authority for the 500-million-history comparison.

FLUKA evidence is the completed `cycloinv_6061_1m` set: FLUKA **4-5.2**, flukadpm,
40,000,000 histories. Unit 32 supplies prompt spectra and unit 21 direct nuclide
production. We do **not** compare MCNP's direct residuals to FLUKA's decay-evolved
unit-22 Bq, because they are different physical quantities.

MCNP F1/F11/F21 current and F2/F12/F22 surface fluence are compared to the summed
18-band USRBDX results at the same 100 cm sphere. MCNP segments run backward to
forward, opposite FLUKA's numbering; segment 18 maps to FLUKA band 1, etc. Photon
and neutron fluence totals are area-weighted sphere averages, not sums of
individually area-normalized bands. All comparisons below are **per proton**.

## Prompt leakage

| Particle | Quantity | MCNP | FLUKA | FLUKA / MCNP |
|---|---|---:|---:|---:|
| neutron | current (crossings/primary) | 0.00316195 | 0.004044556 | 1.279133 |
| neutron | fluence (cm^-2/primary) | 2.51624e-08 | 3.218613e-08 | 1.279136 |
| photon | current (crossings/primary) | 0.0173117 | 0.01734283 | 1.001798 |
| photon | fluence (cm^-2/primary) | 1.37765e-07 | 1.380123e-07 | 1.001795 |
| proton | current (crossings/primary) | 0.980509 | 0.9811545 | 1.000658 |
| proton | fluence (cm^-2/primary) | 7.80284e-06 | 7.807973e-06 | 1.000658 |

**Total prompt photon leakage agrees to about 0.18%; proton leakage to 0.066%.**
That agreement does not mean every spectral bin agrees: in common photon bins,
FLUKA is about 0.665 times MCNP at 10–100 keV, about 1.013 times at 0.1–1 and
1–10 MeV, and about 0.374 times at 10–30 MeV. These are integrals after approximate
rebinning of the printed FLUKA spectrum. The high-energy photon tail is small in
total count but can matter for a response-weighted calculation.

**FLUKA neutron leakage is about 27.9% higher.** Its excess is distributed over
the spectrum: approximately 1.36 times MCNP at 0.1–1 MeV, 1.25 times at 1–10 MeV
and 1.40 times at 10–50 MeV. Spectral agreement is therefore not a simple claim of
identical shapes plus a constant scale. Both calculations are forward biased:
61.11% of MCNP neutron crossings and 59.96% of FLUKA crossings are in the forward
hemisphere. Photon forward fractions are 50.28% and 50.63%, respectively. Proton
angular distributions are strongly forward and nearly identical in the plot.

At the same 40 microA source rate, the full-sphere crossing rates implied by the
prompt current tallies are approximately 7.89e11 versus 1.01e12 neutrons/s and
4.32e12 versus 4.33e12 photons/s (MCNP versus FLUKA). These are leakage source
strengths over the respective acceptance ranges, not dose rates.

### Acceptance and interpolation limits

These native integrated totals have slightly different low-energy acceptance:
MCNP's first E boundary includes an underflow interval from zero; FLUKA's spectra
start at a positive minimum. MCNP protons are actually cut off at **1 MeV**, while
FLUKA scores lower-energy protons; the MCNP output explicitly warns that nine
proton tally bins are below its cutoff. The FLUKA sub-MeV tail should not be
interpreted as a disagreement in proton physics below MCNP's transport range.
The photon tallies extend to 30 MeV and the neutron tallies to 50 MeV. MCNP has
some warnings about photons beyond the last tally bin; those are outside this
comparison rather than silently included in a source total.

The raw MCNP spectrum is bin integrated. The FLUKA processed spectrum is per GeV;
we integrate it using bin overlaps and convert to the MCNP MeV edges. This assumes
constant differential density within each printed FLUKA bin. It is an approximate
rebin, particularly across sharp lines/peaks, not an exact recovery of arbitrary
MCNP bin edges. The original 600-bin FLUKA grid and its tabular rounding remain
limits on close bin-by-bin comparisons. Whole-sphere scalar results above use
FLUKA's higher-precision summary totals, not the rebinned approximation.

## Direct target isotope production

Units: residual nuclei per incident proton, before irradiation/decay evolution.
For isotope identity matching, FLUKA ground and metastable yields are summed
because MCNP FT RES groups them. Their summed error is left unspecified where
covariance is unavailable; ungrouped FLUKA and MCNP relative errors remain in CSV.

| Target nuclide | MCNP nuclei/proton | FLUKA nuclei/proton | FLUKA / MCNP |
|---|---:|---:|---:|
| Cl-34 | 6.092e-06 | 4.9276e-05 | 8.089 |
| Cl-36 | 1.40043e-05 | 3.4725e-05 | 2.48 |
| Ra-224 | 5.96e-07 | 5.75e-07 | 0.9648 |
| Ra-225 | 6.23196e-06 | 6.6e-06 | 1.059 |
| Ra-226 | 0.000154642 | 1.85e-06 | 0.01196 |
| Ac-223 | 1.4484e-05 | 4.85e-05 | 3.349 |
| Ac-224 | 0.000162354 | 0.00014705 | 0.9057 |
| Ac-225 | 1.56e-05 | 2.055e-05 | 1.317 |
| Ac-226 | 4.426e-06 | 4.425e-06 | 0.9998 |

Ac-225 is **31.7% higher** in FLUKA; Ac-224 is **9.43% lower**; Ac-223 is
**3.35 times** MCNP; Ac-226 is approximately equal. These are substantial
channel-specific differences, not just differences in the number of histories.
The Ac-225 reported relative statistical errors are 2.815% (FLUKA) and 1.13%
(MCNP), much smaller than the raw yield difference. This does not isolate a
nuclear-model error because the physical target definitions differ.

Ra-226 itself differs by about a factor of 84 in the direct residual tally. This
must **not** be interpreted as a comparison of the 200 mg remaining target mass:
these scores count reaction/stopped residuals, not the original unreacted loading.
It is a particularly strong reason to audit treatment of unchanged-nuclide
reaction residuals before comparing aggregate residual totals. The cause of this
specific discrepancy has not been established by this review.

### Physical target mismatch

The MCNP M3 card is `88226 1 17035 0.7577 17037 0.3423`, with **1.1 Cl atoms
per Ra**, and a 129.9 micrometre layer. At 4.9 g/cm3 and radius 1 cm it contains
about **200 mg total material**, nominally **170.4 mg Ra-226 and 29.55 mg Cl**.
The corrected FLUKA target contains **200 mg Ra-226 plus 62.74 mg Cl**, in
stoichiometric RaCl2, and is 170.68 micrometres thick. Thus FLUKA has about 17.4%
more radium and **2.12 times the chlorine mass**, with different stopping and
reaction probabilities. An illustrative division of the Ac-225 ratio by the
Ra-mass ratio gives about 1.12, but this is **not a valid geometry/model correction**:
energy loss and reaction probabilities also change. Chlorine-yield ratios cannot
be judged without accounting for its large loading/composition difference.

Both models use Al 6061 with the same recipe and density, the same Havar/water
thicknesses, and a uniform 1 cm-radius 30 MeV proton disk. We preserved the
corrected FLUKA target and did not alter either input to force agreement.

## Important omission in the MCNP residual comparison

The output shows CEM model calls and proton-model treatment for Ra-226 and both
chlorine isotopes. It also explicitly loads **O-16.70h and Al-27.70h proton tables**
(output lines 803–805). The supplied MCNP 6.3.2 manual, section 5.9.18.12,
printed p. 505 (physical PDF p. 509), states that FT RES includes neutron and
model residuals but does not produce residuals from proton/photon library reactions.
That manual is newer than the 6.3.0 executable; it is supporting evidence of a
known tally limitation, not a release-matched code audit. The actual numerical
pattern is consistent with that limitation:

| Region/nuclide | MCNP nuclei/proton | FLUKA nuclei/proton |
|---|---:|---:|
| Water O-15 | 0 in the supplied tally | 5.932e-4 |
| Aluminum Si-27 | 6.0e-9 | 7.462e-4 |
| Aluminum Al-26, summed ground/isomer | 3.46927e-6 | 8.7794e-4 |

These differences are too large to treat the MCNP residual list as a complete
independent check on water/case activation. They are consistent with missing
proton-table residual contributions, rather than evidence that FLUKA should
suppress those products. Conversely, closer agreement in neutron/photon leakage
does not demonstrate completeness of a residual tally. The MCNP output also
warns that elemental cross sections may produce incorrect residuals, specifically
showing natural copper ZA=29000. Such warnings should accompany any use of the
reference inventory.

Additional MCNP warnings include Ra-226 neutron data lacking delayed-neutron and
gamma-production cross sections. Those warnings limit completeness claims; they
do not by themselves quantify the impact on the prompt comparison.

## Irradiation and cooling comparison

The supplied narrative and spreadsheet use **400 microA**, whereas this project's
confirmed FLUKA condition is **40 microA for seven days**. The comparison above
uses per-primary production/leakage and therefore avoids that tenfold source
normalization difference. Absolute Bq from the workbook must not be directly
compared with current FLUKA Bq. We retained 40 microA.

Selected inspected spreadsheet cells demonstrate independent exponential cooling:
`target_isotope_sort_october26_noonCDT.xlsx`, sheet "Sheet1", AG6 uses a saturation
factor and AH6 uses `AG6*EXP(-AE6*3600)` with a threshold; "sorting RACL2"!AN1
computes protons/s from 0.0004 A. Those observations do not certify all sheets or
formulas. There is no full coupled-daughter inventory in the supplied MCNP output.
FLUKA's cooling-linked activities include daughter ingrowth, so an MCNP direct
production table plus independent exponential cooling is not the same calculation.

The supplied note labels the desired reaction Ra-226(p,n)Ac-225. Mass/charge
balance for Ac-225 corresponds to **Ra-226(p,2n)Ac-225**; the original note was
preserved. No new assumption about beam energy was inferred from that wording.

## Shutdown and decay-product exports

We reused the corrected `fluka-util.process_rn_tab` parser through the new local
adapter `scripts/export-cooling-products.py`. It reads unit 22 and its matching
summary; it does not use the legacy experiment-specific pCi/g/dpm conversions,
old half-life lookup or independent decay functions. FLUKA has already evolved
the produced nuclei and their daughters at the requested cooling times.

S/D is provisionally interpreted as shutdown/end of irradiation. Four folders
contain **0 s, 1 h, 1 d and 7 d** inventories at the confirmed 40 microA, seven-day
exposure. Each folder has five component inventories, one file preserving all
regions, and one isotope-summed intact-apparatus inventory: **28 CSVs total**.
Bq, nuclide/state identity, cooling seconds and statistical errors are preserved;
the summed file uses a conservative upper bound on absolute error because
cross-region covariance is unavailable. Round-trip, time/region completeness,
activity conservation and source-hash checks pass.

The original Ra-226 and pre-existing daughters are not included, and no chemical
separation or component removal is assumed. These files are general inventory
CSVs, **not photon emission spectra or runnable SDEF cards**. An inventory Bq is
not a photon/s value; the existing transported delayed-photon scores offer a
separate route to a leakage source. A specific downstream source-file format has
not been inferred from the abbreviation S/D.

## Artifacts and verification

- `results/mcnp-comparison-20261026/integrated-spectra-comparison.csv`
- `results/mcnp-comparison-20261026/angular-comparison.csv`
- `results/mcnp-comparison-20261026/spectra-mcnp-bins.csv`
- `results/mcnp-comparison-20261026/residual-production-comparison.csv`
- `results/mcnp-comparison-20261026/mcnp-fluka-spectra.png`
- `results/decay-products-6061-20261026/`: per-time inventories and provenance.

MCNP parser checks reconcile each spectrum's energy bins with its printed total,
all 18 current segments with the whole-sphere score, and nuclide rows with the
printed total for each of the five cells, within printed rounding (2e-5 relative).
Source hashes are recorded in `comparison-summary.json` and decay `metadata.json`.
The chart was visually checked. No original run, input, spreadsheet or reference
was modified. FLUKA's unresolved decay diagnostics and material-fit warnings from
`analysis/6061_1m_run_review.md` still apply; agreement with MCNP is not a substitute
for nuclear-yield benchmarking or resolving those diagnostics.
