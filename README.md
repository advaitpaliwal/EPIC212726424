# EPIC 212726424.01: an Earth-sized planet candidate on a 1.49-day orbit around a nearby early M dwarf

Advait Paliwal (independent researcher, advaitpaliwal@gmail.com), 2026-10-11.

A shallow dip in brightness repeats every 1.49 days in K2 Campaign 6 (2015) and Campaign 17 (2018) photometry of EPIC 212726424, an early M dwarf 100 pc away. The signal appears in both campaigns with the same depth and duration. If it is a planet, it is slightly smaller than Earth and receives about 130 times the sunlight Earth does.

| | |
|---|---|
| Host | EPIC 212726424 = TIC 196682692 = 2MASS J13305832−0736022, M0 dwarf, 99.9 pc, Kp = 13.15, Gaia RUWE 1.00 |
| Period | 1.4927186 (+0.0000036/−0.0000044) d |
| Mid-transit | 2457685.5911 (+0.0013/−0.0012) BJD_TDB |
| Depth / duration | 220 (+21/−19) ppm / 1.06 (+0.10/−0.09) h (EVEREST light curves, joint fit) |
| Radius | 0.88 (+0.08/−0.07) R⊕ |
| Equilibrium temperature | 936 ± 32 K |
| Data | K2 C6 (2015 July–September) and C17 (2018 March–May), 30-minute cadence; 90 transits with in-transit data |
| False-positive probability | 0.031 ± 0.007, range 0.016–0.040 (TRICERATOPS with MOLUSC Gaia limits, 10 runs, no neighbours removed); 0.151 without; NFPP 0 |
| Wide companion | TIC 196682700 (G = 11.5, K dwarf), 65.8″ away with matching Gaia parallax and proper motion: about 6,530 AU projected (Revision 1) |

Status: **planet candidate**. Not a TOI, CTOI or K2 candidate in the NASA Exoplanet Archive as of 2026-10-11. The in-transit difference-image centroids sit 1.0″ (1.0σ) and 1.1″ (1.0σ) from the out-of-transit centroid in the two campaigns, and the box depths agree within 2σ between campaigns and across four light-curve reductions (175–226 ppm). The transit is too shallow for TESS at this brightness (Sector 91 gave no useful constraint); high-resolution imaging and precise space photometry are the next observations.

## Revision 1 (2026-10-16)

The research note was revised in response to the journal editor. The false-positive probability and the joint-fit values are unchanged. The corrections are:

- **False-positive probability:** FPP = 0.0314 ± 0.0069 (range 0.016–0.040), NFPP = 0, with no stars removed: the two Gaia sources in TRICERATOPS's 40″ field contribute at most 2 × 10⁻⁶ of the flux and get no scenarios. This is above the 0.015 validation threshold.
- **Centroids:** the offsets are measured from the out-of-transit centroid (from the catalogue position they are 1.74″ and 1.19″). The centroids locate the source only to within about 3″.
- **Per-transit χ²:** 94/84 (p = 0.22) about the weighted mean; a second, template-scaled estimator gives 129/73, and the same statistic at 13 null phases gives 0.88–1.80 (median 1.36).
- **Period alias:** 639 and 641 cycles sit 31.0σ and 30.2σ from the Campaign 6 fit but 17.0σ and 19.9σ from the Campaign 17 fit (version 1.0 said about 30σ from either).
- **Smaller fixes:** campaign gap 2.6 yr (was 2.7); companion separation 6,530 AU (was 6,550); target Gaia RV 13.2 ± 1.0 km s⁻¹ over 21 epochs (p = 0.32) replaces "constant radial velocity"; injections 150–257 ppm, 60/60 recovered.
- **MOLUSC:** Gaia RUWE and contrast tests only (no imaging); 200,000 companions generated, 51% kept. ExoFOP lists no high-resolution imaging or spectroscopy for either star as of 2026-10-15.
- **Figure 1** now has three panels: Campaigns 6 and 17 folded, both campaigns unfolded with the trend, and four single transits (`revision1/figure1_combined_EPIC212726424.png`).

`revision1/scripts/numbers.py` re-derives every number quoted in the revised note; its output is `numbers.log`. Every change, with its source, is listed in [`revision1/CHANGES.md`](revision1/CHANGES.md). The revised note text is with the journal and is not included here.

## Contents

- `note/figure1_EPIC212726424.png` — C6 and C17 photometry folded on the joint ephemeris, 10-minute bins, exposure-integrated model with posterior draws, residuals
- `data/lc/folded_lc_everest.csv` — the folded EVEREST data and model shown in Figure 1 (with campaign column); `depths_box.json` — depths per reduction
- `data/fit/` — posterior summary (`posterior_summary_joint_everest.csv`, 40 walkers × 30,000 steps), joint and per-campaign fit outputs, thruster-firing test; `extended_66k/` holds a 66,000-step rerun whose medians agree within 0.5σ
- `data/vetting/`, `data/injection/` — odd/even, secondary-eclipse and per-transit checks; injection-recovery and null tests
- `data/pixels/` — difference images and depth-versus-aperture results, with the same tests on K2-191 b for reference
- `data/fpp/` — false-positive probability runs (`fpp_summary.csv`, scenario tables, MOLUSC summary)
- `data/tess/`, `data/catalogue/`, `data/search/` — TESS coverage check, catalogue queries with their URLs, and the search detection
- `code/` — search, light-curve, fit, vetting, pixel, FPP, TESS, catalogue and figure scripts

Data: K2 (NASA, via MAST), EVEREST, K2SFF and K2SC high-level science products, ESA Gaia DR3, TIC v8. Software: lightkurve, batman, emcee, transitleastsquares, wotan, TRICERATOPS, MOLUSC, tess-point, astropy, matplotlib. Licences: code MIT; text, figures and data CC BY 4.0.

Scripts are kept exactly as run, with the author's absolute working paths (`~/Scratch/k2-hunt`, `~/Scratch/k2-deep`, `~/Scratch/EPIC212726424-work`); edit those paths to rerun them elsewhere.
