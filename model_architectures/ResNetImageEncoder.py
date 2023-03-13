import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

class ResNetImageEncoder:
    def __init__(self):

        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    def encode(self, images):
        preprocessed_images = []
        for image in images:
            # Preprocess the image
            img = tf.keras.preprocessing.image.load_img(image,color_mode='rgb', target_size=(224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            preprocessed_images.append(preprocess_input(img_array))

        # Use the ResNet50 model to generate features
        features = self.model.predict(np.array(preprocessed_images))


        return features