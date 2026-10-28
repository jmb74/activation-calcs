# Completed Al 6061 / 1 m detector run: observations and residual inventories

Review date: 2026-10-26. This review reads the user's completed/processed files;
no simulation, reprocessing, input edit or result overwrite was performed.
New CSV exports and derived summaries are under the ignored
`results/review-6061-1m-20261026/` directory.

## Completion and provenance

All **40 available cycle outputs** (8 run variants, 5 cycles each) have the FLUKA
end banner and report **1,000,000 primaries each**. The processed inventory and
spectrum headers agree on **40,000,000 primaries / weight 40,000,000**. The eight
launcher logs end with `End of FLUKA run`; there is no evidence in these saved
outputs of a simulation frozen midway. A frozen Flair display or later plotting
operation remains possible; these files cannot diagnose the GUI state.

The launcher identifies **FLUKA 4-5.2 / flukadpm**, using `rfluka -d -M 5`.
Run variants 01..08 have distinct RANDOMIZ seeds 54217138..54217145. Their five
cycles continue the respective random streams. Total tracked-particle CPU time
summed over the outputs is **9366.5 seconds (2.60 CPU hours)**; this is not wall
time because the run variants can execute concurrently.

The actual run input `working/cycloinv_6061_1m_01.inp`, echoed control cards and
material initialization were checked rather than relying on the later-saved
master input. They contain 30 MeV protons, uniform 1 cm radius, the corrected salt
geometry, and the Al 6061 recipe at 2.7 g/cm3. The output lists Ra-226 and the alloy
constituents using JEFF-3.3 at 296 K and water-bound hydrogen S(a,b). This confirms
loading/selection, not external validation of the reaction yields.

## Target residual activity

Values below are **GBq per entire target region**, after seven days at 40 microA.
They describe irradiation-produced nuclides and daughters, not the initially
loaded Ra-226 and its pre-existing decay chain. Ground/metastable states remain
separate in the full CSV. Uncertainties are FLUKA's reported relative statistical
errors; they are not nuclear-model uncertainty.

| Nuclide | EOI (GBq) | 1 h (GBq) | 1 d (GBq) | 7 d (GBq) | EOI statistical error |
|---|---:|---:|---:|---:|---:|
| Ac-225 | 2.0722 | 2.0675 | 1.9634 | 1.4239 | 2.64% |
| Ac-224 | 36.713 | 28.908 | 0.11845 | 1.3361e-16 | 1.26% |
| Ac-223 | 12.109 | 3.036e-08 | — | — | 2.15% |
| Ac-226 | 1.0837 | 1.0585 | 0.61542 | 0.020641 | 6.72% |
| Ra-224 | 23.929 | 23.971 | 20.725 | 6.6539 | 1.26% |
| Ra-225 | 0.45797 | 0.45708 | 0.43715 | 0.33068 | 5.2% |
| Ra-223 | 0.041859 | 0.041769 | 0.039412 | 0.027396 | 2.15% |
| Cl-34 | 8.8935 | 0.74828 | 7.8009e-14 | — | 2.41% |
| Cl-34-m1 | 6.151 | 1.6769 | 1.7482e-13 | — | 2.41% |

A dash means no nonzero row in the supplied processed table, not a demonstrated
absence of physical production. Very small printed values can be decay-solver
remainders, not meaningful detectable activities.

Ac-225 is predicted at **2.0722 GBq at EOI**, 1.9634 GBq after one day and
1.4239 GBq after seven days. Its reported statistical error is 2.636% at EOI
(about 0.0546 GBq), falling to 2.355% at seven days. Subsequent parent feeding is
included in the activity evolution.

The target's total irradiation-induced activity is approximately **334.54 GBq
at EOI, 216.60 GBq at one hour, 149.18 GBq at one day and 53.27 GBq at seven days**.
Do not interpret those totals as Ac-225 purity: short-lived nuclei have much
more activity per atom, and daughter activities add to the total. The EOI target
is dominated by Ac-224 and several decay-chain daughters. After seven days,
Ra-224-chain activity remains prominent even though Ac-224 itself has decayed
away in this calculation. These are activities in the modeled intact apparatus;
chemical separation or daughter/radon loss is not represented.

For direct target production, important tallies are:

| Nuclide | Nuclei / primary | Reported statistical error |
|---|---:|---:|
| Ac-224 | 0.00014705 | 1.26% |
| Ac-223 | 4.85e-05 | 2.15% |
| Ac-225 | 2.055e-05 | 2.81% |
| Ac-226 | 4.425e-06 | 6.72% |
| Ra-225 | 6.6e-06 | 5.2% |
| Cl-36 | 3.4725e-05 | 3.06% |

Ac-224 direct production is about 7.16 times Ac-225; Ac-223 about 2.36 times.
The direct-production CSV also contains stable products and stopped light
particles. It is a yield tally, not the remaining original target inventory.
Neither multiplying all yields by exposure nor converting Bq alone recovers a
complete depleted stable/radioactive atom inventory with parent feeding.

## Proton energy through the salt

PIN is HAV2 -> TGT. POUT is TGT -> ALCASE and combines the back and side exits.
Both count crossings, including secondary protons and possible recrossings;
neither is a tagged-primary transmission fraction.

| Score | Crossings / primary | Mean energy | Median | Central 90% energy interval |
|---|---:|---:|---:|---:|
| PIN | 0.9903589 | 22.605 MeV | 22.654 MeV | 22.248–22.989 MeV |
| POUT | 0.9893492 | 21.617 MeV | 21.660 MeV | 21.231–22.037 MeV |

The source is 30 MeV, but the salt sees a narrow distribution near **22.6 MeV**.
The average entry-to-exit difference is about **0.99 MeV**, comparing aggregate
crossing spectra rather than matching individual tracks. Approximately **99.63%**
of entry crossings are above 20 MeV. Only about **0.113%** are in 12–17 MeV.
This helps explain why an assessment based on an assumed 15–17 MeV salt beam
would not describe this run; it does not independently validate any channel's
excitation function. The beam, loading and alloy have changed since the earlier
30 MeV review, so the yield change is not an isolated alloy or target-mass test.
Energy moments/quantiles are approximate integrations of the printed 0.2 MeV bins.

## Radiation spectra at 100 cm

The detectors work: all 18 prompt polar bands have nonzero neutron, photon and
proton integrated scores. Summing the prompt current over the 100 cm sphere gives:

| Species | Crossings / primary | Whole-sphere average fluence rate at 40 microA (cm^-2 s^-1) |
|---|---:|---:|
| Neutron | 0.004044556 | 8.0356e+06 |
| Proton | 0.9811545 | 1.94934e+09 |
| Photon | 0.01734283 | 3.44562e+07 |

These are sphere averages, not a point detector value or dose. Proton leakage
is strongly forward directed: about **91.9%** of proton crossings are in the
first, approximately 0–10 degree band and **99.98%** in the forward hemisphere.
Consequently the sphere-average proton fluence substantially understates the
forward-band fluence. The modeled apparatus is not a full proton beam stop.
Neutron leakage is about 60.0% forward; photons about 50.6% forward.

The neutron current summed over the sphere matches the summed apparatus-surface
current to **0.0023%**; photons to **0.0047%**. Acceptance ranges differ slightly
(neutrons extend to 50 MeV at 1 m; photons start at 10 keV at 1 m versus 1 keV at
the apparatus), so these are strong consistency observations, not exact identities.
They also establish that particles are being transported beyond the 10 cm sphere;
the saved run did not treat the space to 100 cm as blackhole.

Predicted whole-sphere average **decay-photon fluence rates**, for 10 keV–30 MeV:

| Cooling | Photon fluence rate (cm^-2 s^-1) |
|---|---:|
| EOI | 8.53693e+06 |
| 1 h | 1.08855e+06 |
| 1 d | 522025 |
| 7 d | 192341 |

All delayed-neutron spectra are zero in these scores. This does not establish
that the physical Ra target has no neutron source: pre-existing decay, alpha-n
sources, spontaneous fission and detailed delayed-neutron coverage require their
own assessment. No dose conversion is performed in these detector definitions.
The 600-bin spectra can be noisy in rare-energy bins despite precise integrated
values; coarser rebinning is appropriate for interpretation. Errors on sums of
bands are not obtained by assuming independent band estimates.

## Other apparatus activation

| Region | EOI GBq | 1 h GBq | 1 d GBq | 7 d GBq |
|---|---:|---:|---:|---:|
| ALCASE | 300.44 | 1.7792 | 0.7776 | 0.36871 |
| HAV1 | 19.851 | 15.061 | 7.2607 | 3.5908 |
| WAT | 151.12 | 0.2903 | 0.02068 | 0.019138 |
| HAV2 | 26.083 | 20.139 | 8.6372 | 4.3192 |
| TGT | 334.54 | 216.6 | 149.18 | 53.272 |

Case EOI activity is dominated by Si-27 and Al-26-m1; water by O-15. Their
large EOI totals drop rapidly with cooling. Havar retains more longer-lived
activation. This is activity, not an absorbed-dose or handling-risk ranking.
The model keeps water and all components in place throughout cooling.

## Diagnostics requiring follow-up

No fatal/abort/lost-particle/geometry-error text was found in the 40 cycle outputs
or corresponding diagnostic files; every cycle reaches its normal end banner.
There are nevertheless:

- **15,039 `ITCURR,BRBETP,BRBETM,BRALPH` messages** across the diagnostic files,
  many associated with heavy radioactive nuclides. Their precise implementation
  meaning was not found in the installed manual or release notes. The field names
  suggest branching-related internal diagnostics, but that is a hypothesis, not
  a diagnosis. They should be preserved and checked with CERN FLUKA support before
  accepting detailed decay-source predictions as validated.
- Repeated **BLCCRA/BLCCRE least-square-fit warnings** during material initialization.
  In the salt, the printed maximum relative fit discrepancies are **4.3% at
  beta^2=0.21310** and **51.7% at beta^2=0.00358**, respectively. These are the
  internal fit discrepancies printed by FLUKA; **51.7% is not an uncertainty on
  Ac-225 yield**. Their impact at the tracked particle energies/cutoffs has not
  been quantified here. Similar initialization warnings appear for other media.

The stopped/frozen-display report has no identified connection to these warnings.
No input change or rerun is justified solely by assuming such a connection.
Direct-production yields and decay-linked activities should remain distinguished
when investigating these diagnostics.

## Delivered files and checks

- `activity-all-regions.csv`: 2,657 nonzero nuclide/state rows across 20 activity
  detectors, with region/cooling metadata, Bq, relative and absolute errors.
- `production-all-regions.csv`: 959 nonzero direct-production rows across 5 regions,
  including stable products, nuclei/primary.
- `target-activity.csv` and `target-production.csv`: target-only subsets.
- `regional-activity.csv`, `sphere-integrated.csv`, `sphere-bands.csv`:
  detector totals and derived angular/sphere summaries.
- `cycle-status.csv` and `review-summary.json`: completion, provenance, hashes,
  diagnostics and numerical checks.
- `run-review.png`: proton penetration, prompt sphere spectra and selected activity
  evolution. Lines between the four cooling slots are guides, not new decay solves.

Exports use the existing shared RESNUCLEi parser. The sum of printed nuclide rows
agrees with each independently printed regional total to within table rounding.
Numerical integration of the printed USRBDX tabular spectra agrees with detector
summary totals within **0.677%** (rounded printed bin edges/densities); reported
integrated leakage uses the higher-precision `_sum.lis` totals. Source processed
files and run inputs were left unchanged. Reproduce the derived review with
`scripts/review-6061-results.py` after the two all-region CSV exports exist.

Interpretation references: FLUKA Manual 4-5.2, section 7.22.66 RESNUCLEi,
`/usr/local/fluka/doc/FLUKA_Manual.txt:18330-18481` (especially notes 6–7);
section 7.22.64 RADDECAY, lines 18152–18174 (analytical decay evolution);
section 7.22.88 USRBDX, lines 20916–21232 (boundary estimators, normalization
and processed differential/integrated results). These support score semantics,
not the scientific accuracy of a particular production prediction.
