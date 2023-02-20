from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Concatenate

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

    def fit(self, image_features, text_features, target):
        self.model.fit([image_features, text_features], target, epochs=10, batch_size=32)

    def predict(self, image_feature, text_feature):
        return self.model.predict([image_feature, text_feature])

    def save_model(self, path):
        self.model.save(path)