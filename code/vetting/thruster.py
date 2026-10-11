# K2 thruster-firing check: firing cadence period from QUALITY bits 20/21 in the K2 llc files, P/P_thr ratio, in- vs out-of-transit flagged fractions, transit phase vs firing.
import numpy as np, glob, json
from astropy.io import fits
P, T0, T14 = 1.4927186, 2852.59113, 1.06/24
out = {}
for c in ['c06', 'c17']:
    d = fits.getdata(glob.glob(f'lc/mastDownload/K2/ktwo212726424-{c}_lc/*llc.fits')[0], 1)
    t, q = d['TIME'], d['SAP_QUALITY']; ok = np.isfinite(t); t, q = t[ok], q[ok]
    fire = (q & (1 << 19)) | (q & (1 << 20))   # bits 20 (thruster firing) and 21 (possible), 1-indexed
    tf = t[fire > 0]
    dt = np.diff(tf); dt = dt[(dt > 0.1) & (dt < 0.4)]
    Pthr = float(np.median(dt))
    ph = ((t - T0 + 0.5*P) % P) - 0.5*P; intr = np.abs(ph) < 0.5*T14
    # power of firing train folded on candidate P: fraction of firings in transit window vs expectation
    phf = ((tf - T0 + 0.5*P) % P) - 0.5*P
    out[c] = dict(n_cad=int(len(t)), n_fire=int(len(tf)), P_thr_d=Pthr, P_thr_h=Pthr*24, P_over_Pthr=P/Pthr,
                  nearest_harmonic=dict((f'{n}xPthr', n*Pthr) for n in [5, 6, 7]),
                  frac_fire_in_transit_window=float(np.mean(np.abs(phf) < 0.5*T14)), expected=float(T14/P),
                  flagged_frac_in=float(np.mean(fire[intr] > 0)), flagged_frac_out=float(np.mean(fire[~intr] > 0)))
    # Rayleigh-like test: phases of firings relative to candidate period
    z = np.abs(np.mean(np.exp(2j*np.pi*phf/P))); out[c]['firing_phase_coherence_on_P'] = float(z); out[c]['coherence_expected_random'] = float(1/np.sqrt(len(tf)))
    for k in [1, 2, 3]:  # beat: does k*P land on integer number of thruster periods?
        out[c][f'{k}P_mod_Pthr_frac'] = float(((k*P/Pthr) + 0.5) % 1 - 0.5)
    print(c, out[c])
json.dump(out, open('fit/thruster.json', 'w'), indent=1)
