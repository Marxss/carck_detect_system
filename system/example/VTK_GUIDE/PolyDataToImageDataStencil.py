import vtk


def get_program_parameters():
    import argparse
    description = 'Converts the polydata to imagedata and masks the given imagedata.'
    epilogue = '''
        Contributed by: Peter Gruber

   '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue)
    parser.add_argument('filename', help='A filename e.g. fullhead15.png.')
    args = parser.parse_args()
    return args.filename


def main():
    fn = get_program_parameters()
    # A script to test the stencil filter with a polydata stencil.
    # Image pipeline
    reader = vtk.vtkPNGReader()
    reader.SetDataSpacing(0.8, 0.8, 1.5)
    reader.SetDataOrigin(0.0, 0.0, 0.0)
    reader.SetFileName(fn)
    sphere = vtk.vtkSphereSource()
    sphere.SetPhiResolution(12)
    sphere.SetThetaResolution(12)
    sphere.SetCenter(102, 102, 0)
    sphere.SetRadius(60)
    triangle = vtk.vtkTriangleFilter()
    triangle.SetInputConnection(sphere.GetOutputPort())

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(triangle.GetOutputPort())
    dataToStencil = vtk.vtkPolyDataToImageStencil()
    dataToStencil.SetInputConnection(stripper.GetOutputPort())
    dataToStencil.SetOutputSpacing(0.8, 0.8, 1.5)
    dataToStencil.SetOutputOrigin(0.0, 0.0, 0.0)

    stencil = vtk.vtkImageStencil()
    stencil.SetInputConnection(reader.GetOutputPort())
    stencil.SetStencilConnection(dataToStencil.GetOutputPort())
    stencil.ReverseStencilOn()
    stencil.SetBackgroundValue(500)

    # test again with a contour
    reader2 = vtk.vtkPNGReader()
    reader2.SetDataSpacing(0.8, 0.8, 1.5)
    reader2.SetDataOrigin(0.0, 0.0, 0.0)
    reader2.SetFileName(fn)
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, 0)
    plane.SetNormal(0, 0, 1)
    cutter = vtk.vtkCutter()
    cutter.SetInputConnection(sphere.GetOutputPort())
    cutter.SetCutFunction(plane)
    stripper2 = vtk.vtkStripper()
    stripper2.SetInputConnection(cutter.GetOutputPort())
    dataToStencil2 = vtk.vtkPolyDataToImageStencil()
    dataToStencil2.SetInputConnection(stripper2.GetOutputPort())
    dataToStencil2.SetOutputSpacing(0.8, 0.8, 1.5)
    dataToStencil2.SetOutputOrigin(0.0, 0.0, 0.0)
    stencil2 = vtk.vtkImageStencil()
    stencil2.SetInputConnection(reader2.GetOutputPort())
    stencil2.SetStencilConnection(dataToStencil2.GetOutputPort())
    stencil2.SetBackgroundValue(500)

    imageAppend = vtk.vtkImageAppend()
    imageAppend.SetInputConnection(stencil.GetOutputPort())
    imageAppend.AddInputConnection(stencil2.GetOutputPort())

    viewer = vtk.vtkImageViewer()
    interator = vtk.vtkRenderWindowInteractor()
    viewer.SetInputConnection(imageAppend.GetOutputPort())
    viewer.SetupInteractor(interator)
    viewer.SetZSlice(0)
    viewer.SetColorWindow(2000)
    viewer.SetColorLevel(1000)
    viewer.Render()

    interator.Start()


if __name__ == '__main__':
    main()