# -*- coding: utf-8 -*-
import sys, importlib.util, time
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

modfile = sys.argv[1] if len(sys.argv) > 1 else "MacAttack-STB.py"
spec = importlib.util.spec_from_file_location("ma2", modfile)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)

BASE = ma.normalize_base_url("http://vip.rxs1.eu:8080/c/")
MAC = "00:1A:79:14:E1:70"
print(f"[{modfile}] base_url: {BASE}")

sess = ma.create_session_with_retries()
t0 = time.time()
token, rnd = ma.get_token(sess, BASE, MAC, forced_ptype="portal")
print(f"  get_token: {bool(token)} in {time.time()-t0:.2f}s | profile captured: {hasattr(sess,'expire_profile')}")

t0 = time.time()
cats = ma.fetch_categories(sess, BASE, MAC, token, rnd)
print(f"  fetch_categories (parallel): Live={len(cats['Live'])} Movies={len(cats['Movies'])} Series={len(cats['Series'])} in {time.time()-t0:.2f}s")

first = cats["Live"][0] if cats["Live"] else {}
tc = ma.fetch_channel_count(sess, BASE, MAC, token, rnd, first["category_type"], first.get("category_id"))
print(f"  fetch_channel_count: {tc}")

exp = ma.get_expire_date(getattr(sess, "expire_profile", None))
print(f"  get_expire_date: {exp}")

t0 = time.time()
pl, pr = ma.verify_playable(sess, BASE, MAC, token, rnd)
print(f"  verify_playable: playable={pl} reason={pr} in {time.time()-t0:.2f}s")
