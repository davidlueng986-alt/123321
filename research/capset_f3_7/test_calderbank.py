#!/usr/bin/env python3
import unittest
from generate_calderbank_fishburn import construction
from analyze_secants import analyze
from analyze_slices import analyze_slices

class CalderbankFishburnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points=construction()
        cls.analysis=analyze(cls.points)
    def test_certificate_size_and_uniqueness(self):
        self.assertEqual(len(set(self.points)),236)
    def test_three_slices(self):
        self.assertEqual([sum(p[0]==i for p in self.points) for i in range(3)],[112,112,12])
    def test_complete(self):
        self.assertTrue(self.analysis["is_complete"])
        self.assertEqual(self.analysis["outside_points"],1951)
    def test_secant_accounting(self):
        a=self.analysis
        self.assertEqual(a["total_secants"],236*235//2)
        self.assertEqual(a["minimum_secants_per_outside"],10)
        self.assertEqual(a["maximum_secants_per_outside"],56)
    def test_third_slice_unique(self):
        outcome=analyze_slices()
        self.assertEqual(outcome['cross_blocked_slice2'],717)
        self.assertEqual(len(outcome['only_12_compatible_slice2_points']),12)
        self.assertEqual(outcome['minimum_cross_secants_for_nonmember_slice2'],11)

    def test_exact_secant_histogram(self):
        expected={10:24,11:416,12:480,13:160,14:120,15:192,16:224,18:240,25:60,30:32,38:1,56:2}
        self.assertEqual(self.analysis["secant_histogram"],expected)

if __name__=="__main__":
    unittest.main()
