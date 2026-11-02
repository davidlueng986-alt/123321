#!/usr/bin/env python3
"""E021 independent unary exact-cover replay; fixed-A exclusions only.
No E020 imports. Full n! transversal enumeration; memoized remaining-cell
Algorithm X. Node cap is explicit: incomplete roots return UNKNOWN.
"""
import argparse, hashlib, itertools, json, time

PARKER = [
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

def enumerate_masks(a):
 n=len(a)
 assert all(sorted(row)==list(range(n)) for row in a)
 assert all(sorted(a[r][c] for r in range(n))==list(range(n)) for c in range(n))
 masks=[]
 for p in itertools.permutations(range(n)):
  if len({a[r][p[r]] for r in range(n)})==n:
   masks.append(sum(1<<(n*r+p[r]) for r in range(n)))
 return masks

def prepare(masks,n):
 cell_to_ids=[0]*(n*n)
 for j,m in enumerate(masks):
  for c in range(n*n):
   if (m>>c)&1:cell_to_ids[c]|=1<<j
 no_overlap=[]
 for m in masks:
  overlap=0
  for c in range(n*n):
   if (m>>c)&1:overlap|=cell_to_ids[c]
  no_overlap.append(((1<<len(masks))-1)^overlap)
 return cell_to_ids,no_overlap

def test_root(masks,root,cell_to_ids,no_overlap,n,cap=200000):
 universe=(1<<(n*n))-1
 eligible=sum(1<<i for i,m in enumerate(masks) if (m&root).bit_count()==1)
 memo=set();nodes=0;path=[]
 class Limit(Exception):pass
 def visit(remaining,avail):
  nonlocal nodes
  if remaining==0:return True
  if remaining in memo:return False
  nodes+=1
  if nodes>cap:raise Limit
  smallest=None;rem=remaining
  while rem:
   bit=rem&-rem;rem-=bit;cell=bit.bit_length()-1
   choices=cell_to_ids[cell]&avail
   if not choices:
    memo.add(remaining);return False
   if smallest is None or choices.bit_count()<smallest.bit_count():smallest=choices
   if smallest.bit_count()==1:break
  while smallest:
   bit=smallest&-smallest;smallest-=bit;k=bit.bit_length()-1
   path.append(k)
   if visit(remaining^masks[k],avail&no_overlap[k]):return True
   path.pop()
  memo.add(remaining)
  return False
 try:status='SAT' if visit(universe,eligible) else 'UNSAT_EXHAUSTIVE'
 except Limit:status='UNKNOWN_BUDGET';path=[]
 if status=='SAT':
  assert len(path)==n and all(sum(bool(masks[k]>>c&1) for k in path)==1 for c in range(n*n))
  assert all((masks[k]&root).bit_count()==1 for k in path)
 return status,nodes,len(memo),path

def audit(a=None,cap=200000):
 a=PARKER if a is None else a
 n=len(a)
 st=time.monotonic();T=enumerate_masks(a);cell_to_ids,no_overlap=prepare(T,n)
 statuses=[];survivors=[];nodes=0;memo_total=0;maxnodes=0;unknown=[]
 for i,u in enumerate(T):
  status,count,mem,path=test_root(T,u,cell_to_ids,no_overlap,n,cap)
  statuses.append(status);nodes+=count;memo_total+=mem;maxnodes=max(maxnodes,count)
  if status=='SAT':survivors.append(i)
  if status=='UNKNOWN_BUDGET':unknown.append(i)
 coverage=0
 for i in survivors:coverage|=T[i]
 return dict(schema='MOLS10-E021-independent-v1',
  method='10!-permutations + memoized remaining-cell Algorithm X',
  input_sha256=hashlib.sha256(json.dumps(a,separators=(',',':')).encode()).hexdigest(),
  transversals=len(T),
  counts={s:statuses.count(s) for s in ('SAT','UNSAT_EXHAUSTIVE','UNKNOWN_BUDGET')},
  survivors=survivors,uncovered=[c for c in range(n*n) if not coverage>>c&1],
  nodes=nodes,memo_states=memo_total,max_nodes=maxnodes,unknown_roots=unknown,
  cap=cap,elapsed_s=round(time.monotonic()-st,3),
  scope='fixed first Latin square only')

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('--cap',type=int,default=200000)
 ap.add_argument('--out',default='E021_RESULTS.json')
 args=ap.parse_args()
 d=audit(cap=args.cap)
 with open(args.out,'w') as f:json.dump(d,f,indent=2);f.write('\n')
 print(json.dumps(d,indent=2))
