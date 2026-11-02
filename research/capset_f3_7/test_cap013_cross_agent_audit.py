#!/usr/bin/env python3
"""CAP-013: independent, dependency-free regression for cross-agent math claims.
No external data required. Run:
 python -m unittest research/capset_f3_7/test_cap013_cross_agent_audit.py -v
"""
import unittest

def majority_residue(points, direction):
    counts = [0, 0, 0]
    for v in points:
        counts[sum(a*b for a,b in zip(v,direction)) % 3] += 1
    assert counts[1] % 3 == counts[2] % 3
    q = sum(sum(a*b for a,b in zip(v,direction))**2 for v in points) % 3
    return counts[1] % 3, q

def codim2_moments(M=237):
    g7 = ((3**7-1)*(3**7-3))//48
    g6 = ((3**6-1)*(3**6-3))//48
    g5 = ((3**5-1)*(3**5-3))//48
    return (g7*M, g7*M+g6*M*(M-1),
            g7*M+3*g6*M*(M-1)+g5*M*(M-1)*(M-2))

def hyperplane_second_moment(n, s):
    # Sum over all affine hyperplanes in F_3^n of squared section sizes
    num_directions=(3**n-1)//2
    shared_directions=(3**(n-1)-1)//2
    return num_directions*s + shared_directions*s*(s-1)

class CrossAgentAuditTests(unittest.TestCase):
    def test_cap011a_mandatory_negative_sign(self):
        # Centered cap {1,2} in F3: majority residue is +1, sum squares is 2
        a, q=majority_residue([(1,),(2,)], (1,))
        self.assertEqual((a,q), (1,2))
        self.assertEqual(a,(-q)%3)
        self.assertNotEqual(a,q)
    def test_cap011b_global_moments(self):
        self.assertEqual(codim2_moments(),(23572731,639439983,17775438687))
    def test_cap011b_89_slice_subslice_gate(self):
        # If all codimension-1 slices <= cap, maximize sum of squares
        # independently per direction, then compare to forced exact sum.
        for s,upper in [(89,32),(91,33),(92,33),(93,33)]:
            possibilities=[(a,b,s-a-b) for a in range(upper+1)
                           for b in range(upper+1) if 0<=s-a-b<=upper]
            worst=max(sum(x*x for x in t) for t in possibilities)
            self.assertGreater(hyperplane_second_moment(6,s),364*worst)

if __name__=='__main__':unittest.main()
