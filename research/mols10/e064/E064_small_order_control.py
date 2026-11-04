#!/usr/bin/env python3
"""Independent brute-force isotopy/S3 first-column classification for small n;
pass all resulting representatives into full 5-coordinate exact-cover solver.
This is deliberately independent of 9-symbol C++ centralizer implementations.
"""
import itertools,subprocess,json,time,collections,sys
from pathlib import Path


def compose(f,g):return tuple(f[g[i]] for i in range(len(f)))
def invert(f):return tuple(f.index(i) for i in range(len(f)))
def conjugate(f,p):
    pi=invert(p)
    return tuple(p[f[pi[i]]] for i in range(len(f)))

def group_orbits(m):
    alls=list(itertools.permutations(range(m)))
    identity=tuple(range(m))
    ders=[p for p in alls if all(p[i]!=i for i in range(m))]
    universe={(f,g) for f in ders for g in ders if all(f[i]!=g[i] for i in range(m))}
    reps=[];visited=set();maxsize=0
    for seed in sorted(universe):
        if seed in visited:continue
        reps.append(seed)
        todo=[seed];visited.add(seed)
        for f,g in todo:
            fi=invert(f)
            for a,b in ((g,f),(fi,compose(g,fi)),(invert(f),invert(g))):
                # Complete conjugacy orbit under all S_m, rather than one generator.
                for p in alls:
                    z=(conjugate(a,p),conjugate(b,p))
                    if z not in visited:
                        assert z in universe
                        visited.add(z);todo.append(z)
        maxsize=max(maxsize,len(todo))
    assert len(visited)==len(universe)
    return reps,len(universe),maxsize

def main():
    report=[]
    for n in (4,5,6):
        reps,nraw,maxsize=group_orbits(n-1)
        hits=[];statuses=collections.Counter();nodes=0
        for index,(f,g) in enumerate(reps):
            B=[0]+[i+1 for i in f];C=[0]+[i+1 for i in g]
            cmd=[str(Path(__file__).resolve().parent/'E064_firstcol_dlx'),str(n),'15','10000000',','.join(map(str,B)),','.join(map(str,C))]
            x=json.loads(subprocess.run(cmd,capture_output=True,check=True,text=True).stdout)
            assert x['status']!='UNKNOWN_BUDGET',f'n={n} branch={index} unknown'
            statuses[x['status']]+=1;nodes+=x['nodes']
            if x['status']=='SAT':
                mats=x['witness']; pairs=((0,1),(0,2),(1,2))
                assert all(sorted(row)==list(range(n)) for mat in mats for row in mat)
                assert all(sorted(mat[r][c] for r in range(n))==list(range(n)) for mat in mats for c in range(n))
                assert all(len({(mats[a][r][c],mats[b][r][c]) for r in range(n) for c in range(n)})==n*n for a,b in pairs)
                # Construct the transposed triple with correct independent B/C symbol relabel.
                bf=invert(tuple(v-1 for v in B[1:]));cg=invert(tuple(v-1 for v in C[1:]));
                B_inv=[0]+[v+1 for v in bf];C_inv=[0]+[v+1 for v in cg];
                tr=[[[mats[s][c][r] for c in range(n)] for r in range(n)] for s in range(3)];
                for r in range(n):
                    for c in range(n):
                        tr[1][r][c]=B_inv[tr[1][r][c]]
                        tr[2][r][c]=C_inv[tr[2][r][c]]
                assert all(tr[s][0][c]==c for s in range(3) for c in range(n))
                assert all(tr[0][r][0]==r for r in range(n))
                assert [tr[1][r][0] for r in range(n)]==B_inv
                assert [tr[2][r][0] for r in range(n)]==C_inv
                assert all(len({(tr[a][r][c],tr[b][r][c]) for r in range(n) for c in range(n)})==n*n for a,b in pairs)
                hits.append({'id':index,'B_col0':B,'C_col0':C,'transpose_check':'PASS','witness':mats})
        if n==6:assert len(hits)==0
        else:assert len(hits)>0
        s=dict(n=n,raw_pairs=nraw,global_orbits=len(reps),largest_orbit=maxsize,branch_results=dict(statuses),nodes=nodes,sat_witnesses=hits)
        report.append(s)
        print('n',n,'raw',nraw,'global_orbits',len(reps),'statuses',dict(statuses),'total_nodes',nodes,flush=True)
    Path(str(Path(__file__).resolve().parent/'E064_small_order_cover_12.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()