#!/usr/bin/env python3
import argparse
import keras.models
from tensorflow import keras
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense
import numpy as np
import csv


parser = argparse.ArgumentParser()
parser.add_argument("--image_features_path", default='coco_image_embeddings.npy', type=str, help="Images path")
parser.add_argument("--text_embeddings_path", default='coco_text_embeddings.npy', type=str, help="Texts path")
parser.add_argument("--cxc_file", default='C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv', type=str, help="CxC file") #""
parser.add_argument("--output", default='similarity_model', type=str, help="Output file")


def transform_to_dictionary(arr):
    dict = {}
    for i in arr:
        dict[str(int(i[0]))] = i[1:]
    return dict

def build_model():
    image_input = Input(shape=(4096,))
    text_input = Input(shape=(512,))

    x1 = Dense(256, activation='relu')(image_input)
    x2 = Dense(256, activation='relu')(text_input)
    x = keras.layers.multiply([x1, x2])
    x = keras.layers.Dense(128, activation='relu')(x)
    outputs = keras.layers.Dense(1, activation='linear')(x)

    model = Model(inputs=[image_input, text_input], outputs=outputs)
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model

def main(args):
    with open(args.image_features_path, 'rb') as f:
        image_embeddings = np.load(f)

    with open(args.text_embeddings_path, 'rb') as f:
        text_embeddings = np.load(f)

    dict_image_embeddings = transform_to_dictionary(image_embeddings)
    dict_text_embeddings = transform_to_dictionary(text_embeddings)

    cc_file = np.array(list(csv.reader(open(args.cxc_file), delimiter=',')))[1:]

    np.random.seed(42)
    sample = np.random.permutation(cc_file.shape[0])
    sampled_cc_file = cc_file[sample]

    train_captions = []
    for txt in sampled_cc_file[:, 0]:
        train_captions.append(dict_text_embeddings[txt[20:]])

    train_images = []
    for img in sampled_cc_file[:,1]:
        train_images.append(dict_image_embeddings[str(int(img[13:-4]))])

    image_features = np.asarray(train_images)
    text_features = np.asarray(train_captions)
    target = np.array([float(i) for i in sampled_cc_file[:,2]])

    print('fitting')
    model = build_model()
    model.fit([image_features, text_features], target, epochs=70, batch_size=32)
    model.save(args.output)


if __name__ == '__main__':
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)


