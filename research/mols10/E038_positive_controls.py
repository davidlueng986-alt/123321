#!/usr/bin/env python3
"""Triad forcing must not reject prefixes of known complete prime-order 3-MOLS."""
import sys,json
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from E038_triads import triad
res=[]
for n in (5,7,11):
 full=[[[ (r+a*c)%n for c in range(n)] for r in range(n)] for a in (1,2,3)]
 for k in (2,3,4):
  S=[A[:k] for A in full]
  w=triad(S)
  assert w is None,(n,k,w)
  res.append({'n':n,'k':k,'triad':False,'known_full_triple':True})
print(json.dumps({'status':'PASS','positive_controls':res},indent=2))