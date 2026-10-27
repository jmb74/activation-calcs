# Corrected 200 mg Ra-226 target geometry

Use `working/cycloinv_200mgRa.flair` and its referenced authoritative input
`working/cycloinv_200mgRa.inp`. These are new working copies of the 30 MeV
entrance-energy diagnostic configuration; previous inputs/projects/results remain
unchanged. Existing results apply to the old geometry and must not be relabelled.

The requested loading is **0.200 g Ra-226 in anhydrous RaCl2**, rather than
0.200 g of salt. Retain the existing salt density 4.9 g/cm3 and radius 1 cm.
Using nominal molar masses 226 g/mol for Ra-226 and 35.45 g/mol for natural Cl:

- Salt mass = 0.200 * (226 + 2*35.45)/226 = 0.262743363 g.
- Salt volume = mass/4.9 = 0.0536210945 cm3.
- Salt thickness = volume/pi = 0.0170681245 cm = 170.681245 micrometres.
- Salt front remains z=0.31000000 cm; back becomes z=0.32706812 cm.
- Side-wall thickness = 1.15875 - 1 = 0.15875 cm = 1.5875 mm.
- Aluminum back thickness is also 0.15875 cm, so outer back becomes
  z=0.48581812 cm. The previous geometry already had equal back/wall
  thickness; both cylinder endpoints are moved together to retain that equality.

The salt-only PTGTRZ mesh endpoint follows the new salt back. Surface-score
normalization SAREA is updated to 11.97351007272 cm2 using
2*pi*R*(R+L). The existing Cartesian mesh still encloses the apparatus.
Updated regional volumes (ALCASE, HAV1, WAT, HAV2, TGT) in cm3 are
1.021773575, 0.0157079633, 0.9424777961, 0.0157079633, 0.0536210945.
Use these volumes when converting regional track lengths to fluence.

The geometry correction retained the existing source settings. The subsequent
beam-profile update below replaces the pencil beam. Material density/composition,
irradiation, cooling and physics switches remain unchanged. Assumptions remain anhydrous pure salt, fully Ra-226 radium and
uniform bulk density; hydration or packing-density changes require new dimensions.
The conversion uses nominal molar masses and dimensions rounded to 1e-8 cm.

Geometry interpretation: FLUKA Manual 4-5.2, section 8.2.4.4 RCC,
`/usr/local/fluka/doc/FLUKA_Manual.txt:23855-23896` defines the cylinder base,
height vector and radius. Dimensions and volumes above are derived geometrically.

Installed Flair 3.4-5.4 loaded the new referenced project successfully;
preprocessing returned no errors and card validation returned no invalid fields.
These static checks do not establish runtime geometry or scientific acceptance.

No simulation was launched. Retain the selected `flukadpm` executable for any
separately authorized run; the existing executable assessment in REVIEW.md applies.

## Uniform circular proton beam

Updated `working/cycloinv_200mgRa.inp` (also used by its referenced Flair project)
to a uniform disk of **2 cm diameter (1 cm radius)**, covering the full target
face as clarified by the user. BEAM WHAT(4)=1.0 cm outer radius, WHAT(5)=0 cm inner radius and WHAT(6)=-1
select a filled circular spot. Momentum spread and divergence are explicitly zero.
The beam remains centered at x=y=0, z=-1 cm, directed along +z, at 30 MeV.
Total beam current remains 40 microamperes for seven days, distributed over the
full disk area; it is not a current density specification.

Reference: FLUKA Manual 4-5.2, section 7.22.4 BEAM,
`/usr/local/fluka/doc/FLUKA_Manual.txt:6369-6421` (spot radii and annular mode).
No simulation was run for this change.
