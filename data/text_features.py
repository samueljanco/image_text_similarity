import tensorflow_hub as hub
from tensorflow import keras
import numpy as np
import pickle

class TextEncoder:
    def __init__(self):
        # Load the model
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.custom_model = False

    def encode(self, text):
        return np.array(self.model(text))
