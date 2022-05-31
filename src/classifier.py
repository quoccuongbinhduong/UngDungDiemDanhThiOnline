
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
import facenet
import os
import sys
import math
import pickle
from sklearn.svm import SVC

def main(args):
  
    with tf.Graph().as_default():
      
        with tf.Session() as sess:
            
            np.random.seed(seed=args.seed)
            
            if args.use_split_dataset:
                dataset_tmp = facenet.get_dataset(args.data_dir)
                train_set, test_set = split_dataset(dataset_tmp, args.min_nrof_images_per_class, args.nrof_train_images_per_class)
                if (args.mode=='TRAIN'):
                    dataset = train_set
                elif (args.mode=='CLASSIFY'):
                    dataset = test_set
            else:
                dataset = facenet.get_dataset(args.data_dir)

            # Kiểm tra để đảm bảo rằng mỗi lớp có ít nhất một hình ảnh đào tạo
            for cls in dataset:
                assert(len(cls.image_paths)>0, 'Phải có ít nhất một hình ảnh cho mỗi lớp trong tập dữ liệu')

                 
            paths, labels = facenet.get_image_paths_and_labels(dataset)
            
            print('Số lượng lớp: %d' % len(dataset))
            print('Số lượng ảnh: %d' % len(paths))
            
            # load mô hình
            print('Đang tải mô hình trích xuất tính năng')
            facenet.load_model(args.model)
            
            # Nhận bộ căng đầu vào và đầu ra
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]
            
            #Chạy chuyển tiếp để tính toán các lần nhúng
            print('Tính toán các tính năng cho hình ảnh')
            nrof_images = len(paths)
            nrof_batches_per_epoch = int(math.ceil(1.0*nrof_images / args.batch_size))
            emb_array = np.zeros((nrof_images, embedding_size))
            for i in range(nrof_batches_per_epoch):
                start_index = i*args.batch_size
                end_index = min((i+1)*args.batch_size, nrof_images)
                paths_batch = paths[start_index:end_index]
                images = facenet.load_data(paths_batch, False, False, args.image_size)
                feed_dict = { images_placeholder:images, phase_train_placeholder:False }
                emb_array[start_index:end_index,:] = sess.run(embeddings, feed_dict=feed_dict)
            
            classifier_filename_exp = os.path.expanduser(args.classifier_filename)

            if (args.mode=='TRAIN'):
                # Train classifier
                print('Training classifier')
                model = SVC(kernel='linear', probability=True)
                model.fit(emb_array, labels)#sử dụng model
            
                # Tạo danh sách tên lớp
                class_names = [ cls.name.replace('_', ' ') for cls in dataset]

                # Đang lưu mô hình phân loại
                with open(classifier_filename_exp, 'wb') as outfile:
                    pickle.dump((model, class_names), outfile)
                print('Đã lưu mô hình bộ phân loại vào tệp "%s"' % classifier_filename_exp)
                
            elif (args.mode=='CLASSIFY'):
                # Classify images
                print('Kiểm tra trình phân loại')
                with open(classifier_filename_exp, 'rb') as infile:
                    (model, class_names) = pickle.load(infile)

                print('Đã tải mô hình phân loại từ tệp "%s"' % classifier_filename_exp)

                predictions = model.predict_proba(emb_array)
                best_class_indices = np.argmax(predictions, axis=1)
                best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                
                for i in range(len(best_class_indices)):
                    print('%4d  %s: %.3f' % (i, class_names[best_class_indices[i]], best_class_probabilities[i]))
                    
                accuracy = np.mean(np.equal(best_class_indices, labels))
                print('Accuracy: %.3f' % accuracy)
                
            
def split_dataset(dataset, min_nrof_images_per_class, nrof_train_images_per_class):
    train_set = []
    test_set = []
    for cls in dataset:
        paths = cls.image_paths
        # Xóa các lớp có ít hơn min_nrof_images_per_class
        if len(paths)>=min_nrof_images_per_class:
            np.random.shuffle(paths)
            train_set.append(facenet.ImageClass(cls.name, paths[:nrof_train_images_per_class]))
            test_set.append(facenet.ImageClass(cls.name, paths[nrof_train_images_per_class:]))
    return train_set, test_set

            
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, choices=['TRAIN', 'CLASSIFY'],
        help='Cho biết liệu một bộ phân loại mới nên được đào tạo hay một bộ phân loại ' +
        'mô hình nên được sử dụng để phân loại', default='CLASSIFY')
    parser.add_argument('data_dir', type=str,
        help='Đường dẫn đến thư mục dữ liệu chứa các bản vá lỗi khuôn mặt LFW được căn chỉnh.')
    parser.add_argument('model', type=str,
        help='Có thể là một thư mục chứa meta_file và ckpt_file hoặc một mô hình protobuf (.pb) file')
    parser.add_argument('classifier_filename',
            help='Tên tệp mô hình trình phân loại dưới dạng tệp pickle (.pkl). ' +
        'Đối với đào tạo, đây là đầu ra và để phân loại, đây là đầu vào.')
    parser.add_argument('--use_split_dataset',
        help='Chỉ ra rằng tập dữ liệu được chỉ định bởi data_dir nên được tách thành một tập huấn luyện và thử nghiệm. '+
        'Nếu không, một tập hợp thử nghiệm riêng biệt có thể được chỉ định bằng cách sử dụng tùy chọn test_data_dir.', action='store_true')
    parser.add_argument('--test_data_dir', type=str,
        help='Đường dẫn đến thư mục dữ liệu thử nghiệm có chứa các hình ảnh được căn chỉnh được sử dụng để thử nghiệm.')
    parser.add_argument('--batch_size', type=int,
        help='Số lượng hình ảnh cần xử lý trong một loạt.', default=90)
    parser.add_argument('--image_size', type=int,
        help='Kích thước hình ảnh (chiều cao, chiều rộng) tính bằng pixel.', default=160)
    parser.add_argument('--seed', type=int,
        help='Random seed.', default=666)
    parser.add_argument('--min_nrof_images_per_class', type=int,
        help='Chỉ bao gồm các lớp có ít nhất số lượng hình ảnh này trong tập dữ liệu', default=10)
    parser.add_argument('--nrof_train_images_per_class', type=int,
        help='Sử dụng số lượng hình ảnh này từ mỗi lớp để đào tạo và phần còn lại để thử nghiệm', default=10)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
