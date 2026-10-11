# per-campaign version of ../../scripts/prep.py
import sys, json, numpy as np; sys.path.insert(0, '/Users/advaitpaliwal/Scratch/k2-deep/212726424/scripts'); import lcs2 as lcs
epic, P, T0, dur = 212726424, float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])/24
D = f'/Users/advaitpaliwal/Scratch/k2-deep/{epic}'
out = {}
for seg in ['c06', 'c17']:
  for name in ['everest', 'k2sff', 'k2sc', 'fresh']:
    try:
        r = lcs.fresh(epic, P, T0, dur, seg=seg)[:2] if name == 'fresh' else getattr(lcs, name)(epic, seg)
    except Exception as e: print(seg, name, 'ERR', e); continue
    if r is None: continue
    t, f = r; tf, ff = lcs.flat(t, f, P, T0, dur)
    np.savez(f'{D}/lc/{name}_{seg}.npz', t_raw=t, f_raw=f, t=tf, f=ff)
    d, e, n = lcs.boxdepth(tf, ff, P, T0, dur)
    out[f'{name}_{seg}'] = dict(n=len(tf), rms_ppm=float(np.std(ff)*1e6), box_depth_ppm=float(d*1e6), box_err_ppm=float(e*1e6), n_in=n, snr=float(d/e))
    print(seg, name, out[f'{name}_{seg}'], flush=True)
json.dump(out, open(f'{D}/lc/depths_box.json', 'w'), indent=1)
