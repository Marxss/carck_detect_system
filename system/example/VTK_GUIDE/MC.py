from ACWE.CV3d import chanvese3d_yield
from ACWE.toVtkData import toVtkData
from ACWE.ACWE import initialize
from read_images import read_images_cube,read_images,read_images_CT
import vtk
import numpy as np
import os


startNum=0
endNum=1200
# img_height=255
# img_width=255
path = r'D:\carck_detect_system\slices\precombust'
img,img_width,img_height,startNum,endNum=read_images_cube(path,startNum,endNum,flip=True)
print(img_height,img_width)
x,y,z = img.shape
print("x,y,z:",x,y,z,img.dtype)
# r=100
# phi = initialize(x,y,z, x_center=x//2, y_center=y//2, z_center=z//2, radius=min(x,y,z)//2)



colors = vtk.vtkNamedColors()
# Create the RenderWindow, Renderer and Interactor.
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

LSF = img.astype(np.float32)
v16 = toVtkData(LSF)
iso = vtk.vtkMarchingCubes()
iso.SetInputConnection(v16.GetOutputPort())
iso.ComputeNormalsOn()
iso.ComputeGradientsOn()
iso.SetValue(0, 120)

stlWriter = vtk.vtkSTLWriter()
dir = r"animation_img"
if not os.path.exists(dir):
    os.makedirs(dir)
stlWriter.SetFileName(
    dir + "\{0}.stl".format("time_step={}, mu={}".format(1, 1, 1) ))
stlWriter.SetInputConnection(iso.GetOutputPort())
stlWriter.Write()

isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(iso.GetOutputPort())
isoMapper.ScalarVisibilityOff()

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor(colors.GetColor3d("Banana"))
isoActor.GetProperty().SetDiffuseColor(1, .94, .25)
# 设置高光照明系数
isoActor.GetProperty().SetSpecular(.6)
# 设置高光能量
isoActor.GetProperty().SetSpecularPower(30)
isoActor.GetProperty().SetOpacity(0.6)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(v16.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

# Add the actors to the renderer, set the background and size.

# ren1.AddActor(outlineActor)
ren1.AddActor(isoActor)
ren1.SetBackground(colors.GetColor3d("white"))
renWin.SetSize(640 * 2, 512 * 2)

# Render the image.
ren1.ResetCamera()
ren1.GetActiveCamera().Azimuth(20)
ren1.GetActiveCamera().Elevation(20)
renWin.Render()

w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.SetInputBufferTypeToRGB()
w2if.ReadFrontBufferOff()
w2if.Update()


# iren.Start()
iren.Start()