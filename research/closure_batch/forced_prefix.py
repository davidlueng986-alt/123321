"""Sound forced-placement row obstruction; never infer a global MOLS result."""
import hashlib
import itertools
import json
from pathlib import Path


def prefix_hash(prefix):
    return hashlib.sha256(json.dumps(prefix, separators=(",", ":")).encode()).hexdigest()


def model(prefix):
    assert len(prefix) == 3
    k, n = len(prefix[0]), len(prefix[0][0])
    assert 0 < k < n
    pairs = list(itertools.combinations(range(3), 2))
    for square in prefix:
        assert len(square) == k
        assert all(len(row) == n and set(row) == set(range(n)) for row in square)
        assert all(len({row[c] for row in square}) == k for c in range(n))
    used = [{(prefix[a][r][c], prefix[b][r][c]) for r in range(k) for c in range(n)}
            for a, b in pairs]
    assert all(len(s) == k * n for s in used)
    missing = [[set(range(n)) - {row[c] for row in prefix[s]} for c in range(n)]
               for s in range(3)]
    demands = [("c", s, c, x) for s in range(3) for c in range(n)
               for x in sorted(missing[s][c])]
    demands += [("p", i, a, b) for i in range(3) for a in range(n)
                for b in range(n) if (a, b) not in used[i]]
    options, support = [], {d: [] for d in demands}
    for c in range(n):
        for v in itertools.product(*(sorted(missing[s][c]) for s in range(3))):
            if any((v[a], v[b]) in used[i] for i, (a, b) in enumerate(pairs)):
                continue
            j = len(options)
            options.append((c,) + v)
            for s in range(3):
                support["c", s, c, v[s]].append(j)
            for i, (a, b) in enumerate(pairs):
                support["p", i, v[a], v[b]].append(j)
    return n, k, options, support


def graph(points):
    return [[i != j and any(x == y for x, y in zip(p, q))
             for j, q in enumerate(points)] for i, p in enumerate(points)]


def coloring(g, q, budget=100000):
    colors = [-1] * len(g)
    nodes = 0
    if colors:
        colors[0] = 0  # Global color-renaming symmetry only.

    def visit():
        nonlocal nodes
        nodes += 1
        if nodes > budget:
            return {"status": "UNKNOWN"}
        unassigned = [v for v in range(len(g)) if colors[v] < 0]
        if not unassigned:
            return {"status": "SAT", "colors": colors[:]}
        def score(v):
            return len({colors[u] for u, edge in enumerate(g[v]) if edge and colors[u] >= 0}), sum(g[v]), -v
        v = max(unassigned, key=score)
        allowed = [c for c in range(q) if all(not edge or colors[u] != c
                                              for u, edge in enumerate(g[v]))]
        children = []
        for c in allowed:
            colors[v] = c
            result = visit()
            colors[v] = -1
            if result["status"] != "UNSAT":
                return result
            children.append({"color": c, "proof": result})
        return {"status": "UNSAT", "vertex": v, "children": children}

    result = visit()
    result["nodes"] = nodes
    return result


def certificate(prefix):
    n, k, options, support = model(prefix)
    base = {"schema": "forced-row-obstruction-v1", "prefix_sha256": prefix_hash(prefix),
            "n": n, "k": k, "q": n-k, "legal_options": len(options),
            "missing_demands": len(support), "global_status": "OPEN"}
    zero = next((d for d, ids in support.items() if not ids), None)
    if zero is not None:
        return dict(base, status="NO_COMPLETION_OF_THIS_PREFIX", kind="zero_support", demand=list(zero))
    reason = {}
    for d, ids in support.items():
        if len(ids) == 1:
            reason.setdefault(ids[0], d)
    forced = sorted(reason)
    base["initially_forced_options"] = len(forced)
    result = coloring(graph([options[i] for i in forced]), n-k)
    if result["status"] != "UNSAT":
        return dict(base, status="NO_FORCED_OBSTRUCTION" if result["status"] == "SAT" else "UNKNOWN")
    core = forced[:]
    for i in forced:
        trial = [j for j in core if i != j]
        if coloring(graph([options[j] for j in trial]), n-k)["status"] == "UNSAT":
            core = trial
    proof = coloring(graph([options[i] for i in core]), n-k)
    assert proof["status"] == "UNSAT"
    units = [{"placement": list(options[i]), "demand": list(reason[i])} for i in core]
    return dict(base, status="NO_COMPLETION_OF_THIS_PREFIX", kind="forced_row_graph",
                units=units, graph=graph([options[i] for i in core]), color_proof=proof,
                scope="All continuations of this exact prefix, not all seven-row prefixes")


def normalized_cut(prefix, proof):
    # A proof of nonextension is a necessary prerequisite; caller must independently verify it.
    assert proof["status"] == "NO_COMPLETION_OF_THIS_PREFIX"
    n = len(prefix[0][0])
    rename = [{x: c for c, x in enumerate(square[0])} for square in prefix]
    labels = [rename[0][prefix[0][r][0]] for r in range(len(prefix[0]))]
    normalized = [(labels[r], c, *(rename[s][prefix[s][r][c]] for s in range(3)))
                  for r in range(len(prefix[0])) for c in range(n)]
    options = []
    for r in range(n):
        for c in range(n):
            for a in range(n):
                for b in range(n):
                    for d in range(n):
                        if r == 0:
                            good = a == b == d == c
                        else:
                            good = len({a, b, d}) == 3 and c not in (a, b, d) and (c != 0 or a == r)
                        if good:
                            options.append((r, c, a, b, d))
    lookup = {p: i+1 for i, p in enumerate(options)}
    assert all(p in lookup for p in normalized)
    return {"schema": "normalized-oa-prefix-nogood-v1", "n": n,
            "prefix_sha256": prefix_hash(prefix), "required_proof_kind": proof["kind"],
            "numbering": "finite_tools.buildOA(n).tuples index + 1",
            "normalization": "All first rows identity; A first column identity; removed row0 units",
            "physical_to_normalized_row": labels,
            "normalized_tuples": [list(p) for p in normalized if p[0] != 0],
            "clause": [-lookup[p] for p in normalized if p[0] != 0],
            "meaning": "Not all listed cell-value assignments can be selected together",
            "global_status": "OPEN", "performance_gain_established": False}


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = json.loads((root / "row_cover_fixture.json").read_text())["prefix"]
    proof = certificate(prefix)
    from verify_forced_prefix import verify
    verify(prefix, proof)
    (root / "forced_prefix_certificate.json").write_text(json.dumps(proof, indent=2)+"\n")
    (root / "normalized_oa_cut.json").write_text(json.dumps(normalized_cut(prefix, proof), indent=2)+"\n")
    print(json.dumps({k: v for k, v in proof.items() if k not in ("units", "graph", "color_proof")}))
