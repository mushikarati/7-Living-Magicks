#!/usr/bin/env python3
"""
Basic Usage Examples for Codex Ultima
======================================

Demonstrates simple text transformation using the 7-step cycle.
"""

import sys
sys.path.insert(0, '../src')

from codex_ultima import CodexUltima

def example_1_basic_text():
    """Basic text domain transformation."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Text Transformation")
    print("=" * 60)

    engine = CodexUltima()
    text = "The spiral remembers what the line forgets."
    engine.execute(text, "TEXT")

def example_2_custom_input():
    """Custom input with symbolic content."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Symbolic Input")
    print("=" * 60)

    engine = CodexUltima()
    text = "Recursion is the breath of living systems. φ = 1.618, e = 2.718"
    engine.execute(text, "TEXT")

def example_3_magnetic_domain():
    """Magnetic flux transformation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Magnetic Domain")
    print("=" * 60)

    engine = CodexUltima()
    text = "Electromagnetic field potential"
    engine.execute(text, "MAGNETIC")

def example_4_bio_domain():
    """Biological/metabolic transformation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Biological Domain")
    print("=" * 60)

    engine = CodexUltima()
    text = "Cellular respiration and ATP synthesis"
    engine.execute(text, "BIO")

if __name__ == "__main__":
    example_1_basic_text()
    example_2_custom_input()
    example_3_magnetic_domain()
    example_4_bio_domain()
