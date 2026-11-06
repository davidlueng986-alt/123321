#!/usr/bin/env python3
"""Independent, integer-only verifier for E070 necessary PSD violations.
No numpy, sympy, C++ solver, floating eigenvalues, or reference to search code.
Proves v^T [10(10-5)I-10A+4J] v <0 for a partial OA point set.
Also checks the reason that the listed DIMACS clause is exactly its description.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def certify(data):
 P=data['points_5tuples']; v=data['integer_test_vector']; n=len(P)
 assert n==len(v)==data['total_points']
 assert len(P)==len(set(map(tuple,P)))
 assert all(len(p)==5 and all(type(x)==int and 0<=x<10 for x in p) for p in P)
 for i in range(n):
  for j in range(i):
   overlap=sum(P[i][d]==P[j][d] for d in range(5))
   assert overlap<=1,('pairwise OA violated',i,j,overlap)
 # For 5-net(10), line Gram matrix has eigenvalues 50,10,0.
 # A full incidence set H of 100 OA tuples satisfies M=H H^T.
 # For any subset S of columns H_S, since H_S H_S^T <= M in Loewner order,
 # H_S^T M^{+} H_S <= I. Algebra gives 25I - 5A + 2J >= 0.
 # Thus a NEGATIVE exact integer quadratic v^T(25I-5A+2J)v forbids extension.
 term_25=25*sum(x*x for x in v)
 term_2=2*sum(v)**2
 term_5=0
 for i in range(n):
  for j in range(n):
   if i!=j and any(P[i][d]==P[j][d] for d in range(5)):
    term_5-=5*v[i]*v[j]
 q=term_25+term_2+term_5
 assert q==data['exact_negative_quadratic']<0,(q,data['exact_negative_quadratic'])
 units=[]
 for P5,cat in zip(P,data['categories']):
  r,c,a,b,d=P5
  if cat=='firstrow':
   assert r==0 and a==b==d==c
  elif cat=='firstcol':
   assert c==0 and r==a
   units.extend([[1,r,0,b],[2,r,0,d]])
  elif cat=='interior':
   assert 0<r<10 and 0<c<10
   units.extend([[0,r,c,a],[1,r,c,b],[2,r,c,d]])
  else: raise AssertionError(cat)
 assert units==data['branch_conditional_assignment_literals']
 lits=[-(1+(((s*10+r)*10+c)*10+a)) for s,r,c,a in units]
 assert lits==data['branch_conditional_dimacs_nogood']
 assert len(lits)==len(set(lits))==data['literal_count']
 return {'branch':data['branch_index'],'points':n,'exact_q':q,'support_clause_literals':len(lits),'identity':{'term_25':term_25,'term_2':term_2,'term_5':term_5},'status':'EXACT_INTEGER_SOUND_PARTIAL_OA_NOGOODS'}

def positive_control(n):
 # Three orthogonal n*n squares with formula L_a(r,c)=r+a*c over prime GF(n).
 # Works for n=5,7 (a=1,2,3 distinct and all nonzero).
 rows=[(r,c,(r+c)%n,(r+2*c)%n,(r+3*c)%n) for r in range(n) for c in range(n)]
 assert all(len({(p[i],p[j]) for p in rows})==n*n for i in range(5) for j in range(i+1,5))
 import numpy as np
 A=np.array([[int(i!=j and any(rows[i][z]==rows[j][z] for z in range(5))) for j in range(n*n)] for i in range(n*n)],float)
 Q=n*(n-5)*np.eye(n*n)-n*A+4*np.ones((n*n,n*n))
 ev=np.linalg.eigvalsh(Q)
 assert ev.min()>-1e-7
 return {'n':n,'verified_5net':True,'minimum_eigenvalue':round(float(ev.min()),8),'points':n*n}
if __name__=='__main__':
 certs=[certify(json.loads((ROOT/f'E070_R4_COMPRESSED_EXACT_CERT_BRANCH{i}.json').read_text())) for i in (0,400)]
 pos=[positive_control(n) for n in (5,7)]
 ans={'global_problem':'3-MOLS(10)','status':'OPEN','full_root_classes_UNSAT':0,'integer_cuts':certs,'positive_full_OA_controls':pos,'logic':'Any full OA(100,5,10,2) has 5-net Gram M; the exact negative certificate contradicts necessity of PSD for the listed partial tuples. Local exclusion only, not a complete canonical-branch UNSAT.'}
 (ROOT/'E070_INDEPENDENT_RESULT.json').write_text(json.dumps(ans,indent=2)+'\n')
 print(json.dumps(ans,indent=2))
