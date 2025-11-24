#!/bin/sh

wget https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20251120/00/atmos/gfs.t00z.pgrb2.1p00.f240
wgrib2 gfs.t00z.pgrb2.1p00.f240 -bin gfs.bin

g++ -O3 -o float_to_string float_to_string.cpp
./float_to_string gfs.bin | awk 'NR % 10 == 0' > noaa_gfs_1p00.txt

rm gfs.t00z.pgrb2.1p00.f240 gfs.bin
