"""Utility functions for geometry handling and data processing."""

from typing import Any, Dict, Tuple

import numpy as np


def validate_geometry(geom: Dict[str, Any]) -> bool:
    """
    Validate GeoJSON geometry.

    Args:
        geom: GeoJSON geometry dictionary

    Returns:
        True if valid geometry
    """
    required_keys = ["type", "coordinates"]
    return all(key in geom for key in required_keys)


def normalize_band_values(array: np.ndarray, scale_factor: float = 10000) -> np.ndarray:
    """
    Normalize band values to 0-1 range.

    Args:
        array: Input array
        scale_factor: Scale factor for normalization

    Returns:
        Normalized array
    """
    return array / scale_factor


def get_bbox_from_geometry(geom: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """
    Extract bounding box from geometry.

    Args:
        geom: GeoJSON geometry

    Returns:
        Tuple of (minx, miny, maxx, maxy)
    """
    if geom["type"] == "Polygon":
        coords = geom["coordinates"][0]
        lons = [coord[0] for coord in coords]
        lats = [coord[1] for coord in coords]
        return min(lons), min(lats), max(lons), max(lats)

    raise ValueError(f"Unsupported geometry type: {geom['type']}")


def create_sample_geometry(lon: float, lat: float, size: float = 0.1) -> Dict[str, Any]:
    """
    Create a sample square geometry around a point.

    Args:
        lon: Longitude
        lat: Latitude
        size: Size of the square in degrees

    Returns:
        GeoJSON polygon geometry
    """
    half_size = size / 2
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [lon - half_size, lat - half_size],
                [lon + half_size, lat - half_size],
                [lon + half_size, lat + half_size],
                [lon - half_size, lat + half_size],
                [lon - half_size, lat - half_size],
            ]
        ],
    }
