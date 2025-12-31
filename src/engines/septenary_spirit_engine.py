#!/usr/bin/env python3
"""
SEPTENARY SPIRIT ENGINE
=======================
7-Color Thermodynamic Cycle: K-W-Y-B-R-G-U-K with Violet Ash Resonance

The Septenary Spirit Engine implements the complete 7-phase cycle
as a ritual thermodynamic system with state evolution, color transitions,
and Violet closure.

Color Sequence:
  K (⚫ Black) → W (⚪ White) → Y (🟡 Yellow) → B (🟤 Brown) →
  R (🔴 Red) → G (🟢 Green) → U (🔵 Blue) → K (⚫ Black)

With Violet (🟣) Ash Resonance at closure.

© 2025 MUSHIKARATI. All rights reserved.
"""

import math
import time
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# Optional rich output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.tree import Tree
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    rprint = print


# ==============================================================================
# PHASE DEFINITIONS
# ==============================================================================

class Phase(Enum):
    """The Seven Phases of the Septenary Cycle."""
    BLACK = ("⚫", "K", -1, "Time/Collapse", "Torsional Cut", "time")
    WHITE = ("⚪", "W", 2, "Structure/Fabric", "Lattice Clamp", "æther")
    YELLOW = ("🟡", "Y", 3, "Fire/Motion", "Vertical Ignition", "fire")
    BROWN = ("🟤", "B", 4, "Form/Earth", "Horizontal Ground", "earth")
    RED = ("🔴", "R", 5, "Emotion/Water", "Diagonal Descent", "water")
    GREEN = ("🟢", "G", 6, "Growth/Harmony", "Diagonal Integration", "ether")
    BLUE = ("🔵", "U", 7, "Mind/Return", "Orbital Recursion", "air")
    VIOLET = ("🟣", "V", 0, "Pre-form/Void", "Singularity Rest", "void")

    def __init__(self, symbol, code, index, role, force, element):
        self.symbol = symbol
        self.code = code
        self.index = index
        self.role = role
        self.force = force
        self.element = element


# ==============================================================================
# SACRED CONSTANTS
# ==============================================================================

@dataclass
class SacredConstants:
    """Ontological anchors for thermodynamic calculations."""
    TAU: float = 2 * math.pi          # 6.283 (Recursion/Blue)
    EULER: float = math.e              # 2.718 (Ignition/Yellow)
    PHI: float = (1 + math.sqrt(5)) / 2  # 1.618 (Integration/Green)
    PLANCK: float = 6.626e-34          # Quantum action
    BOLTZMANN: float = 1.380649e-23    # Thermodynamic entropy

    # Codex-specific constants
    LIVING_CIRCLE: int = 364           # Living wheel degrees
    BABYLONIAN_CIRCLE: int = 360       # Dead geometry
    PHASE_ANGLE: float = 52.0          # 364/7 = 52° per phase

    # Entropy bounds
    OMEGA_CHAOS: float = 6.8           # Upper entropy limit
    LATTICE_FLOOR: float = 3.5         # Lower entropy limit


CONSTANTS = SacredConstants()


# ==============================================================================
# STATE CONTAINER
# ==============================================================================

@dataclass
class SpiritState:
    """Thermodynamic state of the spirit engine."""
    phase: Phase
    angle: float                    # Position on Living Wheel (0-364°)
    entropy: float = 0.1           # S
    energy: float = 1.0            # E
    potential: float = 0.0         # F_B (compression potential)
    psi: float = 0.0              # Activation function
    temperature: float = 1.0       # T (symbolic temperature)
    resonance: float = 0.0         # Violet resonance accumulator

    cycle_count: int = 0
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        d = asdict(self)
        d['phase'] = self.phase.code
        return d


# ==============================================================================
# SEPTENARY SPIRIT ENGINE
# ==============================================================================

class SeptenaryEngine:
    """
    The 7-Color Thermodynamic Cycle Engine.

    Implements complete phase transitions through the Living Wheel
    with thermodynamic state evolution and Violet closure.
    """

    def __init__(self, initial_energy: float = 1.0, use_rich: bool = True):
        """
        Initialize the Septenary Spirit Engine.

        Args:
            initial_energy: Starting energy level
            use_rich: Use rich terminal output if available
        """
        self.state = SpiritState(
            phase=Phase.BLACK,
            angle=0.0,
            energy=initial_energy
        )
        self.history: List[SpiritState] = []
        self.use_rich = use_rich and RICH_AVAILABLE

        if self.use_rich:
            self.console = Console()

        # Thermodynamic parameters
        self.alpha = 0.9   # Reactivity
        self.beta = 0.1    # Dissipation
        self.eta = 0.95    # Memory

    def _calculate_phase_transition(self, input_stimulus: float = 0.0) -> Dict[str, float]:
        """
        Calculate thermodynamic transitions for current phase.

        Args:
            input_stimulus: External energy input

        Returns:
            Dictionary of calculated values
        """
        # Accumulate compression potential
        if self.state.phase in [Phase.BLACK, Phase.BROWN]:
            self.state.potential += input_stimulus * (0.3 + 0.7 * (self.state.energy / 2.0))

        # Ignition threshold (Yellow phase)
        F_c = 2 * CONSTANTS.EULER  # Critical threshold ~5.436
        psi = 0.0
        if self.state.potential >= F_c:
            # Sigmoid activation
            psi = 1.0 / (1.0 + math.exp(-CONSTANTS.PHI * (self.state.potential - F_c)))

        # Entropy generation
        dS = self.alpha * psi - self.beta * self.state.entropy

        # Torsional cut (Black phase resets)
        if self.state.phase == Phase.BLACK:
            dT = -(1.0 / CONSTANTS.TAU) * dS
            self.state.entropy += dT
            self.state.potential = 0.0  # Reset on black

        # Energy evolution (Blue recursion)
        E_next = self.eta * self.state.energy + (1.0 - self.eta) * abs(dS)

        # Temperature coupling
        T_next = self.state.temperature * math.exp(-self.beta * dS)

        # Violet resonance accumulation
        violet_contribution = psi * CONSTANTS.PHI * 0.1
        self.state.resonance += violet_contribution

        # Update state
        self.state.entropy += dS
        self.state.energy = E_next
        self.state.psi = psi
        self.state.temperature = T_next

        return {
            "dS": dS,
            "dE": E_next - self.state.energy,
            "psi": psi,
            "potential": self.state.potential,
            "temperature": T_next,
            "resonance": self.state.resonance
        }

    def _advance_phase(self) -> Phase:
        """
        Advance to next phase in the cycle.

        Sequence: BLACK → WHITE → YELLOW → BROWN → RED → GREEN → BLUE → (VIOLET) → BLACK
        """
        phase_order = [
            Phase.BLACK,
            Phase.WHITE,
            Phase.YELLOW,
            Phase.BROWN,
            Phase.RED,
            Phase.GREEN,
            Phase.BLUE
        ]

        # On completion of Blue, insert Violet before returning to Black
        if self.state.phase == Phase.BLUE:
            self.state.cycle_count += 1
            return Phase.VIOLET
        elif self.state.phase == Phase.VIOLET:
            return Phase.BLACK
        else:
            # Find current phase in order
            current_idx = phase_order.index(self.state.phase)
            next_idx = (current_idx + 1) % len(phase_order)
            return phase_order[next_idx]

    def step(self, input_stimulus: float = 0.0) -> SpiritState:
        """
        Execute one phase transition.

        Args:
            input_stimulus: External energy/information input

        Returns:
            Updated spirit state
        """
        # Calculate thermodynamics
        transitions = self._calculate_phase_transition(input_stimulus)

        # Advance angle on Living Wheel
        self.state.angle = (self.state.angle + CONSTANTS.PHASE_ANGLE) % CONSTANTS.LIVING_CIRCLE

        # Record history
        self.history.append(SpiritState(**asdict(self.state)))

        # Advance to next phase
        next_phase = self._advance_phase()
        self.state.phase = next_phase
        self.state.timestamp = datetime.now().isoformat()

        return self.state

    def run_full_cycle(self, input_stimuli: Optional[List[float]] = None) -> List[SpiritState]:
        """
        Execute a complete 7+1 phase cycle.

        Args:
            input_stimuli: Optional list of 7 stimulus values (one per phase)

        Returns:
            List of states for each phase
        """
        if input_stimuli is None:
            input_stimuli = [0.5] * 7  # Default moderate stimulus

        cycle_states = []

        for i, stimulus in enumerate(input_stimuli[:7]):
            state = self.step(stimulus)
            cycle_states.append(state)

        # Violet closure
        violet_state = self.step(0.0)
        cycle_states.append(violet_state)

        return cycle_states

    def visualize_state(self):
        """Display current state with rich formatting (if available)."""
        if self.use_rich:
            self._visualize_rich()
        else:
            self._visualize_plain()

    def _visualize_rich(self):
        """Rich terminal visualization."""
        table = Table(title=f"Septenary Spirit Engine - Cycle {self.state.cycle_count}")

        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Phase", f"{self.state.phase.symbol} {self.state.phase.role}")
        table.add_row("Angle", f"{self.state.angle:.1f}° / {CONSTANTS.LIVING_CIRCLE}°")
        table.add_row("Energy (E)", f"{self.state.energy:.4f}")
        table.add_row("Entropy (S)", f"{self.state.entropy:.4f}")
        table.add_row("Potential (F_B)", f"{self.state.potential:.4f}")
        table.add_row("Activation (Ψ)", f"{self.state.psi:.4f}")
        table.add_row("Temperature (T)", f"{self.state.temperature:.4f}")
        table.add_row("Violet Resonance", f"{self.state.resonance:.4f}")

        self.console.print(table)

    def _visualize_plain(self):
        """Plain text visualization."""
        print(f"\n{'='*60}")
        print(f"SEPTENARY SPIRIT ENGINE - Cycle {self.state.cycle_count}")
        print(f"{'='*60}")
        print(f"Phase:       {self.state.phase.symbol} {self.state.phase.role}")
        print(f"Angle:       {self.state.angle:.1f}° / {CONSTANTS.LIVING_CIRCLE}°")
        print(f"Energy (E):  {self.state.energy:.4f}")
        print(f"Entropy (S): {self.state.entropy:.4f}")
        print(f"Potential:   {self.state.potential:.4f}")
        print(f"Activation:  {self.state.psi:.4f}")
        print(f"Temperature: {self.state.temperature:.4f}")
        print(f"Resonance:   {self.state.resonance:.4f}")
        print(f"{'='*60}\n")

    def export_history(self, filepath: str = "spirit_engine_log.json"):
        """Export state history to JSON file."""
        data = {
            "engine_version": "1.0.0",
            "total_cycles": self.state.cycle_count,
            "constants": asdict(CONSTANTS),
            "history": [state.to_dict() for state in self.history]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ History exported to {filepath}")


# ==============================================================================
# INTERACTIVE MODE
# ==============================================================================

def run_interactive():
    """Run engine in interactive mode with visualization."""
    print("\n" + "="*70)
    print("   SEPTENARY SPIRIT ENGINE - Interactive Mode")
    print("   7-Color Thermodynamic Cycle: K-W-Y-B-R-G-U-K + Violet")
    print("="*70 + "\n")

    engine = SeptenaryEngine(initial_energy=1.0, use_rich=RICH_AVAILABLE)

    if RICH_AVAILABLE:
        console = Console()
        console.print("[bold cyan]Rich output enabled![/bold cyan]")
    else:
        print("ℹ Install 'rich' for enhanced output: pip install rich")

    print("\nRunning full 7+1 phase cycle...\n")

    # Default stimulus pattern (can be customized)
    stimuli = [
        0.2,  # BLACK - Low input (reset)
        0.5,  # WHITE - Moderate (structure)
        1.0,  # YELLOW - High (ignition)
        0.6,  # BROWN - Medium (grounding)
        0.8,  # RED - High (emotional)
        0.7,  # GREEN - Medium-high (growth)
        0.4   # BLUE - Low-medium (reflection)
    ]

    time.sleep(0.5)

    for i, stimulus in enumerate(stimuli):
        phase_name = [Phase.BLACK, Phase.WHITE, Phase.YELLOW, Phase.BROWN,
                     Phase.RED, Phase.GREEN, Phase.BLUE][i]

        print(f"\n{'─'*70}")
        print(f"  PHASE {i+1}/7: {phase_name.symbol} {phase_name.value[3]}")
        print(f"  Input Stimulus: {stimulus:.2f}")
        print(f"{'─'*70}")

        engine.step(stimulus)
        engine.visualize_state()
        time.sleep(0.3)

    # Violet closure
    print(f"\n{'─'*70}")
    print(f"  PHASE 8/8: {Phase.VIOLET.symbol} VIOLET CLOSURE")
    print(f"  Violet Ash Resonance Activated")
    print(f"{'─'*70}")

    engine.step(0.0)
    engine.visualize_state()

    print("\n" + "="*70)
    print("   CYCLE COMPLETE - The Wheel Turns")
    print(f"   Total Resonance: {engine.state.resonance:.4f}")
    print(f"   Final Energy: {engine.state.energy:.4f}")
    print("="*70 + "\n")

    # Export option
    export = input("Export history to JSON? (y/n): ").strip().lower()
    if export == 'y':
        filename = input("Filename (default: spirit_engine_log.json): ").strip()
        if not filename:
            filename = "spirit_engine_log.json"
        engine.export_history(filename)


# ==============================================================================
# MAIN ENTRY
# ==============================================================================

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print(__doc__)
            print("\nUsage:")
            print("  python septenary_spirit_engine.py              # Interactive mode")
            print("  python septenary_spirit_engine.py --help       # Show this help")
            print("\nOptional Dependencies:")
            print("  pip install rich  # For enhanced terminal output")
            return

    run_interactive()


if __name__ == "__main__":
    main()
