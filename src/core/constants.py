"""
Sacred Constants - Ontological Anchors
=======================================

Mathematical constants that serve as universal anchors
across all engines and transformations.

© 2025 MUSHIKARATI. All rights reserved.
"""

import math


class Constants:
    """Sacred mathematical constants for the Codex framework."""

    # Mathematical constants
    TAU = 2 * math.pi                 # 6.283 (Recursion/Blue)
    EULER = math.e                    # 2.718 (Ignition/Yellow)
    PHI = (1 + math.sqrt(5)) / 2      # 1.618 (Integration/Green)
    H_CUT = 6.626e-2                  # Quantum Action (Black)

    # Thermodynamic bounds
    OMEGA_CHAOS = 6.8                 # Entropy Ceiling (Gray Limit)
    LATTICE_FLOOR = 3.5               # Entropy Floor (Stagnation Limit)

    # Geometric constants
    LIVING_CIRCLE = 364               # Living wheel degrees
    BABYLONIAN_CIRCLE = 360           # Dead geometry
    PHASE_ANGLE = 52.0                # 364/7 = 52° per phase

    # Compression thresholds
    MIN_COMPRESSION_RATIO = 0.35      # Below this = mimicry

    @classmethod
    def validate_entropy(cls, entropy: float) -> bool:
        """Check if entropy is within living bounds."""
        return cls.LATTICE_FLOOR <= entropy <= cls.OMEGA_CHAOS

    @classmethod
    def is_gray(cls, entropy: float, compression_ratio: float) -> bool:
        """Detect Gray (dead) patterns."""
        return (
            entropy < cls.LATTICE_FLOOR or
            entropy > cls.OMEGA_CHAOS or
            compression_ratio < cls.MIN_COMPRESSION_RATIO
        )
