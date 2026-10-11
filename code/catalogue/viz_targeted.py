import warnings; warnings.filterwarnings('ignore')
from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord
c=SkyCoord(202.74308*u.deg,-7.60062*u.deg)
out=open('vizier_targeted.txt','w'); url=open('vizier_targeted.txt.url','w')
for cat in ['J/AJ/170/183','J/AJ/165/193','J/A+A/657/A7','J/ApJS/247/28']:
    v=Vizier(columns=['**','_r'],row_limit=50,timeout=120)
    r=v.query_region(c,radius=5*u.arcsec,catalog=cat)
    url.write(f'https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-source={cat}&-c=202.74308%20-7.60062&-c.rs=5\n')
    for t in r: out.write(f'### {cat} {t.meta.get("name")} {t.meta.get("description")}\n'); 
    for t in r:
        for row in t: out.write(' | '.join(f'{n}={row[n]}' for n in t.colnames)+'\n')
# catalogue search by keyword, then EPIC lookup in each found catalogue
kws=['K2 ultra-short period','K2 planet candidates','ExoMiner K2','K2 Earth-sized planets','K2 transiting candidates','Scaling K2','K2 short period planets']
seen={}
for kw in kws:
    try:
        for k,v in Vizier.find_catalogs(kw).items(): seen[k]=v.description
    except Exception as e: out.write(f'find {kw} ERR {e}\n')
url.write('astroquery Vizier.find_catalogs(%s) then query_region 5 arcsec + EPIC constraint\n'%kws)
for k,d in sorted(seen.items()):
    try:
        r=Vizier(columns=['**'],row_limit=-1,timeout=120).query_region(c,radius=10*u.arcsec,catalog=k)
        n=sum(len(t) for t in r)
        r2=[]
        for col in ['EPIC','EPIC_ID','ID']:
            try:
                r2=Vizier(columns=['**'],row_limit=5,timeout=60,column_filters={col:'212726424'}).query_constraints(catalog=k)
                if len(r2): break
            except Exception: pass
        n2=sum(len(t) for t in r2)
        out.write(f'{k} | {d[:90]} | cone10as={n} epic_match={n2}\n')
        for t in list(r)+list(r2):
            for row in t: out.write('   HIT '+' | '.join(f'{nn}={row[nn]}' for nn in t.colnames[:25])+'\n')
    except Exception as e: out.write(f'{k} ERR {e}\n')
    out.flush()
