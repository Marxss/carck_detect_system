import numpy as np
import cv2
import vtk
import os

def read_images(path,start,end):
    res=[]
    for filename in sorted(os.listdir(path))[start:end+1]:
        img_path=os.path.join(path,filename)
        img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        res.append(img)
    res=np.asarray(res)
    # res.reshape(())
    print(res.shape)
    res=res.astype(np.uint8)
    return res,img.shape[0],img.shape[1],0,min(end-start,len(os.listdir(path))-1)

if __name__=="__main__":
    path = r'/Users/liaoxiaoqing/Downloads/carck_detect_system-master/precombust'
    read_images(path,1,5)