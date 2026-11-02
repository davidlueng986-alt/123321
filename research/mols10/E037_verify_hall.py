#!/usr/bin/env python3
"""Independent fixed-prefix Hall witness verifier, no external dependencies.
Input JSON: {"prefix":[A,B,C],"hall":{"left_class":["C",0],
 "right_class":["C",1],"left_demands":[...],"right_neighbors":[...],
 "deficit":1}}. A proof excludes only this fixed prefix.
"""
import json,sys

def verify(witness):
    S=witness["prefix"]; H=witness["hall"]
    assert len(S)==3
    n=len(S[0][0]);k=len(S[0]);symbols=set(range(n))
    for A in S:
        assert len(A)==k and all(len(row)==n and set(row)==symbols for row in A)
        assert all(len({A[r][c] for r in range(k)})==k for c in range(n))
    pairs=((0,1),(0,2),(1,2))
    used=[]
    for i,j in pairs:
        e={(S[i][r][c],S[j][r][c]) for r in range(k) for c in range(n)}
        assert len(e)==k*n
        used.append(e)
    left=tuple(H["left_class"]);right=tuple(H["right_class"])
    L={tuple(x) for x in H["left_demands"]}
    R={tuple(x) for x in H["right_neighbors"]}
    assert len(L)==len(H["left_demands"]) and len(R)==len(H["right_neighbors"])
    assert left!=right and all(x[:2]==left for x in L)
    assert all(x[:2]==right for x in R)
    neighbours=set();placements=0
    for c in range(n):
        avail=[symbols-{A[r][c] for r in range(k)} for A in S]
        for a in avail[0]:
            for b in avail[1]:
                if (a,b) in used[0]:continue
                for z in avail[2]:
                    if (a,z) in used[1] or (b,z) in used[2]:continue
                    resources=(("P",0,a,b),("P",1,a,z),("P",2,b,z),
                               ("C",0,c,a),("C",1,c,b),("C",2,c,z))
                    placements+=1
                    d={x[:2]:x for x in resources}
                    if d[left] in L:neighbours.add(d[right])
    assert neighbours==R,(neighbours,R)
    assert len(L)>len(R)
    assert H["deficit"]==len(L)-len(R)
    return dict(status="EXACT_HALL_CERTIFIED",demands=len(L),neighbors=len(R),
                allowed_placements=placements,scope="FIXED_PREFIX_ONLY")

if __name__=="__main__":
    with open(sys.argv[1]) as fp: data=json.load(fp)
    print(json.dumps(verify(data)))
