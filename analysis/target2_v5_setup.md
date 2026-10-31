# Target #2 v5: 24.35 MeV

Created `working/cycloinv_target2_cleanv5.flair` and its synchronized companion
`.inp` from v4 using the installed Flair project reader/writer. V4 input/project
hashes were checked unchanged. The only physical input change is
EBEAM 0.0245 -> 0.02435 GeV. Retained 200 microA, seven days, target geometry,
200 mg Ra226, 0.4429 g graphite, physics settings, seeds and scoring. EMAX remains
0.0245 GeV so the v4/v5 energy grids are identical. The project default run now
explicitly selects recommended `/usr/local/fluka/bin/flukadpm`.

Reasoning: v4's forward entrance mean is 18.654 MeV. The earlier user-reported
17.5 MeV value at 23.5 MeV source gives an approximate response of 1.154 MeV per
MeV of source energy. A linear correction would be about -0.133 MeV, yielding
24.367 MeV source; however, the older entrance value was approximate and the
response is not established as exactly linear. The requested -0.15 MeV is a
reasonable first correction, so v5 uses 24.35 MeV rather than implying additional
precision. It should bring entrance energy close to 18.5 MeV, but the result
requires simulation. The exit may remain above 13 MeV; measure it before tuning
graphite. No new energy prediction is a simulated result.

Reload/preprocessing and card validation passed, with evaluated beam energy
-0.02435 GeV and IRRPROFI 604800 s at 1.2483018148922e15 protons/s. No simulation
was launched. Retain flukadpm; its extra DPMJET/RQMD linkage is not needed for
this primary proton energy. Reference: FLUKA Manual 4-5.2 §7.22.4 BEAM,
`/usr/local/fluka/doc/FLUKA_Manual.txt:6315–6333` (negative WHAT(1) specifies
kinetic energy in GeV). Energy-adjustment reasoning is an empirical inference
from the two reported runs, not a stopping-power calculation.
