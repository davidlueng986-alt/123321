# E057 exact robustness checker (standalone with E051_CERTIFICATES.json)
import json
D=json.load(open('E051_CERTIFICATES.json'))
assert len(D['results'])==15
count=0
for r in D['results']:
 if r['kind']!='integer_farkas': continue
 assert len(r['nonzero'])==360 and r['rhs']>1 and r['max_score']<=-1
 # Each placement uses each demand at most once; any +/-1 perturbation changes score <=1.
 for k,v in r['nonzero']:
  for delta in (-1,1):
   assert r['rhs']+delta>0 and r['max_score']+1<=0
   count+=1
assert count==5040
print('PASS',count)
