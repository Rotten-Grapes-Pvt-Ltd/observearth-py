# 🛰️ observearth-py
> Simplifying Earth Observation Data Access from Microsoft Planetary Computer  

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build](https://img.shields.io/badge/status-in%20development-orange.svg)]()

---

### 🌍 Overview

**observearth** is an open-source Python package designed to make it **extremely easy** to fetch, process, and export satellite imagery from the **Microsoft Planetary Computer (MPC)** and other STAC-compatible endpoints.

It provides a high-level, Pythonic interface for working with satellite datasets like **Sentinel-2** and **Landsat-8** — abstracting away all the complexity of STAC queries and raster handling.

---

## 🚀 Key Features

- 🛰 **Satellite Support** – Sentinel-2 and Landsat-8  
- 🔍 **STAC Search Made Simple** – Filter by date, cloud cover, and geometry  
- 🧮 **On-the-fly Index Computation** – NDVI, NDWI, NDBI (and more soon)  
- 💾 **Export Ready** – Save outputs as GeoTIFF or PNG with colormap  
- ⚡ **Modern Stack** – Built on `rioxarray`, `odc-stac`, and `planetary-computer`  
- 🔧 **Extensible** – Add new sensors and indices with minimal changes  

---

## 🧠 Why?

Interacting with STAC APIs and managing raster data is complex for non-developers.  
`observearth` aims to make that experience simple and intuitive — allowing researchers, GIS analysts, and developers to work with satellite data in **3–5 lines of Python**.

---

## 💡 Example Usage

```python
# Import package
import observearth as oe

# Initiate Satellite 
sat = oe.Sentinel2(product="2A") # 2A,2B,2C, all

# Define Geometry
geometry = {
    "type": "Polygon",
    "coordinates": [[[77.0, 23.0], [77.1, 23.0], [77.1, 23.1], [77.0, 23.1], [77.0, 23.0]]]
}

# Get List of Items
items = sat.search(
    start_date="2025-01-01",
    end_date="2025-01-31",
    cloud_cover=10,
    geom=geometry
)

# Process Index
ndvi = items.compute("NDVI")

# Get numerical output
print("Mean NDVI:", ndvi.mean().item())

# Get Graphical output
ndvi.export(type="tiff", path="./ndvi_output.tif", min=0, max=1, cmap="RdYlGn")
```

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-org>/observearth-py.git
cd observearth
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

### Dependencies

- `pystac-client`
- `planetary-computer`
- `odc-stac`
- `rioxarray`
- `xarray`
- `numpy`
- `matplotlib`

---

## 🧩 Package Architecture

```
observearth/
├── __init__.py
├── core/
│   ├── base_satellite.py
│   ├── items.py
│   ├── indices.py
│   ├── export.py
│   ├── utils.py
├── datasets/
│   ├── sentinel2.py
│   ├── landsat8.py
└── examples/
    └── sentinel2_ndvi_demo.ipynb
```

---

## 🧮 Supported Indices

| Index | Description | Required Bands |
|--------|--------------|----------------|
| **NDVI** | Normalized Difference Vegetation Index | NIR, RED |
| **NDWI** | Normalized Difference Water Index | NIR, GREEN |
| **NDBI** | Normalized Difference Built-up Index | SWIR, NIR |

---

## 🛰 Supported Datasets

| Satellite | Product | Collection Name |
|------------|----------|-----------------|
| Sentinel-2 | 2A / 2B / 2C / all | `sentinel-2-l2a` |
| Landsat-8  | - | `landsat-8-c2-l2` |

---

## 🧭 Roadmap

### v0.1.0 – MVP
- ✅ Sentinel-2 & Landsat-8 support  
- ✅ NDVI / NDWI / NDBI  
- ✅ TIFF & PNG export  
- ✅ Mean statistic  

### v0.2.0
- 🔧 Custom index expressions  
- 📦 Composite generation

### v0.3.0
- 🌧 Sentinel-1 (SAR) integration  
- 📊 RVI & VH/VV indices  

### v1.0.0
- 📚 Full documentation site  
- 🧩 PyPI release  
- 🧠 CLI tool for batch processing  

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch (`feature/sentinel1-support`)  
3. Commit your changes  
4. Submit a pull request 🚀

---

## 🧑‍💻 Maintainer

**Krishna Lodha**  
Founder & Director, [Rotten Grapes Pvt. Ltd.](https://rottengrapes.tech)  
Focused on Open-Source GIS & Earth Observation Development  

---

## 📄 License

MIT License © 2025 [Rotten Grapes Pvt. Ltd.](https://rottengrapes.tech)

---

### 🌟 Star this repo
If you find `observearth` useful, please consider starring the repo — it helps others discover the project!
