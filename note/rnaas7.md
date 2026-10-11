# A 0.9 Earth-radius Planet Candidate on a 1.49-day Orbit around the M Dwarf EPIC 212726424, Seen in Two K2 Campaigns

Advait Paliwal
Independent researcher, Sterling Heights, MI 48314, USA
advaitpaliwal@gmail.com

## Abstract

I report a transit-like signal on EPIC 212726424 (UCAC4 412-055290), an early M dwarf at 99.9 pc, detected independently in K2 Campaigns 6 and 17, 2.7 years apart. A joint transit fit gives a period of 1.4927186 ± 0.0000040 d, a depth of 220 ± 20 ppm and a duration of 1.06 h, implying a radius of 0.88 ± 0.08 R⊕ and an equilibrium temperature of 936 ± 31 K. The star is not a K2 candidate, TOI or CTOI. The two campaigns give consistent periods and depths, and the signal appears in four light-curve extractions with consistent odd and even depths and no secondary eclipse. The difference-image centroid lies within 1.1″ of the target in both campaigns. With Gaia companion limits, TRICERATOPS gives FPP = 0.031 ± 0.007 and NFPP = 0. The candidate awaits high-resolution imaging.

## Star and search

EPIC 212726424 has Kp = 13.15, Teff = 3754 ± 138 K (M0), R★ = 0.561 ± 0.017 R☉ (Hardegree-Ullman et al. 2020) and M★ = 0.564 ± 0.020 M☉ (Stassun et al. 2019). Its Gaia DR3 RUWE is 1.00, with no non-single-star solution and a constant radial velocity (Gaia Collaboration et al. 2023). The K dwarf TIC 196682700, 65.8″ away (about 6,550 AU projected), shares its parallax, proper motion and radial velocity, and is listed as a common-proper-motion companion by Gaia Collaboration et al. (2021). ExoFOP lists no imaging or spectroscopic follow-up for either star.

I searched EVEREST light curves (Luger et al. 2016, 2018) of about 4,200 cool dwarfs within 114 pc observed by K2 (Howell et al. 2014), selected from Hardegree-Ullman et al. (2020), using wotan (Hippke et al. 2019) and Transit Least Squares (Hippke & Heller 2019) over 0.5–30 d. Each detection had to appear at a consistent depth in EVEREST and K2SFF (Vanderburg & Johnson 2014) and in both halves of the campaign. It also had to pass odd–even, secondary-eclipse, shape and stellar-density tests, and have no Gaia neighbour within 12″ bright enough to produce it. The search recovered known K2 planets at their published periods. This signal was found separately in Campaign 6 (SDE 32.7) and Campaign 17 (SDE 25.9).

## Transit fit

I fitted both campaigns' EVEREST light curves jointly with batman (Kreidberg 2015) and emcee (Foreman-Mackey et al. 2013). The model integrates over the 29.4-minute exposures, assumes a circular orbit, and uses a stellar-density prior and uninformative quadratic limb darkening (Kipping 2013). It gives P = 1.4927186 (+0.0000036/−0.0000044) d, T0 = 2457685.5911 ± 0.0012 BJD_TDB, Rp/R★ = 0.0143 ± 0.0010, a/R★ = 8.05 ± 0.33, b = 0.69 (+0.07/−0.10), a depth of 220 (+21/−19) ppm and T14 = 1.06 ± 0.10 h (Figure 1). This implies Rp = 0.88 ± 0.08 R⊕, a = 0.021 AU, an insolation of 128 (+19/−16) S⊕ and Teq = 936 ± 31 K. A longer chain changes no parameter by more than 0.5σ.

## Vetting

Separate fits give 1.492689 ± 0.000077 d and 224 ± 22 ppm for Campaign 6, and 1.492904 ± 0.000127 d and 210 ± 23 ppm for Campaign 17. The periods agree to 1.5σ, and the campaigns are linked by exactly 640 cycles; neighbouring cycle counts would require periods about 30σ from either campaign's own fit. Depths at the joint ephemeris are 194 ± 16 and 198 ± 18 ppm (EVEREST), 175 ± 18 and 210 ± 20 ppm (K2SFF), and 226 ± 16 and 206 ± 23 ppm (fresh aperture photometry) in Campaigns 6 and 17, plus 216 ± 38 ppm from K2SC in Campaign 6 (Aigrain et al. 2016).

Odd and even depths agree to 0.2σ in the joint EVEREST light curve; the largest difference in any single extraction is 2.3σ (K2SFF, Campaign 17). The depth at phase 0.5 is 14 ± 9 ppm. Individual transit depths are consistent (χ² = 94 for 84 degrees of freedom). All 60 injected transits of the same size were recovered. The period is not a multiple of the 6-hour thruster-firing cycle, and firings show no phase coherence with the transit.

The difference-image centroid lies 1.0″ (1.0σ) from the target in Campaign 6 and 1.1″ (1.0σ) in Campaign 17. The known planet K2-191 b, observed in the same campaigns, shows offsets of 2.4″ and 2.8″. The nearest Gaia source is a G = 17.6 star 19.7″ away, outside the photometric aperture.

## False-positive probability

I averaged TRICERATOPS (Giacalone & Dressing 2020; Giacalone et al. 2021), run in its K2 mode, over ten runs of 10⁶ draws each, with companion limits from Gaia astrometry and imaging via MOLUSC (Wood et al. 2021). The result is FPP = 0.0314 ± 0.0069 (range 0.016–0.040; three runs exceed 0.035) and NFPP = 0. Without companion limits the FPP is 0.15. Almost all of the remaining FPP (0.031) comes from a planet orbiting an unresolved bound companion. The star has no high-resolution imaging, and Collier et al. (2026) find that small validated planets in their imaging sample needed contrast curves, so I make no validation claim.

## Summary

EPIC 212726424.01 is an Earth-sized candidate on a 1.49-day orbit around an early M dwarf in a wide binary, detected independently in two K2 campaigns. TESS Sector 91 data are too noisy to test it (expected S/N 0.3). High-resolution imaging would most directly reduce the false-positive probability. Code and data are at https://github.com/advaitpaliwal/EPIC212726424.

## Acknowledgments

This paper includes data collected by the K2 mission, funded by the NASA Science Mission Directorate, and obtained from MAST. It uses data from the ESA mission Gaia, processed by the Gaia DPAC.

## Figure 1

K2 EVEREST photometry of EPIC 212726424 from Campaigns 6 (dots) and 17 (crosses) folded on the joint ephemeris, with 10-minute bins (black), the exposure-integrated median model and posterior draws (blue) and residuals (bottom).

## References

Aigrain, S., Parviainen, H., & Pope, B. J. S. 2016, MNRAS, 459, 2408
Collier, M., Giacalone, S., Derfer, B., et al. 2026, AAS Journals, accepted, arXiv:2608.21560
Foreman-Mackey, D., Hogg, D. W., Lang, D., & Goodman, J. 2013, PASP, 125, 306
Gaia Collaboration, Smart, R. L., Sarro, L. M., et al. 2021, A&A, 649, A6
Gaia Collaboration, Vallenari, A., Brown, A. G. A., et al. 2023, A&A, 674, A1
Giacalone, S., & Dressing, C. D. 2020, triceratops, ascl:2002.004
Giacalone, S., Dressing, C. D., Jensen, E. L. N., et al. 2021, AJ, 161, 24
Hardegree-Ullman, K. K., Zink, J. K., Christiansen, J. L., et al. 2020, ApJS, 247, 28
Hippke, M., David, T. J., Mulders, G. D., & Heller, R. 2019, AJ, 158, 143
Hippke, M., & Heller, R. 2019, A&A, 623, A39
Howell, S. B., Sobeck, C., Haas, M., et al. 2014, PASP, 126, 398
Kipping, D. M. 2013, MNRAS, 435, 2152
Kreidberg, L. 2015, PASP, 127, 1161
Luger, R., Agol, E., Kruse, E., et al. 2016, AJ, 152, 100
Luger, R., Kruse, E., Foreman-Mackey, D., Agol, E., & Saunders, N. 2018, AJ, 156, 99
Stassun, K. G., Oelkers, R. J., Paegert, M., et al. 2019, AJ, 158, 138
Vanderburg, A., & Johnson, J. A. 2014, PASP, 126, 948
Wood, M. L., Mann, A. W., & Kraus, A. L. 2021, AJ, 161, 85
