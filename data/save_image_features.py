#!/usr/bin/env python3
import argparse
import csv
import numpy as np
from image_features import ImageEncoder

parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default='', type=str, help="Image path") #"C:/Users/samoj/Downloads/val2014/val2014/"
parser.add_argument("--cxc_file", default='', type=str, help="CxC file") #"C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv"
parser.add_argument("--output", default='', type=str, help="Output file")


def main(args):
    cc_file = np.array(list(csv.reader(
        open(args.cxc_file),
        delimiter=',')))[1:]
    image_names = np.unique(cc_file[:, 1])

    image_paths = [args.image_path + img for img in image_names]

    image_encoder = ImageEncoder()
    image_features = np.array(image_encoder.encode(image_paths))

    image_features = np.column_stack((np.array(image_names), image_features))

    with open(args.output, 'wb') as f:
        np.save(f, image_features)

if __name__ == '__main__':
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)