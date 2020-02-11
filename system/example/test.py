#coding=utf-8
from vtk import *
from regionGrowFunc import grow
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from otsu import otsu_threshold
import cv2
from read_images import read_images
from ACWE.ACWE import *
import random

startNum=0
endNum=1200
# img_height=255
# img_width=255

path = r'D:\carck_detect_system\crack'
img,img_width,img_height,startNum,endNum=read_images(path,startNum,endNum)
x,y,z = img.shape
r=10
phi0 = initialize(x,y,z, x_center=r, y_center=r, z_center=r, radius=r-2)
a=CV(img, phi0, max_iter=30, time_step=100, mu=0.1, v=0.1, lambda1=1, lambda2=1, epison=10)
# a=phi0
# a=a.astype(np.uint8)
# a=np.zeros((x,y,z),dtype=np.uint8)
# a[30:50,30:50,30:50]=250+random.randint(0,8)
print(img.shape,img.dtype,a.shape,a.dtype)
# a=img
print("img zise: ",img_height," ,",img_width,startNum,endNum)
# a=grow(a,(0,0,0),1)

#numpy2vtk
dataImporter = vtk.vtkImageImport()
# The previously created array is converted to a string of chars and imported.
data_string = a.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
# The type of the newly imported data is set to unsigned char (uint8)
# dataImporter.SetDataScalarTypeToUnsignedChar()
dataImporter.SetDataScalarTypeToFloat()
# Because the data that is imported only contains an intensity value
#  (it isnt RGB-coded or someting similar), the importer must be told this is the case.
dataImporter.SetNumberOfScalarComponents(1)
# The following two functions describe how the data is stored and the dimensions of the array it is stored in.
#  For this simple case, all axes are of length 75 and begins with the first element.
#  For other data, this is probably not the case.
# I have to admit however, that I honestly dont know the difference between SetDataExtent()
#  and SetWholeExtent() although VTK complains if not both are used.
dataImporter.SetDataExtent(0, img_height-1, 0, img_width-1, 0, endNum-startNum)
dataImporter.SetWholeExtent(0, img_height-1, 0, img_width-1, 0, endNum-startNum)
v16=dataImporter
v16.SetDataSpacing(1,1,1)
# v16.SetAllow8BitBMP(16)
v16.Update()


colors = vtk.vtkNamedColors()

# Create the RenderWindow, Renderer and Interactor.
ren1 = vtk.vtkRenderer()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iso = vtk.vtkContourFilter()
iso.SetInputConnection(v16.GetOutputPort())
iso.SetValue(0, 0)

isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(iso.GetOutputPort())
isoMapper.ScalarVisibilityOff()

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor(colors.GetColor3d("Banana"))
isoActor.GetProperty().SetDiffuseColor(1, .94, .25)
# 设置高光照明系数
isoActor.GetProperty().SetSpecular(.1)
# 设置高光能量
isoActor.GetProperty().SetSpecularPower(100)
isoActor.GetProperty().SetOpacity(0.5)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(v16.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

# Add the actors to the renderer, set the background and size.
#
ren1.AddActor(outlineActor)
ren1.AddActor(isoActor)
ren1.SetBackground(colors.GetColor3d("SlateGray"))
renWin.SetSize(640, 512)

# Render the image.
#
ren1.ResetCamera()
ren1.GetActiveCamera().Azimuth(30)
ren1.GetActiveCamera().Elevation(30)
renWin.Render()
iren.Start()