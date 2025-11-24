#!/usr/bin/env python3
import csv
import gzip
import requests
import sys

URL = "https://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/GaiaSource_765325-765403.csv.gz"
OUTFILE = "gaia.txt"

# Some float64 columns from Gaia (as per ECSV metadata)
FP64_COLS = [
    "ra",
    "dec",
    "parallax",
    "pmra",
    "pmdec",
    "phot_g_mean_flux",
    "phot_bp_mean_flux",
    "phot_rp_mean_flux",
]


def main():
    print(f"Downloading: {URL}", file=sys.stderr)
    r = requests.get(URL, stream=True)
    r.raise_for_status()

    with open(OUTFILE, "w") as out:
        gz = gzip.GzipFile(fileobj=r.raw)
        reader = csv.DictReader((line.decode("utf-8", errors="ignore")
                                 for line in gz if not line.startswith(b"#")))

        count = 0
        for row in reader:
            for col in FP64_COLS:
                v = row.get(col, "")
                if v and v.lower() != "null":
                    out.write(v + "\n")
                    count += 1

        print(f"Done. Wrote {count} floats to {OUTFILE}", file=sys.stderr)


if __name__ == "__main__":
    main()
