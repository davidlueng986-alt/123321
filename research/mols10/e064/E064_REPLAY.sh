#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for f in E064_generate_ordered E064_burnside E064_quotient E064_firstcol_dlx E064_support_screen; do
    g++ -O3 -std=c++17 "$f.cpp" -o "$f"
done
./E064_generate_ordered > E064_ordered_orbit_counts.jsonl
./E064_burnside > E064_independent_burnside.jsonl
./E064_quotient > E064_quotient_counts.txt
./E064_support_screen E064_12_representatives.jsonl > E064_all1700_root_support.json
python E064_small_order_control.py
python - <<'PY_CHECK'
from pathlib import Path
import json,collections
A=[json.loads(x) for x in open('E064_ordered_orbit_counts.jsonl') if x.startswith('{')]
B=[json.loads(x) for x in open('E064_independent_burnside.jsonl') if x.startswith('{')]
assert len(A)==len(B)==8
for a,b in zip(A,B):
    assert a['type']==b['type'] and a['centralizer']==b['centralizer']
    assert a['allowed_g']==b['allowed_g'] and a['g_orbits']==b['orbits']
assert len(Path('E064_ordered_representatives.jsonl').read_text().splitlines())==16085
assert len(Path('E064_quotient_representatives.jsonl').read_text().splitlines())==2877
lines=Path('E064_12_representatives.jsonl').read_text().splitlines();assert len(lines)==1700
hist=collections.Counter();weighted=0
for line in lines:
  a=json.loads(line);x=a['B_col0'];y=a['C_col0'];hist[a['S3xC2_orbit_size']]+=1;weighted+=a['S3xC2_orbit_size']
  assert x[0]==y[0]==0 and sorted(x)==sorted(y)==list(range(10))
  assert all(x[i]!=i and y[i]!=i and x[i]!=y[i] for i in range(1,10))
assert weighted==16085 and dict(hist)=={1:8,2:8,3:115,4:2,6:516,12:1051}
assert json.load(open('E064_all1700_root_support.json'))['total_reps']==1700
assert json.load(open('E064_all1700_root_support.json'))['support_unsat_reps']==0
v=json.load(open('E064_small_order_cover_12.json'))
assert [r['global_orbits'] for r in v]==[1,2,3]
assert [r['branch_results'].get('SAT',0) for r in v]==[1,1,0]
print('E064_COMPLETE_CLASSIFICATION_AND_SMALL_ORDER_CONTROLS_PASS')
PY_CHECK