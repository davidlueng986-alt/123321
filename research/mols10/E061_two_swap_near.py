from pathlib import Path
import json,itertools,time
src=json.load(open(str(Path(__file__).with_name('E061_near_triple.json'))))['squares']

def score(S):
 n=len(S[0]); ret=[]
 for a,b in ((0,1),(0,2),(1,2)):
  z=set()
  for r in range(n):
   for c in range(n):z.add((S[a][r][c],S[b][r][c]))
  ret.append(len(z))
 return tuple(ret)

def apply(S,move):
 s,ty,i,j=move
 if ty==0:S[s][i],S[s][j]=S[s][j],S[s][i]
 else:
  for r in range(10):S[s][r][i],S[s][r][j]=S[s][r][j],S[s][r][i]

moves=[(s,typ,i,j) for s in (1,2) for typ in (0,1) for i in range(10) for j in range(i+1,10)]
assert len(moves)==180
best=(sum(score(src)),score(src),None)
cases=0
T=[[row[:] for row in Q] for Q in src]
t0=time.monotonic()
for idx,x in enumerate(moves):
 apply(T,x)
 for y in moves[idx+1:]:
  apply(T,y);sc=score(T);cases+=1
  if sum(sc)>best[0]:
   best=(sum(sc),sc,(x,y));print('IMPROVE',best,flush=True)
  apply(T,y)
 apply(T,x)
assert T==src
out={'source_overlay':score(src),'moves_single':180,'moves_two_combinations':cases,'best_score':best[0],'best_overlays':best[1],'moves':best[2],'seconds':round(time.monotonic()-t0,3),'scope':'two row/column swaps of B,C from one historical neartriple; Latin conditions automatically preserved; all swaps repeated twice restore source'}
json.dump(out,open(str(Path(__file__).with_name('E061_two_swap_near.json')),'w'),indent=2)
print(out)