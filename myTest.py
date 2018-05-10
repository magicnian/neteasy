from PIL import Image
import numpy as np
import cv2

img = Image.open('back_img.jpg')

size = img.size

x_length = size[0]
print('x_length:', x_length)

y_length = size[1]
print('y_length:', y_length)

im_num = np.array(img)

img_blur = cv2.GaussianBlur(im_num, (5, 5), 0)

img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

img_canny = cv2.Canny(img_gray, 100, 200)

cv2.imwrite('back_img_func.jpg', img_canny)

cv2.imshow('image', img_canny)
cv2.waitKey(0)
