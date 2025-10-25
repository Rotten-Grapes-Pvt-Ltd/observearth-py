"""Index computation formulas."""

import xarray as xr


def compute_index(name: str, **bands) -> xr.DataArray:
    """
    Compute vegetation/water indices.

    Args:
        name: Index name (NDVI, NDWI, NDBI)
        **bands: Band data as keyword arguments

    Returns:
        Computed index as xarray DataArray
    """
    if name == "NDVI":
        red, nir = bands["RED"], bands["NIR"]
        return (nir - red) / (nir + red)

    elif name == "NDWI":
        green, nir = bands["GREEN"], bands["NIR"]
        return (green - nir) / (green + nir)

    elif name == "NDBI":
        swir, nir = bands["SWIR"], bands["NIR"]
        return (swir - nir) / (swir + nir)

    else:
        raise ValueError(f"Unknown index: {name}")


def ndvi(red: xr.DataArray, nir: xr.DataArray) -> xr.DataArray:
    """Compute NDVI."""
    return (nir - red) / (nir + red)


def ndwi(green: xr.DataArray, nir: xr.DataArray) -> xr.DataArray:
    """Compute NDWI."""
    return (green - nir) / (green + nir)


def ndbi(swir: xr.DataArray, nir: xr.DataArray) -> xr.DataArray:
    """Compute NDBI."""
    return (swir - nir) / (swir + nir)
