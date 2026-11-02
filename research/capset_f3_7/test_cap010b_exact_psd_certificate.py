#!/usr/bin/env python3
"""CAP-010B exact integer PSD certificate regression; no floats or external deps."""
import unittest
from cap010b_exact_psd_certificate import bareiss_psd_rank, certificate, min_deletions, modular_rank

class ExactPsdTest(unittest.TestCase):
    def test_small_psd_singular(self):
        self.assertEqual(bareiss_psd_rank([[1,1],[1,1]])['rank'],1)
        self.assertEqual(bareiss_psd_rank([[1,0],[0,0]])['rank'],1)
        with self.assertRaises(AssertionError):
            bareiss_psd_rank([[1,0],[0,-1]])
        with self.assertRaises(AssertionError):
            bareiss_psd_rank([[0,1],[1,0]])
    def test_modular_rank(self):
        self.assertEqual(modular_rank([[1,2],[2,4]]),1)
        self.assertEqual(modular_rank([[1,2],[3,4]]),2)
    def test_exact_classical_spectral_certificate(self):
        c=certificate()
        self.assertEqual((c['rank'],c['nullity']),(107,4))
        self.assertEqual(c['lambda_perp_fraction'],'425/576')
        self.assertEqual(c['row_degree_histogram'],{11:32,15:192,16:160,18:240,24:60,30:32,32:1})
    def test_exact_integer_bound(self):
        self.assertEqual(min_deletions(1),2)
        self.assertEqual(min_deletions(29),30)
        self.assertEqual(min_deletions(32),32)
        self.assertEqual(min_deletions(35),34)

if __name__=='__main__':
    unittest.main()
