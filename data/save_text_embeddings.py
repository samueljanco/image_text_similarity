#!/usr/bin/env python3
import argparse
import csv
import numpy as np
from text_features import TextEncoder
import json

parser = argparse.ArgumentParser()
parser.add_argument("--caption_file", default='', type=str, help="Caption file") #"C:/Users/samoj/Downloads/dataset_coco.json/dataset_coco.json"
parser.add_argument("--cxc_file", default='', type=str, help="CxC file") #"C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv"
parser.add_argument("--output", default='', type=str, help="Output file")


def main(args):
    cc_file = np.array(list(csv.reader(
        open(args.cxc_file),
        delimiter=',')))[1:]
    caption_names = np.unique(cc_file[:, 0])
    caption_ids = [int(c[20:]) for c in caption_names]
    json_captions = json.load(open(args.caption_file))
    caption_texts = []
    caption_sentids = []

    for img in json_captions['images']:
        for sentence in img['sentences']:
            if sentence['sentid'] in caption_ids:
                caption_sentids.append(sentence['sentid'])
                caption_texts.append(sentence['raw'])

    caption_sentids = np.array(caption_sentids)
    text_encoder = TextEncoder()
    text_features = np.array(text_encoder.encode(caption_texts))

    text_features = np.column_stack((caption_sentids, text_features))

    with open(args.output, 'wb') as f:
        np.save(f, text_features)

if __name__ == '__main__':
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)