import tensorflow_hub as hub
import numpy as np

class TextEncoder:
    def __init__(self):
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def encode(self, text, pretrained = True):
        return self._encode_pretrained(text) if pretrained else self._encode_custom(text)

    def _encode_pretrained(self, text):
        return np.array(self.model(text))

    def _encode_custom(self, text):
        pass

    def fit_custom(self):
        pass

