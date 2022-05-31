from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import facenet
import  os
datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest')
path = "D:\\CuongDoAn\\DoAn\\Dataset\\FaceData\\processed\\"
dataset = facenet.get_dataset(path)
for cls in dataset:

        for image_path in cls.image_paths:
                output_class_dir = os.path.join(path, cls.name)
                print(image_path)
                img = load_img(image_path)
                x = img_to_array(img)
                x = x.reshape((1,) + x.shape)
                i = 0
                for batch in datagen.flow(x, batch_size=1,
                                          save_to_dir=output_class_dir, save_prefix=cls.name, save_format='png'):
                    i += 1
                    if i > 20:
                        break  #


