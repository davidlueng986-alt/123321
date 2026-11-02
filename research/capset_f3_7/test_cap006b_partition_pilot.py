import unittest
from cap006b_partition_pilot import result
class PartitionAudit(unittest.TestCase):
    def test_seeded_matrices_and_necessary_counts(self):
        a=result()['results']
        self.assertEqual([a[k]['Q'] for k in ('base_012','low_Q2096','high_Q3186')],[2884,2096,3186])
        self.assertEqual([a[k]['max_N'] for k in ('base_012','low_Q2096','high_Q3186')],[124,2,45])
        self.assertEqual([a[k]['naive_margin_positive'] for k in ('base_012','low_Q2096','high_Q3186')],[1,0,0])
if __name__=='__main__':unittest.main()
