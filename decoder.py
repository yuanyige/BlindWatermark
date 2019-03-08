# -*- coding: utf8 -*-

import random
import cv2
import math
import numpy as np
from pyzbar.pyzbar import decode
import sys
from PIL import Image


def decoder(ori_path, wm_path, Watermark, password, alpha):
    ori = cv2.imread(ori_path, 1)
    vm = cv2.imread(wm_path, 1)

    watermark = Image.open(WatterMarkedImagine)
    h_o, w_o = ori.shape[0], ori.shape[1]
    h_v, w_v = vm.shape[0], vm.shape[1]
    if h_o > h_v or w_o > w_v :
        #补宽度
        if w_o>w_v:
            w1 = w_o - w_v
            h1 = h_v
            #裁图
            tmp1 = watermark.copy()
            box1 = (0,0,w1,h1)
            cut1 = tmp1.crop(box1)
            #拼接
            im1 = Image.new('RGB', (w_o, h_v), (0, 0, 0))
            box1 = (0,0,w_v,h_v)
            im1.paste(watermark,box1)
            box1 = (w_v,0,w_o,h_v)
            im1.paste(cut1,box1)
            im1.save("im.png")
            watermark = im1
        # 补高度
        if h_o>h_v:
            w2 = w_o
            h2 = h_o - h_v
            #cut
            tmp2 = watermark.copy()
            box2 = (0,0,w2,h2)
            cut2 = tmp2.crop((box2))
            #link
            im2 = Image.new('RGB',(w_o, h_o),(0,0,0))
            im2.paste(watermark,(0,0))
            im2.paste(cut2,(0,h_v))
            im2.save("im.png")
            vm = cv2.imread("im.png", -1)


    out_tmp = next(decodeImg([ori], vm, password, Watermark, alpha))

    out_data = qrDecode(out_tmp, Watermark)
    if out_data:
        return out_data
    return None

def decodeImg(ori_imgs, img, password, Watermark, alpha):
    for ori_img in ori_imgs:
        if ori_img.shape[0] != img.shape[0] or ori_img.shape[1] != img.shape[1]:
            yield None
        else:
            h, w, t = ori_img.shape
            img_f = np.fft.fft2(img)
            ori_f = np.fft.fft2(ori_img)
            watermark = (img_f - ori_f) / alpha
            watermark = np.real(watermark)
            res = np.zeros(watermark.shape)
            x, y = list(range(int(h / 2))), list(range(int(w / 2)))
            random.seed(password)
            random.shuffle(x)
            random.shuffle(y)
            for i in range(int(h / 2)):
                for j in range(int(w / 2)):
                    res[x[i]][y[j]] = watermark[i][j]
            cv2.imwrite(Watermark, res, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

            yield res
    return


def qrDecode(img, Watermark):

    im_gray = cv2.split(img)[2]
    _, out_tmp = cv2.threshold(im_gray, 100, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(out_tmp, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    closed = cv2.merge([closed, closed, closed])
    gray = cv2.cvtColor(closed.astype('uint8'), cv2.COLOR_BGR2GRAY)
    _, closed = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    _, cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tmp = sorted(cnts, key=cv2.contourArea, reverse=True)
    if len(tmp) == 0:
        return None
    c = tmp[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    crop_height = y2 - y1
    crop_width = x2 - x1
    cropImg = out_tmp[y1:y1 + crop_height, x1:x1 + crop_width]
    cropImg1 = cropImg


    try:
        qr_data = decode(cropImg)
        qr_data = qr_data[0][0].decode('utf-8').encode('sjis').decode('utf-8')

        if qr_data:
            cv2.imwrite(Watermark, cropImg1, [cv2.IMWRITE_PNG_COMPRESSION, 7])
            return qr_data
    except:
        return None


if __name__ == "__main__":
    alpha = 10
    password = 123456789
    # 参数1为原图
    OririnImage = sys.argv[1]
    # 参数2为加了水印的图
    WatterMarkedImagine = sys.argv[2]
    # 参数3为输出的水印
    Watermark = sys.argv[3]
    # 参数4为密码
    if (len(sys.argv) == 5):
        password = int(sys.argv[4].encode('ascii').hex())
    data = decoder(OririnImage, WatterMarkedImagine, Watermark, password, alpha)
    fout = open("1.txt", "w+", encoding="utf-8")
    if data:
        # print(data)
        out = "文字解码成功,内容：" + data
        fout.write(out)
    else:
        fout.write("未成功识别文字内容")