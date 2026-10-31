# Simplified gamma and inventory scoring, 2026-10-27

Prepared `working/cycloinv_gamma_30MeV_simplified.inp` from the actual latest
file `working/cycloinv_gamma_30MeV.inp` (the request called it cycloenv).
Original input SHA-256:
`449393fa6fb0a71af095b69dcb325d62818f8e0c9bace3c99b62e0ad61ecefd4`.
Original input, Flair project, and simulation outputs were not modified.
The new standalone input is authoritative; no companion Flair project was created.
No simulation was launched.

## Evidence and decisions

Existing processed `working/cycloinv_gamma_30MeV_*_sum.lis` files report
48,000,000 primaries. Unit 25 has zero scored delayed neutron response at
shutdown, 1 h, 1 d and 7 d; all 18 delayed sphere neutron current sectors on
each of units 34–37 are also zero. Drop delayed neutron surface detectors and
four delayed neutron regional USRBINs. Zero scores do not establish an exact
physical zero or rule out rare channels at unsampled cooling times. There
were no delayed proton surface detectors to establish a measured proton zero.

Beam-on particles must be distinguished from post-shutdown radiation:
unit 32 gives summed outward sphere currents of 0.00404604 neutrons,
0.981110 protons and 0.0173877 photons per incident proton, within the old
energy windows. Prompt neutrons and protons are not negligible. Retain one
combined prompt current spectrum for each species. Preserve PIN and POUT,
which constrain the proton energies relevant to isotope production.

Gamma isotropy was checked by dividing each original spatial sector's
**current** by its solid angle (old GF detector area / 10000 cm²).
Sector currents themselves cannot be compared without this correction.
The observed full-energy-band max/min photon current per steradian is:

| Condition | Max/min |
|---|---:|
| Prompt | 1.121 |
| Shutdown | 1.213 |
| 1 h | 1.578 |
| 1 d | 1.381 |
| 7 d | 1.381 |

At 1 h, the two sectors nearest the equator give approximately 0.75–0.77
of the isotropic-average current per sr, while polar sectors give about
1.13–1.18. Individual sector statistical errors are about 1–3%, appreciably
smaller than this variation. No covariance-based significance test was made.
These are old 10 keV–30 MeV sphere photon scores; they do not establish the
angular dependence of every energy bin or the newly included 1–10 keV band.
Energy-dependent self-attenuation and the layered apparatus are plausible
causes of anisotropy, not separately demonstrated mechanisms here.

Retain six spatial polar sectors (0–30, 30–60, 60–90, 90–120, 120–150,
150–180 degrees from +z), instead of 18. This is a compact compromise, not
proof that finer angular information is unnecessary for all dose geometries.
Their solid angles are 0.841787, 2.299805, 3.141593, 3.141593, 2.299805,
0.841787 sr. Azimuth is integrated, consistent with the cylindrical apparatus
and centred circular beam. Sector location at 1 m approximates the escaping
far-field direction; it is not an exact tally of momentum polar angle.
The sphere centre remains (0, 0, 0.316495) cm. New planes use exact cosines
of 30-degree increments, removing inherited rounding/plane inconsistencies.
Detailed original-sector evidence is in ignored
`results/scoring-review-20261027/gamma-angular-review.csv`.

## Surrounding region and detector layout

Use the existing 10 cm vacuum sphere as a common collection boundary:
`VACREG -> OUTVAC`. OUTVAC is vacuum from that sphere to the 1 m sphere.
This collects escaped apparatus radiation with one region pair per spectrum,
without merging ALCASE and HAV1, whose different materials must be preserved.
There is no intervening material, so it measures apparatus leakage after
self-attenuation, transported through vacuum. The boundary is centred at the
original world origin, which does not affect its integrated collection role.
The beam starts inside it; incoming primary beam crossings are not scored.

Outside the 1 m sphere, vacuum is divided into six ANG regions extending to
110 cm. `OUTVAC -> ANG01..ANG06` scores spatial sectors at the sphere.
The blackhole shell from 110 to 120 cm is preserved. The original 17 polar
planes become five; all physical bodies and material regions are unchanged.
No actual material surface was removed. Bodies: 26 -> 14; regions: 26 -> 14.

USRBDX uses **current**, one-way outward, normalization area 1 throughout.
Duplicate surface-fluence estimates and duplicate legacy delayed photon
spectra are removed. All 175 RESNUCLE detectors and their cooling associations
are byte-for-byte preserved, including five-region production and all 34
cooling times. Physics, source, materials, irradiation profile, and physical
geometry parameters are preserved. No physics settings were changed.
The 30 MeV protons, 3 mm water, 400 microA, seven days and 200 mg Ra loading
remain. USRBIN retains prompt regional neutron/photon fluence, energy deposition,
proton regional/r-z maps, all three Cartesian particle maps, and the four
legacy activity/photon maps (16 retained USRBIN detectors).

| Unit | New contents |
|---|---|
| 21, 22 | Unchanged production and cooling inventories |
| 23, 26–30 | Retained USRBINs; unit 27 now photons only |
| 24 | PRNTOT, PRPTOT, PRGTOT: total prompt N/P/gamma currents at 10 cm |
| 31 | Unchanged PIN/POUT proton spectra |
| 32 | A000G01..06: prompt gamma spectra in six 1 m sectors |
| 38 | G001LTOT/G001BTOT through G034LTOT/G034BTOT: total delayed gammas |
| 39 | A001G01..06 through A034G01..06: delayed directional gamma spectra |

Unit 25 and units 34–37 are retired in this copy. Use a fresh output directory
so old files cannot be mistaken for new scores. USRBDX count: 574 -> 283.
All delayed directions now cover the full 34-time schedule, rather than just
four times. Total fine photon spectra retain 3000 linear 1 keV bins from
1 keV to 3.001 MeV; broad/sector spectra use 600 log bins from 1 keV to 30 MeV.
Prompt neutron window is 1e-14–0.05 GeV, proton 1e-8–0.04 GeV; these expand
some old windows. Retained PIN/POUT remain 200 linear bins over 0–40 MeV.

## Processing and normalization

Process independent cycles with installed USXSUW first. For photon CSV export:

```sh
python3 -B scripts/export-simplified-gammas.py \
  results/NEW-RUN/gammas.csv \
  results/NEW-RUN/NAME_24_tab.lis results/NEW-RUN/NAME_32_tab.lis \
  results/NEW-RUN/NAME_38_tab.lis results/NEW-RUN/NAME_39_tab.lis
```

This reads the angle-integrated table only. The per-GeV differential values
are divided by 1000 for per-MeV, and multiplied by energy-bin width in GeV
for bin integrals. For sectors, divide by their spatial solid angle for /sr;
the single local-normal USRBDX angular bin is already integrated by USXSUW.
Do not multiply these tables by another 2*pi. Area=1 means no apparatus area
factor. Prompt values remain per incident proton; multiply by the configured
2.4966036e15 p/s for prompt rates. Delayed DCYSCORE values already include
the irradiation history and are per second: never multiply by RATE again.

Fine and broad total grids overlap; never sum them. Sector totals and the
combined spectrum also describe the same escaping photons; never sum them
together. Sector sums should agree statistically with the broad total spectrum
in vacuum, within consistent energy windows. Individual detector errors are
retained; no uncertainty on correlated sums or ratios is invented.
The old `export-gamma-cooling.py` expects paired ALCASE/HAV1 names and must not
be used for this copy. The new exporter deliberately does not overwrite files.
As before, the initial Ra/daughter radioactive source is not added by this
scoring cleanup; results describe irradiation-induced activation radiation.

## Validation and next run

Installed Flair 3.4-5.4 loaded the new standalone deck, preprocessing returned
no errors and active-card validation reported no invalid fields. Independent
checks confirmed all isotope detector cards/associations and source/physics/
material cards were preserved, and all new scoring-region/name references
resolve. A deterministic 100,000-point spatial sample (76,134 inside the outer
bound) found exactly one region for each accepted point, including focused
apparatus sampling. This is a static partition check, not runtime geometry or
scientific acceptance. The photon exporter was checked against 1,200 bins from existing USXSUW
tables with detector headers renamed solely for parser verification; integrated
values agreed with printed detector totals within 1%. This is not new simulation
evidence. New detector results and statistical convergence remain
unverified until an authorized run.

For the next separately approved run, recommend and retain
`/usr/local/fluka/bin/flukadpm`. Extra DPMJET/RQMD models are not needed for
30 MeV incident protons; the executable is retained as the user's selection,
not as an accuracy enhancement. See `REVIEW.md`, executable assessment,
including installed manual thresholds. Confirm histories/cycles, new seeds,
data availability and an isolated ignored run directory before execution.
No expensive production run is authorized by this input cleanup.

## Manual authority

FLUKA Manual **4-5.2**, `/usr/local/fluka/doc/FLUKA_Manual.txt`,
§7.22.88 USRBDX (full entry retrieved for this change):

- Lines 20935–21005: one-way current mode, region pair and area=1 integration.
- Lines 21014–21055: energy and local angular binning fields.
- Lines 21079–21122: USXSUW single/double differential tables, units, and
  angle measured against the local boundary normal, not the beam axis.

Cooling normalization and isotope semantics follow the full card references
already recorded in `analysis/gamma_cooling_setup.md`: §7.22.11 DCYSCORE,
§7.22.64 RADDECAY and §7.22.66 RESNUCLEi. This cleanup makes no new isotope
model-accuracy claim; retained isomer/model limitations still apply.
