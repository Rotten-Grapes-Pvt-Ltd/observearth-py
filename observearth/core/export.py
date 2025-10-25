"""Export functionality for raster data."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


def export_raster(
    data: xr.DataArray,
    export_type: str,
    path: str,
    min_val: float = None,
    max_val: float = None,
    cmap: str = "viridis",
) -> None:
    """
    Export raster data to GeoTIFF or PNG.

    Args:
        data: xarray DataArray to export
        export_type: 'tiff' or 'png'
        path: Output file path
        min_val: Minimum value for scaling
        max_val: Maximum value for scaling
        cmap: Colormap for PNG export
    """
    if export_type.lower() == "tiff":
        _export_geotiff(data, path)
    elif export_type.lower() == "png":
        _export_png(data, path, min_val, max_val, cmap)
    else:
        raise ValueError(f"Unsupported export type: {export_type}")


def _export_geotiff(data: xr.DataArray, path: str) -> None:
    """Export as GeoTIFF using rioxarray."""
    # Ensure CRS is set
    if data.rio.crs is None:
        data = data.rio.write_crs("EPSG:4326")

    data.rio.to_raster(path)


def _export_png(
    data: xr.DataArray,
    path: str,
    min_val: float = None,
    max_val: float = None,
    cmap: str = "viridis",
) -> None:
    """Export as PNG using matplotlib."""
    # Convert to numpy array
    array = data.values

    # Handle NaN values
    array = np.where(np.isnan(array), 0, array)

    # Apply scaling if provided
    if min_val is not None and max_val is not None:
        array = np.clip(array, min_val, max_val)
        array = (array - min_val) / (max_val - min_val)

    # Create figure and save
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(array, cmap=cmap)
    ax.axis("off")
    plt.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
