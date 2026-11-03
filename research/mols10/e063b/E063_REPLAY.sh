#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 E063_cotrade_search.py > E063_cotrade_test.log
python3 E063_deeper_cotrades.py > E063_deeper_test.log
python3 E063_component_trade_graph.py
python3 E063_tradenet_bfs.py
node E063_INDEPENDENT_TRADE_COMPONENT.js
node E063_VERIFY_EGAN_SYMMETRY.js
python3 E063_export_pairs.py
g++ -O3 -std=c++17 E063_2x2_cotrade.cpp -o ./e063_cross
./e063_cross E063_A2_VARIANTS.bin E063_B2_VARIANTS.bin E063_2x2_CROSS_RESULTS.json
python3 E063_verify_44m.py
python3 - <<'PY'
import json
r=json.load(open('E063_TRADENET_RESULTS.json'))
assert r['status']=='EXACT_FINITE_TRADE_COMPONENT_EXHAUSTED' and r['visited_pairs']==64
assert r['trade_edges_tested']==384 and r['max_packing']==1 and r['max_transversals']==10
c=json.load(open('E063_2x2_VERIFIED_SUMMARY.json'))
assert c['none_nonrelabel'] and c['orthogonal_hits']==972
print('E063_ALL_FINITE_SCOPE_INDEPENDENT_REPLAYS_PASS; GLOBAL_OPEN')
PY