from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from imutils.video import VideoStream
import tensorflow as tf
import argparse
import facenet
import pickle
import align.detect_face
import numpy as np
import cv2
import collections
import  imutils
import mysql.connector
from datetime import datetime
import csv

# def mark_attendance(i, r, n):
#     with open("D:\\CuongDoAn\\DoAn\\src\\lop.csv", 'w+', encoding="utf-8", newline='\n') as f:
#         mydataList = csv.reader(f)
#         name_list = []
#         for line in mydataList:
#             try:
#                 name_list.append(line[0])
#             except:
#                 headers = next(mydataList)
#
#         if (i not in name_list):
#             now = datetime.now()
#             d1 = now.strftime("%d/%m/%Y")
#             dtString = now.strftime("%H:%M:%S")
#             f.writelines(f"\n{i}, {r}, {n},{dtString}, {d1}, Có")
#             print("Lưu thành công")
#         else:
#             print("Đã có")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path of the video you want to test on.', default=0)
    args = parser.parse_args()

    MINSIZE = 20
    THRESHOLD = [0.6, 0.7, 0.7]
    FACTOR = 0.709
    IMAGE_SIZE = 182
    INPUT_IMAGE_SIZE = 160
    CLASSIFIER_PATH = 'D:\\CuongDoAn\\DoAn\\Models/facemodel.pkl'
    VIDEO_PATH = args.path
    FACENET_MODEL_PATH = 'D:\\CuongDoAn\\DoAn\\Models/20180402-114759.pb'

    # Load The Custom Classifier
    with open(CLASSIFIER_PATH, 'rb') as file:
        model, class_names = pickle.load(file)
    print("Custom Classifier, Successfully loaded")

    with tf.Graph().as_default():

        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))

        with sess.as_default():

            # Load the model
            print('Loading feature extraction model')
            facenet.load_model(FACENET_MODEL_PATH)

            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]

            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, "D:\\CuongDoAn\\DoAn\\src/align")

            people_detected = set()
            person_detected = collections.Counter()

            cap  = VideoStream(src=0).start()

            while (True):
                frame = cap.read()
                frame = imutils.resize(frame, width=800)
                frame = cv2.flip(frame, 1)

                bounding_boxes, _ = align.detect_face.detect_face(frame, MINSIZE, pnet, rnet, onet, THRESHOLD, FACTOR)

                faces_found = bounding_boxes.shape[0]
                # try:
                if faces_found <=0:
                    cv2.putText(frame, "Khong nhan co nguoi nao", (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1, (255, 255, 255), thickness=1, lineType=2)
                elif faces_found > 0:
                    det = bounding_boxes[:, 0:4]
                    bb = np.zeros((faces_found, 4), dtype=np.int32)
                    for i in range(faces_found):
                        bb[i][0] = det[i][0]
                        bb[i][1] = det[i][1]
                        bb[i][2] = det[i][2]
                        bb[i][3] = det[i][3]
                        print(bb[i][3]-bb[i][1])
                        print(frame.shape[0])
                        print((bb[i][3]-bb[i][1])/frame.shape[0])
                        if (bb[i][3]-bb[i][1])/frame.shape[0]>0.25:
                            cropped = frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :]
                            scaled = cv2.resize(cropped, (INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE),
                                                interpolation=cv2.INTER_CUBIC)
                            scaled = facenet.prewhiten(scaled)
                            scaled_reshape = scaled.reshape(-1, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE, 3)
                            feed_dict = {images_placeholder: scaled_reshape, phase_train_placeholder: False}
                            emb_array = sess.run(embeddings, feed_dict=feed_dict)

                            predictions = model.predict_proba(emb_array)
                            best_class_indices = np.argmax(predictions, axis=1)
                            best_class_probabilities = predictions[
                                np.arange(len(best_class_indices)), best_class_indices]
                            best_name = class_names[best_class_indices[0]]
                            print("Name: {}, Probability: {}".format(best_name, best_class_probabilities))
                            conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root",
                                                           password="root",
                                                           database="face")
                            my_cursor = conn.cursor()


                            if best_class_probabilities > 0.7:
                                with open("D:\\CuongDoAn\\DoAn\\src\\nhandiencamera.csv", 'w+', encoding="utf-8",
                                          newline='\n') as f:
                                    cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)
                                    text_x = bb[i][0]
                                    text_y = bb[i][3] + 20
                                    name = class_names[best_class_indices[0]]
                                    cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (255, 255, 255), thickness=1, lineType=2)
                                    cv2.putText(frame, str(round(best_class_probabilities[0], 3)), (text_x, text_y + 17),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (255, 255, 255), thickness=1, lineType=2)
                                    person_detected[best_name] += 1
                                    my_cursor.execute(
                                        "select HoTen from student where HoTen like '" + str(best_name) + "'")
                                    n = my_cursor.fetchone()
                                    n = "+".join(n)

                                    print(n)
                                    # my_cursor.execute(
                                    #     "select Nam from student where HoTen like '" + str(best_name) + "'")
                                    # r = my_cursor.fetchone()
                                    # r = "+".join(r)
                                    # print(r)

                                    # my_cursor.execute(
                                    #     "select TenGV from student where HoTen like '" + str(best_name) + "'")
                                    # d = my_cursor.fetchone()
                                    # d = "+".join(d)
                                    # print(d)

                                    my_cursor.execute(
                                        "select MaSV from student where HoTen like '" + str(best_name) + "'")
                                    ms = my_cursor.fetchone()
                                    ms = "+".join(ms)
                                    print(ms)
                                    mydataList = csv.reader(f)
                                    name_list = []
                                    print("loi")
                                    try:
                                        print("loi 2")
                                        for line in mydataList:
                                            print("loi 3")
                                            name_list.append(line[0])
                                            print(name_list)
                                        if (ms not in name_list):
                                            now = datetime.now()
                                            d1 = now.strftime("%d/%m/%Y")
                                            dtString = now.strftime("%H:%M:%S")
                                            f.writelines(f"{ms}, {n}, {dtString}, {d1}, Co\n")
                                            print("Đã Lưu")
                                        else:
                                            print("Đã có")
                                    except:
                                        print("Loi")
                                        headers = next(mydataList)

                            else:
                                name = "Người lạ"

                # except:
                #     pass

                cv2.imshow('Nhận Diện khuôn mặt', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()


main()