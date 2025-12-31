"""
Base Domain - Abstract Domain Class
====================================

All domain transformations inherit from this base class.

© 2025 MUSHIKARATI. All rights reserved.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseDomain(ABC):
    """
    Abstract base class for all domain transformations.

    Domains define how symbolic operators transform
    different types of systems (text, magnetic, biological, etc.)
    """

    def __init__(self):
        """Initialize domain with default state."""
        self.state = None

    @abstractmethod
    def apply(self, operator: str, physics_state: Any) -> str:
        """
        Apply symbolic operator transformation.

        Args:
            operator: Symbolic operator (⚫, ⚪, 🟡, etc.)
            physics_state: Current thermodynamic state

        Returns:
            String representation of transformed state
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset domain to initial state."""
        pass

    def get_state(self) -> Any:
        """Get current domain state."""
        return self.state

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(state={self.state})"
