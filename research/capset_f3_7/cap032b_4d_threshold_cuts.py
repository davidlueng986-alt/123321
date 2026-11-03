"""CAP-032B: necessary universal threshold constraints on every 4D quotient line.
Strictly stronger than r3(4)<=20, but CAP027 285 formal count model survives.
This module does not assert a global r3(7) upper bound.
"""
from itertools import product
MAX_THIRD={(6,6):8,(6,7):6,(6,8):6,(6,9):3,(7,7):4,
           (7,8):3,(7,9):2,(8,8):2,(8,9):2,(9,9):2}
Q=list(product(range(3),repeat=4))
INDEX={q:i for i,q in enumerate(Q)}
LINES=tuple((a,b,c) for a in range(81) for b in range(a+1,81)
            for c in [INDEX[tuple((-x-y)%3 for x,y in zip(Q[a],Q[b]))]] if c>b)
assert len(LINES)==1080
def violations(counts):
    assert len(counts)==81 and all(isinstance(x,int) and 0<=x<=9 for x in counts)
    out=[]
    for triple in LINES:
        for a,b,c in ((triple[0],triple[1],triple[2]),
                      (triple[0],triple[2],triple[1]),(triple[1],triple[2],triple[0])):
            for i in range(6,10):
                for j in range(i,10):
                    if ((counts[a]>=i and counts[b]>=j) or
                        (counts[a]>=j and counts[b]>=i)) and counts[c]>MAX_THIRD[(i,j)]:
                        out.append((a,b,c,i,j,counts[c],MAX_THIRD[(i,j)]))
    return out
def formal285():
    chosen={7*i%81 for i in range(11)}
    f=[3+int(q[0]==q[1]==0)+3*int(i in chosen) for i,q in enumerate(Q)]
    assert sum(f)==285
    return f
def audit():
    f=formal285()
    assert not violations(f)
    x=[0]*81;a,b,c=LINES[0];x[a]=x[b]=7;x[c]=5
    assert any(v[3:5]==(7,7) for v in violations(x))
    return {'quotient_lines':len(LINES),'exact_threshold_pairs':len(MAX_THIRD),
            'formal285_still_feasible_count_model':True,'invalid_7_7_5_detected':True,
            'global_bound_improved':False}
if __name__=='__main__':
    import json;print(json.dumps(audit(),sort_keys=True))
