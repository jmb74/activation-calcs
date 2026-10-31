# Target #2 v3 — 1 mm RaCl2/graphite zone

New input: `working/cycloinv_target2_cleanv3.inp`, copied from
`working/cycloinv_target2_cleanv2.inp`. Earlier files remain unchanged.

The target has radius 1 cm, thickness 0.1 cm, and volume pi*0.1 =
0.3141592654 cm3. It contains exactly 0.200 g Ra-226, 0.06274336283 g
natural chlorine, and 0.4429 g natural carbon (graphite). Chlorine is calculated
from anhydrous RaCl2 stoichiometry with nominal molar masses 226 and 35.45 g/mol.
Total mass is 0.7056433628 g, giving bulk density **2.2461325851 g/cm3**,
consistent with the user's rounded 2.246 g/cm3.

| Constituent | Partial density (g constituent/cm3 mixture) | Mass fraction |
|---|---:|---:|
| Ra-226 | 0.6366197724 | 0.2834292938 |
| Chlorine | 0.1997183268 | 0.0889165351 |
| Graphite/carbon | 1.4097944859 | 0.6276541711 |

These are homogeneous-mixture partial densities, not individual grain densities.
The previous supplied rounded Ra/Cl proportions (about 201.2 mg Ra) are replaced
by the newly confirmed exact 200 mg Ra loading and stoichiometric chlorine.

## Axial geometry (cm)

| Region | Front z | Back z | Thickness |
|---|---:|---:|---:|
| Al6061 front (part of ALCASE) | 0 | 0.05 | 0.5 mm |
| WAT | 0.05 | 0.15 | 1 mm |
| TAWIN | 0.15 | 0.155 | 50 microns |
| TGT | 0.155 | 0.255 | 1 mm |
| CUBACK | 0.255 | 0.455 | 2 mm |
| COOL | 0.455 | 1.455 | 1 cm |
| Al6061 back (part of ALCASE) | 1.455 | 1.655 | 2 mm |

The cavity radius is 1 cm; housing radius 1.2 cm. The cavity RCC starts
at z=0.05 with length 1.405 cm, and the housing RCC starts at z=0 with
length 1.655 cm. The target-only PTGTRZ mesh ends at z=0.255 and has
100 axial bins, preserving the previous 10-micron bin thickness. The existing
Cartesian maps still enclose the assembly and are retained. The exterior world
sphere is unchanged; its center has no physical effect on the target stack.

## Beam and energy scoring

Retained actual source card: 23.5 MeV protons, Gaussian x/y FWHM 1.6 cm,
no divergence, starting at z=-5 cm. This includes Gaussian tails outside the
1 cm target radius. Current is 400 microA for seven days. No beam profile
change, physics switch change or transport cutoff change was introduced.

Unit 31 retains PIN, POUT, PSIDE and PBACK, and adds:

- **PINFWD**: TAWIN -> TGT, forward incoming spectrum.
- **POUTFWD**: TGT -> CUBACK, forward exiting spectrum.

The forward detectors use one angular bin from zero to
2*pi*(1-0.98) = 0.1256637061 sr (card rounded to 0.12566371).
At these planar faces the crossing normal is +z, so this selects
0.98 <= cos(theta_z) <= 1, approximately theta_z <= 11.48 degrees.
All proton detectors use current scoring with area divisor 1 and 1200
linear energy bins over 0–60 MeV, i.e. 50 keV/bin.

Use the solid-angle-integrated processed POUTFWD spectrum when comparing with
the supplied forward proton peaks. A peak-weighted mean requires selecting the
peak energy window(s), then weighting each bin midpoint by integrated bin
current (differential spectrum times bin energy width). No peak window has been
assumed or hard-coded. A mean over the complete forward spectrum can differ
from a mean over peaks alone. Raw double differential data also need their
angular-bin width; do not multiply processed angle-integrated spectra by it again.
The user's 12.1 MeV result is a comparison target, not a new FLUKA result.

## Validation and executable

Installed Flair 3.4-5.4: no preprocessing errors or invalid card fields;
evaluated BEAM energy -0.0235 GeV, material density 2.2461325850936 g/cm3.
Independent analytic evaluation of the actual geometry body/region expressions
passed 60,000 sampled points over apparatus/world scales plus axial layer
midpoints. Forward angular limits were checked algebraically. These checks do
not establish FLUKA runtime acceptance or scientific accuracy.

Recommend and retain `/usr/local/fluka/bin/flukadpm` for a separately approved
run. Its extra DPMJET/RQMD linkage is not required for the present low-energy
primary proton beam. No simulation was launched.

References: installed FLUKA Manual 4-5.2, §7.22.88 USRBDX,
`/usr/local/fluka/doc/FLUKA_Manual.txt:20916–21233`, especially lines
21037–21055 (angular bounds) and 21114–21122 (2*pi*(1-cos(theta)) relative
to boundary normal); §7.22.8 COMPOUND, lines 7332–7487 (mass proportions);
§7.22.46 MATERIAL, lines 13888–14052 (bulk density and isotope selection);
§8.2.4.4 RCC, lines 23855–23896 (base, height and radius).
