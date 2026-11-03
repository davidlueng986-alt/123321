#!/usr/bin/env python3
import itertools,json,collections
C=[[0,-1,-1,-1,4,5,6,7,8,9],
[9,7,5,-1,-1,8,4,6,-1,0],
[7,-1,8,6,5,-1,9,0,4,-1],
[8,4,-1,9,7,6,-1,-1,0,5],
[6,5,-1,0,-1,4,8,9,-1,7],
[4,0,6,-1,9,-1,5,8,7,-1],
[5,-1,0,4,6,7,-1,-1,9,8],
[-1,8,7,5,-1,9,0,4,6,-1],
[-1,6,9,8,0,-1,7,-1,5,4],
[-1,9,4,7,8,0,-1,5,-1,6]]
N=10
assert all(len(x)==N for x in C)
assert all(len({v for v in x if v>=0})==7 for x in C)
assert all(len({C[r][c] for r in range(N) if C[r][c]>=0})==7 for c in range(N))
missing={1,2,3}
# For the 30 unfilled cells, each symbol 1/2/3 occurs once per row and column.
allowed=[[(r,c) for c in range(N) if C[r][c]<0] for r in range(N)]
assert all(len(x)==3 for x in allowed)
seen=[0]*3
solutions=[];nodes=0
# each row: six permutations of missing colors in its three holes
forperm=list(itertools.permutations([1,2,3]))
F=[row[:] for row in C]
def dfs(r):
    global nodes
    nodes+=1
    if r==N:
        assert all(sorted(F[r])==list(range(N)) for r in range(N))
        assert all(sorted(F[r][c] for r in range(N))==list(range(N)) for c in range(N))
        solutions.append([row[:] for row in F]);return
    for perm in forperm:
        if any(seen[v-1]>>c&1 for (_,c),v in zip(allowed[r],perm)):continue
        for (_,c),v in zip(allowed[r],perm):seen[v-1]|=1<<c;F[r][c]=v
        dfs(r+1)
        for (_,c),v in zip(allowed[r],perm):seen[v-1]^=1<<c;F[r][c]=-1
dfs(0)
print(json.dumps({'number_of_C_completions':len(solutions),'nodes':nodes,'first':solutions[0] if solutions else None}),flush=True)
open(__import__('pathlib').Path(__file__).with_name('C7_all_complete.json'),'w').write(json.dumps({'Cfixed':C,'C_completions':solutions,'nodes':nodes}))