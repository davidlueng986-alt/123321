#!/usr/bin/env python3
"""CAP-005E: exact six-fiber pair-removal gate; restricted necessary theorem.

Reuses the independently verified CAP-002A exhaustive pair-removal result:
any two new outsiders require deleting >=16 points of the classical 236 cap.
The CAP-005D secant census counts all individually admissible outsiders in
each six-fiber edit neighborhood. If this count <=16, improvement is impossible.
"""
import argparse
import json
from pathlib import Path
from cap005_k6_secant_matching_gate import census

def audit():
    old = census()  # Includes direct arithmetic verification of the 236 fixture.
    hist = {int(k): int(v) for k, v in old["histograms"]["6"].items()}
    assert sum(hist.values()) == 296010
    assert sum(v for n,v in hist.items() if n <= 9) == 288878
    assert sum(v for n,v in hist.items() if n <= 16) == 294394
    assert sum(v for n,v in hist.items() if n >= 17) == 1616
    assert hist[16] == 84 and hist[17] == 16
    return {
        "status": "EXACT_NECESSARY_GATE_ONLY_NOT_GLOBAL",
        "baseline": 236,
        "released_fibers": 6,
        "release_sets": 296010,
        "independently_verified_pair_removal_minimum": 16,
        "pair_removal_source": "analyze_pair_replacement.py (CI 41334968239); cap005_pair_cover_independent.cpp",
        "minimum_insertions_for_improvement": 17,
        "previous_exclusions": 288878,
        "new_exclusions": 5516,
        "total_exclusions": 294394,
        "unresolved": 1616,
        "unresolved_fraction": "1616/296010",
        "histogram": {str(k): v for k,v in sorted(hist.items())},
        "seed": None,
        "gpu": False,
        "novelty_established": False,
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    r=audit()
    if args.out: args.out.write_text(json.dumps(r,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in r.items() if k!="histogram"},sort_keys=True))
