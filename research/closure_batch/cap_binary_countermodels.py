"""Explicit SAT countermodels for the binary-only relaxation of all ten dense-H leaves.
These point sets are deliberately NOT caps. The full ternary clauses remain essential.
"""
import itertools
import json
from pathlib import Path


def vector(code):
    return tuple((code // (3**i)) % 3 for i in range(6, -1, -1))


def code(v):
    out = 0
    for x in v:
        out = 3*out+x
    return out


def third(a, b):
    return code(tuple((-x-y) % 3 for x, y in zip(vector(a), vector(b))))


def cases():
    frame = {0} | {3**i for i in range(7)}
    invalid = frame | {third(a, b) for a, b in itertools.combinations(frame, 2)}
    groups = {}
    for p in range(0, 2187, 3):
        if p in invalid:
            continue
        v = vector(p)
        lam = ((1-sum(v)) % 3,) + v[:6]
        tag = (0,) + tuple(lam.count(x) for x in range(3))
        groups.setdefault(tag, []).append(p)
    assert len(groups) == 10 and sum(map(len, groups.values())) == 701
    return frame, sorted(groups.items())


def generate():
    frame, grouped = cases()
    out = []
    for branch, (tag, ids) in enumerate(grouped):
        selected = frame | {ids[0]}
        zeros = {third(a, b) for a, b in itertools.combinations(selected, 2)}
        free = set(range(2187)) - selected - zeros
        adjacency = {p: set() for p in free}
        for s in selected:
            for p in free:
                q = third(s, p)
                if q in free:
                    adjacency[p].add(q)
        available, chosen = free.copy(), []
        while available:
            high = {p for p in available if p % 3 == 0}
            pool = high or available
            p = min(pool, key=lambda x: (len(adjacency[x] & available), x))
            chosen.append(p)
            available.difference_update(adjacency[p] | {p})
        high = [p for p in chosen if p % 3 == 0]
        outside = [p for p in chosen if p % 3 != 0]
        assert len(high) >= 81 and len(outside) >= 147
        threshold = sorted(high[:81] + outside[:147])
        lookup = set(threshold)
        violation = next((a, b, third(a, b)) for a, b in itertools.combinations(threshold, 2)
                         if third(a, b) in lookup)
        out.append({"branch": branch, "orbit_tag": tag, "orbit_size": len(ids),
                    "ninth_point": ids[0], "selected_frame_codes": sorted(selected),
                    "greedy_free_codes": chosen, "threshold_free_codes": threshold,
                    "threshold_total": 237, "threshold_H_total": 89,
                    "violated_full_model_ternary": violation,
                    "relaxation_status": "SAT_BINARY_PLUS_BOTH_CARDINALITIES",
                    "full_root_status": "UNKNOWN"})
    return {"schema": "ten-leaf-binary-countermodels-v1", "root_cap7_status": "OPEN",
            "coordinate_encoding": "most-significant-first base3; H is code%3==0",
            "scope": "Only binary clauses from fixed selected points plus root cardinalities",
            "cases": out}


if __name__ == "__main__":
    report = generate()
    path = Path(__file__).with_name("cap_binary_countermodels.json")
    path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"branches": len(report["cases"]), "all_thresholds": 237,
                      "root": "OPEN", "actual_caps": False}))
