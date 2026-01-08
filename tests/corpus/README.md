# Golden Test Corpus

This directory contains curated test sequences for validating canon law and degeneracy detection.

## Purpose

The golden corpus provides:
1. **Regression testing** - Ensure new changes don't break existing behavior
2. **Edge case coverage** - Test boundary conditions
3. **Degeneracy examples** - Curated mimic loops and illegal patterns
4. **Documentation** - Living examples of what should/shouldn't pass

## Structure

```
corpus/
├── lawful/          # Sequences that respect adjacency law
├── illegal/         # Sequences with adjacency violations
├── degenerate/      # Sequences with mimic loops or low entropy
└── edge_cases/      # Boundary conditions (empty, single, wrap-around)
```

## File Format

Each test file is either:
- **JSON**: Array of color indices `[0, 1, 2, ...]`
- **Text**: Symbols or names (one per line or continuous)

## Metadata

Each test file has an accompanying `.meta.json` file describing:
- `description`: What this test validates
- `expected_result`: "pass" or "fail"
- `expected_gray_events`: Number of Gray events (for illegal sequences)
- `expected_degeneracy`: true/false (for degeneracy tests)
- `tags`: Categories (e.g., "wrap-around", "mimic-loop", "single-jump")

## Running Tests

```bash
# Validate all lawful sequences
for f in tests/corpus/lawful/*.json; do
    ./codex check "$f" || echo "FAIL: $f"
done

# Validate all illegal sequences (should fail)
for f in tests/corpus/illegal/*.json; do
    ./codex check "$f" && echo "ERROR: $f should have failed"
done

# Run corpus test suite
pytest tests/test_golden_corpus.py -v
```

## Adding New Tests

1. Create test file in appropriate directory
2. Create corresponding `.meta.json` file
3. Run `pytest tests/test_golden_corpus.py` to verify
4. Update this README if adding new categories

## Test Categories

### Lawful Sequences

Valid sequences respecting adjacency law (±1 mod 7):
- Forward full cycle
- Backward full cycle
- Mixed forward/backward
- Multiple cycles
- Random walks with ±1 steps

### Illegal Sequences

Sequences with adjacency violations:
- Single jump (skip 1 color)
- Double jump (skip 2 colors)
- Large jump (skip 3+ colors)
- Multiple violations
- Mixed legal/illegal

### Degenerate Sequences

Sequences with high repetition or low entropy:
- Exact cycle repetition (mimic loop)
- Single color repetition
- Alternating two colors
- Short pattern repetition

### Edge Cases

Boundary conditions:
- Empty sequence
- Single element
- Two elements (legal/illegal)
- Wrap-around (Blue → Black)
- All seven colors once

## Expected Behavior

| Category | codex check Result | Gray Events | Degeneracy |
|----------|-------------------|-------------|------------|
| lawful   | PASS ✓            | 0           | false      |
| illegal  | FAIL ✗            | 1+          | N/A        |
| degenerate | PASS ✓ (adjacency) | 0       | true       |
| edge_cases | varies          | varies      | varies     |

**Note:** Degenerate sequences may pass adjacency checks but fail entropy analysis.

## Maintenance

- Run full corpus tests before each release
- Add new edge cases as discovered
- Update metadata if behavior changes
- Keep corpus small and focused (quality over quantity)

---

Last updated: 2025-01-01
