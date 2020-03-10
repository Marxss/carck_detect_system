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
    input1 = vtk.vtkPolyData()
    input2 = vtk.vtkPolyData()

    sphereSource = vtk.vtkSphereSource()
    # sphereSource.SetCenter(5, 0, 0)
    sphereSource.SetRadius(10)
    sphereSource.Update()

    input1.DeepCopy(sphereSource.GetOutput())

    sphereSource.SetRadius(20)
    sphereSource.SetPhiResolution(30)
    sphereSource.Update()

    input2.DeepCopy(sphereSource.GetOutput())

    # Append the two meshes
    appendFilter = vtk.vtkAppendPolyData()
    appendFilter.AddInputData(input1)
    appendFilter.AddInputData(input2)

    appendFilter.Update()

    #  Remove any duplicate points.
    cleanFilter = vtk.vtkCleanPolyData()
    cleanFilter.SetInputConnection(appendFilter.GetOutputPort())
    cleanFilter.Update()


    reader = cleanFilter

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
    isoActor.GetProperty().SetOpacity(0.3)

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
    noConnectivity = 1
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
