from tensorflow import keras
import numpy as np
import csv
import json
import pickle

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
    # Load the corpus
    corpus = get_captions()

    # Tokenize the text data
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(corpus)
    sequences = tokenizer.texts_to_sequences(corpus)


    # Padding the sequences to the same length
    padded_sequences = keras.preprocessing.sequence.pad_sequences(sequences)

    # Create an embedding layer
    embedding_dim = 512
    embedding_layer = keras.layers.Embedding(input_dim=tokenizer.num_words, output_dim=embedding_dim)

    # Build the model
    model = keras.Sequential([
        embedding_layer,
    ])

    # Compile the model
    model.compile(optimizer="adam", loss="mse")

    # Train the model
    model.fit(padded_sequences, padded_sequences, epochs=10, batch_size=32)

    # Save the tokenizer
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Save the model
    model.save('word_embeddings')


if __name__ == '__main__':
    main()