# MCNP versus current FLUKA: major differences in approach

Compared 2026-10-26. This is a static review, not a code benchmark or a validation
of either simulation. No input, project, manual or result was modified, and no
simulation was executed.

## Files and authority

- MCNP input: `reference/racl2_30MeV_good_flowandflux_fine.i`.
- Current FLUKA input: `working/cycloinv_200mgRa.inp`, referenced by
  `working/cycloinv_200mgRa.flair`.
- Supplied manual: MCNP Code Version 6.3.2 Theory & User Manual,
  LA-UR-26-23119 Rev. 1, issued 2026-05-19. The MCNP executable version,
  loaded nuclear data and successful execution of this particular input have not
  been supplied. Defaults discussed here are those of that manual, not proof
  of the settings used for a historical run.
- FLUKA reference: installed FLUKA Manual 4-5.2,
  `/usr/local/fluka/doc/FLUKA_Manual.txt`.

## Main finding

Both decks describe the same general water-cooled salt target concept and now
use a uniform, parallel 30 MeV proton disk of radius 1 cm. The MCNP deck emphasizes
radiation leakage and dose at 1 metre, with a reaction-residual production tally.
The current FLUKA deck emphasizes residual production plus activity and decay
radiation after a specified irradiation and at several cooling times. They are
not yet equivalent physical targets or equivalent scored quantities.

## Differences, prioritized for isotope production

| Topic | Supplied MCNP deck | Current FLUKA deck | Consequence |
|---|---|---|---|
| Salt composition | M3 is `88226 1 17035 0.7577 17037 0.3423`. These are positive atom proportions: Cl/Ra = 1.1000, not 2. The chlorine isotope entries also sum to 1.1. | COMPOUND uses one Ra-226 atom and two natural chlorine atoms. | A major material mismatch affecting Ra atom density, stopping and reactions. The MCNP title says Ra-226Cl3 and a comment says RaCl2; neither overrides the actual M3 card. Do not treat this as a correctly specified RaCl2 reference. [M1] |
| Target loading and thickness | Radius 1 cm, salt thickness 0.01299 cm (129.9 micrometres), density 4.9 g/cm3: about 199.97 mg total material. With its actual nominal isotope ratios, about 170.4 mg is Ra-226. | Radius 1 cm, salt thickness 0.01706812 cm (170.68 micrometres), density 4.9: 262.74 mg salt containing 200 mg Ra-226. | Different Ra loading and proton energy loss through the target. If MCNP composition were corrected to RaCl2 without resizing it, the old geometry would hold only about 152.2 mg Ra. Mass estimates are derived using nominal atomic masses. |
| Production versus activity | F18:# / FT18 RES 1 92 scores reaction residuals in the five apparatus cells. No BURN, irradiation schedule or cooling-time activity calculation is present. | Unit 21 scores direct production; unit 22 adds DCYSCORE-linked residual activity after seven days at 40 microamperes, at EOI, 1 h, 1 d and 7 d. | Compare MCNP production to FLUKA direct production first, not directly to Bq. Production and post-irradiation inventory/activity are different quantities. FLUKA activity also includes daughter evolution. [M2, F1, F2] |
| Residual tally limitations | The supplied manual says FT RES combines metastable residuals with their non-metastable counterparts, excludes decay daughters, and does not score residuals from proton or photon library reactions (it does score model reactions and neutron reactions). | RESNUCLEi scores stopped residual nuclei in ground/isomeric states; decay-linked scores evolve produced nuclei. Isomer treatment remains approximate. | A yield difference might reflect scoring coverage or isomer grouping, rather than a reaction-model disagreement. Whether the MCNP library limitation matters for Ra-226 requires the actual loaded tables/model diagnostics. [M2, F1] |
| Nuclear data/model selection | No explicit library suffixes/xLIB, MX, PHYS, LCA or LEA selections. Supplied manual gives CEM03.03 as default nucleon cascade choice when applicable; table/model usage depends on available data and defaults. | Explicit JEFF-3.3 pointwise neutrons at 296 K; PRECISIO, heavy-fragment evaporation and coalescence; photonuclear interactions enabled. | These are different nuclear-data/model paths. The MCNP input alone cannot establish which Ra/Cl proton evaluations versus models were used. Neither deck establishes absolute isotope-yield accuracy without experimental comparison. [M1, M3, F1] |
| Encapsulation material | M4 is aluminum 6061 with Mg, Si, Ti, Cr, Mn, Fe, Cu and Zn. | Pure elemental aluminum. | Important for case activation and potentially radiation spectra. Trace alloy constituents can matter greatly even when their mass fraction is small. |
| Water and Havar representation | Water is H-1/O-16 only. Havar lists individual isotopes. No MT water thermal-scattering card is supplied. | Water and Havar use elemental definitions, with pointwise library isotope handling; existing review records water-bound hydrogen treatment, which should be confirmed in output. | Havar elemental proportions are approximately the same recipe, but isotope resolution, minor abundance rounding, and water thermal-neutron treatment need checking. Low-energy neutron spectra and capture activation can differ. [M1, M4] |
| Radiation scoring location | F1/F2 families score neutron, proton and photon spectra on a sphere of radius 100 cm, split into polar bands by planes. | Neutron/photon boundary scores at the apparatus exterior, regional scores and Cartesian maps; extra proton entrance/exit spectra at the salt. | These do not measure the same field. The MCNP geometry is a 1 m sphere, despite dose comments saying 100 m. FLUKA exterior scores are not a dose or fluence measurement at 1 m. |
| Dose versus fluence/current | F32:P and F42:N apply user-entered DE/DF coefficients labeled ICRP 74 to surface-fluence tallies. | No equivalent dose-conversion tally is included in the current deck. | MCNP includes a dose-response calculation absent from this FLUKA input. Its response quantity, angular assumptions, coefficient provenance and interpolation must be matched before comparing dose. F32 also scores energies above the last supplied photon response point (10 MeV); the manual specifies that the endpoint coefficient is then held constant, which needs physical justification. [M5] |
| Normalization and binning | F1 counts surface crossings; F2 is surface-average fluence, ordinarily per source history. Energy bins are nonuniform, up to 30-50 MeV, with polar segmentation. No physical beam current is specified. | Surface scores are normalized using the full apparatus exterior area (11.97351007272 cm2), logarithmic energy bins and one outward hemisphere; delayed scores incorporate the irradiation rate. | Match area, energy-bin integration, angular coverage and source-rate scaling. Raw ordinates cannot be compared directly. MCNP segmented F2 area divisors should be checked in output; no explicit SD cards are supplied. [M5, M6, F3] |
| Transport detail | MODE H P N transports protons, photons and neutrons; IMP:E does not add electrons to MODE. No explicit cutoffs or photonuclear switch are supplied. The manual default PHYS:P has photonuclear production off. | Electron/photon transport is configured with 100 keV electron kinetic and 1 keV photon cutoffs; PHOTONUC is explicitly on. | Electron transport and photonuclear settings differ. Do not assume IMP:E enables electron tracking. MCNP treatment of secondary-electron bremsstrahlung uses its applicable default approximations, rather than the same explicit electron transport as FLUKA. [M7] |
| Statistical effort | NPS = 5e8 (500 million histories). | NHIST = 1e6 per cycle (1 million); total depends on cycles actually run. | MCNP requests 500 times as many histories as one FLUKA cycle. Relative errors, tally efficiency and run totals must be compared, not only nominal histories. More histories do not resolve model or material bias. |

## Similarities that should not be mistaken for differences

- Both beams are monoenergetic 30 MeV protons, parallel, uniform over a disk of
  radius 1 cm. MCNP `SI1 0 1` / `SP1 -21` with nonzero SUR uses the default
  radial power-law exponent 1, giving uniform area sampling. FLUKA uses outer
  radius 1, inner radius 0 and circular-spot mode. MCNP starts at x=-5 cm;
  FLUKA at z=-1 cm, with vacuum before the first window. [M8]
- Beam axes differ only by coordinate convention: MCNP along +x and FLUKA +z.
- Both have 50 micrometre Havar / 3 mm water / 50 micrometre Havar upstream
  of the salt. Both side walls and aluminum back are 1.5875 mm thick. The
  FLUKA back is farther downstream because its corrected salt layer is thicker.
- Both surround the apparatus with vacuum; the MCNP air material is commented out.
- Both request isotope production separately in the target, aluminum, water and
  two Havar windows, although the region ordering differs.
- Neither input specifies an initial Ra-226 decay-source inventory with daughter
  ingrowth/radon retention. A target material definition and a production tally
  do not supply the complete pre-existing radioactive source term.

## Items to verify before interpreting an MCNP result

1. Resolve the actual intended M3 composition and loading in the reference model.
   No correction was made here.
2. Obtain the MCNP output header and loaded-table/model diagnostics. These are
   necessary to determine executable version, data coverage, default cutoffs and
   whether proton-library residual omissions affect the inventory tally.
3. The supplied 6.3.2 manual marks FT RES as requiring an FU card, while this deck
   has no FU18. Its own RES examples omit FU, so there is ambiguity in the manual.
   Treat this as a version/output verification item, not a proven fatal error.
4. Verify segmented F2 surface areas and the dose response at energies beyond the
   supplied photon coefficient table. The sphere centre is x=0.316495 cm, the midpoint of the MCNP salt layer;
   its angular planes are approximate. These details are secondary to the
   composition/loading mismatch.
5. Compare direct isotope production per primary with matching isotope grouping,
   then apply the same irradiation/decay history before comparing activity. For
   radiation, compare the same distance, angular bands, energy bins and response.

## Manual references

MCNP page numbers below are printed page numbers; PDF physical pages are printed
pages plus four. Full relevant passages were checked in the supplied manual.

- M1: sections 5.6.1 and 5.6.3, pp. 323-326 and 330: positive fractions are atomic,
  fractions are normalized, library selection and table/model substitution.
- M2: section 5.9.18.12, pp. 504-506 (PDF pp. 508-510): FT RES semantics,
  scoring coverage, isomer grouping and examples.
- M3: section 5.7.3 LCA, pp. 366-367: default CEM03.03 and evaporation controls.
- M4: section 5.6.2, pp. 327-329: MT thermal-scattering association.
- M5: section 5.9 and Table 5.18, pp. 453-454; DE/DF input cards in section 5.9.8, pp. 484-485.
- M6: sections 5.9.14-5.9.15, pp. 489-492: segmentation and area divisors.
- M7: sections 3.2.5.1 (p. 259) and 5.7.2.3 (p. 342): MODE and photon physics.
- M8: section 5.8.3, p. 414 (PDF p. 418): SP -21 default exponent for RAD with SUR.
- F1: FLUKA Manual 4-5.2, section 7.22.66 RESNUCLEi,
  `/usr/local/fluka/doc/FLUKA_Manual.txt:18330-18481`, especially notes 4, 6 and 7.
- F2: same manual, section 7.22.64 RADDECAY,
  `/usr/local/fluka/doc/FLUKA_Manual.txt:18152-18174`: analytical decay evolution.
- F3: same manual, section 7.22.88 USRBDX,
  `/usr/local/fluka/doc/FLUKA_Manual.txt:20918-21232`: boundary quantities,
  directionality, area and differential normalization.

Input SHA-256 at review:

- FLUKA: `14e04bf5e8b90b1692a9b6797db91481bac7f52c51645f31bc3c5979c58980c6`
- MCNP: `f2bf4486bdd600e01638d40366ae81873d5d21fdae9094c0db5640e9cd936755`
