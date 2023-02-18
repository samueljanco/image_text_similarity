import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import csv
import json

"""
Returns captions not used for training the similarity score model
"""
def get_captions():
    # Load CxC csv
    cc_file = np.array(list(csv.reader(
        open("C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv"),
        delimiter=',')))[1:]

    # Get ids of captions
    caption_names = np.unique(cc_file[:, 0])
    caption_ids = [int(c[20:]) for c in caption_names]

    # Load captions
    json_captions = json.load(open("C:/Users/samoj/Downloads/dataset_coco.json/dataset_coco.json"))

    # Get captions not used in CxC dataset
    caption_texts = []
    for img in json_captions['images']:
        for sentence in img['sentences']:
            if sentence['sentid'] not in caption_ids:
                caption_texts.append(sentence['raw'])


    return caption_texts

def main():
    # Download the pre-trained USE model
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    use_layer = hub.KerasLayer(module_url, trainable=False)

    # Load and preprocess your smaller corpus
    corpus = get_captions()

    # Create a new model that includes the USE encoder layer
    input_text = tf.keras.layers.Input(shape=(), dtype=tf.string)
    embedding = use_layer(input_text)
    dense = tf.keras.layers.Dense(128, activation='relu')(embedding)
    output = tf.keras.layers.Dense(512, activation='softmax')(dense)
    model = tf.keras.Model(inputs=input_text, outputs=output)

    # Train the model using transfer learning
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(corpus, epochs=10, validation_data=0.1)

    model.save('word_embeddings')


if __name__ == '__main__':
    main()