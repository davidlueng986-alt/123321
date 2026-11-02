#!/usr/bin/env python3
"""CAP-007J: exact 2nd/3rd affine-hyperplane moment gate for hypothetical 237-caps.
Pure Python integers, no optimization, GPU, randomness, or external dependencies.
"""
import argparse
import itertools
import json
from pathlib import Path


def coefficients(n):
    assert n >= 2
    return ((3**n - 1)//2, (3**(n-1)-1)//2, (3**(n-2)-1)//2)


def predicted_moments(n, m):
    normals, pair_normals, triple_normals = coefficients(n)
    second = normals*m + pair_normals*m*(m-1)
    third = normals*m + 3*pair_normals*m*(m-1) + triple_normals*m*(m-1)*(m-2)
    return second, third


def affine_normal_representatives(n):
    for a in itertools.product(range(3), repeat=n):
        if any(a) and next(x for x in a if x) == 1:
            yield a


def is_cap(points):
    if len(points) != len(set(points)):
        return False
    S = set(points)
    for i, a in enumerate(points):
        for b in points[i+1:]:
            if tuple((-x-y) % 3 for x, y in zip(a, b)) in S:
                return False
    return True


def measured_moments(points, n):
    assert all(len(p) == n and all(x in (0, 1, 2) for x in p) for p in points)
    s2 = s3 = 0
    maximum = 0
    for a in affine_normal_representatives(n):
        counts = [0, 0, 0]
        for p in points:
            counts[sum(x*y for x, y in zip(a, p)) % 3] += 1
        s2 += sum(x*x for x in counts)
        s3 += sum(x*x*x for x in counts)
        maximum = max(maximum, *counts)
    return s2, s3, maximum


def gate_237():
    n, m, center, cap_at_most = 7, 237, 79, 88
    normals, pairs, triples = coefficients(n)
    s2, s3 = predicted_moments(n, m)
    variance_sum = s2 - 3*center**2*normals
    centered_cubic_sum = (s3 - 3*center*s2
                          + 3*center**2*m*normals - 3*center**3*normals)
    contradiction = centered_cubic_sum + 9*variance_sum
    assert (normals, pairs, triples) == (1093, 364, 121)
    assert (s2, s3, variance_sum, centered_cubic_sum, contradiction) == (
        20618289, 1651763205, 154050, -1421526, -35076)
    checked = 0
    minimum = None
    for a in range(max(0, m-2*cap_at_most), cap_at_most+1):
        for b in range(a, cap_at_most+1):
            c = m-a-b
            if not b <= c <= cap_at_most:
                continue
            deviations = [a-center, b-center, c-center]
            v = sum(x*x for x in deviations)
            w = sum(x*x*x for x in deviations)
            assert w+9*v >= 0, (a,b,c)
            minimum = w+9*v if minimum is None else min(minimum, w+9*v)
            checked += 1
    assert checked == 75 and minimum == 0
    # 89 is optimal for this 2nd/3rd-moment relaxation: rational convex
    # mixture of 3 admissible slice profiles with max 89 matches both moments.
    weights = [(91324,409875), (19829,409875), (99574,136625)]
    profiles = [(59,89,89), (74,74,89), (79,79,79)]
    from fractions import Fraction
    assert sum(Fraction(*w) for w in weights) == 1
    assert sum(Fraction(*weights[i])*sum((x-center)**2 for x in p)
               for i,p in enumerate(profiles)) == Fraction(variance_sum,normals)
    assert sum(Fraction(*weights[i])*sum((x-center)**3 for x in p)
               for i,p in enumerate(profiles)) == Fraction(centered_cubic_sum,normals)
    return {'scope':'any 237-point cap in F3^7',
            'normal_directions':normals,'pair_normal_directions':pairs,
            'noncollinear_triple_normal_directions':triples,
            'sum_squared_slice_sizes':s2,'sum_cubed_slice_sizes':s3,
            'sum_centered_variance':variance_sum,
            'sum_centered_cubic':centered_cubic_sum,
            'if_all_slices_at_most_88_then_cubic_plus_9_variance_at_least':0,
            'required_exact_value':contradiction,
            'sorted_profiles_checked':checked,
            'conclusion':'Every 237-cap has an affine 6D hyperplane containing >=89 points.',
            'does_not_prove_237_exists':True,
            'moment_relaxation_cannot_force_90':True}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--witness', type=Path, help='optional independent 236-cap regression fixture')
    args = p.parse_args()
    result = gate_237()
    if args.witness:
        raw = [line.strip() for line in args.witness.read_text().splitlines() if line.strip()]
        if raw and raw[0].startswith('n:'):
            assert raw.pop(0) == 'n: 7'
        assert all(len(s) == 7 and set(s) <= {'0','1','2'} for s in raw)
        pts = [tuple(map(int, s)) for s in raw]
        assert len(pts) == 236 and is_cap(pts)
        measured = measured_moments(pts,7)
        assert measured[:2] == predicted_moments(7,len(pts))
        result['witness_236_audit'] = {'valid_cap':True, 'second':measured[0],
                                        'third':measured[1], 'max_slice':measured[2]}
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
