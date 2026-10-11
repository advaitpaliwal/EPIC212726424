import json, glob, csv, re, collections, os
H = os.path.expanduser("~/Scratch/k2-hunt")
srch = [json.loads(l) for f in glob.glob(f"{H}/res/run2_w*.jsonl") for l in open(f)]
ok = [s for s in srch if "signals" in s]
print("rows", len(srch), "ok", len(ok), "stars_ok", len({s["epic"] for s in ok}), "stars_all", len({s["epic"] for s in srch}), collections.Counter(s.get("status", "ok") for s in srch))
print("errs", collections.Counter(s.get("err","")[:40] for s in srch if s.get("status")=="err"))
print("campaigns", sorted(collections.Counter(s["camp"] for s in ok).items()))
d = [float(s["dist"]) for s in srch]; print("dist", min(d), max(d))
v = [json.loads(l) for g in glob.glob(f"{H}/res/run2_vet_*.jsonl") for l in open(g)]
print("detections", len(v), "stars", len({(j["epic"],j["camp"]) for j in v}))
def reason(j):
    f = j.get("fail", "")
    for k in ["not in K2SFF", "K2SFF unavailable", "EVEREST/K2SFF depth mismatch", "halves", "epoch depths inconsistent", "fewer than 3",
              "odd/even", "secondary", "V-shaped", "duration too long", "duration too short", "shorter than", "too deep", "shape fit", "Gaia neighbour"]:
        if k in f: return f"{j['gate']}: {k}"
    return f"{j.get('gate')}: {f[:40]}"
print("by gate", collections.Counter(j.get("gate") for j in v))
for k, n in sorted(collections.Counter(reason(j) for j in v).items()): print(" ", n, k)
k2p = {re.sub(r"\D", "", r["epic_hostname"]) for r in csv.DictReader(open(f"{H}/_sources/k2pandc.csv"))}
for j in v:
    if j.get("gate") == "pass": print("PASS", j["epic"], j["camp"], round(j["P"], 4), "known_host" if str(j["epic"]) in k2p else "NEW")
heller = set(re.findall(r"\b2\d{8}\b", " ".join(open(f).read() for f in glob.glob(f"{H}/_sources/heller19/x*/*.tex"))))
print("heller19 EPICs among passes", [j["epic"] for j in v if j.get("gate")=="pass" and str(j["epic"]) in heller])
