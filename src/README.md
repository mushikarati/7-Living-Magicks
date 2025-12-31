# Source Code Documentation

## Overview

The `codex_ultima.py` module implements the core computational engine for the Seven Living Magicks framework.

## Architecture

### 1. Constants (`Constants` class)
Sacred mathematical constants serving as ontological anchors:
- **TAU** (τ = 2π): Recursion/Blue magic
- **EULER** (e = 2.718): Ignition/Yellow magic
- **PHI** (φ = 1.618): Integration/Green magic
- **H_CUT**: Quantum action threshold
- **OMEGA_CHAOS** (6.8): Entropy ceiling (Gray limit)
- **LATTICE_FLOOR** (3.5): Entropy floor (stagnation limit)

### 2. White Lattice (`WhiteLattice` class)
Immune system implementing RK5 "Void Lock" logic:
- **Thermodynamic scanning**: Shannon entropy calculation
- **Structure analysis**: Compression ratio detection
- **Gray detection**: Identifies mimicry and dead loops
- **Void protocol**: Validates lawful void sequences (O → 0 → ⚸)

### 3. Thermo State (`ThermoState` class)
Physics kernel managing thermodynamic evolution:
- **State variables**: Entropy (S), Energy (E), Compression Potential (F_B)
- **Operators**: α (reactivity), β (dissipation), η (memory)
- **Cycle stepping**: Processes input through 7-phase transformations

### 4. Domain Architecture (`CodexDomain` abstract class)
Polymorphic transformation systems:
- **TextDomain**: Symbolic text mutations
- **MagneticDomain**: Electromagnetic flux calculations
- **BioDomain**: Metabolic potential modeling

### 5. Codex Ultima (`CodexUltima` class)
Main orchestrator:
- **Phase 1**: Lattice scan (immune check)
- **Phase 2**: 7-step cycle (⚫⚪🟡🟤🔴🟢🔵)
- **Phase 3**: Violet closure (seal and report)

## Usage

```python
from codex_ultima import CodexUltima

# Create engine instance
engine = CodexUltima()

# Execute transformation
engine.execute("Your input text", "TEXT")
```

### Domain Options
- `"TEXT"` - Text transformation
- `"MAGNETIC"` - Electromagnetic field modeling
- `"BIO"` - Metabolic/biological modeling

## Command Line

```bash
python codex_ultima.py "Your text" TEXT
python codex_ultima.py "Magnetic field" MAGNETIC
python codex_ultima.py "Cell metabolism" BIO
```

## The Seven Operators

1. **⚫ Black** - Torsional cut, sacred ending
2. **⚪ White** - Envelope, structural framing
3. **🟡 Yellow** - Spark, ignition
4. **🟤 Brown** - Womb, grounding
5. **🔴 Red** - Blood, emotional flow
6. **🟢 Green** - Grove, integration
7. **🔵 Blue** - Mirror, recursion

## Gray Detection

The system rejects inputs that exhibit:
- Low entropy (< 3.5) - stagnation
- High entropy (> 6.8) - noise
- Low compression ratio (< 0.35) - mimicry loops
- Unlawful void sequences

## License

© 2025 MUSHIKARATI. All rights reserved.
