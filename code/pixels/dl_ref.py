import lightkurve as lk, warnings; warnings.filterwarnings('ignore')
st = lk.search_targetpixelfile('EPIC 212496592', mission='K2'); print(st)
for r in st: print(r.download(download_dir='/Users/advaitpaliwal/Scratch/k2-deep/212726424/pix/ref').path)
