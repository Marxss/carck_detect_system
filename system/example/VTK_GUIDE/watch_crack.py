import vtk

colors = vtk.vtkNamedColors()

lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues( 10)
lut.Build()
lut.SetTableValue(0, colors.GetColor4d("Gold"))
lut.SetTableValue(1, colors.GetColor4d("Banana"))
lut.SetTableValue(2, colors.GetColor4d("Tomato"))
lut.SetTableValue(3, colors.GetColor4d("Wheat"))
lut.SetTableValue(4, colors.GetColor4d("Lavender"))
lut.SetTableValue(5, colors.GetColor4d("Flesh"))
lut.SetTableValue(6, colors.GetColor4d("Raspberry"))
lut.SetTableValue(7, colors.GetColor4d("Salmon"))
lut.SetTableValue(8, colors.GetColor4d("Mint"))
lut.SetTableValue(9, colors.GetColor4d("Peacock"))


# Create the RenderWindow, Renderer and Interactor.
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

reader=vtk.vtkSTLReader()
reader.SetFileName(r'D:\carck_detect_system\system\example\VTK_GUIDE\animation_img\ct.stl')
reader.Update()
polyData=reader.GetOutput()

connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
connectivityFilter.SetInputData(polyData)
connectivityFilter.SetExtractionModeToAllRegions()
connectivityFilter.ColorRegionsOn()
connectivityFilter.Update()

numberOfRegions = connectivityFilter.GetNumberOfExtractedRegions()
print(numberOfRegions)




mapper=vtk.vtkPolyDataMapper()
mapper.SetInputConnection(connectivityFilter.GetOutputPort())
mapper.SetScalarRange(connectivityFilter.GetOutput().GetPointData().GetArray("RegionId").GetRange())
mapper.SetLookupTable(lut)
mapper.Update()

actor=vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.3)

ren1.AddActor(actor)
# ren1.AddActor(pointActor)
ren1.SetBackground(colors.GetColor3d("white"))

renWin.Render()
iren.Start()

