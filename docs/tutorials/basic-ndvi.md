# Basic NDVI Tutorial

Learn how to calculate NDVI (Normalized Difference Vegetation Index) using ObserveEarth.

## What is NDVI?

NDVI measures vegetation health using the difference between near-infrared and red light reflection:

- **High NDVI (0.6-1.0)**: Dense, healthy vegetation
- **Medium NDVI (0.2-0.6)**: Moderate vegetation  
- **Low NDVI (0.0-0.2)**: Bare soil, urban areas
- **Negative NDVI**: Water bodies

## Step-by-Step Example

### 1. Import and Initialize

```python
import observearth as oe

# Initialize Sentinel-2 with product type
sat = oe.Sentinel2(product="2A")  # Options: 2A, 2B, 2C, all
```

### 2. Define Study Area

```python
# Small agricultural area in India
geometry = {
    "type": "Polygon",
    "coordinates": [[[77.0, 23.0], [77.05, 23.0], [77.05, 23.05], [77.0, 23.05], [77.0, 23.0]]]
}
```

### 3. Search for Images

```python
items = sat.search(
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_cover=20,  # Maximum 20% cloud cover
    geom=geometry
)

print(f"Found {len(items.items)} images")
```

### 4. Inspect Available Items

```python
# Check first few items
for i in range(min(3, len(items.items))):
    info = items.get_item_info(i)
    print(f"Item {i}: {info['datetime']} - Cloud: {info['cloud_cover']}%")
```

### 5. Compute NDVI

```python
# Process the first (best quality) item
ndvi = items.compute("NDVI", item_index=0)

# Get statistics
mean_ndvi = ndvi.mean()
print(f"Mean NDVI: {mean_ndvi:.3f}")
```

### 6. Export Results

```python
# Export as GeoTIFF for GIS software
ndvi.export(type="tiff", path="ndvi_result.tif")

# Export as PNG with vegetation colormap
ndvi.export(
    type="png", 
    path="ndvi_result.png", 
    min=0, max=1, 
    cmap="RdYlGn"  # Red-Yellow-Green colormap
)
```

## Complete Example

```python
import observearth as oe

def calculate_ndvi():
    # Initialize
    sat = oe.Sentinel2(product="2A")
    
    # Define area
    geometry = {
        "type": "Polygon",
        "coordinates": [[[77.0, 23.0], [77.05, 23.0], [77.05, 23.05], [77.0, 23.05], [77.0, 23.0]]]
    }
    
    # Search
    items = sat.search(
        start_date="2024-01-01",
        end_date="2024-01-31",
        cloud_cover=20,
        geom=geometry
    )
    
    if len(items.items) > 0:
        # Compute and export
        ndvi = items.compute("NDVI", item_index=0)
        ndvi.export(type="tiff", path="ndvi.tif")
        
        print(f"✅ NDVI calculated: {ndvi.mean():.3f}")
        return ndvi
    else:
        print("❌ No suitable images found")
        return None

# Run the example
result = calculate_ndvi()
```

## Interpreting Results

- **Forest/Dense Crops**: NDVI > 0.6
- **Grassland/Sparse Vegetation**: NDVI 0.2-0.6  
- **Bare Soil/Urban**: NDVI 0.0-0.2
- **Water**: NDVI < 0.0

## Next Steps

- [Multiple Indices Tutorial](multiple-indices.md)
- [Sentinel-2 vs Landsat Comparison](comparison.md)
- [API Reference](../api/satellites.md)