#!/usr/bin/env python3
"""Goal-backward: exact symmetry quotient for cyclic k-row 3-OLS Latin rectangles.
Each square S_s(r,c)=(c+o_s[r]) mod n, row0 offsets all 0.
For valid partial overlays the six offset/difference sets each have k distinct values.
A complete 3-MOLS extension would induce Mx=1 in the *cyclic averaged* LP.
By averaging any feasible full column-aware LP solution under cyclic relabeling,
the quotient is equivalent to full column-aware fractional LP for these inputs.
No proof of global 3-MOLS(10) existence/nonexistence follows from a restricted family.
"""
import numpy as np, random,time,json,sys
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

N=10;K=4

def deltas(o,n=N):
 a,b,c=o
 return [set(a),set(b),set(c),{(b[i]-a[i])%n for i in range(len(a))},
         {(c[i]-a[i])%n for i in range(len(a))},{(c[i]-b[i])%n for i in range(len(a))}]

def valid(o,n=N):
 k=len(o[0]);d=deltas(o,n)
 return len(o)==3 and all(len(x)==k for x in d) and all(o[s][0]==0 for s in range(3))

def quotient(o,n=N):
 assert valid(o,n)
 used=deltas(o,n)
 free=[sorted(set(range(n))-z) for z in used]
 keys=[(t,v) for t in range(6) for v in free[t]]
 idx={z:i for i,z in enumerate(keys)}
 rows=[];cols=[];data=[];choices=[]
 for u in free[0]:
  for v in free[1]:
   if (v-u)%n in used[3]:continue
   for w in free[2]:
    if (w-u)%n in used[4] or (w-v)%n in used[5]:continue
    j=len(choices);choices.append((u,v,w))
    for t,x in enumerate((u,v,w,(v-u)%n,(w-u)%n,(w-v)%n)):
     rows.append(idx[t,x]);cols.append(j);data.append(1)
 A=coo_matrix((data,(rows,cols)),shape=(len(keys),len(choices))).tocsr()
 return A,choices,keys

def screen(o,lp=True):
 A,T,E=quotient(o)
 degrees=np.diff(A.indptr)
 ans={'placements':len(T),'constraints':len(E),'zero_support':int((degrees==0).sum())}
 if ans['zero_support'] or not lp:return ans
 r=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(len(E)),bounds=(0,None),method='highs',options={'time_limit':2})
 ans.update(lp_status=int(r.status),lp_msg=r.message)
 if r.status==0:
  ans['maxerr']=float(np.max(abs(A@r.x-1)))
  ans['nonzero']=[[list(T[i]),float(v)] for i,v in enumerate(r.x) if v>1e-8]
 return ans

def generator(n=N,k=K,seed=0,count=10000):
 rng=random.Random(seed);I=list(range(1,n))
 for t in range(count):
  A=[0]+rng.sample(I,k-1)
  B=[0];C=[0]
  # sequential compatible offsets to minimize bias
  ok=True
  for r in range(1,k):
   arr=[b for b in I if b not in B and (b-A[r])%n not in {(B[q]-A[q])%n for q in range(r)}]
   if not arr:ok=False;break
   b=rng.choice(arr);B.append(b)
   arr=[c for c in I if c not in C and (c-A[r])%n not in {(C[q]-A[q])%n for q in range(r)}
        and (c-b)%n not in {(C[q]-B[q])%n for q in range(r)}]
   if not arr:ok=False;break
   C.append(rng.choice(arr))
  if ok and valid([A,B,C],n):yield [A,B,C]

if __name__=='__main__':
 k=int(sys.argv[1]) if len(sys.argv)>1 else 4
 attempts=int(sys.argv[2]) if len(sys.argv)>2 else 5000
 t0=time.monotonic();stats={'k':k,'attempts':attempts,'tested':0,'zero':0,'lp_unsat':0,'lp_sat':0,'unknown':0,'total_choices':0,'best_choices':0,'example':None}
 for o in generator(k=k,seed=11032026,count=attempts):
  d=screen(o)
  stats['tested']+=1;stats['total_choices']+=d['placements'];stats['best_choices']=max(stats['best_choices'],d['placements'])
  if d['zero_support']:stats['zero']+=1
  elif d['lp_status']==2:stats['lp_unsat']+=1
  elif d['lp_status']==0:
   stats['lp_sat']+=1;stats['example']={'offsets':o,'lp':d}
   break
  else:stats['unknown']+=1
 stats['seconds']=round(time.monotonic()-t0,4)
 print(json.dumps(stats,indent=2))
 with open('/mnt/data/e059/E059_cyclic_result.json','w') as f:json.dump(stats,f,indent=2)