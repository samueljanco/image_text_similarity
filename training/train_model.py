#!/usr/bin/env python3
import argparse
import keras.models
from tensorflow import keras
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense
import numpy as np
import csv


parser = argparse.ArgumentParser()
parser.add_argument("--v_image_file", default='v_image_features.npy', type=str, help="Images path")
parser.add_argument("--v_text_file", default='v_text_embeddings.npy', type=str, help="Texts path")
parser.add_argument("--v_cxc_file", default='D:/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv', type=str, help="CxC file")
parser.add_argument("--t_image_file", default='t_image_features.npy', type=str, help="Images path")
parser.add_argument("--t_text_file", default='t_text_embeddings.npy', type=str, help="Texts path")
parser.add_argument("--t_cxc_file", default='D:/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_test.csv', type=str, help="CxC file")
parser.add_argument("--output", default='similarity_model', type=str, help="Output file")


def transform_to_dictionary(arr):
    dict = {}
    for i in arr:
        dict[str(int(i[0]))] = i[1:]
    return dict

def build_model(combine_via = 'multiply'):
    image_input = Input(shape=(4096,))
    text_input = Input(shape=(512,))

    x1 = Dense(256, activation='relu')(image_input)
    x2 = Dense(256, activation='relu')(text_input)
    if combine_via == 'multiply':
        x = keras.layers.multiply([x1, x2])
    elif combine_via == 'add':
        x = keras.layers.add([x1, x2])
    else:
        x = keras.layers.concatenate([x1, x2])
        
    x = keras.layers.Dense(128, activation='relu')(x)
    outputs = keras.layers.Dense(1, activation='linear')(x)

    model = Model(inputs=[image_input, text_input], outputs=outputs)
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model

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

    v_images, v_texts, v_targets = prepare_data(args.v_image_file, args.v_text_file, args.v_cxc_file)
    t_images, t_texts, t_targets = prepare_data(args.t_image_file, args.t_text_file, args.t_cxc_file)

    np.random.seed(42)
    v_sample = np.random.permutation(v_targets.shape[0])
    t_sample = np.random.permutation(t_targets.shape[0])

    train_v_images, train_v_texts, train_v_target = v_images[v_sample], v_texts[v_sample], v_targets[v_sample]
    train_t_images, train_t_texts, train_t_target = (t_images[t_sample])[:-8000], (t_texts[t_sample])[:-8000], (t_targets[t_sample])[:-8000]

    train_images = np.concatenate((train_v_images, train_t_images), axis=0)
    train_texts = np.concatenate((train_v_texts, train_t_texts), axis=0)
    train_targets = np.concatenate((train_v_target, train_t_target), axis=0)

    model = build_model()
    model.fit([train_images, train_texts], train_targets, epochs=70, batch_size=32)
    model.save(args.output)


if __name__ == '__main__':
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)

