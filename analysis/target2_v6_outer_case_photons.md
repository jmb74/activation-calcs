# V6 outer-case photon energy/time export

Updated `scripts/export-gamma-cooling.py` to use the working reader in
`working/readers/export_photons.py`. The old reader expected two separate case
and front surfaces; v6 uses one full ALCASE -> VACREG boundary. The exporter
now validates that boundary, the one-way current scoring mode, area divisor,
binning, and DCYSCORE cooling-time association against the run input and summaries.
It derives the closed case area from the input RCC outer body: radius 1.2 cm,
length 1.655 cm, full external area **21.5261928624 cm²**.

## Run and outputs

```sh
python3 -B scripts/export-gamma-cooling.py \
  working/cycloinv_target2_cleanv6_38_tab.lis \
  results/v6-outer-case-photons-20261031 \
  --input working/cycloinv_target2_cleanv6_01.inp \
  --prompt-table working/cycloinv_target2_cleanv6_24_tab.lis
```

This command was executed. Outputs:

- `photon-escaping-delayed.csv`: 122,400 energy/time rows, all 34 cooling times.
- `photon-escaping-prompt.csv`: 600 bins for photons during irradiation.
- `photon-detector-checks.csv`: comparisons against all 69 summary detector totals.
- `metadata.json`: input/output hashes, area, normalization and source beam rate.

The RESNUCLEi entry point also accepts `--photon-tables` to produce both packages
in one operation, using a **new** output directory:

```sh
python3 -B scripts/process-rn-tab.py \
  working/cycloinv_target2_cleanv6_21_tab.lis \
  working/cycloinv_target2_cleanv6_22_tab.lis \
  --input working/cycloinv_target2_cleanv6_01.inp \
  -o results/NEW_EXPORT_DIRECTORY \
  --photon-tables working/cycloinv_target2_cleanv6_38_tab.lis \
                  working/cycloinv_target2_cleanv6_24_tab.lis
```

This optional combined command writes photon results into `photons/`. Existing
output directories are refused. No simulations or aggregation utilities run.
The executable for these exports is the installed `python3`. A future approved
simulation should retain the selected `/usr/local/fluka/bin/flukadpm`; its extra
DPMJET/RQMD models are unnecessary for the v6 24.4 MeV primary protons.

## Units and use

| Column | Unit |
|---|---|
| `energy_low_MeV`, `energy_high_MeV` | MeV |
| `cooling_time_s` | seconds after irradiation ends |
| `escaping_photons_per_s_per_MeV` | photons/(s MeV), integrated over the complete case |
| `escaping_photons_per_s_in_bin` | photons/s in that energy bin |
| `surface_average_outward_current_photons_per_cm2_s_MeV` | photons/(cm² s MeV) |
| `surface_average_outward_current_photons_per_cm2_s_in_bin` | photons/(cm² s) in that energy bin |
| `relative_statistical_error_percent` | percent |
| `absolute_statistical_error_photons_per_s_in_bin` | photons/s |

V6 scores **outward photon current**, which counts outward surface crossings.
Scalar fluence scoring has an additional inverse-cosine weight and cannot be
reconstructed from these current spectra. The area-normalized columns are
surface-average outward current densities. True scalar fluence rates would
need an additional estimator in a future approved simulation; no scoring or
physics settings were changed here.

Delayed results are instantaneous rates at the specified cooling times, not
fluence integrated over the intervals between cooling times. They already
incorporate the v6 200 microA, seven-day irradiation. Prompt columns also retain
photons/incident proton/MeV and photons/incident proton per bin; their rate
columns use the actual input beam rate 1.2483018148922e15 protons/s. Prompt
emission occurs during irradiation and is not added to a post-irradiation spectrum.
This export adds no initial-source Ra-226 or pre-existing daughter radiation.

The fine grid has 3000 linear bins from 0.001 to 3.001 MeV; the broad grid has
600 logarithmic bins from 0.001 to 30 MeV. They overlap and must **not** be added
together. Solid angle is already integrated in the selected USXSUW tables;
no additional 2π or 4π multiplier is applied. The scoring divisor of 1 is undone
to obtain whole-case photon rates before dividing by the real case area.
Printed spectrum values are converted from per GeV to per MeV by dividing by
1000. Input-defined exact linear/log bin edges avoid the rounding of printed
table boundaries when integrating each energy bin. All bins, including zeros,
are retained.

## Verification

All 69 spectrum integrals agree with their independent summary totals within
the bounds from the last printed digits of the spectral values. The maximum
relative discrepancy is **0.000159775 (0.01598%)**. CSV counts, cooling-time
coverage and all source/output hashes were verified. Seven reader regression
tests pass, including unit conversion, non-unit scoring area, prompt current
scaling, angular-table exclusion, missing-bin rejection and refusal to label a
fluence estimator as current. Earlier inventory tests also remain passing.
Generated files are under ignored `results/`; inputs/raw data are unchanged.

Primary references inspected: *FLUKA Manual 4-5.2*, section 7.22.88 USRBDX,
`/usr/local/fluka/doc/FLUKA_Manual.txt:20923` (current/fluence distinction at
20968; area normalization at 21009; single-differential USXSUW tables at 21079),
and section 7.22.65 RADDECAY, Note 7 at 18207 (activation scores per unit time).
