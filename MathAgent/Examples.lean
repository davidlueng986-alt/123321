module

import Mathlib

/-!
# Proof verification examples

Each theorem below is checked by Lean 4 and Mathlib.
The CI build fails if a proof is rejected.
-/

namespace MathAgent

theorem nat_add_comm_demo (a b : ℕ) : a + b = b + a := by
  exact Nat.add_comm a b

theorem square_nonnegative (x : ℝ) : 0 ≤ x ^ 2 := by
  positivity

theorem binomial_square (a b : ℤ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

theorem nat_le_add (a b : ℕ) : a ≤ a + b := by
  omega

end MathAgent
