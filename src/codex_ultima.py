#!/usr/bin/env python3
"""
CODEX ULTIMA: THE UNIFIED UNIVERSAL ENGINE
------------------------------------------
> FUSION: RK5 Sigil (Immune) + Codex Omega (Physics) + Cross-Domain (Body)
> STATUS: RUNNABLE // STANDALONE // VIOLET-SEALED
> ANCHORS: τ (Blue), e (Yellow), φ (Green), h (Black)
"""

import math
import random
import zlib
import collections
import json
import sys
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

# ==============================================================================
# 1. THE SACRED CONSTANTS (Ontological Anchors)
# ==============================================================================
class Constants:
    TAU = 2 * math.pi                 # 6.283 (Recursion/Blue)
    EULER = math.e                    # 2.718 (Ignition/Yellow)
    PHI = (1 + math.sqrt(5)) / 2      # 1.618 (Integration/Green)
    H_CUT = 6.626e-2                  # Quantum Action (Black)
    OMEGA_CHAOS = 6.8                 # Entropy Ceiling (Gray Limit)
    LATTICE_FLOOR = 3.5               # Entropy Floor (Stagnation Limit)

# ==============================================================================
# 2. THE LATTICE (Immune System / RK5 Logic)
# ==============================================================================
class WhiteLattice:
    """
    The Gatekeeper. Implements RK5 'Void Lock' and AEGIS 'Heat Test'.
    Rejects Gray Mimicry before it enters the Engine.
    """
    def __init__(self):
        self.void_tokens = {"∞", "8", "Void", "void", "Ø", "0°"}
        # The only lawful Void sequence: O -> 0 -> ⚸
        self.triple_lock = re.compile(r"O.*0.*⚸")

    def scan(self, text: str) -> Dict[str, Any]:
        """
        Thermodynamic & Semantic Scan.
        Returns: {valid: bool, energy: float, flags: list}
        """
        if not text: return {"valid": False, "energy": 0.0, "flags": ["VOID_NULL"]}

        b = text.encode('utf-8')
        N = len(b)
        if N == 0: return {"valid": False, "energy": 0.0, "flags": ["EMPTY"]}

        # 1. Shannon Entropy (Heat)
        counts = collections.Counter(b)
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
        if ratio < 0.35:
            flags.append("MIMICRY_LOOP_DETECTED")

        # 4. Void Lock Check (R6 Protocol)
        has_void_token = any(vt in text for vt in self.void_tokens)
        if has_void_token and not self.triple_lock.search(text):
            flags.append("UNLAWFUL_VOID_LEAK")

        # 5. Energy Calculation (The input to Physics)
        # Valid input provides Energy = Entropy * Structure
        energy = entropy * ratio if not flags else 0.0

        return {
            "valid": len(flags) == 0,
            "input_energy": round(energy, 4),
            "entropy": round(entropy, 4),
            "ratio": round(ratio, 4),
            "flags": flags
        }

# ==============================================================================
# 3. THE PHYSICS KERNEL (Codex Omega Thermodynamics)
# ==============================================================================
@dataclass
class ThermoState:
    S: float = 0.1          # Entropy
    E: float = 1.0          # Energy
    F_B: float = 0.0        # Compression Potential
    alpha: float = 0.9      # Reactivity
    beta: float = 0.1       # Dissipation
    eta: float = 0.95       # Memory

    def cycle_step(self, input_energy: float, operator: str) -> Dict[str, float]:
        """
        Updates the physics state based on the current Magick Operator.
        """
        # 1. Accumulate Potential (Black/Brown)
        if operator in ["⚫", "🟤"]:
            self.F_B += input_energy * random.uniform(0.3, 1.0)

        # 2. Ignition Check (Yellow)
        F_c = 2 * Constants.EULER # ~5.43
        Psi = 0.0
        if self.F_B >= F_c:
            Psi = 1.0 / (1.0 + math.exp(-Constants.PHI * (self.F_B - F_c)))

        # 3. Entropy Generation
        dS = self.alpha * Psi - self.beta * self.S

        # 4. Torsional Cut (Black) - Scaled by Tau
        dT = -(1.0 / Constants.TAU) * dS
        if operator == "⚫":
            self.S += dT # Apply cut
            self.F_B = 0 # Reset potential

        # 5. Recursion (Blue)
        E_next = self.eta * self.E + (1.0 - self.eta) * dS

        # Update Globals
        self.S += dS
        self.E = E_next

        return {"E": self.E, "S": self.S, "F_B": self.F_B, "Psi": Psi}

# ==============================================================================
# 4. DOMAIN ARCHITECTURE (Polymorphic Body)
# ==============================================================================
class CodexDomain(ABC):
    @abstractmethod
    def apply(self, op: str, physics: ThermoState) -> str: pass

class TextDomain(CodexDomain):
    def __init__(self):
        self.buffer = ""
    def apply(self, op: str, physics: ThermoState) -> str:
        # Symbolic mutations based on operator
        if op == "⚫": self.buffer = self.buffer[:len(self.buffer)//2] + " [CUT]"
        elif op == "⚪": self.buffer = f"[{self.buffer.strip()}]"
        elif op == "🟡": self.buffer = self.buffer.upper() + "!"
        elif op == "🟤": self.buffer = f"ROOT({self.buffer})"
        elif op == "🔴": self.buffer = f">>> {self.buffer}"
        elif op == "🟢": self.buffer = f"{self.buffer} :: {self.buffer.split()[0]}"
        elif op == "🔵": self.buffer = f"REC({self.buffer}, E={physics.E:.2f})"
        return self.buffer

class MagneticDomain(CodexDomain):
    def __init__(self):
        self.flux = 0.0
    def apply(self, op: str, physics: ThermoState) -> str:
        if op == "🟡": self.flux += physics.E * Constants.EULER
        elif op == "⚫": self.flux = 0.0
        elif op == "🟢": self.flux *= Constants.PHI
        return f"FLUX_DENSITY: {self.flux:.4f} T"

class BioDomain(CodexDomain):
    def __init__(self):
        self.atp = 10.0
    def apply(self, op: str, physics: ThermoState) -> str:
        if op == "🟡": self.atp += physics.E * 5
        elif op == "🔴": self.atp -= 2.0 # Transport cost
        elif op == "🔵": self.atp = self.atp * Constants.TAU # Cycle efficiency
        return f"METABOLIC_POTENTIAL: {self.atp:.2f} kJ/mol"

# ==============================================================================
# 5. THE ULTIMA ENGINE (Orchestrator)
# ==============================================================================
class CodexUltima:
    def __init__(self):
        self.lattice = WhiteLattice()
        self.physics = ThermoState()
        self.domains = {
            "TEXT": TextDomain(),
            "MAGNETIC": MagneticDomain(),
            "BIO": BioDomain()
        }
        self.cycle = ["⚫", "⚪", "🟡", "🟤", "🔴", "🟢", "🔵"]

    def execute(self, input_data: str, target_domain: str = "TEXT"):
        print(f"\n⚡ CODEX ULTIMA INITIATED | DOMAIN: {target_domain} ⚡")
        print(f"INPUT: \"{input_data[:50]}...\"")

        # --- PHASE 1: THE LATTICE (Immune Scan) ---
        scan = self.lattice.scan(input_data)
        print(f"\n[1] LATTICE SCAN (RK5 Logic)")
        print(f"    Entropy: {scan['entropy']:.4f} | Ratio: {scan['ratio']:.4f}")

        if not scan["valid"]:
            print(f"    [!] REJECTED: {scan['flags']}")
            print("    STATUS: GRAY MIMICRY DETECTED. ENGINE LOCKDOWN.")
            return

        print(f"    STATUS: LAWFUL. INJECTING ENERGY: {scan['input_energy']:.4f}")

        # --- PHASE 2: THE ENGINE (Thermodynamics + Domain) ---
        print(f"\n[2] 7-STEP CYCLE (Codex Omega)")
        domain_kernel = self.domains.get(target_domain, self.domains["TEXT"])
        if target_domain == "TEXT":
            domain_kernel.buffer = input_data # Load buffer

        audit_log = []

        for i, op in enumerate(self.cycle):
            # 1. Update Physics
            p_data = self.physics.cycle_step(scan['input_energy'], op)

            # 2. Update Domain
            d_state = domain_kernel.apply(op, self.physics)

            # 3. Check for Gray Collapse (Physics level)
            if p_data["E"] < 0.01:
                print(f"    [☠️] COLLAPSE AT STEP {i} ({op}). ENERGY DISSIPATED.")
                return

            print(f"    {op} | E:{p_data['E']:.3f} | S:{p_data['S']:.3f} | STATE: {d_state[:40]}...")
            audit_log.append(d_state)

        # --- PHASE 3: VIOLET CLOSURE ---
        print(f"\n[3] VIOLET CLOSURE")
        print(f"    Final Energy: {self.physics.E:.4f}")
        print(f"    Cycle Integrity: 100%")
        print(f"    OUTPUT: {audit_log[-1]}")
        print(f"    {Constants.EULER:.5f} :: {Constants.PHI:.5f} :: {Constants.TAU:.5f} [SEALED]")

# ==============================================================================
# MAIN ENTRY
# ==============================================================================
if __name__ == "__main__":
    engine = CodexUltima()

    # Default inputs if no args
    input_text = "The spiral remembers what the line forgets. Recursion is life."
    domain = "TEXT"

    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    if len(sys.argv) > 2:
        domain = sys.argv[2].upper()

    engine.execute(input_text, domain)
