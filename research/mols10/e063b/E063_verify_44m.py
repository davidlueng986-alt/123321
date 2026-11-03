#!/usr/bin/env python3
"""Independently check every C++ reported orthogonal pair and relabel provenance.
C++ scan completeness is deterministic within the documented 44.3M finite family.
"""
import pathlib,json
D=pathlib.Path(__file__).resolve().parent
R=json.load(open(D/'E063_2x2_CROSS_RESULTS.json'))
S=json.load(open(D/'E061_near_triple.json'))['squares'];A,B=S[:2]
A2=(D/'E063_A2_VARIANTS.bin').read_bytes();B2=(D/'E063_B2_VARIANTS.bin').read_bytes()
assert len(A2)==100*9192 and len(B2)==100*4824
assert R['candidates']==9192*4824 and R['orthogonal_hits']==972 and not R['hits_truncated']

def mapping(old,new):
 d={}
 for x,y in zip(old,new):
  if x in d and d[x]!=y:return None
  d[x]=y
 if len(d)!=10 or len(set(d.values()))!=10:return None
 return tuple(d[k] for k in range(10))
A0=[x for row in A for x in row];B0=[x for row in B for x in row]
a_maps=set();b_maps=set();new=[]
for i,j in R['saved_hits']:
 aa=A2[100*i:100*(i+1)];bb=B2[100*j:100*(j+1)]
 assert len({(x,y) for x,y in zip(aa,bb)})==100
 ma=mapping(A0,aa);mb=mapping(B0,bb)
 if ma is None or mb is None:new.append([i,j])
 else:a_maps.add(ma);b_maps.add(mb)
assert len(new)==0 and len(a_maps)==36 and len(b_maps)==27 and len(R['saved_hits'])==36*27
result={'status':'EXACT_FINITE_PAIR_NEIGHBORHOOD_EXHAUSTED_ONLY_RELABELLINGS',
 'A_unique_two_trade_variants':9192,'B_unique_two_trade_variants':4824,'pair_candidates':R['candidates'],
 'orthogonal_hits':R['orthogonal_hits'],'all_hits_independently_orthogonal':True,
 'none_nonrelabel':True,'A_relabelings':len(a_maps),'B_relabelings':len(b_maps),
 'full_3MOLS10_witness':False,
 'scope':'all pairwise combinations of at most 2 sequential two-symbol cycle trades per square, excluding original A/B; one Egan A/B seed only'}
(D/'E063_2x2_VERIFIED_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))