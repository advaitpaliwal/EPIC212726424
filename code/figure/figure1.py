# Figure 1 + folded CSV + posterior summary for EPIC 212726424 (joint C6+C17 EVEREST fit). usage: figure1.py FITDIR TAG OUTDIR
import sys, json, numpy as np, batman
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD, TAG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
G = 6.674e-8; RSUN = 6.957e10; RHOSUN = 1.989e33/(4/3*np.pi*RSUN**3)
def a_rs(rho, P): return ((G*rho*RHOSUN*(P*86400)**2)/(3*np.pi))**(1/3)
c = np.load(f'{FD}/chain_{TAG}.npz'); ch = c['ch']; Tref = float(c['Tref']); np.random.seed(1)
t0, P, lrp, b, rho, q1, q2, lsig, f0 = ch.T; k = np.exp(lrp); a = a_rs(rho, P); inc = np.degrees(np.arccos(b/a))
u1 = 2*np.sqrt(q1)*q2; u2 = np.sqrt(q1)*(1-2*q2)
bm = np.load(f'{FD}/bestmodel_{TAG}.npz'); t, f = bm['t'], bm['f']
r = json.load(open(f'{FD}/result_{TAG}.json'))
Pm, Tm = np.median(P), np.median(Tref+t0)
EXP = 1765.5/86400; SS = 15   # same as fit_joint.py
def params(i=None):
    p = batman.TransitParams(); p.t0 = 0; p.ecc = 0; p.w = 90; p.limb_dark = 'quadratic'
    if i is None: p.per = Pm; p.rp = np.median(k); p.a = np.median(a); p.inc = np.median(inc); p.u = [np.median(u1), np.median(u2)]
    else: p.per = P[i]; p.rp = k[i]; p.a = a[i]; p.inc = inc[i]; p.u = [u1[i], u2[i]]
    return p
f0m = np.median(f0); fn = f/f0m
camp = np.where(t < 3000, 6, 17)   # C6 BKJD 2384-2463, C17 BKJD 3346-3414
ph = ((t - Tm + 0.5*Pm) % Pm - 0.5*Pm)
pm = params()
mod_data = batman.TransitModel(pm, ph, supersample_factor=SS, exp_time=EXP).light_curve(pm)
res = fn - mod_data
w = 4.0; bw = 10/60; bins = np.arange(-w, w+1e-9, bw); bc = (bins[1:]+bins[:-1])/2; idx = np.digitize(ph*24, bins)
def bstat(y):
    n = np.array([(idx == j).sum() for j in range(1, len(bins))])
    m = np.array([np.mean(y[idx == j]) if (idx == j).sum() >= 2 else np.nan for j in range(1, len(bins))])
    e = np.array([np.std(y[idx == j], ddof=1)/np.sqrt((idx == j).sum()) if (idx == j).sum() >= 2 else np.nan for j in range(1, len(bins))]); return m, e, n
mb, eb, nb = bstat(fn); rb, re_, _ = bstat(res)
fig, ax = plt.subplots(2, 1, figsize=(7.5, 6.2), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
for A in ax:
    for s in ('top', 'right'): A.spines[s].set_visible(False)
    A.grid(axis='y', c='0.92', lw=0.6)
tt = np.linspace(-w/24, w/24, 3000)
for i in np.random.choice(len(ch), 50):
    pi = params(i); ax[0].plot(tt*24, (batman.TransitModel(pi, tt, supersample_factor=SS, exp_time=EXP).light_curve(pi)-1)*1e6, c='#2a78d6', alpha=0.06, lw=1)
sty = {6: dict(marker='.', c='0.72', ms=3), 17: dict(marker='x', c='0.55', ms=2.2, mew=0.5)}
for cc in (6, 17):
    s = camp == cc
    ax[0].plot(ph[s]*24, (fn[s]-1)*1e6, ls='none', zorder=0, label=f'K2 C{cc} EVEREST 30-min (unbinned)', **sty[cc])
    ax[1].plot(ph[s]*24, res[s]*1e6, ls='none', zorder=0, **sty[cc])
ax[0].errorbar(bc, (mb-1)*1e6, eb*1e6, fmt='o', c='0.1', ms=3, lw=0.9, label='C6+C17, 10-min phase bins')
integ = batman.TransitModel(pm, tt, supersample_factor=SS, exp_time=EXP).light_curve(pm)
ax[0].plot(tt*24, (integ-1)*1e6, c='#2a78d6', lw=1.6, label='median model integrated over 29.4 min')
ax[0].set_ylim(-700, 450); ax[0].set_ylabel('relative flux [ppm]'); ax[0].legend(fontsize=7, loc='lower left', frameon=False)
dep = r['depth_ppm'][0]; Rp = r['Rp_earth'][0]
ax[0].set_title('EPIC 212726424 K2 C6+C17   P = %.5f d   depth %.0f ppm   Rp = %.2f R$_\\oplus$' % (Pm, dep, Rp), fontsize=10)
ax[1].errorbar(bc, rb*1e6, re_*1e6, fmt='o', c='0.1', ms=3, lw=0.9); ax[1].axhline(0, c='#2a78d6', lw=1.6)
ax[1].set_ylim(-450, 450); ax[1].set_ylabel('resid. [ppm]'); ax[1].set_xlabel('hours from mid-transit'); ax[1].set_xlim(-w, w)
plt.tight_layout(); plt.savefig(OUT+'/figure1_EPIC212726424.png', dpi=300)
o = np.argsort(ph)
np.savetxt(OUT+'/folded_lc_everest.csv', np.column_stack([t[o]+2454833.0, camp[o], ph[o]*24, fn[o], mod_data[o], res[o]]), delimiter=',', fmt=['%.6f', '%d', '%.5f', '%.7f', '%.7f', '%.7f'],
           header='bjd_tdb,k2_campaign,hours_from_mid_transit,rel_flux,model_exposure_integrated,residual', comments='')
print('Tm_BKJD', Tm, 'Tm_BJD', Tm+2454833.0, 'Pm', Pm, 'n', len(t), 'nC6', (camp == 6).sum(), 'nC17', (camp == 17).sum(), 'bins_with_data', np.isfinite(mb).sum(),
      'resid_rms_ppm', np.std(res)*1e6, 'binned_resid_rms_ppm', np.nanstd(rb)*1e6, 'min_bin_n', nb[np.isfinite(mb)].min())
