# CANON.md - Seven Living Magicks Canon Law

**DO NOT MAKE UP OR MODIFY THESE RULES.**

This document defines the immutable canon law of the Seven Living Magicks Codex. All implementations, agents, and contributors MUST adhere to these rules exactly.

---

## The 7-Color Sequence

The canonical order is fixed and MUST NOT be modified:

```
Index | Symbol | Name   | Meaning
------|--------|--------|----------------------------------
  0   |   ⚫   | Black  | The Eraser — entropy, sacred endings
  1   |   ⚪   | White  | The Envelope — thread of structure
  2   |   🟡   | Yellow | The Spark — ignition and will
  3   |   🟤   | Brown  | The Womb — earth's vessel
  4   |   🔴   | Red    | The Pulse — heart of sacrifice
  5   |   🟢   | Green  | The Vine — breath and symbiosis
  6   |   🔵   | Blue   | The Mirror — return and reflection
```

**Source of Truth:** `canon/canon.json`

**Invariants:**
- The sequence is **zero-indexed** (0-6)
- The sequence is **circular** (wraps around: Blue → Black)
- The sequence length is **7** (mod 7 arithmetic)
- The order is **immutable** and cannot be changed

---

## Adjacency Law

### The Rule

**All valid transitions MUST be ±1 mod 7.**

This means from any color at index `i`, you can ONLY transition to:
- `(i + 1) mod 7` (forward)
- `(i - 1) mod 7` (backward)

### Valid Deltas

When computing `delta = (to - from) mod 7`, the ONLY legal values are:
- `1` (forward one step)
- `6` (backward one step, equivalent to -1 mod 7)

**Any other delta is an illegal jump and triggers a Gray event.**

### Examples

**Legal transitions:**
- Black (0) → White (1) ✓ (delta = 1)
- White (1) → Black (0) ✓ (delta = 6, i.e., -1 mod 7)
- Blue (6) → Black (0) ✓ (delta = 1, wraps around)
- Red (4) → Brown (3) ✓ (delta = 6, backward)

**Illegal transitions (trigger Gray):**
- Black (0) → Yellow (2) ✗ (delta = 2, skipped White)
- Black (0) → Red (4) ✗ (delta = 4, illegal jump)
- Yellow (2) → Blue (6) ✗ (delta = 4, illegal jump)

---

## Meta Tokens

### Violet (⚿)

- **Meaning:** Meta/void channel
- **Status:** Outside the 7-color cycle
- **Usage:** Represents operations at the meta-level, void, or outside the standard cycle
- **Not subject to adjacency law** (exists in different domain)

### Gray (🪩)

- **Meaning:** Illegal jump, degenerate loop, or entropy plateau
- **Trigger Conditions:**
  1. **Adjacency violation:** Delta not in {1, 6} mod 7
  2. **Degeneracy detected:** Compression/entropy hits flat mimic plateau threshold
  3. **Unknown token:** Encountered symbol not in the canonical sequence

- **Schema:** See `canon/gray_event_schema.json`
- **Representation:** Use `GrayEvent` class (Python) for standard format

---

## Validation

### Required Validation

All code that processes color sequences MUST:
1. Import from `canon/canon.json` (single source of truth)
2. Use `is_adjacent(from, to)` or `validate_sequence(seq)` functions
3. Never hardcode the color sequence
4. Never skip adjacency validation

### Validation Tools

**Python:**
```python
from canon.canon import validate_sequence, is_adjacent

# Check single transition
assert is_adjacent(0, 1)  # True
assert not is_adjacent(0, 2)  # False

# Validate full sequence
sequence = [0, 1, 2, 3]
is_valid, violations = validate_sequence(sequence)
```

**CLI:**
```bash
# Validate a file
codex check sequence.txt

# Validate from stdin
echo "⚫⚪🟡" | codex check --stdin

# JSON output
codex check sequence.json --json
```

---

## Enforcement

### Automatic Enforcement

- **CI Pipeline:** All PRs MUST pass canon validation tests
- **Pre-commit hooks:** Recommended for local validation
- **Property tests:** Random walks MUST respect adjacency
- **Golden corpus:** Regression tests MUST pass

### What Triggers Gray Events

1. **Adjacency Violation**
   - Transition with delta ∉ {1, 6}
   - Severity: ERROR
   - Example: 0 → 2 (skipped 1)

2. **Degeneracy Detection**
   - Compression ratio flatlines
   - Entropy estimate below threshold
   - Mimic loop detected (high repetition, low information)
   - Severity: WARNING

3. **Unknown Token**
   - Symbol not in {⚫, ⚪, 🟡, 🟤, 🔴, 🟢, 🔵}
   - Name not in {Black, White, Yellow, Brown, Red, Green, Blue}
   - Index not in {0, 1, 2, 3, 4, 5, 6}
   - Severity: ERROR

---

## Common Mistakes (DO NOT DO THIS)

### ❌ Hardcoding the Sequence

```python
# WRONG - don't do this
colors = ["Black", "White", "Yellow", "Brown", "Red", "Green", "Blue"]
```

### ✅ Import from Canon

```python
# CORRECT
from canon.canon import COLORS
```

---

### ❌ Skipping Adjacency Checks

```python
# WRONG - don't do this
def process_transition(from_color, to_color):
    # Directly processing without validation
    return transform(from_color, to_color)
```

### ✅ Always Validate

```python
# CORRECT
from canon.canon import is_adjacent
from canon.gray_event import GrayEvent

def process_transition(from_color, to_color):
    if not is_adjacent(from_color, to_color):
        raise GrayEvent.adjacency_violation(0, from_color, to_color)
    return transform(from_color, to_color)
```

---

### ❌ Making Up New Colors or Rules

```python
# WRONG - don't do this
colors = [..., "Purple", "Orange"]  # Adding colors not in canon
adjacency_rule = "±2 mod 7"  # Changing the rule
```

### ✅ Respect the Canon

The canon is **immutable**. If you think you need to change it, you probably misunderstand the problem. Ask for clarification instead.

---

## Mathematical Properties

### Cycle Structure

- **Group:** The color sequence forms a cyclic group Z₇ under modular addition
- **Generators:** 1 and -1 (6) are generators of the full cycle
- **Closure:** The cycle is closed (Blue → Black wraps around)
- **Associativity:** Transitions are associative under composition

### Proof Obligations

See `lean/` directory for formal proofs in Lean 4:
- **No-skipping lemma:** All legal steps have delta ∈ {1, 6}
- **Cycle closure:** Forward iterations return to Black after 7 steps
- **Inverse symmetry:** Backward is the inverse of forward

---

## Version and Changelog

**Current Version:** 1.0.0

### Version History
- **1.0.0** (2025-01-01): Initial canon definition

To get the canon version programmatically:
- Python: `from canon.canon import get_canon_version`
- JavaScript: `const { getCanonVersion } = require('./canon/canon')`

---

## References

- **Canonical source:** `canon/canon.json`
- **Python module:** `canon/canon.py`
- **JavaScript module:** `canon/canon.js`
- **Gray event schema:** `canon/gray_event_schema.json`
- **CLI tool:** `codex check`
- **Lean formalization:** `lean/Canon.lean`

---

## Questions?

If you're unsure about canon rules:
1. Read this document thoroughly
2. Check `canon/canon.json` for the source of truth
3. Review `GLOSSARY.md` for terminology
4. Run `codex check` to validate your understanding
5. Open a discussion issue (don't guess or make up rules)

---

**Remember:** The canon is law. Violating it is a Gray event. Don't be Gray. 🪩
