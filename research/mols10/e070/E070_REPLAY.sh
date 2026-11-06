#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
python E070_EIGHT_CYCLE_INDEPENDENT_VERIFY.py
python E070_INDEPENDENT_VERIFY.py
python E070_dynamic_oracle.py E070_R4_COMPRESSED_EXACT_CERT_BRANCH0.json --output E070_REPLAY_DYNAMIC_ORACLE.json
python - <<'PY'
import json
x=json.load(open('E070_REPLAY_DYNAMIC_ORACLE.json'))
assert x['status']=='SOUND_NOGOODS_INT_QUADRATIC_CERTIFIED'
assert x['exact_negative_quadratic']==-90 and x['nogood_size']==38
r=json.load(open('E070_EIGHT_CYCLE_INDEPENDENT_RESULTS.json'))
assert len(r['eight_independent_exact_cuts'])==8
print('E070 CLEAN INDEPENDENT PROOF REPLAY PASS. E064 complete branches UNSAT remains 0/1700.')
PY

# E070-B: full exact-cover solver R4 integration smoke test
python E070_make_psd_features.py 0
g++ -std=c++17 -O3 E070_DLX_PSD_EXPERIMENT.cpp -o E070_DLX_PSD_EXPERIMENT
./E070_DLX_PSD_EXPERIMENT 10 2 1000000 \
  '0,2,1,4,3,6,5,8,9,7' '0,3,4,1,2,7,8,9,5,6' E070_branch0_psd_features.bin \
  > E070_REPLAY_DLX_PSD.json 2> E070_REPLAY_DLX_PSD.log
python E070_VERIFY_DLX_FIRST_CUT.py E070_DLX_FIRST_CUT_LIVE.json
python - <<'PY_DELTA'
import json
r=json.load(open('E070_REPLAY_DLX_PSD.json'))
assert r['status']=='UNKNOWN_BUDGET'
assert r['psd_cuts']>0 and r['psd_uncertified']>=0
assert json.load(open('E070_DLX_FIRST_CUT_LIVE.json'))['exact_negative_quadratic']<0
print('E070-B live DLX R4 integer-gated pruning smoke PASS:',r['psd_cuts'],'integer-certified internal cuts; status UNKNOWN')
PY_DELTA
