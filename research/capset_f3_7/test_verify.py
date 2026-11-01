#!/usr/bin/env python3
import itertools
import tempfile
import unittest
from pathlib import Path
from verify_capset import read_points, verify

class CapSetTests(unittest.TestCase):
    def test_full_binary_cube(self):
        self.assertEqual(verify(itertools.product((0,1),repeat=7)),128)
    def test_invalid_triple(self):
        a=(0,)*7; b=(1,)+(0,)*6; c=(2,)+(0,)*6
        with self.assertRaisesRegex(ValueError,"Forbidden triple"):
            verify([a,b,c])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            verify([(0,)*7,(0,)*7])
    def test_bad_coordinate(self):
        with self.assertRaisesRegex(ValueError,"Malformed"):
            verify([(3,)*7])
    def test_parser(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"points.txt"
            p.write_text("n: 7\n0000000\n1000000\n",encoding="utf-8")
            self.assertEqual(verify(read_points(p)),2)
            p.write_text("0000009\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"Invalid coordinate"):
                read_points(p)
if __name__=="__main__":
    unittest.main()
