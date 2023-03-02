#!/usr/bin/env python3
import argparse
import shutil
import os
import csv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--target", default='', type=str, help="Target")
parser.add_argument("--source", default='', type=str, help="Source")
parser.add_argument("--cxc_file", default='', type=str, help="CxC file")

def main(args):
    cc_file = np.array(list(csv.reader(
            open(args.cxc_file),
            delimiter=',')))[1:]
    image_names = np.unique(cc_file[:, 1])

    for fname in image_names:
        # copying the files to the destination directory
        shutil.copy2(os.path.join(args.source, fname), args.target)

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)