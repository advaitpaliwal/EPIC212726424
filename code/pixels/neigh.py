# Difference-image flux at the Gaia neighbour positions (19.7" G=17.58, 28.6" G=19.22) per campaign, from pix/diff_*.npz; WCS from the TPF.
import numpy as np, glob, json, lightkurve as lk, warnings; warnings.filterwarnings('ignore')
nb = {'gaia_3630391411264580864_G17.58_19.7as': (202.73954789893597, -7.596401222390358), 'gaia_3630391411264578944_G19.22_28.6as': (202.73701333628136, -7.60580042959247), 'target': (202.74322971885326, -7.600642690228004)}
out = {}
for c in ['c06', 'c17']:
    z = np.load(f'pix/diff_{c}.npz'); tp = lk.read(glob.glob(f'lc/mastDownload/K2/ktwo212726424-{c}_lc/*lpd-targ.fits.gz')[0])
    diff, sig, oot, ap = z['diff'], z['sig'], z['oot'], z['ap']; out[c] = {'shape': list(diff.shape)}
    for k, (ra, de) in nb.items():
        x, y = tp.wcs.all_world2pix([[ra, de]], 0)[0]; ix, iy = int(round(x)), int(round(y))
        inside = 0 <= ix < diff.shape[1] and 0 <= iy < diff.shape[0]
        r = dict(colrow=[float(x), float(y)], in_tpf=bool(inside))
        if inside:
            sl = (slice(max(iy-1, 0), iy+2), slice(max(ix-1, 0), ix+2))
            r.update(in_aperture=bool(ap[iy, ix]), diff3x3_e_per_s=float(np.nansum(diff[sl])), diff3x3_snr=float(np.nansum(diff[sl])/np.sqrt(np.nansum(sig[sl]**2))), oot3x3=float(np.nansum(oot[sl])))
        out[c][k] = r
    out[c]['aperture_diff_snr'] = float(np.nansum(diff[ap])/np.sqrt(np.nansum(sig[ap]**2)))
    print(c, json.dumps(out[c]))
json.dump(out, open('pix/neighbours_diff.json', 'w'), indent=1)
