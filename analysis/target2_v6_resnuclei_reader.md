# V6 RESNUCLEi reader and export

Updated the project entry point `scripts/process-rn-tab.py` to run the working
copy in `working/readers/`. The sibling `../fluka-util` remains unchanged.
Its installed `process-rn-tab.py` is a legacy reader, and the `process_rn_tab`
module referenced by earlier project export scripts is absent on this host.
Existing simulation inputs and results are preserved.

The new reader obtains the numeric region ordering from the supplied run input,
checks every detector against that input's RESNUCLE scoring card and the summary,
and reads cooling times directly from the summary. It refuses conditional geometry;
provide an unconditional COMBNAME input. It does not infer region identity from R
suffixes or cooling times from D/G suffixes. For this run:

| Region number | Name | Component |
|---:|---|---|
| 3 | ALCASE | Aluminium housing |
| 4 | WAT | Front water layer |
| 5 | TAWIN | Tantalum window |
| 6 | CUBACK | Copper backing |
| 7 | COOL | Rear cooling water |
| 8 | TGT | RaCl2/graphite target |

## Execution and conditions

```sh
python3 -B scripts/process-rn-tab.py \
  working/cycloinv_target2_cleanv6_21_tab.lis \
  working/cycloinv_target2_cleanv6_22_tab.lis \
  --input working/cycloinv_target2_cleanv6_01.inp \
  -o results/v6-resnuclei-20261031-validated
```

Executable for this read/export operation: the installed `python3`; no simulation
or USRSUW aggregation is needed or launched. For future approved simulations,
retain `/usr/local/fluka/bin/flukadpm`, the user's selected executable. Its
additional DPMJET/RQMD models are unnecessary for the v6 primary proton energy.
No physics settings were changed.

The processed source summaries dated October 31 report **300,000,000 primaries**
for both units. The matching run input specifies **24.4 MeV**, and the activity
summary records **1.24830178e15 protons/s (~200 microA)** for **604800 seconds**.
This export preserves those actual v6 conditions with no scaling. It does not
relabel this existing run as the 30 MeV/400 microA project condition.

Unit 21 yields 6 production detectors and 845 nonzero nuclide/state entries.
Unit 22 yields 204 activity detectors and 14,761 nonzero entries: six regions
at 34 cooling times (end of bombardment, hourly through 24 hours, then daily
through ten days). `D003R4` is the target at 86400 seconds, and `D004R4` is the
target at 604800 seconds. Redundant mass/charge projections are not re-counted.

The output directory contains per-region wide CSVs, complete long CSVs with
per-state statistical errors, component-summed CSVs, regional total checks,
and source/output hashes in metadata.json. `activity-TGT.csv` and
`production-TGT.csv` are the target results. Wide activity columns are explicitly
labelled in Bq. Relative errors in the long table are percentages.

The earlier `results/v6-resnuclei-20261031` directory is the initial export;
use the `-validated` directory linked above for the final package.

## Validation and interpretation

All 15,606 nonzero states, identities, values and absolute statistical errors
agree with the installed CERN `fluresnucle_formatter.py` parser (version 1.0).
Every detector's summed table entries agree with its independently printed
summary total within a bound calculated from the last printed digit of each
nonzero table value. This accommodates the coarser printed precision of large
production yields without applying a loose blanket tolerance.

Four regression tests pass: v6 geometry/nonsequential time names, last-row
metastable preservation and normalization, truncated-table rejection, and
renumbered-geometry rejection. Run them with:

```sh
python3 -B -m unittest discover -s working/readers -p 'test_*.py' -v
```

Normalization WHAT(6)=1 in all v6 detectors means exported values cover each
whole region. Do not multiply these by the actual geometric volume. Production
values are nuclei/incident primary, not atom inventories after seven days.
Activities already incorporate the irradiation/decay calculation. Ground and
metastable states remain separate, and all printed nonzero values are retained.
No summed statistical error is fabricated because regional covariance is absent.
The initially loaded Ra-226 and its pre-existing daughters are not added by this
export. These activation products therefore do not constitute the complete
initial-plus-induced radiation source inventory.

Primary local references: *FLUKA Manual 4-5.2*, section 7.22.66 RESNUCLEi,
`/usr/local/fluka/doc/FLUKA_Manual.txt:18330` (WHAT(6) at 18392; decay-associated
Bq at 18443); installed `/usr/local/fluka/bin/fluresnucle_formatter.py`,
`load_resnucle_tablis` for ground/metastable table interpretation. The referenced
shared FLUKA skill was not available in the installed skill locations during
this session; these installed primary references were inspected directly.

Generated tables remain under Git-ignored `results/`. Reader code and this note
can be versioned; original inputs and raw outputs were not edited.
