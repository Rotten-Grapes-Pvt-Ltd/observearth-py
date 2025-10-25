# 🛰️ ObserveEarth

> Simplifying Earth Observation Data Access from Microsoft Planetary Computer

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue.svg)](https://python-poetry.org/)

---

## Overview

**ObserveEarth** is a Python package that makes it **extremely easy** to fetch, process, and export satellite imagery from the **Microsoft Planetary Computer (MPC)** and other STAC-compatible endpoints.

It provides a high-level, Pythonic interface for working with satellite datasets like **Sentinel-2** and **Landsat-8** — abstracting away all the complexity of STAC queries and raster handling.

## Key Features

- 🛰 **Satellite Support** – Sentinel-2 and Landsat-8  
- 🔍 **STAC Search Made Simple** – Filter by date, cloud cover, and geometry  
- 🧮 **On-the-fly Index Computation** – NDVI, NDWI, NDBI (and more soon)  
- 💾 **Export Ready** – Save outputs as GeoTIFF or PNG with colormap  
- ⚡ **Modern Stack** – Built on `rioxarray`, `odc-stac`, and `planetary-computer`  
- 🔧 **Extensible** – Add new sensors and indices with minimal changes  

## Quick Example

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
    start_date="2025-01-01",
    end_date="2025-01-31",
    cloud_cover=10,
    geom=geometry
)

# Compute NDVI for first item
ndvi = items.compute("NDVI", item_index=0)
print(f"Mean NDVI: {ndvi.mean():.3f}")

# Export results
ndvi.export(type="tiff", path="ndvi.tif")
ndvi.export(type="png", path="ndvi.png", min=0, max=1, cmap="RdYlGn")
```

## Supported Indices

| Index | Description | Required Bands |
|--------|--------------|----------------|
| **NDVI** | Normalized Difference Vegetation Index | NIR, RED |
| **NDWI** | Normalized Difference Water Index | NIR, GREEN |
| **NDBI** | Normalized Difference Built-up Index | SWIR, NIR |

## Supported Datasets

| Satellite | Product | Collection Name |
|------------|----------|-----------------|
| Sentinel-2 | 2A / 2B / 2C / all | `sentinel-2-l2a` |
| Landsat-8  | - | `landsat-8-c2-l2` |

## Getting Started

1. **[Installation](getting-started/installation.md)** - Install ObserveEarth with Poetry
2. **[Quick Start](getting-started/quick-start.md)** - Your first NDVI calculation
3. **[Tutorials](tutorials/basic-ndvi.md)** - Step-by-step guides

## Contributing

We welcome contributions! See our [Contributing Guide](contributing/setup.md) to get started.

## License

MIT License © 2025 [Rotten Grapes Pvt. Ltd.](https://rottengrapes.tech)