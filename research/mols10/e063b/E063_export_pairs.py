#!/usr/bin/env python3
"""Deterministic pair variant export; also regenerates exhaustive 2+1 results."""
import sys,pathlib,contextlib
P=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(P))
with open(P/'E063_export_prep.log','w') as f,contextlib.redirect_stdout(f):
 import E063_deeper_cotrades as r
for label,variants in [('A2',r.a2),('B2',r.b2)]:
 with open(P/f'E063_{label}_VARIANTS.bin','wb') as f:
  for mat,_ in variants:f.write(bytes(x for row in mat for x in row))
print('A2',len(r.a2),'B2',len(r.b2),'possible_cross',len(r.a2)*len(r.b2))