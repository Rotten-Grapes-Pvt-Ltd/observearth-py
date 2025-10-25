# Quick Start

Get started with ObserveEarth in 5 minutes.

## Basic NDVI Calculation

```python
import observearth as oe

# Initialize Sentinel-2
sat = oe.Sentinel2(product="2A")

# Define area of interest
geometry = {
    "type": "Polygon",
    "coordinates": [[[77.0, 23.0], [77.1, 23.0], [77.1, 23.1], [77.0, 23.1], [77.0, 23.0]]]
}

# Search for images
items = sat.search(
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_cover=10,
    geom=geometry
)

# Compute NDVI for first item
ndvi = items.compute("NDVI", item_index=0)
print(f"Mean NDVI: {ndvi.mean():.3f}")

# Export results
ndvi.export(type="tiff", path="ndvi.tif")
```

## Key Concepts

- **Single Item Processing**: Each `compute()` call processes one satellite image
- **Geometry Clipping**: Data is automatically clipped to your area of interest
- **Index Selection**: Choose from NDVI, NDWI, NDBI indices

## Next Steps

- [Multiple Indices Tutorial](../tutorials/multiple-indices.md)
- [API Reference](../api/satellites.md)