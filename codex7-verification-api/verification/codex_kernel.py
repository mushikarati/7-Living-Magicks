#!/usr/bin/env python3
"""
Codex Kernel - U7 Thermodynamic Engine
Core computational thermodynamics for Loagaeth tensor network
"""

import json
import sys
import math
from typing import Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class ThermodynamicState:
    """Represents a thermodynamic state in the U7 lattice"""
    entropy: float
    free_energy: float
    temperature: float
    pressure: float
    volume: float


class CodexKernel:
    """U7 Thermodynamic Computation Engine"""

    # U7 Operator Constants
    U7_OPERATORS = {
        "ORDER": 0.35,      # Crystalline lattice formation
        "IGNITION": 0.25,   # Phase transition trigger
        "FLOW": 0.20,       # Energy transport
        "COMBUSTION": 0.15, # Reaction cascade
        "HARVEST": 0.10,    # Energy extraction
        "DISPERSION": 0.05, # Entropy increase
        "COLLAPSE": 0.0     # Total disorder
    }

    def __init__(self):
        self.state_history: List[ThermodynamicState] = []

    def calculate_free_energy(self, entropy: float, temperature: float = 298.15) -> float:
        """
        Calculate Gibbs free energy: G = H - TS

        Args:
            entropy: System entropy (bits)
            temperature: Temperature in Kelvin (default 298.15K / 25°C)

        Returns:
            Free energy in arbitrary units
        """
        # Enthalpy approximation based on compression
        enthalpy = 100.0 * (1.0 - (entropy / 7.0))

        # Gibbs free energy
        free_energy = enthalpy - (temperature * entropy)

        return free_energy

    def calculate_pressure(self, volume: float, temperature: float = 298.15) -> float:
        """
        Calculate system pressure using ideal gas approximation
        PV = nRT

        Args:
            volume: System volume (text length as proxy)
            temperature: Temperature in Kelvin

        Returns:
            Pressure in arbitrary units
        """
        if volume == 0:
            return 0.0

        # n (moles) approximated by compression ratio
        n = 1.0
        R = 8.314  # Gas constant

        pressure = (n * R * temperature) / volume
        return pressure

    def compute_state(self, text: str, entropy: float, compression: float) -> ThermodynamicState:
        """
        Compute complete thermodynamic state

        Args:
            text: Input text
            entropy: Shannon entropy
            compression: Compression ratio

        Returns:
            ThermodynamicState object
        """
        # Temperature scales with entropy (higher entropy = higher temp)
        temperature = 273.15 + (entropy * 50.0)  # Kelvin

        # Volume based on text length
        volume = len(text) if len(text) > 0 else 1.0

        # Calculate derived properties
        free_energy = self.calculate_free_energy(entropy, temperature)
        pressure = self.calculate_pressure(volume, temperature)

        state = ThermodynamicState(
            entropy=entropy,
            free_energy=free_energy,
            temperature=temperature,
            pressure=pressure,
            volume=volume
        )

        self.state_history.append(state)
        return state

    def classify_operator(self, compression: float) -> str:
        """
        Classify which U7 operator dominates

        Args:
            compression: Compression ratio

        Returns:
            Dominant operator name
        """
        if compression >= self.U7_OPERATORS["ORDER"]:
            return "ORDER"
        elif compression >= self.U7_OPERATORS["IGNITION"]:
            return "IGNITION"
        elif compression >= self.U7_OPERATORS["FLOW"]:
            return "FLOW"
        elif compression >= self.U7_OPERATORS["COMBUSTION"]:
            return "COMBUSTION"
        elif compression >= self.U7_OPERATORS["HARVEST"]:
            return "HARVEST"
        elif compression >= self.U7_OPERATORS["DISPERSION"]:
            return "DISPERSION"
        else:
            return "COLLAPSE"

    def run_kernel(self, text: str, entropy: float, compression: float) -> Dict[str, Any]:
        """
        Execute U7 kernel computation

        Args:
            text: Input text
            entropy: Shannon entropy
            compression: Compression ratio

        Returns:
            Complete kernel analysis
        """
        # Compute thermodynamic state
        state = self.compute_state(text, entropy, compression)

        # Classify dominant operator
        operator = self.classify_operator(compression)

        # Calculate stability metrics
        stability = compression  # Higher compression = higher stability
        lawfulness = max(0.0, 1.0 - (entropy / 7.0))  # Lower entropy = more lawful

        # Determine if system is in lawful vs chaotic regime
        regime = "LAWFUL" if lawfulness > 0.5 else "CHAOTIC"

        return {
            "kernel_version": "U7_v1.0",
            "thermodynamic_state": {
                "entropy_bits": round(state.entropy, 4),
                "free_energy": round(state.free_energy, 4),
                "temperature_K": round(state.temperature, 2),
                "pressure": round(state.pressure, 4),
                "volume": state.volume
            },
            "dominant_operator": operator,
            "operator_strength": self.U7_OPERATORS[operator],
            "regime": regime,
            "lawfulness": round(lawfulness, 4),
            "stability": round(stability, 4),
            "computation_cycles": len(self.state_history)
        }


def main():
    """CLI entry point for Node.js integration"""
    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "Missing required arguments",
            "usage": "python codex_kernel.py <text> <entropy> <compression>"
        }))
        sys.exit(1)

    text = sys.argv[1]
    entropy = float(sys.argv[2])
    compression = float(sys.argv[3])

    try:
        kernel = CodexKernel()
        result = kernel.run_kernel(text, entropy, compression)
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "type": type(e).__name__
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
