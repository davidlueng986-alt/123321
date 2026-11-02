"""CAP-006A: check projection invariants without using a numerical optimizer."""
import unittest
from cap006_projection_audit import (read_cap, assert_cap, coordinate_audit, random_audit)
class ProjectionAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cap = read_cap()
    def test_cap_and_coordinate_profiles(self):
        assert_cap(self.cap)
        data = coordinate_audit(self.cap)
        self.assertEqual(data["number_coordinate_projections"], 35)
        self.assertEqual(sorted(x["count"] for x in data["profiles"]), [15, 20])
        self.assertEqual(sorted(x["Q"] for x in data["profiles"]), [2290, 2884])
    def test_deterministic_noncoordinate_sample(self):
        d = random_audit(self.cap)
        self.assertEqual((d["Q_min"], d["Q_median_lower"], d["Q_max"]), (2096, 2234, 3186))
        self.assertEqual(d["count_Q_at_least_2884"], 2)
        self.assertEqual((d["empty_fiber_min"], d["empty_fiber_max"]), (0, 3))
if __name__ == "__main__":
    unittest.main()
