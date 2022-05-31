
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.naive_bayes import GaussianNB

# from xgboost import XGBClassifier

import facenet
from sklearn.svm import SVC
import numpy as np

import facenet

import math


DataSetFile = "D:\\CuongDoAn\\DoAn\\Models\\20180402-114759.pb "

# Run forward pass to calculate embeddings

with tf.Graph().as_default():
    with tf.Session() as sess:

        dataset = facenet.get_dataset("D:\\CuongDoAn\\DoAn\\Dataset\\FaceData\\processed")
        paths, labels = facenet.get_image_paths_and_labels(dataset)
        print('Tính toán các tính năng cho hình ảnh')
        facenet.load_model(DataSetFile)
        # Nhận bộ căng đầu vào và đầu ra
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]
        nrof_images = len(paths)
        nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / 160))
        emb_array = np.zeros((nrof_images, embedding_size))
        for i in range(nrof_batches_per_epoch):
            start_index = i * 160
            end_index = min((i + 1) * 160, nrof_images)
            paths_batch = paths[start_index:end_index]
            images = facenet.load_data(paths_batch, False, False, 160)
            feed_dict = {images_placeholder: images, phase_train_placeholder: False}
            emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)
        models = [
            # XGBClassifier(),
            GaussianNB(),
            SVC(probability=True, kernel='linear')
        ]

        # kiem tra bang ty le train/test
        ti_le = [{"key": "60/40", "value": 0.4}, {"key": "70/30", "value": 0.3}, {"key": "80/20", "value": 0.2}]

        ketqua = {'Tyle': [],
                  'PhuongPhap': [],
                  'Accuracy': [],
                  'AUC': []}

        ketqua = pd.DataFrame(ketqua)

        for ratio in ti_le:
            X_train, X_test, y_train, y_test = train_test_split(emb_array, labels, test_size=ratio["value"], random_state=18)
            kq_row = {"Tyle": ratio["key"]}
            for model in models:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_prod = model.predict_proba(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                auc = roc_auc_score(y_test, y_prod, multi_class='ovr', average='weighted')
                kq_row["PhuongPhap"] = type(model).__name__
                kq_row["Accuracy"] = accuracy
                kq_row["AUC"] = auc
                ketqua = ketqua.append(kq_row, ignore_index=True)
        print("----------------KET QUA PHAN CHIA THEO TY LE TRAIN/TEST------------------")
        print(ketqua.groupby(["Tyle", "PhuongPhap"]).mean())
        print("\n----------------TONG HOP KET QUA....................:")
        print(ketqua.groupby("PhuongPhap").mean())