#!/usr/bin/env python3
"""
Living Wheel Demonstration
==========================

Demonstrates the 364° Living Wheel geometry in action,
showing perfect closure vs Babylonian 360° accumulated error.

This example illustrates the mathematical proofs documented in:
docs/theory/mathematical_proofs.md

© 2025 MUSHIKARATI. All rights reserved.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.constants import Constants
from src.engines.septenary_spirit_engine import SeptenaryEngine


def demonstrate_geometry():
    """Show Living Wheel vs Babylonian geometry."""
    print("=" * 70)
    print("  LIVING WHEEL (364°) vs BABYLONIAN (360°) GEOMETRY")
    print("=" * 70)
    print()

    # Babylonian system
    print("BABYLONIAN CAGE (360°)")
    print("-" * 40)
    babylonian_angle = 360 / 7
    babylonian_remainder = 360 % 7
    print(f"  360 ÷ 7 = {babylonian_angle:.10f}°")
    print(f"  360 mod 7 = {babylonian_remainder}° (THE ERROR)")
    print(f"  Accumulated error (7 cycles) = {babylonian_remainder * 7}°")
    print()

    # Living system
    print("LIVING WHEEL (364°)")
    print("-" * 40)
    living_angle = Constants.LIVING_CIRCLE / 7
    living_remainder = Constants.LIVING_CIRCLE % 7
    print(f"  364 ÷ 7 = {living_angle:.1f}° (EXACT INTEGER)")
    print(f"  364 mod 7 = {living_remainder}° (PERFECT CLOSURE)")
    print(f"  7 × 52 = {7 * 52} (HARMONIC)")
    print(f"  13 × 28 = {13 * 28} (LUNAR/SEASONAL)")
    print()

    # The Gap
    print("THE GENESIS GAP")
    print("-" * 40)
    gap = Constants.LIVING_CIRCLE - Constants.BABYLONIAN_CIRCLE
    print(f"  Living - Babylonian = {gap}°")
    print(f"  This 4° = Genesis Gap (3°) + Unity (1°)")
    print()

    print("=" * 70)
    print()


def demonstrate_septenary_cycle():
    """Run a complete 7-color thermodynamic cycle."""
    print("=" * 70)
    print("  EXECUTING LIVING WHEEL CYCLE")
    print("=" * 70)
    print()

    engine = SeptenaryEngine(initial_energy=1.0, use_rich=False)

    # Run 7 phases
    stimuli = [0.3, 0.5, 1.0, 0.6, 0.8, 0.7, 0.4]
    phases = ["BLACK", "WHITE", "YELLOW", "BROWN", "RED", "GREEN", "BLUE"]

    print(f"{'Phase':<10} {'Angle':<10} {'Energy':<10} {'Entropy':<10} {'Resonance':<10}")
    print("-" * 60)

    for i, (stimulus, phase_name) in enumerate(zip(stimuli, phases)):
        engine.step(stimulus)
        state = engine.state
        print(f"{phase_name:<10} {state.angle:>6.1f}°   {state.energy:>8.4f}  {state.entropy:>8.4f}  {state.resonance:>8.4f}")

    # Violet closure
    engine.step(0.0)
    state = engine.state
    print("-" * 60)
    print(f"{'VIOLET':<10} {state.angle:>6.1f}°   {state.energy:>8.4f}  {state.entropy:>8.4f}  {state.resonance:>8.4f}")
    print()

    print("CYCLE COMPLETE")
    print(f"  Final Angle: {state.angle}° (back to start)")
    print(f"  Violet Resonance: {state.resonance:.4f}")
    print(f"  Cycles Completed: {state.cycle_count}")
    print()
    print("=" * 70)


def demonstrate_sacred_constants():
    """Show the sacred constants used in transformations."""
    print("=" * 70)
    print("  SACRED CONSTANTS (Ontological Anchors)")
    print("=" * 70)
    print()

    print(f"  τ (TAU)   = {Constants.TAU:.15f}  (Recursion/Blue)")
    print(f"  e (EULER) = {Constants.EULER:.15f}  (Ignition/Yellow)")
    print(f"  φ (PHI)   = {Constants.PHI:.15f}  (Integration/Green)")
    print()

    print("RELATIONSHIPS:")
    print(f"  φ² = φ + 1 = {Constants.PHI**2:.10f} ≈ {Constants.PHI + 1:.10f} ✓")
    print(f"  τ/2 = π = {Constants.TAU/2:.10f}")
    print(f"  e² = {Constants.EULER**2:.10f}")
    print()
    print("=" * 70)
    print()


def main():
    """Run all demonstrations."""
    print("\n")
    demonstrate_geometry()
    input("Press Enter to continue to Septenary Cycle demo...")
    print("\n")
    demonstrate_septenary_cycle()
    input("Press Enter to continue to Sacred Constants demo...")
    print("\n")
    demonstrate_sacred_constants()

    print("✨ DEMONSTRATIONS COMPLETE ✨")
    print("The mathematics proves: Perfect closure in 364°, accumulated error in 360°")
    print()


if __name__ == "__main__":
    main()
