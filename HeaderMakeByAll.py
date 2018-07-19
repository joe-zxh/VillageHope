# -*- coding: utf-8 -*-

#通过全部的微信好友的头像，创建一个全村希望的头像

import itchat
import os
import math
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import random


# 获取头像
def headImg():
    # itchat.login()
    # 关键字实参hotReload取True使得短时间内无需再次扫码登录
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)
    # itchat.get_head_img() 获取到头像二进制，并写入文件，保存每张头像
    for count, f in enumerate(friends):
        # 根据userName获取头像
        img = itchat.get_head_img(userName=f["UserName"])
        # imgFile = open("img/" + f["UserName"] + ".jpg", "wb")
        imgFile = open("img/" + str(count) + ".jpg", "wb")
        imgFile.write(img)
        imgFile.close()


w = 640


# 头像拼接图
def createImg():
    x = 0
    y = 0
    imgs = os.listdir("img")
    random.shuffle(imgs)
    # 创建640*640的图片用于填充各小图片
    newImg = Image.new('RGBA', (w, w))
    # 以640*640来拼接图片，math.sqrt()开平方根计算每张小图片的宽高，

    width = int(math.sqrt(w * w / len(imgs)))
    # 每行图片数
    numLine = int(w / width)

    if numLine * numLine < len(imgs):
        numLine = numLine + 1

    i = 0
    while i < numLine * numLine:
        if i < len(imgs):
            img = Image.open("img/" + imgs[i]);
        else:
            img = Image.open("img/" + imgs[i % len(imgs)]);
        i = i + 1
        # 缩小图片
        img = img.resize((width, width), Image.ANTIALIAS)
        # 拼接图片，一行排满，换行拼接
        newImg.paste(img, (x * width, y * width))
        x += 1
        if x >= numLine:
            x = 0
            y += 1

    newImg.save("all.png")


# 皮一下
def QuanCunXiWang():
    icon1 = Image.open("全村底图.png")
    icon2 = Image.open("all.png")

    newim2 = Image.blend(icon1, icon2, 0.3)
    newim2.save('output.png', "PNG")

if __name__ == '__main__':
    if not os.path.exists("./img"):
        os.makedirs("./img")

    # 微信好友头像拼接
    headImg()
    createImg()
    QuanCunXiWang()


