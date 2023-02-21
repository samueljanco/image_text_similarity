import keras.models
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Concatenate
from image_features import ImageEncoder
from text_features import TextEncoder

class SimilarityScore:
    def __init__(self):
        image_input = Input(shape=(4096,))
        text_input = Input(shape=(512,))

        x1 = Dense(64, activation='relu')(image_input)
        x2 = Dense(64, activation='relu')(text_input)
        x = Concatenate()([x1, x2])
        output = Dense(1, activation='sigmoid')(x)

        self.model = Model(inputs=[image_input, text_input], outputs=output)
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.image_encoder = ImageEncoder()
        self.text_encoder = TextEncoder()

    def fit(self, image_features, text_features, target):
        self.model.fit([image_features, text_features], target, epochs=10, batch_size=32)

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