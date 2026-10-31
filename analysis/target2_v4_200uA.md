# Target #2 v4 — 24.5 MeV, 200 microA

Updated `working/cycloinv_target2_cleanv4.flair` through installed Flair's
project reader/writer and synchronized its companion `.inp`. The pre-edit pair
is preserved in `working/backups/v4_before_200uA_20261030_230302/`.

User-supplied previous run observations: about 17.5 MeV entering and 11.9 MeV
leaving at 23.5 MeV source energy. Desired values: 18.5 MeV entrance, 12–13 MeV
exit. These results were reported by the user, not independently reprocessed here.

V4 already defined EBEAM=0.0245 GeV. That value and the user's current EMAX
0.0245 GeV were retained. Seven-day irradiation, 1 mm target, 0.200 g Ra226,
0.4429 g graphite, geometry, physics and scoring are unchanged.

The inspected v4 pair lacked a RATE definition even though IRRPROFI referenced
$RATE. Added RATE=1248301814892200 protons/s, calculated from
200e-6 A / (1.602176634e-19 C/proton). IRRT remains 604800 s. Updated stale
current/beam-energy comments. No run overrides were present. The embedded project
input and companion input are synchronized; the stored md5 matches the input.

Validation: installed Flair 3.4-5.4 reload/preprocessing and card validation
passed. Evaluated IRRPROFI is 604800 s at 1.2483018148922e15 protons/s;
BEAM=-0.0245 GeV and target density=2.2461325850936 g/cm3. Diff against backup
shows the RATE addition and comment/whitespace edits, with no other physical
parameter changes. No simulation launched.

Recommendation: test 24.5 MeV first with graphite fixed. The source increase is
an empirical first correction for the reported 1 MeV entrance deficit; the
resulting entrance/exit shifts should be measured rather than assumed to be
exactly 1 MeV. Use the same forward angular acceptance and peak windows when
comparing runs. Set entrance energy using source energy, then adjust graphite
if exit energy is outside 12–13 MeV. If entrance remains off target, the two
runs provide a local finite-difference response for the next adjustment.
Changing beam current alone does not change transport energies in this fixed
material model; thermal/density feedback is not included.

Retain recommended `/usr/local/fluka/bin/flukadpm` for a separately approved run.
Its additional DPMJET/RQMD models are unnecessary for this low-energy primary
proton beam. FLUKA Manual 4-5.2 §7.22.38 IRRPROFIle,
`/usr/local/fluka/doc/FLUKA_Manual.txt:12177–12306`, specifies irradiation
intervals in seconds and intensities in particles/s. Executable assessment:
§7.22.59 PHYSICS/DPMTHRES, same manual lines 16932–17005.
