def sp_noise(image,prob):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                rdn = random.random()
                if rdn < prob:
                    output[i][j][k] = 0
                elif rdn > thres:
                    output[i][j][k] = 255
                else:
                    output[i][j][k] = image[i][j][k]
    return output


def gasuss_noise(image, mean=0, var=0.001):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise

    out = np.clip(out, 0, 1)
    out = np.uint8(out*255)
    #cv.imshow("gasuss", out)
    return out


from ACWE.CV3d import chanvese3d_yield
from ACWE.toVtkData import toVtkData
from ACWE.ACWE import initialize
from read_images import read_images_cube,read_images,read_images_CT
import vtk
import numpy as np
import os
import skimage
import random
import datetime

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

# img=sp_noise(img.astype(np.uint8),0.005)
img=gasuss_noise(img.astype(np.uint8),0,0.05)
print(img.shape,img.dtype)
print(img.max())

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
    dir + "\{0}.stl".format("time:{}".format(datetime.datetime.now()) ))
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





