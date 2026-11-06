#!/usr/bin/env python3
"""Independent exact-integer verification of a live E070 DLX pruning example.
No NumPy or C++ code reused; all graph and line quadratic forms recomputed.
"""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('E070_DLX_FIRST_EXACT_CERT.json')
x=json.loads(p.read_text());P=x['points'];v=x['integer_test_vector'];n=len(P)
assert len(v)==n and n>=20
assert len(set(map(tuple,P)))==n
for i in range(n):
 for j in range(i):
  assert sum(P[i][d]==P[j][d] for d in range(5))<=1
z_direct=25*sum(a*a for a in v)+2*sum(v)**2
for i in range(n):
 for j in range(n):
  if i!=j and any(P[i][d]==P[j][d] for d in range(5)):
   z_direct-=5*v[i]*v[j]
z_lines=50*sum(a*a for a in v)+2*sum(v)**2
for d in range(5):
 for sym in range(10):
  line=sum(v[i] for i in range(n) if P[i][d]==sym)
  z_lines-=5*line*line
assert z_direct==z_lines==x['exact_negative_quadratic']<0,(z_direct,z_lines)
print(json.dumps({'status':'INDEPENDENT_EXACT_NEGATIVE_INTEGER_PSD_CERTIFICATE','point_count':n,'q_direct':z_direct,'q_line_decomposition':z_lines,'global_branch_closed':False}))
