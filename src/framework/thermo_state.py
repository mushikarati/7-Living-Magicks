"""
Thermodynamic State
===================

State container for thermodynamic evolution.

© 2025 MUSHIKARATI. All rights reserved.
"""

from dataclasses import dataclass
from ..core.constants import Constants


@dataclass
class ThermoState:
    """Thermodynamic state of the system."""

    S: float = 0.1          # Entropy
    E: float = 1.0          # Energy
    F_B: float = 0.0        # Compression Potential
    alpha: float = 0.9      # Reactivity
    beta: float = 0.1       # Dissipation
    eta: float = 0.95       # Memory

    def cycle_step(self, input_energy: float, operator: str) -> dict:
        """
        Updates the physics state based on the current Magick Operator.

        Args:
            input_energy: External energy input
            operator: Current symbolic operator

        Returns:
            Dictionary of calculated thermodynamic values
        """
        import random
        import math

        # 1. Accumulate Potential (Black/Brown)
        if operator in ["⚫", "🟤"]:
            self.F_B += input_energy * random.uniform(0.3, 1.0)

        # 2. Ignition Check (Yellow)
        F_c = 2 * Constants.EULER  # ~5.43
        Psi = 0.0
        if self.F_B >= F_c:
            Psi = 1.0 / (1.0 + math.exp(-Constants.PHI * (self.F_B - F_c)))

        # 3. Entropy Generation
        dS = self.alpha * Psi - self.beta * self.S

        # 4. Torsional Cut (Black) - Scaled by Tau
        dT = -(1.0 / Constants.TAU) * dS
        if operator == "⚫":
            self.S += dT  # Apply cut
            self.F_B = 0  # Reset potential

        # 5. Recursion (Blue)
        E_next = self.eta * self.E + (1.0 - self.eta) * dS

        # Update Globals
        self.S += dS
        self.E = E_next

        return {"E": self.E, "S": self.S, "F_B": self.F_B, "Psi": Psi}
