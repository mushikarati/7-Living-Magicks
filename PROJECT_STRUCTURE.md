# Project Structure - Seven Living Magicks Codex

This document describes the complete project scaffolding and organization.

## Directory Layout

```
7-Living-Magicks/
├── .github/                      # GitHub configuration
│   ├── ISSUE_TEMPLATE/           # Issue templates
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   ├── research_note.yml
│   │   └── archive_ingest.yml
│   ├── workflows/                # CI/CD pipelines
│   │   └── canon-validation.yml
│   ├── pull_request_template.md
│   ├── CODEOWNERS
│   └── labels.yml                # Label definitions
│
├── canon/                        # Canon law single source of truth
│   ├── canon.json               # ⭐ Canonical definition (immutable)
│   ├── canon.py                 # Python module
│   ├── canon.js                 # JavaScript module
│   ├── gray_event_schema.json   # Gray event JSON schema
│   ├── gray_event.py            # GrayEvent class
│   └── README.md
│
├── docs/                         # Documentation
│   ├── CANON.md                 # ⭐ Canon law reference (authoritative)
│   ├── GLOSSARY.md              # Term definitions
│   └── research/                # Non-canonical research
│       ├── README.md
│       └── crowley_comparison.md
│
├── src/                          # Source code modules
│   ├── cli/                      # Command-line tools
│   │   └── codex_check.py
│   ├── compression/              # Compression & entropy metrics
│   │   └── metrics.py
│   ├── engine/                   # Symbolic recursion engine
│   │   └── trace.py
│   └── parsers/                  # Archive ingestion
│       └── manifest_generator.py
│
├── lean/                         # Lean 4 formal proofs
│   ├── Canon.lean
│   ├── lakefile.lean
│   └── README.md
│
├── tests/                        # Test suite
│   ├── test_canon.py            # Unit tests
│   ├── test_properties.py       # Property-based tests
│   ├── test_sequences/          # Test data
│   │   ├── valid_forward.txt
│   │   ├── invalid_jump.txt
│   │   └── valid_sequence.json
│   └── corpus/                   # Golden test corpus (TODO)
│
├── api/                          # Vercel API (existing)
├── codex7-verification-api/      # Stripe integration (existing)
├── codex                         # Main CLI entry point
├── CONTRIBUTING.md               # Contribution guide
├── PROJECT_STRUCTURE.md          # This file
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview

```

## Key Files

### Single Source of Truth

**`canon/canon.json`** - The ONLY place where canon law is defined:
- 7-color sequence with indices, symbols, meanings
- Adjacency rule: ±1 mod 7
- Meta tokens: Violet (⚿) and Gray (🪩)

**All code must import from this file. No duplication allowed.**

### Documentation Hierarchy

1. **`docs/CANON.md`** - Authoritative canon law reference
2. **`docs/GLOSSARY.md`** - Term definitions
3. **`CONTRIBUTING.md`** - Contribution guidelines
4. **`docs/research/`** - Non-canonical research (speculative)

### CLI Tools

**`codex`** - Main CLI entry point
- `codex check <file>` - Validate sequences
- `codex --version` - Show version
- `codex --help` - Show help

**`src/cli/codex_check.py`** - Canon validation tool

### Tests

**Unit tests:** `tests/test_canon.py`
**Property tests:** `tests/test_properties.py` (using Hypothesis)
**Test data:** `tests/test_sequences/`

### CI Pipeline

**`.github/workflows/canon-validation.yml`**
- Validates canon.json schema
- Tests adjacency validator
- Runs unit and property tests
- Checks code quality
- Verifies documentation

## Module Dependencies

```
canon/ (no dependencies - pure canonical data)
  ↓
src/cli/ (depends on canon/)
src/compression/ (standalone)
src/engine/ (depends on canon/)
src/parsers/ (standalone)
  ↓
tests/ (depends on all modules)
```

## Development Workflow

1. **Check canon:** Read `docs/CANON.md`
2. **Import canon:** `from canon.canon import ...`
3. **Write code:** Implement features in `src/`
4. **Test:** Add tests to `tests/`
5. **Validate:** Run `codex check` and `pytest`
6. **Document:** Update docs if needed
7. **Submit PR:** Use template, ensure CI passes

## Agent Assignments (Reference)

From the original spec:

- **Agent A (Core Law):** canon/, CLI, Gray events ✅ DONE
- **Agent B (Compression):** metrics.py, degeneracy detector (stub created)
- **Agent C (Archive):** manifest_generator.py, zip walker (stub created)
- **Agent D (Lean):** lean/Canon.lean ✅ DONE
- **Agent E (Docs/UX):** docs/, templates, research ✅ DONE

## Implementation Status

### ✅ Completed (Scaffolding Ready)

- [x] EPIC 1: Project scaffolding (labels, templates, CODEOWNERS)
- [x] EPIC 2: Canon Law (single source of truth, validators, CLI)
- [x] EPIC 7: Documentation (CANON.md, GLOSSARY.md, research)
- [x] EPIC 8: CI (GitHub Actions, property tests)
- [x] EPIC 5: Lean (formalization, proofs)

### 🚧 Stubbed (Ready for Implementation)

- [ ] EPIC 3: Compression (metrics.py - basic stub)
- [ ] EPIC 4: Archive (manifest_generator.py - basic stub)
- [ ] EPIC 6: Engine (trace.py - basic implementation)

### 📋 TODO (Future Work)

- [ ] EPIC 3: Gray-by-degeneracy detector (compression thresholds)
- [ ] EPIC 3: Golden test corpus (curated test sequences)
- [ ] EPIC 4: Zip walker (recursive archive extraction)
- [ ] EPIC 4: Canon receipts extractor (doc analysis)
- [ ] EPIC 6: Mirror/Return operator (Blue closure mechanics)
- [ ] EPIC 6: 364/13 calendar module

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run property tests only
pytest tests/test_properties.py -v

# Run specific test
pytest tests/test_canon.py::TestAdjacency -v

# Check a sequence
./codex check tests/test_sequences/valid_forward.txt

# Validate with JSON output
./codex check sequence.json --json
```

## Building Lean Proofs

```bash
cd lean
lake build
```

## Code Quality

```bash
# Format code
black canon/ src/ tests/

# Lint
flake8 canon/ src/ tests/ --max-line-length=100
```

## Next Steps

1. Implement compression degeneracy detection
2. Build golden test corpus with known edge cases
3. Implement zip walker for archive ingestion
4. Add canon receipts extractor
5. Implement Blue closure mechanics
6. Build 364/13 calendar generator
7. Extend Lean proofs (uniqueness, homomorphisms)

---

**Last Updated:** 2025-01-01
**Scaffolding Version:** 1.0.0
**Canon Version:** 1.0.0
