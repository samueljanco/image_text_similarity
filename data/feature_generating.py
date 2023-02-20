import csv
import json
import numpy as np
from image_features import  ImageEncoder
from text_features import TextEncoder

def save_image_features():
    cc_file = np.array(list(csv.reader(
        open("C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv"),
        delimiter=',')))[1:]
    image_names = np.unique(cc_file[:, 1])

    path = "C:/Users/samoj/Downloads/val2014/val2014/"
    image_paths = [path + img for img in image_names]

    image_encoder = ImageEncoder()
    image_features = np.array(image_encoder.encode(image_paths))

    image_features = np.column_stack((np.array(image_names), image_features))

    with open('coco_image_embeddings.npy', 'wb') as f:
        np.save(f, image_features)

 
def save_text_features():
    cc_file = np.array(list(csv.reader(
        open("C:/Users/samoj/Downloads/Crisscrossed-Captions-master/Crisscrossed-Captions-master/data/sits_val.csv"),
        delimiter=',')))[1:]
    caption_names = np.unique(cc_file[:, 0])
    caption_ids = [int(c[20:]) for c in caption_names]
    json_captions = json.load(open("C:/Users/samoj/Downloads/dataset_coco.json/dataset_coco.json"))
    caption_texts = []
    caption_sentids = []

    for img in json_captions['images']:
        for sentence in img['sentences']:
            if sentence['sentid'] in caption_ids:
                caption_sentids.append(sentence['sentid'])
                caption_texts.append(sentence['raw'])

    caption_sentids = np.array(caption_sentids)
    text_encoder = TextEncoder()
    text_features = np.array(text_encoder.encode(caption_texts))

    text_features = np.column_stack((caption_sentids, text_features))

    with open('coco_text_embeddings.npy', 'wb') as f:
        np.save(f, text_features)
