"""
Test Sacred Constants
=====================

Verify mathematical constants and validation logic.
"""

import pytest
import math
from src.core.constants import Constants


class TestConstants:
    """Test suite for Constants class."""

    def test_tau_value(self):
        """TAU should equal 2π."""
        assert Constants.TAU == 2 * math.pi
        assert abs(Constants.TAU - 6.283185307179586) < 1e-10

    def test_euler_value(self):
        """EULER should equal e."""
        assert Constants.EULER == math.e
        assert abs(Constants.EULER - 2.718281828459045) < 1e-10

    def test_phi_value(self):
        """PHI should equal golden ratio."""
        expected_phi = (1 + math.sqrt(5)) / 2
        assert Constants.PHI == expected_phi
        assert abs(Constants.PHI - 1.618033988749895) < 1e-10

    def test_living_circle_degrees(self):
        """Living circle should be 364°."""
        assert Constants.LIVING_CIRCLE == 364

    def test_babylonian_circle_degrees(self):
        """Babylonian (dead) circle should be 360°."""
        assert Constants.BABYLONIAN_CIRCLE == 360

    def test_phase_angle(self):
        """Phase angle should be exactly 52° (364/7)."""
        assert Constants.PHASE_ANGLE == 52.0
        assert Constants.LIVING_CIRCLE / 7 == Constants.PHASE_ANGLE

    def test_entropy_bounds(self):
        """Entropy bounds should be properly set."""
        assert Constants.LATTICE_FLOOR == 3.5
        assert Constants.OMEGA_CHAOS == 6.8
        assert Constants.OMEGA_CHAOS > Constants.LATTICE_FLOOR

    def test_validate_entropy_in_bounds(self):
        """Valid entropy should pass validation."""
        assert Constants.validate_entropy(4.0) is True
        assert Constants.validate_entropy(5.5) is True
        assert Constants.validate_entropy(6.5) is True

    def test_validate_entropy_out_of_bounds(self):
        """Out of bounds entropy should fail validation."""
        assert Constants.validate_entropy(2.0) is False  # Below floor
        assert Constants.validate_entropy(8.0) is False  # Above ceiling
        assert Constants.validate_entropy(0.0) is False

    def test_validate_entropy_edge_cases(self):
        """Entropy at exact bounds should pass."""
        assert Constants.validate_entropy(3.5) is True   # Exact floor
        assert Constants.validate_entropy(6.8) is True   # Exact ceiling

    def test_is_gray_low_entropy(self):
        """Low entropy should be detected as Gray."""
        assert Constants.is_gray(2.0, 0.5) is True

    def test_is_gray_high_entropy(self):
        """High entropy (noise) should be detected as Gray."""
        assert Constants.is_gray(7.5, 0.5) is True

    def test_is_gray_low_compression(self):
        """Low compression ratio should be detected as Gray (mimicry)."""
        assert Constants.is_gray(4.0, 0.2) is True

    def test_is_not_gray(self):
        """Valid entropy and compression should not be Gray."""
        assert Constants.is_gray(4.5, 0.6) is False
        assert Constants.is_gray(5.0, 0.8) is False
