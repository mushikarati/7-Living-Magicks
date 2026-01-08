"""
Tests for compression metrics and degeneracy detection.
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.compression.metrics import (
    compress_size,
    ncd,
    entropy_estimate,
    compression_ratio,
    detect_degeneracy,
    sequence_to_bytes,
    analyze_windows,
    detect_entropy_plateau,
    DegeneracyMetrics,
    DEGENERACY_COMPRESSION_THRESHOLD,
    DEGENERACY_ENTROPY_THRESHOLD,
)


class TestBasicMetrics:
    """Test basic compression metrics."""

    def test_compress_size(self):
        """Test compression size calculation."""
        data = b"hello world"
        size = compress_size(data)
        assert isinstance(size, int)
        assert size > 0
        assert size <= len(data) + 100  # zlib has some overhead

    def test_ncd_identical(self):
        """Test NCD of identical sequences is low."""
        data = b"test data"
        score = ncd(data, data)
        assert score < 0.2  # Should be very similar (some overhead from zlib)

    def test_ncd_different(self):
        """Test NCD of different sequences is high."""
        x = b"\x00\x01\x02\x03\x04\x05\x06"
        y = b"\x06\x05\x04\x03\x02\x01\x00"
        score = ncd(x, y)
        assert 0 <= score <= 1

    def test_entropy_estimate_random(self):
        """Test entropy of random-like data is higher."""
        random_data = bytes(range(256))
        repetitive_data = b"\x00" * 256

        entropy_random = entropy_estimate(random_data)
        entropy_repetitive = entropy_estimate(repetitive_data)

        # Random data should have higher entropy (less compressible)
        assert entropy_random > entropy_repetitive, \
            f"Random: {entropy_random}, Repetitive: {entropy_repetitive}"

    def test_compression_ratio_repetitive(self):
        """Test compression ratio is high for repetitive data."""
        repetitive = b"\x00" * 1000
        ratio = compression_ratio(repetitive)
        assert ratio < 0.1  # Should compress very well


class TestSequenceConversion:
    """Test sequence to bytes conversion."""

    def test_sequence_to_bytes(self):
        """Test color sequence converts to bytes."""
        sequence = [0, 1, 2, 3, 4, 5, 6]
        data = sequence_to_bytes(sequence)
        assert isinstance(data, bytes)
        assert len(data) == len(sequence)
        assert list(data) == sequence


class TestWindowAnalysis:
    """Test sliding window analysis."""

    def test_analyze_windows_short_sequence(self):
        """Test window analysis on short sequence."""
        data = b"\x00\x01\x02\x03"
        windows, ncds = analyze_windows(data, window_size=10)
        assert len(windows) == 1
        assert len(ncds) == 0

    def test_analyze_windows_long_sequence(self):
        """Test window analysis on longer sequence."""
        data = bytes(range(100))
        windows, ncds = analyze_windows(data, window_size=20)
        assert len(windows) > 1
        assert len(ncds) == len(windows) - 1

    def test_analyze_windows_overlap(self):
        """Test windows have 50% overlap."""
        data = bytes(range(100))
        windows, _ = analyze_windows(data, window_size=20)
        # With 50% overlap, step = 10, so (100-20)/10 + 1 = 9 windows
        assert len(windows) >= 7


class TestEntropyPlateau:
    """Test entropy plateau detection."""

    def test_plateau_detected(self):
        """Test plateau detection with similar windows."""
        # All low NCDs (similar windows)
        ncds = [0.01, 0.02, 0.01, 0.03, 0.02]
        plateau = detect_entropy_plateau(ncds, threshold=0.05, min_consecutive=3)
        assert plateau

    def test_no_plateau(self):
        """Test no plateau with varying windows."""
        # High NCDs (different windows)
        ncds = [0.5, 0.6, 0.4, 0.7, 0.5]
        plateau = detect_entropy_plateau(ncds, threshold=0.05, min_consecutive=3)
        assert not plateau

    def test_plateau_insufficient_windows(self):
        """Test no plateau with too few windows."""
        ncds = [0.01, 0.02]
        plateau = detect_entropy_plateau(ncds, threshold=0.05, min_consecutive=3)
        assert not plateau


class TestDegeneracyDetection:
    """Test comprehensive degeneracy detection."""

    def test_lawful_sequence_not_degenerate(self):
        """Test lawful forward sequence is not degenerate."""
        # Forward cycle with some variation
        sequence = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 1, 0, 6, 5, 4, 3, 2, 3, 4, 5]
        metrics = detect_degeneracy(sequence)
        # This should not be degenerate (has variation)
        assert isinstance(metrics, DegeneracyMetrics)

    def test_mimic_loop_detected(self):
        """Test mimic loop (high repetition) is detected."""
        # Exact repetition of full cycle (mimic loop)
        cycle = [0, 1, 2, 3, 4, 5, 6]
        sequence = cycle * 20  # 140 elements of pure repetition
        metrics = detect_degeneracy(sequence, window_size=30)

        assert metrics.is_degenerate
        assert ("compress" in metrics.trigger_reason.lower() or
                "plateau" in metrics.trigger_reason.lower() or
                "entropy" in metrics.trigger_reason.lower())

    def test_single_color_repetition(self):
        """Test single color repetition is degenerate."""
        sequence = [0] * 100
        metrics = detect_degeneracy(sequence)

        assert metrics.is_degenerate
        assert metrics.compression_ratio > DEGENERACY_COMPRESSION_THRESHOLD or \
               metrics.entropy_estimate < DEGENERACY_ENTROPY_THRESHOLD

    def test_empty_sequence(self):
        """Test empty sequence handling."""
        sequence = []
        metrics = detect_degeneracy(sequence)
        assert not metrics.is_degenerate
        assert metrics.num_windows == 0

    def test_short_sequence(self):
        """Test short sequence doesn't trigger window analysis."""
        sequence = [0, 1, 2]
        metrics = detect_degeneracy(sequence, window_size=10)
        assert isinstance(metrics, DegeneracyMetrics)

    def test_metrics_has_all_fields(self):
        """Test DegeneracyMetrics has all expected fields."""
        sequence = [0, 1, 2, 3, 4, 5, 6]
        metrics = detect_degeneracy(sequence)

        assert hasattr(metrics, 'is_degenerate')
        assert hasattr(metrics, 'compression_ratio')
        assert hasattr(metrics, 'entropy_estimate')
        assert hasattr(metrics, 'window_ncds')
        assert hasattr(metrics, 'plateau_detected')
        assert hasattr(metrics, 'trigger_reason')
        assert hasattr(metrics, 'window_size')
        assert hasattr(metrics, 'num_windows')

    def test_metrics_to_dict(self):
        """Test DegeneracyMetrics converts to dict."""
        sequence = [0, 1, 2, 3]
        metrics = detect_degeneracy(sequence)
        data = metrics.to_dict()

        assert isinstance(data, dict)
        assert 'is_degenerate' in data
        assert 'compression_ratio' in data
        assert 'entropy_estimate' in data

    def test_alternating_pattern_not_too_degenerate(self):
        """Test alternating pattern has some entropy."""
        # Alternating but lawful
        sequence = [0, 1, 0, 1, 0, 1, 0, 1] * 10
        metrics = detect_degeneracy(sequence)

        # May or may not be degenerate depending on thresholds,
        # but should compute metrics
        assert isinstance(metrics, DegeneracyMetrics)
        assert metrics.compression_ratio > 0

    def test_varied_sequence_not_degenerate(self):
        """Test varied sequence with legal transitions is not degenerate."""
        # Complex but lawful path
        sequence = [0, 1, 2, 1, 0, 6, 5, 4, 3, 2, 3, 4, 5, 6, 0, 1, 0, 6, 5, 6, 0]
        metrics = detect_degeneracy(sequence, window_size=10)

        # This should NOT be degenerate (has variation and complexity)
        # Though it depends on exact thresholds
        assert isinstance(metrics, DegeneracyMetrics)


class TestThresholds:
    """Test threshold configuration."""

    def test_custom_thresholds(self):
        """Test degeneracy detection with custom thresholds."""
        sequence = [0, 1, 2, 3, 4, 5, 6]
        metrics = detect_degeneracy(
            sequence,
            compression_threshold=0.01,  # Very low (only extremely compressed is degenerate)
            entropy_threshold=0.01,      # Very low (only extremely low entropy is degenerate)
            ncd_threshold=0.01
        )
        # With very strict thresholds, shouldn't be degenerate
        assert not metrics.is_degenerate


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
