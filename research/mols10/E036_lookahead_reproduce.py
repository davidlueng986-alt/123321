#!/usr/bin/env python3
"""E036 bounded row6 diversification and row7/8 feasibility checks (fixed 5-row prefixes).
Only an UNSAT claim for each FIXED prefix when exact DFS exhausts, never global.
Requires python E036_reproduce.py to generate E036_WITNESSES.json first.
"""
import json,hashlib
from E036_reproduce import extend,verify
W=json.load(open('E036_WITNESSES.json'));stats={'row6_SAT':0,'row7_SAT':0,'row7_UNSAT_FIXED_PREFIX':0,'row7_UNKNOWN':0,'row8_SAT':0,'row8_UNSAT_FIXED_PREFIX':0,'row8_UNKNOWN':0};found=[]
for idx,P in enumerate(W):
    for j in range(20):
        R=[[row[:] for row in A[:5]] for A in P]
        try:extend(R,12000+idx*31+j,50000)
        except (AssertionError,RuntimeError):continue
        stats['row6_SAT']+=1
        try:extend(R,22000+idx*31+j,50000)
        except AssertionError:stats['row7_UNSAT_FIXED_PREFIX']+=1;continue
        except RuntimeError:stats['row7_UNKNOWN']+=1;continue
        stats['row7_SAT']+=1;verify(R)
        found.append({'idx':idx,'seed':j,'prefix':[ [row[:] for row in A] for A in R]})
        try:extend(R,32000+idx*31+j,50000)
        except AssertionError:stats['row8_UNSAT_FIXED_PREFIX']+=1
        except RuntimeError:stats['row8_UNKNOWN']+=1
        else:stats['row8_SAT']+=1;verify(R)
        break
print(json.dumps({'status':'OPEN','scope':'fixed five-row prefixes, <=20 row6 choices per g orbit','stats':stats,'k7_indices':[x['idx'] for x in found]},indent=2))
assert stats=={'row6_SAT':3093,'row7_SAT':2,'row7_UNSAT_FIXED_PREFIX':3091,'row7_UNKNOWN':0,'row8_SAT':0,'row8_UNSAT_FIXED_PREFIX':2,'row8_UNKNOWN':0}
with open('E036_K7_WITNESSES.json','w') as out:json.dump(found,out,separators=(',',':'))
