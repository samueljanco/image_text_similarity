import keras.models
from tensorflow import keras
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense
from image_features import ImageEncoder
from text_features import TextEncoder
import numpy as np
import csv

class SimilarityScore:
    def __init__(self,init_encoder=False, combine_via='multiplication'):
        image_input = Input(shape=(4096,))
        text_input = Input(shape=(512,))

        if combine_via == 'multiplication':
            x1 = Dense(256, activation='relu')(image_input)
            x2 = Dense(256, activation='relu')(text_input)
            x = keras.layers.multiply([x1, x2])
        elif combine_via == 'shared_layer':
            shared_dense_layer = keras.layers.Dense(64, activation='relu')
            x_1 = shared_dense_layer(image_input)
            x_2 = shared_dense_layer(text_input)
            x = keras.layers.concatenate([x_1, x_2])
        else:
            x_1 = keras.layers.Dense(64, activation='relu')(image_input)
            x_2 = keras.layers.Dense(64, activation='relu')(text_input)
            x = keras.layers.concatenate([x_1, x_2])

        x = keras.layers.Dense(128, activation='relu')(x)
        outputs = keras.layers.Dense(1, activation='linear')(x)

        self.model = Model(inputs=[image_input, text_input], outputs=outputs)
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        if init_encoder:
            self.image_encoder = ImageEncoder()
            self.text_encoder = TextEncoder()

    def fit(self, image_features, text_features, target):
        self.model.fit([image_features, text_features], target, epochs=70, batch_size=32)

    def fit_from_features(self, path):
        print("loading data")
        with open('coco_image_embeddings.npy', 'rb') as f:
            image_embeddings = np.load(f)

        with open('coco_text_embeddings.npy', 'rb') as f:
            text_embeddings = np.load(f)

        print("perparing data")
        dict_image_embeddings = self.transform_to_dictionary(image_embeddings)
        dict_text_embeddings = self.transform_to_dictionary(text_embeddings)

        cc_file = np.array(list(csv.reader(
            open(
                "C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv"),
            delimiter=',')))[1:]

        np.random.seed(42)
        sample = np.random.permutation(cc_file.shape[0])

        sampled_cc_file = cc_file[sample]

        train_captions = []
        for txt in sampled_cc_file[:, 0]:
            train_captions.append(dict_text_embeddings[txt[20:]])

        train_images = []
        for img in sampled_cc_file[:, 1]:
            train_images.append(dict_image_embeddings[str(int(img[13:-4]))])

        train_images = np.asarray(train_images)
        train_captions = np.asarray(train_captions)
        target = np.array([float(i) for i in sampled_cc_file[:, 2]])

        print('fitting')
        self.model.fit([train_images, train_captions], target, epochs=70, batch_size=32)
        self.model.save(path)

    def transform_to_dictionary(self, arr):
        dict = {}
        for i in arr:
            dict[str(int(i[0]))] = i[1:]
        return dict

    def predict_from_features(self, image_feature, text_feature):
        return self.model.predict([image_feature, text_feature])

    def predict(self, image_path, text):
        image_features = self.image_encoder.encode([image_path])[0]
        text_embeddings = self.text_encoder.encode([text])[0]
        return self.predict_from_features(image_features, text_embeddings)

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = keras.models.load_model(path)
