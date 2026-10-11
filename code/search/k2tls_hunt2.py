"""Run 2: same search (k2tls_hunt.run) + same gates (k2vet.vet) + same detection thresholds (k2drive),
continuing down the distance-sorted list. Usage: k2tls_hunt2.py worker_idx nworkers max_rows
Writes res/run2_w{i}.jsonl (search) and res/run2_vet_{i}.jsonl (gates). Stops when res/run2_STOP exists."""
import sys, os, json, csv, glob, urllib.request, shutil
sys.path.insert(0, os.path.dirname(__file__))
import k2tls_hunt, k2vet

H = os.path.expanduser("~/Scratch/k2-hunt"); LC = k2tls_hunt.LC
SDE, SNR, NTR = 9.0, 7.0, 3          # frozen, as in k2drive.py
SKIP = {201395714, 248630648, 246184797}

def fetch(url, path):                 # in-process download (no curl child processes)
    if not os.path.exists(path):
        tmp = path + ".part%d" % os.getpid()
        with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as fo:
            shutil.copyfileobj(r, fo)
        os.rename(tmp, path)
    return path
k2tls_hunt.fetch = fetch; k2vet.fetch = fetch

def rm(e, c):
    for pre in ("ev", "sff"):
        p = f"{LC}/{pre}_{e}_c{c}.fits"
        if os.path.exists(p): os.remove(p)

if __name__ == "__main__":
    wi, nw, maxrows = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rows = list(csv.DictReader(open(f"{H}/targets_all.csv")))
    done = set()
    for g in glob.glob(f"{H}/res/w*.jsonl") + glob.glob(f"{H}/res/run2_w*.jsonl"):
        for l in open(g):
            j = json.loads(l); done.add((j["epic"], j["camp"]))
    todo = [r for r in rows if (int(r["EPIC"]), int(r["Camp"])) not in done and int(r["EPIC"]) not in SKIP][:maxrows]
    todo = todo[wi::nw]
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(3); futs = {}
    def pf(r):
        try: fetch(k2tls_hunt.ev_url(r["EPIC"], r["Camp"]), f"{LC}/ev_{int(r['EPIC'])}_c{int(r['Camp'])}.fits")
        except Exception: pass
    fo = open(f"{H}/res/run2_w{wi}.jsonl", "a"); fv = open(f"{H}/res/run2_vet_{wi}.jsonl", "a")
    for i, row in enumerate(todo):
        if os.path.exists(f"{H}/res/run2_STOP"): break
        if shutil.disk_usage(H).free < 16e9: print("disk low, stopping", flush=True); break
        for r2 in todo[i:i + 6]:
            k = (r2["EPIC"], r2["Camp"])
            if k not in futs: futs[k] = pool.submit(pf, r2)
        futs.pop((row["EPIC"], row["Camp"])).result()
        e, c = int(row["EPIC"]), int(row["Camp"])
        try: o = k2tls_hunt.run(row)
        except Exception as ex: o = dict(epic=e, camp=c, status="err", err=str(ex)[:200])
        o["dist"] = row["Dist"]
        fo.write(json.dumps(o) + "\n"); fo.flush()
        keep = False
        for s in o.get("signals") or []:
            if not (s["sde"] >= SDE and s["snr"] >= SNR and s["ntr"] >= NTR): continue
            try:
                v = k2vet.vet(e, c, s["period"], s["t0"], s["duration"],
                              R=float(row["Rstar"]) if row["Rstar"] else None,
                              M=float(row["Mstar"]) if row["Mstar"] else None,
                              ra=float(row["_RA"]), dec=float(row["_DE"]), gaia_id=None)
            except Exception as ex:
                v = dict(epic=e, camp=c, P=s["period"], gate="err", fail=str(ex)[:150])
            v.update(sde=s["sde"], snr_tls=s["snr"], depth_tls=s["depth"], ntr=s["ntr"], dist=row["Dist"], Rstar=row["Rstar"], Teff=row["Teff"])
            fv.write(json.dumps(v, default=float) + "\n"); fv.flush()
            print(e, c, round(s["period"], 4), v.get("gate"), v.get("fail", ""), flush=True)
            keep |= v.get("gate") in ("pass", "err")
        if not keep: rm(e, c)
