#!/usr/bin/env python3
"""R4 Gram-PSD sound-cut oracle for a partial OA(100,5,10,2).
The numerical eigendecomposition only proposes a conflict. A CUT is accepted
only after an exact integer quadratic certificate v^T(25I-5A+2J)v<0.
Any result lacking this strict exact witness is UNKNOWN, never UNSAT.
"""
import argparse,json,math
from pathlib import Path
import numpy as np

def audit_partial(points):
  if len(points)!=len({tuple(p) for p in points}):raise ValueError('duplicate tuples')
  for i,p in enumerate(points):
    if len(p)!=5 or any(not isinstance(x,int) or x<0 or x>9 for x in p):raise ValueError('bad point')
    r,c,a,b,d=p
    if r==0 and not(a==b==d==c):raise ValueError('point violates normalized first row')
    if c==0 and a!=r:raise ValueError('point violates normalized A first column')
    for j in range(i):
      m=sum(p[z]==points[j][z] for z in range(5))
      if m>1:raise ValueError('tuple collection already has OA pairwise conflict')

def coeff(points):
  return [[25*(i==j)+2-5*int(i!=j and any(points[i][k]==points[j][k] for k in range(5)))
           for j in range(len(points))]for i in range(len(points))]

def qform(M,v):
  return sum(v[i]*sum(M[i][j]*v[j] for j in range(len(v)))for i in range(len(v)))

def nogood(points):
  lit=[]
  for r,c,a,b,d in points:
    if r==0:continue
    if c==0:lit.extend([[1,r,0,b],[2,r,0,d]])
    else:lit.extend([[0,r,c,a],[1,r,c,b],[2,r,c,d]])
  ids=sorted({-(1+(((s*10+r)*10+c)*10+w)) for s,r,c,w in lit})
  return ids

def oracle(points):
  points=[list(map(int,p))for p in points]
  audit_partial(points);M=coeff(points)
  eigen,V=np.linalg.eigh(np.array(M,float))
  ret={'points':len(points),'min_float_eigenvalue':float(eigen[0]),'status':'NO_PSD_CONTRADICTION_CERTIFIED'}
  if eigen[0]>=-1e-5:return ret
  best=None
  for scale in [10,15,20,30,50,100,200,500,1000,2000,5000,20000]:
    v=[round(float(x)*scale) for x in V[:,0]]
    gcd=0
    for x in v:gcd=math.gcd(gcd,abs(x))
    if gcd>1:v=[x//gcd for x in v]
    q=qform(M,v)
    if q<0 and (best is None or sum(map(abs,v))<sum(map(abs,best[0]))):best=(v,q)
  if best is None:return ret
  v,q=best
  assert qform(coeff(points),v)==q<0
  ret.update(status='SOUND_NOGOODS_INT_QUADRATIC_CERTIFIED',integer_test_vector=v,
             exact_negative_quadratic=q,
             nogood_dimacs_literals=nogood(points),
             nogood_size=len(nogood(points)),
             scope='partial configuration only; no statement about other completions in full branch')
  return ret

if __name__=='__main__':
  p=argparse.ArgumentParser();p.add_argument('points_json');p.add_argument('--output')
  a=p.parse_args();d=json.loads(Path(a.points_json).read_text());points=d['points_5tuples'] if 'points_5tuples' in d else d['points']
  result=oracle(points)
  if a.output:Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
  print(json.dumps({k:v for k,v in result.items() if k!='integer_test_vector'},indent=2))
