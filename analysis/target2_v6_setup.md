# V6 trial: 24.4 MeV, 0.5100 g graphite

Created `working/cycloinv_target2_cleanv6.flair` and its companion `.inp`
from v5 with the installed Flair project reader/writer. Earlier files are unchanged.
The two physical changes are source energy 24.35 -> **24.4 MeV** and graphite
mass 0.4429 -> **0.5100 g** (+0.0671 g, +15.15%). Carbon partial density becomes
1.6233804195373 g/cm3, and bulk mixture density becomes **2.4597185187229 g/cm3**.
Ra/Cl partial densities are unchanged: exactly 200 mg Ra226 with stoichiometric
Cl (nominal molar masses 226,35.45). Target radius 1 cm, thickness 1 mm,
all surrounding layers, 200 microA, seven days, Gaussian beam profile,
physics/cutoffs, histories, seed, and scoring are unchanged. EMAX=24.5 MeV
remains above the new beam energy and preserves the previous bin edges.

## Estimate, not a simulated prediction

Interpret the user's requested extra '0.7 meV' as **0.7 MeV** of extra target
energy loss relative to v5, not a 0.7 MeV reduction of source energy.
V5 forward means: entrance 18.468347455 MeV, exit 13.248398616 MeV,
difference 5.219948839 MeV. This difference compares two crossing populations;
it is not a trajectory-paired mean loss. Treating it as a representative normal
trajectory is an approximation used only to choose the next trial loading.

Measured v4/v5 entrance response:
(18.654026463 - 18.468347455)/(24.5 - 24.35) = 1.237860053 MeV/MeV.
Extrapolating +0.05 MeV source suggests entrance about 18.53024 MeV.
An increase of 0.7 MeV in target loss would suggest exit about 12.61029 MeV.
These are local extrapolations, not FLUKA results.

For a first loading estimate, `scripts/estimate-target2-v6-graphite.py` integrates
a simplified Bethe electronic stopping model along a straight trajectory in mass
columns. It uses K=0.307075 MeV cm2/g, proton rest energy 938.27208816 MeV,
electron rest energy 0.51099895 MeV, graphite Z/A=6/12.0107 and I=81 eV.
Mixture weighted Z/A=0.46653 and I=150.44 eV are the values printed in
`working/cycloinv_target2_cleanv5_01001.out:2861–2864`. The baseline mixture
stopping curve is multiplied by its fixed mass column. Additional carbon adds
its own stopping curve times the added carbon mass column; this is an approximate
additive stopping construction, not a new run's FLUKA stopping table.

The model omits shell/Barkas/Bloch/nuclear/density corrections, scattering,
straggling, reaction losses and acceptance changes. It is calibrated with one
scalar factor (0.98754405) so that the baseline reproduces the v5 entrance/exit
means. Calibration is not validation. Midpoint integration uses 1200 spatial
steps; bisection solves for the added carbon mass. It estimates total graphite
0.51233 g for exactly +0.7 MeV loss under these assumptions. Choose the rounded
**0.5100 g trial**, for which the same approximate model gives exit **12.63 MeV**
and an increase in target loss of **0.675 MeV** (about 0.7). No narrow uncertainty
interval is justified. A run must check the actual means and spectral shapes.

Independent source for graphite I=81 eV: NIST, *Update to ESTAR, PSTAR, and ASTAR
Databases*, ICRU Report 90 addendum, PDF page 1,
https://www.nist.gov/system/files/documents/2017/04/26/newstar.pdf.
NIST describes Bethe-based stopping and its corrections in PSTAR documentation:
https://physics.nist.gov/PhysRefData/Star/Text/programs.html.
These external graphite data do not establish FLUKA's internal graphite
stopping parameters. The model explicitly substitutes I=81 eV for the estimate.
Installed FLUKA Manual 4-5.2 describes ionisation theory at
`/usr/local/fluka/doc/FLUKA_Manual.txt:632` and compound stopping at
lines 3566–3581. MATERIAL/COMPOUND syntax and normalization remain as in v5.

## Validation and next run

The v6 project reloads/preprocesses with zero invalid card fields. Evaluated
beam energy -0.0244 GeV, density 2.4597185187229 g/cm3, irradiation 604800 s at
1.2483018148922e15 protons/s. Diff against v5 confirms only the energy and
carbon/density parameters plus descriptive title/comments changed. Source
project and input hashes were checked unchanged. Geometry itself is unchanged.

Recommend and persist `/usr/local/fluka/bin/flukadpm` in the project default run.
Its extra DPMJET/RQMD linkage is unnecessary for this primary proton energy;
retain the user's selection. No simulation was launched. After an approved run,
compare PINFWD/POUTFWD full-spectrum means using the same analysis method as v5,
and distinguish any peak-window mean if that is used instead.
