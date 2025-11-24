#!/usr/bin/env python3
import torch
import torchvision.models as models
import numpy as np
import subprocess
import os
import sys

CPPCONV = "./float_to_string"
OUTFILE = "mobilenetv3_large.txt"

TMPFILE = "mobilenetv3_large.bin"


def extract_mobilenetv3():
    print("Loading MobileNetV3-Large weights…", file=sys.stderr)
    model = models.mobilenet_v3_large(
        weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V2)
    sd = model.state_dict()

    floats = []
    for k, v in sd.items():
        if torch.is_floating_point(v):
            floats.append(v.reshape(-1).cpu().numpy().astype("float32"))

    arr = np.concatenate(floats)
    print(f"Saving {arr.size} floats to {TMPFILE}", file=sys.stderr)
    arr.tofile(TMPFILE)


def compile_cpp():
    print("Compiling C++ program…", file=sys.stderr)
    if not os.path.exists("float_to_string.cpp"):
        print("ERROR: float_to_string.cpp not found.", file=sys.stderr)
        sys.exit(1)

    cmd = ["g++", "-O3", "-o", "float_to_string", "float_to_string.cpp"]
    subprocess.check_call(cmd)

    print("Compilation done.", file=sys.stderr)


def run_float_to_string():
    print(f"Running float_to_string → {OUTFILE}", file=sys.stderr)

    if not os.path.exists(CPPCONV):
        print("ERROR: executable not found, compile failed?", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(TMPFILE):
        print("ERROR: binary weights file missing.", file=sys.stderr)
        sys.exit(1)

    with open(OUTFILE, "w") as out:
        subprocess.check_call([CPPCONV, TMPFILE], stdout=out)

    print(f"Removing temporary file {TMPFILE}", file=sys.stderr)
    os.remove(TMPFILE)


def main():
    extract_mobilenetv3()
    compile_cpp()
    run_float_to_string()


if __name__ == "__main__":
    main()
