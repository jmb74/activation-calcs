# V6 prompt neutrons and prompt detector identification

`scripts/export-prompt-neutrons.py` now exports the outer-case neutron spectrum
using the shared boundary/grid/normalization helpers in the working reader
`working/readers/export_photons.py`. The photon interface is preserved.

| Unit 24 detector | Name | Scored particle |
|---:|---|---|
| 1 | PRNTOT | Prompt neutrons |
| 2 | PRPTOT | Prompt protons |
| 3 | PRGTOT | Prompt photons |

All three are one-way current detectors on ALCASE -> VACREG (numeric regions
3 -> 2), covering the complete outer case. In Flair, select the processed unit
24 data and then PRNTOT or PRGTOT. These prompt detectors describe radiation
while the beam is on; the GnnnLTOT/GnnnBTOT detectors on unit 38 describe decay
photons at cooling times after irradiation. They do not supply a combined
prompt-plus-activation-photon spectrum during irradiation.

Executed command (existing inputs/results unchanged):

```sh
python3 -B scripts/export-prompt-neutrons.py \
  working/cycloinv_target2_cleanv6_24_tab.lis \
  results/v6-outer-case-prompt-neutrons-20261031-validated \
  --input working/cycloinv_target2_cleanv6_01.inp
```

The export executable is installed `python3`; no simulation or aggregation is
launched. For any future approved simulation, retain the selected
`/usr/local/fluka/bin/flukadpm`. Its extra DPMJET/RQMD models are unnecessary for
the v6 24.4 MeV primary protons. No physics or scoring settings were changed.

The CSV has **600 logarithmic energy bins**, approximately 1e-11 to 50 MeV.
Energy edges are input-defined; spectral values are from the angle-integrated
USXSUW table. No extra 2π/4π factor is applied. Units:

- Whole-case differential rate: **neutrons/(s MeV)**.
- Whole-case rate per energy bin: **neutrons/s**.
- Surface-average outward current: **neutrons/(cm² s MeV)**, or
  **neutrons/(cm² s)** per bin, using the full 21.5261928624 cm² case area.
- Per-primary columns: **neutrons/incident proton/MeV** or
  **neutrons/incident proton** per energy bin.
- Relative statistical error: percent; absolute bin-rate error: neutrons/s.

The source v6 current is **200 microA**, with beam rate
1.2483018148922e15 protons/s. The prompt rate is yield/proton multiplied by
that rate, with no multiplier for irradiation duration. It has no cooling-time
coordinate. These are outward-current spectra, not scalar fluence rates.

PRNTOT's independent summary yield is **0.0026369956 neutrons/proton**,
equivalent to **3.29176639334e12 escaping neutrons/s** at the v6 beam rate,
with summary relative statistical error **0.1566958%**. The rounded spectral
integral differs from that total by 0.001721%, within its printed-rounding bound.
All CSV rate conversions and source/output hashes were verified. Eight reader
regression tests pass, including neutron selection without photon contamination.
The final output directory is the `-validated` directory above; an initial
export is preserved in the directory without that suffix.

Primary evidence: `working/cycloinv_target2_cleanv6_01.inp` scoring definitions
and `working/cycloinv_target2_cleanv6_24_sum.lis` detector metadata. Scoring
interpretation follows *FLUKA Manual 4-5.2*, section 7.22.88 USRBDX,
`/usr/local/fluka/doc/FLUKA_Manual.txt:20923`, especially WHAT(1), WHAT(6), and
Notes 1/9 on angle-integrated USXSUW tables. Generated exports stay in ignored
`results/`; the original inputs, raw outputs and earlier photon exports remain
unchanged.
