from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLWidget
import sys
from OpenGL.GL import *
from system.OpenGLWidget import OpenGLWidget
from system.untitled import *
from system.showImage import showImage
from myPaper.crack_detection import getImage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    img=getImage()
    print(img.shape)
    showImage(img,ui.image_lable)
    MainWindow.show()
    sys.exit(app.exec_())