import itk
import vtk

imageFileName = '0-00203.bmp'

Dimension = 2
PixelType = itk.UC
ImageType = itk.Image[PixelType, Dimension]

reader = itk.ImageFileReader[ImageType].New()
reader.SetFileName(imageFileName)

itkToVtkFilter = itk.ImageToVTKImageFilter[ImageType].New()
itkToVtkFilter.SetInput(reader.GetOutput())

itkToVtkFilter.Update()
myvtkImageData = itkToVtkFilter.GetOutput()
print(myvtkImageData)
