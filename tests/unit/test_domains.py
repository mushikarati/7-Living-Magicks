"""
Test Domains
============

Verify domain transformations (TEXT, MAGNETIC, BIO).
"""

import pytest
from src.framework.domains import TextDomain, MagneticDomain, BioDomain
from src.framework.thermo_state import ThermoState
from src.core.constants import Constants


class TestTextDomain:
    """Test TEXT domain transformations."""

    def setup_method(self):
        """Create fresh domain for each test."""
        self.domain = TextDomain()
        self.physics = ThermoState()

    def test_black_operator_cuts_text(self):
        """⚫ BLACK should cut text in half."""
        self.domain.set_input("Hello World")
        result = self.domain.apply("⚫", self.physics)
        assert "[CUT]" in result
        assert len(result) < len("Hello World") + 10

    def test_white_operator_encloses(self):
        """⚪ WHITE should enclose text in brackets."""
        self.domain.set_input("test")
        result = self.domain.apply("⚪", self.physics)
        assert result == "[test]"

    def test_yellow_operator_ignites(self):
        """🟡 YELLOW should uppercase and add exclamation."""
        self.domain.set_input("hello")
        result = self.domain.apply("🟡", self.physics)
        assert "HELLO!" in result

    def test_brown_operator_grounds(self):
        """🟤 BROWN should add ROOT wrapper."""
        self.domain.set_input("text")
        result = self.domain.apply("🟤", self.physics)
        assert "ROOT(text)" in result

    def test_reset(self):
        """Domain should reset properly."""
        self.domain.set_input("test")
        self.domain.apply("⚪", self.physics)
        self.domain.reset()
        assert self.domain.buffer == ""
        assert self.domain.state is None


class TestMagneticDomain:
    """Test MAGNETIC domain transformations."""

    def setup_method(self):
        """Create fresh domain for each test."""
        self.domain = MagneticDomain()
        self.physics = ThermoState()

    def test_initial_flux_zero(self):
        """Initial flux should be zero."""
        assert self.domain.flux == 0.0

    def test_yellow_increases_flux(self):
        """🟡 YELLOW should increase magnetic flux."""
        initial_flux = self.domain.flux
        result = self.domain.apply("🟡", self.physics)
        assert self.domain.flux > initial_flux
        assert "FLUX_DENSITY" in result

    def test_black_resets_flux(self):
        """⚫ BLACK should reset flux to zero."""
        # Build up flux first
        self.domain.flux = 10.0
        self.domain.apply("⚫", self.physics)
        assert self.domain.flux == 0.0

    def test_green_multiplies_by_phi(self):
        """🟢 GREEN should multiply flux by φ."""
        self.domain.flux = 10.0
        self.domain.apply("🟢", self.physics)
        expected = 10.0 * Constants.PHI
        assert abs(self.domain.flux - expected) < 1e-10

    def test_reset(self):
        """Domain should reset properly."""
        self.domain.flux = 100.0
        self.domain.reset()
        assert self.domain.flux == 0.0


class TestBioDomain:
    """Test BIO (biological/metabolic) domain transformations."""

    def setup_method(self):
        """Create fresh domain for each test."""
        self.domain = BioDomain()
        self.physics = ThermoState()

    def test_initial_atp(self):
        """Initial ATP should be 10.0 kJ/mol."""
        assert self.domain.atp == 10.0

    def test_yellow_increases_atp(self):
        """🟡 YELLOW should increase ATP (metabolic ignition)."""
        initial_atp = self.domain.atp
        self.domain.apply("🟡", self.physics)
        assert self.domain.atp > initial_atp

    def test_red_decreases_atp(self):
        """🔴 RED should decrease ATP (transport cost)."""
        initial_atp = self.domain.atp
        self.domain.apply("🔴", self.physics)
        assert self.domain.atp < initial_atp

    def test_blue_multiplies_by_tau(self):
        """🔵 BLUE should multiply ATP by τ (cycle efficiency)."""
        self.domain.atp = 5.0
        self.domain.apply("🔵", self.physics)
        expected = 5.0 * Constants.TAU
        assert abs(self.domain.atp - expected) < 1e-6

    def test_atp_cannot_go_negative(self):
        """ATP should not go below zero."""
        self.domain.atp = 1.0
        # Apply RED multiple times
        for _ in range(10):
            self.domain.apply("🔴", self.physics)
        assert self.domain.atp >= 0.0

    def test_reset(self):
        """Domain should reset to initial ATP."""
        self.domain.atp = 100.0
        self.domain.reset()
        assert self.domain.atp == 10.0
