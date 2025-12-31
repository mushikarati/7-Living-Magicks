# Test Suite for 7 Living Magicks

## Overview

Comprehensive testing across three layers:

1. **Unit Tests** (`tests/unit/`) - Individual component testing
2. **Integration Tests** (`tests/integration/`) - Combined system testing
3. **Mythological Tests** (`tests/mythological/`) - Symbolic consistency verification

## Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/mythological/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_constants.py

# Run specific test
pytest tests/unit/test_constants.py::TestConstants::test_tau_value
```

## Test Categories

### Unit Tests
- `test_constants.py` - Sacred constants and validation
- `test_white_lattice.py` - Immune system scanning
- `test_domains.py` - Domain transformations
- `test_thermo_state.py` - Thermodynamic evolution
- `test_operators.py` - Operator behavior

### Integration Tests
- `test_codex_ultima.py` - Full engine execution
- `test_seven_cycle.py` - Complete 7-step cycles
- `test_domain_switching.py` - Cross-domain operations

### Mythological Tests
- `test_364_geometry.py` - Living Wheel vs Babylonian geometry
- `test_operator_order.py` - Operator sequence integrity
- `test_sacred_constants.py` - Mathematical anchor verification

## Test Coverage Goals

- **Unit Tests**: > 90% coverage
- **Integration Tests**: > 80% coverage
- **Mythological Tests**: 100% (non-negotiable truths)

## Writing New Tests

Follow pytest conventions:
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

Example:
```python
import pytest
from src.core.constants import Constants

class TestNewFeature:
    def setup_method(self):
        """Run before each test."""
        pass

    def test_something(self):
        """Test description."""
        assert True
```

## Continuous Integration

Tests run automatically on:
- Every commit (GitHub Actions)
- Pull requests
- Before deployment

See `.github/workflows/tests.yml` for CI configuration.
