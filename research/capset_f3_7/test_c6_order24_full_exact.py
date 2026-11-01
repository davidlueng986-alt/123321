#!/usr/bin/env python3
"""Independent CI replay of CAP-004G's finite order-24 invariant exhaustion."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent

class TestOrder24FullExact(unittest.TestCase):
    def test_full_exact_bound_with_direct_236_witness(self):
        with tempfile.TemporaryDirectory(prefix="capset24-") as tmp:
            tmp = Path(tmp)
            data = tmp / "orbit_data.txt"
            binary = tmp / "checker"
            gen = subprocess.run(
                [sys.executable, str(HERE / "c6_order24_full_exact_data.py"),
                 "--out", str(data)],
                check=True, capture_output=True, text=True, timeout=60)
            g = json.loads(gen.stdout)
            self.assertEqual(g["valid_slice_masks"], 11434)
            self.assertEqual(g["enumeration_nodes"], 87862)
            self.assertEqual(g["known_236_direct_arithmetic"], "PASS")
            subprocess.run(
                ["g++", "-std=c++17", "-O3",
                 str(HERE / "c6_order24_full_exact.cpp"), "-o", str(binary)],
                check=True, capture_output=True, text=True, timeout=60)
            run = subprocess.run(
                [str(binary), str(data)], check=True,
                capture_output=True, text=True, timeout=120)
            result = json.loads(run.stdout)
            self.assertEqual(result["status"], "NO_237_ORDER24_INVARIANT")
            self.assertEqual(result["unordered_pairs_total"], 65373895)
            self.assertEqual(result["inspected_pairs"], 3436063)
            self.assertEqual(result["eligible_pairs"], 3424629)

if __name__ == "__main__":
    unittest.main()
