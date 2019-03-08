# -*- coding: utf8 -*-

import sys
import cv2
import numpy as np
import qrcode
import random
import math

def encodeByTextQr(img_path, txt, out_path, password, alpha):
    img = cv2.imread(img_path, -1)
    h ,w ,t = img.shape
    QR_size = math.ceil(min(h, w) / 150)
    qr = qrcode.QRCode(box_size=QR_size, border=4)
    qr.add_data(txt)
    wm = qr.make_image()
    (wm_w, wm_h) = wm.size
    wm = list(wm.getdata())
    wm = np.array(wm)
    wm = wm.reshape((wm_h, wm_w))
    out_img = encodeImg(img, wm, password, alpha)
    if not out_path.endswith(".png"):
        out_path = out_path + ".png"
    cv2.imwrite(out_path, out_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    return out_path


def encodeImg(img, wm, password, alpha):
    h, w, t = img.shape
    wm_height, wm_width = wm.shape[0], wm.shape[1]
    x, y = list(range(int(h / 2))), list(range(int(w / 2)))
    random.seed(password)
    random.shuffle(x)
    random.shuffle(y)
    tmp = np.zeros(img.shape)
    for i in range(int(h / 2)):
        for j in range(int(w / 2)):
            if x[i] < wm_height and y[j] < wm_width:
                tmp[i][j] = wm[x[i]][y[j]]
                tmp[h - 1 - i][w - 1 - j] = tmp[i][j]
    img_f = np.fft.fft2(img)
    res_f = img_f + alpha * tmp
    res = np.fft.ifft2(res_f)
    res = np.real(res)

    return res


def encodePIC(img, wm, Output, password, alpha):
    img = cv2.imread(img, -1)
    wm = cv2.imread(wm, -1)
    h, w, t = img.shape
    wm_height, wm_width = wm.shape[0], wm.shape[1]
    x, y = list(range(int(h / 2))), list(range(int(w / 2)))
    random.seed(password)
    random.shuffle(x)
    random.shuffle(y)
    tmp = np.zeros(img.shape)
    for i in range(int(h / 2)):
        for j in range(int(w / 2)):
            if x[i] < wm_height and y[j] < wm_width:
                tmp[i][j] = wm[x[i]][y[j]]
                tmp[h - 1 - i][w - 1 - j] = tmp[i][j]
    img_f = np.fft.fft2(img)
    res_f = img_f + alpha * tmp
    res = np.fft.ifft2(res_f)
    res = np.real(res)
    cv2.imwrite(Output, res, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

if __name__ == "__main__":
    password = 123456789
    alpha = 10
    # 参数1为原图
    OririnImage = sys.argv[1]
    # 参数2为FLAG,flag=0 文字，flag=1图片
    pic_flag = sys.argv[2]
    # 参数3为水印
    WatterMark = sys.argv[3]
    # 参数4为输出
    Output = sys.argv[4]
    # 参数5为密码
    if (len(sys.argv) == 6):
        password = int(sys.argv[5].encode('ascii').hex())
    if (pic_flag == '0'):
        encodeByTextQr(OririnImage, WatterMark, Output, password, alpha)
    elif (pic_flag == '1'):
        encodePIC(OririnImage, WatterMark, Output, password, alpha)
