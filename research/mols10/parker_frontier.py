"""Compact exhaustive depth-profile certificate for a fixed orthogonal pair.

Depth i counts valid i-row partial common transversals, row order 0..n-1.
For the Parker example depth 9 has only 21 partials, each excluded on
row 10 by collisions in BOTH A and B symbols.
"""
import json
from pathlib import Path
from verify import analyze

def prefix_certificate(a,b):
    n=len(a)
    if not analyze([a,b],n)[0]["orthogonal"]:
        raise ValueError("invalid input pair")
    profile=[0]*(n+1);profile[0]=1
    frontier=[];path=[]
    def dfs(i,columns,aa,bb):
        if i==n: return
        if i==n-1:
            rem=[j for j in range(n) if not columns>>j&1]
            assert len(rem)==1
            j=rem[0]
            frontier.append({"prefix":"".join(map(str,path)),
                             "remaining_column":j,
                             "blocked_A":bool(aa & (1<<a[i][j])),
                             "blocked_B":bool(bb & (1<<b[i][j]))})
        for j in range(n):
            bit=1<<j;av=1<<a[i][j];bv=1<<b[i][j]
            if columns&bit or aa&av or bb&bv: continue
            profile[i+1]+=1
            path.append(j)
            dfs(i+1,columns|bit,aa|av,bb|bv)
            path.pop()
    dfs(0,0,0,0)
    return {"depth_profile":profile,"depth_n_minus_1_frontier":frontier}

if __name__=="__main__":
    a,b=json.loads(Path("parker_pair.json").read_text())["squares"]
    print(json.dumps(prefix_certificate(a,b),indent=2))
