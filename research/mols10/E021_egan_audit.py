#!/usr/bin/env python3
"""E021 Egan first-square unary screen: exact complete negative-control for
Parker's compact unary obstruction (Egan survivors cover every cell)."""
import json
from E021_independent_replay import audit

EGAN = [
 [0,8,9,7,5,6,4,2,3,1],
 [9,1,4,6,2,7,3,8,0,5],
 [7,4,2,5,1,3,8,6,9,0],
 [8,6,5,3,9,2,1,0,4,7],
 [6,2,1,8,4,0,9,5,7,3],
 [4,9,3,2,7,5,0,1,6,8],
 [5,3,7,1,0,8,6,9,2,4],
 [3,5,0,9,8,4,2,7,1,6],
 [1,7,6,0,3,9,5,4,8,2],
 [2,0,8,4,6,1,7,3,5,9]]
if __name__=='__main__':
 result=audit(EGAN)
 result['case']='Egan published first A'
 with open('E021_EGAN_RESULTS.json','w') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))
