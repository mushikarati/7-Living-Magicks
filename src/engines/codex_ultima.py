#!/usr/bin/env python3
"""
CODEX ULTIMA: THE UNIFIED UNIVERSAL ENGINE
------------------------------------------
> FUSION: RK5 Sigil (Immune) + Codex Omega (Physics) + Cross-Domain (Body)
> STATUS: RUNNABLE // STANDALONE // VIOLET-SEALED
> ANCHORS: τ (Blue), e (Yellow), φ (Green), h (Black)

Refactored to use modular framework components.

© 2025 MUSHIKARATI. All rights reserved.
"""

import sys
from typing import Optional, List, Dict, Any

# Import from modular framework
from ..core import BaseEngine, Constants
from ..framework import (
    WhiteLattice,
    TextDomain,
    MagneticDomain,
    BioDomain,
    ThermoState,
    SevenCycle
)


# ==============================================================================
# CODEX ULTIMA ENGINE
# ==============================================================================

class CodexUltima(BaseEngine):
    """
    The Codex Ultima Engine - Unified Universal Transformation System.

    Orchestrates:
    1. White Lattice immune scanning
    2. Thermodynamic state evolution
    3. 7-step symbolic cycle
    4. Polymorphic domain transformations
    5. Violet closure
    """

    def __init__(self):
        """Initialize Codex Ultima with default configuration."""
        # Initialize lattice
        lattice = WhiteLattice()

        # Initialize domains
        domains = {
            "TEXT": TextDomain(),
            "MAGNETIC": MagneticDomain(),
            "BIO": BioDomain()
        }

        # Call parent constructor
        super().__init__(lattice, domains)

        # Initialize physics kernel
        self.physics = ThermoState()

        # Initialize 7-step cycle
        self.cycle = SevenCycle()

    def execute(self, input_data: str, target_domain: str = "TEXT", **kwargs) -> Dict[str, Any]:
        """
        Execute full transformation through 7-step cycle.

        Args:
            input_data: Input text to transform
            target_domain: Target domain (TEXT, MAGNETIC, BIO)
            **kwargs: Additional parameters

        Returns:
            Dictionary with execution results
        """
        print(f"\n⚡ CODEX ULTIMA INITIATED | DOMAIN: {target_domain} ⚡")
        print(f"INPUT: \"{input_data[:50]}...\"")

        # --- PHASE 1: THE LATTICE (Immune Scan) ---
        scan = self.lattice.scan(input_data)
        print(f"\n[1] LATTICE SCAN (RK5 Logic)")
        print(f"    Entropy: {scan['entropy']:.4f} | Ratio: {scan['ratio']:.4f}")

        if not scan["valid"]:
            print(f"    [!] REJECTED: {scan['flags']}")
            print("    STATUS: GRAY MIMICRY DETECTED. ENGINE LOCKDOWN.")
            return {
                "status": "REJECTED",
                "scan": scan,
                "output": None
            }

        print(f"    STATUS: LAWFUL. INJECTING ENERGY: {scan['input_energy']:.4f}")

        # --- PHASE 2: THE ENGINE (Thermodynamics + Domain) ---
        print(f"\n[2] 7-STEP CYCLE (Codex Omega)")

        # Get target domain
        domain_kernel = self.domains.get(target_domain, self.domains["TEXT"])

        # Load input into domain if TEXT
        if target_domain == "TEXT":
            domain_kernel.set_input(input_data)

        # Reset cycle
        self.cycle.reset()

        # Execute 7-step cycle
        audit_log = []
        for i, op in enumerate(self.cycle):
            # 1. Update Physics
            p_data = self.physics.cycle_step(scan['input_energy'], op)

            # 2. Update Domain
            d_state = domain_kernel.apply(op, self.physics)

            # 3. Check for Gray Collapse
            if p_data["E"] < 0.01:
                print(f"    [☠️] COLLAPSE AT STEP {i} ({op}). ENERGY DISSIPATED.")
                return {
                    "status": "COLLAPSED",
                    "scan": scan,
                    "output": audit_log
                }

            print(f"    {op} | E:{p_data['E']:.3f} | S:{p_data['S']:.3f} | STATE: {d_state[:40]}...")
            audit_log.append({
                "operator": op,
                "physics": p_data,
                "domain_state": d_state
            })

            # Record in history
            self.history.append({
                "step": i,
                "operator": op,
                "physics": p_data,
                "domain": d_state
            })

        # --- PHASE 3: VIOLET CLOSURE ---
        print(f"\n[3] VIOLET CLOSURE")
        print(f"    Final Energy: {self.physics.E:.4f}")
        print(f"    Cycle Integrity: 100%")
        print(f"    OUTPUT: {audit_log[-1]['domain_state']}")
        print(f"    {Constants.EULER:.5f} :: {Constants.PHI:.5f} :: {Constants.TAU:.5f} [SEALED]")

        return {
            "status": "COMPLETE",
            "scan": scan,
            "output": audit_log,
            "final_state": audit_log[-1],
            "final_energy": self.physics.E
        }

    def step(self, operator: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute single operator step.

        Args:
            operator: Operator to use (if None, uses next in cycle)
            **kwargs: Additional parameters

        Returns:
            Step result
        """
        if operator is None:
            operator = self.cycle.next()

        # Get current domain or default to TEXT
        target_domain = kwargs.get('domain', 'TEXT')
        domain_kernel = self.domains.get(target_domain, self.domains["TEXT"])

        # Apply operator
        input_energy = kwargs.get('energy', 0.5)
        p_data = self.physics.cycle_step(input_energy, operator)
        d_state = domain_kernel.apply(operator, self.physics)

        result = {
            "operator": operator,
            "physics": p_data,
            "domain_state": d_state
        }

        self.history.append(result)
        return result


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    """Main entry point for standalone execution."""
    engine = CodexUltima()

    # Default inputs if no args
    input_text = "The spiral remembers what the line forgets. Recursion is life."
    domain = "TEXT"

    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    if len(sys.argv) > 2:
        domain = sys.argv[2].upper()

    engine.execute(input_text, domain)


if __name__ == "__main__":
    main()
