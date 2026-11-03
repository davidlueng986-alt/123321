from pathlib import Path
import json,itertools,collections
M=json.load(open(str(Path(__file__).with_name('E061_near_triple.json'))))['squares'];n=10

def trades(Q):
  out=[]
  for a,b in itertools.combinations(range(n),2):
    edges=[]
    for r in range(n):
      ca=Q[r].index(a);cb=Q[r].index(b);edges.append((ca,cb))
    parent=list(range(n))
    def find(x):
      while x!=parent[x]:x=parent[x]
      return x
    for ca,cb in edges:
      x,y=find(ca),find(cb);parent[x]=y
    blocks=collections.defaultdict(list)
    for r,(ca,cb) in enumerate(edges):blocks[find(ca)].append(r)
    if len(blocks)<2:continue
    for rows in blocks.values():
      if len(rows)<n:
        out.append((a,b,tuple(rows)))
  return out

def move(Q,tr):
  a,b,rows=tr
  for r in rows:
    Q[r]=[b if x==a else a if x==b else x for x in Q[r]]

def check(Q):
  assert all(sorted(row)==list(range(n)) for row in Q)
  assert all(sorted(Q[r][c] for r in range(n))==list(range(n)) for c in range(n))

def score(M):
  return tuple(len({(M[a][r][c],M[b][r][c]) for r in range(n) for c in range(n)}) for a,b in ((0,1),(0,2),(1,2)))

out=[];allmoves=[];best=(sum(score(M)),score(M),None)
for s in range(3):
  ts=trades(M[s]);out.append({'square':s,'nontrivial_trades':len(ts),'smallest_rows':min((len(z[2]) for z in ts),default=0),'largest_rows':max((len(z[2]) for z in ts),default=0)})
  for t in ts:
    V=[[row[:] for row in Q] for Q in M];move(V[s],t);check(V[s]);sc=score(V)
    allmoves.append((s,t))
    if sum(sc)>best[0]:best=(sum(sc),sc,(s,t));print('IMPROVE',best,flush=True)
print('RESULT',out,'total',len(allmoves),'best',best)
json.dump({'trades':out,'tested_single_moves':len(allmoves),'best_overlay_sum':best[0],'best_overlay':best[1],'best_move':best[2]},open(str(Path(__file__).with_name('E061_symbol_trades.json')),'w'),indent=2)