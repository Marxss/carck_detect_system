import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from slice import *


class myMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        imageViewer = vtkImageViewer2()
        self.vtkWidget.GetRenderWindow().AddRenderer(imageViewer.GetRenderer())
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()


        imageViewer.SetInputConnection(reslice.GetOutputPort())
        # imageViewer.SetupInteractor(self.iren)
        imageViewer.SetColorLevel(100)
        imageViewer.SetColorWindow(200)

        # imageViewer.Render()

        # self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = myMainWindow()

    sys.exit(app.exec_())