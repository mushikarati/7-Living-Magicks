"""
Seven Living Magicks Canon Definition
Single source of truth for the 7-color sequence and adjacency rules.

DO NOT modify this file directly.
The canonical definition is in canon/canon.json.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from enum import IntEnum

# Load canonical definition
_CANON_PATH = Path(__file__).parent / "canon.json"
with open(_CANON_PATH, "r", encoding="utf-8") as f:
    _CANON = json.load(f)


class Color(IntEnum):
    """The 7 colors in canonical order (0-indexed)."""
    BLACK = 0
    WHITE = 1
    YELLOW = 2
    BROWN = 3
    RED = 4
    GREEN = 5
    BLUE = 6


# Canonical sequence
COLORS: List[Dict[str, Any]] = _CANON["canon"]["colors"]["ordered_sequence"]
COLOR_COUNT = len(COLORS)

# Adjacency rule
ADJACENCY_RULE = _CANON["canon"]["adjacency"]["rule"]
MODULUS = _CANON["canon"]["adjacency"]["modulus"]
VALID_DELTAS = _CANON["canon"]["adjacency"]["valid_deltas"]

# Meta tokens
VIOLET = _CANON["canon"]["meta_tokens"]["violet"]
GRAY = _CANON["canon"]["meta_tokens"]["gray"]

# Symbol mappings
SYMBOL_TO_INDEX = {color["symbol"]: color["index"] for color in COLORS}
NAME_TO_INDEX = {color["name"].lower(): color["index"] for color in COLORS}
INDEX_TO_SYMBOL = {color["index"]: color["symbol"] for color in COLORS}
INDEX_TO_NAME = {color["index"]: color["name"] for color in COLORS}


def get_color_by_index(index: int) -> Dict[str, Any]:
    """Get color definition by index."""
    return COLORS[index % MODULUS]


def get_color_by_name(name: str) -> Dict[str, Any]:
    """Get color definition by name (case-insensitive)."""
    index = NAME_TO_INDEX.get(name.lower())
    if index is None:
        raise ValueError(f"Unknown color name: {name}")
    return COLORS[index]


def get_color_by_symbol(symbol: str) -> Dict[str, Any]:
    """Get color definition by symbol."""
    index = SYMBOL_TO_INDEX.get(symbol)
    if index is None:
        raise ValueError(f"Unknown color symbol: {symbol}")
    return COLORS[index]


def is_adjacent(from_index: int, to_index: int) -> bool:
    """
    Check if transition from from_index to to_index respects adjacency law.

    Args:
        from_index: Starting color index (0-6)
        to_index: Target color index (0-6)

    Returns:
        True if transition is legal (±1 mod 7), False otherwise
    """
    delta = (to_index - from_index) % MODULUS
    return delta in VALID_DELTAS


def validate_sequence(sequence: List[int]) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Validate a sequence of color indices respects adjacency law.

    Args:
        sequence: List of color indices

    Returns:
        (is_valid, violations) where violations is a list of Gray events
    """
    violations = []

    for i in range(len(sequence) - 1):
        from_idx = sequence[i]
        to_idx = sequence[i + 1]

        if not is_adjacent(from_idx, to_idx):
            delta = (to_idx - from_idx) % MODULUS
            violations.append({
                "type": "adjacency_violation",
                "index": i,
                "from": from_idx,
                "to": to_idx,
                "delta": delta,
                "reason": f"Illegal jump: delta {delta} not in {VALID_DELTAS}"
            })

    return len(violations) == 0, violations


def get_canon_version() -> str:
    """Get the canon definition version."""
    return _CANON["version"]


# Export all relevant constants and functions
__all__ = [
    "Color",
    "COLORS",
    "COLOR_COUNT",
    "ADJACENCY_RULE",
    "MODULUS",
    "VALID_DELTAS",
    "VIOLET",
    "GRAY",
    "SYMBOL_TO_INDEX",
    "NAME_TO_INDEX",
    "INDEX_TO_SYMBOL",
    "INDEX_TO_NAME",
    "get_color_by_index",
    "get_color_by_name",
    "get_color_by_symbol",
    "is_adjacent",
    "validate_sequence",
    "get_canon_version",
]
