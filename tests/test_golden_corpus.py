"""
Golden Corpus Test Suite

Validates all test sequences in the corpus against their expected behavior.
"""

import json
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from canon.canon import validate_sequence
from src.compression.metrics import detect_degeneracy


CORPUS_ROOT = Path(__file__).parent / "corpus"


def load_test_case(test_file: Path):
    """
    Load a test case and its metadata.

    Returns:
        (sequence, metadata)
    """
    with open(test_file, 'r') as f:
        sequence = json.load(f)

    meta_file = test_file.with_suffix('.meta.json')
    if meta_file.exists():
        with open(meta_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}

    return sequence, metadata


def discover_tests(category: str):
    """
    Discover all test files in a category.

    Args:
        category: Category name (lawful, illegal, degenerate, edge_cases)

    Returns:
        List of test file paths
    """
    category_dir = CORPUS_ROOT / category
    if not category_dir.exists():
        return []

    # Filter out .meta.json files
    all_json = list(category_dir.glob("*.json"))
    return sorted([f for f in all_json if not f.stem.endswith('.meta')])


class TestLawfulSequences:
    """Test all lawful sequences pass validation."""

    @pytest.mark.parametrize("test_file", discover_tests("lawful"))
    def test_lawful_sequence(self, test_file):
        """Lawful sequences should pass adjacency validation."""
        sequence, metadata = load_test_case(test_file)

        is_valid, violations = validate_sequence(sequence)

        assert is_valid, \
            f"{test_file.name} should be valid but got violations: {violations}"
        assert len(violations) == 0, \
            f"{test_file.name} should have 0 violations, got {len(violations)}"

        # Check metadata expectations
        if metadata.get("expected_result") == "pass":
            assert is_valid
        if "expected_gray_events" in metadata:
            assert len(violations) == metadata["expected_gray_events"]


class TestIllegalSequences:
    """Test all illegal sequences fail validation."""

    @pytest.mark.parametrize("test_file", discover_tests("illegal"))
    def test_illegal_sequence(self, test_file):
        """Illegal sequences should fail adjacency validation."""
        sequence, metadata = load_test_case(test_file)

        is_valid, violations = validate_sequence(sequence)

        assert not is_valid, \
            f"{test_file.name} should be invalid (illegal jump)"
        assert len(violations) > 0, \
            f"{test_file.name} should have violations"

        # Check metadata expectations
        if metadata.get("expected_result") == "fail":
            assert not is_valid
        if "expected_gray_events" in metadata:
            expected = metadata["expected_gray_events"]
            actual = len(violations)
            assert actual == expected, \
                f"{test_file.name}: expected {expected} violations, got {actual}"

        # Validate violation structure
        for v in violations:
            assert "type" in v
            assert "from" in v
            assert "to" in v
            assert "delta" in v


class TestDegenerateSequences:
    """Test degenerate sequences are detected."""

    @pytest.mark.parametrize("test_file", discover_tests("degenerate"))
    def test_degenerate_sequence(self, test_file):
        """Degenerate sequences should be detected by compression analysis."""
        sequence, metadata = load_test_case(test_file)

        metrics = detect_degeneracy(sequence, window_size=20)

        # Check degeneracy detection if metadata specifies
        if metadata.get("expected_degeneracy") is True:
            assert metrics.is_degenerate, \
                f"{test_file.name} should be degenerate. " \
                f"Compression: {metrics.compression_ratio:.3f}, " \
                f"Entropy: {metrics.entropy_estimate:.3f}, " \
                f"Plateau: {metrics.plateau_detected}"

        # If metadata says should pass adjacency, verify
        if metadata.get("expected_result") == "pass":
            is_valid, _ = validate_sequence(sequence)
            assert is_valid, \
                f"{test_file.name} should pass adjacency (even if degenerate)"


class TestEdgeCases:
    """Test edge cases behave correctly."""

    @pytest.mark.parametrize("test_file", discover_tests("edge_cases"))
    def test_edge_case(self, test_file):
        """Edge cases should match expected behavior."""
        sequence, metadata = load_test_case(test_file)

        is_valid, violations = validate_sequence(sequence)

        # Check against metadata expectations
        expected_result = metadata.get("expected_result")
        if expected_result == "pass":
            assert is_valid, \
                f"{test_file.name} should pass but got violations: {violations}"
        elif expected_result == "fail":
            assert not is_valid, \
                f"{test_file.name} should fail but passed"

        if "expected_gray_events" in metadata:
            expected = metadata["expected_gray_events"]
            actual = len(violations)
            assert actual == expected, \
                f"{test_file.name}: expected {expected} violations, got {actual}"


class TestCorpusMetadata:
    """Test corpus metadata is valid."""

    def test_all_tests_have_metadata(self):
        """All test files should have corresponding metadata."""
        for category in ["lawful", "illegal", "degenerate", "edge_cases"]:
            test_files = discover_tests(category)
            for test_file in test_files:
                meta_file = test_file.with_suffix('.meta.json')
                assert meta_file.exists(), \
                    f"Missing metadata for {test_file}"

    def test_metadata_has_required_fields(self):
        """All metadata files should have required fields."""
        required_fields = ["description", "expected_result", "tags"]

        for category in ["lawful", "illegal", "degenerate", "edge_cases"]:
            test_files = discover_tests(category)
            for test_file in test_files:
                meta_file = test_file.with_suffix('.meta.json')
                if meta_file.exists():
                    with open(meta_file, 'r') as f:
                        metadata = json.load(f)

                    for field in required_fields:
                        assert field in metadata, \
                            f"{test_file.name}: missing field '{field}' in metadata"


class TestCorpusCoverage:
    """Test corpus has good coverage."""

    def test_corpus_not_empty(self):
        """Corpus should have test files."""
        total_tests = sum(
            len(discover_tests(cat))
            for cat in ["lawful", "illegal", "degenerate", "edge_cases"]
        )
        assert total_tests > 0, "Corpus should have at least one test"

    def test_lawful_category_exists(self):
        """Lawful category should have tests."""
        tests = discover_tests("lawful")
        assert len(tests) > 0, "Should have lawful test cases"

    def test_illegal_category_exists(self):
        """Illegal category should have tests."""
        tests = discover_tests("illegal")
        assert len(tests) > 0, "Should have illegal test cases"

    def test_degenerate_category_exists(self):
        """Degenerate category should have tests."""
        tests = discover_tests("degenerate")
        assert len(tests) > 0, "Should have degenerate test cases"

    def test_edge_cases_category_exists(self):
        """Edge cases category should have tests."""
        tests = discover_tests("edge_cases")
        assert len(tests) > 0, "Should have edge case tests"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
