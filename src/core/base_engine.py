"""
Base Engine - Abstract Engine Class
====================================

All engines (Ultima, Alpha, Omega, etc.) inherit from this base class.

© 2025 MUSHIKARATI. All rights reserved.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict
from .base_domain import BaseDomain
from .base_lattice import BaseLattice


class BaseEngine(ABC):
    """
    Abstract base class for all Codex engines.

    Engines orchestrate the transformation of inputs through:
    1. Lattice scanning (immune check)
    2. Thermodynamic evolution
    3. Domain transformations
    4. Operator cycles
    """

    def __init__(self, lattice: BaseLattice, domains: Dict[str, BaseDomain]):
        """
        Initialize engine with lattice and domains.

        Args:
            lattice: Immune system for input validation
            domains: Dictionary of available transformation domains
        """
        self.lattice = lattice
        self.domains = domains
        self.history: List[Any] = []

    @abstractmethod
    def execute(self, input_data: str, target_domain: str, **kwargs) -> Any:
        """
        Execute transformation through the engine.

        Args:
            input_data: Raw input to transform
            target_domain: Target domain for transformation
            **kwargs: Additional engine-specific parameters

        Returns:
            Transformation result
        """
        pass

    @abstractmethod
    def step(self, **kwargs) -> Any:
        """
        Execute single transformation step.

        Returns:
            Step result
        """
        pass

    def get_history(self) -> List[Any]:
        """Get transformation history."""
        return self.history

    def clear_history(self):
        """Clear transformation history."""
        self.history = []

    def list_domains(self) -> List[str]:
        """List available domains."""
        return list(self.domains.keys())

    def get_domain(self, name: str) -> BaseDomain:
        """Get domain by name."""
        return self.domains.get(name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(domains={self.list_domains()}, history_size={len(self.history)})"
