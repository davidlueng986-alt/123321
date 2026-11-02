import unittest
from cap010a_110_111_unique_completion import certificate
class SecantCompletionTest(unittest.TestCase):
    def test_all_6216_pair_deletions(self):
        r=certificate(exhaustive=True)
        self.assertEqual(r['outside_secants_histogram'],{10:616,56:1})
        self.assertEqual(r['removed_pair_completions_exhaustively_checked'],6216)
        self.assertEqual(r['disjoint_secants_per_external_point_minimum'],10)
if __name__=='__main__':unittest.main()
