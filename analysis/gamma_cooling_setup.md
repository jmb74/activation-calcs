# Gamma spectra after shutdown, 30 MeV

Prepared input: `working/cycloinv_gamma_30MeV.inp`, copied from
`working/cycloinv_400uA_1m.inp` (SHA-256
`390cb7323e84102df9c353e5ea147ae96bfaa117a61b0d3d7df7ae71bb8b4070`).
Original files and results are preserved. No simulation was launched.

The supplied conditions remain 30 MeV incident protons, a uniform 1 cm radius
beam, the existing 3 mm water layer, 200 mg Ra-226 as anhydrous RaCl2,
Al-6061 encapsulation, and 400 microA for seven days. No 24 MeV case is added.
Transport and nuclear physics settings are inherited, including the approximate
equal-sharing isomer model; this setup does not establish absolute inventory accuracy.
Existing sphere centres/angular planes remain as in the baseline: this change
does not incorporate the separate proposed MCNP scoring-centre adjustment.

The 34 cooling times are shutdown, 1 through 24 hours, then days 2 through 10.
`analysis/gamma_cooling_schedule.csv` records their DCYTIMES indices. The original
four detector groups are remapped to indices 1, 2, 25 and 31. Five-region isotope
activities on unit 22 now cover the full schedule, retaining direct production
yields on unit 21. The existing four-time activity exporter is not compatible
with this expanded table; use the general residual-nuclei parser for unit 22.

## Meaning of the photon output

User-confirmed scope: photons escaping the complete assembly, including reaction
photons during irradiation and radiation from radioactive decay products. An
intrinsic photon birth spectrum is not required. Keep the beam-on prompt and
post-shutdown delayed spectra separate: unit 24 already contains prompt exterior
photon scores, while the new unit 38 contains delayed exterior spectra at the
34 cooling times. Prompt reaction photons cease with the beam; the shutdown
time point is the delayed rate immediately after beam removal. Activation
products formed by reactions contribute to the subsequent delayed spectra.
For unit 24, sum PRPAJ and PRPHJ and multiply by SAREA and RATE after energy/angle
integration to obtain prompt escaping photons/s. These inherited scores use
the physical SAREA divisor and per-primary normalization, unlike unit 38.
Beam-on total radiation additionally includes the contemporaneous decay
contribution; the unit-24 prompt spectrum alone is not that total.

New unit-38 USRBDX current detectors score delayed photons leaving the assembly
through ALCASE -> VACREG and HAV1 -> VACREG. Sum the two boundaries, which cover
the exterior of the assembly. Normalization area is 1, so these scores integrate
over the surface rather than divide by the physical apparatus area. These are
outward crossing spectra after self-absorption and scattering, including secondary
photons from decay-radiation transport. They include activation of all assembly
materials, not exclusively the salt. They are not a photon birth spectrum and
should not be injected back inside the same assembly with attenuation applied again.
Outward crossings can include recrossings; they are not unique photon identities.

For each cooling time, detector GnnnLA/GnnnLH uses 3,000 linear 1 keV bins from
1 keV to 3.001 MeV. GnnnBA/GnnnBH uses 600 logarithmic bins from 1 keV to 30 MeV.
These are overlapping alternative grids: do not sum them. Energy bins approximate
the lines and do not represent detector resolution or an exact line catalogue.
Photons below the inherited 1 keV transport cutoff are excluded.

DCYSCORE already includes the irradiation profile and gives rates per second.
Do not multiply these delayed spectra by the beam rate again. Shutdown means
the instantaneous delayed rate at end of irradiation, excluding prompt radiation.
The current baseline does not add the initial Ra-226/daughter radioactive source:
these are irradiation-induced activation results, not the total pre-existing
plus induced radioactivity of a real radium target.

An intrinsic source term requires a separate, state-resolved calculation:
q(E,t) = sum_i A_i(t) I_i(E), using absolute photons/decay and consistent decay
branches. No intrinsic emission spectrum has been calculated here. Activities
alone are not photons/s, and surface scores must not be labelled intrinsic.

## Processing after an authorized run

Combine independent-cycle unit-38 files using the installed USXSUW (or Flair's
USRBDX processing). Use its angle-integrated `*_tab.lis`, then run:

```sh
python3 -B scripts/export-gamma-cooling.py /path/to/unit38_tab.lis /path/to/new-gamma.csv
```

The CSV gives cooling seconds, grid, energy edges in MeV, photons/s/MeV and
photons/s in each bin. Integrate one grid for its energy-band photon rate.
For the fine grid, divide differential per-GeV values by 1,000 to obtain per-MeV;
multiply by bin width in GeV to obtain photons/s/bin. The USXSUW table has already
integrated solid angle, so do not multiply by 2*pi again. Individual face percent
errors are retained; a combined error is not fabricated because face scores can
be correlated. A covariance-aware uncertainty on their sum needs cycle-level
processing. Likewise, do not combine time-point uncertainties as independent.

## Validation and execution

Installed Flair 3.4-5.4 preprocessing returned no errors, and active-card
validation returned no invalid fields. Counts: 6 DCYTIMES cards, 175 RESNUCLE
detectors and 574 USRBDX detectors (below the documented 1,100 limit). These are
static checks, not runtime geometry acceptance or statistical/physics validation.

For a separately authorized run, recommend and retain
`/usr/local/fluka/bin/flukadpm`. Its additional DPMJET/RQMD models are not needed
for this 30 MeV proton case (see REVIEW.md executable assessment); the executable
choice is not an accuracy improvement by itself. Before execution, confirm
histories/cycles, fresh seeds, data and an isolated ignored output directory.
The input retains 1,000,000 histories as a configuration value; no cycle count
or expensive production run is authorized by this setup change.

## Local manual authority

FLUKA Manual 4-5.2, `/usr/local/fluka/doc/FLUKA_Manual.txt`:

- Section 7.22.11 DCYSCORE, lines 7782–7926: estimator association, per-second
  normalization, and cooling factors unavailable to COMSCW/FLUSCW.
- Section 7.22.12 DCYTIMES, lines 7927–8099: seconds after irradiation, insertion
  order, duplicate handling and multiple cards.
- Section 7.22.64 RADDECAY, lines 17993–18246: analytical evolution, transported
  decay radiation, approximate isomer production and per-time normalization.
- Section 7.22.88 USRBDX, lines 20916–21239: one-way current, normalization,
  differential spectra and USXSUW processing; detector limit at line 21133.

The beam-energy observation comes from `analysis/6061_1m_run_review.md`: mean
salt entry 22.605 MeV and mean exit 21.617 MeV for the earlier 30 MeV case.
Those results are evidence about the existing setup, not new results for this deck.
