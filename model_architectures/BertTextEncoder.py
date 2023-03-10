import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Input
from transformers import BertTokenizer, TFBertModel

class BertTextEncoder:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = TFBertModel.from_pretrained('bert-base-uncased')
        self.max_len = self.bert_model.config.max_position_embeddings

    def encode(self, text_list, batch_size=32):

        tokenized_text = [self.tokenizer.encode(text, add_special_tokens=True) for text in text_list]


        padded_text = tf.keras.preprocessing.sequence.pad_sequences(tokenized_text,
                                                                    padding='post')

        bert_model = TFBertModel.from_pretrained('bert-base-uncased')

        embeddings = []
        for i in range(0, len(padded_text), batch_size):
            inputs = {
                'input_ids': padded_text[i:i + batch_size],
                'attention_mask': tf.where(padded_text[i:i + batch_size] != 0, 1, 0),
                'token_type_ids': tf.zeros_like(padded_text[i:i + batch_size])
            }
            batch_embeddings = bert_model(inputs)[1].numpy()
            embeddings.append(batch_embeddings)

        embeddings = np.concatenate(embeddings, axis=0)

        return embeddings






