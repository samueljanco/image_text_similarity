import numpy as np
import tensorflow_hub as hub

class TextEncoder:
    def __init__(self):
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def encode(self, texts):
        return np.array(self.model(texts))

