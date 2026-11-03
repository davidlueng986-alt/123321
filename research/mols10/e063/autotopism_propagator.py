#!/usr/bin/env python3
"""Exhaustive *autotopism* search via Latin quasigroup propagation.
Given row, column, symbol permutations f,g,h, insist h(Q[r,c]) = Q[f(r),g(c)].
This is only autotopism (not full autoparatopism), and can exclude a C
from any 3-MOLS(10) using McKay-Meynert-Myrvold (2007) if nontrivial exists.
"""
import json,time,sys
from pathlib import Path
D=Path(__file__).parent
Q=json.load(open(D/'C7_all_complete.json'))['C_completions'][int(sys.argv[1])]
N=10
invrow=[[row.index(s) for s in range(N)] for row in Q]
invcol=[[next(r for r in range(N) if Q[r][c]==s) for s in range(N)] for c in range(N)]
alltr=[(r,c,Q[r][c]) for r in range(N) for c in range(N)]
start=time.monotonic();limit=float(sys.argv[2]) if len(sys.argv)>2 else 5;nodes=0;found=[];timed=False

def setmap(m,s,t):
 if m[s]>=0:return m[s]==t,False
 if t in m:return False,False
 m[s]=t;return True,True

def propagate(f,g,h):
 changed=True
 while changed:
  changed=False
  for r,c,s in alltr:
   rr=f[r];cc=g[c];ss=h[s]
   if rr>=0 and cc>=0:
    ok,new=setmap(h,s,Q[rr][cc]);
    if not ok:return False
    changed|=new
   elif rr>=0 and ss>=0:
    ok,new=setmap(g,c,invrow[rr][ss]);
    if not ok:return False
    changed|=new
   elif cc>=0 and ss>=0:
    ok,new=setmap(f,r,invcol[cc][ss]);
    if not ok:return False
    changed|=new
 return True

def dfs(f,g,h):
 global nodes,timed
 nodes+=1
 if (nodes&1023)==0 and time.monotonic()-start>limit:timed=True;return False
 if not propagate(f,g,h):return False
 if min(f)>=0 and min(g)>=0 and min(h)>=0:
  assert all(Q[f[r]][g[c]]==h[Q[r][c]] for r in range(N) for c in range(N))
  if f!=list(range(N)) or g!=list(range(N)) or h!=list(range(N)):
   found.append({'row_perm':f,'col_perm':g,'symbol_perm':h})
   return True
  return False
 # Choose an unmatched column (most connected to assigned row/symbol relations)
 choices=[(sum(f[r]>=0 and h[Q[r][c]]>=0 for r in range(N)),c) for c in range(N) if g[c]<0]
 if choices:typ=1;k=max(choices)[1];avail=[c for c in range(N) if c not in g]
 elif any(v<0 for v in f):typ=0;k=f.index(-1);avail=[v for v in range(N) if v not in f]
 else:typ=2;k=h.index(-1);avail=[v for v in range(N) if v not in h]
 for v in avail:
  ff,gg,hh=f[:],g[:],h[:];[ff,gg,hh][typ][k]=v
  if dfs(ff,gg,hh):return True
  if timed:return False
 return False

for rr in range(N):
 for cc in range(N):
  f=[-1]*N;g=[-1]*N;h=[-1]*N
  f[0]=rr;g[0]=cc;h[Q[0][0]]=Q[rr][cc]
  if dfs(f,g,h):break
  if timed:break
 if timed or found:break
out={'rep':int(sys.argv[1]),'status':'AUTOTOPISM_FOUND' if found else 'UNKNOWN_TIME' if timed else 'NO_NONTRIVIAL_AUTOTOPISM','nodes':nodes,'seconds':round(time.monotonic()-start,3),'certificate':found[0] if found else None,'scope':'autotopism, not full autoparatopism'}
(D/f'E063_autotopism_{sys.argv[1]}.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='certificate'}),flush=True)