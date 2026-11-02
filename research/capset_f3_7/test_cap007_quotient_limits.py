import unittest
from cap007_quotient_limits import result,check,planes,lines,WITNESS333
class QuotaAudit(unittest.TestCase):
    def test_exact_333_relaxation(self):
        x=result()
        self.assertEqual(x['quotient_occupancy_relaxation_optimum'],333)
        self.assertEqual([v['mod9_obstruction'] for v in x['excluded_334_through_336']],[6,4,3])
        self.assertEqual((len(lines()),len(planes())),(117,39))
        self.assertTrue(check(WITNESS333)['all_quotas_hold'])
if __name__=='__main__':unittest.main()
