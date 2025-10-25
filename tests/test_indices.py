"""Tests for index computation."""

import numpy as np
import pytest
import xarray as xr

from observearth.core.indices import compute_index, ndbi, ndvi, ndwi


def create_test_data():
    """Create test data arrays."""
    data = np.random.rand(10, 10) * 1000 + 1000  # Values between 1000-2000
    coords = {"x": range(10), "y": range(10)}
    return xr.DataArray(data, coords=coords)


def test_ndvi_computation():
    """Test NDVI computation."""
    red = create_test_data()
    nir = create_test_data() + 500  # NIR typically higher than red

    result = ndvi(red, nir)

    # NDVI should be between -1 and 1
    assert result.min() >= -1
    assert result.max() <= 1

    # For vegetation, NDVI should be positive when NIR > RED
    assert result.mean() > 0


def test_ndwi_computation():
    """Test NDWI computation."""
    green = create_test_data()
    nir = create_test_data()

    result = ndwi(green, nir)

    # NDWI should be between -1 and 1
    assert result.min() >= -1
    assert result.max() <= 1


def test_ndbi_computation():
    """Test NDBI computation."""
    swir = create_test_data()
    nir = create_test_data()

    result = ndbi(swir, nir)

    # NDBI should be between -1 and 1
    assert result.min() >= -1
    assert result.max() <= 1


def test_compute_index_function():
    """Test the main compute_index function."""
    red = create_test_data()
    nir = create_test_data() + 500
    green = create_test_data()
    swir = create_test_data()

    # Test NDVI
    ndvi_result = compute_index("NDVI", RED=red, NIR=nir)
    assert ndvi_result is not None

    # Test NDWI
    ndwi_result = compute_index("NDWI", GREEN=green, NIR=nir)
    assert ndwi_result is not None

    # Test NDBI
    ndbi_result = compute_index("NDBI", SWIR=swir, NIR=nir)
    assert ndbi_result is not None

    # Test invalid index
    with pytest.raises(ValueError):
        compute_index("INVALID", RED=red, NIR=nir)
