#!/usr/bin/env python3
"""Independent integer certificate audit, no numpy/scipy/solver imported.
Tests E070 8 cycle-type conditional inequalities and their sound CNF nogoods.
"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
R=[json.loads(s) for s in open(str(Path(__file__).resolve().parent/'E064_12_representatives.jsonl'))]

def check(d):
 i=d['branch_index'];rr=R[i]
 assert d['cycle_type']==rr['type']
 assert d['firstcol_B']==rr['B_col0'] and d['firstcol_C']==rr['C_col0']
 points=d['points_5tuples'];cats=d['categories'];v=d['integer_test_vector'];n=len(points)
 assert n==len(v)==len(cats)==d['total_points']
 assert all(len(p)==5 and min(p)>=0 and max(p)<=9 for p in points)
 assert len(set(map(tuple,points)))==n
 assign=[]
 for p,categ in zip(points,cats):
  row,col,a,b,c=p
  if categ=='firstrow': assert row==0 and col==a==b==c
  elif categ=='firstcol':
   assert 1<=row<10 and col==0 and a==row and b==rr['B_col0'][row] and c==rr['C_col0'][row]
   assign.extend([[1,row,col,b],[2,row,col,c]])
  elif categ=='interior':
   assert row>0 and col>0
   assign.extend([[0,row,col,a],[1,row,col,b],[2,row,col,c]])
  else:raise ValueError(categ)
 assert assign==d['branch_conditional_assignment_literals']
 ll=[-(1+(((s*10+r)*10+c)*10+w))for s,r,c,w in assign]
 assert ll==d['branch_conditional_dimacs_nogood'] and len(ll)==d['literal_count']
 y1=25*sum(x*x for x in v);y2=2*sum(v)**2;y3=0
 for j in range(n):
  for k in range(n):
   if j==k:continue
   agree=sum(points[j][q]==points[k][q] for q in range(5))
   assert agree<=1,('pairwise OA conflict',j,k,agree)
   if agree:y3-=5*v[j]*v[k]
 result=y1+y2+y3
 assert result==d['exact_negative_quadratic'] and result<0
 return {'branch':i,'type':rr['type'],'point_count':n,'clause_len':len(ll),
         'exact_vT_M_v':result,'terms':{'25_norm_v_sq':y1,'2_sum_v_sq':y2,'negative_adj_term':y3},'status':'EXACT_NO_EXTENSION_OF_THIS_PARTIAL_POINT_SET'}

if __name__=='__main__':
 src=json.loads((P/'E070_EIGHT_CYCLE_TYPES_EXACT_CUTS.json').read_text())
 a=[check(d)for d in src['eight_distinct_cycle_types']]
 assert len(a)==8 and len({tuple(x['type'])for x in a})==8
 (P/'E070_EIGHT_CYCLE_INDEPENDENT_RESULTS.json').write_text(json.dumps({'global_status':'OPEN','full_branch_proofs':0,'eight_independent_exact_cuts':a},indent=2)+'\n')
 print(json.dumps(a,indent=2))
