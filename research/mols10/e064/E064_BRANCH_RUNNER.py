#!/usr/bin/env python3
"""On-demand sharded search over the mathematically complete E064 1700-orbit list.
UNKNOWN never considered UNSAT. A found full triple is immediately checked independently.
No automatic scheduling or background processes.
"""
import argparse,hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def verify(S,n=10):
    assert len(S)==3
    assert all(len(M)==n and all(sorted(row)==list(range(n)) for row in M) for M in S)
    assert all(sorted(M[r][c] for r in range(n))==list(range(n)) for M in S for c in range(n))
    for a,b in ((0,1),(0,2),(1,2)):
        pairs={(S[a][r][c],S[b][r][c]) for r in range(n) for c in range(n)}
        assert len(pairs)==n*n
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--start',type=int,default=0)
    p.add_argument('--count',type=int,default=5)
    p.add_argument('--seconds',type=float,default=.3)
    p.add_argument('--max-nodes',type=int,default=1_000_000)
    p.add_argument('--output',default='E064_branch_log.jsonl')
    a=p.parse_args()
    reps=[json.loads(t) for t in (ROOT/'E064_12_representatives.jsonl').read_text().splitlines()]
    assert len(reps)==1700
    assert 0<=a.start<1700 and 0<a.count<=1700-a.start
    output=Path(a.output)
    with output.open('a') as f:
        for i in range(a.start,a.start+a.count):
            z=reps[i]
            cmd=[str(ROOT/'E064_firstcol_dlx'),'10',str(a.seconds),str(a.max_nodes),','.join(map(str,z['B_col0'])),','.join(map(str,z['C_col0']))]
            raw=subprocess.run(cmd,capture_output=True,text=True,check=True)
            run=json.loads(raw.stdout)
            assert run['n']==10 and run['status'] in {'SAT','UNSAT_EXHAUSTIVE','UNKNOWN_BUDGET'}
            if run['status']=='SAT':
                assert verify(run['witness'])
                witness={'n':10,'verified':'INDEPENDENT_100_100_100','squares':run['witness'],'branch':i}
                name=ROOT/f'E064_CLOSED_WITNESS_{i}.json'
                name.write_text(json.dumps(witness,indent=2)+'\n')
                print('CLOSED_WITNESS',name,flush=True)
            record={'branch':i,'type':z['type'],'status':run['status'],'nodes':run['nodes'],'maxdepth':run['maxdepth'],'seconds':run['seconds'],'stdout_sha256':hashlib.sha256(raw.stdout.encode()).hexdigest()}
            f.write(json.dumps(record,sort_keys=True)+'\n');f.flush();print(record,flush=True)