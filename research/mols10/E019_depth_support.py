#!/usr/bin/env python3
"""Reproducible fixed-Parker-A depth-k common-transversal support audit.
A chosen set of B symbol classes can extend to a C square only if each cell
lies in some A-transversal meeting every chosen B class exactly once.
This script checks only this necessary condition; no unrestricted claim.
"""
import argparse, hashlib, itertools, json, random, time
PARKER_A = [
[0,4,1,7,2,9,8,3,6,5],
[8,1,5,2,7,3,9,4,0,6],
[9,8,2,6,3,7,4,5,1,0],
[5,9,8,3,0,4,7,6,2,1],
[7,6,9,8,4,1,5,0,3,2],
[6,7,0,9,8,5,2,1,4,3],
[3,0,7,1,9,8,6,2,5,4],
[1,2,3,4,5,6,0,7,8,9],
[2,3,4,5,6,0,1,8,9,7],
[4,5,6,0,1,2,3,9,7,8]]

def enumerate_transversals(A):
 n=len(A); out=[]
 def dfs(r,cols,syms,mask):
  if r==n:out.append(mask);return
  for c in range(n):
   s=1<<A[r][c];b=1<<c
   if not(cols&b or syms&s):dfs(r+1,cols|b,syms|s,mask|(1<<(n*r+c)))
 dfs(0,0,0,0)
 return out

def audit(A, sample=20000, seed=19):
 start=time.monotonic();n=len(A);T=enumerate_transversals(A);m=len(T)
 refs=[0]*(n*n)
 for i,mask in enumerate(T):
  for r in range(n*n):
   if mask>>r&1:refs[r]|=1<<i
 compatible=[];disjoint=[]
 for i,mask in enumerate(T):
  ci=di=0
  for j,other in enumerate(T):
   h=(mask&other).bit_count()
   if h==1:ci|=1<<j
   if h==0:di|=1<<j
  compatible.append(ci);disjoint.append(di)
 def blocker(possible):
  return next((c for c,ref in enumerate(refs) if not possible&ref),None)
 pair_total=pair_blocked=0; blocked_pairs=[];good_pairs=[]
 for i in range(m):
  for j in range(i+1,m):
   if not (disjoint[i]>>j&1):continue
   pair_total+=1
   bad=blocker(compatible[i]&compatible[j])
   if bad is not None:
    pair_blocked+=1
    if len(blocked_pairs)<4:blocked_pairs.append([i,j,bad])
   else:good_pairs.append((i,j))
 # Exhaustive rooted depth-3 slice: all unordered (0,j,k) with pairwise disjoint classes.
 root=0;root_triples=root_blocked=root_new_blocked=0;root_witness=None
 for j in range(1,m):
  if not (disjoint[root]>>j&1):continue
  for k in range(j+1,m):
   if not (disjoint[root]>>k&1 and disjoint[j]>>k&1):continue
   root_triples+=1
   possible=compatible[root]&compatible[j]&compatible[k]
   b=blocker(possible)
   if b is not None:
    root_blocked+=1
    if blocker(compatible[root]&compatible[j]) is None and blocker(compatible[root]&compatible[k]) is None and blocker(compatible[j]&compatible[k]) is None:
     root_new_blocked+=1
     if root_witness is None:root_witness=[root,j,k,b]
 rng=random.Random(seed)
 # Sample disjoint triples by drawing surviving pairs and a third disjoint class.
 attempted=valid_triples=blocked_triples=0;examples=[]
 for _ in range(sample):
  i,j=good_pairs[rng.randrange(len(good_pairs))]
  eligible=disjoint[i]&disjoint[j]
  if not eligible:continue
  v=eligible; skip=rng.randrange(v.bit_count())
  for _ in range(skip):v&=v-1
  k=(v&-v).bit_length()-1
  attempted+=1
  b=blocker(compatible[i]&compatible[j]&compatible[k])
  valid_triples+=1
  if b is not None:
   blocked_triples+=1
   if len(examples)<10:examples.append([i,j,k,b])
 return dict(schema='MOLS10-E019-depth3-v1',input_sha256=hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest(),transversals=m,disjoint_pairs=pair_total,pair_support_blocked=pair_blocked,pair_surviving=pair_total-pair_blocked,blocked_pair_examples=blocked_pairs,rooted_at=0,root_disjoint_triples=root_triples,root_blocked_triples=root_blocked,root_new_depth3_blocked=root_new_blocked,root_new_witness=root_witness,seed=seed,sample=sample,triples_attempted=attempted,triples_blocked=blocked_triples,triples_survived=valid_triples-blocked_triples,blocked_triple_examples=examples,elapsed_seconds=round(time.monotonic()-start,3),status='BOUNDED_SUPPORT_AUDIT_NOT_GLOBAL_PROOF')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--sample',type=int,default=20000);p.add_argument('--seed',type=int,default=19);p.add_argument('--output',default='E019_RESULTS.json');a=p.parse_args()
 result=audit(PARKER_A,a.sample,a.seed)
 print(json.dumps(result,indent=2))
 with open(a.output,'w') as f:json.dump(result,f,indent=2);f.write('\n')
