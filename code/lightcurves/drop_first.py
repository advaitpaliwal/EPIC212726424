"""TLS on the EVEREST/fresh/k2sff light curve with data before BKJD 3073.2 removed (first transit at the campaign start)."""
import sys, json, numpy as np, warnings; warnings.filterwarnings('ignore')
from transitleastsquares import transitleastsquares
sys.path.insert(0, '/Users/advaitpaliwal/Scratch/k2-hunt/scripts'); from k2tls_hunt import clean
out = {}
for src in ['everest', 'k2sff', 'fresh']:
    z = np.load(f'/Users/advaitpaliwal/Scratch/k2-deep/248630648/lc/{src}.npz'); t, f = z['t_raw'], z['f_raw']
    for tag, m in [('all', np.ones(len(t), bool)), ('drop_first_0.5d', t > t.min() + 0.5)]:
        tc, fc = clean(t[m], f[m])
        r = transitleastsquares(tc, fc).power(period_min=0.5, period_max=30, R_star=0.397, M_star=0.387, R_star_min=0.08, R_star_max=1.0, M_star_min=0.08, M_star_max=1.0,
            oversampling_factor=2, duration_grid_step=1.15, use_threads=1, show_progress_bar=False)
        # SDE at the candidate period
        i = np.argmin(np.abs(r.periods - 15.8648)); 
        out[f'{src}_{tag}'] = dict(best_P=float(r.period), best_SDE=float(r.SDE), best_snr=float(r.snr), power_at_15p86=float(r.power[i]), ntr=int(r.distinct_transit_count))
        print(src, tag, out[f'{src}_{tag}'], flush=True)
json.dump(out, open('/Users/advaitpaliwal/Scratch/k2-deep/248630648/inj/tls_dropfirst.json', 'w'), indent=1)
