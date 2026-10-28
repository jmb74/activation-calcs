# Pm-147 origin check, 2026-10-26

No input or result was changed. Pm-147 is present in the original processed
FLUKA table, not introduced by the CSV exporter. The target row has A=147,
Z=61, m=0; direct production Y4 is zero for Pm-147. Original activity rows are
in `working/cycloinv_6061_1m_22_tab.lis` at lines 3551, 8593, 12912 and 16872.

| Cooling | Target Nd-147 Bq | Target Pm-147 Bq | Pm statistical error |
|---|---:|---:|---:|
| Shutdown | 57,877,000 | 156,820 | 16.10% |
| 1 h | 57,852,000 | 158,560 | 16.10% |
| 1 d | 54,461,000 | 197,380 | 16.10% |
| 7 d | 37,290,000 | 392,980 | 16.11% |

The observed behavior is consistent with the beta-decay chain
Ba-147 -> La-147 -> Ce-147 -> Pr-147 -> Nd-147 -> Pm-147 -> Sm-147.
Current NNDC ENSDF adopted data give Nd-147 about 11.03 days and Pm-147
2.6234 years, each beta-minus decaying. This lets Nd feed Pm during cooling,
while Pm loses little activity over a week. References:

- https://www.nndc.bnl.gov/ensnds/147/Nd/adopted.pdf (March 2022 evaluation, p. 1).
- https://www.nndc.bnl.gov/ensnds/147/Pm/adopted.pdf (March 2022 evaluation, p. 1).

The direct target tallies include these mass-147 precursor yields:

| Nuclide | Nuclei/primary | 40-million-history unweighted-event equivalents |
|---|---:|---:|
| Ba-147 | 2.5e-8 | 1 |
| La-147 | 1.25e-7 | 5 |
| Ce-147 | 2.5e-7 | 10 |
| Pr-147 | 2.0e-7 | 8 |
| Nd-147 | 5.0e-8 | 2 |
| Total | 6.5e-7 | 26 |

This is a sparse precursor population. Individual direct precursor errors range
from 31% to 99%; the evolved target Pm-147 score reports about 16%. These are
sampling errors, not uncertainties in the fragment-production model.

The output explicitly records proton-induced fission: the first cycle lists
4.2e-5 high-energy fissions per primary, all from protons, at
`working/cycloinv_6061_1m_01001.out:9664`. Across all 40 cycle summaries there
are 1825 fission-event equivalents (mean 4.5625e-5/primary). Production of
neutron-rich mass-147 fragments from the heavy Ra target, followed by beta decay,
is therefore the supported physical interpretation. The existing scores do not
record the parent reaction of each individual fragment; assigning every precursor
to a specific fissioning parent/channel remains an inference, not an event-tag audit.

An independent two-member Nd -> Pm post-shutdown Bateman check, initialized with
the actual shutdown activities, reproduces the Pm scores to about 0.12% over a
week. The effective Nd decay constant was estimated from the shutdown/seven-day
Nd scores (effective half-life 11.0375 days, including small precursor feeding).
Using Pm half-life 2.6234 years gives predicted Pm activities 158557, 197272 and
392527 Bq at 1 h, 1 d and 7 d versus 158560, 197380 and 392980 Bq from FLUKA.
This verifies the ingrowth interpretation, not the nuclear production yield.

For scale, 156820 Bq is 0.157 MBq, about 4.57 ng of Pm-147 using the evaluated
half-life and nominal atomic mass 146.915 g/mol. At seven days, 392980 Bq is about
11.45 ng. Activity values in Bq are not atom counts or masses.

The small Pm-147 contribution assigned to HAV2 is 6029 Bq at shutdown and
15113 Bq at seven days, with 99% statistical error. Its direct precursor is
Ce-147 at 2.5e-8/primary (one unweighted-event equivalent). The region/transport
origin of that individual contribution is not established by the current scores;
it should not be interpreted as independently demonstrated production in Havar.

The MCNP direct-residual table has zero Pm-147; that is not inconsistent with
zero FLUKA direct Pm production followed by nonzero FLUKA daughter activity.
FLUKA Manual 4-5.2, section 7.22.66 RESNUCLEi note 7,
`/usr/local/fluka/doc/FLUKA_Manual.txt:18449-18455`, distinguishes produced
residuals from cooling-linked activity. Absolute mass-147 fission yields remain
unbenchmarked, and the previously recorded decay diagnostics remain unresolved.
