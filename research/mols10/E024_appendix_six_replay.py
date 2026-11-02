#!/usr/bin/env python3
"""E024: EJC 2026 appendix pages 32-33: six exact TRP fixed-pair replays.
Source: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i1p30/pdf/
No inference about all pairs of a Myrvold type or unrestricted 3-MOLS(10).
"""
import itertools,json,time
RAW={
  "UW": [
    "0234561789 1460923857 2359087461 5671308294 6012854973 7503419628 8725196340 9148270536 3897642015 4986735102",
    "0372495816 1537286904 3716520498 5049132687 9263807145 2481659730 6150748329 7928364051 8694013572 4805971263"
  ],
  "UX": [
    "0124563789 1382647590 2895314076 5901278634 7043192865 9537026148 3476805921 6710489352 4658930217 8269751403",
    "0591837462 3215670849 5364109278 6408321795 1936452087 2783965104 4820796531 7159048326 8647213950 9072584613"
  ],
  "VX": [
    "0234561789 1375094826 3029685147 4618207953 5103972468 7540138692 2786349015 6892713504 9451826370 8967450231",
    "0349817265 1508629734 2630984571 4152390687 3876251490 5924708316 6487032159 7061543928 8295176043 9713465802"
  ],
  "WW": [
    "0234561789 1376294058 2715048936 3540817692 8023975164 4168359207 5897126340 6901783425 9452630871 7689402513",
    "0358172496 2061597843 5932418067 6125804379 9704325618 1583649720 3819760254 4270986531 8647231905 7496053182"
  ],
  "WX": [
    "0134562789 1502798643 2690813475 3257041896 7918235064 4075629318 5423986107 6789104532 8361457920 9846370251",
    "6172083954 7305914286 8720345619 9051836742 0248697135 1684250397 2817469503 3469528071 4593172860 5936701428"
  ],
  "XX": [
    "0134562789 1763285940 2915637804 6298314075 3607849251 4529703168 5840176392 7052498613 8471920536 9386051427",
    "0728159634 3254087196 6802731549 8930415267 1047963825 2693570418 4375296081 5416802973 7189624350 9561348702"
  ]
}
def parse(rows):
    a=[[int(x) for x in s] for s in rows.split()]
    assert len(a)==10 and all(len(r)==10 for r in a)
    return a
def latin(a):
    full=set(range(10))
    return all(set(row)==full for row in a) and all({a[r][c] for r in range(10)}==full for c in range(10))
def derive(p,q):
    inv=[{p[r][c]:r for r in range(10)} for c in range(10)]
    return [[inv[c][q[r][c]] for c in range(10)] for r in range(10)]
def dfs(a,b):
    witnesses=[]
    def rec(r,cols,asym,bsym,perm):
        if r==10:
            witnesses.append(tuple(perm));return
        for c in range(10):
            x,y=a[r][c],b[r][c]
            if (cols>>c)&1 or (asym>>x)&1 or (bsym>>y)&1:continue
            rec(r+1,cols|1<<c,asym|1<<x,bsym|1<<y,perm+[c])
    rec(0,0,0,0,[])
    return witnesses
def brute(a,b):
    out=[]
    for perm in itertools.permutations(range(10)):
        x=y=0
        for r,c in enumerate(perm):
            i,j=a[r][c],b[r][c]
            if (x>>i)&1 or (y>>j)&1:break
            x|=1<<i;y|=1<<j
        else:out.append(perm)
    return out
def main():
    results={}
    for label,(pstr,qstr) in RAW.items():
        start=time.monotonic()
        p,q=parse(pstr),parse(qstr)
        assert latin(p) and latin(q)
        z=derive(p,q)
        assert latin(z)
        assert len({(z[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
        assert all(p[z[r][c]][c]==q[r][c] for r in range(10) for c in range(10))
        w1=dfs(z,q);w2=brute(z,q)
        assert w1==w2, (label,len(w1),len(w2))
        support={r*10+c for w in w1 for r,c in enumerate(w)}
        # All six have <10 common transversals; exact cover is impossible.
        assert len(w1)<10
        results[label]={"latin_p_q_z":True,"overlay":100,"common_transversals":len(w1),
                        "independent_10factorial":len(w2),"supported_cells":len(support),
                        "witness_permutations":w1,"status":"UNSAT_FIXED_PAIR",
                        "elapsed_seconds":round(time.monotonic()-start,3)}
        print(label,results[label],flush=True)
    print(json.dumps(results,indent=2))
if __name__=="__main__":main()
