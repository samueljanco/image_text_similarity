#!/usr/bin/env python3
import argparse
import numpy as np
from tensorflow import keras
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--random_seed", default=42, type=int, help="Random seed")
parser.add_argument("--test_size", default=8000, type=int, help="Test data size")
parser.add_argument("--v_size", default=44723, type=int, help="Val data size")
parser.add_argument("--t_image_file", default='t_image_features.npy', type=str, help="Images path")
parser.add_argument("--t_text_file", default='t_text_embeddings.npy', type=str, help="Texts path")
parser.add_argument("--t_cxc_file", default='D:/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_test.csv', type=str, help="CxC file")
parser.add_argument("--model", default='similarity_model_1', type=str, help="Similarity model")

def transform_to_dictionary(arr):
    dict = {}
    for i in arr:
        dict[str(int(i[0]))] = i[1:]
    return dict

def prepare_data(image_file, text_file, cxc_file):
    with open(image_file, 'rb') as f:
        image_features = np.load(f)

    with open(text_file, 'rb') as f:
        text_embeddings = np.load(f)

    dict_image_features = transform_to_dictionary(image_features)
    dict_text_embeddings = transform_to_dictionary(text_embeddings)

    cxc = np.array(list(csv.reader(open(cxc_file), delimiter=',')))[1:]

    image_features = []
    for img in cxc[:, 1]:
        image_features.append(dict_image_features[str(int(img[13:-4]))])

    text_embeddings = []
    for txt in cxc[:, 0]:
        text_embeddings.append(dict_text_embeddings[txt[20:]])

    target = np.array([float(i) for i in cxc[:, 2]])

    return np.array(image_features), np.array(text_embeddings), target

def main(args):
    t_images, t_texts, t_targets = prepare_data(args.t_image_file, args.t_text_file, args.t_cxc_file)

    np.random.seed(args.random_seed)
    _ = np.random.permutation(args.v_size)
    t_sample = np.random.permutation(t_targets.shape[0])

    test_t_images, test_t_texts, test_t_target = (t_images[t_sample])[-args.test_size:], (t_texts[t_sample])[-args.test_size:], (t_targets[t_sample])[-args.test_size:]

    model = keras.models.load_model(args.model)
    model.evaluate([test_t_images, test_t_texts], test_t_target)


if __name__ == '__main__':
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)

