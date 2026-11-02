#!/usr/bin/env python3
"""GF(9) positive control: genuine nontrivial 3-symbol orthogonality-preserving trade.
GF(9)=F3[a]/(a^2+1), x=low_digit+3*high_digit.
Z=r+c and Q=r+a*c; recolor Z symbols {0,1,2}, fixing row0.
"""
import json
N=9
add=lambda x,y:(x%3+y%3)%3+3*((x//3+y//3)%3)
mulalpha=lambda x:(2*(x//3)%3)+3*(x%3)
z=[[add(r,c) for c in range(N)] for r in range(N)]
q=[[add(r,mulalpha(c)) for c in range(N)] for r in range(N)]
S=[0,1,2]
cells=[(r,c) for r in range(N) for c in range(N) if z[r][c] in S]
groups=[[i for i,(r,c) in enumerate(cells) if (r,c,q[r][c])[dim]==v] for dim in range(3) for v in range(N)]
assert len(cells)==27 and all(len(g)==3 for g in groups)
original=[S.index(z[r][c]) for r,c in cells]
dom=[7]*27
for i,(r,c) in enumerate(cells):
 if r==0:dom[i]=1<<original[i]
def propagate(d):
 changed=True
 while changed:
  changed=False
  for g in groups:
   used=0
   for i in g:
    x=d[i]
    if x&(x-1)==0:
     if used&x:return False
     used|=x
   for i in g:
    if d[i]&(d[i]-1):
     y=d[i]&~used
     if not y:return False
     if y!=d[i]:d[i]=y;changed=True
   for bit in (1,2,4):
    poss=[i for i in g if d[i]&bit]
    if not poss:return False
    if len(poss)==1 and d[poss[0]]!=bit:d[poss[0]]=bit;changed=True
 return True
sol=[]
def dfs(d):
 if not propagate(d):return
 u=[i for i in range(27) if d[i]&(d[i]-1)]
 if not u:
  b=[row[:] for row in z]
  for i,(r,c) in enumerate(cells):b[r][c]=S[d[i].bit_length()-1]
  assert all(len(set(row))==N for row in b)
  assert all(len({b[r][c] for r in range(N)})==N for c in range(N))
  assert len({(b[r][c],q[r][c]) for r in range(N) for c in range(N)})==N*N
  sol.append(b);return
 i=min(u,key=lambda i:d[i].bit_count())
 for bit in (1,2,4):
  if d[i]&bit:
   e=d.copy();e[i]=bit;dfs(e)
dfs(dom)
assert len(sol)==4 and sum(b!=z for b in sol)==3
print(json.dumps({'GF9_normalized_solutions':len(sol),'nontrivial':3,
 'Z_original':z,'Q':q,'Z_trade_example':next(b for b in sol if b!=z)},indent=2))
