import unittest
from cap006c_funsearch_slice_audit import read,check_cap,spectrum
class FunSearchProjectionAudit(unittest.TestCase):
    def test_source_512_and_complete_3280_direction_census(self):
        p=read()
        self.assertTrue(check_cap(p))
        s=spectrum(p)
        self.assertEqual(s['directions'],3280)
        self.assertEqual(s['max_7D_section'],208)
        self.assertEqual(s['directions_attaining_208'],8)
if __name__=='__main__':unittest.main()
