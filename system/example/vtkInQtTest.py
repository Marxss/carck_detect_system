import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from system.example.slice import *


class myMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        imageViewer = vtkImageViewer2()
        renderWindowInteractor = self.vtkWidget
        imageViewer.SetInputConnection(reslice.GetOutputPort())
        imageViewer.SetupInteractor(renderWindowInteractor)
        imageViewer.SetColorLevel(100)
        imageViewer.SetColorWindow(200)

        imageViewer.Render()

        self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = myMainWindow()

    sys.exit(app.exec_())