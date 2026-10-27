# Review of 30 MeV water-cooled run, 2026-10-26

The `cyclotron_inventory_30` and `cycloinv_30mev` processed files both contain
5,000,000 primaries and identical reported target Ac-225 activities. Treat these
as duplicate result sets, not independent evidence. The run output
`working/cyclotron_inventory_30_01001.out:81` confirms BEAM=-0.030 GeV;
line 294 confirms the 604800 s, 2.4966e14 p/s irradiation profile. WATER remains
assigned to WAT and Ra-226 chloride to TGT in the 30 MeV source input.

## Observed inventory

Source: `working/cyclotron_inventory_30_22_tab.lis`, target detectors D001R4–D004R4,
rows A=225, Z=89 (lines 1571, 5021, 7804, 10282).

| Cooling time | Ac-225 activity (Bq) | Activity (mCi) | Reported statistical error |
|---|---:|---:|---:|
| EOI | 1.3496e9 | 36.48 | 6.551% |
| 1 hour | 1.3466e9 | 36.39 | 6.560% |
| 1 day | 1.2783e9 | 34.55 | 6.763% |
| 7 days | 9.2517e8 | 25.00 | 8.428% |

Unit 22 is whole-region Bq because RESNUCLEi normalization WHAT(6)=1. These
activities already include the irradiation intensity and duration. Do not
multiply by beam current or target volume. FLUKA Manual 4-5.2 §7.22.66 RESNUCLEi,
`/usr/local/fluka/doc/FLUKA_Manual.txt:18383–18462`, and §7.22.11 DCYSCORE,
lines 7857–7863. Conversion uses 1 mCi = 3.7e7 Bq.

At EOI the target total is about 2.5983e11 Bq, so Ac-225 contributes only about
0.52% of total activity. Target Ac-224 alone is 2.7563e10 Bq, about 20 times
Ac-225 activity. Activities are affected by half-lives and daughter ingrowth;
they are not production-probability fractions.

The direct production table Y4 (unit 21) gives:

| Product | Nuclei/primary | Reported statistical error |
|---|---:|---:|
| Ac-226 | 4.4000e-6 | 17.01% |
| Ac-225 | 1.3400e-5 | 6.063% |
| Ac-224 | 1.1040e-4 | 2.507% |
| Ac-223 | 3.8400e-5 | 5.682% |

Thus the model produces about 8.24 times as much Ac-224 as Ac-225 directly.
The target scoring bounds include Z through 92 and A=225, Z=89 is explicitly
present; this is not an Ac-225 omission caused by the RESNUCLEi bounds.

## Observed proton penetration and energy loss

The unit-29 processed file also includes 5,000,000 primaries. Its PREG salt
integrated proton track length is 0.01297592 cm/primary, compared with the salt
thickness 0.01299 cm. PTGTRZ has 924 nonzero bins out of 1300. These establish
proton penetration, unlike the earlier 16 MeV case. The ratio of track length to
thickness is not an exact transmission fraction because scattering, secondary
protons and different path lengths contribute.

Unit 28 reports mean prompt energy deposited per incident primary:

| Region | MeV deposited/primary |
|---|---:|
| Front Havar HAV1 | 0.513981 |
| Water WAT | 6.293460 |
| Rear Havar HAV2 | 0.628956 |
| Salt TGT | 0.761943 |

Subtracting the three upstream deposits from 30 MeV gives **22.56 MeV** as an
approximate energy-budget indicator at salt entry. This is an inference, not a
measurement of the proton entrance spectrum: secondary transport and energy
exchanged between regions prevent regional deposition from giving that spectrum
exactly. The salt is thin enough that its 0.76 MeV average deposition does not
suggest a broad slowing-down interval through the 15–17 MeV range.

## Physical interpretation and limits

The expected reaction is Ra-226(p,2n)Ac-225. Published experimental work specifically
examines the near-maximum excitation-function region around 15–17 MeV:

- [Actinium isotope cross sections for 226Ra(p,xn) reactions measured at low energies](https://pubmed.ncbi.nlm.nih.gov/39182352/),
  thin-target measurements at 15.1–16.8 MeV.
- [Cross sections of the 226Ra(p,xn) reactions relevant for 225Ac production](https://www.sciencedirect.com/science/article/pii/S0969805125000046),
  measurements over 12.0–17.2 MeV around the expected (p,2n) maximum.

The likely explanation for Ac-225 being a minority product is that the salt sees
protons above that favourable region, permitting competing higher-neutron-emission
channels. This agrees qualitatively with the predicted Ac-224/Ac-223 production.
It does not prove the FLUKA excitation functions are quantitatively accurate.
No absolute yield benchmark has yet been performed. The statistical error on
Ac-225 is not an estimate of nuclear-model uncertainty.

## Prepared diagnostic, not executed

`working/cyclotron_inventory_30_diagnostic.inp` copies the actual 30 MeV input and
adds prompt USRBDX proton current spectra on unit 31:

- PIN: HAV2 -> TGT, measuring entry crossing energies.
- POUT: TGT -> ALCASE, measuring exits through the case-facing salt boundaries
  (side and back together).

Both use 0–40 MeV, 200 linear energy bins, one outgoing hemisphere, normalization
area 1. Integrating the processed current spectra gives crossing counts per
incident primary; it is not automatically a primary-only transmission fraction.
No DCYSCORE is applied. Syntax and normalization follow FLUKA Manual 4-5.2
§7.22.88 USRBDX, `/usr/local/fluka/doc/FLUKA_Manual.txt:20930–21065`.
Installed Flair preprocessing and card validation passed. No simulation was run.
Use the established `flukadpm` executable for a separately authorized diagnostic
run. Existing run inputs and results were preserved.

After checking PIN, compare measured excitation functions across the actual
target energy interval before changing physics models or interpreting the
absolute Ac-225 prediction as validated. Keep the supplied 30 MeV/water apparatus
as the reference configuration; geometry changes would be separate sensitivity
studies requiring agreement on the actual apparatus design.
