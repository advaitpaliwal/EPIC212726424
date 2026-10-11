import json, glob, csv, re, collections, os
H = os.path.expanduser("~/Scratch/k2-hunt")
srch = [json.loads(l) for f in glob.glob(f"{H}/res/w*.jsonl") for l in open(f)]
ok = [s for s in srch if "signals" in s]
print("searched rows", len(srch), "ok", len(ok), "stars", len({s["epic"] for s in ok}),
      "status", collections.Counter(s.get("status", "ok") for s in srch))
print("campaigns", sorted(collections.Counter(s["camp"] for s in ok).items()))
T = {(int(r["EPIC"]), int(r["Camp"])): r for r in csv.DictReader(open(f"{H}/targets_all.csv"))}
d = [float(T[(s["epic"], s["camp"])]["Dist"]) for s in ok]
print("dist range pc", min(d), max(d))
v = [json.loads(l) for g in glob.glob(f"{H}/res/vet*.jsonl") for l in open(g)]
print("detections vetted", len(v), "stars", len({j["epic"] for j in v}))
def reason(j):
    f = j.get("fail", "")
    for k in ["not in K2SFF", "K2SFF unavailable", "EVEREST/K2SFF depth mismatch", "halves", "epoch depths inconsistent", "fewer than 3",
              "odd/even", "secondary", "V-shaped", "duration too long", "duration too short", "shorter than", "too deep", "shape fit", "Gaia neighbour"]:
        if k in f: return f"{j['gate']}: {k}"
    return f"{j.get('gate')}: {f[:40]}"
print(collections.Counter(reason(j) for j in v).most_common())
# per-star stop: first failure in gate order per star (star rejected only if all its detections fail)
k2p = {}
for r in csv.DictReader(open(f"{H}/_sources/k2pandc.csv")):
    k2p.setdefault(re.sub(r"\D", "", r["epic_hostname"]), set()).add(r["pl_orbper"][:6])
known = [j for j in v if str(j["epic"]) in k2p]
print("vetted detections on k2pandc hosts", len(known), collections.Counter(reason(j) for j in known).most_common())
for j in v:
    if j.get("gate") == "pass": print("PASS", j["epic"], j["camp"], round(j["P"], 4))
