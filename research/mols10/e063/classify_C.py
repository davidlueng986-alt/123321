import json,itertools,networkx as nx,collections,time
z=json.load(open(str(__import__('pathlib').Path(__file__).with_name('C7_all_complete.json'))));C=z['Cfixed'];Q=z['C_completions'];n=10
G=nx.Graph()
for r in range(n):G.add_node(('r',r),color='row')
for c in range(n):G.add_node(('c',c),color='column')
for r in range(n):
 for c in range(n):
  if C[r][c]<0:G.add_edge(('r',r),('c',c))
node_match=lambda a,b:a['color']==b['color']
gm=nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=node_match)
possible=0;allowed=[];t=time.monotonic();limit=500000
for m in gm.isomorphisms_iter():
 possible+=1
 # aut of missing-edge bipartite graph: preserve seven fixed colors up to some permutation
 ren={};rev={};good=True
 for r in range(n):
  for c in range(n):
   x=C[r][c]
   if x>=0:
    r2=m[('r',r)][1];c2=m[('c',c)][1];y=C[r2][c2]
    if y<0 or (x in ren and ren[x]!=y) or (y in rev and rev[y]!=x):good=False;break
    ren[x]=y;rev[y]=x
  if not good:break
 if good:allowed.append({'r':[m[('r',r)][1] for r in range(n)],'c':[m[('c',c)][1] for c in range(n)],'fixed_relabel':ren})
 if possible>=limit:break
print('missing_incidence_auts',possible,'pattern_strong_auts',len(allowed),'elapsed',round(time.monotonic()-t,3),'exceeded',possible>=limit,flush=True)
# independent verification group maps complete Cs into complete Cs, including missing perm
index={tuple(tuple(row) for row in M):i for i,M in enumerate(Q)}
perms=list(itertools.permutations((1,2,3)))
act=[]
for a in allowed:
 for tail in perms:
  rename={**a['fixed_relabel'],**dict(zip((1,2,3),tail))}
  if set(rename)!=set(range(n)) or len(set(rename.values()))!=n:raise AssertionError('bad map')
  mapping=[]
  for M in Q:
   N=[[None]*n for _ in range(n)]
   for r in range(n):
    for c in range(n):N[a['r'][r]][a['c'][c]]=rename[M[r][c]]
   idx=index.get(tuple(tuple(row) for row in N))
   assert idx is not None
   mapping.append(idx)
  act.append(mapping)
seen=set();orbits=[]
for i in range(len(Q)):
 if i in seen:continue
 orbit={u[i] for u in act};assert all({u[j] for u in act}==orbit for j in orbit)
 seen|=orbit;orbits.append(sorted(orbit))
print('complete_C_216_orbits',len(orbits),'sizes',dict(collections.Counter(map(len,orbits))),'representatives',[o[0] for o in orbits],flush=True)
json.dump({'input_completions':len(Q),'underlying_missing_graph_automorphisms':possible,'strong_pattern_automorphisms':len(allowed),'combined_actions':len(act),'orbits':orbits,'representatives':[o[0] for o in orbits]},open(str(__import__('pathlib').Path(__file__).with_name('E063_C_orbits.json')),'w'),indent=2)