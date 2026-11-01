"""Generate diversity of the FIRST Latin square using exact two-symbol row/column trades.

A two-symbol support has 20 cells and splits into connected components under
shared row/column edges. A proper connected component may be swapped while
preserving the Latin property. Only one representative of complementary
component flips is used for each symbol pair. This does not exhaust all
Latin squares, and supplies no orthogonal mate on its own.
"""
from collections import Counter, defaultdict
from verify import analyze
from sample_mates import transversals_single

def is_latin(a):
    n=len(a);target=set(range(n))
    return all(set(row)==target for row in a) and all(
        {a[i][j] for i in range(n)}==target for j in range(n))

def first_square_trades(a):
    if not is_latin(a):
        raise ValueError("first square must be Latin")
    n=len(a)
    result=[]
    for p in range(n):
        for q in range(p+1,n):
            cells=[(i,j) for i in range(n) for j in range(n)
                   if a[i][j] in (p,q)]
            adj={c:set() for c in cells}
            for coordinate in (0,1):
                groups=defaultdict(list)
                for cell in cells:groups[cell[coordinate]].append(cell)
                for pair in groups.values():
                    if len(pair)!=2:raise AssertionError("not two-per-coordinate")
                    u,v=pair;adj[u].add(v);adj[v].add(u)
            components=[];seen=set()
            for root in cells:
                if root in seen:continue
                todo=[root];seen.add(root);component=[]
                while todo:
                    current=todo.pop();component.append(current)
                    for nxt in adj[current]:
                        if nxt not in seen:
                            seen.add(nxt);todo.append(nxt)
                components.append(sorted(component))
            # Flipping every component merely globally exchanges p and q.
            # Skip the final component to avoid redundant complements.
            for component in components[:-1]:
                b=[row.copy() for row in a]
                for i,j in component:
                    b[i][j]=q if b[i][j]==p else p
                if not is_latin(b):raise AssertionError("invalid Latin trade")
                result.append({"symbols":[p,q],"size":len(component),"square":b})
    return result

if __name__=="__main__":
    import json
    from pathlib import Path
    sq=json.loads(Path("near_triple.json").read_text())["squares"]
    trades=first_square_trades(sq[0])
    print(json.dumps({"number_of_first_square_trades":len(trades),
        "component_size_histogram":dict(Counter(t["size"] for t in trades)),
        "single_A_transversal_count_distribution":dict(
            Counter(len(transversals_single(t["square"])) for t in trades)),
        "B_orthogonal_to_modified_A":sum(analyze([t["square"],sq[1]],10)[0]["orthogonal"] for t in trades),
        "C_orthogonal_to_modified_A":sum(analyze([t["square"],sq[2]],10)[0]["orthogonal"] for t in trades)},
        indent=2))
