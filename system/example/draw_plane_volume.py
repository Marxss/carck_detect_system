#coding=utf-8
from vtk import *

# aRenderer=vtkRenderer()
# renWin=vtkRenderWindow()
# renWin.AddRenderer(aRenderer)
# iren=vtkRenderWindowInteractor()
# iren.SetRenderWindow(renWin)

v16=vtkBMPReader()
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix("D:\\carck_detect_system\\myPaper\\crack\\0-00")
v16.SetFilePattern("%s%03d.bmp")
v16.SetDataByteOrderToLittleEndian()
i = 0
v16.SetDataOrigin(0, 0, 0)
v16.SetAllow8BitBMP(16)
v16.SetDataExtent(0 + i, 452 - i, 0 + i, 452 - i, 194, 320)
v16.SetDataSpacing(1,1,1)
v16.Update()

# 利用封装好的MC算法抽取等值面，对应filter
# marchingCubes = vtk.vtkImageMarchingCubes()
marchingCubes=vtk.vtkContourFilter()
marchingCubes=vtk.vtkMarchingContourFilter()
marchingCubes.SetInputConnection(v16.GetOutputPort())
marchingCubes.SetValue(0, 125)
marchingCubes.ComputeGradientsOn()
marchingCubes.ComputeNormalsOn()
marchingCubes.Update()


# 剔除旧的或废除的数据单元，提高绘制速度，对应filter
Stripper = vtk.vtkStripper()
Stripper.SetInputConnection(marchingCubes.GetOutputPort())

# 建立映射，对应mapper
mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(marchingCubes.GetOutputPort())
mapper.SetInputConnection(Stripper.GetOutputPort())

# 建立角色以及属性的设置，对应actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
# 角色的颜色设置
actor.GetProperty().SetDiffuseColor(1, .94, .25)
# 设置高光照明系数
actor.GetProperty().SetSpecular(.1)
# 设置高光能量
actor.GetProperty().SetSpecularPower(100)
actor.GetProperty().SetOpacity(0.5)

# 创建灰度查询表，建立投影切面图
lut=vtkLookupTable()
lut.SetTableRange(0,15)
lut.SetSaturationRange(0,1)
lut.SetHueRange(0,1)
lut.SetValueRange(0,1)
lut.Build()

bwColors=vtkImageMapToColors()
bwColors.SetInputConnection(v16.GetOutputPort())
bwColors.SetLookupTable(lut)
bwActor=vtkImageActor()
bwActor.SetInputData(bwColors.GetOutput())
bwActor.SetDisplayExtent(0,633,0,633,0,11)



# 定义舞台，也就是渲染器，对应render
renderer = vtk.vtkRenderer()

# 定义舞台上的相机，对应render
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(1, 1, 1)
aCamera.SetFocalPoint(0, 0, 0)
# aCamera.SetViewAngle(6)
aCamera.ComputeViewPlaneNormal()

# 定义整个剧院(应用窗口)，对应renderwindow
rewin = vtk.vtkRenderWindow()

# 定义与actor之间的交互，对应interactor
interactor = vtk.vtkRenderWindowInteractor()

# 将相机添加到舞台renderer
renderer.SetActiveCamera(aCamera)
aCamera.Dolly(1.5)

# 设置交互方式
style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# 将舞台添加到剧院中
rewin.AddRenderer(renderer)
interactor.SetRenderWindow(rewin)

# 将角色添加到舞台中
# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.0)
opacityTransferFunction.AddPoint(150, 0.01)
opacityTransferFunction.AddPoint(255, 0.05)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 1.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.0, 1.0)

# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(v16.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

renderer.AddVolume(volume)

renderer.AddActor(actor)
# renderer.AddActor(bwActor)
renderer.SetBackground(1,1,1)
renderer.SetGradientBackground(True)

# 将相机的焦点移动至中央，The camera will reposition itself to view the center point of the actors,
# and move along its initial view plane normal
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()