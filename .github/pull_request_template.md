# Pull Request: [Brief Description]

## Summary

<!-- Provide a concise summary of the changes -->

## Canon Impact Assessment

### Does this PR affect the 7-color sequence or adjacency rules?

- [ ] Yes - Details below
- [ ] No - Only implementation/tooling changes

**If yes, describe the impact:**

<!-- Explain how the canon is affected -->

### Adjacency Respected?

- [ ] All transitions verified to be ±1 mod 7
- [ ] No new illegal jumps introduced
- [ ] Tested with adjacency validator
- [ ] N/A - No sequence operations in this PR

**Validation method:**

<!-- How did you verify adjacency? (e.g., ran `codex check`, unit tests, manual review) -->

### Gray Conditions

- [ ] Gray events properly detected
- [ ] Gray events properly reported in standard schema
- [ ] Added tests for Gray conditions
- [ ] N/A - No Gray detection logic in this PR

**Gray handling:**

<!-- Describe how Gray events are detected/reported, if applicable -->

## Test Evidence

- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Property tests updated (if adjacency logic changed)
- [ ] Golden corpus tests pass (if parser/compression changed)
- [ ] Manual testing completed

**Test results summary:**

```
<!-- Paste test output or link to CI run -->
```

## Documentation

- [ ] CANON.md updated (if canon rules changed)
- [ ] GLOSSARY.md updated (if new terms introduced)
- [ ] Code comments added for non-obvious logic
- [ ] Research crosswalk updated (if external system mappings changed)
- [ ] No docs changes needed

## Type of Change

- [ ] Bug fix (canon violation, incorrect behavior)
- [ ] New feature (parser, compression, tooling)
- [ ] Refactor (no behavior change)
- [ ] Documentation update
- [ ] CI/infrastructure change
- [ ] Lean formalization/proof

## Checklist

- [ ] Code follows project style
- [ ] Self-review completed
- [ ] No secrets or sensitive data committed
- [ ] Branch is up-to-date with target branch
- [ ] Commit messages are clear and descriptive

## Additional Context

<!-- Any additional information, design decisions, tradeoffs, or blockers -->

## Related Issues

<!-- Link related issues: Closes #123, Relates to #456 -->

---

**Reviewer Focus Areas:**

<!-- Highlight specific areas where you want careful review -->
