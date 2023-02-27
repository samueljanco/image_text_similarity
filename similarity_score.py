import keras.models
from tensorflow import keras
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense
from image_features import ImageEncoder
from text_features import TextEncoder

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
