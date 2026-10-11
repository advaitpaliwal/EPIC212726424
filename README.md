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
| False-positive probability | 0.031 ± 0.007 (TRICERATOPS with MOLUSC Gaia limits, 10 runs); 0.151 without; NFPP 0 |
| Wide companion | TIC 196682700 (G = 11.5, K dwarf), 65.8″ away with matching Gaia parallax and proper motion: about 6,550 AU projected |

Status: **planet candidate**. Not a TOI, CTOI or K2 candidate in the NASA Exoplanet Archive as of 2026-10-11. The difference-image centroids sit 1.0″ (1.0σ) and 1.1″ (1.0σ) from the star in the two campaigns, and the box depths agree within 2σ between campaigns and across four light-curve reductions (175–226 ppm). The transit is too shallow for TESS at this brightness (Sector 91 gave no useful constraint); high-resolution imaging and precise space photometry are the next observations.

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
