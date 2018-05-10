#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import BytesIO

import cv2
import numpy as np
import requests
from PIL import Image

# 偏移量
bias = -1


def predict(back_img_path, small_img_path):
    # response = requests.get(slide_captcha_url)
    # base64_image = response.json()['data']['dataUrl']
    # base64_image_without_head = base64_image.replace('data:image/png;base64,', '')

    img = np.array(Image.open(back_img_path).convert('RGB'))
    # print(img.shape)
    #
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imwrite('img_blur.jpg',img_blur)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('img_gray.jpg',img_gray)
    img_canny = cv2.Canny(img_gray, 100, 200)
    # cv2.imwrite('img_canny.jpg',img_canny)


    small_img = np.array(Image.open(small_img_path).convert('RGB'))
    small_img_blur = cv2.GaussianBlur(small_img, (5, 5), 0)
    small_img_gray = cv2.cvtColor(small_img_blur, cv2.COLOR_BGR2GRAY)
    small_img_canny = cv2.Canny(small_img_gray, 100, 200)

    cv2.imwrite(small_img_path, small_img_canny)
    #
    operator = get_operator(small_img_path)
    #
    (x, y), _ = best_match(img_canny, operator)
    x = x + bias
    print('the position of x is', x)
    return x
    #
    # buffer = mark(img, x, y)
    #
    # return {'value': x, 'image': base64.b64encode(buffer.getbuffer()).decode()}


def get_operator(path, url=False, expand=False):
    if url:
        req = requests.get(path)
        arr = np.asarray(bytearray(req.content), dtype=np.uint8)
        shape = cv2.resize(cv2.imdecode(arr, -1), (69, 69))
    shape = cv2.imread(path)
    # else:
        # shape = cv2.resize(cv2.imread(path), (69, 69))

    shape_gray = cv2.cvtColor(shape, cv2.COLOR_BGR2GRAY)

    _, shape_binary = cv2.threshold(shape_gray, 220, 255, cv2.THRESH_BINARY)

    img, contours, hierarchy = cv2.findContours(shape_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.imshow('imageshow', img)
    cv2.waitKey()
    print(np.size(contours))
    # contour = contours[0]
    #
    # operator = np.zeros((69, 69))
    #
    # for point in contour:
    #     operator[point[0][0]][point[0][1]] = 1
    #     if expand:
    #         if point[0][0] > 0:
    #             operator[point[0][0] - 1][point[0][1]] = 1
    #         if point[0][0] < 68:
    #             operator[point[0][0] + 1][point[0][1]] = 1
    #         if point[0][1] > 0:
    #             operator[point[0][0]][point[0][1] - 1] = 1
    #         if point[0][1] < 68:
    #             operator[point[0][0]][point[0][1] + 1] = 1
    #
    # return operator


def best_match(image, operator):
    y_range, x_range = image.shape
    max_value, position = 0, (1, 1)

    for y in range(1, y_range - 1):
        for x in range(1, x_range - 1):
            if y + 69 > 240 or x + 69 > 480:
                continue
            block = image[(y - 1):(y + 68), (x - 1):(x + 68)]
            value = (block * operator).sum()
            if value > max_value:
                max_value = value
                position = (x, y)

    return position, max_value


    # def mark(img, x, y):
    #     cv2.putText(img, 'O', (x - 15, y + 70), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 2, cv2.LINE_AA)
    #
    #     buffer = BytesIO()
    #     imsave(buffer, img)
    #     return buffer

if __name__ == '__main__':
    get_operator('small_img.png')
