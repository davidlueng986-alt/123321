#!/usr/bin/env python3
"""Independent exact verifier for E063's FINITE fixed-C-pattern orbit closure claims.
This script does NOT certify unrestricted 3-MOLS(10) nonexistence.
No LP/SAT solver, networkx, or other package required.
"""
import itertools,json,collections,copy
from pathlib import Path
D=Path(__file__).parent
n=10
prefix=json.loads((D/'C7_all_complete.json').read_text())['Cfixed']
stored=json.loads((D/'C7_all_complete.json').read_text())['C_completions']
group=json.loads((D/'E063_group_actions.json').read_text())
cls=json.loads((D/'E063_C_orbits.json').read_text())
excl=json.loads((D/'E063_symmetric_C_exclusions.json').read_text())

def valid_C(Q):
 assert len(Q)==n and all(len(row)==n and sorted(row)==list(range(n)) for row in Q)
 assert all(sorted(Q[r][c] for r in range(n))==list(range(n)) for c in range(n))
 for r in range(n):
  for c in range(n):
   if prefix[r][c]>=0:assert Q[r][c]==prefix[r][c]

for Q in stored:valid_C(Q)
assert len(stored)==216 and len({tuple(v for row in Q for v in row) for Q in stored})==216
# Independent exhaustive DFS using 1/2/3 symbol placements for 30 holes.
usedcols=[set() for _ in range(3)];Q=[row[:] for row in prefix];cols=[[c for c in range(n) if prefix[r][c]<0] for r in range(n)]
assert all(len(x)==3 for x in cols)
regenerated=set()
def dfs(r):
 if r==n:
  regenerated.add(tuple(v for row in Q for v in row));return
 for perm in itertools.permutations([1,2,3]):
  if any(c in usedcols[v-1] for c,v in zip(cols[r],perm)):continue
  for c,v in zip(cols[r],perm):usedcols[v-1].add(c);Q[r][c]=v
  dfs(r+1)
  for c,v in zip(cols[r],perm):usedcols[v-1].remove(c);Q[r][c]=-1
dfs(0)
assert len(regenerated)==216 and regenerated=={tuple(v for row in Q for v in row) for Q in stored}
index={tuple(v for row in Q for v in row):i for i,Q in enumerate(stored)}

def remap(Q,act):
 rr,cc,ss=act['row_perm'],act['col_perm'],act['symbol_perm']
 assert sorted(rr)==sorted(cc)==sorted(ss)==list(range(n))
 T=[[-1]*n for _ in range(n)]
 for r in range(n):
  for c in range(n):T[rr[r]][cc[c]]=ss[Q[r][c]]
 return T

assert len(group['actions'])==18
maps=[]
for a in group['actions']:
 m=[]
 for Q in stored:
  Y=remap(Q,a)
  m.append(index[tuple(v for row in Y for v in row)])
 assert sorted(m)==list(range(216));maps.append(m)
seen=set();orbits=[]
for i in range(216):
 if i in seen:continue
 orbit={m[i] for m in maps}
 assert all({m[j] for m in maps}==orbit for j in orbit)
 seen|=orbit;orbits.append(sorted(orbit))
assert len(orbits)==14 and orbits==cls['orbits']==group['expected_orbits']
assert collections.Counter(map(len,orbits))=={18:11,6:3}

def validate_autotopism(idx,p):
 Q=stored[idx]
 assert any(p[k]!=list(range(n)) for k in ('row_perm','col_perm','sym_perm'))
 assert all(Q[p['row_perm'][r]][p['col_perm'][c]]==p['sym_perm'][Q[r][c]] for r in range(n) for c in range(n))

assert len(excl['excluded_orbits'])==3
for w in excl['excluded_orbits']:
 assert w['C_index'] in [x[0] for x in orbits if len(x)==6]
 validate_autotopism(w['C_index'],w['nontrivial'])
# Independent negative test: deliberately break the witness at one output index.
x=copy.deepcopy(excl['excluded_orbits'][0])
x['nontrivial']['sym_perm'][0]=(x['nontrivial']['sym_perm'][0]+1)%10
mutation_rejected=False
try:validate_autotopism(x['C_index'],x['nontrivial'])
except AssertionError:mutation_rejected=True
assert mutation_rejected
# Audit all supplied SAT statuses; unknown does not imply UNSAT.
statuses={}
for rep in cls['representatives']:
 data=json.loads((D/f'E063_z3_C{rep}_results.json').read_text())
 assert data['status'] in ('SAT','UNSAT','UNKNOWN')
 statuses[rep]=data['status']
assert len(statuses)==14
out={'status':'E063_FINITE_PATTERN_CERTIFICATES_VERIFIED','C_completions':216,'orbits':14,'orbit_sizes':{'18':11,'6':3},'excluded_by_published_theorem':3,'still_open_C_orbits':11,'z3_statuses':collections.Counter(statuses.values()),'mutated_autotopism_rejected':mutation_rejected,'GLOBAL_MOLS10_STATUS':'OPEN'}
(D/'E063_VERIFICATION.json').write_text(json.dumps(out,indent=2,default=dict))
print(json.dumps(out,indent=2,default=dict))