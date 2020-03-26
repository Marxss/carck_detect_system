import vtk
import cv2

colors = vtk.vtkNamedColors()
# Create the RenderWindow, Renderer and Interactor.
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

reader=vtk.vtkSTLReader()
reader.SetFileName(r'D:\carck_detect_system\system\example\VTK_GUIDE\animation_img\time_step=1, mu=1.stl')
reader.Update()
polyData=reader.GetOutput()

connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
connectivityFilter.SetInputData(polyData)
connectivityFilter.SetExtractionModeToSpecifiedRegions()
connectivityFilter.AddSpecifiedRegion(1)
# connectivityFilter.SetExtractionModeToLargestRegion()
connectivityFilter.Update()



# ployData=vtk.vtkSelectEnclosedPoints()
# ployData.SetInputConnection(connectivityFilter.GetOutputPort())
# ployData.SetInputData(connectivityFilter.GetOutput())
ployData=connectivityFilter.GetOutput()
# print(ployData)
# print("num:",ployData.GetNumberOfPoints())
arr=set()
print(ployData.GetNumberOfCells())
for i in range(ployData.GetNumberOfCells()):
    # print(ployData.GetCell(i))
    # print(ployData.GetCell(i).GetPoints().GetPoint(0))
    arr.add(ployData.GetCell(i).GetPoints().GetPoint(0))
    arr.add(ployData.GetCell(i).GetPoints().GetPoint(1))
    arr.add(ployData.GetCell(i).GetPoints().GetPoint(2))
print(len(arr))
x=[]
y=[]
z=[]
for i in arr:
    x.append(i[0])
    y.append(i[1])
    z.append(i[2])
print("x=",x,";")
print("y=",y,";")
print("z=",z,";")
cell=vtk.vtkCell()


cv2.waitKey(0)

sphere = vtk.vtkSphereSource()
sphere.SetPhiResolution(21)
sphere.SetThetaResolution(21)
sphere.SetRadius(.08)
pointMapper = vtk.vtkGlyph3DMapper()
pointMapper.SetInputConnection(connectivityFilter.GetOutputPort())
pointMapper.SetSourceConnection(sphere.GetOutputPort())
pointMapper.ScalingOff()
pointMapper.ScalarVisibilityOff()
pointActor = vtk.vtkActor()
pointActor.SetMapper(pointMapper)
pointActor.GetProperty().SetDiffuseColor(colors.GetColor3d("red"))
# pointActor.GetProperty().SetSpecular(.6)
# pointActor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
# pointActor.GetProperty().SetSpecularPower(100)



mapper1=vtk.vtkPolyDataMapper()
mapper1.SetInputConnection(connectivityFilter.GetOutputPort())

actor1=vtk.vtkActor()
actor1.SetMapper(mapper1)
actor1.GetProperty().SetOpacity(0.9)
actor1.GetProperty().SetColor(colors.GetColor3d("banana"))
actor1.GetProperty().EdgeVisibilityOn()
actor1.GetProperty().EdgeVisibilityOn()

connectivityFilter.AddSpecifiedRegion(1)
connectivityFilter.Update()
mapper2=vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(connectivityFilter.GetOutputPort())

actor2=vtk.vtkActor()
actor2.SetMapper(mapper1)
actor2.GetProperty().SetOpacity(0.3)
actor2.GetProperty().SetColor(colors.GetColor3d("Banana"))



ren1.AddActor(actor1)
# ren1.AddActor(actor2)
ren1.AddActor(pointActor)
ren1.SetBackground(colors.GetColor3d("white"))





renWin.Render()
iren.Start()

