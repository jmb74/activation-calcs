# 400 microA correction and combined cooling-time products

The user corrected the supplied condition from 40 to **400 microA** and authorized
using a factor-of-ten rescaling of the existing results for an initial estimate.
The current condition is now 30 MeV, uniform 1 cm-radius protons, 3 mm water,
200 mg Ra-226 as RaCl2, 400 microA continuously for seven days. AGENTS.md has been
updated; historical 40 microA inputs, outputs and export packages are preserved.

## Updated simulation setup

Use `working/cycloinv_400uA_1m.flair` and its companion input.
RATE is **2.4966036e15 protons/s**. The full target/material/transport/scoring
configuration and four cooling slots are retained. The copied project retains
all 20 geometry/data plot definitions; data paths and eight run names use the
new basename. Stored process IDs, start times and run status are cleared. Seeds
54227137 (default) and 54227138..54227145 (variants) are fresh for a future
independent run. Histories remain 1 million/cycle; no costly increase is applied.

The recommended executable remains the selected **flukadpm**. It is explicitly
selected on the default run and inherited by the family in Flair. The additional
DPMJET/RQMD models are not needed for this 30 MeV proton beam, so retaining this
executable is for consistency, not an accuracy upgrade. Installed Flair static
validation passes after save/reload. All effective run commands were inspected
with Flair's family-executable propagation and use `rfluka -d`; none was executed.
For a future run, use a fresh ignored results directory and retain the input and
executable identity with its results. The original 40 microA project is unchanged.

## Why tenfold scaling includes decay and daughter ingrowth

For fixed geometry, material composition and transport, let y be the nuclide
production vector per proton and M the decay/branching matrix. With zero initial
irradiation-produced population:

    dN/dt = M N + I(t) y

Scaling the entire irradiation-current profile I(t) by ten scales N(t) and
lambda*N(t) by ten at every irradiation and cooling time. This holds for coupled
daughter chains and saturation as well as a single isotope. For the latter:

    A(T,t) = I*y * (1 - exp(-lambda*T)) * exp(-lambda*t)

The decay/saturation factors are independent of I. The current deck evolves
radioactivity analytically without updating material composition or temperature
from the accumulated irradiation. A rerun solely changing RATE would implement
the same linear correction with a new Monte Carlo sample, not introduce a
nonlinear decay-rate effect.

This is a property of the present model, not a guarantee that physical heating,
burnup, secondary irradiation of the accumulated inventory, or density/geometry
changes are negligible in the real target at 400 microA. Such effects require an
explicit model/assessment; merely changing RATE in a rerun does not add them.
Initial Ra-226 and pre-existing daughters are independent source terms and must
not be multiplied by this current factor.

FLUKA Manual 4-5.2, `/usr/local/fluka/doc/FLUKA_Manual.txt`:
- Section 7.22.38 IRRPROFIle, lines 12177-12306: intensity in primaries/s and
  irradiation intervals.
- Section 7.22.64 RADDECAY, lines 18152-18174 and 18198-18212: analytical
  decay/daughter evolution and cooling-time weighting.

The linear-scaling statement above is a mathematical consequence of that
fixed-coefficient production/decay model. Supporting CERN forum explanation of
analytical Bateman evolution (advice, secondary to the installed manual):
https://fluka-forum.web.cern.ch/t/question-about-raddecay-modes/3171

## New product-table layout

`results/decay-products-wide-400uA-scaled-20261026/` contains seven CSVs:

- ALCASE.csv, HAV1.csv, WAT.csv, HAV2.csv, TGT.csv.
- all-components-by-region.csv: preserves component identity.
- all-components-summed.csv: isotope/state sums across the intact apparatus.

Each isotope/state has one row, with **activity_0s, activity_3600s,
activity_86400s, activity_604800s**, all in **Bq**. The statistical-upper-bound
column is removed. Per-component relative errors and absolute statistical errors
are retained as separate time-specific columns. Relative errors are unchanged;
absolute statistical errors scale by ten. The summed table has no aggregate
error because regional covariance is unavailable. No isotope cutoff is applied;
nonzero source entries are retained and unprinted/zero time cells are filled
with zero activity and blank uncertainty.

These are **400 microA estimates scaled from the completed 40 microA run**, not
new simulation results. metadata.json states source/output current, factor ten,
source hashes, cooling times and output hashes. No extra irradiation, decay or
beam multiplier should be applied to these tables. They include irradiation-
produced daughters but exclude original Ra-226 and pre-existing daughter activity.
The combined component sum assumes all components remain present, including water.

Selected target activities (GBq), illustrating the scaling:

| Nuclide | 0 s | 3600 s | 86400 s | 604800 s |
|---|---:|---:|---:|---:|
| Ac-225 | 20.722 | 20.675 | 19.634 | 14.239 |
| Pm-147 | 0.0015682 | 0.0015856 | 0.0019738 | 0.0039298 |

The exporter uses the corrected shared `fluka-util.process_rn_tab` parser, checks
the declared source current against the summary, and rejects mislabeled source
currents. It checks every region/time total, component summation, CSV round trips,
isomer identity and unchanged source hashes. Four regression tests pass, including
an independent coupled Nd/Pm Bateman calculation demonstrating tenfold scaling
while daughter activity increases during cooling. The wide CSV values were also
checked directly against the completed-run export.

Reproduce the estimate (use a new output directory):

```sh
python3 -B scripts/export-cooling-products.py working/cycloinv_6061_1m_22_tab.lis --summary working/cycloinv_6061_1m_22_sum.lis --source-current-ua 40 --target-current-ua 400 -o results/new-wide-400uA-estimate
```

For newly simulated 400 microA data, use its matching table and summary with
`--source-current-ua 400` and omit `--target-current-ua` (factor one).

## Recommendations for the next refinement

1. **Resolve the decay diagnostics and material-fit warnings.** Preserve and seek
   a specific CERN explanation of ITCURR/BRBETP/BRBETM/BRALPH messages before
   accepting detailed shutdown spectra. Do not alter branching ratios or disable
   fission simply to remove unexpected products such as Pm-147.
2. **Increase histories only if rare products matter to the intended comparison.**
   Ac-225 already has about 2.6% sampling error. The mass-147 chain is sparse,
   with Pm-147 around 16%. About ten times the histories (400 million total)
   would nominally reduce 16% to roughly 5% if sampling remains similar. Raising
   beam current alone does not improve sampling statistics. More histories do
   not reduce nuclear-model uncertainty. No history increase/run was executed.
3. **Assess target evolution at the corrected current.** The incident beam power
   is I*30 MV = **12 kW**, ten times the former condition; only part is deposited
   in the apparatus. Retain/review the existing energy-deposition scores and
   determine whether fixed density/geometry and negligible depletion are adequate.
   This is an assessment item, not a proposed unmeasured density change.
4. **Extend high-energy photon scoring in a future scoring revision.** The MCNP
   output reports some photons beyond its 30 MeV tally ceiling, and our prompt
   photon detectors also stop at 30 MeV. A higher upper edge would check the full
   tail. Preserve the existing MCNP-comparison range as a subset. No range change
   is mixed into this current-only update.
5. **Keep the physics/target definition and original-radioactivity distinction.**
   The MCNP residual list omits important proton-library products and has a
   different salt loading/composition. It is not a reason to suppress FLUKA
   products or tune the beam energy for agreement. Add an independently specified
   initial Ra/daughter source later for total shutdown dose, with no assumed
   daughter equilibrium.

The coincident-cylinder cleanup remains on the to-do list, as agreed. No geometry,
material, beam-energy, evaporation/coalescence, cutoff or cooling-time changes
were made in this update. No simulation has been launched.
