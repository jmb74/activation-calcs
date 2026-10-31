# V4 proton mean energies

Analyzed existing `working/cycloinv_target2_cleanv4_31.bnx` with installed
Flair `Data.Usrbdx` (read-only). Header: 40,000,000 primary histories, primary
weight 40,000,000, 40 batches. No simulation or reprocessing was launched.

| Detector | Mean energy (MeV) | Crossings per source proton |
|---|---:|---:|
| PIN | 18.632614 | 0.658780197 |
| POUT | 13.460092 | 0.654764300 |
| PINFWD (requested FWDPIN) | 18.654026 | 0.646581176 |
| POUTFWD (requested FWDPOUT) | 13.488715 | 0.622074946 |

These are full-spectrum current-weighted means, including tails and secondary
protons, not means restricted to selected peak windows. Forward detectors
select 0.98 <= cos(theta_z) <= 1 at the planar entrance/exit faces.

For each bin with midpoint E_i, width dE_i and differential current f_i,
mean energy = sum(E_i*f_i*dE_i)/sum(f_i*dE_i), converted from GeV to MeV.
The binary raw data are double differential, but each detector has one angular
bin, so the constant angular width cancels from its mean. For total crossings,
that angular width was included; all four calculated yields agree with stored
USXSUW detector totals to relative tolerance 1e-5. Bin edges were reconstructed
from the binary header; 1200 linear bins over 0–24.5 MeV, approximately
20.4167 keV/bin. Means use bin midpoints and are therefore binned estimates.
No statistical uncertainty on the means was calculated.

Independent integration of the angle-integrated spectra in
`working/cycloinv_target2_cleanv4_31_tab.lis` agrees within 0.00056 MeV;
that text file prints rounded bin edges and spectrum values. Binary data were
used for the reported results to avoid this rounding loss.

The forward means are approximately 0.154 MeV above the desired 18.5 MeV
entrance and 0.489 MeV above the upper 13 MeV exit goal.

Normalization reference: FLUKA Manual 4-5.2, §7.22.88 USRBDX,
`/usr/local/fluka/doc/FLUKA_Manual.txt:21079–21122` describes the processed
angle-integrated spectra and the energy/angular widths required for integration.
The mean formula is the derived first moment divided by integrated current.
