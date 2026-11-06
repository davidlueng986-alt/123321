#!/usr/bin/env bash
# Exact independent reproducer. No internet, no GPU, no untrusted solver output.
set -euo pipefail
cd "$(dirname "$0")"
g++ -std=c++17 -O3 -Wall -Wextra E068_partial_transversal_core.cpp -o E068_partial_transversal_core
python E068_independent_verify.py
python E068_normalize_clause.py
python - <<'PY'
import json
x=json.load(open('E068_independent_results.json'))
assert x['global_problem_status']=='OPEN'
assert x['best_partial_core_size']==116
assert len(x['all_12_unsupported_anchors_verified'])==12
assert all(a['every_one_literal_deletion_has_transversal']=='VERIFIED' for a in x['all_12_unsupported_anchors_verified'])
assert x['independent_positive_GF5_anchor_checks']==25
v=json.load(open('E068_all_12_sound_nogoods.json'))
assert len(v['cuts'])==12 and sum(z['count'] for z in v['cuts'])==1446
print('E068 PROOF-SOUND LOCAL NOGOODS: 12/12 VERIFIED; GF5 POSITIVE 25/25; GLOBAL MOLS10 STILL OPEN')
PY
