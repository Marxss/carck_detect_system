import vtk

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