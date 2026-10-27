# Export isotope tables

The shared implementation lives in the sibling `fluka-util` repository.
`scripts/process-rn-tab.py` is a launcher, so fixes remain in one place.
If the repositories are not siblings, set `FLUKA_UTIL_DIR` to that checkout.
The new exporter requires Python 3.10+ and no third-party packages. CSV can be
opened in Excel; JSON retains structured metadata. It reads already processed
RESNUCLEi tables and does not run FLUKA or aggregate simulation cycles.

From the activation-calcs root:

```sh
python3 -B scripts/process-rn-tab.py working/cyclotron_inventory_30_22_tab.lis --detector '*R4' -o results/inventory-30mev/target-inventory.csv
python3 -B scripts/process-rn-tab.py working/cyclotron_inventory_30_22_tab.lis --detector '*R4' --isotope Ac-225 -o results/inventory-30mev/ac225.csv
python3 -B scripts/process-rn-tab.py working/cyclotron_inventory_30_21_tab.lis --detector Y4 -o results/inventory-30mev/target-production.csv
```

Each CSV has a `.metadata.json` companion listing all source detectors, including
empty ones, normalization factors and file hashes. The sibling `_sum.lis` is
automatically read to recover region numbers, cooling times and units. An explicit
`--summary` path can be supplied for one table. Without summary metadata, units,
region and cooling time remain unknown with a warning; names and filename suffixes
are not used to guess them. Table/summary identity mismatches fail clearly.
Use a fresh summary from the same processing operation: matching detector names
alone cannot establish that a summary and table came from the same run.

Columns include detector name/id, region number, cooling seconds, A/Z/m, isotope
label, value, percent relative statistical error, and absolute statistical error
`abs(value) * percent / 100`. No normalization or beam-current multiplier is
applied. Bq is reported only when the summary states activity and the normalization
factor is 1; other factors remain explicit as Bq/normalization. Direct-production
tables are labelled separately as nuclei/primary (or normalized nuclei/primary).

Ground states and metastable states retain separate identities, e.g. Cl-34 and
Cl-34-m1. No sums across detectors, cooling times, regions or files are performed.
This avoids assuming independence when combining uncertainties. By default zero
rows are omitted; `--include-zero` includes the original FLUKA grid padding too.
`--min-value` filters in the original values' units. Repeat `--detector` and
`--isotope` to select multiple names. Existing exports are protected; `--force`
replaces exports but never a source table/summary. No matches is an error.

## Validation, 2026-10-26

- Sixteen automated tests cover empty and single-row sections, marginal
  distributions, isomer states including m12, Fortran D exponents, duplicate
  names/ids, malformed data, metadata identity, units, filtering, export
  provenance and overwrite protection.
- Six real project tables (units 21 and 22 for `cyclotron_inventory`,
  `cyclotron_inventory_30` and `cycloinv_30mev`) were compared with the installed
  CERN `fluresnucle_formatter.py` v1.0. All 75 detectors and all 4,548 nonzero
  rows matched exactly in values, nuclide/state identity and absolute errors.
  Some source datasets are duplicates; this is parser validation, not independent
  simulation evidence or validation of nuclear yields.
- Ac-225 target exports reproduce 1.3496e9, 1.3466e9, 1.2783e9 and 9.2517e8 Bq at
  0, 3600, 86400 and 604800 s respectively.
- Unit definitions follow FLUKA Manual 4-5.2 §7.22.66 RESNUCLEi and §7.22.11
  DCYSCORE (`/usr/local/fluka/doc/FLUKA_Manual.txt:18330` and `:7782`). State
  handling is cross-checked against the installed formatter's
  `load_resnucle_tablis` implementation.

The original utility's experiment-specific Excel/mixing/half-life workflow is
preserved as `process-rn-tab-legacy.py` in fluka-util. The modern CLI/API replaces
the generic table-processing entry point; it does not claim API compatibility
with all legacy classes or supply new half-life/decay calculations.
