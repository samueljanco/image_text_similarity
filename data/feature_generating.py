import csv
import numpy as np
from image_features import  ImageEncoder

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
