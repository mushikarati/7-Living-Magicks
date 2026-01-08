/-
Seven Living Magicks Canon Law - Lean 4 Formalization

This file formalizes the 7-color sequence and adjacency law in Lean 4.
-/

import Mathlib.Data.Fin.Basic
import Mathlib.Data.ZMod.Basic

namespace SevenMagicks

/-- The seven colors as a finite type (0-6) -/
abbrev Color := Fin 7

/-- Named constructors for each color -/
def black   : Color := ⟨0, by norm_num⟩
def white   : Color := ⟨1, by norm_num⟩
def yellow  : Color := ⟨2, by norm_num⟩
def brown   : Color := ⟨3, by norm_num⟩
def red     : Color := ⟨4, by norm_num⟩
def green   : Color := ⟨5, by norm_num⟩
def blue    : Color := ⟨6, by norm_num⟩

/-- The adjacency relation: colors are adjacent if they differ by ±1 mod 7 -/
def adjacent (c1 c2 : Color) : Prop :=
  (c2.val = (c1.val + 1) % 7) ∨ (c2.val = (c1.val + 6) % 7)

/-- Decidable instance for adjacency (allows computation) -/
instance : DecidablePred (adjacent c1) :=
  fun c2 => Or.decidable

/-- Forward step: c → (c + 1) mod 7 -/
def forward (c : Color) : Color :=
  ⟨(c.val + 1) % 7, by
    have : (c.val + 1) % 7 < 7 := Nat.mod_lt _ (by norm_num)
    exact this⟩

/-- Backward step: c → (c - 1) mod 7 -/
def backward (c : Color) : Color :=
  ⟨(c.val + 6) % 7, by
    have : (c.val + 6) % 7 < 7 := Nat.mod_lt _ (by norm_num)
    exact this⟩

/-- Forward steps are always adjacent -/
theorem forward_adjacent (c : Color) : adjacent c (forward c) := by
  left
  rfl

/-- Backward steps are always adjacent -/
theorem backward_adjacent (c : Color) : adjacent c (backward c) := by
  right
  rfl

/-- No-skipping lemma: if adjacent, then delta is 1 or 6 -/
theorem no_skipping (c1 c2 : Color) :
    adjacent c1 c2 → ((c2.val = (c1.val + 1) % 7) ∨ (c2.val = (c1.val + 6) % 7)) := by
  intro h
  exact h

/-- Self-transitions are not adjacent -/
theorem not_adjacent_self (c : Color) : ¬ adjacent c c := by
  intro h
  cases h with
  | inl h1 =>
    -- Case: c = (c + 1) mod 7
    have : c.val = (c.val + 1) % 7 := h1
    have : c.val < 7 := c.isLt
    omega
  | inr h2 =>
    -- Case: c = (c + 6) mod 7
    have : c.val = (c.val + 6) % 7 := h2
    have : c.val < 7 := c.isLt
    omega

/-- The full cycle returns to start -/
theorem cycle_closure (c : Color) :
    forward (forward (forward (forward (forward (forward (forward c)))))) = c := by
  cases c with | mk val hval =>
  simp [forward]
  omega

/-- Adjacency is symmetric -/
theorem adjacent_symm (c1 c2 : Color) : adjacent c1 c2 → adjacent c2 c1 := by
  intro h
  cases h with
  | inl h1 =>
    -- Case: c2 = (c1 + 1) mod 7, need to show c1 = (c2 + 6) mod 7
    right
    simp [h1]
    omega
  | inr h2 =>
    -- Case: c2 = (c1 + 6) mod 7, need to show c1 = (c2 + 1) mod 7
    left
    simp [h2]
    omega

/-- Gray event: a transition that is not adjacent -/
def is_gray_event (c1 c2 : Color) : Prop := ¬ adjacent c1 c2

/-- Result type: either Ok or Gray error -/
inductive Result (α : Type _) where
  | ok : α → Result α
  | gray : Color → Color → Result α

/-- Validate a single transition -/
def validate_transition (c1 c2 : Color) : Result Color :=
  if adjacent c1 c2 then
    Result.ok c2
  else
    Result.gray c1 c2

end SevenMagicks
