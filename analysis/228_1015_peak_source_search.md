# Source search for the 228 and 1015 keV features

2026-10-28. No simulation, input modification, compilation or installation was
performed. Reviewed the original 48-million-primary gamma run, not the unrun
simplified deck. Earlier two-parent screening was incomplete; this note records
the broader search and distinguishes prompt and delayed features explicitly.

## Are both delayed?

Both energy neighborhoods contain photons after shutdown, but the features
originally discussed came from different scores:

| Feature | Score originally identified | Present after shutdown? | Assessment |
|---|---|---|---|
| Strong 227.0–230.1 keV maximum | Unit 32, prompt sphere current | A separate 228–229 keV delayed feature exists | Te-132 is a strong candidate for the persistent delayed component; prompt feature is not uniquely assigned |
| Strong 1014–1015 keV spike | Unit 38, delayed current at shutdown | Yes; very large at shutdown, then nearly disappears | Later hourly component matches Mg-27; enormous initial component remains physically unvalidated |
| 1012–1025 keV prompt feature | Unit 32 | Not the same population as the delayed spike | Consistent with prompt Al-27 de-excitation |

Unit 32 has no DCYSCORE and excludes decay radiation. Unit 38 has explicit
positive cooling associations. 'Shutdown' is the instantaneous decay rate at
end of irradiation, not an average over the first hour or an integrated count.
No unit-38 samples exist between zero and 3600 seconds. The results cannot
measure the initial spike's seconds-scale half-life.

Authority: FLUKA Manual 4-5.2, §7.22.11 DCYSCORE,
`/usr/local/fluka/doc/FLUKA_Manual.txt:7853–7892`; §7.22.12 DCYTIMES,
lines 7930–7985. The full card entries were retrieved during the preceding review.

## Search scope and evidence

Verified SHA-256 of the local ENSDF archive and ran its integrity verifier.
Searched all 300 mass files in NNDC ENSDF release 2026-10-01, not just a list of
familiar nuclides. Search windows were 227–230.1 and 1013–1017 keV, covering
the original coarse prompt bin and the delayed line with neighboring bins.
For decay datasets, matched explicit parent records against the complete
five-region shutdown inventory. For adopted gammas, retained candidates even
when stable nuclei do not appear in the cooling inventory.

Found 102 matching parent/line records in decay datasets and 1176 adopted
transition records. These are records, not unique isotope counts or physical
source assignments. Multiple evaluations, multiple-parent datasets, isomers,
uncertain placements and relative-intensity normalizations remain distinct.
Qualified/non-numeric energies were not forced to numerical matches. Raw source
records and normalization records are retained in the candidate CSVs. Pooled
state activities were used only for initial ranking; they are not state-resolved
emission predictions. Normalization was inspected manually for the principal
Te-132, Mg-27 and Si-27 candidates.

Artifacts under ignored `results/peak-sources-20261028/`:

- `decay-candidates.csv`, `adopted-candidates.csv`: source records and provenance.
- `time-behavior.csv`: bin currents at every cooling time, separate face errors,
  and selected isotope activities. No covariance-free combined error is invented.
- `cooling-evidence.png`: persistent 228 keV and hourly 1015 keV behavior.
- `search_peak_sources.py`, `peak_time_analysis.py`: read-only investigation code
  copied for reproducibility (run from repository root; the latter uses the
  installed MacPorts Python with NumPy/SciPy).

The time analysis reads the original unit-38 tables directly with the existing
paired-face parser, checks detector/grid counts and energy edges, sums LA+LH,
and integrates differential per-GeV values over the 1 keV bin width. It does not
use the simplified exporter flagged in the adversarial review.

## Delayed 228 keV: strong Te-132 identification

Evaluated Te-132 beta decay populates I-132, which emits a 228.16 keV gamma.
The ENSDF relative gamma intensity 100(2) has normalization NR=0.88(3), BR=1:
approximately **0.88 photons per Te-132 decay**, not 100 photons per decay.
The parent half-life is **3.204(13) days**. This line belongs to Te-132 decay
through an excited I-132 daughter; it should not be assigned the 2.295 h
half-life of I-132's subsequent ground-state decay.

The shutdown inventory has Te-132 = **1.33891e9 Bq**: 1.2172e9 Bq in the salt
and 1.2171e8 Bq in HAV2. Regional inventory errors are 14.78% and 56.49%,
respectively. Its expected intrinsic 228 keV source is about **1.178e9 photons/s**.

| Cooling | Escaping 228–229 keV bin, photons/s | Te-132 intrinsic 228 keV estimate, photons/s |
|---|---:|---:|
| Shutdown | 3.711e9 | 1.178e9 |
| 1 h | 1.1239e9 | 1.168e9 |
| 1 d | 8.983e8 | 9.491e8 |
| 7 d | 2.6299e8 | 2.592e8 |
| 10 d | 1.4691e8 | 1.354e8 |

After the early component dies away, energy, intensity scale and days-long
behavior all support Te-132 as the dominant delayed 228 keV source. This is
strong consistency evidence, not an event-tagged proof of every photon.
The shutdown bin includes additional short-lived sources and continuum.
Candidates in this same 1 keV bin include Zn-75, Se-86, Tc-107, Ba-144, Sn-127
and others. Ac-224 has an uncertain 228 keV record; Ac-225's evaluated 228.2 keV
line is weak. Their raw records cannot be normalized indiscriminately.
The late bin slightly exceeding the Te-only estimate can reflect other sources,
statistical uncertainty and data differences; it must not be called an escape
probability greater than one.

A diagnostic nonnegative fit of the bin's time shape after 1 h to the Te-132,
Ac-225 and Ac-224 inventory curves has maximum relative residual about 1.8%.
Its fitted Te coefficient is 0.792 photons per decay. The other coefficients
are empirical time-shape components, NOT validated Ac-225/Ac-224 line yields;
in particular the fitted Ac-225 coefficient exceeds its evaluated weak line
branch. This fit only supports a dominant Te-like time dependence plus smaller
components. It is not an absolute source reconstruction or a statistical
significance test (the cooling scores are correlated).

Te-132 and related iodine fragments are consistent with the observed fission
inventory. This supports the user's suggestion for the delayed 228 keV line.

## Delayed 1015 keV: two components must be separated

The actual strong fine bin is **1014–1015 keV**, containing the evaluated
**1014.52 keV Al-27 transition**. Different parent decays can populate it.

| Cooling | Escaping 1014–1015 keV bin, photons/s | Mg-27 activity, Bq |
|---|---:|---:|
| Shutdown | 1.7344e12 | 2.2886e9 |
| 1 h | 1.0032e7 | 2.8176e7 |
| 2 h | 1.2350e5 | 3.4689e5 |
| 3 h | 1.5206e3 | 4.2710e3 |

Between 1 and 2 h, the line gives an effective half-life **567.469 seconds =
9.4578 minutes**, matching the evaluated Mg-27 half-life **9.458(12) minutes**.
The ratios bin_current/Mg27_activity at 1, 2 and 3 h are 0.356048, 0.356021 and
0.356029. This is strong evidence that the hourly component is Mg-27 decay.
The absolute ratio is above the evaluated 0.282 photons/decay for this line;
Mg-27 production has 14.83% reported error, and photon scores have additional
sampling uncertainty. The time-shape match does not certify the absolute yield.
No independent-errors significance estimate was made.

The enormous shutdown component is a separate problem. Si-27, in ALCASE, has
1.8576e12 Bq at shutdown (0.4976% inventory error), and a 4.16(4) second evaluated
half-life. The observed line is equivalent to approximately **0.934 escaping
photons per Si-27 decay** if assigned entirely to it. However, evaluated Si-27
decay gives only approximately **0.02 photons per 100 decays = 0.0002 per decay**
at 1014.52 keV. That predicts ~3.72e8 intrinsic photons/s, about **4700 times
below** the observed escaping bin. Adding evaluated Mg-27 emission gives
~1.017e9 photons/s, still about 1700 times below the bin.

Thus Si-27 is a strong candidate for the simulated short-lived component based
on energy and activity scale, but a physical Si-27 line at the reported intensity
is NOT validated. The gap in cooling times prevents a direct seconds-scale
half-life identification. Wrong/incomplete installed decay branching data or
its interpretation is a hypothesis, not a confirmed FLUKA defect. Decoding
internal binary decay data or a parent-tagged/single-isotope diagnostic is still
needed to settle that attribution.

The broader ENSDF search finds fission-product decay lines in this bin from
As-83, Ge-80, Cd-119, Ag-119, Ce-143, Sb-132/Sb-133 and others. The combined
shutdown activities of matching mass-60–170 candidate parents are only
~1.55e10 Bq, before actual line branching and attenuation. This is a useful
scale comparison, not a formal upper bound or complete decay-source solver.
Those candidates do not currently offer a convincing explanation for the
1.7344e12 photons/s spike. Fission must not simply be assumed to solve it.

Two independent scores confirm the shutdown feature's scale:

- Unit 25 physical-surface photon current: ~1.7703e12 photons/s in its broad
  965.5–1034 keV bin, after applying its physical-area divisor.
- Unit 34 sphere current: ~1.6636e12 photons/s in its 1012–1025 keV bin.

Windows differ, but these confirm it is not a unit-38 CSV-only artifact. Unit-38
shutdown line errors are 0.5439% (ALCASE face) and 0.7208% (HAV1 face), far too
small individually to explain the orders-of-magnitude discrepancy. They are not
uncertainties on the nuclear data or on the combined face sum.

## Original prompt 228 keV feature remains non-unique

The original unit-32 bin spans 227.0–230.1 keV. That is too coarse to distinguish
Te/I-related 228.16, the 228.305 keV Al-26 isomer level energy, Ra-224 228.3,
Ni-57 229.8, W-182 229.3207 and many other transitions. The adopted-data search
finds possible transitions in reaction products and fission fragments, including
I-132, Br-85, Br-86, Cd-115 and Ru isotopes. I-132's evaluated adopted dataset
even notes a ~228.5 keV prompt line observed in Cf-252 spontaneous-fission work;
that is supporting context, not a Ra-226 fission yield assignment.

A level energy is not itself a gamma branch: Al-26m at 228.305 keV is evaluated
as a 6.3460 s 0+ beta-plus/electron-capture emitter, not a documented 228 keV
isomeric gamma source. No unique physical assignment of the original prompt
peak can be justified from these coarse scores. Since prompt gammas are not
currently needed, no scoring change or additional run is proposed as a prerequisite
for the delayed-radiation analysis.

## Nuclear-data and result provenance

ENSDF release 2026-10-01, `ensdf_261001.zip`, SHA-256:
`2546aefea0190587fdf4d7ceba30eea032e44b1a070b1c3b1ff804e57e913799`.
The archive is independent of FLUKA's internal data. Raw member/line citations:

- `ensdf.132:3188–3209,3256`: Te-132 decay dataset, parent half-life,
  normalization and 228.16 keV gamma. Live NNDC counterpart:
  https://www.nndc.bnl.gov/nudat3/getdecaydataset.jsp?dsid=132te+bM+decay+%283.204+d%29&nucleus=132I
- `ensdf.027:2830–2843`: Mg-27 parent, normalization and 1014.52 keV line.
- `ensdf.027:2864–2881`: Si-27 parent, normalization, weak gamma branching.
- `ensdf.026:5875–5877`: Al-26m energy, lifetime and decay mode.
- `ensdf.132:3097–3098`, I-132 adopted dataset: Cf prompt-line observation;
  also checked against https://www.nndc.bnl.gov/ensnds/132/I/adopted.pdf .

Full candidate provenance is in the CSVs. Original spectra are
`working/cycloinv_gamma_30MeV_{25,32,34,38}_tab.lis`; inventory is
`results/inventory-gamma-30MeV-20261027/all-regions-inventory.csv` derived from
unit 22. All are preserved. No unique-emitter labels were added to simulation
outputs and no baseline physics settings were changed.
