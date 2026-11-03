#!/usr/bin/env python3
"""Exhaustive search for autoparatopism of each 10x10 Latin square C rep.
A paratopy may permute coordinate roles (row,col,sym), then apply bijections
within each. With 6 coordinate permutations this is 6 isotopism problems.
Witness is independently checked against all 100 cell triples.
"""
import json,itertools,time
from pathlib import Path
D=Path(__file__).parent
Qall=json.loads((D/'C7_all_complete.json').read_text())['C_completions']
reps=json.loads((D/'E063_C_orbits.json').read_text())['representatives']
n=10

def transform(Q,pi):
 T=[[-1]*n for _ in range(n)]
 for r in range(n):
  for c in range(n):
   coords=(r,c,Q[r][c]);a,b,d=(coords[pi[0]],coords[pi[1]],coords[pi[2]])
   assert T[a][b]==-1;T[a][b]=d
 assert all(sorted(row)==list(range(n)) for row in T)
 return T

def isotopy(src,tgt,identity=False):
 rowinv=[[row.index(s) for s in range(n)] for row in tgt]
 colinv=[[next(r for r in range(n) if tgt[r][c]==s) for s in range(n)] for c in range(n)]
 triples=[(r,c,src[r][c]) for r in range(n) for c in range(n)]
 nodes=0;found=None
 def setm(m,j,v):
  if m[j]>=0:return m[j]==v,False
  if v in m:return False,False
  m[j]=v;return True,True
 def propagate(f,g,h):
  changed=True
  while changed:
   changed=False
   for r,c,s in triples:
    rr=f[r];cc=g[c];ss=h[s]
    if rr>=0 and cc>=0:ok,new=setm(h,s,tgt[rr][cc])
    elif rr>=0 and ss>=0:ok,new=setm(g,c,rowinv[rr][ss])
    elif cc>=0 and ss>=0:ok,new=setm(f,r,colinv[cc][ss])
    else:continue
    if not ok:return False
    changed|=new
  return True
 def dfs(f,g,h):
  nonlocal nodes,found
  nodes+=1
  if not propagate(f,g,h):return False
  if min(f)>=0 and min(g)>=0 and min(h)>=0:
   assert all(tgt[f[r]][g[c]]==h[src[r][c]] for r in range(n) for c in range(n))
   if identity and f==list(range(n)) and g==list(range(n)) and h==list(range(n)):return False
   found={'f':f,'g':g,'h':h};return True
  # Propagation ensures all unassigned candidates subject only to injectivity.
  options=[(c,sum(f[r]>=0 and h[src[r][c]]>=0 for r in range(n))) for c in range(n) if g[c]<0]
  if options: typ=1;k=max(options,key=lambda z:z[1])[0];avail=[v for v in range(n) if v not in g]
  elif min(f)<0:typ=0;k=f.index(-1);avail=[v for v in range(n) if v not in f]
  else:typ=2;k=h.index(-1);avail=[v for v in range(n) if v not in h]
  for v in avail:
   ff,gg,hh=f[:],g[:],h[:];[ff,gg,hh][typ][k]=v
   if dfs(ff,gg,hh):return True
  return False
 for rr in range(n):
  for cc in range(n):
   f=[-1]*n;g=[-1]*n;h=[-1]*n
   f[0]=rr;g[0]=cc;h[src[0][0]]=tgt[rr][cc]
   if dfs(f,g,h):return found,nodes
 return None,nodes

out=[];perm=list(itertools.permutations(range(3)))
for idx in reps:
 Q=Qall[idx];ncheck=0;witness=None;t0=time.monotonic();certs=[]
 for pi in perm:
  T=transform(Q,pi)
  found,nodes=isotopy(Q,T,identity=pi==(0,1,2));ncheck+=nodes
  if found:
   # In terms of the original Q relation, (f,g,h) is an isotopy Q -> Q^pi;
   # composing with inverse pi is a genuine autoparatopy.
   assert all(T[found['f'][r]][found['g'][c]]==found['h'][Q[r][c]] for r in range(n) for c in range(n))
   certs.append({'coordinate_perm':pi,**found})
   if witness is None:witness=certs[-1]
   # stop once any nontrivial paratopy is witnessed
   break
 row={'rep':idx,'status':'NONTRIVIAL_AUTOPARATOPY' if witness else 'TRIVIAL_AUTOPARATOPY','nodes':ncheck,'seconds':round(time.monotonic()-t0,3),'witness':witness}
 out.append(row);print('REP',idx,row['status'],'nodes',ncheck,'secs',row['seconds'],flush=True)
json.dump({'scope':'All fourteen isotopy classes of 216 completions of one C7 partial pattern','cases':out,'count_nontrivial':sum(x['witness'] is not None for x in out),'current_status':'not global CLOSED'},open(D/'E063_full_C_autoparatopy_audit.json','w'),indent=2)