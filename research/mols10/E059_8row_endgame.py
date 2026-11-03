#!/usr/bin/env python3
from pathlib import Path
"""Exact 8-row endgame: enumerate all Latin ways to add the last two rows
in each square independently, then test the 3 orthogonality overlays.
Each square's missing-symbol bipartite graph on 10 columns and 10 symbols
is 2-regular; all perfect matchings can be enumerated by DFS (not heuristic).
Source partial arrays: Jäger et al EJC 2024 Fig. 3, attributed.
Scope only specified 8-row subrectangles of this one 9-row witness.
"""
import itertools,json,collections,time
S=json.load(open(str(Path(__file__).with_name('E059_2024_9x10_analysed.json'))))['published_9x10_rectangles']
n=10;P=((0,1),(0,2),(1,2))
def latin_completions(A):
 assert len(A)==n-2
 miss=[sorted(set(range(n))-{row[c] for row in A}) for c in range(n)]
 assert all(len(z)==2 for z in miss)
 sols=[];row=[None]*n
 def dfs(c,seen):
  if c==n:
   assert seen==(1<<n)-1
   other=[next(x for x in miss[j] if x!=row[j]) for j in range(n)]
   assert sorted(other)==list(range(n))
   sols.append((row[:],other));return
  for x in miss[c]:
   if not (seen>>x&1):
    row[c]=x;dfs(c+1,seen|(1<<x))
 dfs(0,0)
 return sols

def test_partial(W):
 k=len(W[0]);assert all(len(x)==k for x in W)
 for A in W:
  assert all(sorted(row)==list(range(n)) for row in A)
  assert all(len({A[r][c] for r in range(k)})==k for c in range(n))
 for a,b in P:
  assert len({(W[a][r][c],W[b][r][c]) for r in range(k) for c in range(n)})==k*n

def test_complete(W):
 for a,b in P:
  if len({(W[a][r][c],W[b][r][c]) for r in range(n) for c in range(n)})<n*n:return False
 return True

out=[];t0=time.monotonic();best=None
for omitted in range(9):
 W=[[row[:] for i,row in enumerate(A) if i!=omitted] for A in S]
 test_partial(W)
 opts=[latin_completions(A) for A in W]
 # Exact all combinations; some may have duplicate overlays early; no time budget needed.
 sat=0;attempted=0;best_here=None
 for z0,z1,z2 in itertools.product(*opts):
  attempted+=1
  Z=[[row[:] for row in W[s]]+[*x] for s,z in enumerate((z0,z1,z2)) for x in []]
  Z=[W[s]+[list(z[0]),list(z[1])] for s,z in enumerate((z0,z1,z2))]
  overlay=[len({(Z[a][r][c],Z[b][r][c]) for r in range(n) for c in range(n)}) for a,b in P]
  if best_here is None or sum(overlay)>sum(best_here):best_here=overlay
  if min(overlay)==100:
   assert test_complete(Z)
   best={'omitted':omitted,'full_squares':Z}
   sat+=1;break
 item={'omitted_original_row':omitted,'options_by_square':list(map(len,opts)),
       'full_completion_combinations_checked':attempted,'full_sat':sat>0,
       'best_overlay':best_here}
 out.append(item)
 print(json.dumps(item),flush=True)
 if best:break
summary={'status':'COMPLETE_WITNESS_FOUND' if best else 'ALL_NINE_ANCHORED_8_ROW_PREFIXES_EXCLUDED',
         'results':out,'elapsed':round(time.monotonic()-t0,3),
         'any_full_witness':best,
         'scope':'ONLY 9 overlapping eight-row restrictions of a single 2024 published 9x10 example; not unrestricted 3MOLS10'}
json.dump(summary,open(str(Path(__file__).with_name('E059_8ROW_ENDGAME.json')),'w'),indent=2)
print('SUMMARY',json.dumps({k:v for k,v in summary.items() if k not in ('results','any_full_witness')},indent=2))
