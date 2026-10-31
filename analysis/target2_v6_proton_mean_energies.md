# V6 proton mean energies and Flair font warning

Read existing `working/cycloinv_target2_cleanv6_31.bnx` using installed Flair
`Data.Usrbdx`. Header: 7,999,950 primary histories, same total primary weight,
8 batches; title identifies 24.4 MeV, 200 microA and 0.5100 g graphite.

| Detector | V6 mean MeV | V5 mean MeV |
|---|---:|---:|
| PIN | 18.509563 | 18.447353 |
| POUT | 12.599216 | 13.219545 |
| PINFWD | 18.530279 | 18.468347 |
| POUTFWD | 12.629627 | 13.248399 |

Full-spectrum current-weighted bin-midpoint means, including tails. Forward
acceptance is 0.98 <= cos(theta_z) <= 1; no peak window was selected. Bin widths
are 20.4167 keV, 1200 bins over 0–24.5 MeV. Statistical uncertainties of the
means were not calculated. Means use sum(E_mid*f*dE)/sum(f*dE); the constant
single angular-bin width cancels. Binary data avoid printed text rounding.
Independent angle-integrated text-spectrum integration agrees within 0.00088 MeV.
Integrated binary crossing yields agree with stored USXSUW totals within 1e-5
relative tolerance. No new simulation or processing run was launched.

The forward entrance is 0.030279 MeV above 18.5 MeV, and the forward exit
is inside 12–13 MeV. The mean difference is 5.900652 MeV, versus 5.219949 MeV
in v5: +0.680703 MeV, close to the intended +0.7 MeV. As before, differences
of means compare crossing populations and are not paired per-track losses.
Recommendation: retain v6 for the requested entrance/exit criteria.

One worker, `working/cycloinv_target2_cleanv6_05001.out:5988`, reports forced
external termination and feeder timeout, then writes its output normally with
999,950 primaries. The other seven contribute 1,000,000 each, matching the merged
header. The merged normalization reflects the actual histories; the deficit is
50/8,000,000 = 0.000625%. This is separate from the plotting warning.

## Plotting warning

Installed Gnuplot is `/opt/homebrew/bin/gnuplot`, version 6.0 patchlevel 6.
Its installed `help qt` documents default FontFace 'Sans' and the explicit
syntax `set term qt font "Arial,12"`. Arial exists locally at
`/System/Library/Fonts/Supplemental/Arial.ttf` (Helvetica is also installed).

Installed Flair `GPPlot.py:351–370` reads Gnuplot output and sets the generic
"Gnuplot errors or warnings found" result for any nonempty diagnostic. It does
not distinguish this font warning from an actual plotting error in that summary.
Thus the supplied messages are consistent with font lookup/startup latency,
not proof of damaged simulation data or failed graph generation.

Recommended first fix in Flair: Preferences -> Gnuplot -> Terminal:

```text
qt font "Arial,12"
```

Enter just the terminal specification, without 'set terminal'. Flair constructs
`set terminal {term} {index} enhanced ...` in `GPPlot.py:106–121`. The settings
widget is implemented in `ConfigDialog.py:1347–1382`. Save preferences, close
existing plot windows, and restart Flair to create a fresh Gnuplot session.
Check explicit fonts in plot labels if 'Sans' remains in a per-plot setting.
The general Flair GUI Fonts preferences control a different font system and
are not the relevant first fix. For noninteractive export, pdfcairo/pngcairo
with an explicit installed font can avoid the Qt window path. Do not globally
suppress stderr, since that would hide genuine plotting errors.

Only code/help/font availability were checked here. No GUI reproduction,
preference modification, installation patch or package update was performed.
If a graph is actually missing or malformed after this change, inspect its full
Gnuplot diagnostic/script rather than assuming every error has this cause.

Primary Gnuplot documentation (Qt font syntax/defaults):
https://gnuplot.info/docs_6.0/Gnuplot_6.pdf (Qt terminal section).
Implementation: https://github.com/gnuplot/gnuplot/blob/master/src/qtterminal/qt_term.cpp
contains the 'Warning: slow font initialization' diagnostic.
Scoring reference: FLUKA Manual 4-5.2 §7.22.88 USRBDX,
`/usr/local/fluka/doc/FLUKA_Manual.txt:21079–21122`.
