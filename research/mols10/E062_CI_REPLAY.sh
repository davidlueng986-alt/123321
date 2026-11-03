#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python E062_public_pair.py
python - <<'PY_SMALL'
import sys,json
from pathlib import Path
from E062_scan_wanless_pairs import enumerate_common,packing_best,construct_third,check_pair
base=Path('E061_dlx_runs.jsonl')
for z in map(json.loads,base.read_text().splitlines()):
    n=z['n']
    if n not in (4,5):continue
    A,B,C=z['witness'];check_pair(A,B)
    tr,nodes=enumerate_common(A,B);p=packing_best(tr,n)
    assert p['status']=='EXACT' and p['size']==n-1,p
    D=construct_third(A,B,tr,p['indices'])
    print('POSITIVE_CONSTRUCTION',n,'PASS')
PY_SMALL
python E062_scan_wanless_pairs.py --input E062_LOCAL_TEST_PAIRS.txt --output E062_EGAN_SCAN_TEST.json
python - <<'PY'
import json
r=json.load(open('E062_EGAN_SCAN_TEST.json'))
assert r['max_common_transversals']==14, r
assert r['disjoint_packing_distribution_exact_or_lowerbound']=={'7':1},r
assert not r['packing_unknown_cases'],r
print('EGAN EXACT CONTROL PASS')
PY
python E062_scan_wanless_pairs.py --output E062_WANLESS_PAIR_SCAN.json --maxpack-nodes 200000
python - <<'PY'
import json
r=json.load(open('E062_WANLESS_PAIR_SCAN.json'))
assert r['source_squares']==5562 and r['source_pairs']==2781,r
assert r['pairs_processed']==2781 or r['complete_witness'] is not None,r
if r['complete_witness'] is not None:
 w=r['complete_witness']; A,B,C=w['A'],w['B'],w['C']
 for M in (A,B,C):
  assert all(set(row)==set(range(10)) for row in M)
  assert all({M[r][c] for r in range(10)}==set(range(10)) for c in range(10))
 for X,Y in ((A,B),(A,C),(B,C)):
  assert len({(X[r][c],Y[r][c]) for r in range(10) for c in range(10)})==100
 print('CLOSED: INDEPENDENT TRIPLE VERIFIED')
else:
 print('PUBLIC DATASET ONLY; GLOBAL STATUS OPEN')
print('PUBLIC PAIRS:',r['pairs_processed'],'MAX TR=',r['max_common_transversals'],'UNKNOWN PACKINGS:',len(r['packing_unknown_cases']))
PY