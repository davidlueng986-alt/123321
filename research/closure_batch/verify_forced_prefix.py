"""Independent exhaustive support reconstruction and proof replay. No search-generator imports."""
import hashlib
import itertools
import json
from pathlib import Path


def verify(prefix, cert):
    digest = hashlib.sha256(json.dumps(prefix, separators=(",", ":")).encode()).hexdigest()
    assert digest == cert["prefix_sha256"]
    assert len(prefix) == 3
    n, k = len(prefix[0][0]), len(prefix[0])
    assert 0 < k < n and (cert["n"], cert["k"], cert["q"]) == (n, k, n-k)
    targets = set(range(n))
    for square in prefix:
        assert len(square) == k
        assert all(len(row) == n and set(row) == targets for row in square)
        assert all(len({row[c] for row in square}) == k for c in range(n))
    pairs = ((0, 1), (0, 2), (1, 2))
    seen = [set(zip((x for row in prefix[a] for x in row),
                    (x for row in prefix[b] for x in row))) for a, b in pairs]
    assert all(len(s) == n*k for s in seen)
    demands = set()
    for s in range(3):
        for c in range(n):
            for x in range(n):
                if all(row[c] != x for row in prefix[s]):
                    demands.add(("c", s, c, x))
    for i in range(3):
        for a, b in itertools.product(range(n), repeat=2):
            if (a, b) not in seen[i]:
                demands.add(("p", i, a, b))
    options, support = [], {d: [] for d in demands}
    # All n^4 possibilities, independent of the producer's missing-symbol product.
    for p in itertools.product(range(n), repeat=4):
        c, a, b, d = p
        values = a, b, d
        if any(any(row[c] == values[s] for row in prefix[s]) for s in range(3)):
            continue
        if any((values[x], values[y]) in seen[i] for i, (x, y) in enumerate(pairs)):
            continue
        resources = [("c", s, c, values[s]) for s in range(3)]
        resources += [("p", i, values[x], values[y]) for i, (x, y) in enumerate(pairs)]
        options.append(p)
        for resource in resources:
            support[resource].append(p)
    assert len(options) == cert["legal_options"]
    assert len(demands) == cert["missing_demands"]
    assert cert["status"] == "NO_COMPLETION_OF_THIS_PREFIX"
    if cert["kind"] == "zero_support":
        assert tuple(cert["demand"]) in support and not support[tuple(cert["demand"])]; return True
    assert cert["kind"] == "forced_row_graph"
    assert cert["initially_forced_options"] == len({pts[0] for pts in support.values() if len(pts) == 1})
    placements = []
    for unit in cert["units"]:
        p, demand = tuple(unit["placement"]), tuple(unit["demand"])
        assert support[demand] == [p]
        placements.append(p)
    assert len(set(placements)) == len(placements) > 0
    graph = [[i != j and bool(set((z, x) for z, x in enumerate(p)) &
                               set((z, x) for z, x in enumerate(q)))
              for j, q in enumerate(placements)] for i, p in enumerate(placements)]
    assert graph == cert["graph"]
    colors = [-1] * len(graph)
    colors[0] = 0  # Any q-coloring can be globally renamed this way.

    def replay(proof):
        assert proof["status"] == "UNSAT"
        v = proof["vertex"]
        assert type(v) is int and 0 <= v < len(graph) and colors[v] == -1
        allowed = {c for c in range(n-k)
                   if all(not edge or colors[u] != c for u, edge in enumerate(graph[v]))}
        children = proof["children"]
        assert len(children) == len(allowed) and {x["color"] for x in children} == allowed
        for child in children:
            colors[v] = child["color"]; replay(child["proof"]); colors[v] = -1
    replay(cert["color_proof"])
    return True


if __name__ == "__main__":
    root = Path(__file__).parent
    source = json.loads((root / "row_cover_fixture.json").read_text())
    proof = json.loads((root / "forced_prefix_certificate.json").read_text())
    assert verify(source["prefix"], proof)
    print("INDEPENDENT_FULL_PREFIX_OBSTRUCTION_PASS; global MOLS10 OPEN")
