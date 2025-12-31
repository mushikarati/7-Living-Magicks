"""
Domain Transformations
======================

Concrete implementations of transformation domains.

© 2025 MUSHIKARATI. All rights reserved.
"""

from ..core.base_domain import BaseDomain
from ..core.constants import Constants
from .thermo_state import ThermoState


class TextDomain(BaseDomain):
    """Text transformation domain."""

    def __init__(self):
        super().__init__()
        self.buffer = ""

    def apply(self, operator: str, physics_state: ThermoState) -> str:
        """Apply symbolic operator to text."""
        if operator == "⚫":
            self.buffer = self.buffer[:len(self.buffer)//2] + " [CUT]"
        elif operator == "⚪":
            self.buffer = f"[{self.buffer.strip()}]"
        elif operator == "🟡":
            self.buffer = self.buffer.upper() + "!"
        elif operator == "🟤":
            self.buffer = f"ROOT({self.buffer})"
        elif operator == "🔴":
            self.buffer = f">>> {self.buffer}"
        elif operator == "🟢":
            words = self.buffer.split()
            if words:
                self.buffer = f"{self.buffer} :: {words[0]}"
        elif operator == "🔵":
            self.buffer = f"REC({self.buffer}, E={physics_state.E:.2f})"

        self.state = self.buffer
        return self.buffer

    def reset(self):
        """Reset buffer."""
        self.buffer = ""
        self.state = None

    def set_input(self, text: str):
        """Set input text."""
        self.buffer = text


class MagneticDomain(BaseDomain):
    """Electromagnetic flux domain."""

    def __init__(self):
        super().__init__()
        self.flux = 0.0

    def apply(self, operator: str, physics_state: ThermoState) -> str:
        """Apply symbolic operator to magnetic field."""
        if operator == "🟡":
            self.flux += physics_state.E * Constants.EULER
        elif operator == "⚫":
            self.flux = 0.0
        elif operator == "🟢":
            self.flux *= Constants.PHI

        self.state = self.flux
        return f"FLUX_DENSITY: {self.flux:.4f} T"

    def reset(self):
        """Reset flux."""
        self.flux = 0.0
        self.state = None


class BioDomain(BaseDomain):
    """Biological/metabolic domain."""

    def __init__(self):
        super().__init__()
        self.atp = 10.0

    def apply(self, operator: str, physics_state: ThermoState) -> str:
        """Apply symbolic operator to metabolic state."""
        if operator == "🟡":
            self.atp += physics_state.E * 5
        elif operator == "🔴":
            self.atp -= 2.0  # Transport cost
        elif operator == "🔵":
            self.atp = self.atp * Constants.TAU  # Cycle efficiency

        # Ensure ATP doesn't go negative
        self.atp = max(0.0, self.atp)

        self.state = self.atp
        return f"METABOLIC_POTENTIAL: {self.atp:.2f} kJ/mol"

    def reset(self):
        """Reset ATP."""
        self.atp = 10.0
        self.state = None
