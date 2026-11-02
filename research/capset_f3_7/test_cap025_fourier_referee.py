"""CAP-025: invoke independent Node integer Fourier/convolution referee in CI.

Node is preinstalled on GitHub ubuntu-latest. No Python packages required.
"""
import json
from pathlib import Path
import subprocess
import unittest

SCRIPT = Path(__file__).with_name("cap025_fourier_referee.js")

class CAP025FourierReferee(unittest.TestCase):
    def test_exact_six_pair_fourier_and_deletion_edge_cases(self):
        result = subprocess.run(
            ["node", str(SCRIPT)], capture_output=True, text=True,
            timeout=25, check=True
        )
        cert = json.loads(result.stdout)
        self.assertEqual(cert["projective_normals"], 364)
        self.assertEqual(cert["full_convolution_vectors_per_case"], 729)
        self.assertEqual(len(cert["cases"]), 6)
        self.assertEqual([x["mstar"] for x in cert["cases"]],
                         [56,16,18,17,16,10])
        self.assertTrue(all(x["formula_errors"] == 0 for x in cert["cases"]))
        self.assertEqual([x["holes"] for x in cert["identical_dual_deletions"]],
                         list(range(5)))

if __name__ == "__main__":
    unittest.main(verbosity=2)
