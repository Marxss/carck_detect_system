#coding=utf-8
from vtk import *
from regionGrowFunc import grow
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from otsu import otsu_threshold
import cv2

startNum=20
endNum=23
img_height=347
img_width=350


v16=vtkBMPReader()
v16.SetDataByteOrderToLittleEndian()
#crack
# v16.SetFilePrefix("D:\carck_detect_system\myPaper\crack_test\\0-00")
# v16.SetFilePattern("%s%03d.bmp")
#engine
# v16.SetFilePrefix("D:\carck_detect_system\engine\engine0")
# v16.SetFilePattern("%s%03d.bmp")
#precombust
v16.SetFilePrefix("D:\carck_detect_system\precombust\precombust0")
v16.SetFilePattern("%s%03d.bmp")
#gear
# v16.SetFilePrefix("D:\carck_detect_system\myPaper\gear_CT_slices\\")
# v16.SetFilePattern("%s%01d.bmp")

v16.SetDataByteOrderToLittleEndian()
v16.SetDataOrigin(0, 0, 0)
v16.SetAllow8BitBMP(8)
# v16.Allow8BitBMPOff()
v16.SetDataExtent(0, img_height+1, 0, img_width+1, startNum, endNum)
v16.SetDataSpacing(1,1,1)
v16.Update()

#vtk2numpy
# print(dataImporter.SetDataScalarTypeToInt()[0,0,0])
im = v16.GetOutput()
print(im.GetNumberOfPoints())
rows, cols, _ = im.GetDimensions()
sc = im.GetPointData().GetScalars()
a = vtk_to_numpy(sc)
a = a.reshape(rows, cols, -1)
# a[:,:,:]=0
print(a.shape)
# print(a[(100,100,5)])
assert a.shape == im.GetDimensions()
#begin region grow
print(a[:,50,:].shape)
cv2.imshow("slice",a[:,50,:])
cv2.waitKey()
a=grow(a,(0,0,0),1)

#numpy2vtk
dataImporter = vtk.vtkImageImport()
# The previously created array is converted to a string of chars and imported.
data_string = a.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
# The type of the newly imported data is set to unsigned char (uint8)
dataImporter.SetDataScalarTypeToUnsignedChar()
# Because the data that is imported only contains an intensity value
#  (it isnt RGB-coded or someting similar), the importer must be told this is the case.
dataImporter.SetNumberOfScalarComponents(1)
# The following two functions describe how the data is stored and the dimensions of the array it is stored in.
#  For this simple case, all axes are of length 75 and begins with the first element.
#  For other data, this is probably not the case.
# I have to admit however, that I honestly dont know the difference between SetDataExtent()
#  and SetWholeExtent() although VTK complains if not both are used.
dataImporter.SetDataExtent(0, img_height, 0, img_width, 0, endNum-startNum)
dataImporter.SetWholeExtent(0, img_height, 0, img_width, 0, endNum-startNum)
v16=dataImporter
v16.SetDataSpacing(1,1,10)
# v16.SetAllow8BitBMP(16)
v16.Update()

###############################################################################################
colors = vtk.vtkNamedColors()
# This is a simple volume rendering example that
# uses a vtkFixedPointVolumeRayCastMapper

# Create the standard renderer, render window
# and interactor.
ren1 = vtk.vtkRenderer()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.0)
opacityTransferFunction.AddPoint(50, 0.002)
opacityTransferFunction.AddPoint(150, 0.1)
opacityTransferFunction.AddPoint(255, 0.1)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(50, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(100, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(150, 0.0, 0.0, 1.0)

# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
# volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(v16.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

ren1.AddVolume(volume)
ren1.SetBackground(colors.GetColor3d("White"))
ren1.SetGradientBackground(True)
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()

renWin.SetSize(600, 600)
renWin.Render()

iren.Start()