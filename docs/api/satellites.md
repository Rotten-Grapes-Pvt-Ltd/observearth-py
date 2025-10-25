# Satellites API

API reference for satellite classes and methods.

## Sentinel2

::: observearth.datasets.sentinel2.Sentinel2

### Usage

```python
import observearth as oe

# Initialize with product type
sat = oe.Sentinel2(product="2A")  # 2A, 2B, 2C, or all

# Search for items
items = sat.search(
    start_date="2024-01-01",
    end_date="2024-01-31", 
    cloud_cover=10,
    geom=geometry
)
```

### Product Types

- **2A**: Level-2A (atmospherically corrected)
- **2B**: Level-2B (enhanced processing)  
- **2C**: Level-2C (additional corrections)
- **all**: Search all product types

## Landsat8

::: observearth.datasets.landsat8.Landsat8

### Usage

```python
# Initialize Landsat-8
sat = oe.Landsat8()

# Search (same interface as Sentinel-2)
items = sat.search(
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_cover=15,
    geom=geometry
)
```

## SatelliteItems

::: observearth.core.items.SatelliteItems

### Key Methods

#### compute()
Process a single satellite item to calculate vegetation indices.

```python
# Compute NDVI for first item
ndvi = items.compute("NDVI", item_index=0)

# Compute NDWI for second item  
ndwi = items.compute("NDWI", item_index=1)
```

#### get_item_info()
Get metadata about a specific item.

```python
info = items.get_item_info(0)
print(f"Date: {info['datetime']}")
print(f"Cloud cover: {info['cloud_cover']}%")
```

## RasterData

::: observearth.core.items.RasterData

### Methods

#### mean()
Calculate mean value of the raster.

```python
mean_value = ndvi.mean()
```

#### export()
Export raster to file.

```python
# Export as GeoTIFF
ndvi.export(type="tiff", path="output.tif")

# Export as PNG with colormap
ndvi.export(type="png", path="output.png", min=0, max=1, cmap="RdYlGn")
```