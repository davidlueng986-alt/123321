import unittest
from cap007k_cross_slice_resilience import audit
class CrossSliceMultiplicityTest(unittest.TestCase):
    def test_all_3812(self):
        a=audit()
        self.assertEqual(a['matrices'],3812)
        self.assertEqual(a['hole_and_minimum_histogram']['12:11'],121)
        self.assertEqual(sum(a['hole_histogram'].values()),3812)
if __name__=='__main__':unittest.main()
