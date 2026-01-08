# Contributing to 7-Living-Magicks

Thank you for your interest in contributing to the Seven Living Magicks Codex project.

## Core Invariants

Before contributing, understand these non-negotiable canon laws:

### The 7-Color Sequence

The canonical order is:

```
⚫ Black → ⚪ White → 🟡 Yellow → 🟤 Brown → 🔴 Red → 🟢 Green → 🔵 Blue
  (0)       (1)        (2)        (3)       (4)       (5)       (6)
```

### Adjacency Law

**All transitions must respect ±1 mod 7.**

Legal transitions:
- Forward: color[i] → color[(i+1) mod 7]
- Backward: color[i] → color[(i-1) mod 7]

Illegal jumps trigger **Gray events**.

### Meta Tokens

- **Violet (⚿)**: Meta/void channel, outside the cycle
- **Gray (🪩)**: Illegal jump, degenerate loop, or entropy plateau

## Label Taxonomy

### Domain Labels

- **canon-law**: Core adjacency rules, sequence validation, law enforcement
- **parser**: Archive ingestion, token extraction, document parsing
- **compression**: MDL/NCD metrics, entropy analysis, degeneracy detection
- **lean**: Lean 4 formalization, proofs, formal verification
- **cli**: Command-line tools, `codex check`, user-facing tooling
- **docs**: Documentation files (CANON.md, glossary, research pages)
- **tests**: Test infrastructure, golden corpus, property tests
- **ci**: GitHub Actions, automated validation, regression prevention

### Type Labels

- **bug**: Canon violations, incorrect behavior, test failures
- **refactor**: Code restructuring without behavior changes

### Meta Labels

- **good-first-issue**: Suitable for newcomers
- **blocked**: Cannot proceed until dependency resolves
- **gray-event**: Detected canon violation (illegal jump or degeneracy)

## Pull Request Requirements

All PRs must address:

1. **Canon Impact**: Does this change affect the 7-color sequence or adjacency rules?
2. **Adjacency Respected?**: Have you verified no illegal jumps are introduced?
3. **Gray Conditions?**: Are Gray events properly detected and reported?
4. **Test Evidence**: Do tests pass? Are new tests added for new behavior?
5. **Docs Updated?**: Are CANON.md, glossary, or other docs updated if needed?

See `.github/pull_request_template.md` for the full checklist.

## Development Workflow

1. Fork and clone the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes respecting canon law
4. Run tests: `npm test` or `pytest` (depending on module)
5. Ensure no Gray events in CI
6. Submit PR using the template

## Code Areas and CODEOWNERS

Changes to specific areas auto-request reviews:

- `/lean/**`: Lean formalization experts
- `/engine/**`: Core engine maintainers
- `/docs/**`: Documentation reviewers
- `/parsers/**`: Archive/parser specialists

See `.github/CODEOWNERS` for details.

## Questions?

- Check `docs/CANON.md` for canonical law definitions
- Check `docs/GLOSSARY.md` for terminology
- Open a discussion issue with the `docs` label
