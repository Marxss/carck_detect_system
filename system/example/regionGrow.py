#coding=utf-8
from vtk import *
from regionGrowFunc import grow
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from otsu import otsu_threshold
import cv2
from read_images import read_images

startNum=0
endNum=1200
# img_height=255
# img_width=255


path = r'D:\carck_detect_system\crack'
a,img_width,img_height,startNum,endNum=read_images(path,startNum,endNum)
print("img zise: ",img_height," ,",img_width,startNum,endNum)
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
dataImporter.SetDataExtent(0, img_height-1, 0, img_width-1, 0, endNum-startNum)
dataImporter.SetWholeExtent(0, img_height-1, 0, img_width-1, 0, endNum-startNum)
v16=dataImporter
v16.SetDataSpacing(1,1,1)
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
opacityTransferFunction.AddPoint(50, 0.0)
opacityTransferFunction.AddPoint(150, 0.6)
opacityTransferFunction.AddPoint(255, 0.0)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(50, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(100, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(150, 0.0, 0.7, 0.7)
colorTransferFunction.AddRGBPoint(255, 0.0, 0.0, 0.0)

#Creat opacity gradient function
gradientTransferFunction=vtkPiecewiseFunction()
gradientTransferFunction.AddPoint(0,0.0)
gradientTransferFunction.AddPoint(255,2.0)
# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.SetGradientOpacity(gradientTransferFunction)

volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.5)  #设置环境光系数
volumeProperty.SetDiffuse(1)  #设置散射光系数
volumeProperty.SetSpecular(0.5)  #设置反射光系数
volumeProperty.SetSpecularPower(50)
#设置灯光
myLight2 = vtkLight()
myLight2.PositionalOn()
myLight2.SetColor(1, 1, 1)
myLight2.SetPosition(-9999999, -9999999, -9999999)
myLight2.SetFocalPoint(ren1.GetActiveCamera().GetFocalPoint())
# ren1.AddLight(myLight2)

volumeProperty.SetInterpolationTypeToLinear()
# volumeProperty.SetInterpolationTypeToNearest()

# The mapper / ray cast function know how to render the data.
# volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
# volumeMapper=vtkGPUVolumeRayCastMapper()
volumeMapper=vtkSmartVolumeMapper()
volumeMapper.SetRequestedRenderModeToRayCast()
volumeMapper.SetRequestedRenderModeToGPU()
# volumeMapper.SetInterpolationModeToLinear()
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