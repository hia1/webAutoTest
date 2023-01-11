# -- coding: utf-8 --
# 验证码识别工具类
import time

import easyocr
import pytesseract
from PIL import Image
from selenium import webdriver
import requests
#古诗文网登陆验证码验证


#获取img
def get_img(img_path):
    img=Image.open(img_path)
    return img

#验证码灰度处理，消除线条影响
def image_grayscale_deal(image):
    img=image.convert("L")
    # img.show()
    return img

#验证码二值化处理
def image_threashoding_method(image):
    threshold = 160
    table=[]
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image=image.point(table,"1")
    # image.show()
    return image

#pytresseract库识别
def captcha_crack(image):
    result=pytesseract.image_to_string(image)
    return result

def getCode(img_path):
        img = get_img(img_path)
        img_gray = image_grayscale_deal(img)
        img_process = image_threashoding_method(img_gray)
        #用开源 easyocr库识别验证码
        reader=easyocr.Reader(["ch_sim","en"])
        result=reader.readtext(img_process,detail=0)
        code_text=result[0]
        # print(result[0])
        return code_text


