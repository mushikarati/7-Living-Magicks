"""
Compression and entropy metrics module.

Provides NCD (Normalized Compression Distance), MDL (Minimum Description Length),
and entropy estimation for detecting degeneracy in color sequences.
"""

import zlib
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass


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
        Estimated entropy (higher = more random/informative, range 0-1+)
    """
    if len(data) == 0:
        return 0.0

    compressed = compress_size(data)
    original = len(data)

    # If data compresses poorly (compressed ~= original), high entropy
    # If data compresses well (compressed << original), low entropy
    ratio = compressed / original

    # Return ratio directly: higher ratio = less compression = higher entropy
    return ratio


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


# Degeneracy detection thresholds
DEGENERACY_COMPRESSION_THRESHOLD = 0.30  # If compressed < 30% of original → high repetition
DEGENERACY_ENTROPY_THRESHOLD = 0.50      # Entropy < 0.5 indicates compressible (low information)
DEGENERACY_NCD_THRESHOLD = 0.15          # Low NCD between windows indicates similarity
DEGENERACY_PLATEAU_WINDOW_COUNT = 3      # Number of similar windows to trigger plateau


@dataclass
class DegeneracyMetrics:
    """Metrics for degeneracy analysis."""
    is_degenerate: bool
    compression_ratio: float
    entropy_estimate: float
    window_ncds: List[float]
    plateau_detected: bool
    trigger_reason: Optional[str] = None
    window_size: int = 0
    num_windows: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_degenerate": self.is_degenerate,
            "compression_ratio": self.compression_ratio,
            "entropy_estimate": self.entropy_estimate,
            "window_ncds": self.window_ncds,
            "plateau_detected": self.plateau_detected,
            "trigger_reason": self.trigger_reason,
            "window_size": self.window_size,
            "num_windows": self.num_windows
        }


def sequence_to_bytes(sequence: List[int]) -> bytes:
    """
    Convert color index sequence to bytes for compression analysis.

    Args:
        sequence: List of color indices (0-6)

    Returns:
        Bytes representation
    """
    return bytes(sequence)


def analyze_windows(data: bytes, window_size: int = 50) -> Tuple[List[bytes], List[float]]:
    """
    Split data into sliding windows and compute NCD between consecutive windows.

    Args:
        data: Sequence data
        window_size: Size of each window

    Returns:
        (windows, ncds) where ncds[i] is NCD between windows[i] and windows[i+1]
    """
    if len(data) < window_size * 2:
        return [data], []

    windows = []
    step = window_size // 2  # 50% overlap

    for i in range(0, len(data) - window_size + 1, step):
        window = data[i:i + window_size]
        windows.append(window)

    # Compute NCD between consecutive windows
    ncds = []
    for i in range(len(windows) - 1):
        ncd_score = ncd(windows[i], windows[i + 1])
        ncds.append(ncd_score)

    return windows, ncds


def detect_entropy_plateau(ncds: List[float], threshold: float = DEGENERACY_NCD_THRESHOLD,
                          min_consecutive: int = DEGENERACY_PLATEAU_WINDOW_COUNT) -> bool:
    """
    Detect if there's a plateau in entropy (many similar consecutive windows).

    Args:
        ncds: NCD scores between consecutive windows
        threshold: Maximum NCD to consider windows similar
        min_consecutive: Minimum number of consecutive similar windows

    Returns:
        True if plateau detected
    """
    if len(ncds) < min_consecutive:
        return False

    consecutive_count = 0
    for ncd_score in ncds:
        if ncd_score < threshold:
            consecutive_count += 1
            if consecutive_count >= min_consecutive:
                return True
        else:
            consecutive_count = 0

    return False


def detect_degeneracy(sequence: List[int],
                     window_size: int = 50,
                     compression_threshold: float = DEGENERACY_COMPRESSION_THRESHOLD,
                     entropy_threshold: float = DEGENERACY_ENTROPY_THRESHOLD,
                     ncd_threshold: float = DEGENERACY_NCD_THRESHOLD) -> DegeneracyMetrics:
    """
    Comprehensive degeneracy detection for color sequences.

    Detects:
    1. High compression ratio (repetitive patterns)
    2. Low entropy (lack of information)
    3. Entropy plateau (consecutive similar windows)

    Args:
        sequence: List of color indices
        window_size: Size of sliding window for analysis
        compression_threshold: Threshold for compression ratio
        entropy_threshold: Threshold for entropy estimate
        ncd_threshold: Threshold for NCD similarity

    Returns:
        DegeneracyMetrics with detailed analysis
    """
    if len(sequence) == 0:
        return DegeneracyMetrics(
            is_degenerate=False,
            compression_ratio=0.0,
            entropy_estimate=0.0,
            window_ncds=[],
            plateau_detected=False,
            window_size=window_size,
            num_windows=0
        )

    data = sequence_to_bytes(sequence)

    # Compute global metrics
    comp_ratio = compression_ratio(data)
    entropy = entropy_estimate(data)

    # Window analysis
    windows, window_ncds = analyze_windows(data, window_size)
    plateau = detect_entropy_plateau(window_ncds, ncd_threshold)

    # Determine if degenerate
    # Lower compression ratio = better compression = more repetitive = degenerate
    # Lower entropy = less random = more predictable = degenerate
    is_degenerate = False
    trigger_reason = None

    if comp_ratio < compression_threshold:
        is_degenerate = True
        trigger_reason = f"High compressibility: {comp_ratio:.3f} < {compression_threshold} (repetitive pattern)"
    elif entropy < entropy_threshold:
        is_degenerate = True
        trigger_reason = f"Low entropy: {entropy:.3f} < {entropy_threshold}"
    elif plateau:
        is_degenerate = True
        trigger_reason = f"Entropy plateau detected: {len([x for x in window_ncds if x < ncd_threshold])} similar windows"

    return DegeneracyMetrics(
        is_degenerate=is_degenerate,
        compression_ratio=comp_ratio,
        entropy_estimate=entropy,
        window_ncds=window_ncds,
        plateau_detected=plateau,
        trigger_reason=trigger_reason,
        window_size=window_size,
        num_windows=len(windows)
    )


def is_degenerate(data: bytes, window_size: int = 50) -> bool:
    """
    Simple boolean degeneracy check (legacy interface).

    For detailed analysis, use detect_degeneracy() instead.

    Args:
        data: Sequence data
        window_size: Size of analysis window

    Returns:
        True if degeneracy detected
    """
    ratio = compression_ratio(data)
    entropy = entropy_estimate(data)

    # Lower ratio = better compression = more degenerate
    return ratio < DEGENERACY_COMPRESSION_THRESHOLD or entropy < DEGENERACY_ENTROPY_THRESHOLD


__all__ = [
    "compress_size",
    "ncd",
    "entropy_estimate",
    "compression_ratio",
    "is_degenerate",
    "detect_degeneracy",
    "DegeneracyMetrics",
    "sequence_to_bytes",
    "analyze_windows",
    "detect_entropy_plateau",
    "DEGENERACY_COMPRESSION_THRESHOLD",
    "DEGENERACY_ENTROPY_THRESHOLD",
    "DEGENERACY_NCD_THRESHOLD",
    "DEGENERACY_PLATEAU_WINDOW_COUNT",
]
