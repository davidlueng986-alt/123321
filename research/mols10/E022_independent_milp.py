#!/usr/bin/env python3
"""Independent SciPy/HiGHS MILP spot-check for E022 pair-root exact covers.
Independent recursive A-transversal enumeration; does not import E022 solver.
"""
import argparse,hashlib,json,random,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
A=[[0,8,9,7,5,6,4,2,3,1],[9,1,4,6,2,7,3,8,0,5],[7,4,2,5,1,3,8,6,9,0],[8,6,5,3,9,2,1,0,4,7],[6,2,1,8,4,0,9,5,7,3],[4,9,3,2,7,5,0,1,6,8],[5,3,7,1,0,8,6,9,2,4],[3,5,0,9,8,4,2,7,1,6],[1,7,6,0,3,9,5,4,8,2],[2,0,8,4,6,1,7,3,5,9]]

def enumerate_independent():
 out=[]
 def rec(row,usedcols,usedsyms,cells):
  if row==10:
   out.append(sum(1<<c for c in cells));return
  for col in range(10):
   sym=A[row][col]
   if not(usedcols>>col&1) and not(usedsyms>>sym&1):
    rec(row+1,usedcols|1<<col,usedsyms|1<<sym,cells+[10*row+col])
 rec(0,0,0,[])
 return out

def verify_pair(T,roots,seconds=5):
 eligible=[i for i,u in enumerate(T) if all((u&T[r]).bit_count()==1 for r in roots)]
 matrix=lil_matrix((100,len(eligible)),dtype=float)
 for j,k in enumerate(eligible):
  u=T[k]
  while u:
   b=u&-u;u-=b;matrix[b.bit_length()-1,j]=1.
 res=milp(np.zeros(len(eligible)),integrality=np.ones(len(eligible)),bounds=Bounds(0,1),
          constraints=LinearConstraint(matrix.tocsr(),np.ones(100),np.ones(100)),
          options={'time_limit':seconds,'mip_rel_gap':0.0})
 if res.status==0:
  selected=[eligible[j] for j,v in enumerate(res.x) if v>.5]
  assert len(selected)==10
  assert sum(T[j] for j in selected)==(1<<100)-1
  assert all(all((T[j]&T[r]).bit_count()==1 for r in roots) for j in selected)
  return 'SAT',selected
 if res.status==2:return 'UNSAT_EXHAUSTIVE',[]
 return 'UNKNOWN',[]

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',default='E022_REPLAY.json');p.add_argument('--output',default='E022_MILP_REPLAY.json');p.add_argument('--each',type=int,default=15);p.add_argument('--all',action='store_true');args=p.parse_args()
 t0=time.monotonic();r=json.load(open(args.input));T=enumerate_independent()
 assert len(T)==r['transversal_count']==1080
 assert hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest()==r['input_sha256']
 for key,w in r['sat_witnesses'].items():
  roots=list(map(int,key.split(',')))
  assert len(w)==10 and len(set(w))==10
  assert sum(T[j] for j in w)==(1<<100)-1
  assert all(all((T[j]&T[i]).bit_count()==1 for i in roots) for j in w)
 sat=[(list(map(int,k.split(','))),'SAT') for k in r['sat_witnesses']]
 unsat=[(x,'UNSAT_EXHAUSTIVE') for x in r['unsat_pairs']]
 rng=random.Random(20261102)
 chosen=sat+unsat if args.all else [sat[i] for i in sorted(rng.sample(range(len(sat)),min(args.each,len(sat))))]+[unsat[i] for i in sorted(rng.sample(range(len(unsat)),min(args.each,len(unsat))))]
 checks=[]
 for roots,expected in chosen:
  status,w=verify_pair(T,roots)
  checks.append({'roots':roots,'expected':expected,'milp':status,'witness':w})
  if not args.all or len(checks)%200==0:print(len(checks),roots,expected,status,flush=True)
 out={'method':'independent recursive A-transversals + SciPy/HiGHS exact-cover MILP',
      'all_sat_witnesses_verified':len(sat),
      'counts':{'SAT':sum(z['milp']=='SAT' for z in checks),'UNSAT_EXHAUSTIVE':sum(z['milp']=='UNSAT_EXHAUSTIVE' for z in checks),'UNKNOWN':sum(z['milp']=='UNKNOWN' for z in checks)},
      'all_agree':all(z['expected']==z['milp'] for z in checks),'checks':checks,'seconds':round(time.monotonic()-t0,3)}
 with open(args.output,'w') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
