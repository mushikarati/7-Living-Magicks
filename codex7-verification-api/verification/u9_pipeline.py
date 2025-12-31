#!/usr/bin/env python3
"""
U9 Pipeline - 9-Phase Verification Engine
Thermodynamic verification system with extended phase analysis
"""

import json
import sys
import math
import zlib
from datetime import datetime
from typing import Dict, Any, Tuple

# 9-Phase Thermodynamic Bounds (U9 Extension)
PHASE_BOUNDS = {
    "CRYSTAL_WHITE": {"entropy_max": 3.5, "compression_min": 0.40, "phase": 1},
    "WHITE_LATTICE": {"entropy_max": 3.8, "compression_min": 0.35, "phase": 2},
    "YELLOW_IGNITION": {"entropy_max": 4.2, "compression_min": 0.25, "phase": 3},
    "GREEN_ACCUMULATION": {"entropy_max": 4.5, "compression_min": 0.20, "phase": 4},
    "RED_COMBUSTION": {"entropy_max": 4.8, "compression_min": 0.15, "phase": 5},
    "ORANGE_HARVEST": {"entropy_max": 5.2, "compression_min": 0.10, "phase": 6},
    "BLUE_DISPERSION": {"entropy_max": 5.5, "compression_min": 0.05, "phase": 7},
    "VIOLET_DISSOLUTION": {"entropy_max": 6.2, "compression_min": 0.02, "phase": 8},
    "BLACK_COLLAPSE": {"entropy_max": 7.0, "compression_min": 0.0, "phase": 9}
}


def shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy in bits"""
    if not text:
        return 0.0

    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    total = len(text)
    entropy = -sum((count/total) * math.log2(count/total) for count in freq.values())

    return entropy


def compression_ratio(text: str) -> float:
    """Calculate compression ratio as fuel density measure"""
    if not text:
        return 0.0

    raw = text.encode('utf-8')
    compressed = zlib.compress(raw, level=9)
    ratio = 1.0 - (len(compressed) / len(raw))

    return ratio


def calculate_coherence(text: str) -> float:
    """Calculate semantic coherence score (0-1)"""
    if not text:
        return 0.0

    # Word-level analysis
    words = text.split()
    if len(words) < 2:
        return 0.5

    # Average word length (longer words = higher coherence)
    avg_word_len = sum(len(w) for w in words) / len(words)
    coherence = min(1.0, avg_word_len / 10.0)

    return coherence


def calculate_stability(entropy_val: float, comp_ratio: float) -> float:
    """Calculate thermodynamic stability (0-1, higher = more stable)"""
    # Lower entropy + higher compression = higher stability
    entropy_factor = max(0, 1.0 - (entropy_val / 7.0))
    compression_factor = comp_ratio

    stability = (entropy_factor + compression_factor) / 2.0
    return stability


def classify_phase(entropy_val: float, comp_ratio: float) -> Tuple[str, int]:
    """Determine U9 phase based on thermodynamic bounds"""
    # Ordered by strictness (Crystal White → Black Collapse)
    if entropy_val <= 3.5 and comp_ratio >= 0.40:
        return "CRYSTAL_WHITE", 1
    elif entropy_val <= 3.8 and comp_ratio >= 0.35:
        return "WHITE_LATTICE", 2
    elif entropy_val <= 4.2 and comp_ratio >= 0.25:
        return "YELLOW_IGNITION", 3
    elif entropy_val <= 4.5 and comp_ratio >= 0.20:
        return "GREEN_ACCUMULATION", 4
    elif entropy_val <= 4.8 and comp_ratio >= 0.15:
        return "RED_COMBUSTION", 5
    elif entropy_val <= 5.2 and comp_ratio >= 0.10:
        return "ORANGE_HARVEST", 6
    elif entropy_val <= 5.5 and comp_ratio >= 0.05:
        return "BLUE_DISPERSION", 7
    elif entropy_val <= 6.2 and comp_ratio >= 0.02:
        return "VIOLET_DISSOLUTION", 8
    else:
        return "BLACK_COLLAPSE", 9


def verify_text(text: str, threshold: str = "WHITE_LATTICE") -> Dict[str, Any]:
    """
    Main U9 verification logic

    Args:
        text: Input text to verify
        threshold: Minimum acceptable phase

    Returns:
        Dictionary with verification results
    """
    # Calculate core metrics
    entropy_val = shannon_entropy(text)
    comp_ratio = compression_ratio(text)
    coherence = calculate_coherence(text)
    stability = calculate_stability(entropy_val, comp_ratio)

    # Classify phase
    detected_phase, phase_num = classify_phase(entropy_val, comp_ratio)

    # Get threshold phase number
    threshold_phase_num = PHASE_BOUNDS.get(threshold, {}).get("phase", 2)

    # Verification passes if detected phase <= threshold phase
    verified = phase_num <= threshold_phase_num

    # Calculate confidence score
    confidence = stability * coherence

    return {
        "verified": verified,
        "detected_phase": detected_phase,
        "phase_number": phase_num,
        "threshold_phase": threshold,
        "threshold_number": threshold_phase_num,
        "confidence": round(confidence, 4),
        "metrics": {
            "entropy_bits": round(entropy_val, 4),
            "compression_ratio": round(comp_ratio, 4),
            "coherence": round(coherence, 4),
            "stability": round(stability, 4),
            "text_length": len(text),
            "word_count": len(text.split())
        },
        "bounds_used": PHASE_BOUNDS[detected_phase],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "engine": "U9_PIPELINE_v1.0"
    }


def main():
    """CLI entry point for Node.js child_process.spawn"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing required argument: text",
            "usage": "python u9_pipeline.py <text> [threshold]"
        }))
        sys.exit(1)

    text = sys.argv[1]
    threshold = sys.argv[2] if len(sys.argv) > 2 else "WHITE_LATTICE"

    try:
        result = verify_text(text, threshold)
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
