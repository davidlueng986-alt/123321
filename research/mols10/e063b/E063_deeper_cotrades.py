#!/usr/bin/env python3
"""Two valid sequential two-symbol Latin cycle trades on ONE square, at most one on OTHER.
Each intermediate matrix is Latin by construction; no change in row/column indexing.
Pair orthogonality is checked exactly. NO global inference.
"""
import importlib.util,json,itertools,time,pathlib
P=pathlib.Path(__file__).parent
z=importlib.util.spec_from_file_location('e063',P/'E063_cotrade_search.py');e=importlib.util.module_from_spec(z);z.loader.exec_module(e)
m=e.m
S=json.load(open(P/'E061_near_triple.json'))['squares'];A,B=S[0],S[1]

def key(x):return tuple(v for row in x for v in row)

def variants_2(base,one):
 seen={key(base)};out=[];count=0
 for i,(A,aa) in enumerate(one):
  for Z,bb in e.twosym_component_trades(A):
   count+=1;k=key(Z)
   if k in seen:continue
   seen.add(k);out.append((Z,{'first':aa,'second':bb}))
 print('TWO_TRADE_VARIANTS',len(one),len(out),count,flush=True)
 return out

a1=e.twosym_component_trades(A);b1=e.twosym_component_trades(B)
a2=variants_2(A,a1);b2=variants_2(B,b1)
# prefix + one move; no need recompute any Latin validation for generated variants.
bases=[(A,{'base':True})]+a1;shortB=[(B,{'base':True})]+b1
start=time.monotonic();hits=[];seenPairs=set();counts={'A_two_B_at_most_one':0,'B_two_A_at_most_one':0}
for tag,variantA,variantB in [('A_two_B_at_most_one',a2,shortB),('B_two_A_at_most_one',bases,b2)]:
 for ai,(AA,ka) in enumerate(variantA):
  for bi,(BB,kb) in enumerate(variantB):
   counts[tag]+=1
   if e.ov(AA,BB):
    kp=(key(AA),key(BB))
    if kp in seenPairs:continue
    seenPairs.add(kp);assert m.validate(AA,BB)
    T,n=m.exact_transversals(AA,BB);r=m.max_disjoint(AA,BB,T,node_cap=400000)
    hits.append({'from':tag,'A':ka,'B':kb,'total_transversals':len(T),'max_pack':r['best_found_pack'],'closure_found':r['closure_found']})
    print('ORTHOGONAL_PAIR_FOUND',tag,ai,bi,len(T),r['best_found_pack'],flush=True)
    if r['closure_found']:
     C=m.build_full(AA,BB,T,r)
     (P/'E063_CLOSED_WITNESS.json').write_text(json.dumps({'squares':C},indent=2))
     raise SystemExit('COMPLETE_TRIPLE_FOUND')
 print('FINISHED_BLOCK',tag,counts[tag],'elapsed',round(time.monotonic()-start,2),flush=True)
only_relabels=all((lambda v:v['first']['symbols']==v['second']['symbols'] and (v['first']['subset']&v['second']['subset'])==0 and (v['first']['subset']|v['second']['subset'])==(1<<v['first']['components'])-1)(h['A'] if h['from'].startswith('A_') else h['B']) for h in hits)
assert only_relabels, 'new non-isotopic pair found; investigate immediately'
result={'status':'ONLY_WHOLE_SYMBOL_RELABELLINGS_SURVIVE' if only_relabels else 'NEW_NONTRIVIAL_ORTHOGONAL_PAIR_FOUND',
 'A_one_trade_variants':len(a1),'B_one_trade_variants':len(b1),
 'A_two_trade_unique_variants':len(a2),'B_two_trade_unique_variants':len(b2),
 'candidate_count_by_family':counts,'orthogonal_new_pairs':hits,
 'elapsed_seconds':round(time.monotonic()-start,4),
 'scope':'at most two sequential two-symbol Latin cycle trades in A and at most one in B, OR reversed; original pair excluded; not an unrestricted search'}
(P/'E063_DEEP_COTRADE_RESULTS.json').write_text(json.dumps(result,indent=2))
print('FINAL',json.dumps({k:v for k,v in result.items() if k!='orthogonal_new_pairs'}),flush=True)