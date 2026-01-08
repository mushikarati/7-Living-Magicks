# Research Crosswalks

This directory contains comparisons and mappings between the Seven Living Magicks Codex and external symbolic systems.

**IMPORTANT:** Research content is **speculative** and **non-canonical**. These mappings are for comparative analysis only and do not modify the canon law.

---

## Purpose

External system comparisons help:
1. Contextualize the Codex within existing symbolic frameworks
2. Identify structural similarities and differences
3. Document historical/theoretical connections
4. Keep research separate from canonical implementation

---

## Files

### `crowley_comparison.md`
Mapping between Crowley's Thelemic system and the 7-color Codex.

### `enochian_analysis.md`
Comparison with Enochian magical systems and calls.

### `kabbalah_parallels.md`
Structural parallels with Kabbalistic Tree of Life and Sephirot.

### `tarot_mapping.md`
Correspondences between Tarot systems and color operators.

### `calendar_systems.md`
Analysis of 364/13 calendar in relation to other sacred calendar systems.

---

## Guidelines

### For Contributors

When adding research content:

1. **Clearly mark speculation** - Distinguish canonical facts from comparative analysis
2. **Cite sources** - Include references for external system claims
3. **No canon modification** - Research does NOT change `canon/canon.json`
4. **Use issue template** - File research notes using the "Research Note" issue template
5. **Separate files** - Keep each external system in its own file

### For Agents

**DO NOT:**
- Use research files to infer canon law
- Mix research speculation with canonical implementation
- Import research claims into production code
- Treat comparative mappings as authoritative

**DO:**
- Keep research isolated in `docs/research/`
- Reference `docs/CANON.md` for authoritative rules
- Mark all research content as non-canonical
- Use research for context only, not for validation

---

## Research vs Canon

| Aspect | Canon | Research |
|--------|-------|----------|
| **Source** | `canon/canon.json`, `docs/CANON.md` | `docs/research/*` |
| **Status** | Immutable, authoritative | Speculative, comparative |
| **Usage** | Import into code, enforce in CI | Context, analysis, discussion |
| **Modification** | Requires version bump | Open to iteration |
| **Validation** | Enforced by tests | No enforcement |

---

## Example: Crowley Comparison

**Canonical fact:**
- The Codex has 7 colors in a fixed order: ⚫→⚪→🟡→🟤→🔴→🟢→🔵

**Research note:**
- Crowley's system has 7 classical planets with symbolic correspondences
- Potential mapping: Saturn (⚫), Moon (⚪), Mercury (🟡), Venus (🟤), Mars (🔴), Jupiter (🟢), Sol (🔵)
- **This mapping is speculative and NOT canonical**

---

## Contributing Research

1. Use the "Research Note" issue template
2. Document findings in a new file in `docs/research/`
3. Submit PR with research content only (no code changes)
4. Reviewers assess accuracy of citations, not truth of claims
5. Merge when properly formatted and sourced

---

## Open Research Questions

- How does the 7-color cycle relate to other 7-fold systems (chakras, days of week, musical scales)?
- What are the compression theory foundations for degeneracy detection?
- How do other symbolic systems handle "illegal jumps" or "Gray events"?
- What is the relationship between 364/13 calendar and lunar/solar cycles?

**File research questions as issues with the `docs` label.**

---

**Remember:** Canon is law. Research is context. Keep them separate.
