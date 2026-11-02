#!/usr/bin/env python3
"""Exact 3-demand Farkas motifs: d1+d2 <= d3 on EVERY candidate.
Fast support-set implementation, independently replayed by JS verifier.
Only FIXED partial prefixes are excluded.
"""
import sys,json,time,collections
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));from E035_column_residual import model
D=json.load(open(BASE/'E037_ALL_CYCLES.json'))
def triad(S):
 A,T,E=model(S);m=len(E);n=len(T);B=A.tocsc();resources=[B.indices[B.indptr[j]:B.indptr[j+1]].tolist() for j in range(n)]
 assert all(len(v)==6 for v in resources)
 support=[0]*m;forced=[(1<<m)-1]*m
 for j,rr in enumerate(resources):
  bits=sum(1<<i for i in rr)
  for i in rr:support[i]|=1<<j;forced[i]&=bits
 groups={}
 for i,mask in enumerate(forced):
  if not support[i]:continue
  mask &= ~(1<<i)
  while mask:
   bit=mask & -mask;k=bit.bit_length()-1;mask^=bit
   groups.setdefault(k,[]).append(i)
 for target,indices in groups.items():
  for ai,i in enumerate(indices):
   for j in indices[ai+1:]:
    if E[i][:2]==E[j][:2]:continue # beyond single bipartite Hall
    if not(support[i]&support[j]):
     return {'positive':[list(E[i]),list(E[j])],'negative':list(E[target]),'candidate_count':n,'demand_count':m}
 return None
if __name__=="__main__":
 stats=collections.Counter();examples=[];allresults=[];t=time.time()
 for block in D['cycle_results']:
  for idx,z in enumerate(block['results']):
   if z['status']=='UNSAT_BY_SUPPORT':continue
   w=triad(z['prefix']);stats['tested']+=1
   if w:
    stats['triad_found']+=1
    if not z['hall15']:stats['triad_beyond_Hall15']+=1
    allresults.append({'cycle':block['cycle'],'index':idx,'hall15':z['hall15'],'witness':w})
   else:stats['no_triad']+=1
  print('cycle',block['cycle'],dict(stats),flush=True)
 obj={'scope':'E037 317 LP-infeasible fixed four-row prefixes with no zero support','stats':dict(stats),'results':allresults,'seconds':round(time.time()-t,2)}
 open(str(BASE/'E038_TRIADS.json'),'w').write(json.dumps(obj,separators=(',',':'))+'\n')
 print('FINAL',dict(stats),'seconds',obj['seconds'],flush=True)