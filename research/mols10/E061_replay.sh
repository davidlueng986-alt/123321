#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -O3 -std=c++17 E061_full_oa_dlx.cpp -o e061_dlx
for n in 3 4 5 6; do ./e061_dlx "$n" 5 10000000 > "/tmp/e061_${n}.json"; done
g++ -O3 -std=c++17 E061_three_cycle_trade.cpp -o e061_trade3
./e061_trade3 >/tmp/e061_trade3.json
python E061_transversal_route.py > /tmp/e061_transversal_route.json
python E061_two_transversal_completion.py > /tmp/e061_two_transversal_completion.json
python E061_verify.py