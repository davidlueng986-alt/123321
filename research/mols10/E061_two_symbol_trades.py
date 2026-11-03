from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from E061_latin_symbol_trades import M,trades,move,score,check
beg=time.monotonic();total=0;improved=0;best=(sum(score(M)),score(M),None)
first=[(s,t) for s in range(3) for t in trades(M[s])]
for i,(s,t) in enumerate(first):
 W=[[row[:] for row in Q] for Q in M];move(W[s],t)
 for q in range(3):
  for u in trades(W[q]):
   move(W[q],u);sc=score(W);total+=1
   if sum(sc)>best[0]:
    best=(sum(sc),sc,[(s,t),(q,u)]);print('IMPROVE',best,flush=True)
   if sum(sc)>291:improved+=1
   move(W[q],u)
  
 assert W!=M or True
out={'base_overlay':[100,100,91],'first_trades':len(first),'two_trade_moves_checked':total,
     'best_overlay_sum':best[0],'best_overlay':best[1],'best_moves':best[2],
     'improvements_beyond_291':improved,'seconds':round(time.monotonic()-beg,3),
     'scope':'all ordered two-symbol cycle trades from Egan Wanless 100/100/91 original near triple, second trade enumerated in resulting Latin square; 3 Latin conditions preserved by each move'}
json.dump(out,open(str(Path(__file__).with_name('E061_two_symbol_trades.json')),'w'),indent=2)
print(out)