#!/usr/bin/env python3
import argparse
import numpy as np
from tensorflow import keras
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--image_features_path", default='test_image_features.npy', type=str, help="Images path")
parser.add_argument("--text_embeddings_path", default='test_text_embeddings.npy', type=str, help="Texts path")
parser.add_argument("--cxc_file", default='C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_test.csv', type=str, help="CxC file")
parser.add_argument("--model", default='similarity_model', type=str, help="Similarity model")

def transform_to_dictionary(arr):
    dict = {}
    for i in arr:
        dict[str(int(i[0]))] = i[1:]
    return dict

def main(args):
    print("loading data...")
    with open(args.image_features_path, 'rb') as f:
        image_embeddings = np.load(f)

    with open(args.text_embeddings_path, 'rb') as f:
        text_embeddings = np.load(f)

    print("perparing data...")
    dict_image_embeddings = transform_to_dictionary(image_embeddings)
    dict_text_embeddings = transform_to_dictionary(text_embeddings)

    cc_file = np.array(list(csv.reader(
        open(args.cxc_file),
        delimiter=',')))[1:]

    np.random.seed(42)
    sample = np.random.permutation(cc_file.shape[0])

    sampled_cc_file = cc_file[sample]

    train_captions = []
    for txt in sampled_cc_file[:, 0]:
        train_captions.append(dict_text_embeddings[txt[20:]])


    train_images = []
    for img in sampled_cc_file[:,1]:
        train_images.append(dict_image_embeddings[str(int(img[13:-4]))])

    train_images = np.asarray(train_images)
    train_captions = np.asarray(train_captions)
    target = np.array([float(i) for i in sampled_cc_file[:,2]])

    print('evaluating...')
    model = keras.models.load_model(args.model)
    model.evaluate([train_images, train_captions], target)


if __name__ == '__main__':
    main()
