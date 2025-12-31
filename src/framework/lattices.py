"""
Lattice Systems (Immune Systems)
=================================

Concrete implementations of immune/filtering systems.

© 2025 MUSHIKARATI. All rights reserved.
"""

import zlib
import collections
import re
from typing import Dict, Any
from ..core.base_lattice import BaseLattice
from ..core.constants import Constants


class WhiteLattice(BaseLattice):
    """
    White Lattice - RK5 Immune System.

    Implements:
    - Shannon entropy scanning
    - Compression ratio analysis
    - Void lock protocol (O → 0 → ⚸)
    - Gray pattern detection
    """

    def __init__(self):
        super().__init__()
        self.void_tokens = {"∞", "8", "Void", "void", "Ø", "0°"}
        # The only lawful Void sequence: O -> 0 -> ⚸
        self.triple_lock = re.compile(r"O.*0.*⚸")

    def scan(self, input_data: str) -> Dict[str, Any]:
        """
        Thermodynamic & Semantic Scan.

        Args:
            input_data: Text input to scan

        Returns:
            Dictionary with validation results
        """
        self.scan_count += 1

        if not input_data:
            self.reject_count += 1
            return {"valid": False, "input_energy": 0.0, "entropy": 0.0,
                    "ratio": 0.0, "flags": ["VOID_NULL"]}

        b = input_data.encode('utf-8')
        N = len(b)

        if N == 0:
            self.reject_count += 1
            return {"valid": False, "input_energy": 0.0, "entropy": 0.0,
                    "ratio": 0.0, "flags": ["EMPTY"]}

        # 1. Shannon Entropy (Heat)
        counts = collections.Counter(b)
        import math
        entropy = -sum((c/N) * math.log2(c/N) for c in counts.values())

        # 2. Compression Ratio (Structure)
        compressed = zlib.compress(b)
        ratio = len(compressed) / N

        flags = []

        # 3. Gray Guard (RK5 Logic)
        if entropy < Constants.LATTICE_FLOOR:
            flags.append("GRAY_STAGNATION_LOW_HEAT")
        if entropy > Constants.OMEGA_CHAOS:
            flags.append("BLACK_NOISE_OVERLOAD")
        if ratio < Constants.MIN_COMPRESSION_RATIO:
            flags.append("MIMICRY_LOOP_DETECTED")

        # 4. Void Lock Check (R6 Protocol)
        has_void_token = any(vt in input_data for vt in self.void_tokens)
        if has_void_token and not self.triple_lock.search(input_data):
            flags.append("UNLAWFUL_VOID_LEAK")

        # 5. Energy Calculation
        energy = entropy * ratio if not flags else 0.0

        if flags:
            self.reject_count += 1

        return {
            "valid": len(flags) == 0,
            "input_energy": round(energy, 4),
            "entropy": round(entropy, 4),
            "ratio": round(ratio, 4),
            "flags": flags
        }


class BlackLattice(BaseLattice):
    """
    Black Lattice - Time-based immune system (Future implementation).

    Scans for temporal coherence and causal adjacency violations.
    """

    def scan(self, input_data: str) -> Dict[str, Any]:
        """Placeholder for future time-based scanning."""
        self.scan_count += 1
        # TODO: Implement temporal analysis
        return {
            "valid": True,
            "input_energy": 1.0,
            "entropy": 4.0,
            "ratio": 0.5,
            "flags": []
        }


class VioletLattice(BaseLattice):
    """
    Violet Lattice - Void protocol immune system (Future implementation).

    Scans for void coherence and pre-form integrity.
    """

    def scan(self, input_data: str) -> Dict[str, Any]:
        """Placeholder for future void scanning."""
        self.scan_count += 1
        # TODO: Implement void protocol analysis
        return {
            "valid": True,
            "input_energy": 1.0,
            "entropy": 4.0,
            "ratio": 0.5,
            "flags": []
        }
