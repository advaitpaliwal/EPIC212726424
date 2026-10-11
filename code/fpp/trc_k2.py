"""TRICERATOPS (mission='K2') FPP for a K2 candidate. usage: trc_k2.py EPIC CAMP P T0 DUR_H DEPTH_PPM SRC RUN TPFSEG"""
import sys, os, json, pickle, time, numpy as np, warnings; warnings.filterwarnings('ignore')
epic, camp, P, T0, dur, depth, src, k, seg = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])/24, float(sys.argv[6])*1e-6, sys.argv[7], int(sys.argv[8]), sys.argv[9]
D = f'/Users/advaitpaliwal/Scratch/k2-deep/{epic}/fpp'; os.chdir(D)
import triceratops.triceratops as tr, lightkurve as lk
pk = f'out/target_{epic}.pkl'
if not os.path.exists(pk):
    tg = tr.target(ID=epic, sectors=np.array([camp]), mission='K2', lightkurve_cache_dir=D + '/lkcache', search_radius=10)
    pickle.dump(tg, open(pk, 'wb'))
tg = pickle.load(open(pk, 'rb'))
if os.environ.get('PLX'):
    tg.stars.loc[0, 'plx'] = float(os.environ['PLX'])  # Gaia DR3 parallax; TIC row lacks plx
import glob
tpp = [p for p in glob.glob(f'/Users/advaitpaliwal/Scratch/k2-deep/{epic}/lc/mastDownload/K2/*/*lpd-targ.fits.gz') if seg in p][0]
tp = lk.read(tpp)
ap = tp.create_threshold_mask(threshold=3, reference_pixel='center')
rows, cols = np.nonzero(ap); apx = np.column_stack([cols + tp.column, rows + tp.row])
z = np.load(f'/Users/advaitpaliwal/Scratch/k2-deep/{epic}/lc/{src}.npz'); t, f = z['t'], z['f']
ph = t - T0 - np.round((t - T0)/P)*P; w = np.abs(ph) < 0.3
edges = np.arange(-0.3, 0.3 + 1e-9, 15/1440); idx = np.digitize(ph[w], edges)
tb = np.array([ph[w][idx == i].mean() for i in np.unique(idx)]); fb = np.array([f[w][idx == i].mean() for i in np.unique(idx)])
err = float(np.std(fb[np.abs(tb) > dur]))
tg.calc_depths(tdepth=depth, all_ap_pixels=[apx])
np.random.seed(2000 + k); t0 = time.time()
tg.calc_probs(time=tb, flux_0=fb, flux_err_0=err, P_orb=P, contrast_curve_file=None, filt='Kepler', N=1000000, parallel=False,
              exptime=29.4/1440, nsamples=20, verbose=0)
tg.probs.to_csv(f'out/probs_{epic}_{k}.csv', index=False)
tg.stars.to_csv(f'out/stars_{epic}.csv', index=False)
json.dump(dict(epic=epic, run=k, P=P, T0=T0, depth_ppm=depth*1e6, err_ppm=err*1e6, nbins=len(tb), aperture=apx.tolist(), FPP=float(tg.FPP), NFPP=float(tg.NFPP),
               n_stars=len(tg.stars), sec=time.time() - t0, contrast_curve=None, filt='Kepler'), open(f'out/res_{epic}_{k}.json', 'w'), indent=1)
print(epic, k, tg.FPP, tg.NFPP, round(time.time() - t0))
