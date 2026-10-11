# Posterior summary CSV + extra derived numbers for EPIC 212726424. usage: summary.py FITDIR TAG OUTCSV
import sys, json, numpy as np
FD, TAG, OUT = sys.argv[1:4]
G = 6.674e-8; RSUN = 6.957e10; RHOSUN = 1.989e33/(4/3*np.pi*RSUN**3)
def a_rs(rho, P): return ((G*rho*RHOSUN*(P*86400)**2)/(3*np.pi))**(1/3)
c = np.load(f'{FD}/chain_{TAG}.npz'); ch, lp, Tref = c['ch'], c['lp'], float(c['Tref']); r = json.load(open(f'{FD}/result_{TAG}.json'))
t0, P, lrp, b, rho, q1, q2, lsig, f0 = ch.T; k = np.exp(lrp); a = a_rs(rho, P)
rng = np.random.default_rng(3); Rs = 0.561 + 0.02*rng.standard_normal(len(ch))
aAU = a*Rs*0.00465047; Ms = 0.564328 + 0.0203177*rng.standard_normal(len(ch)); aK = (Ms*(P/365.25)**2)**(1/3)
def q(x): p = np.percentile(x, [16, 50, 84]); return [p[1], p[1]-p[0], p[2]-p[1]]
rows = [('P_d', r['P_d']), ('T0_BJD_TDB', r['T0_BJD_TDB']), ('RpRs', r['RpRs']), ('a_Rs', r['a_Rs']), ('b', r['b']), ('inc_deg', r['inc_deg']), ('rho_star_solar', r['rho_sun']),
        ('depth_ppm', r['depth_ppm']), ('T14_h', r['T14_h']), ('Rp_earth', r['Rp_earth']), ('a_AU', q(aAU)), ('S_earth', r['S_earth']), ('Teq_K', r['Teq_K']), ('q1', r['q1']), ('q2', r['q2']), ('jitter_ppm', r['jitter_ppm'])]
with open(OUT, 'w') as fo:
    fo.write('parameter,median,minus_1sigma,plus_1sigma\n')
    for n, v in rows: fo.write(f'{n},{v[0]:.12g},{v[1]:.3g},{v[2]:.3g}\n')
nw = 40; w = np.arange(len(ch)) % nw; low = lp < lp.max() - 50
print('nsamp', len(ch), 'tau_max', max(r['tau']), 'post_burn_steps', r['nstep'] - r['nstep']//3, 'n_tau', (r['nstep'] - r['nstep']//3)/max(r['tau']))
print('frac lp<max-50', low.mean(), 'walkers', np.unique(w[low]).tolist(), 'frac k>0.03', (k > 0.03).mean())
good = ~low
for n, x in [('T0', Tref+t0+2454833), ('P', P), ('RpRs', k), ('b', b), ('rho', rho), ('jitter', np.exp(lsig)*1e6)]:
    print(n, 'all', np.round(q(x), 7), 'main-mode', np.round(q(x[good]), 7))
print('a_AU', q(aAU), 'a_Kepler3_TICmass', q(aK), 'b95', np.percentile(b, 95))
print('corr T0-P', np.corrcoef(t0, P)[0, 1])
for name, bjd in [('S91_mid 2025-04-23', 2460788.5), ('S115_mid 2027-03-28', 2461492.5)]:
    T = Tref + t0 + 2454833; n = np.round((bjd - np.median(T))/np.median(P)); Tp = T + n*P
    print(name, 'epoch', n, 'Tpred', np.median(Tp), 'sigma_h(16-84/2)', (np.percentile(Tp, 84)-np.percentile(Tp, 16))/2*24, 'std_h', np.std(Tp)*24, 'std_h main', np.std(Tp[good])*24)
