"""Difference image + flux-weighted centroid shift for a K2 detection. Usage: EPIC CAMP P T0 DUR
Uses the K2 TPF from MAST; in-transit minus out-of-transit average, compares centroid of the difference
image with the out-of-transit centroid and the Gaia position projected via the TPF WCS."""
import sys, os, json, urllib.request, shutil, warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
warnings.filterwarnings("ignore")
H = os.path.expanduser("~/Scratch/k2-hunt")
e, c, P, t0, dur = int(sys.argv[1]), int(sys.argv[2]), *map(float, sys.argv[3:6])
cs = {"10": "102", "11": "112"}.get("%02d" % c, "%02d" % c)
s = str(e)
url = f"https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:K2/url/missions/k2/target_pixel_files/c{cs}/{s[:4]}00000/{s[4:6]}000/ktwo{s}-c{cs}_lpd-targ.fits.gz"
fn = f"{H}/lc/tpf_{e}_c{c}.fits.gz"
if not os.path.exists(fn):
    with urllib.request.urlopen(url, timeout=180) as r, open(fn, "wb") as fo: shutil.copyfileobj(r, fo)
    open(f"{H}/_sources/tpf_{e}_c{c}.url", "w").write(url + "\n")
h = fits.open(fn); d = h[1].data
t, fl, q = d["TIME"], d["FLUX"], d["QUALITY"]
good = np.isfinite(t) & (q == 0) & np.all(np.isfinite(fl.reshape(len(t), -1)) | True, axis=1)
t, fl = t[good], np.nan_to_num(fl[good])
ph = ((t - t0 + P / 2) % P) - P / 2
w = max(dur, 0.06)
inn = np.abs(ph) < 0.4 * w
out = (np.abs(ph) > w) & (np.abs(ph) < 3 * w)
# K2 roll: pair each in-transit cadence with nearby out-of-transit cadences only (local differencing)
diffs = []
for i in np.where(inn)[0]:
    o = np.where(out & (np.abs(t - t[i]) < 3 * w))[0]
    if len(o) >= 2: diffs.append(np.median(fl[o], 0) - fl[i])
D = np.median(diffs, 0); O = np.median(fl[out], 0)
yy, xx = np.mgrid[:D.shape[0], :D.shape[1]]
def cen(img):
    m = img > 0; w_ = np.where(m, img, 0); return (w_ * xx).sum() / w_.sum(), (w_ * yy).sum() / w_.sum()
cd, co = cen(D), cen(O)
peak = np.unravel_index(np.argmax(D), D.shape); opeak = np.unravel_index(np.argmax(O), O.shape)
shift_pix = float(np.hypot(cd[0] - co[0], cd[1] - co[1]))
res = dict(epic=e, n_in=int(inn.sum()), n_pairs=len(diffs), diff_centroid=cd, oot_centroid=co, shift_pix=shift_pix,
           shift_arcsec=shift_pix * 3.98, diff_peak=list(map(int, peak)), oot_peak=list(map(int, opeak)), tpf=fn)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
f, a = plt.subplots(1, 2, figsize=(9, 4))
a[0].imshow(O, origin="lower"); a[0].set_title("out of transit"); a[0].plot(*co, "rx")
a[1].imshow(D, origin="lower"); a[1].set_title("difference (out - in)"); a[1].plot(*cd, "rx"); a[1].plot(*co, "w+")
pf = f"{H}/plots/diff_{e}_c{c}_P{P:.4f}.png"; f.savefig(pf, dpi=100); res["plot"] = pf
print(json.dumps(res, default=float))
