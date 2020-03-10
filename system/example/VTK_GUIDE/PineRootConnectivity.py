#!/usr/bin/env python

import vtk


def pine_root_connectivity(fileName, noConnectivity):
    def NumberOfTriangles(pd):
        """
        Count the number of triangles.
        :param pd: vtkPolyData.
        :return: The number of triangles.
        """
        cells = pd.GetPolys()
        numOfTriangles = 0
        idList = vtk.vtkIdList()
        for i in range(0, cells.GetNumberOfCells()):
            cells.GetNextCell(idList)
            # print(idList)
            # If a cell has three points it is a triangle.
            # print(idList.GetNumberOfIds())
            if idList.GetNumberOfIds() == 3:
                numOfTriangles += 1
        return numOfTriangles

    colors = vtk.vtkNamedColors()

    # Create the pipeline.
    v16 = vtk.vtkBMPReader()
    v16.SetDataByteOrderToLittleEndian()
    v16.SetFilePrefix("D:\slice_data\\bmp-lungu\\200503180")
    v16.SetFilePattern("%s%03d.bmp")
    i = 0
    v16.SetDataExtent(0 + i, 452 - i, 0 + i, 452 - i, 19, 83)
    v16.SetDataSpacing(1, 1, 1)
    v16.Update()

    # 利用封装好的MC算法抽取等值面，对应filter
    # marchingCubes = vtk.vtkImageMarchingCubes()
    marchingCubes = vtk.vtkContourFilter()
    # marchingCubes = vtk.vtkMarchingContourFilter()
    marchingCubes.SetInputConnection(v16.GetOutputPort())
    marchingCubes.SetValue(0, 100)
    marchingCubes.ComputeGradientsOn()
    marchingCubes.ComputeNormalsOn()
    marchingCubes.Update()

    # 剔除旧的或废除的数据单元，提高绘制速度，对应filter
    # Stripper = vtk.vtkStripper()
    # Stripper.SetInputConnection(marchingCubes.GetOutputPort())
    reader = marchingCubes

    if not noConnectivity:
        reader.Update()
        print("Before Connectivity.")
        print("There are: ", NumberOfTriangles(reader.GetOutput()), "triangles")

    connect = vtk.vtkPolyDataConnectivityFilter()
    connect.SetInputConnection(reader.GetOutputPort())
    connect.SetExtractionModeToLargestRegion()
    if not noConnectivity:
        connect.Update()
        print("After Connectivity.")
        print("There are: ", NumberOfTriangles(connect.GetOutput()), "triangles")

    isoMapper = vtk.vtkPolyDataMapper()
    if noConnectivity:
        isoMapper.SetInputConnection(reader.GetOutputPort())
    else:
        isoMapper.SetInputConnection(connect.GetOutputPort())
    isoMapper.ScalarVisibilityOff()
    isoActor = vtk.vtkActor()
    isoActor.SetMapper(isoMapper)
    isoActor.GetProperty().SetColor(colors.GetColor3d("raw_sienna"))

    #  Get an outline of the data set for context.
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(colors.GetColor3d("Black"))

    # Create the Renderer, RenderWindow and RenderWindowInteractor.
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size.
    ren.AddActor(outlineActor)
    ren.AddActor(isoActor)
    renWin.SetSize(512, 512)
    ren.SetBackground(colors.GetColor3d("SlateGray"))

    # render the image
    #
    # iren AddObserver UserEvent {wm deiconify .vtkInteract}
    cam = ren.GetActiveCamera()
    cam.SetFocalPoint(40.6018, 37.2813, 50.1953)
    cam.SetPosition(40.6018, -280.533, 47.0172)
    cam.ComputeViewPlaneNormal()
    cam.SetClippingRange(26.1073, 1305.36)
    cam.SetViewAngle(20.9219)
    cam.SetViewUp(0.0, 0.0, 1.0)

    iren.Initialize()
    renWin.Render()
    iren.Start()

def main():
    fileName, noConnectivity = 'D:\\VTKExamples\\src\\Testing\\Data\\pine_root.tri',0
    noConnectivity = 0
    pine_root_connectivity(fileName, noConnectivity)


def get_program_parameters():
    import argparse
    description = 'Applying connectivity filter to remove noisy isosurfaces.'
    epilogue = '''
        Applying connectivity filter to remove noisy isosurfaces.

This example demonstrates how to use the vtkConnectivityFilter.
If the extra parameter 'noConnectivity' is non zero, the connectivity filter will not be used.

   '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='D:\VTKExamples\src\Testing\Data\pine_root.tri')
    parser.add_argument('noConnectivity', default=0, type=int, nargs='?',
                        help='If non-zero do not use the connectivity filter.')
    args = parser.parse_args()
    return args.filename, args.noConnectivity


if __name__ == '__main__':
    main()
