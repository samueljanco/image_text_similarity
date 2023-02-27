import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
import numpy as np

class TextEncoder:
    def __init__(self):
        # Load the pre-trained BERT model and tokenizer
        self.bert_model = TFBertModel.from_pretrained('bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')



    def encode(self, text_list, batch_size=32):
        
        tokenized_text = [self.tokenizer.encode(text, add_special_tokens=True) for text in text_list]


        max_length = max([len(text) for text in tokenized_text])
        padded_text = tf.keras.preprocessing.sequence.pad_sequences(tokenized_text, maxlen=max_length, padding='post')

   
        embeddings = []
        for i in range(0, len(padded_text), batch_size):
            inputs = {
                'input_ids': padded_text[i:i+batch_size],
                'attention_mask': tf.where(padded_text[i:i+batch_size] != 0, 1, 0),
                'token_type_ids': tf.zeros_like(padded_text[i:i+batch_size])
            }
            batch_embeddings = self.bert_model(inputs)[1].numpy()
            embeddings.append(batch_embeddings)
        embeddings = np.concatenate(embeddings, axis=0)

        return embeddings
