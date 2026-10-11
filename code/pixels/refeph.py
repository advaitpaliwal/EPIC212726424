import lightkurve as lk, numpy as np, glob, warnings, json; warnings.filterwarnings('ignore')
from astropy.timeseries import BoxLeastSquares
out={}
for c in ['c06','c17']:
    p=glob.glob(f'mastDownload/K2/ktwo212496592-{c}_lc/*lpd-targ.fits.gz')[0]
    tp=lk.read(p, quality_bitmask='default'); ap=tp.create_threshold_mask(3, reference_pixel='center')
    lc=tp.to_lightcurve(aperture_mask=ap).remove_nans(); lc=lc[np.isfinite(lc.centroid_col.value)]
    lc=lk.SFFCorrector(lc).correct(windows=20,bins=15).flatten(window_length=41).remove_outliers(sigma_upper=4,sigma_lower=20)
    t=lc.time.value; f=lc.flux.value
    b=BoxLeastSquares(t,f); P=np.linspace(2.855,2.862,3000); r=b.power(P,0.09)
    i=np.argmax(r.power); out[c]=dict(P=float(r.period[i]),T0=float(r.transit_time[i]),depth_ppm=float(r.depth[i]*1e6),snr=float(r.depth_snr[i]))
    print(c,out[c],flush=True)
json.dump(out,open('ref_ephem.json','w'),indent=1)
