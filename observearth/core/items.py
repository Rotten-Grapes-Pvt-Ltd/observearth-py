"""Handles STAC items and index computation."""

import datetime
from typing import Any, Dict, List, Optional

import odc.stac
import rioxarray
import shapely.geometry
import xarray as xr

from .indices import compute_index


def harmonised(xx):
    """Harmonize Sentinel-2 data for processing baseline change."""
    cutoff = datetime.datetime(2022, 1, 25)
    offset = 1000
    new = xx.sel(time=slice(cutoff, None))
    if len(new.time) > 1:
        old = xx.sel(time=slice(None, cutoff))
        new_harmonized = xx.sel(time=slice(cutoff, None)).clip(offset)
        new_harmonized -= offset
        final = xr.concat([old, new_harmonized], dim="time")
        return final
    else:
        return xx


class RasterData:
    """Wrapper for computed raster data."""

    def __init__(self, data: xr.DataArray):
        """Initialize with xarray DataArray."""
        self.data = data

    def mean(self) -> float:
        """Calculate mean value of the raster."""
        return float(self.data.mean().compute().values.item())

    def export(
        self,
        type: str,
        path: str,
        min: float = None,
        max: float = None,
        cmap: str = "viridis",
    ) -> None:
        """
        Export raster data to file.

        Args:
            type: Export type ('tiff' or 'png')
            path: Output file path
            min: Minimum value for scaling
            max: Maximum value for scaling
            cmap: Colormap for PNG export
        """
        from .export import export_raster

        export_raster(self.data, type, path, min, max, cmap)


class SatelliteItems:
    """Container for STAC items with processing capabilities."""

    def __init__(
        self,
        items: List[Any],
        collection_id: str,
        geometry: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize with STAC items.

        Args:
            items: List of STAC items
            collection_id: Collection identifier
            geometry: GeoJSON geometry for clipping
        """
        self.items = items
        self.collection_id = collection_id
        self.geometry = geometry
        self._band_mapping = self._get_band_mapping()

    def _get_band_mapping(self) -> Dict[str, str]:
        """Get band mapping for the collection."""
        if "sentinel-2" in self.collection_id:
            return {
                "RED": "B04",
                "GREEN": "B03",
                "BLUE": "B02",
                "NIR": "B08",
                "SWIR": "B11",
            }
        elif "landsat" in self.collection_id:
            return {
                "RED": "red",
                "GREEN": "green",
                "BLUE": "blue",
                "NIR": "nir08",
                "SWIR": "swir16",
            }
        return {}

    def compute(self, index_name: str, item_index: int = 0) -> RasterData:
        """
        Compute vegetation/water index for a single item with geometry clipping.

        Args:
            index_name: Name of index to compute (NDVI, NDWI, NDBI)
            item_index: Index of the item to process (default: 0)

        Returns:
            RasterData object with computed and clipped index
        """
        if not self.items:
            raise ValueError("No items available for computation")

        if item_index >= len(self.items):
            raise ValueError(
                f"Item index {item_index} out of range. Available items: {len(self.items)}"
            )

        # Get single item
        item = self.items[item_index]

        # Determine required bands for the index
        required_bands = self._get_required_bands(index_name)
        band_names = [self._band_mapping[band] for band in required_bands]

        # Load data using odc-stac for single item
        load_params = {
            "items": [item],
            "groupby": "solar_day",
            "chunks": {"x": 2048, "y": 2048},
            "resolution": 5,
        }

        # Add geometry for initial loading if available
        if self.geometry is not None:
            geom_shape = shapely.geometry.shape(self.geometry)
            load_params["geopolygon"] = geom_shape

        data = odc.stac.load(**load_params)

        # Apply additional clipping if geometry is provided
        if self.geometry is not None:
            dc = data.rio.clip([self.geometry], crs="epsg:4326")
            # dc = harmonised(dc_nonharmonised).compute()
            # dc = (dc_nonharmonised).compute()
        else:
            # dc = harmonised(data).compute()
            dc = (data).compute()

        # # Extract bands and apply harmonization for Sentinel-2
        bands = {band: dc[self._band_mapping[band]] for band in required_bands}

        # if "sentinel-2" in self.collection_id:
        #     harmonized_bands = {}
        #     for band_name, band_data in bands.items():
        #         harmonized_bands[band_name] = harmonised(band_data)
        #     bands = harmonized_bands

        # Compute index
        index = compute_index(index_name, **bands)

        return RasterData(index)

    def _get_required_bands(self, index_name: str) -> List[str]:
        """Get required bands for an index."""
        index_bands = {
            "NDVI": ["RED", "NIR"],
            "NDWI": ["GREEN", "NIR"],
            "NDBI": ["SWIR", "NIR"],
        }

        if index_name not in index_bands:
            raise ValueError(f"Unknown index: {index_name}")

        return index_bands[index_name]

    def get_item_info(self, item_index: int = 0) -> Dict[str, Any]:
        """
        Get information about a specific item.

        Args:
            item_index: Index of the item to get info for

        Returns:
            Dictionary with item information
        """
        if not self.items or item_index >= len(self.items):
            return {}

        item = self.items[item_index]
        return {
            "id": item.id,
            "datetime": item.datetime.isoformat() if item.datetime else None,
            "cloud_cover": item.properties.get("eo:cloud_cover"),
            "platform": item.properties.get("platform"),
            "bbox": item.bbox,
        }
