#!/usr/bin/env python3
"""100 deterministic exact row/column/independent-symbol isotopy replays.
Input E041_NEW_22_SPARSE_CERTIFICATE.json; Python standard library only.
"""
import json,random
z=json.load(open('E041_NEW_22_SPARSE_CERTIFICATE.json'))
P=z['source_prefix']
def R(c,a,b,d):
 return (('P',0,a,b),('P',1,a,d),('P',2,b,d),('C',0,c,a),('C',1,c,b),('C',2,c,d))
def check(Q,core,W):
 used=set()
 for j in core:
  r,c=divmod(j,10);a,b,d=[Q[s][r][c] for s in range(3)]
  for k in R(c,a,b,d):
   assert k not in used
   used.add(k)
 assert sum(v for k,v in W.items() if k not in used)==1
 allowed=0;mx=-999
 for c in range(10):
  for a in range(10):
   for b in range(10):
    for d in range(10):
     ks=R(c,a,b,d)
     if any(k in used for k in ks):continue
     allowed+=1;score=sum(W.get(k,0) for k in ks)
     assert score<=0
     mx=max(mx,score)
 assert allowed==2596 and mx==0
W={tuple(k):v for k,v in z['weights']}
rng=random.Random(20261102)
for seed in range(100):
 row=list(range(4));col=list(range(10));sym=[list(range(10)) for _ in range(3)]
 rng.shuffle(row);rng.shuffle(col)
 for v in sym:rng.shuffle(v)
 Q=[[[0]*10 for _ in range(4)] for _ in range(3)]
 for s in range(3):
  for r in range(4):
   for c in range(10):Q[s][row[r]][col[c]]=sym[s][P[s][r][c]]
 core={row[j//10]*10+col[j%10] for j in z['forced_cell_indices']}
 WW={}
 for k,v in W.items():
  if k[0]=='P':
   _,p,a,b=k;s,t=((0,1),(0,2),(1,2))[p];kk=('P',p,sym[s][a],sym[t][b])
  else:
   _,s,c,a=k;kk=('C',s,col[c],sym[s][a])
  WW[kk]=v
 check(Q,core,WW)
print(json.dumps({'status':'EXACT_PASS','transforms':100,'placements_per_transform':10000}))
