#!/usr/bin/env python3
import csv
import sys
import re
import requests

TARGET = 1_000_000  # number of values to extract
YEAR = 2023
BASE = f"https://www.ncei.noaa.gov/data/global-hourly/access/{YEAR}/"
OUTFILE = "noaa_global_hourly_2023.txt"


def main():
    print("Downloading NOAA Global Hourly data...")
    idx = requests.get(BASE).text  # Download index
    files = re.findall(r'(\d{11}\.csv)', idx)  # Match 11-digit .csv filenames
    print(f"Found {len(files)} files. Extracting data...")

    count = 0
    with open(OUTFILE, "w") as out:
        for fname in files:
            url = BASE + fname
            with requests.get(url, stream=True) as r:
                r.raise_for_status()

                lines = (line.decode('utf-8') for line in r.iter_lines())
                reader = csv.reader(lines)

                fields = ['TMP', 'DEW', 'SLP', 'VIS']
                header = next(reader)
                idxs = [header.index(f) for f in fields if f in header]

                for row in reader:
                    for i in idxs:
                        raw = row[i]
                        if raw and "," in raw:
                            v = raw.split(",")[0]

                            # NOAA stores TMP like -0022 meaning –2.2°C
                            val = float(v) / 10.0
                            out.write(f"{val}\n")
                            count += 1

                            if count >= TARGET:
                                print(f"Wrote {count} floats to {OUTFILE}.")
                                sys.exit(0)


if __name__ == '__main__':
    main()
