#!/usr/bin/env python3
"""Replay published Bright–Keita–Stevens 2026 Appendix UU TRP, construct orthogonal pair."""
import json
from E023_SX_pair_replay import latin,overlay,transversals
P=[[int(x) for x in s.split()] for s in """
0 1 2 4 5 6 3 7 8 9
1 7 8 0 4 2 5 9 3 6
2 9 7 1 8 3 0 4 6 5
3 5 0 7 2 4 6 8 9 1
4 2 6 3 0 9 7 1 5 8
9 6 1 2 3 7 8 5 0 4
5 8 3 6 9 1 4 0 2 7
8 3 4 9 1 5 2 6 7 0
6 0 9 5 7 8 1 2 4 3
7 4 5 8 6 0 9 3 1 2
""".strip().splitlines()]
Q=[[int(x) for x in s.split()] for s in """
0 3 6 1 9 7 5 8 4 2
2 5 1 8 0 6 4 9 7 3
3 0 4 6 8 2 7 5 1 9
6 9 2 0 1 4 8 3 5 7
8 7 0 3 5 1 9 2 6 4
9 2 3 7 4 0 1 6 8 5
1 6 5 4 7 3 2 0 9 8
7 1 8 5 3 9 6 4 2 0
4 8 9 2 6 5 0 7 3 1
5 4 7 9 2 8 3 1 0 6
""".strip().splitlines()]
def replay():
    assert latin(P) and latin(Q)
    Z=[[next(t for t in range(10) if P[t][c]==Q[r][c])
        for c in range(10)] for r in range(10)]
    assert latin(Z) and overlay(Z,Q)==100
    assert all(P[Z[r][c]][c]==Q[r][c] for r in range(10) for c in range(10))
    ts=transversals(Z,Q)
    return {'source':'Bright Keita Stevens EJC 2026 P1.30 Appendix p.31 UU pair',
        'P':P,'Q':Q,'Z':Z,'orthogonal_overlay_ZQ':100,
        'latin_P':True,'latin_Q':True,'latin_Z':True,
        'common_transversal_count':len(ts),
        'common_transversals_columns':ts,
        'third_square_extension':'UNSAT_FIXED_PAIR' if len(ts)<10 else 'UNKNOWN_REQUIRES_EXACT_COVER'}
if __name__=='__main__':print(json.dumps(replay(),indent=2))
