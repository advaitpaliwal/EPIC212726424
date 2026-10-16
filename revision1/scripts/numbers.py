# Prints every number quoted in rnaas_rev1.md, read from the k2-deep and prerev files.
import json, csv, numpy as np, sys
K='~/Scratch/k2-deep/212726424/'; P='~/Scratch/planet-hunt/prerev/scripts/'
J=lambda f: json.load(open(K+f))
r=J('fit/result_joint_everest.json')
for k in ['P_d','T0_BJD_TDB','RpRs','a_Rs','b','depth_ppm','T14_h','Rp_earth','Teq_K','S_earth']:
    v=r[k]; print('joint',k, v[0], '-',v[1],'+',v[2])
print('joint keys', [k for k in r if k not in ('P_d',)])
for c in ['c06','c17']:
    x=J(f'fit/result_{c}_everest.json'); print(c,'P',x['P_d'],'depth',x['depth_ppm'])
    # period agreement
p6=J('fit/result_c06_everest.json')['P_d']; p17=J('fit/result_c17_everest.json')['P_d']
e6=np.mean(p6[1:]); e17=np.mean(p17[1:]); print('dP sigma', abs(p6[0]-p17[0])/np.hypot(e6,e17))
t6=J('fit/result_c06_everest.json')['T0_BKJD'][0]; t17=J('fit/result_c17_everest.json')['T0_BKJD'][0]
for n in range(638,643):
    Pn=(t17-t6)/n; print('n',n,'P',Pn,'sig vs c06',(Pn-p6[0])/e6,'vs c17',(Pn-p17[0])/e17)
db=J('lc/depths_box.json')
for k,v in db.items(): print('box',k, round(v['box_depth_ppm'],1), round(v['box_err_ppm'],1), v['n_in'])
for f in ['everest_joint','everest_c06','everest_c17','k2sff_c06','k2sff_c17','fresh_c06','fresh_c17','k2sc_c06']:
    v=J(f'fit/vet_{f}.json'); print('vet',f,'oe',round(v['odd_even_sigma'],2),'chi2',round(v['per_transit_chi2'],1),v['per_transit_dof'],'sec',[round(a,1) for a in v['secondary_phase0.5'][:2]])
for c in ['c06','c17']:
    d=J(f'inj/inj_{c}.json'); print('inj',c,sum(x['recovered_period'] for x in d if x['mode']=='inj'),'/',sum(x['mode']=='inj' for x in d))
th=J('fit/thruster.json')
for c in th: print('thr',c,{k:th[c][k] for k in ['P_over_Pthr','firing_phase_coherence_on_P','coherence_expected_random']})
pd=json.load(open(P+'../scripts/chi2_defs.json')) if False else None
for c in ['c06','c17']:
    t=J(f'pix/diff_{c}.json'); rf=J(f'pix/ref/diff_K2-191_{c}.json')
    def g(d):
        d=d.get('target',d); return {k:d.get(k) for k in ['n_in','offset_arcsec','offset_sigma','offset_from_catalog_arcsec']}
    print('pix',c,'target',g(t)); print('pix',c,'K2-191',g(rf))
nd=J('pix/neighbours_diff.json'); print('neigh', json.dumps(nd)[:900])
s=J('fpp_joint/summary.json')
for v in ['exp294','none294']:
    f=s[v]['FPP']; print('FPP',v,f['mean'],f['sd'],f['min'],f['max'],'<=0.035',f['runs_le_0.035'],'n',len(f['all']),'NFPP',s[v]['NFPP'])
print('STP',s['exp294']['scenarios']['STP']['mean'],'PTP',s['exp294']['scenarios']['PTP']['mean'],'TP',s['exp294']['scenarios']['TP']['mean'])
rows=list(csv.DictReader(open(K+'fpp_joint/run_results_exp294.csv'))); print('n_stars',set(r['n_stars'] for r in rows),'N',set(r['N'] for r in rows))
tc=J('tess/tess_check.json'); print('tess S91 expected snr', tc['sectors']['91']['expected_snr'])
print(open(K+'fpp_joint/molusc_summary.txt').read().splitlines()[0:3])
