"""Exact-cover style backtracking for a THIRD mate of a fixed orthogonal pair.

For each cell (i,j), choose c. Unique keys must hold simultaneously:
  (row i, c), (column j, c), (A[i,j], c), (B[i,j], c).
Budget exhaustion is UNKNOWN, never UNSAT.
This is a baseline, not an efficient solver for unrestricted order 10.
"""
import time
from verify import analyze

class SearchBudget(Exception):
    pass

def extend_pair(a, b, *, max_nodes=100000, max_seconds=5.0):
    n = len(a)
    if not analyze([a,b], n)[0]["orthogonal"]:
        raise ValueError("input pair must be Latin and mutually orthogonal")
    taken = [[set() for _ in range(n)] for _ in range(4)]
    c = [[-1]*n for _ in range(n)]
    nodes = 0
    deadline = time.monotonic() + max_seconds

    def candidate(i,j):
        return [v for v in range(n)
                if v not in taken[0][i] and v not in taken[1][j]
                and v not in taken[2][a[i][j]]
                and v not in taken[3][b[i][j]]]

    def dfs(left):
        nonlocal nodes
        if left == 0:
            return True
        if nodes >= max_nodes or time.monotonic() >= deadline:
            raise SearchBudget
        nodes += 1
        best = None
        for i in range(n):
            for j in range(n):
                if c[i][j] >= 0:
                    continue
                choices = candidate(i,j)
                if not choices:
                    return False
                if best is None or len(choices) < len(best[2]):
                    best = (i,j,choices)
        i,j,choices = best
        key = (i,j,a[i][j],b[i][j])
        for v in choices:
            c[i][j] = v
            for t in range(4):
                taken[t][key[t]].add(v)
            if dfs(left-1):
                return True
            for t in range(4):
                taken[t][key[t]].remove(v)
            c[i][j] = -1
        return False

    try:
        status = "SAT" if dfs(n*n) else "UNSAT_FIXED_PAIR"
    except SearchBudget:
        status = "UNKNOWN_BUDGET_EXHAUSTED"
    return {"status":status, "nodes":nodes, "solution":c if status=="SAT" else None}
