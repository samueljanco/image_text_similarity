#!/usr/bin/env python3
import numpy as np
import csv

class SimilarityScorer:
    def __int__(self, img_size, txt_size,  v_images, t_images, v_texts, t_texts, v_cxc, t_cxc, epochs = 70, batch_size = 32, test_size = 8000, random_seed = 42):

        self.v_images = v_images
        self.t_images = t_images
        self.v_texts = v_texts
        self.t_texts = t_texts
        self.v_cxc = v_cxc
        self.t_cxc = t_cxc
        self.epochs = epochs
        self.batch_size = batch_size
        self.test_size = test_size
        self.random_seed = random_seed
        self.model = None


    def fit(self):
        v_images, v_texts, v_targets = self._prepare_data(self.v_images, self.v_texts, self.v_cxc)
        t_images, t_texts, t_targets = self._prepare_data(self.t_images, self.t_texts, self.t_cxc)

        np.random.seed(self.random_seed)
        v_sample = np.random.permutation(v_targets.shape[0])
        t_sample = np.random.permutation(t_targets.shape[0])

        train_v_images, train_v_texts, train_v_target = v_images[v_sample], v_texts[v_sample], v_targets[v_sample]
        train_t_images, train_t_texts, train_t_target = (t_images[t_sample])[:-self.test_size], (t_texts[t_sample])[:-self.test_size], (t_targets[t_sample])[:-self.test_size]

        train_images = np.concatenate((train_v_images, train_t_images), axis=0)
        train_texts = np.concatenate((train_v_texts, train_t_texts), axis=0)
        train_targets = np.concatenate((train_v_target, train_t_target), axis=0)

        self.model.fit([train_images, train_texts], train_targets, epochs=self.epochs, batch_size=self.batch_size)

    def _prepare_data(self, image_file, text_file, cxc_file):
        with open(image_file, 'rb') as f:
            image_features = np.load(f)

        with open(text_file, 'rb') as f:
            text_embeddings = np.load(f)

        dict_image_features = self._transform_to_dictionary(image_features)
        dict_text_embeddings = self._transform_to_dictionary(text_embeddings)

        cxc = np.array(list(csv.reader(open(cxc_file), delimiter=',')))[1:]

        image_features = []
        for img in cxc[:, 1]:
            image_features.append(dict_image_features[str(int(img[13:-4]))])

        text_embeddings = []
        for txt in cxc[:, 0]:
            text_embeddings.append(dict_text_embeddings[txt[20:]])

        target = np.array([float(i) for i in cxc[:, 2]])

        return np.array(image_features), np.array(text_embeddings), target

    def _transform_to_dictionary(self, arr):
        dict = {}
        for i in arr:
            dict[str(int(i[0]))] = i[1:]
        return dict
