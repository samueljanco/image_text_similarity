import keras.models
from tensorflow import keras
from image_features import ImageEncoder
from text_features import TextEncoder

class SimilarityScore:
    def __init__(self, model_path='similarity_model'):
        self.MAX = 5
        self.image_encoder = ImageEncoder()
        self.text_encoder = TextEncoder()
        self.similarity_model = keras.models.load_model(model_path)

    def predict(self, image_path, text):
        image_features = self.image_encoder.encode([image_path])[0]
        text_embeddings = self.text_encoder.encode([text])[0]
        prediction = self.similarity_model.predict([image_features.reshape(1,-1), text_embeddings.reshape(1,-1)])[0]
        return prediction

    def preprocess_text(self, text):
        return text.replace('\n', ' ').replace('\r', '')

    def get_percentage(self, score):
        return (100/self.MAX) * score

    def compare(self, image_path, text):
        prep_text = self.preprocess_text(text)
        score = self.predict(image_path, prep_text)
        result = self.get_percentage(score)
        return result


