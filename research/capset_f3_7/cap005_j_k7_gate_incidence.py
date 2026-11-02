#!/usr/bin/env python3
"""CAP-005J: exact seven-fiber outsider necessary gate via incidence enumeration.
NOT a cap construction and NOT a global upper bound. Independent C++ checker
enumerates release neighborhoods directly, rather than outsider incidences.
"""
import argparse
import itertools
import json
import math
from array import array
from collections import Counter
from pathlib import Path

N = math.comb(27, 7)

def load_points(path):
    lines = [s.strip() for s in Path(path).read_text().splitlines()]
    pts = [tuple(map(int, s)) for s in lines if len(s) == 7 and set(s) <= {'0','1','2'}]
    assert len(pts) == 236 and len(set(pts)) == 236
    return pts

def fid(p): return 9*p[0] + 3*p[1] + p[2]

def rank(mask):
    out = 0
    j = 1
    while mask:
        bit = mask & -mask
        out += math.comb(bit.bit_length() - 1, j)
        mask ^= bit
        j += 1
    assert j == 8
    return out

def unrank(r):
    ans = []
    for k in range(7, 0, -1):
        n = 26
        while math.comb(n, k) > r: n -= 1
        ans.append(n)
        r -= math.comb(n, k)
    return sorted(ans)

def census(path):
    points = load_points(path)
    present = set(points)
    edges = {p:set() for p in itertools.product(range(3), repeat=7) if p not in present}
    for a, b in itertools.combinations(points, 2):
        x = tuple((-u-v) % 3 for u, v in zip(a, b))
        assert x not in present
        if fid(a) != fid(b): edges[x].add((1 << fid(a)) | (1 << fid(b)))
    assert len(edges) == 1951
    counts = array('H', [0]) * N
    k_hist = Counter()
    incidences = 0
    formula_total = 0
    for x in sorted(edges):
        f = fid(x)
        pair_masks = sorted(edges[x])
        k = len(pair_masks)
        k_hist[k] += 1
        used = 1 << f
        pairs = []
        for e in pair_masks:
            assert e.bit_count() == 2 and not (used & e), (x, e)
            a = (e & -e).bit_length() - 1
            b = (e ^ (e & -e)).bit_length() - 1
            pairs.append((a,b))
            used |= e
        if k > 6: continue
        extras = [i for i in range(27) if not ((used >> i) & 1)]
        assert len(extras) == 26 - 2*k
        formula_total += sum(math.comb(k,t) * 2**(k-t) * math.comb(26-2*k, 6-k-t)
                             for t in range(7-k))
        def select_pairs(i, mask, selected):
            nonlocal incidences
            if selected > 6: return
            if i == k:
                for extra in itertools.combinations(extras, 6-selected):
                    mm = mask
                    for b in extra: mm |= 1 << b
                    counts[rank(mm)] += 1
                    incidences += 1
                return
            a, b = pairs[i]
            select_pairs(i+1, mask | (1 << a), selected+1)
            select_pairs(i+1, mask | (1 << b), selected+1)
            select_pairs(i+1, mask | (1 << a) | (1 << b), selected+2)
        select_pairs(0, 1 << f, 0)
    assert incidences == formula_total == 2946160
    hist = Counter(counts)
    excluded = sum(v for k, v in hist.items() if k <= 16)
    mx = max(hist)
    max_groups = [unrank(i) for i, v in enumerate(counts) if v == mx]
    assert (N, excluded, mx, hist[mx], len(max_groups)) == (888030, 862906, 198, 8, 8)
    assert dict(sorted(k_hist.items())) == {1:8,2:16,3:64,4:142,5:712,6:297,7:320,8:8,9:384}
    return dict(status='NECESSARY_ONLY_RESTRICTED_NO_GLOBAL_BOUND',
                baseline=236, released_fibers=7, total=N, excluded_by_16_outsider_gate=excluded,
                not_excluded=N-excluded, max_admissible_outsiders=mx,
                max_groups=sorted(max_groups), incidence_count=incidences,
                outsider_matching_size_histogram={str(k):v for k,v in sorted(k_hist.items())},
                histogram={str(k):v for k,v in sorted(hist.items())}, seed=None, gpu=False)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', type=Path, default=Path(__file__).parent/'candidates'/'calderbank_fishburn_236.txt')
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    result = census(args.baseline)
    s = json.dumps(result, sort_keys=True, separators=(',',':'))+'\n'
    if args.out: args.out.write_text(s)
    print(json.dumps({k:v for k,v in result.items() if k not in ('histogram','max_groups')},sort_keys=True))
