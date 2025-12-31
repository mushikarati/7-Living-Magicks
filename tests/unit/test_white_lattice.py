"""
Test White Lattice (Immune System)
===================================

Verify entropy scanning, compression detection, and Gray rejection.
"""

import pytest
from src.framework.lattices import WhiteLattice


class TestWhiteLattice:
    """Test suite for WhiteLattice immune system."""

    def setup_method(self):
        """Create fresh lattice for each test."""
        self.lattice = WhiteLattice()

    def test_accepts_valid_text(self):
        """Valid text should pass lattice scan."""
        result = self.lattice.scan("The spiral remembers what the line forgets.")
        assert result['valid'] is True
        assert result['input_energy'] > 0
        assert len(result['flags']) == 0

    def test_rejects_empty_input(self):
        """Empty input should be rejected."""
        result = self.lattice.scan("")
        assert result['valid'] is False
        assert "VOID_NULL" in result['flags']
        assert result['input_energy'] == 0.0

    def test_rejects_low_entropy(self):
        """Low entropy (Gray stagnation) should be rejected."""
        # Highly repetitive = low entropy
        result = self.lattice.scan("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        assert result['valid'] is False
        assert any("GRAY_STAGNATION" in flag for flag in result['flags'])

    def test_calculates_entropy(self):
        """Entropy calculation should be reasonable."""
        result = self.lattice.scan("Hello world!")
        assert 0 <= result['entropy'] <= 8  # Shannon entropy in bits
        assert result['entropy'] > 0

    def test_calculates_compression_ratio(self):
        """Compression ratio should be calculated."""
        result = self.lattice.scan("The quick brown fox jumps over the lazy dog.")
        assert 0 < result['ratio'] <= 1.0  # Compressed size / original size

    def test_detects_low_compression_mimicry(self):
        """Low compression ratio indicates mimicry/loops."""
        # Already compressed data won't compress much
        compressed_like = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP1234567890!@#$%^&*()"
        result = self.lattice.scan(compressed_like)
        # Should have low compression ratio
        assert result['ratio'] > 0.5  # Less compressible

    def test_void_lock_rejects_unlawful_void(self):
        """Unlawful void sequences should be rejected."""
        # Has void token but not lawful sequence (O -> 0 -> ⚸)
        result = self.lattice.scan("The void ∞ calls without proper sequence")
        assert result['valid'] is False
        assert any("UNLAWFUL_VOID" in flag for flag in result['flags'])

    def test_void_lock_accepts_lawful_void(self):
        """Lawful void sequence (O -> 0 -> ⚸) should be accepted."""
        # Contains lawful sequence
        result = self.lattice.scan("The path from O through 0 to ⚸ is lawful and complete")
        # Should pass void check (may still fail entropy, but not void)
        assert not any("UNLAWFUL_VOID" in flag for flag in result['flags'])

    def test_tracks_scan_count(self):
        """Lattice should track number of scans."""
        initial_count = self.lattice.scan_count
        self.lattice.scan("test 1")
        self.lattice.scan("test 2")
        self.lattice.scan("test 3")
        assert self.lattice.scan_count == initial_count + 3

    def test_tracks_reject_count(self):
        """Lattice should track rejections."""
        initial_rejects = self.lattice.reject_count
        self.lattice.scan("")  # Will be rejected
        self.lattice.scan("aaaaaaaaaaaaaaaa")  # Low entropy, rejected
        assert self.lattice.reject_count > initial_rejects

    def test_statistics(self):
        """Get statistics should return correct data."""
        self.lattice.scan("valid text here")
        self.lattice.scan("")  # Rejected
        stats = self.lattice.get_statistics()

        assert stats['total_scans'] >= 2
        assert stats['total_rejects'] >= 1
        assert 0 <= stats['accept_rate'] <= 1.0

    def test_reset_statistics(self):
        """Statistics should reset."""
        self.lattice.scan("test")
        self.lattice.reset_statistics()
        assert self.lattice.scan_count == 0
        assert self.lattice.reject_count == 0
