# Adversarial review, 2026-10-28

Scope: the untracked simplified input, new photon CSV exporter, and accompanying
scoring/peak-review notes created in this conversation. This is a review of those
changes, not an audit of every historical input or a validation of FLUKA's models.
No production code or simulation input was modified during this review. No
simulation was executed.

## Findings

### P2 — Truncated or incomplete spectra pass as successful exports

Location: `scripts/export-simplified-gammas.py:21–28,62–69`.

The parser ignores `# N. of energy intervals` and never verifies the number of
rows, complete energy range, contiguity or expected detector coverage. Its only
final completeness condition is that at least one output row exists.
Reproduced with a G002LTOT header declaring 3000 bins followed by just one valid
row: the CLI exited successfully and printed `Wrote 1 energy bins`.
A prematurely copied/truncated processed file can therefore become a plausible
but incomplete CSV. Integrating it underestimates radiation without a warning.

Validate each recognized detector against its declared and configured bin count,
ordered contiguous boundaries and endpoint acceptance before writing. Define
which detector groups were requested (partial unit selection can be intentional)
and require completeness within those groups. A full four-unit export should
contain 279 photon detectors: 1 prompt total, 6 prompt sectors, 68 delayed total
spectra and 204 delayed sector spectra. It should contain 249000 energy-bin rows
with the current grids. Partial exports should be explicitly identified.

### P2 — Invalid numeric data are propagated into physical results

Location: `scripts/export-simplified-gammas.py:37–54`.

`float()` accepts NaN and infinities, and there are no physical/grid checks.
Reproduced acceptance of NaN response, negative response and reversed energy
edges. The latter two produced negative `photons_in_bin`; NaN propagated to the
CSV fields. Noncontiguous energy rows were also accepted (related to finding 1).
For this positive-current scoring setup, these are invalid physical outputs.

Reject non-finite values, require 0 <= low < high, nonnegative response and
nonnegative finite uncertainty, and report filename/detector/line on failure.
Do not silently clamp corrupted values. The older `export-gamma-cooling.py`
already performs several of these checks; the new exporter regressed here.

### P2 — Output meaning depends on unverified hardcoded run configuration

Location: `scripts/export-simplified-gammas.py:14,38–53`.

Cooling times come from a Python constant, while sector solid angles come from
an assumed 30-degree geometry. Neither is checked against the run input or a
run-specific manifest. Detector names only encode an index, not elapsed time or
geometry. A valid input edit changing the second DCYTIMES value from 3600 to
5400 seconds leaves G002 detector names unchanged; the exporter still labels
those results 3600 seconds. Changing sector planes similarly leaves the angular
normalization unchanged. Unchecked changes to current/fluence mode, area divisor
or DCYSCORE association could also invalidate the name-derived interpretation.

Require the actual preprocessed run input or an immutable manifest tied to it.
Derive or validate cooling associations, scoring quantity/normalization, grids
and sector geometry. Record input provenance in export metadata. With the current
unmodified simplified input, the hardcoded time and angular values agree; the
bug is silent reuse after ordinary configuration changes.

## Checks and negative findings

- Compared source, beam position, materials/compounds, nuclear physics,
  pointwise neutron library, RADDECAY, irradiation profile, DCYTIMES, all 175
  RESNUCLE detector cards and all RESNUCLE DCYSCORE associations byte-for-byte
  against the original input. All match.
- Re-ran installed Flair 3.4-5.4 parsing/preprocessing/card validation:
  load succeeded, preprocessing returned no errors, no invalid active fields;
  283 USRBDX, 175 RESNUCLE, 16 USRBIN and 14 regions.
- Checked region construction and scoring associations. No demonstrated geometry
  partition, current-area conversion or per-GeV/per-MeV conversion regression was
  found. The six sectors cover the sphere and the common vacuum collection
  boundary preserves the material geometry. These static conclusions do not
  replace transport geometry acceptance.
- Positive DCYSCORE results are correctly kept per second; prompt CSV values are
  explicitly labelled per primary. No extra RATE, SAREA or 2*pi factor is applied.
- The known 1014–1015 keV discrepancy is a physics/data-attribution question, not
  evidence of an identified exporter conversion bug. The peak review explicitly
  limits its two-parent estimate and subsequently adds fission-product candidates.
- Fine/broad spectra and total/sector spectra overlap. Documentation warns against
  adding them; exporter retains identifying fields. No claim that rows are
  independent spectra or independent statistical samples was found.

## Remaining validation limits

No end-to-end results exist yet for the simplified deck. Original-table parser
checks used renamed detector headers and therefore do not validate new geometry,
score normalization or new-run statistical performance. A future authorized run
should compare sector sums to total broad current with consistent acceptance,
check processed detector metadata, and verify normal transport termination.

Inherited inventory limitations remain: RADDECAY WHAT(2)=1 uses an approximate
equal-sharing isomer treatment, absolute production/fission yields are not
benchmarked, and initial Ra/daughter radioactivity is not an explicit source.
These are documented baseline limitations, not newly introduced code defects.

Reference authority: FLUKA Manual 4-5.2,
`/usr/local/fluka/doc/FLUKA_Manual.txt`, §7.22.11 DCYSCORE (7853–7892),
§7.22.12 DCYTIMES (7930–7985: seconds and insertion-order indices),
§7.22.64 RADDECAY (18019–18030: approximate isomer sharing), and
§7.22.88 USRBDX (20935–21055,21079–21122: current, area and differential units).
Full DCYSCORE/DCYTIMES card entries were retrieved for this review; the full
USRBDX entry and shared workflow references were read earlier in this session.
