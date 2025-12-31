"""
Symbolic Operators
==================

The Seven Magick Operators and cycle management.

© 2025 MUSHIKARATI. All rights reserved.
"""

from typing import List
from enum import Enum


class Operator(Enum):
    """The Seven Living Magick Operators."""

    BLACK = ("⚫", -1, "Time/Collapse", "Torsional Cut")
    WHITE = ("⚪", 2, "Structure/Fabric", "Lattice Clamp")
    YELLOW = ("🟡", 3, "Fire/Motion", "Vertical Ignition")
    BROWN = ("🟤", 4, "Form/Earth", "Horizontal Ground")
    RED = ("🔴", 5, "Emotion/Water", "Diagonal Descent")
    GREEN = ("🟢", 6, "Growth/Harmony", "Diagonal Integration")
    BLUE = ("🔵", 7, "Mind/Return", "Orbital Recursion")
    VIOLET = ("🟣", 0, "Pre-form/Void", "Singularity Rest")
    GRAY = ("🪩", 8, "Mimicry/Dead Loop", "False Recursion")

    def __init__(self, symbol, index, role, force):
        self.symbol = symbol
        self.index = index
        self.role = role
        self.force = force


class SevenCycle:
    """Manages the 7-step operator cycle."""

    DEFAULT_CYCLE = [
        Operator.BLACK.symbol,
        Operator.WHITE.symbol,
        Operator.YELLOW.symbol,
        Operator.BROWN.symbol,
        Operator.RED.symbol,
        Operator.GREEN.symbol,
        Operator.BLUE.symbol
    ]

    def __init__(self, custom_cycle: List[str] = None):
        """
        Initialize cycle with optional custom operator sequence.

        Args:
            custom_cycle: Optional custom operator sequence
        """
        self.cycle = custom_cycle or self.DEFAULT_CYCLE
        self.position = 0

    def current(self) -> str:
        """Get current operator."""
        return self.cycle[self.position]

    def next(self) -> str:
        """Advance to next operator and return it."""
        self.position = (self.position + 1) % len(self.cycle)
        return self.current()

    def reset(self):
        """Reset cycle to beginning."""
        self.position = 0

    def __iter__(self):
        """Make cycle iterable."""
        return iter(self.cycle)

    def __len__(self):
        """Get cycle length."""
        return len(self.cycle)
