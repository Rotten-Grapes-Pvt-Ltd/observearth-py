# Testing Guide

This guide covers testing practices and procedures for ObserveEarth development.

## Test Structure

```
tests/
├── test_indices.py      # Index computation tests
├── test_sentinel2.py    # Sentinel-2 specific tests
├── test_landsat8.py     # Landsat-8 specific tests
├── test_export.py       # Export functionality tests
└── test_utils.py        # Utility function tests
```

## Running Tests

### Basic Testing
```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_indices.py

# Run specific test function
poetry run pytest tests/test_indices.py::test_ndvi_computation
```

### Coverage Testing
```bash
# Run tests with coverage report
poetry run pytest --cov=observearth

# Generate HTML coverage report
poetry run pytest --cov=observearth --cov-report=html
open htmlcov/index.html
```

### Performance Testing
```bash
# Run tests with timing
poetry run pytest --durations=10
```

## Writing Tests

### Test Categories

#### 1. Unit Tests
Test individual functions in isolation:

```python
def test_ndvi_computation():
    """Test NDVI computation with known values."""
    red = xr.DataArray([100, 200, 300])
    nir = xr.DataArray([400, 500, 600])
    
    result = ndvi(red, nir)
    expected = (nir - red) / (nir + red)
    
    assert result.equals(expected)
```

#### 2. Integration Tests
Test component interactions:

```python
def test_sentinel2_search_integration():
    """Test Sentinel-2 search with mock data."""
    sat = Sentinel2(product="2A")
    
    # Mock the search to avoid real API calls
    with patch.object(sat.client, 'search') as mock_search:
        mock_search.return_value.items.return_value = []
        
        items = sat.search(
            start_date="2024-01-01",
            end_date="2024-01-31",
            geom=test_geometry,
            cloud_cover=10
        )
        
        assert len(items.items) == 0
```

#### 3. Property-Based Tests
Test with generated data:

```python
from hypothesis import given, strategies as st

@given(
    red=st.lists(st.floats(0, 1000), min_size=1, max_size=100),
    nir=st.lists(st.floats(0, 1000), min_size=1, max_size=100)
)
def test_ndvi_properties(red, nir):
    """Test NDVI properties with random data."""
    if len(red) == len(nir):
        red_arr = xr.DataArray(red)
        nir_arr = xr.DataArray(nir)
        
        result = ndvi(red_arr, nir_arr)
        
        # NDVI should be between -1 and 1
        assert result.min() >= -1
        assert result.max() <= 1
```

### Test Fixtures

Create reusable test data:

```python
import pytest

@pytest.fixture
def sample_geometry():
    """Sample GeoJSON geometry for testing."""
    return {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    }

@pytest.fixture
def sample_xarray():
    """Sample xarray DataArray for testing."""
    import numpy as np
    data = np.random.rand(10, 10)
    return xr.DataArray(data, dims=['x', 'y'])
```

### Mocking External Services

Mock Microsoft Planetary Computer API calls:

```python
from unittest.mock import patch, MagicMock

def test_search_with_mock():
    """Test search functionality with mocked API."""
    
    # Create mock item
    mock_item = MagicMock()
    mock_item.id = "test-item-1"
    mock_item.datetime = datetime(2024, 1, 15)
    mock_item.properties = {"eo:cloud_cover": 5}
    
    # Mock the search response
    with patch('pystac_client.Client.open') as mock_client:
        mock_search = MagicMock()
        mock_search.items.return_value = [mock_item]
        mock_client.return_value.search.return_value = mock_search
        
        sat = Sentinel2()
        items = sat.search(
            start_date="2024-01-01",
            end_date="2024-01-31",
            geom=sample_geometry,
            cloud_cover=10
        )
        
        assert len(items.items) == 1
        assert items.items[0].id == "test-item-1"
```

## Test Data Management

### Using Test Data Files
```python
import os
from pathlib import Path

def get_test_data_path(filename):
    """Get path to test data file."""
    return Path(__file__).parent / "data" / filename

def test_with_sample_data():
    """Test using sample data file."""
    data_path = get_test_data_path("sample_ndvi.tif")
    if data_path.exists():
        # Test with real data
        pass
    else:
        # Skip or use synthetic data
        pytest.skip("Test data not available")
```

### Environment-Based Testing
```python
import os
import pytest

@pytest.mark.skipif(
    not os.getenv("PLANETARY_COMPUTER_KEY"),
    reason="Requires Planetary Computer API key"
)
def test_real_api_call():
    """Test with real API (requires credentials)."""
    # This test only runs if API key is available
    pass
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run tests
      run: poetry run pytest --cov=observearth
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Performance Testing

### Benchmarking
```python
import time
import pytest

def test_ndvi_performance():
    """Test NDVI computation performance."""
    # Create large arrays
    size = 1000
    red = xr.DataArray(np.random.rand(size, size))
    nir = xr.DataArray(np.random.rand(size, size))
    
    start_time = time.time()
    result = ndvi(red, nir)
    end_time = time.time()
    
    # Should complete within reasonable time
    assert end_time - start_time < 1.0  # 1 second
    assert result.shape == (size, size)
```

### Memory Testing
```python
import psutil
import os

def test_memory_usage():
    """Test memory usage doesn't exceed limits."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operation
    large_array = xr.DataArray(np.random.rand(5000, 5000))
    result = ndvi(large_array, large_array)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable
    assert memory_increase < 500 * 1024 * 1024  # 500MB
```

## Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Coverage Configuration
```toml
# pyproject.toml
[tool.coverage.run]
source = ["observearth"]
omit = [
    "*/tests/*",
    "*/examples/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Best Practices

1. **Test Names**: Use descriptive names that explain what is being tested
2. **Arrange-Act-Assert**: Structure tests clearly
3. **One Assertion**: Focus each test on one specific behavior
4. **Fast Tests**: Keep unit tests fast (< 1 second)
5. **Isolated Tests**: Tests should not depend on each other
6. **Mock External Dependencies**: Don't rely on external services
7. **Test Edge Cases**: Include boundary conditions and error cases

## Debugging Tests

```bash
# Run tests with debugger
poetry run pytest --pdb

# Run single test with output
poetry run pytest tests/test_indices.py::test_ndvi_computation -s

# Run tests with detailed output
poetry run pytest -vvv --tb=long
```

## Test Examples

See the existing test files for examples:
- `tests/test_indices.py` - Index computation tests
- `tests/test_sentinel2.py` - Satellite class tests

Happy testing! 🧪