# float-data — Diverse Floating-Point Datasets

This repository provides a diverse suite of **real-world** and **synthetic**
floating-point datasets designed for benchmarking numeric parsing and
string-conversion algorithms.

All datasets are stored as **plain text**, one numeric value per line, making
them easy to inspect and reproducible across systems.

The goal of this dataset collection is to provide a **representative, diverse,
and challenging benchmark corpus** mirroring the numeric values commonly
encountered in practice—ranging from geospatial data, scientific simulations,
astronomy catalogs, financial time series, and machine-learning model weights,
up to pathological IEEE-754 edge cases. Only two datasets (`numbers.txt` and
`hellfloat64.txt`) are synthetic, serving well-defined roles: a simple uniform
baseline and a comprehensive stress-test for string-conversion algorithms.

---

# 📦 Dataset Overview

Below is a detailed description of each dataset, including the type of numeric
values they contain and typical real-world scenarios they represent.

## 🌎 `canada.txt` — Geospatial Coordinates (FP64)
- Extracted from the GeoJSON dataset of geographic features.
- Contains latitude, longitude, elevations, and associated attributes.
- Representative of **GIS pipelines**, navigation systems, and open-data APIs.

## 🐟 `marine_ik.txt` — Inverse Kinematics (FP32)
- Numeric values from a marine robotics inverse-kinematics example.
- Contains small real numbers (between -1 and 4.4) from a physical simulation.
- Typical of **control systems** and **scientific computing** workloads.

## 🧱 `mesh.txt` — 3D Mesh Geometry (FP64)
- Vertex coordinates and related mesh data from a triangulated 3D surface.
- Similar to formats used in CAD, graphics engines, and scientific visualization.
- Heavy on **small numbers** (between -1 and 3), but realistic and widespread.

## 🪙 `bitcoin.txt` — Historical Market Data (FP64)
- Daily closing prices of Bitcoin (USD), from 2020-01-01 to 2022-07-31.
- Representative of **financial APIs**, trading systems, and real-time dashboards.

## 🎲 `numbers.txt` — Uniform Random in [0,1] (FP64)
- Synthetic baseline dataset.
- Useful for comparisons but **not intended** to represent real-world patterns.

## 🤖 `mobilenetv3_large.txt` — Deep Learning Model Weights (FP32)
- Serialized weights of the [MobileNetV3-Large](https://research.google/blog/introducing-the-next-generation-of-on-device-vision-models-mobilenetv3-and-mobilenetedgetpu/) ImageNet model.
- Contains millions of FP32 values (both small and moderately large), typical of:
  - neural networks,
  - gradient updates,
  - machine-learning pipelines.

## ✨ `gaia.txt` — Astrometric & Photometric Data (FP64)
- Extracted from [ESA Gaia DR3](https://www.cosmos.esa.int/web/gaia/dr3).
- Includes:
  - right ascension / declination,  
  - parallax, proper motions,  
  - photometric fluxes,  
  - galactic & ecliptic coordinates.
- True scientific dataset with **large dynamic range**, typical of astronomy and big-science archives.

## 🌤️ `noaa_global_hourly_2023.txt` — Weather Station Measurements (FP32)
- [NOAA NCEI “Global Hourly”](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database) dataset (temperature, dew point, visibility, pressure).
- Extremely common real-world data format: noisy, irregular, and API-like.

## 🌍 `noaa_gfs_1p00.txt` — Global Forecast System Model Output (FP32)
- Extracted from [NOAA GFS](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast) model GRIB2 files.
- Contains fields such as geopotential height, temperature, humidity, pressure, wind components.
- True **scientific FP32** with meaningful numerical variety and scaling.

## 🔥 `hellfloat64.txt` — Synthetic IEEE-754 Stress-Test (FP64)
A custom-built dataset designed to **stress special values**.  
Contains:
- subnormals,  
- powers of two across the full range,  
- powers of ten in ±308,  
- values near rounding boundaries,  
- extreme magnitudes,  
- structured edge cases (±0, EPS, min/max normal/subnormal),  
- log-distributed extreme values.

This dataset is purely synthetic and intended as a **worst-case test harness**.

---

# ⚙️ Reproducibility and Regeneration

Several datasets can be regenerated automatically using the scripts found in
the `scripts/` directory. All Python dependencies are managed using
[uv](https://github.com/astral-sh/uv).

Example commands:

```bash
cd scripts
uv sync
./noaa_gfs_1p00.sh
uv run ./noaa_global_hourly_f32.py
uv run ./gaia.py
uv run ./mobilenetv3.py
uv run ./hellfloat64.py
```

# 📖 Quick usage

You can list or inspect the files with these shell commands:

```zsh
ls -l number_files/
head -n 30 number_files/canada.txt
wc -l number_files/gaia.txt
```

## 📚 Citation

If you use this dataset in research or a publication, please cite it.

Example BibTeX entry:

```bibtex
@misc{float-data,
  title = {float-data: A collection of floating-point numbers},
  author = {Jaël Champagne Gareau and Daniel Lemire},
  year = {2025},
  howpublished = {\url{https://github.com/fastfloat/float-data}}
}
```
