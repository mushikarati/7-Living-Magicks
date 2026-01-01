"""
Unit tests for canon module.
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from canon.canon import (
    COLORS,
    COLOR_COUNT,
    MODULUS,
    VALID_DELTAS,
    is_adjacent,
    validate_sequence,
    get_color_by_index,
    get_color_by_name,
    get_color_by_symbol,
    Color
)
from canon.gray_event import GrayEvent, EntropyMetrics, create_gray_events_from_violations


class TestCanonConstants:
    """Test canon constants and invariants."""

    def test_color_count(self):
        assert COLOR_COUNT == 7
        assert len(COLORS) == 7

    def test_modulus(self):
        assert MODULUS == 7

    def test_valid_deltas(self):
        assert VALID_DELTAS == [1, -1, 6]

    def test_color_sequence_order(self):
        expected_names = ["Black", "White", "Yellow", "Brown", "Red", "Green", "Blue"]
        actual_names = [c["name"] for c in COLORS]
        assert actual_names == expected_names

    def test_color_indices(self):
        for i, color in enumerate(COLORS):
            assert color["index"] == i


class TestAdjacency:
    """Test adjacency validation."""

    def test_forward_transitions(self):
        """Test all forward transitions are valid."""
        for i in range(7):
            next_i = (i + 1) % 7
            assert is_adjacent(i, next_i), f"Forward {i} → {next_i} should be valid"

    def test_backward_transitions(self):
        """Test all backward transitions are valid."""
        for i in range(7):
            prev_i = (i - 1) % 7
            assert is_adjacent(i, prev_i), f"Backward {i} → {prev_i} should be valid"

    def test_wrap_around(self):
        """Test wrap-around transitions."""
        assert is_adjacent(6, 0)  # Blue → Black
        assert is_adjacent(0, 6)  # Black → Blue

    def test_illegal_jumps(self):
        """Test illegal jumps are detected."""
        assert not is_adjacent(0, 2)  # Skip 1
        assert not is_adjacent(0, 3)  # Skip 1, 2
        assert not is_adjacent(0, 4)  # Skip 1, 2, 3
        assert not is_adjacent(0, 5)  # Skip 1, 2, 3, 4

    def test_self_transition(self):
        """Test self-transitions are illegal."""
        for i in range(7):
            assert not is_adjacent(i, i)


class TestSequenceValidation:
    """Test sequence validation."""

    def test_empty_sequence(self):
        """Empty sequence should be valid (no transitions to check)."""
        is_valid, violations = validate_sequence([])
        assert is_valid
        assert len(violations) == 0

    def test_single_element(self):
        """Single element should be valid (no transitions)."""
        is_valid, violations = validate_sequence([0])
        assert is_valid
        assert len(violations) == 0

    def test_valid_forward_sequence(self):
        """Full forward cycle should be valid."""
        sequence = [0, 1, 2, 3, 4, 5, 6]
        is_valid, violations = validate_sequence(sequence)
        assert is_valid
        assert len(violations) == 0

    def test_valid_backward_sequence(self):
        """Backward sequence should be valid."""
        sequence = [6, 5, 4, 3, 2, 1, 0]
        is_valid, violations = validate_sequence(sequence)
        assert is_valid
        assert len(violations) == 0

    def test_valid_mixed_sequence(self):
        """Mixed forward/backward should be valid."""
        sequence = [0, 1, 0, 6, 0, 1, 2, 1]
        is_valid, violations = validate_sequence(sequence)
        assert is_valid
        assert len(violations) == 0

    def test_simple_illegal_jump(self):
        """Simple illegal jump should be detected."""
        sequence = [0, 2]  # Skip 1
        is_valid, violations = validate_sequence(sequence)
        assert not is_valid
        assert len(violations) == 1
        assert violations[0]["from"] == 0
        assert violations[0]["to"] == 2
        assert violations[0]["delta"] == 2

    def test_multiple_violations(self):
        """Multiple violations should all be detected."""
        sequence = [0, 2, 5]  # Two illegal jumps
        is_valid, violations = validate_sequence(sequence)
        assert not is_valid
        assert len(violations) == 2


class TestColorLookup:
    """Test color lookup functions."""

    def test_get_by_index(self):
        color = get_color_by_index(0)
        assert color["name"] == "Black"

    def test_get_by_name(self):
        color = get_color_by_name("Black")
        assert color["index"] == 0

    def test_get_by_name_case_insensitive(self):
        assert get_color_by_name("black")["index"] == 0
        assert get_color_by_name("BLACK")["index"] == 0

    def test_get_by_symbol(self):
        color = get_color_by_symbol("⚫")
        assert color["name"] == "Black"

    def test_get_by_name_invalid(self):
        with pytest.raises(ValueError):
            get_color_by_name("InvalidColor")

    def test_get_by_symbol_invalid(self):
        with pytest.raises(ValueError):
            get_color_by_symbol("❓")


class TestGrayEvents:
    """Test Gray event creation."""

    def test_adjacency_violation_creation(self):
        event = GrayEvent.adjacency_violation(index=0, from_color=0, to_color=2)
        assert event.type == "adjacency_violation"
        assert event.from_color == 0
        assert event.to_color == 2
        assert event.delta == 2
        assert "illegal jump" in event.reason.lower()

    def test_degeneracy_detection_creation(self):
        metrics = EntropyMetrics(compression_ratio=0.95, entropy_estimate=0.1)
        event = GrayEvent.degeneracy_detected(index=10, entropy_metrics=metrics)
        assert event.type == "degeneracy_detected"
        assert event.entropy_metrics.compression_ratio == 0.95

    def test_unknown_token_creation(self):
        event = GrayEvent.unknown_token(index=5, token="🟣")
        assert event.type == "unknown_token"
        assert "🟣" in event.reason

    def test_gray_event_to_dict(self):
        event = GrayEvent.adjacency_violation(index=0, from_color=0, to_color=2)
        data = event.to_dict()
        assert data["type"] == "adjacency_violation"
        assert data["index"] == 0
        assert data["from"] == 0
        assert data["to"] == 2
        assert data["delta"] == 2

    def test_create_from_violations(self):
        violations = [{"index": 0, "from": 0, "to": 2, "delta": 2, "reason": "test"}]
        events = create_gray_events_from_violations(violations)
        assert len(events) == 1
        assert events[0].type == "adjacency_violation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
