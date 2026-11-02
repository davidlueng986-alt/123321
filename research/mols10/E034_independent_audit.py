#!/usr/bin/env python3
"""Independent semantic replay of E034 solver outputs and the Egan row-subset coverage.
Does not equate enumerated DFS result flags with an external proof certificate.
"""
import json,itertools,collections,hashlib,os
from pathlib import Path
import sys;sys.path.insert(0,str(Path(__file__).resolve().parent))
from E032_residual_hypergraph import structure,unit_propagation
D=Path(__file__).resolve().parent
S=json.load(open(D/'near_triple.json'))['squares']; n=10
P=((0,1),(0,2),(1,2))
def latin_partial(X):
 k=len(X[0]);assert len(X)==3 and all(len(L)==k for L in X)
 for A in X:
  for row in A:assert len(row)==n and set(row)==set(range(n))
  for c in range(n):assert len({A[r][c] for r in range(k)})==k
 return [len({(X[i][r][c],X[j][r][c]) for r in range(k) for c in range(n)}) for i,j in P]
assert latin_partial(S)==[100,100,91]
subsets={k:[] for k in range(4,11)}
for k in range(4,11):
 for rows in itertools.combinations(range(n),k):
  X=[[A[r] for r in rows] for A in S]
  if latin_partial(X)==[n*k]*3:subsets[k].append(rows)
assert len(subsets[4])==39
assert len(subsets[5])==9
assert not any(subsets[k] for k in range(6,11))
manifest=json.load(open(D/'E034_NEAR_PREFIXES.json'))
assert len(manifest)==39 and {tuple(z['rows']) for z in manifest}==set(subsets[4])
for e in manifest:
 data=list(map(int,open(e['file']).read().split()));assert data[0]==4 and len(data)==121
 X=[[[data[1+(r*n+c)*3+s] for c in range(n)] for r in range(4)] for s in range(3)]
 assert all(L[0]==list(range(n)) for L in X)
 assert X[1][1][0]<X[2][1][0]
 assert latin_partial(X)==[40]*3
near=[json.loads(line) for line in open(D/'E034_NEAR_COMPLETE.jsonl')]
assert len(near)==39 and set(z['index'] for z in near)==set(range(39))
assert all(z['status']=='UNSAT_EXHAUSTIVE_NORMALIZED' and not z.get('squares') for z in near)
for z in near:
 if 'deepest_prefix' in z:
  k=len(z['deepest_prefix'][0]);assert latin_partial(z['deepest_prefix'])==[10*k]*3
  assert [z['deepest_prefix'][s][r][c] for s in range(3) for r in range(4) for c in range(n)] == [list(map(int,open(manifest[z['index']]['file']).read().split()))[1+(r*n+c)*3+s] for s in range(3) for r in range(4) for c in range(n)]
global_data=[json.loads(line) for line in open(D/'E034_GLOBAL_CYCLE20M.jsonl')]
assert len(global_data)==12 and len({tuple(z['cycle_type']) for z in global_data})==12
assert all(z['status']=='UNKNOWN_BUDGET' for z in global_data)
for z in global_data:
 k=len(z['deepest_prefix'][0]);assert latin_partial(z['deepest_prefix'])==[10*k]*3
# Independent certificate of six zero-node failures: each residual forbidden edge
# must be assigned a future column; check missing support explicitly.
def column_support(X):
 k=len(X[0]);used=[{(X[i][r][c],X[j][r][c]) for r in range(k) for c in range(n)} for i,j in P]
 missing=[[[a for a in range(n) if a not in {X[s][r][c] for r in range(k)}] for c in range(n)] for s in range(3)]
 ES=[{(a,b) for a in range(n) for b in range(n)}-u for u in used]
 supported=[set(),set(),set()]
 for a,b in ES[0]:
  for c in range(n):
   if (a,c) not in ES[1] or (b,c) not in ES[2]:continue
   if not any(a in missing[0][col] and b in missing[1][col] and c in missing[2][col] for col in range(n)):continue
   supported[0].add((a,b));supported[1].add((a,c));supported[2].add((b,c))
 for j in range(3):
  for e in sorted(ES[j]-supported[j]):return (j,e)
 return None
zeros=[]
for z in near:
 if z['nodes']==0:
  e=manifest[z['index']]
  q=list(map(int,open(e['file']).read().split()))
  X=[[[q[1+(r*n+c)*3+s] for c in range(n)] for r in range(4)] for s in range(3)]
  obs=column_support(X)
  E,T,tri=structure(X)
  missing=[[[v for v in range(n) if v not in {X[s][r][c] for r in range(4)}] for c in range(n)] for s in range(3)]
  filtered=[edges for values,edges in zip(T,tri) if any(all(values[s] in missing[s][c] for s in range(3)) for c in range(n))]
  unit=unit_propagation(sum(map(len,E)),filtered)
  assert obs is not None or unit['status']=='UNIT_UNSAT'
  zeros.append(dict(index=z['index'],rows=e['rows'],unsupported_pair=([obs[0],list(obs[1])] if obs else None),column_aware_unit=unit['status'],candidate_triples=len(filtered)))
result={
 'source_near_triple_overlays':[100,100,91],
 'valid_row_subset_counts':{k:len(v) for k,v in subsets.items()},
 'all_39_four_row_inputs_latin_and_three_overlays_40':True,
 'full_search_prefixes':39,
 'completed_unsat_reports':sum(z['status']=='UNSAT_EXHAUSTIVE_NORMALIZED' for z in near),
 'near_search_nodes_total':sum(z['nodes'] for z in near),
 'near_search_wall_summed':round(sum(z['time'] for z in near),4),
 'six_root_column_support_obstructions':zeros,
 'global_cycle_classes_tested':len(global_data),
 'global_unknown':sum(z['status']=='UNKNOWN_BUDGET' for z in global_data),
 'global_solutions':0,
 'source_sha256':hashlib.sha256((D/'E034_direct_solver.cpp').read_bytes()).hexdigest(),
 'note':'Exhaustive search status derives from a single C++ implementation, not an independently certified full proof. The six zero-node prefix obstructions were independently checked.'
}
(D/'E034_AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))