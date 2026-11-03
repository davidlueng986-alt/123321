#!/usr/bin/env python3
"""One-shot Wanless order10 2-MOLS dataset exact transversal enumeration and 8+endgame search.
SCOPE: only input listed pairs; not unrestricted pair classification or 3-MOLS proof.
Downloaded data expected: https://users.monash.edu.au/~iwanless/data/MOLS/MOLS10.txt
"""
import argparse,collections,hashlib,json,os,pathlib,re,time,urllib.request

N=10; ALL=(1<<N)-1

def read_pairs(path):
 data=pathlib.Path(path).read_bytes();lines=data.decode('ascii').splitlines()
 header=lines[0].strip(); m=re.fullmatch(r'10\s+10\s+(\d+)',header)
 if not m:raise ValueError('missing 10 10 count header')
 count=int(m.group(1)); rows=[l.strip() for l in lines[1:] if l.strip()]
 if len(rows)!=10*count or count%2:raise ValueError(f'row count mismatch, expected {count*10} got {len(rows)}')
 if any(not re.fullmatch('[abcdefghij]{10}',row) for row in rows):raise ValueError('invalid row alphabet/length')
 def sq(i):return [[ord(ch)-97 for ch in row] for row in rows[i*10:(i+1)*10]]
 return ([(sq(i),sq(i+1)) for i in range(0,count,2)],hashlib.sha256(data).hexdigest())

def validate(A,B):
 n=len(A);T=set(range(n))
 for S in (A,B):
  if any(set(row)!=T for row in S):return False
  if any({S[r][c] for r in range(n)}!=T for c in range(n)):return False
 return len({(A[r][c],B[r][c]) for r in range(n) for c in range(n)})==n*n

def exact_transversals(A,B):
 n=len(A);t=[];p=[0]*n;nodes=0
 def rec(r,cols,aa,bb):
  nonlocal nodes
  nodes+=1
  if r==n:
   t.append(tuple(p));return
  for c in range(n):
   bit=1<<c;a=A[r][c];b=B[r][c]
   if (cols&bit) or (aa&(1<<a)) or (bb&(1<<b)):continue
   p[r]=c;rec(r+1,cols|bit,aa|(1<<a),bb|(1<<b))
 rec(0,0,0,0)
 return t,nodes

def bipartite(A,B,pack,transversals):
 n=len(A);occ={(r,c) for t in pack for r,c in enumerate(transversals[t])}
 R=[(r,c) for r in range(n) for c in range(n) if (r,c) not in occ]
 assert len(R)==2*n
 groups=[collections.defaultdict(list) for _ in range(4)]
 for i,(r,c) in enumerate(R):
  for k,v in enumerate([r,c,A[r][c],B[r][c]]):groups[k][v].append(i)
 adj=[[] for _ in R]
 for g in groups:
  assert len(g)==n and all(len(q)==2 for q in g.values())
  for i,j in g.values():adj[i].append(j);adj[j].append(i)
 col=[-1]*len(R)
 for st in range(len(R)):
  if col[st]!=-1:continue
  col[st]=0;stack=[st]
  while stack:
   v=stack.pop()
   for u in adj[v]:
    if col[u]==-1:col[u]=1-col[v];stack.append(u)
    elif col[u]==col[v]:return None
 T1=[R[i] for i in range(len(R)) if col[i]==0]
 T2=[R[i] for i in range(len(R)) if col[i]==1]
 assert len(T1)==len(T2)==n
 return T1,T2

def max_disjoint(A,B,transversals,node_cap=2_000_000):
 n=len(transversals);N=len(A);masks=[sum(1<<(N*r+c) for r,c in enumerate(T)) for T in transversals]
 compat=[0]*n
 for i in range(n):
  for j in range(i+1,n):
   if not masks[i]&masks[j]:compat[i]|=1<<j
 best=[];counter=0;complete=True;two_tests=0;two_hits=0;proof=None
 def rec(cand,pack):
  nonlocal best,counter,complete,two_tests,two_hits,proof
  if not complete or proof is not None:return
  counter+=1
  if counter>node_cap:
   complete=False;return
  if len(pack)>len(best):best=pack[:]
  if len(pack)>=N-2:
   two_tests+=1
   bip=bipartite(A,B,pack,transversals)
   if bip:
    two_hits+=1;proof=(pack[:],bip)
    return
   # Beyond 8 items could still create a 9-pack; any 9-pack contains an 8-pack
   # whose 20-cell residual splits into 2 transversals, hence the failed bipartite
   # test rules out every extension of this particular 8-pack.
   return
  if len(pack)+cand.bit_count() < (N-2 if len(best)>=N-2 else len(best)+1):return
  while cand and complete and proof is None:
   low=cand&-cand;i=low.bit_length()-1;cand^=low
   if len(pack)+1+cand.bit_count() < (N-2 if len(best)>=N-2 else len(best)+1):break
   rec(cand&compat[i],pack+[i])
 rec((1<<n)-1,[])
 return {'max_pack':len(best) if complete else None,'best_found_pack':len(best),'search_nodes':counter,
         'search_complete':complete,'tested_eight_pack':two_tests,'eight_pack_bipartite_hits':two_hits,
         'closure_found':proof is not None,'closure_pack':proof[0] if proof else None,
         'closure_residual':proof[1] if proof else None}

def build_full(A,B,T,packet):
 pack=packet['closure_pack'];x=packet['closure_residual'];n=len(A)
 trans=[list(T[i]) for i in pack]
 for lst in x:trans.append([next(c for r,c in lst if r==rr) for rr in range(n)])
 assert len(trans)==n
 C=[[-1]*n for _ in range(n)]
 for z,t in enumerate(trans):
  for r,c in enumerate(t):C[r][c]=z
 assert validate(A,B)
 assert all(set(C[r])==set(range(n)) for r in range(n))
 assert all({C[r][c] for r in range(n)}==set(range(n)) for c in range(n))
 assert all(len({(S[r][c],C[r][c]) for r in range(n) for c in range(n)})==n*n for S in (A,B))
 return [A,B,C]

def scan(args):
 inpath=pathlib.Path(args.input)
 if args.download:
  url='https://users.monash.edu.au/~iwanless/data/MOLS/MOLS10.txt'
  with urllib.request.urlopen(url,timeout=45) as f:inpath.write_bytes(f.read())
 pairs,sha=read_pairs(inpath)
 total=len(pairs);count=min(total,args.limit or total)
 output={'status':'IN_PROGRESS','dataset_sha256':sha,'dataset_pairs':total,'pairs_processed':0,
  'invalid_pairs':0,'transversals_hist':{},'pack_hist_exact':{},'pack_unknown':0,
  'best_pack_found':0,'max_transversals':0,'largest_transversals_samples':[],
  'eight_pack_bipartite_tests':0,'closure_found':False,'witness':None,'first_high_pack':None,
  'unresolved_searches':[], 'time_seconds':None,'scope':'ONLY WANLESS PUBLIC DATASET; no full species enumeration'}
 hT=collections.Counter();hP=collections.Counter();start=time.monotonic()
 out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
 for idx in range(count):
  A,B=pairs[idx]
  if not validate(A,B):
   output['invalid_pairs']+=1
   raise ValueError(f'Invalid 2MOLS at pair {idx}')
  T,tn=exact_transversals(A,B)
  output['max_transversals']=max(output['max_transversals'],len(T));hT[len(T)]+=1
  if len(T)>30:
   output['largest_transversals_samples'].append({'index':idx,'transversals':len(T)})
  k=max_disjoint(A,B,T,args.node_cap)
  output['best_pack_found']=max(output['best_pack_found'],k['best_found_pack'])
  output['eight_pack_bipartite_tests']+=k['tested_eight_pack']
  if k['search_complete']:hP[k['max_pack']]+=1
  else:
   output['pack_unknown']+=1
   output['unresolved_searches'].append({'index':idx,'transversals':len(T),'best_found_pack':k['best_found_pack'],'nodes':k['search_nodes']})
  if k['closure_found']:
   output['closure_found']=True
   output['pairs_processed']=idx+1
   output['witness']=build_full(A,B,T,k)
   output['closure_pair_index']=idx
   print('INDEPENDENTLY_VERIFIED_CLOSURE',idx,flush=True)
   break
  if k['best_found_pack']>=7 and output['first_high_pack'] is None:
   output['first_high_pack']={'index':idx,'pack_size':k['best_found_pack'],'T_count':len(T),'A':A,'B':B}
  if idx%args.progress_every==0:
   print('PROGRESS',idx,'T',len(T),'pack',k['best_found_pack'],'best',output['best_pack_found'],'elapsed',round(time.monotonic()-start,1),flush=True)
  output['pairs_processed']=idx+1
  if (idx+1)%args.checkpoint_every==0:
   output.update(transversals_hist=dict(hT),pack_hist_exact=dict(hP),time_seconds=round(time.monotonic()-start,3))
   out.write_text(json.dumps(output,indent=2))
 output['status']='CLOSED_WITNESS_VERIFIED' if output['closure_found'] else ('COMPLETE_DATASET_SCAN' if output['pairs_processed']==total else 'PARTIAL_DATASET_SCAN')
 output.update(transversals_hist=dict(hT),pack_hist_exact=dict(hP),time_seconds=round(time.monotonic()-start,3))
 out.write_text(json.dumps(output,indent=2))
 print('SCAN_SUMMARY',json.dumps({z:output[z] for z in ['status','dataset_pairs','pairs_processed','max_transversals','best_pack_found','pack_unknown','eight_pack_bipartite_tests','closure_found','time_seconds']}),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser()
 parser.add_argument('--input',default='MOLS10.txt');parser.add_argument('--download',action='store_true')
 parser.add_argument('--output',default='E062_SCAN_RESULTS.json');parser.add_argument('--limit',type=int)
 parser.add_argument('--node-cap',type=int,default=2_000_000)
 parser.add_argument('--progress-every',type=int,default=100);parser.add_argument('--checkpoint-every',type=int,default=100)
 scan(parser.parse_args())