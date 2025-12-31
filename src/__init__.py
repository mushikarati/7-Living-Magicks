"""
7 Living Magicks - Symbolic Framework for Emergent Systems
===========================================================

A symbolic, recursive, and structural model for interpreting
and engineering complex phenomena across computation, consciousness,
ecology, and meaning-making systems.

© 2025 MUSHIKARATI. All rights reserved.
"""

__version__ = "1.0.0"
__author__ = "MUSHIKARATI"
__codex_version__ = "1.0"

# Core framework
from .core import Constants, BaseEngine, BaseDomain, BaseLattice

# Framework implementations
from .framework import (
    TextDomain,
    MagneticDomain,
    BioDomain,
    WhiteLattice,
    SevenCycle,
    ThermoState
)

# Engines
from .engines.codex_ultima import CodexUltima
from .engines.septenary_spirit_engine import SeptenaryEngine

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__codex_version__",

    # Core abstractions
    "Constants",
    "BaseEngine",
    "BaseDomain",
    "BaseLattice",

    # Framework components
    "TextDomain",
    "MagneticDomain",
    "BioDomain",
    "WhiteLattice",
    "SevenCycle",
    "ThermoState",

    # Engines
    "CodexUltima",
    "SeptenaryEngine"
]
