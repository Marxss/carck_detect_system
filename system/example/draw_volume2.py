#!/usr/bin/env python

import vtk
from vtk import *

def main():
    v16 = vtkBMPReader()
    v16.SetDataByteOrderToLittleEndian()
    v16.SetFilePrefix("D:\\carck_detect_system\\myPaper\\crack\\0-00")
    v16.SetFilePattern("%s%03d.bmp")
    v16.SetDataByteOrderToLittleEndian()
    i = 0
    v16.SetDataOrigin(0, 0, 0)
    v16.SetDataExtent(0 + i, 452 - i, 0 + i, 452 - i, 195, 319)
    # v16.SetDataExtent (0,0,0,0,19,83)
    v16.SetDataSpacing(1, 1, 1)
    v16.SetAllow8BitBMP(16)
    # v16.SetOrigin([0,0,0])
    v16.Update()
    reader=v16
    print(reader.GetOutput().GetNumberOfPoints())
    # print(reader.GetOutput().GetRange())
    print(reader.GetOutput())

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
    opacityTransferFunction.AddPoint(150, 0.01)
    opacityTransferFunction.AddPoint(255, 0.1)

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
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    # The volume holds the mapper and the property and
    # can be used to position/orient the volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    ren1.AddVolume(volume)
    ren1.SetBackground(colors.GetColor3d("Wheat"))
    ren1.GetActiveCamera().Azimuth(45)
    ren1.GetActiveCamera().Elevation(30)
    ren1.ResetCameraClippingRange()
    ren1.ResetCamera()

    renWin.SetSize(600, 600)
    renWin.Render()

    iren.Start()




if __name__ == '__main__':
    main()