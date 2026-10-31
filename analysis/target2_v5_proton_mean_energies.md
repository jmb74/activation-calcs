# V5 proton mean energies

Read existing `working/cycloinv_target2_cleanv5_31.bnx` with installed Flair's
`Data.Usrbdx`. Header: 8,000,000 primary histories, total weight 8,000,000,
8 batches, title identifying v5 at 24.35 MeV and 200 microA.

| Detector | V5 mean (MeV) | V4 mean (MeV) | Change (MeV) |
|---|---:|---:|---:|
| PIN | 18.447353 | 18.632614 | -0.185260 |
| POUT | 13.219545 | 13.460092 | -0.240547 |
| PINFWD | 18.468347 | 18.654026 | -0.185679 |
| POUTFWD | 13.248399 | 13.488715 | -0.240316 |

These are full-spectrum current-weighted bin-midpoint averages, including tails,
not peak-window means. Forward scores accept 0.98 <= cos(theta_z) <= 1.
The means use sum(E_mid*f*dE)/sum(f*dE); the single angular bin's constant
width cancels. Raw binary data avoid rounded text-edge precision loss.
All detectors have 1200 linear bins from 0 to 24.5 MeV (20.4167 keV/bin).
Statistical uncertainty on the mean was not calculated.

As an independent check, integrating the angle-integrated spectra in
`working/cycloinv_target2_cleanv5_31_tab.lis` gave means within 0.001 MeV
of the binary results. Binary integrated yields, after including the angular
bin widths, agree with the stored USXSUW detector totals to relative tolerance
1e-5. Calculated crossings per source proton: PIN 0.6586341263,
POUT 0.6546056281, PINFWD 0.6462793748, POUTFWD 0.6209813705.

Forward entrance is 0.031653 MeV below 18.5 MeV, and forward exit is
0.248399 MeV above 13 MeV. This supports the user's interpretation: entrance
is very close, while exit needs additional slowing. A small graphite increase
at fixed Ra/Cl loading and geometry is the appropriate next parameter to test;
no new loading has been chosen or input modified in this analysis.

Reference for scoring integration: FLUKA Manual 4-5.2, §7.22.88 USRBDX,
`/usr/local/fluka/doc/FLUKA_Manual.txt:21079–21122`. Mean formula is a derived
first-moment calculation. No simulation or reprocessing was launched.
