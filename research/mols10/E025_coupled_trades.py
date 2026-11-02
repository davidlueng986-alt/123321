#!/usr/bin/env python3
"""E025: exhaustive proper two-symbol Latin cycle flips around six published
orthogonal pairs. Source arrays: E024_appendix_six_replay.py.
Scope is six *specific* pairs, not all Myrvold families or 3-MOLS(10).
"""
import json
from collections import Counter
from E024_appendix_six_replay import RAW, parse, derive, latin

def component_trades(a):
    n=len(a)
    for x in range(n):
        for y in range(x+1,n):
            cells=[(r,c) for r in range(n) for c in range(n) if a[r][c] in (x,y)]
            assert len(cells)==2*n
            unseen=set(cells); components=[]
            while unseen:
                first=min(unseen);unseen.remove(first);stack=[first];component=[first]
                while stack:
                    r,c=stack.pop()
                    for z in [z for z in unseen if z[0]==r or z[1]==c]:
                        unseen.remove(z);stack.append(z);component.append(z)
                components.append(sorted(component))
            k=len(components)
            for mask in range(1,(1<<k)-1):
                b=[row[:] for row in a];flipped=0
                for i,component in enumerate(components):
                    if mask>>i&1:
                        for r,c in component:
                            b[r][c]=y if a[r][c]==x else x
                            flipped+=1
                assert latin(b)
                yield {'symbols':[x,y],'mask':mask,'cycles':k,'flipped':flipped},b

def overlay(a,b):
    n=len(a)
    return len({(a[r][c],b[r][c]) for r in range(n) for c in range(n)})

def run():
    results={}
    for label,(pstr,qstr) in RAW.items():
        p,q=parse(pstr),parse(qstr)
        assert latin(p) and latin(q)
        z=derive(p,q)
        assert latin(z) and overlay(z,q)==100
        aa=list(component_trades(z));bb=list(component_trades(q))
        assert len(aa)==len({tuple(map(tuple,a)) for _,a in aa})
        assert len(bb)==len({tuple(map(tuple,b)) for _,b in bb})
        singles=[Counter(overlay(a,q) for _,a in aa),
                 Counter(overlay(z,b) for _,b in bb)]
        assert singles[0].get(100,0)==singles[1].get(100,0)==0
        hist=Counter();best=[];maximum=0;ww_high=[]
        for am,a in aa:
            for bm,b in bb:
                score=overlay(a,b);hist[score]+=1
                if score>maximum:maximum=score;best=[]
                if score==maximum:best.append((am,bm,a,b))
                if label=='WW' and score>=96:ww_high.append((am,bm,a,b))
        assert hist.get(100,0)==0
        # Only best double flips, plus an expanded >=96 WW pilot.
        def one_more(items):
            counts=Counter();witnesses=[]
            for am,bm,a,b in items:
                for cm,c in component_trades(a):
                    n=overlay(c,b);counts[n]+=1
                    if n==100:witnesses.append(('A',am,bm,cm))
                for cm,c in component_trades(b):
                    n=overlay(a,c);counts[n]+=1
                    if n==100:witnesses.append(('B',am,bm,cm))
            return {'trials':sum(counts.values()),'max_overlay':max(counts,default=None),
                    'orthogonal':len(witnesses),'hist':dict(sorted(counts.items()))}
        best_follow=one_more(best)
        ww_follow=one_more(ww_high) if label=='WW' else None
        assert best_follow['orthogonal']==0
        if ww_follow:assert ww_follow['orthogonal']==0
        results[label]={
            'A_trades':len(aa),'B_trades':len(bb),
            'A_single_hist':dict(sorted(singles[0].items())),
            'B_single_hist':dict(sorted(singles[1].items())),
            'double_trials':len(aa)*len(bb),'double_max_overlay':maximum,
            'double_best_count':len(best),'double_hist':dict(sorted(hist.items())),
            'double_best_example':{'A':best[0][0],'B':best[0][1]},
            'best_followup':best_follow,
            'WW_ge96_count':len(ww_high) if label=='WW' else None,
            'WW_ge96_followup':ww_follow,
        }
        print(label,len(aa),len(bb),len(aa)*len(bb),maximum,len(best),
              best_follow['trials'],flush=True)
    return results

if __name__=='__main__':
    results=run()
    with open('E025_RESULTS.json','w') as f:json.dump(results,f,indent=2)
    print('TOTAL_DOUBLE',sum(x['double_trials'] for x in results.values()))
