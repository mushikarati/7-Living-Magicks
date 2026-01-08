"""
Compression and entropy metrics module.

Provides NCD (Normalized Compression Distance), MDL (Minimum Description Length),
and entropy estimation for detecting degeneracy in color sequences.
"""

import zlib
from typing import Any


def compress_size(data: bytes) -> int:
    """
    Get compressed size of data using zlib.

    Args:
        data: Bytes to compress

    Returns:
        Compressed size in bytes
    """
    return len(zlib.compress(data))


def ncd(x: bytes, y: bytes) -> float:
    """
    Compute Normalized Compression Distance between x and y.

    NCD(x, y) = [C(xy) - min(C(x), C(y))] / max(C(x), C(y))

    Args:
        x: First byte sequence
        y: Second byte sequence

    Returns:
        NCD score in range [0, 1] where 0 = identical, 1 = completely different
    """
    c_x = compress_size(x)
    c_y = compress_size(y)
    c_xy = compress_size(x + y)

    numerator = c_xy - min(c_x, c_y)
    denominator = max(c_x, c_y)

    if denominator == 0:
        return 0.0

    return numerator / denominator


def entropy_estimate(data: bytes) -> float:
    """
    Estimate Shannon entropy of data based on compression ratio.

    Args:
        data: Bytes to analyze

    Returns:
        Estimated entropy (higher = more random/informative)
    """
    if len(data) == 0:
        return 0.0

    compressed = compress_size(data)
    compression_ratio = compressed / len(data)

    # Lower compression ratio → higher entropy
    # This is a rough estimate; true entropy requires symbol frequency analysis
    return 1.0 - compression_ratio


def compression_ratio(data: bytes) -> float:
    """
    Compute compression ratio: compressed_size / original_size

    Args:
        data: Bytes to compress

    Returns:
        Compression ratio in range [0, 1+]
        Lower = more compressible (less entropy)
    """
    if len(data) == 0:
        return 0.0

    return compress_size(data) / len(data)


# TODO: Implement degeneracy detection thresholds
DEGENERACY_COMPRESSION_THRESHOLD = 0.9  # Placeholder
DEGENERACY_ENTROPY_THRESHOLD = 0.2      # Placeholder


def is_degenerate(data: bytes, window_size: int = 100) -> bool:
    """
    Detect if data shows signs of degeneracy (mimic loops, low entropy).

    TODO: Implement proper degeneracy detection with:
    - Sliding window analysis
    - NCD between consecutive windows
    - Entropy plateau detection

    Args:
        data: Sequence data
        window_size: Size of analysis window

    Returns:
        True if degeneracy detected
    """
    # Placeholder implementation
    ratio = compression_ratio(data)
    entropy = entropy_estimate(data)

    return ratio > DEGENERACY_COMPRESSION_THRESHOLD or entropy < DEGENERACY_ENTROPY_THRESHOLD


__all__ = [
    "compress_size",
    "ncd",
    "entropy_estimate",
    "compression_ratio",
    "is_degenerate",
    "DEGENERACY_COMPRESSION_THRESHOLD",
    "DEGENERACY_ENTROPY_THRESHOLD",
]
