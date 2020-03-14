#coding=utf-8
from vtk import *
from regionGrowFunc import grow
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from otsu import otsu_threshold
import cv2
from read_images import *
from ACWE.ACWE import *
import random
import os

time_step=1
mu=0.1
nu=0.1
v=0.1
lambda1=1
lambda2=1
epison=1

def toVtkData(LSF):
    # numpy2vtk
    # print(LSF.shape)
    img_num,img_width,img_height=LSF.shape
    dataImporter = vtk.vtkImageImport()
    # The previously created array is converted to a string of chars and imported.
    data_string = LSF.tostring()
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
    dataImporter.SetDataExtent(0, img_height - 1, 0, img_width - 1, 0, img_num-1)
    dataImporter.SetWholeExtent(0, img_height - 1, 0, img_width - 1, 0, img_num-1)
    v16 = dataImporter
    v16.SetDataSpacing(1, 1, 1)
    # v16.SetAllow8BitBMP(16)
    v16.Update()
    return v16



if __name__=="__main__":
    startNum=0
    endNum=1200
    # img_height=255
    # img_width=255
    path = r'D:\carck_detect_system\slices\crack'
    img,img_width,img_height,startNum,endNum=read_images_cube(path,startNum,endNum)
    print(img_height,img_width)
    x,y,z = img.shape
    print("x,y,z:",x,y,z,img.dtype)
    r=100
    LSF = initialize(x,y,z, x_center=x//2, y_center=y//2, z_center=z//2, radius=min(x,y,z)//2)
    # LSF = np.ones(img.shape,img.dtype)
    # LSF[20:x-20,20:y-20,20:z-20]=-1
    # LSF[x//2-10:x//2+10,y//2-10:y//2+10,z//2-10:z//2+10]=-1
    # LSF=-LSF


    colors = vtk.vtkNamedColors()
    # Create the RenderWindow, Renderer and Interactor.
    ren1 = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    cyc=450
    for _ in range(cyc):
        ren1 = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren1)
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        print("iterators:",_+1)
        if _==0:
            pass
        else:
            LSF=LSF.astype(np.float32)
            LSF=CV_once(img, LSF, time_step=time_step, mu=mu,nu=nu, v=v, lambda1=lambda1, lambda2=lambda2, epison=epison)
        LSF=LSF.astype(np.float32)
        v16=toVtkData(LSF)
        iso = vtk.vtkMarchingCubes()
        iso.SetInputConnection(v16.GetOutputPort())
        iso.ComputeNormalsOn()
        iso.ComputeGradientsOn()
        iso.SetValue(0, 0)
        # iso.Update()
        if _%30==0 or _==cyc-1:
            stlWriter = vtk.vtkSTLWriter()
            dir=r"animation_img\tmp\stl"
            if not os.path.exists(dir):
                os.makedirs(dir)
            stlWriter.SetFileName(dir+"\{0}.stl".format("time_step={}, mu={},nu={}_".format(time_step,mu,nu,v)+str(_).zfill(3)))
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
        renWin.SetSize(640*2, 512*2)

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
        writer = vtk.vtkPNGWriter()
        writer.SetFileName("animation_img\\tmp\{0}.png".format("time_step={}, mu={},nu={}_".format(time_step,mu,nu,v)+str(_).zfill(3)))
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.Write()

        # iren.Start()
    iren.Start()


