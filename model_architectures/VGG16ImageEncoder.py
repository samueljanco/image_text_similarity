import tensorflow as tf
from keras.applications.vgg16 import VGG16
import numpy as np


class VGG16ImageEncoder:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = tf.keras.models.Sequential(base_model.layers[:-1])

    def encode(self, images):
        features = []
        for image in images:
            img = tf.keras.preprocessing.image.load_img(image, color_mode='rgb', target_size=(224, 224))
            x = tf.keras.preprocessing.image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.vgg16.preprocess_input(x)
            f = self.model.predict(x)
            features.append(f.reshape(-1))

        return np.array(features)
