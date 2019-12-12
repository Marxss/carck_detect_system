from vtk import *

v16=vtkBMPReader()
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix("D:\slice_data\\bmp-lungu\\200503180")
v16.SetFilePattern("%s%03d.bmp")
i=0
v16.SetDataExtent (0+i,452-i,0+i,452-i,19,83)
v16.SetDataSpacing(1,1,1)
v16.Update()

coronalElements=[[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]]#平行于XZ平面
sagittalElements=[[0,0,-1,0],[1,0,0,0],[0,-1,0,0],[0,0,0,1]]#平行于YZ平面
horizontalElements=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]#平行于XY平面
coronalElements=[i for j in coronalElements for i in j]
sagittalElements=[i for j in sagittalElements for i in j]
horizontalElements=[i for j in horizontalElements for i in j]

center=[250,250,1]
resliceAxes=vtkMatrix4x4()
resliceAxes.DeepCopy(coronalElements)
resliceAxes.SetElement(0,3,center[0])
resliceAxes.SetElement(1,3,center[1])
resliceAxes.SetElement(2,3,center[2])

reslice=vtkImageReslice()
reslice.SetInputConnection(v16.GetOutputPort())
reslice.SetOutputDimensionality(2)
reslice.SetResliceAxes(resliceAxes)
reslice.SetInterpolationModeToLinear()

# imageViewer=vtkImageViewer2()
# renderWindowInteractor=vtkRenderWindowInteractor()
# imageViewer.SetInputConnection(reslice.GetOutputPort())
# imageViewer.SetupInteractor(renderWindowInteractor)
# imageViewer.SetColorLevel(100)
# imageViewer.SetColorWindow(200)
#
# imageViewer.Render()
# renderWindowInteractor.Start()