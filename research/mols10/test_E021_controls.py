#!/usr/bin/env python3
"""GF(4) independent positive control and exact 3-overlay replay."""
from E021_independent_replay import audit

def mul(a,b):
 p=0
 for i in range(2):
  for j in range(2):
   if (a>>i)&1 and (b>>j)&1:p^=1<<(i+j)
 if p&8:p^=0b1110
 if p&4:p^=0b111
 return p

A=[[r^c for c in range(4)] for r in range(4)]
B=[[r^mul(2,c) for c in range(4)] for r in range(4)]
C=[[r^mul(3,c) for c in range(4)] for r in range(4)]
assert all(sorted(row)==list(range(4)) for M in (A,B,C) for row in M)
assert all(len({(X[r][c],Y[r][c]) for r in range(4) for c in range(4)})==16
           for X,Y in ((A,B),(A,C),(B,C)))
d=audit(A)
assert d['counts']=={'SAT':8,'UNSAT_EXHAUSTIVE':0,'UNKNOWN_BUDGET':0},d
print('GF4: 16/16/16 and all 8 unary roots SAT')
