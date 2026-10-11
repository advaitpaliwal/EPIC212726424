# Re-pickle the K2 target so pandas 2.3.3 (hunt4 venv) can load it: StringDtype columns -> object; values unchanged.
import pickle, warnings, pandas as pd; warnings.filterwarnings('ignore')
D='/Users/advaitpaliwal/Scratch/k2-deep/201395714/fpp_joint/out/'
tg=pickle.load(open(D+'target_201395714.pkl','rb'))
for name,v in list(vars(tg).items()):
    if isinstance(v,pd.DataFrame):
        for c in v.columns:
            if isinstance(v[c].dtype,pd.StringDtype): v[c]=v[c].astype(object)
        v.columns=pd.Index([str(c) for c in v.columns],dtype=object); v.index=pd.Index(list(v.index),dtype=object if v.index.dtype==object or isinstance(v.index.dtype,pd.StringDtype) else v.index.dtype)
        print(name, dict(v.dtypes.astype(str)))
tg.stars.to_csv(D+'stars_from_original_pickle.csv',index=False)
pickle.dump(tg,open(D+'target_201395714_obj.pkl','wb'))
