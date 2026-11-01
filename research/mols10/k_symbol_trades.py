"""Restricted k-symbol re-partition trades preserving a fixed Latin A and orthogonal mate B.

Choose k symbols of B, hold other cells fixed, and partition their kn cells
into k common A transversals. Every resulting B' is orthogonal to A.
All alternatives are enumerated for each support up to max_partitions; if
the cap is reached report it, do not claim complete search.
"""
import itertools
from sample_mates import transversals_single,transversals_pair
from verify import analyze

def repartitions_on_support(a,b,chosen,all_t,max_partitions=1000):
    n=len(a); selected=set(chosen);k=len(selected)
    orig=[sum(1<<(n*i+j) for i in range(n) for j in range(n)
              if b[i][j]==v) for v in sorted(selected)]
    support=0
    for m in orig:support|=m
    candidates=[]
    for p in all_t:
        m=sum(1<<(n*i+j) for i,j in enumerate(p))
        if m & ~support==0:candidates.append((p,m))
    sols=[];capped=False
    def dfs(remaining,selection):
        nonlocal capped
        if len(sols)>=max_partitions:
            capped=True
            return
        if remaining==0:
            if len(selection)==k:sols.append(tuple(selection))
            return
        if len(selection)>=k:return
        bit=remaining & -remaining
        for idx,(p,m) in enumerate(candidates):
            if m&bit and m&remaining==m:
                dfs(remaining^m,selection+[idx])
    dfs(support,[])
    baseline=frozenset(orig)
    new=[sol for sol in sols
         if frozenset(candidates[i][1] for i in sol)!=baseline]
    return new,candidates,len(sols),capped

def scan_k(a,b,k=3,max_neighbors=20,max_partitions=1000):
    n=len(a)
    if not 2<=k<=n:raise ValueError("2<=k<=n required")
    if not analyze([a,b],n)[0]["orthogonal"]:
        raise ValueError("invalid pair")
    T=transversals_single(a)
    valid=0;results=[];total_partitions=0;capped_supports=0
    for chosen in itertools.combinations(range(n),k):
        new,candidates,num,capped=repartitions_on_support(
            a,b,chosen,T,max_partitions=max_partitions)
        total_partitions+=num
        if capped:capped_supports+=1
        if not new:continue
        valid+=1
        for sol in new[:max_neighbors]:
            out=[row.copy() for row in b]
            for symbol,idx in zip(chosen,sol):
                for i,j in enumerate(candidates[idx][0]):
                    out[i][j]=symbol
            assert analyze([a,out],n)[0]["orthogonal"]
            joint,support=transversals_pair(a,out)
            results.append({"symbols":chosen,"count":len(joint),
                            "unsupported":sum(v==0 for v in support),
                            "neighbor":out})
    return {"k":k,"supports_with_alternatives":valid,
            "total_solutions_before_baseline_filter":total_partitions,
            "neighbors_checked":len(results),"results":results,
            "single_A_transversals":len(T),
            "capped_supports":capped_supports,
            "per_support_solution_cap":max_partitions,
            "per_support_neighbor_cap":max_neighbors}
