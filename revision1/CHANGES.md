Changes made in Revision 1 of the research note. The revised note text is with the journal and is not in this repository; the figure, new runs, scripts and source files it cites are in this folder. Paths in this file are the author's working paths.

# AAS82180 (EPIC 212726424): changes from submission7/rnaas7.md to rnaas_rev1.md

Number check: `../scripts/numbers.py` prints every quoted number from `~/Scratch/k2-deep/212726424/` and `~/Scratch/planet-hunt/prerev/`; its output is in `../scripts/numbers.log`. ExoFOP was re-fetched 2026-10-15 into `../_sources/exofop_tic_19668269{2,700}_20261015.json` (+ `.url`): `imaging` and `spectroscopy` are both empty for the target and for the companion.
Docx: built with the AAS82088 R1 tool, `tools/mkdocx.py` (python-docx 1.1.2): `uv run --no-project --with python-docx==1.1.2 python -I ~/Scratch/planet-hunt/tools/mkdocx.py rnaas_rev1.md figure1_combined_EPIC212726424.png Paliwal_EPIC212726424_RNAAS_rev1.docx`. Same package structure as the R1 docx, with one embedded image.
Body: 979 words (Star and search through Summary, headings excluded). Abstract: 149 words.

## Header
- Removed the postal address. It now reads "Independent researcher" and the email only.

## Editor question 1 (scope of the difference analysis)
- Difference images were already made for all available data: K2 C6 and C17 are the only K2 campaigns for this star, and TESS S91 has an expected S/N of 0.3. No change was needed; the response says so.
- "from the target" changed to "from the out-of-transit centroid" (abstract and Vetting). The offsets from the catalogue position are 1.74″ and 1.19″ (PREREV f).
- K2-191 b is now quoted with its significance: 2.4″ (5.0σ) and 2.8″ (1.8σ). Added that the formal errors are underestimated and the centroids locate the source only to within about 3″.
- The G = 17.6 neighbour: "outside the photometric aperture" replaced by its flux share in the aperture, 2 × 10⁻⁶ (`trc_neigh.json` fluxratio 1.85e-6).

## Editor question 2 (χ² values)
- The per-transit χ² is now defined: median out-of-transit flux within 0.5 d minus mean in-transit flux, error = OOT scatter / √(in-transit cadences), 85 epochs of 1–2 cadences, χ² = 94/84 about the weighted mean, p = 0.22 (`chi2_defs.log`).
- Added the second estimator, so the claim is not read as clean: template-scaled χ² = 129/73, and the same statistic at 13 null phases gives 0.88–1.80 (median 1.36) (`null_pertransit.log`). The old phrase "Individual transit depths are consistent" was removed.
- Period alias: "about 30σ from either campaign's own fit" was wrong for C17. 639/641 cycles sit 31.0/30.2σ from C6 but 17.0/19.9σ from C17 (`numbers.log`). The text now gives "30–31σ from the Campaign 6 fit and 17–20σ from the Campaign 17 fit".

## Editor question 3 (neighbour exclusion in TRICERATOPS)
- Stated that no stars were removed. The two Gaia sources in the 40″ field have flux ratios ≤ 1.8e-6, so TRICERATOPS sets their depth to 0 and gives them no scenarios. `n_stars` = 3 in every run (PREREV a).
- The abstract now says "no neighbours removed" and "above the 0.015 validation threshold".
- Dropped "three runs exceed 0.035". The range 0.016–0.040 is kept (7 of 10 runs are ≤ 0.035, `summary.json`).

## Editor question 4 (wotan / detrending)
- Search step spelled out: wotan biweight, 0.4 d window, no transit mask, clipping +3σ / −20σ (`k2-hunt/scripts/k2tls_hunt.py` `clean`).
- Fit step added: a second wotan biweight with a 0.75 d window; points within ±54 min of each predicted transit masked and the trend interpolated; OOT clipped +4σ / −8σ (`lcs2.py flat`, `chi2_defs.log` mask ±54 min).
- Fit details added: 1,999 points within 6 h of transit (`result_joint_everest.json` npts), 40 walkers × 30,000 steps, ≥ 44 autocorrelation times (30,000 / max τ 682).
- Removed "A longer chain changes no parameter by more than 0.5σ". No longer-chain output exists in the files: `result_everest.json` is a symlink to the joint result, and the run log warns that the chain is under 50τ. It is replaced by the τ statement above.

## Editor question 5 (unfolded light curve)
- Figure 1 is now the three-panel `prerev/212726424/figure1_combined_EPIC212726424.png`: folded C6 + C17, both campaigns unfolded with trend and 6 h bins, and four evenly spaced single transits (S/N 0.4–4, `make_figs.log`). The caption has been rewritten.

## Editor question 6 (MOLUSC)
- "companion limits from Gaia astrometry and imaging via MOLUSC" was wrong. It now says only the Gaia RUWE and contrast tests were used and no imaging went in. 200,000 companions generated, 51% kept (`molusc_summary.txt` 0.5096). The kept companions replaced the default prior for the bound-companion scenarios.
- Added: "As of 2026 October 15, ExoFOP lists no high-resolution imaging and no spectroscopy for either star" (re-fetched today). Replaces "ExoFOP lists no imaging or spectroscopic follow-up".

## Other number fixes (recomputed; all small)
- Campaign gap 2.7 → 2.6 yr (C6 mid BKJD 2424, C17 mid 3380: 956 d = 2.62 yr).
- Companion projected separation: "about 6,550 AU" → 6,530 AU (Gaia Collaboration 2021 LinSep in `vizier_targeted.txt`).
- Added the target's Gaia RV, 13.2 ± 1.0 km s⁻¹, 21 epochs, p = 0.32 (`gaia_dr3_60as.csv`). Replaces the unsupported "constant radial velocity".
- Errors shown asymmetric where the posterior is asymmetric: Rp (+0.08/−0.07), T14 (+0.10/−0.09), Teq (+32/−31), C6 P (+0.000075/−0.000078) and depth (+22/−21), C17 depth (+25/−21).
- EVEREST C6 box error 16 → 15 ppm (15.50). K2SC error 38 → 37 ppm (37.47) (`lc/depths_box.json`).
- Injections now give their range: 150–257 ppm at 1.05–1.92 d, 60/60 recovered (`inj/inj_c0?.json`).
- Dropped "The period is not a multiple of the 6-hour thruster-firing cycle" (P/P_thr = 6.088). The coherence statement is kept (0.013 and 0.005 against ~0.075 random, `fit/thruster.json`).

## Unchanged
- FPP 0.0314 ± 0.0069, NFPP 0, FPP without MOLUSC 0.15. All joint-fit values; odd/even 0.2σ; secondary 14 ± 9 ppm; centroid offsets 1.0″/1.1″; SDE 32.7/25.9; stellar parameters.
