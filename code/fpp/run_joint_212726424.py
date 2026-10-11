# Joint TRICERATOPS(K2)+MOLUSC FPP for EPIC 212726424. Adapted from ../../201395714/fpp_joint/scripts/run_joint.py (same shim, binning, filt Kepler,
# N=1e6, seed 2000+k, molusc_file) with: both campaigns' EVEREST LCs folded on the joint ephemeris, both campaigns' threshold apertures, parallel=False (4-process cap).
# usage: run_joint_212726424.py VARIANT K   VARIANT in {exp294 (molusc), none294 (no molusc, reference)}
import sys, os, json, pickle, time, glob, types, numpy as np, warnings; warnings.filterwarnings('ignore')
D = '/Users/advaitpaliwal/Scratch/k2-deep/212726424/fpp_joint'; os.chdir(D)
import triceratops.triceratops as tr, triceratops.marginal_likelihoods as ml, lightkurve as lk
class _F:
    def __init__(s, d): s.d = d
    def __getitem__(s, k):
        if isinstance(k, str): return types.SimpleNamespace(values=s.d[k].to_numpy(copy=True))
        return _F(s.d[np.asarray(k)])
_rc = ml.read_csv
ml.read_csv = lambda f, *a, **kw: _F(_rc(f, *a, **kw)) if 'molusc' in str(f) else _rc(f, *a, **kw)
var, k = sys.argv[1], int(sys.argv[2]); exptime = 29.4/1440
epic = 212726424
R = json.load(open('../fit/result_joint_everest.json'))
P, T0, dur, depth = R['P_d'][0], R['T0_BKJD'][0], R['T14_h'][0]/24, R['depth_ppm'][0]*1e-6
camps = [int(c) for c in os.environ.get('CAMPS', '6,17').split(',')]
pk = f'out/target_{epic}_{"_".join(map(str,camps))}.pkl'
if not os.path.exists(pk):
    if os.environ.get('GAIAPATCH'): sys.path.insert(0, D + '/scripts'); import gaia_patch
    tg = tr.target(ID=epic, sectors=np.array(camps), mission='K2', lightkurve_cache_dir=D + '/lkcache', search_radius=10)
    pickle.dump(tg, open(pk, 'wb')); tg.stars.to_csv(f'out/stars_{epic}.csv', index=False)
tg = pickle.load(open(pk, 'rb'))
aps = []
for c in camps:
    tpp = glob.glob(f'/Users/advaitpaliwal/Scratch/k2-deep/{epic}/lc/mastDownload/K2/ktwo{epic}-c{c:02d}_lc/*lpd-targ.fits.gz')[0]
    tp = lk.read(tpp); ap = tp.create_threshold_mask(threshold=3, reference_pixel='center')
    rows, cols = np.nonzero(ap); aps.append(np.column_stack([cols + tp.column, rows + tp.row]))
t = np.concatenate([np.load(f'../lc/everest_c{c:02d}.npz')['t'] for c in camps]); f = np.concatenate([np.load(f'../lc/everest_c{c:02d}.npz')['f'] for c in camps])
ph = t - T0 - np.round((t - T0)/P)*P; w = np.abs(ph) < 0.3
edges = np.arange(-0.3, 0.3 + 1e-9, 15/1440); idx = np.digitize(ph[w], edges)
tb = np.array([ph[w][idx == i].mean() for i in np.unique(idx)]); fb = np.array([f[w][idx == i].mean() for i in np.unique(idx)])
err = float(np.std(fb[np.abs(tb) > dur]))
tg.calc_depths(tdepth=depth, all_ap_pixels=aps)
mf = None if var.startswith('none') else D + '/molusc_out/molusc_for_trc_N1e6.csv'
np.random.seed(2000 + k); t0 = time.time()
tg.calc_probs(time=tb, flux_0=fb, flux_err_0=err, P_orb=P, contrast_curve_file=None, filt='Kepler', N=1000000, parallel=False,
              exptime=exptime, nsamples=20, verbose=0, molusc_file=mf)
tag = f'{var}_{k}'
tg.probs.to_csv(f'out/probs_{tag}.csv', index=False)
json.dump(dict(epic=epic, variant=var, run=k, seed=2000+k, N=1000000, exptime_min=exptime*1440, camps=camps, P=P, T0=T0, depth_ppm=depth*1e6, err_ppm=err*1e6, nbins=len(tb),
               molusc=mf, filt='Kepler', FPP=float(tg.FPP), NFPP=float(tg.NFPP), n_stars=len(tg.stars), sec=time.time() - t0, apertures=[a.tolist() for a in aps]), open(f'out/res_{tag}.json', 'w'), indent=1)
print(tag, tg.FPP, tg.NFPP, len(tg.stars), round(time.time() - t0), flush=True)
