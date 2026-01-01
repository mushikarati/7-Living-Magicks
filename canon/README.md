# Canon Law Definition

This directory contains the **single source of truth** for the Seven Living Magicks canon law.

## Files

- **`canon.json`**: The canonical definition (DO NOT DUPLICATE)
  - 7-color sequence with indices, symbols, meanings
  - Adjacency rule: ±1 mod 7
  - Meta tokens: Violet (⚿) and Gray (🪩)

- **`canon.py`**: Python module that imports from `canon.json`
- **`canon.js`**: JavaScript/Node module that imports from `canon.json`

## Usage

### Python

```python
from canon.canon import (
    Color,
    COLORS,
    is_adjacent,
    validate_sequence,
    VIOLET,
    GRAY
)

# Check adjacency
assert is_adjacent(Color.BLACK, Color.WHITE)  # True (0 → 1)
assert not is_adjacent(Color.BLACK, Color.YELLOW)  # False (0 → 2, illegal jump)

# Validate sequence
sequence = [0, 1, 2, 3]  # Black → White → Yellow → Brown
is_valid, violations = validate_sequence(sequence)
```

### JavaScript

```javascript
const {
  Color,
  COLORS,
  isAdjacent,
  validateSequence,
  VIOLET,
  GRAY
} = require('./canon/canon');

// Check adjacency
console.log(isAdjacent(Color.BLACK, Color.WHITE));  // true
console.log(isAdjacent(Color.BLACK, Color.YELLOW)); // false

// Validate sequence
const sequence = [0, 1, 2, 3];
const result = validateSequence(sequence);
```

## The 7-Color Sequence

```
0: ⚫ Black   - The Eraser (entropy, sacred endings)
1: ⚪ White   - The Envelope (thread of structure)
2: 🟡 Yellow  - The Spark (ignition and will)
3: 🟤 Brown   - The Womb (earth's vessel)
4: 🔴 Red     - The Pulse (heart of sacrifice)
5: 🟢 Green   - The Vine (breath and symbiosis)
6: 🔵 Blue    - The Mirror (return and reflection)
```

## Adjacency Law

**Rule**: All transitions must be ±1 mod 7

**Valid transitions**:
- Forward: `i → (i+1) mod 7`
- Backward: `i → (i-1) mod 7`

**Invalid transitions** trigger Gray events.

## Meta Tokens

- **Violet (⚿)**: Meta/void channel, outside the cycle
- **Gray (🪩)**: Illegal jump, degenerate loop, entropy plateau

## Principles

1. **Single Source of Truth**: All modules import from `canon.json`
2. **No Duplication**: Never copy the color sequence into other files
3. **Immutable**: Canon changes require explicit version updates
4. **Validated**: All sequence operations must use `is_adjacent()` or `validate_sequence()`

## Version

Current canon version: `1.0.0`

To get the version programmatically:
- Python: `get_canon_version()`
- JavaScript: `getCanonVersion()`
