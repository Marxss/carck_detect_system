import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def showImage(Im,image_label):
    # Im = cv2.imread('***.jpg')  # 通过Opencv读入一张图片
    print(type(image_label))
    print(image_label.geometry())
    print(image_label.frameRect())
    size=image_label.geometry()
    x1=size.x()
    y1=size.y()
    x2=size.width()
    y2=size.height()
    w=x2-x1
    h=y2-y1
    Im = cv2.resize(Im, (0, 0), fx=h/Im.shape[0], fy=w/Im.shape[1], interpolation=cv2.INTER_CUBIC)
    image_height, image_width, image_depth = Im.shape  # 获取图像的高，宽以及深度。
    QIm = cv2.cvtColor(Im, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
    QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                 image_width * image_depth,
                 QImage.Format_RGB888)
    image_label.setPixmap(QPixmap.fromImage(QIm))  # 将QImage显示在之前创建的QLabel控件中
