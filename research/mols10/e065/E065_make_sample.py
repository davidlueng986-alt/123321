import json,random
L=[json.loads(s) for s in open('E064_12_representatives.jsonl')]
by={}
for i,z in enumerate(L):by.setdefault(tuple(z['type']),[]).append(i)
indices=[]
for ty,a in by.items():
 indices.extend([a[0],a[len(a)//2]])
rng=random.Random(20261104)
indices+=rng.sample([i for i in range(1700) if i not in indices],16)
assert len(indices)==32 and len(set(indices))==32
with open('E065_32_sample_reps.jsonl','w') as o:
 for i in indices:
  z=dict(L[i]);z['original_branch_index']=i;o.write(json.dumps(z)+'\n')
json.dump({'indices':indices,'types':[L[i]['type'] for i in indices]},open('E065_sample_manifest.json','w'),indent=2)
print(json.dumps({'total':len(indices),'types':[list(x) for x in by],'first_sixteen':indices[:16]}))