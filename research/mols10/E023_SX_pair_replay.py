#!/usr/bin/env python3
"""Replay published Bright–Keita–Stevens 2026 Appendix SX TRP, construct orthogonal pair (Z,Q)."""
import json
P=[[int(x) for x in line.split()] for line in """
0 1 3 4 5 6 2 7 8 9
1 6 9 2 3 4 0 8 5 7
3 8 2 1 7 5 6 4 9 0
4 2 7 0 1 8 3 9 6 5
5 0 8 9 2 3 7 1 4 6
7 3 0 5 9 1 4 6 2 8
8 5 1 6 0 2 9 3 7 4
2 4 5 7 6 9 8 0 3 1
6 9 4 3 8 7 1 5 0 2
9 7 6 8 4 0 5 2 1 3
""".strip().splitlines()]
Q=[[int(x) for x in line.split()] for line in """
2 6 1 4 7 3 5 9 0 8
4 9 3 5 2 0 6 8 7 1
7 1 2 9 0 4 8 5 6 3
8 0 5 3 1 6 4 2 9 7
0 5 7 8 3 9 1 4 2 6
1 4 6 0 9 5 7 3 8 2
3 7 9 6 8 1 2 0 4 5
5 3 4 2 6 8 9 7 1 0
6 8 0 7 4 2 3 1 5 9
9 2 8 1 5 7 0 6 3 4
""".strip().splitlines()]
N=10

def latin(S):
    return len(S)==N and all(sorted(row)==list(range(N)) for row in S) and all(
        sorted(S[i][j] for i in range(N))==list(range(N)) for j in range(N))
def overlay(A,B):
    return len({(A[i][j],B[i][j]) for i in range(N) for j in range(N)})
def transversals(A,B=None):
    result=[]
    def dfs(r,usedcol,useda,usedb,cols):
        if r==N:result.append(cols);return
        for c in range(N):
            if (usedcol>>c)&1 or (useda>>A[r][c])&1 or (
                B is not None and (usedb>>B[r][c])&1):continue
            dfs(r+1,usedcol|(1<<c),useda|(1<<A[r][c]),
                usedb|(1<<B[r][c]) if B is not None else 0,cols+[c])
    dfs(0,0,0,0,[])
    return result
def replay():
    assert latin(P) and latin(Q)
    Z=[[next(t for t in range(N) if P[t][c]==Q[r][c])
        for c in range(N)] for r in range(N)]
    assert latin(Z) and overlay(Z,Q)==100
    assert all(P[Z[r][c]][c]==Q[r][c] for r in range(N) for c in range(N))
    ts=transversals(Z,Q)
    coverage=len({(r,c) for t in ts for r,c in enumerate(t)})
    return {'source':'Bright Keita Stevens EJC 2026 P1.30 Appendix p.31 SX pair',
        'P':P,'Q':Q,'Z':Z,'latin_P':True,'latin_Q':True,'latin_Z':True,
        'orthogonal_overlay_ZQ':overlay(Z,Q),
        'common_transversal_count':len(ts),
        'common_transversals_columns':ts,
        'distinct_cells_covered_by_common_transversals':coverage,
        'third_square_extension':'UNSAT_FIXED_PAIR' if len(ts)<10 or coverage<100
            else 'UNKNOWN_REQUIRES_EXACT_COVER'}
if __name__=='__main__':
    print(json.dumps(replay(),indent=2))
