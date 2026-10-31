# Gamma peaks versus inventory, 2026-10-27

## What unit 32 measures

Reviewed existing `working/cycloinv_gamma_30MeV_32_tab.lis`, summing only
M0GJ01–M0GJ18 (outward current), and the matching input. These are the original
48-million-primary results, not results from the newly simplified deck.
Unit 32 has no DCYSCORE association; RADDECAY=1. Therefore it scores prompt
particles, excluding radioactive-decay particles. It is not an inventory-decay
spectrum and does not include the decay component of total beam-on radiation.
The new simplified unit 32 is also prompt-only.

Authority: FLUKA Manual 4-5.2, §7.22.11 DCYSCORE, installed
`/usr/local/fluka/doc/FLUKA_Manual.txt:7853–7892`. The default explicitly excludes
decay particles; positive DCYSCORE associates decay scores with cooling times.
The full USRBDX entry was retrieved in the preceding scoring review; §7.22.88,
lines 21079–21122 documents processed single/double differential results.

The RESNUCLE production inventory helps identify products, but prompt photons
also arise from de-excitation of stable nuclei. A stable final nucleus can
produce a prompt line without appearing among the radioactive cooling inventory.
Peak energy agreement is a candidate identification, not proof of reaction
channel, emitting region or emission yield.

## Observed prompt features

Summed angle-integrated per-GeV differential currents have local maxima in
these energy intervals. Listed assignments are energy matches to independently
evaluated transitions, not emitter tags from FLUKA:

| Observed unit-32 bin, keV | Candidate/assessment |
|---|---|
| 227.0–230.1 | Strongest differential local maximum; unassigned in this review |
| 413.9–419.4 | Consistent with Al-26 416.848 keV transition |
| 839.5–850.7 | Consistent with Al-27 843.76 keV transition |
| 1012–1025 | Consistent with Al-27 1014.52 keV transition |
| 1357–1375 | Consistent with Mg-24 1368.625 keV transition |
| 1796–1820 | Consistent with Mg-26 1808.68 keV transition |
| 505.6–512.4 | Contains the electron/positron annihilation energy |

Al-6061 contains Al and Mg, and proton reactions can also produce Mg and Al
residuals. These matches support qualitative material/reaction consistency.
They do not show that the Al-26 inventory is the cause of the prompt 1809 keV
line: that same Mg-26 transition can be populated promptly by nuclear reactions.
Logarithmic bins broaden at high energy, and multiple transitions/continuum can
contribute to a bin. No aggregate statistical uncertainty was fabricated.

Do not assign the strongest ~228 keV prompt feature to Al-26m radioactive
gamma decay just because its level energy is 228.305 keV. The evaluated adopted
record identifies that state as 0+, 6.3460 s, with %EC+%B+=100; the 228 keV level
energy alone is not a gamma branch. Other candidate emitters and FLUKA's prompt
isomer/de-excitation treatment were not resolved here. The observed peak is not
established to be an error, but is not validated by this inventory comparison.

## Delayed spectra: consistency examples and a separate flag

The actual decay/inventory comparison belongs to unit 38 (total delayed gamma
spectra) or the original units 34–37 (four cooling times at the sphere).
Summing G001LA+G001LH at shutdown gives peaks at 510–511, 238–239,
583–584 and 2614–2615 keV. The inventory contains abundant positron emitters
(O-15, Si-27, Al-26m), Pb-212 (2.2630e11 Bq) and Tl-208 (9.2635e10 Bq),
consistent qualitatively with annihilation, Pb-212 decay and Tl-208 decay
features. These inventories include all five apparatus material regions.
Pb-212/Tl-208 energies refer to transitions in their daughters Bi-212/Pb-208.

However, **the very strong delayed 1014–1015 keV bin needs a separate audit**.
The printed differential spectrum integrates to approximately 1.7344e12
escaping photons/s in that single 1 keV bin. The independently evaluated
1014.52 keV line intensities for the obvious parents are about 0.02 photons
per 100 Si-27 decays (approximate) and 28.20 per 100 Mg-27 decays.
The shutdown inventory contains 1.8576e12 Bq Si-27 and 2.2886e9 Bq Mg-27.
Their simple unattenuated line-source estimate is only

`1.8576e12 * 0.0002 + 2.2886e9 * 0.282 = 1.0169052e9 photons/s`.

This does not explain a 1.7344e12 photons/s escaping bin. The estimate is a
screening calculation for two candidate parents, not a complete gamma source
reconstruction: other parents, unresolved transitions, transport contributions
and the installed FLUKA decay data remain to be audited. Do not conclude from
energy matches alone that delayed intensities or all inventory-to-radiation
conversion are validated. No input/data edits or simulations were performed.

## Independent nuclear-data provenance

NNDC ENSDF release **2026-10-01**, archive `ensdf_261001.zip`,
SHA-256 `2546aefea0190587fdf4d7ceba30eea032e44b1a070b1c3b1ff804e57e913799`.
Official archive: https://www.nndc.bnl.gov/ensdfarchivals/distributions/dist26/ensdf_261001.zip
DOI: https://doi.org/10.18139/nndc.ensdf/1845010.
Read directly from the pinned local archive; these are independent evaluations,
not certification of the data used internally by FLUKA.

Member/1-based line references:

- `ensdf.024:4387,4415`, Mg-24 adopted levels/gammas: 1368.625 keV gamma.
- `ensdf.026:2122,2132`, Mg-26 adopted levels/gammas: 1808.68 keV gamma.
- `ensdf.026:5875–5877`, Al-26 adopted levels/gammas: 228.305 keV isomer,
  half-life, spin and decay mode; `5884,5892`: 416.848 keV gamma.
- `ensdf.027:1802–1813`, Al-27 adopted levels/gammas: 843.76 and 1014.52 keV.
- `ensdf.027:2830–2843`, Mg-27 beta decay: parent, normalization NR=1,
  BR=1, and 1014.52 keV intensity 28.20(2) per 100 decays.
- `ensdf.027:2845,2864–2881`, Si-27 EC decay: dataset, parent,
  normalization NR=1, BR=1, and approximately 0.02 per 100 decays at 1014.52 keV.
- `ensdf.208:4386,4393,4410`, Tl-208 beta decay into Pb-208: 2614.511 and
  583.187 keV transitions (normalizations not used for a yield calculation here).
- `ensdf.212:544,549`, Pb-212 beta decay into Bi-212: 238.632 keV transition
  (raw relative intensity not treated as absolute photons per decay).

Inventory source:
`results/inventory-gamma-30MeV-20261027/all-regions-inventory.csv`,
filtered to cooling_time_s=0 and summed by isotope; original FLUKA table is
`working/cycloinv_gamma_30MeV_22_tab.lis`.

## Resolution versus statistics

The original unit-32 photon spectra have 600 logarithmic bins from 10 keV to
30 MeV. Bin widths are approximately 1.343% of their lower-edge energy.
The simplified directional spectra have 600 logarithmic bins from 1 keV to
30 MeV, approximately 1.733% per bin. Expanding the range without adding bins
therefore slightly coarsens their resolution in the MeV range.
Approximate widths near selected energies:

| Energy | Original unit 32 | Simplified broad/directional |
|---|---:|---:|
| 511 keV | 6.9 keV | 8.9 keV |
| 1015 keV | 13.6 keV | 17.6 keV |
| 1809 keV | 24.3 keV | 31.4 keV |
| 2615 keV | 35.1 keV | 45.3 keV |

Widths are derived from E*((Emax/Emin)**(1/600)-1); exact widths depend on the
bin containing the line. More histories reduce statistical fluctuations but
cannot separate two energies within a single bin. The existing unit-38 fine
total spectra already have 1 keV linear bins and visibly resolve numerous
narrow lines (e.g. the strong 510–511 and 1014–1015 keV features). Increasing
statistics is a separate decision based on errors in the actual bins/angles
of interest, not just total run histories.

Recommended next scoring change, not applied here: add 1 keV linear prompt
total and prompt/delayed directional photon grids over 1 keV–3.001 MeV,
matching the existing delayed total fine grid. Keep broad logarithmic grids to
30 MeV for higher-energy coverage. These grids overlap and must not be summed.
Smaller windows/finer bins can later be used for close multiplets. Finer bins
increase scoring storage and can increase statistical noise per continuum bin;
they do not change the inventory physics or establish correct emission data.
A USRBDX crossing spectrum is an escaping photon spectrum, not a simulated
spectrometer pulse-height response with detector efficiency/resolution.

A different historical scenario could also have used multigroup neutron photon
production: installed Manual 4-5.2 §10.1.2.1, lines 26845–26860, describes photons
sampled within 42 production energy groups except selected lines. That can smear
lines at their source, which finer scoring or more histories cannot recover.
The present deck explicitly uses LOW-PWXS JEFF-3.3, so the multigroup description
must not automatically be attributed to this run. Manual §10.2.3,
lines 27997–28010, describes pointwise interactions and FLUKA de-excitation.

Installed release notes also document relevant model improvements: FLUKA 4.5.0,
`/usr/local/fluka/RELEASE-NOTES:182–199`, introduced ENSDF-based thermal capture
emission for 168 isotopes and removed a crude fallback level-energy estimate
that caused spurious gamma lines. Thus old code version/library and whether a
plot is prompt or delayed matter in comparisons. This is not evidence that the
unspecified earlier scenario used a particular older model. No universal
'high-resolution gamma physics' switch is established by this review.

## Follow-up: could fission contribute?

Yes. The current run explicitly reports high-energy fission: the first cycle
`working/cycloinv_gamma_30MeV_01001.out:13292–13309` lists 3.6e-5 fissions per
incident proton, all attributed to protons in that cycle. Summing the printed
fission rates weighted by histories over all 48 cycle .out files gives 2267
fission-event equivalents / 48,000,000 primaries = 4.7229167e-5 per primary.
At the configured beam rate this is about 1.1791e11 fissions/s during irradiation.
These are model results, not benchmarked experimental cross sections or
per-event identification of the fissioning target nucleus. Assignment to Ra
is supported by the heavy target and the fragment inventory, rather than a
parent tag in these summaries. The output term 'high energy' is FLUKA's category,
not evidence for a GeV beam.

The target cooling inventory contains Br-84 (4.8978e9 Bq), Xe-135 (3.9014e9 Bq),
Ba-139 (3.2196e9 Bq), and many other fragment-mass nuclei at shutdown. Prompt
fission-fragment de-excitation can contribute to unit 32; subsequent radioactive
fragment/daughter decays can contribute to units 38/39 after shutdown. This is
beam-induced fission, not evidence of a spontaneous-fission source term.
Experimental proton-induced Ra-226 fission has been measured even at 11 MeV:
https://journals.aps.org/pr/abstract/10.1103/PhysRev.109.942 . That establishes
physical possibility, not the validity of the present simulated yield.

A screening search of the same pinned ENSDF archive for 1014–1015 keV decay
transitions with parent nuclides present in the shutdown inventory finds, among
others, As-83 (1014.0 keV, `ensdf.083:1470`), Ge-80 (1014.0 keV,
`ensdf.080:1877`) and Sb-133 (1014.41 keV, `ensdf.133:1938`). Their summed
all-region parent activities are approximately 2.42e9, 2.13e9 and 1.04e8 Bq,
respectively. The screening pooled ground/isomer parent activities only to
find candidates; it is not a state-resolved source calculation, and raw ENSDF
relative intensities were not assumed to be photons per decay. Thus the
previous two-parent estimate was incomplete; fission-derived candidates do
exist. They do not individually explain the ~1.7344e12 photons/s bin.
No complete normalized inventory-to-gamma synthesis or unique assignment of
228 keV/1015 keV peaks has been established. Scoring and physics remain unchanged
at the user's request; no simulations were launched.
