import cv2
from PIL import Image

img = Image.open("D:\\CuongDoAn\\DoAn\\Dataset\\FaceData\\processed\\Nguyen Quoc Cuong\\Nguyen Quoc Cuong_0_335.png")


# If you want a greyscale image, simply convert it to the L (Luminance) mode:
new_img = img.convert('L')
new_img.show()
