# E030: exact direct triple feasibility via row-column permutation candidates.
# Each Latin symbol is a permutation transversal. Triple existence is a
# selection of three partitions with pairwise intersections exactly once.
from itertools import permutations
def candidates(n):
    return [tuple(r*n+p[r] for r in range(n)) for p in permutations(range(n))]
def search(n, limit_nodes=100000):
    T=candidates(n); allcells=(1<<(n*n))-1
    masks=[sum(1<<c for c in t) for t in T]
    bycell=[[i for i,m in enumerate(masks) if m>>c&1] for c in range(n*n)]
    nodes=0
    def partitions(chosen,used):
        nonlocal nodes
        nodes+=1
        if nodes>limit_nodes: raise TimeoutError
        if used==allcells:
            yield tuple(chosen);return
        cell=min((c for c in range(n*n) if not(used>>c&1)),key=lambda c:sum(not(masks[i]&used) for i in bycell[c]))
        for i in bycell[cell]:
            if not(masks[i]&used):
                yield from partitions(chosen+[i],used|masks[i])
    try:
        for a in partitions([],0):
            for b in partitions([],0):
                if all((masks[i]&masks[j]).bit_count()==1 for i in a for j in b):
                    for c in partitions([],0):
                        if all((masks[i]&masks[k]).bit_count()==1 for i in a for k in c) and all((masks[j]&masks[k]).bit_count()==1 for j in b for k in c):
                            return {'status':'SAT','n':n,'nodes':nodes,'squares':[[[next(s for s,i in enumerate(part) if (masks[i]>>(r*n+col))&1) for col in range(n)] for r in range(n)] for part in (a,b,c)]}
        return {'status':'UNSAT','n':n,'nodes':nodes}
    except TimeoutError:return {'status':'UNKNOWN_BUDGET','n':n,'nodes':nodes}
if __name__=='__main__':
    import json
    for n in (2,3,4):
        print(json.dumps(search(n)))
