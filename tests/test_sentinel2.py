"""Tests for Sentinel-2 functionality."""

import pytest

from observearth.datasets.sentinel2 import Sentinel2


def test_sentinel2_initialization():
    """Test Sentinel-2 initialization."""
    # Valid products
    for product in ["2A", "2B", "2C", "all"]:
        sat = Sentinel2(product=product)
        assert sat.product == product
        assert sat.collection_id == "sentinel-2-l2a"

    # Invalid product
    with pytest.raises(ValueError):
        Sentinel2(product="invalid")


def test_sentinel2_collection_id():
    """Test collection ID property."""
    sat = Sentinel2()
    assert sat.collection_id == "sentinel-2-l2a"


def test_sentinel2_product_validation():
    """Test product validation."""
    sat = Sentinel2(product="2A")
    assert sat.product == "2A"

    # Test that invalid products raise error
    with pytest.raises(ValueError, match="Invalid product"):
        Sentinel2(product="3A")
