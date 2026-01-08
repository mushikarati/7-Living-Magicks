"""
Property-based tests for canon law using Hypothesis.

These tests verify that adjacency law holds for randomly generated sequences.
"""

import pytest
from hypothesis import given, strategies as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from canon.canon import (
    is_adjacent,
    validate_sequence,
    MODULUS,
    VALID_DELTAS,
    Color
)


# Strategies for generating test data
valid_color = st.integers(min_value=0, max_value=6)
color_sequence = st.lists(valid_color, min_size=2, max_size=100)


class TestAdjacencyProperties:
    """Property-based tests for adjacency law."""

    @given(color=valid_color)
    def test_forward_step_always_adjacent(self, color):
        """Property: Forward step (i+1 mod 7) is always legal."""
        next_color = (color + 1) % MODULUS
        assert is_adjacent(color, next_color), \
            f"Forward step {color} → {next_color} should be legal"

    @given(color=valid_color)
    def test_backward_step_always_adjacent(self, color):
        """Property: Backward step (i-1 mod 7) is always legal."""
        prev_color = (color - 1) % MODULUS
        assert is_adjacent(color, prev_color), \
            f"Backward step {color} → {prev_color} should be legal"

    @given(from_color=valid_color, to_color=valid_color)
    def test_delta_validity(self, from_color, to_color):
        """Property: is_adjacent returns True iff delta in VALID_DELTAS."""
        delta = (to_color - from_color) % MODULUS
        expected = delta in VALID_DELTAS
        actual = is_adjacent(from_color, to_color)
        assert actual == expected, \
            f"is_adjacent({from_color}, {to_color}) = {actual}, but delta {delta} in VALID_DELTAS = {expected}"

    @given(color=valid_color)
    def test_self_transition_illegal(self, color):
        """Property: Transition to self (delta=0) is illegal."""
        assert not is_adjacent(color, color), \
            f"Self-transition {color} → {color} should be illegal"

    @given(color=valid_color, skip=st.integers(min_value=2, max_value=5))
    def test_skip_transitions_illegal(self, color, skip):
        """Property: Skipping colors (delta > 1 and delta < 6) is illegal."""
        to_color = (color + skip) % MODULUS
        if skip not in VALID_DELTAS:
            assert not is_adjacent(color, to_color), \
                f"Skip transition {color} → {to_color} (delta={skip}) should be illegal"


class TestSequenceProperties:
    """Property-based tests for sequence validation."""

    def test_all_forward_sequence_valid(self):
        """Property: A full forward cycle is always valid."""
        sequence = list(range(7))  # [0, 1, 2, 3, 4, 5, 6]
        is_valid, violations = validate_sequence(sequence)
        assert is_valid, f"Forward cycle should be valid, got violations: {violations}"
        assert len(violations) == 0

    def test_all_backward_sequence_valid(self):
        """Property: A full backward cycle is always valid."""
        sequence = list(range(6, -1, -1))  # [6, 5, 4, 3, 2, 1, 0]
        is_valid, violations = validate_sequence(sequence)
        assert is_valid, f"Backward cycle should be valid, got violations: {violations}"
        assert len(violations) == 0

    @given(st.integers(min_value=1, max_value=20))
    def test_repeated_forward_cycles_valid(self, repetitions):
        """Property: Repeating forward cycles is valid (though may be degenerate)."""
        cycle = list(range(7))
        sequence = cycle * repetitions
        is_valid, violations = validate_sequence(sequence)
        assert is_valid, f"Repeated forward cycles should be valid"

    @given(start=valid_color, steps=st.integers(min_value=1, max_value=50))
    def test_random_walk_forward_valid(self, start, steps):
        """Property: A random walk taking only forward steps is valid."""
        sequence = [start]
        current = start
        for _ in range(steps):
            current = (current + 1) % MODULUS
            sequence.append(current)

        is_valid, violations = validate_sequence(sequence)
        assert is_valid, f"Forward random walk should be valid"

    @given(start=valid_color,
           directions=st.lists(st.sampled_from([1, -1]), min_size=1, max_size=50))
    def test_random_walk_forward_backward_valid(self, start, directions):
        """Property: A random walk with ±1 steps is always valid."""
        sequence = [start]
        current = start
        for direction in directions:
            current = (current + direction) % MODULUS
            sequence.append(current)

        is_valid, violations = validate_sequence(sequence)
        assert is_valid, f"±1 random walk should be valid, got: {violations}"

    def test_simple_illegal_jump_detected(self):
        """Property: A sequence with one illegal jump is detected."""
        sequence = [0, 2]  # Black → Yellow (skip White)
        is_valid, violations = validate_sequence(sequence)
        assert not is_valid
        assert len(violations) == 1
        assert violations[0]["from"] == 0
        assert violations[0]["to"] == 2
        assert violations[0]["delta"] == 2

    @given(color_sequence)
    def test_validate_never_crashes(self, sequence):
        """Property: validate_sequence never crashes, always returns valid result."""
        is_valid, violations = validate_sequence(sequence)
        assert isinstance(is_valid, bool)
        assert isinstance(violations, list)
        # If valid, should have no violations
        if is_valid:
            assert len(violations) == 0
        # If invalid, should have at least one violation
        else:
            assert len(violations) > 0


class TestEnumProperties:
    """Property-based tests for Color enum."""

    def test_enum_matches_indices(self):
        """Property: Color enum values match canonical indices."""
        assert Color.BLACK == 0
        assert Color.WHITE == 1
        assert Color.YELLOW == 2
        assert Color.BROWN == 3
        assert Color.RED == 4
        assert Color.GREEN == 5
        assert Color.BLUE == 6

    def test_enum_covers_all_colors(self):
        """Property: Color enum has exactly 7 members."""
        assert len([c for c in Color]) == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
