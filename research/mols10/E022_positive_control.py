"""GF(4) positive control: A=x+y, B=x+alpha*y, C=x+alpha^2*y."""
import itertools

def mul(a,b):
 out=0
 for i in range(2):
  for j in range(2):
   if a>>i&1 and b>>j&1:out^=1<<(i+j)
 if out&8:out^=0b1110
 if out&4:out^=0b111
 return out

def sq(slope):return [[x^mul(slope,y) for y in range(4)] for x in range(4)]
A,B,C=[sq(a) for a in (1,2,3)]
for M in (A,B,C):
 assert all(set(row)==set(range(4)) for row in M)
 assert all(set(M[r][c] for r in range(4))==set(range(4)) for c in range(4))
for P,Q in itertools.combinations((A,B,C),2):
 assert len({(P[r][c],Q[r][c]) for r in range(4) for c in range(4)})==16
for i,j in itertools.combinations(range(4),2):
 u={(r,c) for r in range(4) for c in range(4) if B[r][c]==i}
 v={(r,c) for r in range(4) for c in range(4) if B[r][c]==j}
 classes=[{(r,c) for r in range(4) for c in range(4) if C[r][c]==k} for k in range(4)]
 assert all(len(z&u)==len(z&v)==1 for z in classes)
 assert len(set.union(*classes))==16
print('GF4 POSITIVE: 16/16/16, all 6 B-root pairs C-completable')
