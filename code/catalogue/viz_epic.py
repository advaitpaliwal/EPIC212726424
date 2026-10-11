import warnings; warnings.filterwarnings('ignore')
from astroquery.vizier import Vizier
kws=['K2 ultra-short period planets','ExoMiner','K2 planet candidates','K2 Earth-sized','K2 transit candidates','Scaling K2','Kruse K2','K2 machine learning candidates','K2 validated planets']
cats={}
for kw in kws:
    try:
        for k,v in Vizier.find_catalogs(kw).items(): cats[k]=v.description
    except Exception as e: print('find',kw,e)
for k in ['J/AJ/155/21','J/ApJS/244/11','J/AJ/162/259','J/AJ/155/136','J/AJ/152/47','J/AJ/154/31','J/AJ/161/261','J/MNRAS/509/1075','J/ApJS/222/14','J/AJ/151/159']: cats.setdefault(k,'(explicit)')
print('N catalogues',len(cats),flush=True)
for k,d in sorted(cats.items()):
    try:
        meta=Vizier(row_limit=1,columns=['**']).get_catalogs(k)
    except Exception as e: print(k,'ERR meta',e); continue
    for t in meta:
        tn=t.meta.get('name'); cols=[c for c in t.colnames if 'EPIC' in c.upper() or c in ('ID','Name','Star','K2','Host')]
        hit=None
        for c in cols:
            for val in (['212726424','EPIC 212726424','EPIC212726424'] if c not in ('ID',) else ['212726424']):
                try:
                    r=Vizier(row_limit=5,columns=['**'],column_filters={c:f'={val}' if val.isdigit() else val}).query_constraints(catalog=tn)
                except Exception as e: r=[]
                if len(r) and len(r[0])<5: hit=(c,val,r[0]); break
            if hit: break
        print(f'{tn} | {d[:80]} | epic_cols={cols} | hit={"YES "+str(list(hit[2][0])) if hit else "no"}',flush=True)
