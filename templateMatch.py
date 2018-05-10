import cv2
import numpy as np


def get_loc(target, template):
    img_rgb = cv2.imread(target)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template, 0)

    run = 1

    w, h = template.shape[::-1]
    print(w, h)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    L = 0
    R = 1
    while run < 20:
        run += 1
        threshold = (R + L) / 2
        print(threshold)
        if threshold < 0:
            print('Error')
        loc = np.where(res >= threshold)
        print(len(loc[1]))
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            print('目标区域起点x坐标为：%d' % loc[1][0])
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2

    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 279, 151), 2)
    #     cv2.imshow('Dectected', img_rgb)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    return loc[1][0]
