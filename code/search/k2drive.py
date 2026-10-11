"""Collect detections above threshold from res/*.jsonl and vet each new one. Appends to res/vet.jsonl."""
import json, glob, csv, os, sys, traceback
sys.path.insert(0, os.path.dirname(__file__))
from k2vet import vet, LC

SDE, SNR, NTR = 9.0, 7.0, 3
H = os.path.expanduser("~/Scratch/k2-hunt")
T = {(int(r["EPIC"]), int(r["Camp"])): r for r in csv.DictReader(open(f"{H}/targets_all.csv"))}
done = set()
vf = f"{H}/res/vet.jsonl"
if os.path.exists(vf):
    for l in open(vf):
        j = json.loads(l); done.add((j["epic"], j["camp"], round(j["P"], 4)))
dets = []
for f in glob.glob(f"{H}/res/w*.jsonl"):
    for l in open(f):
        j = json.loads(l)
        for s in j.get("signals") or []:
            if s["sde"] >= SDE and s["snr"] >= SNR and s["ntr"] >= NTR:
                dets.append((j["epic"], j["camp"], s))
vf_out = vf if len(sys.argv) < 3 else f"{H}/res/vet_{sys.argv[1]}.jsonl"
for g in glob.glob(f"{H}/res/vet*.jsonl"):
    for l in open(g):
        j = json.loads(l); done.add((j["epic"], j["camp"], round(j["P"], 4)))
with open(vf_out, "a") as fo:
    for epic, c, s in dets:
        if len(sys.argv) > 2 and (epic % int(sys.argv[2])) != int(sys.argv[1]): continue
        key = (epic, c, round(s["period"], 4))
        if key in done: continue
        row = T[(epic, c)]
        try:
            r = vet(epic, c, s["period"], s["t0"], s["duration"],
                    R=float(row["Rstar"]) if row["Rstar"] else None,
                    M=float(row["Mstar"]) if row["Mstar"] else None,
                    ra=float(row["_RA"]), dec=float(row["_DE"]), gaia_id=None)
        except Exception as ex:
            r = dict(epic=epic, camp=c, P=s["period"], gate="err", fail=str(ex)[:150])
        r.update(sde=s["sde"], snr_tls=s["snr"], depth_tls=s["depth"], ntr=s["ntr"], dist=row["Dist"], Rstar=row["Rstar"], Teff=row["Teff"])
        fo.write(json.dumps(r, default=float) + "\n"); fo.flush()
        print(epic, c, round(s["period"], 4), r.get("gate"), r.get("fail", ""))
        done.add(key)

# delete light curves for stars whose detections all failed
import collections
st = collections.defaultdict(list)
for l in (x for g in glob.glob(f"{H}/res/vet*.jsonl") for x in open(g)):
    j = json.loads(l); st[(j["epic"], j["camp"])].append(j.get("gate"))
pend = {(e, c) for e, c, s in dets if (e, c, round(s["period"], 4)) not in done}
for (e, c), gs in st.items():
    if "pass" not in gs and (e, c) not in pend:
        for pre in ("ev", "sff"):
            p = f"{LC}/{pre}_{e}_c{c}.fits"
            if os.path.exists(p): os.remove(p)
