"""Exact-cover completion of a FIXED orthogonal Latin pair by common transversals.

Each candidate transversal is a possible symbol class of a third orthogonal
mate. Cover all n^2 cells by disjoint transversals. This solver branches on
the most-constrained uncovered cell, not on arbitrary transversal subsets.
Budget exhaustion always returns UNKNOWN rather than UNSAT.
"""
import time
from verify import analyze

def exact_cover(transversals, n, *, max_nodes=200000, max_seconds=10.0):
    if n < 2 or max_nodes <= 0 or max_seconds <= 0:
        raise ValueError("invalid positive n and budgets")
    full = (1 << (n*n)) - 1
    masks, cell_to_candidates = [], [[] for _ in range(n*n)]
    for idx, p in enumerate(transversals):
        if len(p) != n or sorted(p) != list(range(n)):
            raise ValueError(f"candidate {idx} must be a column permutation")
        m = sum(1 << (n*i+j) for i,j in enumerate(p))
        masks.append(m)
        for i,j in enumerate(p):
            cell_to_candidates[n*i+j].append(idx)
    if any(not v for v in cell_to_candidates):
        return {"status":"UNSAT_FIXED_PAIR_EXACT", "nodes":0,
                "reason":"uncovered cell", "indices":[]}
    start=time.monotonic()
    selected=[]
    nodes=0
    class LimitReached(Exception): pass
    def dfs(used):
        nonlocal nodes
        if used == full:
            return True
        if nodes >= max_nodes or time.monotonic()-start > max_seconds:
            raise LimitReached
        nodes += 1
        best=None
        remainder=full & ~used
        while remainder:
            bit=remainder & -remainder
            c=bit.bit_length()-1
            avail=[t for t in cell_to_candidates[c] if not(masks[t] & used)]
            if not avail: return False
            if best is None or len(avail)<len(best):
                best=avail
                if len(best)==1: break
            remainder-=bit
        for t in best:
            selected.append(t)
            if dfs(used | masks[t]): return True
            selected.pop()
        return False
    try:
        sat=dfs(0)
    except LimitReached:
        return {"status":"UNKNOWN_BUDGET", "nodes":nodes, "indices":[],
                "elapsed_s":round(time.monotonic()-start,3)}
    if sat:
        if len(selected)!=n: raise AssertionError("bad exact-cover cardinality")
        return {"status":"SAT_EXACT", "nodes":nodes, "indices":selected.copy(),
                "elapsed_s":round(time.monotonic()-start,3)}
    return {"status":"UNSAT_FIXED_PAIR_EXACT", "nodes":nodes, "indices":[],
            "reason":"complete exact-cover search",
            "elapsed_s":round(time.monotonic()-start,3)}

def build_third(a,b,transversals,solution):
    if solution["status"]!="SAT_EXACT": return None
    n=len(a)
    c=[[-1]*n for _ in range(n)]
    for value,index in enumerate(solution["indices"]):
        for row,col in enumerate(transversals[index]):
            c[row][col]=value
    if not all(x["orthogonal"] for x in analyze([a,b,c],n)):
        raise AssertionError("candidate failed independent full witness check")
    return c
