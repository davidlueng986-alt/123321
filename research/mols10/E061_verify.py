#!/usr/bin/env python3
"""Independent replay of E061 positive witnesses, data scopes and theorem controls.
This does not itself constitute an exhaustive order-10 UNSAT certificate.
"""
import json,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent

def verify_triple(S):
 n=len(S[0]);assert len(S)==3;X=set(range(n))
 for A in S:
  assert len(A)==n and all(len(row)==n and set(row)==X for row in A)
  assert all({A[r][c] for r in range(n)}==X for c in range(n))
 vals=[len({(S[a][r][c],S[b][r][c]) for r in range(n) for c in range(n)}) for a,b in [(0,1),(0,2),(1,2)]]
 assert vals==[n*n]*3
 return vals

base=[json.loads(x) for x in open(D/'E061_dlx_runs.jsonl')]
assert [x['n'] for x in base]==[3,4,5,6,10]
assert [x['status'] for x in base]==['UNSAT_EXHAUSTIVE','SAT','SAT','UNSAT_EXHAUSTIVE','UNKNOWN_BUDGET']
for x in base:
 if x['status']=='SAT':assert verify_triple(x['witness'])==[x['n']**2]*3
f=[json.loads(x) for x in open(D/'E061_12types.jsonl')]
assert len(f)==12 and len({x['cycle_type'] for x in f})==12
assert all(x['status']=='UNKNOWN_BUDGET' for x in f)
pair=json.load(open(D/'E061_pair_random_seeds.json'))
assert len(pair)==10 and all(x['status']=='UNKNOWN_BUDGET' for x in pair)
route=json.load(open(D/'E061_transversal_route.json'))
assert route['controls'][0]['overlays']==[16]*3
assert route['controls'][1]['overlays']==[25]*3
assert route['controls'][2]['max_disjoint']==7
finaltwo=json.load(open(D/'E061_two_transversal_completion.json'))
assert all(x['bipartite'] for x in finaltwo['controls'])
trade=json.load(open(D/'E061_three_cycle_trade_results.json'))
assert trade['best']==291 and trade['nodes']>=3000000
trades2=json.load(open(D/'E061_two_symbol_trades.json'))
assert trades2['best_overlay_sum']==291
k6=json.load(open('/mnt/data/E060_ALL_84_SIX_ROW_RESULTS.json')) if (Path('/mnt/data/E060_ALL_84_SIX_ROW_RESULTS.json')).exists() else None
if k6:assert (k6['anchors'],k6['complete_unsets'],k6['unknown'])==(84,84,0)
print(json.dumps({'E061_exact_controls':'PASS','small_orders':[(x['n'],x['status']) for x in base[:4]],'full_n10_status':'UNKNOWN','12_canonical_cycle_types':'12/12 UNKNOWN','neartriple_cycle_trade_depth3':'NO_IMPROVEMENT','constructive_transversal_lemma':'PASS_n4_n5','Egan_pair_max_packing':7,'full_problem':'OPEN'},indent=2))