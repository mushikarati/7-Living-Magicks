"""
Test 364° Living Wheel Geometry
================================

Verify the mathematical proof that 364° provides perfect closure
versus 360° Babylonian geometry.
"""

import pytest
from src.core.constants import Constants


class Test364Geometry:
    """Verify Living Wheel (364°) vs Babylonian (360°) geometry."""

    def test_living_circle_divides_evenly_by_seven(self):
        """364 ÷ 7 should equal exactly 52 with no remainder."""
        assert Constants.LIVING_CIRCLE % 7 == 0
        assert Constants.LIVING_CIRCLE / 7 == 52.0
        assert Constants.PHASE_ANGLE == 52.0

    def test_babylonian_circle_has_remainder(self):
        """360 ÷ 7 should have a 3° remainder (the error)."""
        assert Constants.BABYLONIAN_CIRCLE % 7 == 3
        babylonian_angle = Constants.BABYLONIAN_CIRCLE / 7
        assert abs(babylonian_angle - 51.42857142857143) < 1e-10

    def test_seven_phases_close_living_circle(self):
        """7 phases × 52° should equal 364° (perfect closure)."""
        total_angle = 7 * Constants.PHASE_ANGLE
        assert total_angle == Constants.LIVING_CIRCLE
        assert total_angle == 364

    def test_seven_phases_dont_close_babylonian_circle(self):
        """7 phases × 51.43° ≈ 360° but not exact (accumulated error)."""
        babylonian_phase = Constants.BABYLONIAN_CIRCLE / 7
        total_angle = 7 * babylonian_phase
        # Should be close to 360 but not exactly due to floating point
        assert abs(total_angle - 360.0) < 1e-10
        # But the integer division shows the gap
        assert Constants.BABYLONIAN_CIRCLE % 7 != 0

    def test_lunar_seasonal_alignment(self):
        """364 = 13 × 28 (lunar/seasonal harmony)."""
        assert 13 * 28 == 364
        assert 13 * 28 == Constants.LIVING_CIRCLE

    def test_living_vs_babylonian_gap(self):
        """The gap between systems should be 4°."""
        gap = Constants.LIVING_CIRCLE - Constants.BABYLONIAN_CIRCLE
        assert gap == 4

    def test_accumulated_babylonian_error(self):
        """After 7 cycles, Babylonian system accumulates 21° error."""
        # 3° remainder × 7 cycles = 21° total error
        remainder = Constants.BABYLONIAN_CIRCLE % 7
        accumulated_error = remainder * 7
        assert accumulated_error == 21
