#!/usr/bin/env python3
"""E045 bounded LP-guided k3->k4 fourth-row rounding. Heuristic, not proof."""
import json, random, time, hashlib, argparse
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model
from E044_disjoint_probe import valid

def extract_row(S,T,weights,rng,temperature=.1,node_cap=12000):
    opts=[[] for _ in range(10)]
    for j,(col,a,b,d) in enumerate(T):
        if weights[j]>1e-8: opts[col].append((a,b,d,float(weights[j])))
    if any(not v for v in opts): return None,0,"no positive candidate in column"
    for c in range(10):
        rng.shuffle(opts[c])
        opts[c].sort(key=lambda x:x[3]+temperature*rng.gammavariate(1,1),reverse=True)
    seen=[set(),set(),set()];fill=[None]*10;nodes=0
    def dfs(left):
        nonlocal nodes
        nodes+=1
        if nodes>node_cap:return False
        if not left:return True
        poss=[]
        for c in left:
            q=[t for t in opts[c] if t[0] not in seen[0] and t[1] not in seen[1] and t[2] not in seen[2]]
            if not q:return False
            poss.append((len(q),c,q))
        _,c,q=min(poss,key=lambda x:x[0])
        for a,b,d,w in q:
            fill[c]=(a,b,d)
            for s,v in enumerate((a,b,d)):seen[s].add(v)
            if dfs([v for v in left if v!=c]):return True
            for s,v in enumerate((a,b,d)):seen[s].remove(v)
        fill[c]=None
        return False
    if not dfs(list(range(10))):return None,nodes,"bounded matching failed"
    U=[S[s]+[[fill[c][s] for c in range(10)]] for s in range(3)]
    valid(U)
    return U,nodes,"valid"

def run(num_parents=48,per_parent=12,sec=40,seed=20261102045):
    D=json.load(open("E044_RESULTS.json"));rng=random.Random(seed);t0=time.monotonic()
    cases=[];parents=[];seen=set()
    total={"LP_FEASIBLE":0,"LP_INFEASIBLE":0,"ZERO_SUPPORT":0,"UNKNOWN":0,"MATCHING_FAIL":0}
    ids=[int(x) for x in np.linspace(0,len(D["cases"])-1,num_parents)]
    for ix in ids:
        if time.monotonic()-t0>sec:break
        S=[a[:3] for a in D["cases"][ix]["prefix"]]
        A,T,E=model(S)
        z=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(A.shape[0]),bounds=(0,1),method="highs",options={"time_limit":3})
        parents.append({"parent_index":ix,"lp_status":int(z.status),"candidates":len(T),"residual":float(max(abs(A@z.x-1))) if z.x is not None else None})
        if z.status!=0:continue
        for attempt in range(per_parent):
            if time.monotonic()-t0>sec:break
            U,nodes,reason=extract_row(S,T,z.x,rng,temperature=.05+.5*(attempt%6)/5)
            if U is None:
                total["MATCHING_FAIL"]+=1
                cases.append({"parent":ix,"attempt":attempt,"status":"MATCHING_FAIL","nodes":nodes,"reason":reason})
                continue
            h=hashlib.sha256(json.dumps(U,separators=(",",":")).encode()).hexdigest()
            if h in seen:continue
            seen.add(h);B,V,F=model(U);zeros=int(sum(np.diff(B.indptr)==0))
            rec={"parent":ix,"attempt":attempt,"nodes":nodes,"sha256":h,"variables":len(V),"zero_support":zeros,"prefix":U}
            if zeros:rec["status"]="ZERO_SUPPORT"
            else:
                y=linprog(np.zeros(len(V)),A_eq=B,b_eq=np.ones(B.shape[0]),bounds=(0,1),method="highs",options={"time_limit":2})
                rec["status"]={0:"LP_FEASIBLE",1:"UNKNOWN",2:"LP_INFEASIBLE",3:"UNKNOWN",4:"UNKNOWN"}[y.status]
                if y.status==0:rec["residual"]=float(max(abs(B@y.x-1)))
            total[rec["status"]]+=1;cases.append(rec)
            print("parent",ix,"attempt",attempt,rec["status"],"candidates",len(V),"elapsed",round(time.monotonic()-t0,1),flush=True)
            if rec["status"]=="LP_FEASIBLE":break
    out={"experiment":"E045","seed":seed,"limits":{"parents":num_parents,"per_parent":per_parent,"seconds":sec},"elapsed_s":round(time.monotonic()-t0,2),"summary":total,"parents":parents,"cases":cases,"scope":"Fixed valid k4 prefixes; LP necessary only"}
    json.dump(out,open("E045_GUIDED_RESULTS.json","w"),indent=2)
    print("SUMMARY",total,"unique",len(seen),"seconds",out["elapsed_s"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--parents",type=int,default=48)
    p.add_argument("--per-parent",type=int,default=12)
    p.add_argument("--seconds",type=int,default=40)
    a=p.parse_args()
    run(a.parents,a.per_parent,a.seconds)
