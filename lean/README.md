# Lean 4 Formalization of Canon Law

This directory contains formal proofs of the Seven Living Magicks canon law using Lean 4.

## Files

- **`Canon.lean`**: Core definitions and theorems
  - `Color : Fin 7` - The seven colors as a finite type
  - `adjacent` - The adjacency relation (±1 mod 7)
  - `forward`, `backward` - Transition operators
  - `no_skipping` - Proof that legal deltas are exactly {1, 6}
  - `cycle_closure` - Proof that 7 forward steps return to start
  - `Result` type - Typed Gray errors

- **`lakefile.lean`**: Lake build configuration

## Building

Install Lean 4 and Lake:
```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
```

Build the project:
```bash
cd lean
lake build
```

## Theorems Proven

### ✓ `forward_adjacent`
Forward steps are always adjacent: `adjacent c (forward c)`

### ✓ `backward_adjacent`
Backward steps are always adjacent: `adjacent c (backward c)`

### ✓ `no_skipping`
If two colors are adjacent, their delta is exactly 1 or 6 mod 7.

### ✓ `not_adjacent_self`
Self-transitions are not adjacent: `¬ adjacent c c`

### ✓ `cycle_closure`
Seven forward steps return to the starting color.

### ✓ `adjacent_symm`
Adjacency is symmetric: if c1 is adjacent to c2, then c2 is adjacent to c1.

## Usage

Import the formalization:
```lean
import Canon

open SevenMagicks

#check adjacent
#check forward_adjacent
#check cycle_closure
```

## Future Work

- [ ] Prove uniqueness of forward/backward operators
- [ ] Formalize entropy metrics and degeneracy conditions
- [ ] Prove properties about sequence validation
- [ ] Define homomorphisms between color sequences
- [ ] Formalize the 364/13 calendar structure

## References

- [Lean 4 Manual](https://leanprover.github.io/lean4/doc/)
- [Mathlib4 Docs](https://leanprover-community.github.io/mathlib4_docs/)
- Canon source: `../canon/canon.json`
- Canon docs: `../docs/CANON.md`
