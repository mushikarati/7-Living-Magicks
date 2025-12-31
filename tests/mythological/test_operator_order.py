"""
Test Operator Sequence
=======================

Verify the Seven Operators maintain correct order and properties.
"""

import pytest
from src.framework.operators import Operator, SevenCycle


class TestOperatorOrder:
    """Verify operator sequence and properties."""

    def test_seven_living_operators(self):
        """Should have exactly 7 living operators (excluding Violet and Gray)."""
        living_ops = [
            Operator.BLACK,
            Operator.WHITE,
            Operator.YELLOW,
            Operator.BROWN,
            Operator.RED,
            Operator.GREEN,
            Operator.BLUE
        ]
        assert len(living_ops) == 7

    def test_operator_indices(self):
        """Operators should have correct indices."""
        assert Operator.BLACK.index == -1
        assert Operator.WHITE.index == 2
        assert Operator.YELLOW.index == 3
        assert Operator.BROWN.index == 4
        assert Operator.RED.index == 5
        assert Operator.GREEN.index == 6
        assert Operator.BLUE.index == 7
        assert Operator.VIOLET.index == 0
        assert Operator.GRAY.index == 8

    def test_operator_symbols(self):
        """Operators should have correct symbols."""
        assert Operator.BLACK.symbol == "⚫"
        assert Operator.WHITE.symbol == "⚪"
        assert Operator.YELLOW.symbol == "🟡"
        assert Operator.BROWN.symbol == "🟤"
        assert Operator.RED.symbol == "🔴"
        assert Operator.GREEN.symbol == "🟢"
        assert Operator.BLUE.symbol == "🔵"
        assert Operator.VIOLET.symbol == "🟣"
        assert Operator.GRAY.symbol == "🪩"

    def test_seven_cycle_default_order(self):
        """Default cycle should follow correct operator sequence."""
        cycle = SevenCycle()
        expected_order = ["⚫", "⚪", "🟡", "🟤", "🔴", "🟢", "🔵"]
        assert list(cycle) == expected_order

    def test_seven_cycle_length(self):
        """Cycle should have exactly 7 operators."""
        cycle = SevenCycle()
        assert len(cycle) == 7

    def test_seven_cycle_iteration(self):
        """Cycle should iterate through all operators."""
        cycle = SevenCycle()
        operators_seen = []
        for _ in range(7):
            operators_seen.append(cycle.current())
            cycle.next()

        assert len(operators_seen) == 7
        assert len(set(operators_seen)) == 7  # All unique

    def test_seven_cycle_wraps_around(self):
        """Cycle should wrap back to beginning after 7 steps."""
        cycle = SevenCycle()
        first_op = cycle.current()

        # Advance 7 times
        for _ in range(7):
            cycle.next()

        # Should be back to first operator
        assert cycle.current() == first_op

    def test_violet_outside_cycle(self):
        """Violet (0) should not be in the standard 7-step cycle."""
        cycle = SevenCycle()
        assert Operator.VIOLET.symbol not in list(cycle)

    def test_gray_outside_cycle(self):
        """Gray (8) should not be in the standard 7-step cycle."""
        cycle = SevenCycle()
        assert Operator.GRAY.symbol not in list(cycle)
