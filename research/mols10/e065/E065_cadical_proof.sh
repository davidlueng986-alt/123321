#!/usr/bin/env bash
# Proof-carrying SAT branch gate: supply proof checker independently.
# Examples: bash E065_cadical_proof.sh 5 0 30 E065_n5_reps.jsonl
#           bash E065_cadical_proof.sh 10 0 60 E064_12_representatives.jsonl
# Requires pinned CaDiCaL>=1.7 and lrat-check; no network operations here.
set -euo pipefail
cd "$(dirname "$0")"
N="${1:?order}"; BR="${2:?canonical branch index}"; SEC="${3:-30}"; REPS="${4:-E064_12_representatives.jsonl}"
CADICAL="${CADICAL:-cadical}"; LRAT_CHECK="${LRAT_CHECK:-lrat-check}"
mkdir -p E065_proof_outputs
BASE="E065_proof_outputs/E065_n${N}_base.cnf"
CNF="E065_proof_outputs/E065_n${N}_branch${BR}.cnf"
PROOF="E065_proof_outputs/E065_n${N}_branch${BR}.lrat"
LOG="E065_proof_outputs/E065_n${N}_branch${BR}.log"
python E065_cnf.py "$N" --output "$BASE"
python E065_branch_dimacs.py --base "$BASE" --n "$N" --reps "$REPS" --branch "$BR" --output "$CNF"
set +e
"$CADICAL" --lrat --no-binary --no-factor -t "$SEC" "$CNF" "$PROOF" > "$LOG" 2>&1
STATUS=$?
set -e
if [[ "$STATUS" == 10 ]]; then
  python E065_verify.py --n "$N" --sat-output "$LOG" --output "E065_proof_outputs/E065_n${N}_branch${BR}_witness.json"
  echo "SAT_FULL_WITNESS_VERIFIED branch=$BR"
elif [[ "$STATUS" == 20 ]]; then
  set +e
  "$LRAT_CHECK" "$CNF" "$PROOF" > "E065_proof_outputs/E065_n${N}_branch${BR}_lrat_check.log" 2>&1
  CHECK_STATUS=$?
  set -e
  [[ "$CHECK_STATUS" == 0 || "$CHECK_STATUS" == 20 ]] || { cat "E065_proof_outputs/E065_n${N}_branch${BR}_lrat_check.log"; exit 1; }
  grep -Eq '^(s VERIFIED|VERIFIED)( |$)' "E065_proof_outputs/E065_n${N}_branch${BR}_lrat_check.log" || { cat "E065_proof_outputs/E065_n${N}_branch${BR}_lrat_check.log"; exit 1; }
  echo "UNSAT_WITH_INDEPENDENT_LRAT_CERTIFICATE branch=$BR"
elif [[ "$STATUS" == 0 || "$STATUS" == 124 ]]; then
  echo "UNKNOWN_BUDGET branch=$BR"
else
  cat "$LOG" >&2
  echo "UNEXPECTED_SOLVER_EXIT=$STATUS" >&2
  exit 1
fi