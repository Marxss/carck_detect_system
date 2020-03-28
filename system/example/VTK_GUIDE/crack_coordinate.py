import vtk
import cv2
from fit_plane import fit_plane

colors = vtk.vtkNamedColors()
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
# print("x=",x,";")
# print("y=",y,";")
# print("z=",z,";")

# create source
points = vtk.vtkPoints()
vertices = vtk.vtkCellArray()
for index,i in enumerate(arr):
    # print(i)
    p=i
    pid = [0]
    pid[0] = points.InsertNextPoint(p)
    # print(pid)
    vertices.InsertNextCell(1, pid)


# Create a polydata object
point = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and topology of the polydata
point.SetPoints(points)
point.SetVerts(vertices)

# Visualize
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(point)

# actor
point_actor = vtk.vtkActor()
point_actor.SetMapper(mapper)
point_actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
point_actor.GetProperty().SetPointSize(2)



a,b,c,d,e,f,g,h,i,j=[-0.020340259251952153, -0.013760746890380537, -2.9658989938576674, -0.007123131059559554, 0.00023497385314377874, 1.4561288032929662e-05, 2.951499531936364, 2.8213808201505954, 486.38118554632064, -80467.28854785529]


quadric = vtk.vtkQuadric()
# F(x,y,z) = a0*x^2 + a1*y^2 + a2*z^2 + a3*x*y + a4*y*z + a5*x*z + a6*x + a7*y + a8*z + a9
quadric.SetCoefficients(a,b,c,2*d,2*f,2*e,2*g,2*h,2*i,j)

# The sample function generates a distance function from the implicit
# function. This is then contoured to get a polygonal surface.
sample = vtk.vtkSampleFunction()
sample.SetImplicitFunction(quadric)
center=[91.89398545346178, 157.565675900567, 164.00026179252038]
r=40
sample.SetModelBounds(center[0]-r, center[0]+r, center[1]-r,center[1]+ r,center[2] -r,center[2]+ r)
sample.SetSampleDimensions(400, 400, 400)
sample.ComputeNormalsOff()

# contour
surface = vtk.vtkContourFilter()
surface.SetInputConnection(sample.GetOutputPort())
surface.SetValue(0, 0.0)

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetColor(colors.GetColor3d('AliceBlue'))
actor.GetProperty().SetEdgeColor(colors.GetColor3d('SteelBlue'))
actor.GetProperty().SetOpacity(0.3)

args=fit_plane(x,y,z)
a,b,c,d=(args[0],args[1],1,args[2])

planeSource=vtk.vtkPlane()
planeSource.SetOrigin(0, 0, d)
# planeSource.SetCenter(165, 165*0.66, d)
planeSource.SetNormal(a+0.01, b, -1)
# planeSource.SetPoint1(100, 100*0.66,d)
# planeSource.SetPoint2(100, 100*0.66,d)
# planeSource.Update()

sample = vtk.vtkSampleFunction()
sample.SetImplicitFunction(planeSource)
center=[91.89398545346178, 157.565675900567, 164.00026179252038]
r=45
sample.SetModelBounds(center[0]-r, center[0]+r, center[1]-r,center[1]+ r,center[2] -r,center[2]+ r)
sample.SetSampleDimensions(430, 430, 430)
sample.ComputeNormalsOff()

# contour
plane_surface = vtk.vtkContourFilter()
plane_surface.SetInputConnection(sample.GetOutputPort())
plane_surface.SetValue(0, 0.0)

# Create a mapper and actor
plane_mapper = vtk.vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_surface.GetOutputPort())

plane_actor = vtk.vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(colors.GetColor3d("Banana"))
plane_actor.GetProperty().SetEdgeColor(colors.GetColor3d('SteelBlue'))
plane_actor.GetProperty().SetOpacity(0.3)

cutPlane = vtk.vtkTriangleFilter()
cutPlane.SetInputConnection(plane_surface.GetOutputPort())
cutPlane.Update()
print(surface)
print(plane_surface)

vtkIntersectionPolyDataFilter=vtk.vtkIntersectionPolyDataFilter()
vtkIntersectionPolyDataFilter.SetInputConnection(0,surface.GetOutputPort())
vtkIntersectionPolyDataFilter.SetInputConnection(1,cutPlane.GetOutputPort())
vtkIntersectionPolyDataFilter.Update()
# print(vtkIntersectionPolyDataFilter)
crack_mapper = vtk.vtkPolyDataMapper()
crack_mapper.SetInputConnection(vtkIntersectionPolyDataFilter.GetOutputPort())
crack_actor = vtk.vtkActor()
crack_actor.SetMapper(crack_mapper)
crack_actor.GetProperty().SetColor(colors.GetColor3d('Black'))

vtkIntersectionPolyDataFilter=vtkIntersectionPolyDataFilter.GetOutput()

print(vtkIntersectionPolyDataFilter.GetNumberOfCells())
arr=[]

print(vtkIntersectionPolyDataFilter.GetNumberOfLines())
arr=vtkIntersectionPolyDataFilter.GetPoints()
print(arr)
s=set()
for i in range(arr.GetNumberOfPoints()):
    print(arr.GetPoint(i))
    s.add(arr.GetPoint(i))
s=sorted(list(s),key=lambda x:x[0])
print(len(s))
s=s[ : : 165]

def dist(x,y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])+abs(x[2]-y[2])


points=set(s)
res=[]
res.append(points.pop())
for i in range(len(points)-1):
    orign=res[-1]
    nearstDist=99999999999999
    nearstPoint=None
    for point in points:
        if dist(orign,point)<nearstDist:
            nearstDist=dist(x,y)
            nearstPoint=point
    res.append(point)
    points.discard(point)



filename = r'D:\crack_grow\crack.txt'
with open(filename, 'w') as file_object:
    for i in res:
        file_object.write("{:.8f}  {:.8f}  {:.8f}  1\n".format(i[0],i[1],i[2]))
# filename = r'D:\crack_order.txt'
# order=[1,2,4,6,8,12,11,10,9,7,5,3]
# with open(filename, 'w') as file_object:
#     for i in order:
#         file_object.write("{} {} {} 1\n".format(res[i-1][0],res[i-1][1],res[i-1][2]))







# ren1.AddActor(crack_actor)
# # ren1.AddActor(plane_actor)
# ren1.AddActor(point_actor)
# # ren1.AddActor(actor)
# ren1.SetBackground(colors.GetColor3d("white"))

# renWin.Render()
# iren.Start()

