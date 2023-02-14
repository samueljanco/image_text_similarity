import tensorflow_hub as hub
from tensorflow import keras
import numpy as np
import pickle

class TextEncoder:
    def __init__(self, model_path=""):
        if model_path != "":
            # Load the model
            self.model = keras.models.load_model(model_path)

            # Load the tokenizer
            with open('tokenizer.pickle', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            self.custom_model = True
        else:
            # Load the model
            self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
            self.custom_model = False

    def encode(self, text):
        return self._encode_pretrained(text) if self.custom_model else self._encode_custom(text)

    def _encode_pretrained(self, text):
        return np.array(self.model(text))

    def _encode_custom(self, text):
        return  self.model.predict(self.tokenizer.texts_to_sequences([text]))

