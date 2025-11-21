# float-data — Numeric data examples

This repository contains a set of plain text files with numeric data samples. The files are stored in the `number_files/` directory.

Contents

- `number_files/` — directory containing the following files:
	- `number_files/canada.txt` — text extracted from a GeoJSON-style dataset representing geographic data for Canada (contains coordinates and feature attributes).
	- `number_files/marine_ik.txt` — numeric data related to a marine inverse-kinematics example (used for testing numeric parsing and algorithms).
	- `number_files/mesh.txt` — numeric representation of a 3D mesh (vertices, indices or related mesh data for testing mesh processing).
	- `number_files/numbers.txt` — a collection of numeric values ranging from 0 to 1, useful for tes
	- `number_files/bitcoin.txt` — daily close prices of bitcoin in USD from 2020-01-01 to 2022-07-31.

Quick usage

You can list or inspect the files with these shell commands:

```zsh
ls -l number_files/
head -n 30 number_files/canada.txt
```

## Citation

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
