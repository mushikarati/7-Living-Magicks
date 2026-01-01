# GLOSSARY - Seven Living Magicks Terminology

Canonical definitions for terms used throughout the Codex project.

---

## Core Concepts

### Adjacency Law
The fundamental rule governing transitions between colors: **±1 mod 7**. All legal transitions must move exactly one step forward or backward in the cycle.

**Example:** Black (0) → White (1) is legal (forward). White (1) → Yellow (2) → Brown (3) is legal (two forward steps). Black (0) → Yellow (2) is **illegal** (skipped White).

### Canon / Canon Law
The immutable set of rules defining the 7-color sequence, adjacency requirements, and meta tokens. Defined in `canon/canon.json` and documented in `docs/CANON.md`.

### Codex
The complete system of Seven Living Magicks, including:
1. The 7-color symbolic framework
2. The adjacency law
3. Compression/entropy engine
4. Archive of canonical texts
5. Formal proofs (Lean)

### Color Sequence
The ordered cycle of seven symbolic operators:
```
⚫ Black → ⚪ White → 🟡 Yellow → 🟤 Brown → 🔴 Red → 🟢 Green → 🔵 Blue → (wraps to Black)
```

### Delta
The computed difference between two color indices in a transition: `delta = (to - from) mod 7`. Legal deltas are **1** (forward) or **6** (backward, equivalent to -1 mod 7).

---

## Colors and Operators

### ⚫ Black (0) - The Eraser
**Meaning:** Entropy, sacred endings, dissolution, the void that makes space for new beginnings.

**Symbolic role:** Termination, release, sacred destruction, clearing.

### ⚪ White (1) - The Envelope
**Meaning:** Thread of structure, containment, the boundary that defines form.

**Symbolic role:** Structure, containment, form, definition, scaffolding.

### 🟡 Yellow (2) - The Spark
**Meaning:** Ignition and will, the initial impulse, creative fire.

**Symbolic role:** Initiation, will, ignition, creative impulse.

### 🟤 Brown (3) - The Womb
**Meaning:** Earth's vessel, gestation, the ground that holds and nourishes.

**Symbolic role:** Grounding, vessel, holding space, earth connection.

### 🔴 Red (4) - The Pulse
**Meaning:** Heart of sacrifice, lifeblood, vital force, the beating center.

**Symbolic role:** Sacrifice, vitality, lifeforce, circulation.

### 🟢 Green (5) - The Vine
**Meaning:** Breath and symbiosis, connection, growth, the living network.

**Symbolic role:** Connection, symbiosis, breath, living systems.

### 🔵 Blue (6) - The Mirror
**Meaning:** Return and reflection, closure, the loop that brings wholeness.

**Symbolic role:** Reflection, return, closure, completion.

---

## Meta Tokens

### Violet (⚿)
**Status:** Meta/void channel, outside the 7-color cycle.

**Usage:** Represents operations at the meta-level, the void, or processes that exist outside the standard cycle. Not subject to adjacency law.

### Gray (🪩)
**Status:** Error token, violation marker.

**Meaning:** Illegal jump, degenerate loop, or entropy plateau.

**Trigger conditions:**
1. Adjacency violation (delta ∉ {1, 6})
2. Degeneracy detected (compression flatlines)
3. Unknown token encountered

**See also:** `GrayEvent`, `gray_event_schema.json`

---

## Events and Violations

### Gray Event
A standardized event object representing canon violations or degeneracy. Includes:
- Type (adjacency_violation, degeneracy_detected, unknown_token, etc.)
- Index (where in sequence)
- Reason (human-readable explanation)
- Optional: delta, entropy metrics, context

**Schema:** `canon/gray_event_schema.json`

**Class:** `GrayEvent` (Python), exported from `canon.gray_event`

### Illegal Jump
A transition that violates the adjacency law by skipping colors.

**Example:** Black → Yellow (skipped White, delta = 2)

### Adjacency Violation
Synonym for **illegal jump**. Triggers a Gray event.

---

## Compression and Entropy

### MDL (Minimum Description Length)
A measure of information content based on compression. Lower MDL indicates higher compressibility (less information).

**Usage:** Used to detect mimic loops and degeneracy.

### NCD (Normalized Compression Distance)
A similarity metric based on compression:
```
NCD(x, y) = [C(xy) - min(C(x), C(y))] / max(C(x), C(y))
```
Where `C(x)` is the compressed size of `x`.

**Range:** 0 (identical) to 1 (completely different)

**Usage:** Measuring semantic similarity and detecting degeneracy.

### Mimic Loop
A sequence with high repetition and low meaningful change. The sequence appears to be "going through the motions" without genuine transformation.

**Detection:** Compression ratio flatlines, entropy estimate drops below threshold.

**Example:** `[0,1,2,3,4,5,6, 0,1,2,3,4,5,6, 0,1,2,3,4,5,6, ...]` (repeating full cycle with no variation)

### Degeneracy
A state where the sequence has lost meaningful variation and is mechanically repeating patterns without genuine semantic content.

**Indicators:**
- Compression ratio > threshold (e.g., 0.9)
- Entropy estimate < threshold (e.g., 0.2)
- NCD between consecutive windows approaches 1.0

**Action:** Trigger Gray event (type: `degeneracy_detected`)

### Entropy Plateau
When entropy measurements flatline, indicating the sequence has lost informational richness.

**Related:** Mimic loop, degeneracy

---

## Recursive and Symbolic Concepts

### Recursive Flow
A sequence that returns to itself in a meaningful way, forming closed loops that preserve or transform information.

**Contrast:** Mimic loop (degenerate recursion without transformation)

### Clarified Loop
A cycle that achieves closure with genuine transformation, as opposed to mechanical repetition.

### Symbolic Closure
When Blue (The Mirror) returns the cycle to Black, completing the seven-fold transformation.

### Living Code
Symbolic sequences that carry active semantic content, not just syntactic patterns. The symbols are "alive" with meaning and transformation potential.

---

## Calendar System

### 364/13 Calendar
A calendar structure based on:
- **364 days** = 7 × 52 = 13 × 28
- **13 months** of 28 days each
- **28-day lunar cycle**
- **Perfect alignment with 7-day weeks**

**Properties:**
- Every month starts on the same day of the week
- 52 complete weeks per year
- No irregular months (unlike Gregorian calendar)

**Codex relevance:** Aligns with the 7-color cycle structure.

---

## Archive and Parsing

### Corpus
The collection of archived documents, texts, and data that constitute the Codex knowledge base.

**Location:** `/corpus/`

### Manifest
A JSON index file listing all files in the corpus with metadata:
- File hash
- Size
- Type
- Topic tags
- Extracted headings
- Canon receipts

**Generated by:** `manifest_generator.py`

### Canon Receipts
Extracted references to canon law found in corpus documents. Includes:
- Explicit color order statements
- Adjacency mentions
- Definitions of Gray/Violet
- Source file and location

**Output:** `docs/canon_receipts.md`

---

## Formal Verification

### Lean 4
A proof assistant and functional programming language used for formal verification of canon laws.

**Usage:** Proving properties like the no-skipping lemma, cycle closure, etc.

**Location:** `/lean/`

### Color : Fin 7
The Lean type definition for colors as finite set {0, 1, 2, 3, 4, 5, 6}.

### Adjacent : Color → Color → Prop
The Lean predicate defining the adjacency relation.

### No-Skipping Lemma
A proven theorem that all legal steps have `delta ∈ {+1, -1} mod 7`.

---

## Tools and CLI

### `codex check`
CLI command for validating token sequences against canon law.

**Usage:**
```bash
codex check <file>
codex check --stdin
codex check --json  # JSON output
```

**Output:** PASS/FAIL verdict, Gray events, summary statistics

---

## Development Terms

### Single Source of Truth
The principle that canon definitions exist in **one place only**: `canon/canon.json`. All modules import from this file; no duplication allowed.

### Property Tests
Automated tests that verify properties hold for random inputs.

**Example:** "Any random walk respecting adjacency must have all deltas in {1, 6}"

### Golden Corpus
A curated set of test sequences used for regression testing:
- Lawful sequences (should pass)
- Known illegal jumps (should fail with specific Gray events)
- Mimic loops (should trigger degeneracy detection)

**Location:** `/tests/corpus/`

---

## Miscellaneous

### Dew
*(From corpus doctrine)* A term referencing the condensation of meaning from the void, the moisture that enables growth. Related to the generative potential of the cycle.

**Note:** Appears in archive texts; exact usage context-dependent.

### Spore
*(From corpus)* A seed of symbolic potential, dormant patterns that can activate when conditions align.

**Note:** Metaphorical; used in narrative contexts.

---

## Anti-Patterns (What NOT to Do)

### Hallucinating Canon
Making up colors, rules, or sequences not defined in `canon/canon.json`.

**Example:** Adding "Purple" or "Orange" to the sequence.

**Action:** Read `CANON.md`, check the source of truth.

### Hardcoding
Copying the color sequence into multiple files instead of importing from canon.

**Solution:** Always `from canon.canon import COLORS`

### Skipping Validation
Processing transitions without calling `is_adjacent()` or `validate_sequence()`.

**Solution:** Always validate before processing.

---

## References

- **Canon Law:** `docs/CANON.md`
- **Source of Truth:** `canon/canon.json`
- **Gray Event Schema:** `canon/gray_event_schema.json`
- **Contributing Guide:** `CONTRIBUTING.md`

---

**Last Updated:** 2025-01-01
**Canon Version:** 1.0.0

For questions or clarifications, open a discussion issue with the `docs` label.
