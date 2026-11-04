#!/usr/bin/env bash
# Single-turn exact model benchmark with no asynchronous/background execution.
set -euo pipefail
cd "$(dirname "$0")"
g++ -std=c++17 -O2 E065_incremental_z3.cpp -o E065_incremental_z3 -l:libz3.so.4
g++ -std=c++17 -O2 E065_pb_oa.cpp -o E065_pb_oa -l:libz3.so.4
g++ -std=c++17 -O3 E065_independent_dlx.cpp -o E065_independent_dlx
if [[ ! -f E064_12_representatives.jsonl ]]; then
  cp ../e064/E064_12_representatives.jsonl E064_12_representatives.jsonl
fi
for n in 4 5 6 10; do python E065_cnf.py "$n" --output "E065_n${n}.cnf"; done
python - <<'PY'
import json
from E065_small_order_symmetry import group_orbits
for n,expected in [(4,1),(5,2),(6,3)]:
    reps,_,_=group_orbits(n-1)
    assert len(reps)==expected
    with open(f'E065_n{n}_reps.jsonl','w') as f:
        for a,b in reps:f.write(json.dumps({'B_col0':[0]+[x+1 for x in a],'C_col0':[0]+[x+1 for x in b]})+'\n')
PY
./E065_incremental_z3 E065_n4.cnf 4 4 E065_n4_reps.jsonl 1 0 E065_replay_n4_cnf.jsonl
./E065_pb_oa 4 4 E065_n4_reps.jsonl 1 0 E065_replay_n4_pb.jsonl
./E065_incremental_z3 E065_n5.cnf 5 4 E065_n5_reps.jsonl 2 0 E065_replay_n5_cnf.jsonl
./E065_pb_oa 5 4 E065_n5_reps.jsonl 2 0 E065_replay_n5_pb.jsonl
./E065_incremental_z3 E065_n6.cnf 6 4 E065_n6_reps.jsonl 3 0 E065_replay_n6_cnf.jsonl
./E065_pb_oa 6 4 E065_n6_reps.jsonl 3 0 E065_replay_n6_pb.jsonl
python - <<'PY'
import json
from E065_verify import verify
for n,expected in [(4,['SAT']),(5,['UNSAT','SAT']),(6,['UNSAT']*3)]:
    for engine in ('cnf','pb'):
        src=f'E065_replay_n{n}_{engine}.jsonl'
        rec=[json.loads(t) for t in open(src)]
        assert [z['status'] for z in rec]==expected,(src,rec)
        for z in rec:
            if z['status']=='SAT':verify(z['witness'],n)
print('INDEPENDENT_SAT_AND_ORDER6_BRANCH_EXHAUSTION_CHECK_PASS')
PY

python - <<'PY_INDEPENDENT_DLX'
import json,subprocess
reps=[json.loads(s) for s in open('E065_n6_reps.jsonl')]
results=[]
for i,z in enumerate(reps):
 cmd=['./E065_independent_dlx','6','10','10000000',','.join(map(str,z['B_col0'])),','.join(map(str,z['C_col0']))]
 d=json.loads(subprocess.run(cmd,text=True,capture_output=True,check=True).stdout)
 assert d['status']=='UNSAT_EXHAUSTIVE',d
 results.append(d['nodes'])
assert sum(results)==1203,results
print('INDEPENDENT_DLX_N6_3_OF_3_EXHAUSTIVE_UNSAT',results)
PY_INDEPENDENT_DLX

# n10 probes are explicitly bounded, never claim these mean UNSAT.
./E065_incremental_z3 E065_n10.cnf 10 2 E064_12_representatives.jsonl 3 0 E065_replay_n10_cnf.jsonl
./E065_pb_oa 10 2 E064_12_representatives.jsonl 3 0 E065_replay_n10_pb.jsonl
python - <<'PY'
import json
from E065_verify import verify
for mode in ('cnf','pb'):
    r=[json.loads(s) for s in open(f'E065_replay_n10_{mode}.jsonl')]
    for z in r:
        assert z['n']==10 and z['status'] in ('SAT','UNSAT','UNKNOWN')
        if z['status']=='SAT':
            verify(z['witness'],10)
            print('CLOSED_COMPLETE_WITNESS',mode,z['branch'])
print('ORDER10_BOUNDED_RUNS_RECORDED_WITHOUT_FALSE_UNSAT')
PY