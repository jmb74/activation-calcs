> Current condition corrected to **400 microA** on 2026-10-26. Use
> `working/cycloinv_400uA_1m.flair`; earlier completed runs and historical
> discussion below used 40 microA. See `analysis/400uA_update.md` for scaling,
> recommendations and revised wide cooling-product exports.

# Activation input review

Prepared for CERN FLUKA 4-5.2. The original `cyclotron_activation.inp` is unchanged.
`working/cyclotron_inventory.inp` is the editable working candidate. The latest
user clarification specifies **30 MeV, 3 mm water, and 40 microamperes for seven
continuous days**, superseding the earlier 16 MeV condition discussed below.
See [the 30 MeV result review](analysis/30MeV_inventory_review.md) for the user's
completed run results and prepared entrance-energy diagnostic. No simulation
was launched by the assistant.

## Executable selection

The user selected `/usr/local/fluka/bin/flukadpm` for the current run. Retain and
record this executable for project runs; explicitly check executable selection in
future run recommendations. Installed `rfluka` documents `-d` as selecting
`bin/flukadpm` (`/usr/local/fluka/bin/rfluka:38,129`).

This selection is acceptable, but the extra DPMJET/RQMD linkage is not required
for the present 16 MeV proton beam. The installed manual gives default thresholds
of 20 TeV for hadron DPMJET, 5 GeV/n for ion DPMJET and 0.125 GeV/n for ion RQMD
(FLUKA Manual 4-5.2, §7.22.59 PHYSICS/DPMTHRES,
`/usr/local/fluka/doc/FLUKA_Manual.txt:16932–16958`). For ion interactions below
125 MeV/n, BME is already linked in standard `fluka` (§7.22.37 IONTRANS,
lines 12165–12171). Thus `flukadpm` is not by itself an accuracy upgrade for this
beam. Do not interrupt the current run solely to change the executable.

## Configure with the FLUKA preprocessor

Edit the `#define` block at the top of `working/cyclotron_inventory.inp` directly;
no JSON or Python generation step is required. The superseded generator and its
JSON files have been removed.

| Definition | Meaning / default |
|---|---|
| EBEAM | Positive kinetic energy in GeV, 0.016; BEAM uses -$EBEAM |
| IRRT | Irradiation duration in seconds, 604800 |
| RATE | Proton intensity in particles/s, 2.4966036E14 for 40 microamperes |
| CT0–CT3 | Cooling-time slots in seconds: 0, 3600, 86400, 604800 |
| NHIST / SEED | Histories and random-sequence initializer |
| ECUT / GCUT | Electron kinetic / photon cutoffs in GeV |
| NTEMP | Neutron temperature in kelvin; library is literal JEFF-3.3 on LOW-PWXS |
| SAREA | Whole apparatus exterior area in cm2 |
| EMAX / NMIN / NBINS | Spectrum upper energy, neutron lower energy, energy bins |
| PHNUC / PENETR | Enable photonuclear interactions / proton penetration detectors |
| XYZMAP | Enable the three prompt Cartesian fluence maps on unit 30 |
| XYMAX / ZMIN / ZMAX | Cartesian map bounds: x,y = ±1.275 cm; z = -0.02..0.50 cm |
| NXY / NZ | Cartesian map bins: 51 in x and y, 260 in z |

Use `$NAME` to substitute a constant. These native directives support constants,
conditional inclusion and includes; they are not a loop or arithmetic language.
Keep the hyphenated neutron library name literal in LOW-PWXS rather than in a
`#define`. The first runtime attempt aborted in EXPREV on codeword JEFF with
`#define NDATA JEFF-3.3`; Flair static validation did not catch this expression
evaluation incompatibility. The working input now uses literal JEFF-3.3.
RATE must be entered in particles/s: current_uA * 1e-6 / 1.602176634e-19.
To disable a switch, remove its definition or use `#undef`; defining it as 0
still enables it. If changing ECUT, also review the PROD-CUT FUDGEM field (currently
1 for 100 keV electrons). EMAX must remain above the incident energy and encompass
secondary energies of interest. Units and detailed card references are below.

Keep CT0=0 and CT1–CT3 positive, distinct and increasing; duplicate cooling times
are collapsed by FLUKA, changing subsequent indices. Editing a slot changes its
associated isotope, activity and radiation scores together. Detector prefixes
D001–D004 indicate slots, not fixed physical times. To add another cooling time,
add a constant, extend DCYTIMES, copy a complete cooling scoring block with unique
names, and associate it with the new index in all three DCYSCORE estimator types.
For more irradiation intervals, add IRRPROFI cards with duration/intensity pairs;
zero intensity describes a beam interruption. Cooling times are measured from
the end of the final interval. [M2, M11]

The working candidate retains the supplied pencil beam, geometry and materials.
The original header saying 18 MeV disagrees with its actual BEAM card; the working
copy uses the confirmed 16 MeV. Keep simulation outputs in ignored `results/`.

## Findings requiring physical confirmation

1. **Measure energy arriving at the salt.** The supplied water thickness is confirmed. On axis the sequence is
   50 micrometres Havar, 3 mm water, 50 micrometres Havar, then 129.9 micrometres
   RaCl2. The target front is at z=0.31 cm, not z=0. The existing 16 MeV beam enters
   the first foil from z=-1 cm. Whether enough protons reach the salt, and at what
   energy, needs a stopping-range check and pilot tally. Do not assume 16 or 18 MeV
   at the salt. The proposition that the water may stop much of the beam is a
   physical concern to test, not a transport result from this review.
2. **Confirm target mass and chemical form.** Radius 1 cm and thickness 0.01299 cm
   give 0.0408093 cm3 and approximately 0.19997 g RaCl2 at 4.9 g/cm3. This implies
   approximately 0.1522 g Ra-226 for anhydrous salt. Verify actual loading, packing
   density, hydration, purity, isotope composition and backing dimensions. The
   chlorine density on its elemental MATERIAL card does not describe the bulk
   compound; the RACL2 density is the relevant bulk density. Havar fractions sum
   to 1, but verify the alloy certificate and impurities; aluminium is currently
   pure elemental aluminium, not an engineering alloy.
3. **Refine source details when available.** The supplied energy/current/duration are confirmed. Use measured entrance energy/spread,
   spot size and alignment, transmitted beam current, duty cycle and interruptions.
   A pencil beam may misrepresent window/case activation and energy deposition.
   The regional energy-deposition tally supports a thermal-load estimate; thermal
   evolution and density changes are not calculated by this deck.
4. **Separate initial radioactivity from beam-induced inventory.** A radioactive
   MATERIAL definition is not an initial radionuclide source inventory. These
   RESNUCLEi scores describe produced residuals and their subsequent evolution;
   add independently specified initial Ra-226 and existing daughters for total
   post-irradiation source terms. Document chemical separation date, daughter
   ingrowth and radon retention/release. Do not assume secular equilibrium.
   Flowing water, removal of components and daughter migration also require a
   separate handling/transport model; the deck keeps the apparatus in place.

## Inventory and scoring changes

The original has five isotope detectors, all associated only with cooling index 1.
Its ACTIVITY region binnings already cover ALCASE through TGT at four times, but
they do not replace isotope-resolved inventories. The original boundary DCYSCORE
lines contain invalid punctuation/fields and inappropriate continuation records;
the last block also uses index 3 again instead of 4. These records were replaced.
Sharing a unit among detectors of the same estimator type is allowed; the shared
unit 33 in the original is not itself an error. [M1, M3, M4]

| Unit | Candidate score | Interpretation |
|---|---|---|
| 21 | Five unassociated RESNUCLEi detectors Y0–Y4 | Direct residual production, nuclei/primary; no cooling evolution |
| 22 | Five RESNUCLEi detectors for each cooling time | Isotope-resolved **Bq per whole region**, including decay evolution |
| 23 | ACTIVITY by region at each cooling time | Total Bq in each region; cross-check against unit 22 |
| 24 | Prompt neutron/photon exterior spectra | Per-primary surface fluence and outward current |
| 25 | Cooling-time neutron/photon exterior spectra | Surface fluence rate and outward current rate |
| 26 | Prompt neutron/photon region USRBIN | Integrated track length per region per primary |
| 27 | Cooling-time neutron/photon region USRBIN | Integrated track length per region per second |
| 28 | Prompt region ENERGY | GeV deposited per region per primary |
| 29 | PREG and PTGTRZ proton fluence | Regional track length and salt r-z fluence map |
| 30 | PXYZ / NXYZ / GXYZ | Prompt Cartesian proton / neutron / photon fluence maps |

Region order is ALCASE, HAV1, WAT, HAV2, TGT. `D001`, etc., identify cooling
indices; CT0–CT3 in the preprocessor block give the corresponding seconds. Unit 22 normalization is 1,
so it is not Bq/cm3. Activity is not an atom inventory: for a radioactive isotope,
N=A/lambda using an appropriate evaluated half-life. Stable inventories cannot be
recovered from Bq. Retain unit 21 for production yields, including stable products;
full time-dependent stable populations and initial target depletion require a
separate inventory/depletion calculation. Do not interpret production yields as
the remaining initial target population. [M1–M3]

The whole non-vacuum/non-blackhole apparatus consists of the five scored regions.
Only ALCASE and HAV1 touch external vacuum in the existing geometry: the case
has an open front aperture occupied by HAV1. Consequently both boundaries must
be scored. The candidate uses **one-way logarithmic-energy** USRBDX: code 99 for
fluence and -1 for current, one angular bin over 2pi. The original code 112 means
two-way, linear-energy, logarithmic-angle fluence; its 10 keV minimum omits thermal
and epithermal neutrons. The candidate neutron range begins at 1e-14 GeV and the
photon range at 1 keV, both ending at 30 MeV. [M4]

For each species/time, add detector components A (ALCASE) and H (HAV1), separately
for F (fluence) and J (current). Both components are divided by the **same total
exterior area**, 2*pi*R*(R+L), approximately 11.94 cm2. Their sum is therefore the
area-averaged exterior score, not a sum of separately averaged surfaces. This
area and boundary list must change if geometry changes. Multiplying the integrated
summed J score by that area gives outward crossings per primary (prompt) or per
second (decay). Fluence uses inverse-cosine weights and is not particle leakage
count. These are scores at the apparatus surface, not at a remote observer. [M4]

USRBDX spectra are differential in energy/solid angle. Use USXSUW's integrated
and cumulative outputs or explicitly integrate with bin widths; summing raw
ordinate values is incorrect. Prompt rate = per-primary score times beam p/s.
DCYSCORE-linked scores already include the irradiation profile: **do not multiply
them by beam current again**. A decay-time score is an instantaneous rate, not
fluence integrated over a cooling interval. The regional fluence bins must be
divided by their respective region volumes to obtain cm^-2 per primary or
cm^-2/s. Region ACTIVITY bins already give whole-region Bq. [M2–M5]

Delayed neutron scores are diagnostic tallies, not evidence that a complete
delayed-neutron, spontaneous-fission or alpha-neutron source model is present.
Audit those source mechanisms separately if required for the total Ra apparatus
neutron source. A zero tally does not establish a zero physical source.

## Physics recommendations and implemented choices

- Retain PRECISIO, EVAPORAT=3 and COALESCE=1. The manual specifically recommends
  heavy-fragment evaporation and coalescence for residual production. These were
  already good choices in the original. Do not suppress secondary transport or
  enable aggressive biasing before the analogue pilot is understood. [M1, M6]
- Explicitly select pointwise JEFF-3.3 neutron treatment at 296 K; PRECISIO already
  enables pointwise treatment. This documents the choice rather than introducing
  a previously missing neutron model. Local JEFF-3.3 files for Ra-226 elastic,
  capture, inelastic and fission channels were found; file presence is not proof
  of complete residual yields. Inspect loaded isotope/data diagnostics. Compare
  key capture products with another installed evaluated library as a sensitivity
  study, and use actual operating temperatures. Hydrogen defaults to water-bound
  thermal scattering; check that association in output. [M7, R1]
- Lower photon transport/production cutoff from PRECISIO's 100 keV to **1 keV**
  for prompt and decay radiation so the photon spectrum includes low-energy
  emissions. Retain 100 keV electron kinetic cutoff; set FUDGEM=1 consistently.
  Expect additional CPU cost. Confirm important photon observables are stable
  against an electron-cutoff reduction before accepting low-energy spectra. [M6, M8]
- Enable PHOTONUC=1 for all physical materials. This includes secondary-photon
  nuclear reactions otherwise disabled by default; it is a completeness choice,
  not a claim that they dominate proton-induced activation. Quantify their effect
  with a controlled comparison if necessary. [M9]
- Explicitly retain activation mode RADDECAY=1, three decay replicas and the
  default equal-sharing isomer model. **Isomer ratios are approximate**, so key
  metastable/ground-state inventories need evaluated or experimental comparison.
  Increasing replicas improves decay-radiation sampling, not nuclear-production
  model accuracy. [M3]
- Benchmark important proton-induced Ra/Cl and apparatus isotope yields against
  measured excitation functions over the actual slowing-down energy interval.
  This is a proposed scientific acceptance step, not a claim of benchmarked
  accuracy. Model switches and one million histories alone cannot establish it.

## Validation and proposed run sequence

Completed: installed Flair 3.4-5.4 loads the preprocessor-based working input,
preprocessing returns no errors, and card validation reports no invalid fields.
Resolved values are BEAM=-0.016 GeV, IRRPROFI=604800 s at 2.4966036e14 p/s,
and cooling times 0/3600/86400/604800 s. These are static checks, not FLUKA runtime
or geometry tracking acceptance. Original geometry/material text is retained.
No simulation, compilation, GUI save or installation change was performed.

Before production: confirm actual target loading and inspect geometry in Flair
(especially foil contacts and front aperture). Then authorize a short pilot in a
fresh ignored `results/` directory. Inspect loaded materials/isotopes and cross
sections, geometry diagnostics, proton penetration, scoring headers, isotope bounds
and normalization. Inspect whether the 100 keV charged-hadron cutoff affects
required low-energy reaction channels before changing it.

### Proton penetration detectors (unit 29)

`PREG` is prompt proton USRBIN type 12 across ALCASE, HAV1, WAT, HAV2 and TGT.
It scores total proton track length in each region per primary. Divide by region
volume for the volume-averaged fluence in cm^-2/primary. Volumes in that order are
1.017382949, 0.0157079633, 0.9424777961, 0.0157079633, 0.0408092886 cm3.

`PTGTRZ` is prompt proton USRBIN type 11, a cylindrical r-z fluence map covering
exactly the salt: r=0..1 cm, z=0.31..0.32299 cm, with 50 radial and 26 axial bins.
The axial bin thickness is about 5 micrometres. Its values are already normalized
by bin volume, in cm^-2/primary; multiply by RATE for cm^-2/s during irradiation.
Neither detector has DCYSCORE, so these are prompt transport diagnostics. [M5]

A nonzero map demonstrates proton tracks in the salt, including secondary protons.
It does not alone give the fraction of incident protons transmitted or their
arrival energy. A zero tally in a finite pilot gives an upper bound limited by
statistics, not proof of no penetration. If needed, add a proton boundary-current
energy spectrum at HAV2-to-TGT to resolve arrival energy and crossings explicitly.

### Cartesian penetration maps (unit 30)

`PXYZ`, `NXYZ`, and `GXYZ` are USRBIN type 10 track-length fluence maps on an
identical x/y/z grid. They cover the full apparatus and a small vacuum margin:
x,y = -1.275..1.275 cm; z = -0.02..0.50 cm. The 51 x 51 x 260 bins give voxels
0.5 mm x 0.5 mm x 20 micrometres. Odd transverse bin counts put the pencil beam
inside the central voxel rather than on a bin boundary. The default three maps
contain approximately 8.1 MB of score values per cycle, before processing overhead.

These are prompt fluences, including secondary particles, in cm^-2 per primary;
multiply by RATE for irradiation fluence rates. They do not include cooling-time
decay radiation and are not energy spectra. Their spatial bins include vacuum
where it lies within the rectangular mesh. [M5]

After a new run, process unit 30 with USBSUW. In Flair, select PXYZ, NXYZ or GXYZ
from the processed file and plot an x-z slice through y=0 (or a narrow central
y interval). Use matching spatial limits, geometry overlays and logarithmic
colour scaling to compare particle penetration. The water spans z=0.005..0.305 cm;
the salt begins at z=0.31 cm. Bins crossing an interface average over that voxel.
For the pencil beam, map magnitudes depend strongly on transverse voxel size;
use the spatial falloff to visualize stopping, rather than treating the central
voxel as a measured finite beam profile. Existing runs cannot supply these new
scores retroactively. No additional simulation was launched for this edit.

For production, use independent random sequences/cycles and size the history
count against uncertainties of the specific isotopes of interest. Process unit
21/22 with USRSUW, boundary files with USXSUW, and region files with USBSUW.
USRSUWEV offers offline irradiation/cooling evolution of direct production
scores; this is useful when exploring many schedules without rerunning transport,
subject to its decay-data/model scope. Keep direct production and cooling-time
activity files separate. The installed `fluresnucle_formatter.py` can export
processed isotope tables as CSV/JSON. [M1, M4, M5]

## Reference passages

Primary authority: **FLUKA Manual, Version 4-5.2**, installed at
`/usr/local/fluka/doc/FLUKA_Manual.txt` (version header line 6).

| ID | Section and line locations |
|---|---|
| M1 | §7.22.66 RESNUCLEi, lines 18330–18520: fields, normalization, model recommendations, offline evolution and formatting |
| M2 | §7.22.11 DCYSCORE, lines 7782–7925; §7.22.12 DCYTIMES, lines 7927–8100; §7.22.38 IRRPROFIle, lines 12177–12315 |
| M3 | §7.22.64 RADDECAY, lines 17993–18249: isomers, replicas, evolution and rate normalization |
| M4 | §7.22.88 USRBDX, lines 20916–21233: codes, area normalization, spectra and USXSUW |
| M5 | §7.22.89 USRBIN, lines 21234–21900: region layout, activity, track length and regional normalization (Note 13) |
| M6 | §7.22.13 DEFAULTS/PRECISIO, lines 8421–8464; §7.22.59 PHYSICS/COALESCE, lines 16855–16872 and EVAPORAT, lines 17027–17050 |
| M7 | §7.22.44 LOW-PWXS, lines 13331–13550: pointwise defaults, library, temperature and water binding |
| M8 | §7.22.21 EMFCUT, lines 9847–10020: production/transport thresholds and FUDGEM |
| M9 | §7.22.58 PHOTONUC, lines 16491–16580 |
| M10 | §7.22.4 BEAM, lines 6315–6328 (negative energy in GeV); §7.22.46 MATERIAL, lines 13888–14030 (density and isotope fields) |
| M11 | §6.1 input preprocessor, lines 3904–4048: #define, $ substitution, conditional switches and includes |
| R1 | Installed `/usr/local/fluka/RELEASE-NOTES`, Fluka-4.5.2, lines 1–15: JEFF-3.3 remains default |

For external background, CERN's [Radiation Protection specific calculations
training slides](https://indico.cern.ch/event/1123370/contributions/4716073/attachments/2447835/4194554/18_Activation_2022_ULB.pdf)
describe combined production/decay calculations. These are explanatory; the
installed 4-5.2 manual above governs the candidate's syntax and settings.
