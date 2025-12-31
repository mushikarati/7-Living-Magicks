"""
Base Lattice - Abstract Immune System
======================================

All lattice (immune) systems inherit from this base class.

© 2025 MUSHIKARATI. All rights reserved.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLattice(ABC):
    """
    Abstract base class for lattice (immune) systems.

    Lattices scan inputs for Gray patterns, mimicry,
    and thermodynamic violations before allowing
    entry into the engine.
    """

    def __init__(self):
        """Initialize lattice with default configuration."""
        self.scan_count = 0
        self.reject_count = 0

    @abstractmethod
    def scan(self, input_data: str) -> Dict[str, Any]:
        """
        Scan input for validity and extract thermodynamic properties.

        Args:
            input_data: Raw input to scan

        Returns:
            Dictionary with keys:
                - valid (bool): Whether input passes scan
                - input_energy (float): Extracted energy
                - entropy (float): Shannon entropy
                - flags (list): List of any warnings/errors
        """
        pass

    def get_statistics(self) -> Dict[str, int]:
        """Get scan statistics."""
        return {
            'total_scans': self.scan_count,
            'total_rejects': self.reject_count,
            'accept_rate': (
                (self.scan_count - self.reject_count) / self.scan_count
                if self.scan_count > 0 else 0.0
            )
        }

    def reset_statistics(self):
        """Reset scan counters."""
        self.scan_count = 0
        self.reject_count = 0

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return f"{self.__class__.__name__}(scans={stats['total_scans']}, rejects={stats['total_rejects']})"
