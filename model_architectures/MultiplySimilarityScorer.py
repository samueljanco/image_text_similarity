#!/usr/bin/env python3
import keras.models
from tensorflow import keras
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense
from SimilarityScorer import SimilarityScorer


class MultiplySimilarityScorer(SimilarityScorer):
    def __int__(self, img_size, txt_size, v_images, t_images, v_texts, t_texts, v_cxc, t_cxc, epochs = 70, batch_size = 32, test_size = 8000, random_seed = 42):

        super().__init__(v_images, t_images, v_texts, t_texts, v_cxc, t_cxc, epochs,  batch_size, test_size, random_seed)

        image_input = Input(shape=(img_size,))
        text_input = Input(shape=(txt_size,))

        x1 = Dense(256, activation='relu')(image_input)
        x2 = Dense(256, activation='relu')(text_input)
        x = keras.layers.multiply([x1, x2])
        x = keras.layers.Dense(128, activation='relu')(x)
        outputs = keras.layers.Dense(1, activation='linear')(x)

        self.model = Model(inputs=[image_input, text_input], outputs=outputs)
        self.model.compile(optimizer='adam', loss='mean_squared_error')


