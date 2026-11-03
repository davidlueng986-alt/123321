#!/usr/bin/env python3
"""Exact BFS of orthogonality-preserving two-symbol trade graph (fixed cell indexing).
If queue empties: this trade-connected component is exhausted, NOT all 2-MOLS(10).
"""
import pathlib,json,collections,time,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('component',D/'E063_component_trade_graph.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
m=h.m

def key(A,B):return bytes(x for S in (A,B) for row in S for x in row)

def neighbors(A,B):
 for side,(X,Y) in enumerate([(A,B),(B,A)]):
  for x in range(10):
   for y in range(x+1,10):
    comps=h.get_components(X,Y,x,y)
    if len(comps)<=1:continue
    for subset in range(1,(1<<len(comps))-1):
     Z=[row[:] for row in X]
     for i,comp in enumerate(comps):
      if subset>>i&1:
       for r,c in comp:Z[r][c]=y if Z[r][c]==x else x
     if side==0:yield Z,Y
     else:yield Y,Z

def main():
 X=json.load(open(D/'E061_near_triple.json'))['squares'];A,B=X[0],X[2]
 seen={key(A,B)};q=collections.deque([(A,B)]);out={'status':'IN_PROGRESS','source':'Egan A/C',
 'visited_pairs':0,'trade_edges_tested':0,'max_transversals':0,'max_packing':0,'eight_packing_candidates':0,'closure_witness':None,
 'pair_distributions':collections.Counter(),'time_limit_seconds':20}
 t0=time.monotonic()
 while q and len(seen)<=2000 and time.monotonic()-t0<20:
  aa,bb=q.popleft();out['visited_pairs']+=1
  assert m.validate(aa,bb)
  T,_=m.exact_transversals(aa,bb);r=m.max_disjoint(aa,bb,T)
  out['pair_distributions'][(len(T),r['best_found_pack'])]+=1
  out['max_transversals']=max(out['max_transversals'],len(T));out['max_packing']=max(out['max_packing'],r['best_found_pack'])
  if r['best_found_pack']>=8:out['eight_packing_candidates']+=1
  if r['closure_found']:
   out['closure_witness']=m.build_full(aa,bb,T,r);break
  for ac,bc in neighbors(aa,bb):
   out['trade_edges_tested']+=1
   k=key(ac,bc)
   if k not in seen:
    seen.add(k);q.append((ac,bc))
  if out['visited_pairs']%100==0:print('PROGRESS',out['visited_pairs'],len(q),out['max_packing'],flush=True)
 out['status']='CLOSED_WITNESS_VERIFIED' if out['closure_witness'] is not None else ('EXACT_FINITE_TRADE_COMPONENT_EXHAUSTED' if not q else 'UNKNOWN_BUDGET')
 out['total_seen_pairs']=len(seen);out['queue_unprocessed']=len(q);out['seconds']=round(time.monotonic()-t0,4)
 out['pair_distributions']={f'{k[0]},{k[1]}':v for k,v in out['pair_distributions'].items()}
 (D/'E063_TRADENET_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
 print('SUMMARY',json.dumps({k:v for k,v in out.items() if k not in ('pair_distributions','closure_witness')},indent=2),flush=True)

if __name__=='__main__':main()