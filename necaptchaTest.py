#!/usr/local/bin/python
# -*- coding: utf8 -*-

'''
Created on 2018年5月4日

@author: lnn
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import PIL.Image as image
import time, re, io, urllib, random
from urllib import request
import requests
import cv2
import templateMatch


def get_img(driver, filename, location):
    time.sleep(1)

    # WebDriverWait(driver, 30).until(
    #     lambda the_driver: the_driver.find_element_by_css_selector('#bg > div:nth-child(2) > div > div > div > div > form > div.m-tab > div.m-tab-content > div:nth-child(2) > div > div > div.yidun_panel > div > div.yidun_bgimg > img.yidun_bg-img').is_displayed())

    background_images = driver.find_elements_by_css_selector(location)

    img_url = background_images[0].get_attribute('src')

    print(img_url)
    response = requests.get(img_url)
    img = image.open(io.BytesIO(response.content))
    img.save(filename)

    return filename


# def is_similar(image1, image2, x, y):
#     '''
#     对比RGB值
#     '''
#     pass
#
#     pixel1 = image1.getpixel((x, y))
#     pixel2 = image2.getpixel((x, y))
#
#     for i in range(0, 3):
#         if abs(pixel1[i] - pixel2[i]) >= 50:
#             return False
#
#     return True
#
# def get_diff_location(image1, image2):
#     '''
#     计算缺口的位置
#     '''
#
#     i = 0
#
#     for i in range(0, 320):
#         for j in range(0, 160):
#             if is_similar(image1, image2, i, j) == False:
#                 return i

def get_track(length):
    '''
    根据缺口的位置模拟x轴移动的轨迹
    '''
    pass

    list = []

    # 间隔通过随机范围函数来获得
    x = random.randint(5, 10)

    while length - x >= 10:
        list.append(x)

        length = length - x
        x = random.randint(5, 10)

    for i in range(length):
        list.append(1)

    return list


def main():
    #     这里的文件路徑是webdriver的文件路径
    driver = webdriver.Chrome(executable_path=r"E:\chromedriver\chromedriver.exe")

    # 打开网页
    driver.get("https://id.163yun.com/register")

    back_img_name = get_img(driver, 'back_img.jpg',
                            '#bg > div:nth-child(2) > div > div > div > div > form > div.m-tab > div.m-tab-content > div:nth-child(2) > div > div > div.yidun_panel > div > div.yidun_bgimg > img.yidun_bg-img')
    small_img_name = get_img(driver, 'small_img.png',
                             '#bg > div:nth-child(2) > div > div > div > div > form > div.m-tab > div.m-tab-content > div:nth-child(2) > div > div > div.yidun_panel > div > div.yidun_bgimg > img.yidun_jigsaw')

    #     计算缺口位置
    # loc = get_diff_location(img_1, img_2)

    loc = templateMatch.get_loc(back_img_name, small_img_name)

    #     生成x的移动轨迹点
    track_list = get_track(loc)

    button = driver.find_elements_by_xpath(
        '//*[@id="bg"]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]')
    button = button[0]
    location = button.location
    #     获得滑动圆球的高度
    y = location['y']

    # 鼠标点击元素并按住不放
    print("第一步,点击元素")
    ActionChains(driver).click_and_hold(on_element=button).perform()
    time.sleep(1)

    print("第二步，拖动元素")
    # track_string = ""
    # for track in track_list:
    #     track_string = track_string + "{%d,%d}," % (track, y - 445)
    #     #         xoffset=track+22:这里的移动位置的值是相对于滑动圆球左上角的相对值，而轨迹变量里的是圆球的中心点，所以要加上圆球长度的一半。
    #     #         yoffset=y-445:这里也是一样的。不过要注意的是不同的浏览器渲染出來的结果是不一样的，要保证最终的计算后的值是22，也就是圆球高度的一半
    #     ActionChains(driver).move_to_element_with_offset(to_element=button, xoffset=track + 22,
    #                                                      yoffset=y - 445).perform()
    #     #         间隔时间也通过随机函数來获得
    #     time.sleep(random.randint(10, 30) / 100)
    #
    # print(track_string)
    # #     xoffset=21，本质就是向后退一格。这里退了5格是因为圆球的位置和滑动条的左边缘有5格的距离
    # ActionChains(driver).move_to_element_with_offset(to_element=button, xoffset=21, yoffset=y - 445).perform()
    # time.sleep(0.1)
    # ActionChains(driver).move_to_element_with_offset(to_element=button, xoffset=21, yoffset=y - 445).perform()
    # time.sleep(0.1)
    # ActionChains(driver).move_to_element_with_offset(to_element=button, xoffset=21, yoffset=y - 445).perform()
    # time.sleep(0.1)
    # ActionChains(driver).move_to_element_with_offset(to_element=button, xoffset=21, yoffset=y - 445).perform()
    # time.sleep(0.1)
    # ActionChains(driver).move_to_element_with_offset(to_element=button, xoffset=21, yoffset=y - 445).perform()
    ActionChains(driver).move_to_element_with_offset(to_element=button,xoffset=loc,yoffset=0).perform()

    print("第三步，释放鼠标")
    #     释放鼠标
    ActionChains(driver).release(on_element=button).perform()

    time.sleep(3)

    driver.quit()


if __name__ == '__main__':
    main()
