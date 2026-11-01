module

import Mathlib

/-!
# Erdős–Straus: an elementary infinite residue class

For each k ≥ 0, let n = 3k+2. The positive integer witnesses are
  x = k+1
  y = n
  z = n(k+1).
Then 4/n = 1/x + 1/y + 1/z.

This is a previously known subcase, **not** a resolution of the conjecture.
-/

namespace MathAgent

theorem erdos_straus_mod3_family (k : ℕ) :
    ∃ x y z : ℕ,
      0 < x ∧ 0 < y ∧ 0 < z ∧
      (4 : ℚ) / (3 * (k : ℚ) + 2) =
        1 / (x : ℚ) + 1 / (y : ℚ) + 1 / (z : ℚ) := by
  refine ⟨k + 1, 3 * k + 2, (k + 1) * (3 * k + 2), ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · positivity
  · have hk : (k : ℚ) + 1 ≠ 0 := by positivity
    have hn : 3 * (k : ℚ) + 2 ≠ 0 := by positivity
    push_cast
    field_simp
    ring

end MathAgent
