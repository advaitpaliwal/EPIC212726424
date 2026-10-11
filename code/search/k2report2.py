"""For survivors (gate==pass): folded plot, radius, catalogue cross-checks."""
import json, csv, os, sys, re
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from k2tls_hunt import load_everest, clean
from k2vet import load_sff, phase

H = os.path.expanduser("~/Scratch/k2-hunt")
S = f"{H}/_sources"
HELD = os.path.expanduser("~/Scratch/planet-hunt/held/_sources")

k2p = {}
for r in csv.DictReader(open(f"{S}/k2pandc.csv")):
    e = re.sub(r"\D", "", r["epic_hostname"]); k2p.setdefault(e, []).append(f'{r["pl_name"]}:{r["disposition"]}:P={r["pl_orbper"][:8]}')
def sections(n):
    out, cur = {}, None
    for line in open(f"{S}/{n}.tsv", errors="ignore"):
        if line.startswith("#Table"): cur = line.split()[1].rstrip(":"); continue
        if cur and not line.startswith("#"):
            for e in re.findall(r"\b2[0-9]{8}\b", line):
                out.setdefault(cur, {}).setdefault(e, []).append(re.sub(r"\s+", " ", line.strip())[:90])
    return out
WANT = {"J_AJ_162_259": ["J_AJ_162_259_table1"], "J_ApJS_244_11": ["J_ApJS_244_11_table7", "J_ApJS_244_11_table9"],
        "J_AJ_155_136": ["J_AJ_155_136_Planets"], "J_AJ_157_169": ["J_AJ_157_169_table1", "J_AJ_157_169_table3"]}
cats = {}
for n, tabs in WANT.items():
    sec = sections(n)
    cats[n] = {t: sec.get(t, {}) for t in tabs}
    print(n, {t: len(v) for t, v in cats[n].items()}, file=sys.stderr)
def incat(n, e):
    return {t: v[str(e)] for t, v in cats[n].items() if str(e) in v}

def radec_list(fn, rcol, dcol):
    out = []
    for r in csv.DictReader(open(fn, errors="ignore")):
        try: out.append((float(r[rcol]), float(r[dcol]), r))
        except Exception: pass
    return out
toi = radec_list(f"{HELD}/toi_2026-10-10.csv", "RA", "Dec")
ctoi = radec_list(f"{HELD}/ctoi_2026-10-10.csv", "RA", "Dec")

def near(lst, ra, dec, r=30):
    o = []
    for a, d, row in lst:
        s = np.hypot((a - ra) * np.cos(np.radians(dec)), d - dec) * 3600
        if s < r: o.append((round(s, 1), row.get("TOI") or row.get("CTOI"), row.get("Period (days)")))
    return o

T = {(int(r["EPIC"]), int(r["Camp"])): r for r in csv.DictReader(open(f"{H}/targets_all.csv"))}
os.makedirs(f"{H}/plots", exist_ok=True)
for l in (l for g in __import__("glob").glob(f"{H}/res/run2_vet_*.jsonl") for l in open(g)):
    j = json.loads(l)
    if j.get("gate") != "pass": continue
    e, c, P, t0, dur = j["epic"], j["camp"], j["P"], j["t0"], j["dur"]
    row = T[(e, c)]; ra, dec = float(row["_RA"]), float(row["_DE"])
    R = float(row["Rstar"]); dep = j.get("fit_depth") or j["depth_ev"]
    rp = np.sqrt(dep) * R * 109.1
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a, (lab, (t, f)) in zip(ax, [("EVEREST", clean(*load_everest(e, c))), ("K2SFF", clean(*load_sff(e, c)))]):
        ph = phase(t, P, t0) * 24
        m = np.abs(ph) < 6 * max(dur, 0.06) * 24
        a.plot(ph[m], f[m], ".", ms=2, color="0.5")
        b = np.linspace(ph[m].min(), ph[m].max(), 60); idx = np.digitize(ph[m], b)
        a.plot([ph[m][idx == i].mean() for i in range(1, 60) if (idx == i).sum()], [f[m][idx == i].mean() for i in range(1, 60) if (idx == i).sum()], "o", color="k", ms=4)
        a.set_title(f"EPIC {e} C{c} {lab}  P={P:.5f} d"); a.set_xlabel("hours from mid-transit"); a.set_ylabel("rel. flux")
    fn = f"{H}/plots/epic{e}_c{c}_P{P:.4f}.png"; fig.tight_layout(); fig.savefig(fn, dpi=110); plt.close(fig)
    out = dict(epic=e, camp=c, gaia=row["Gaia"], P=P, t0_bkjd=t0, depth_ppm=dep * 1e6, dur_h=j.get("T14", dur) * 24,
               snr=j["snr_ev"], Rstar=R, Rp_earth=round(rp, 2), dist_pc=row["Dist"], Teff=row["Teff"], plot=fn,
               k2pandc=k2p.get(str(e), []), zink21=incat("J_AJ_162_259", e), kruse19=incat("J_ApJS_244_11", e),
               mayo18=incat("J_AJ_155_136", e), dattilo19=incat("J_AJ_157_169", e),
               toi_30as=near(toi, ra, dec), ctoi_30as=near(ctoi, ra, dec))
    print(json.dumps(out, default=str))
