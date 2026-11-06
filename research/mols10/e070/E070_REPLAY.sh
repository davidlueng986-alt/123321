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
