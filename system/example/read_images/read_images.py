import numpy as np
import cv2
import os
import math

def read_images(path,start,end):
    res=[]
    numOfFiles = len(os.listdir(path))
    for index, filename in enumerate(sorted(os.listdir(path))[start:end + 1]):
        img_path=os.path.join(path,filename)
        img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        if index==0:
            res.append(np.zeros(img.shape))
            res.append(np.zeros(img.shape))
        res.append(img)
        if index==numOfFiles-1:
            res.append(np.zeros(img.shape))
            res.append(np.zeros(img.shape))
    res=np.asarray(res)
    # res.reshape(())
    print(res.shape)
    res=res.astype(np.uint8)
    return res,img.shape[0],img.shape[1],0,min(end-start,len(os.listdir(path))-1)

def read_images_CT(path,start,end):
    res=[]
    numOfFiles=len(os.listdir(path))
    for index,filename in enumerate(sorted(os.listdir(path))[start:end+1]):
        img_path=os.path.join(path,filename)
        img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        res.append(img)
        if index<=1 or index>=numOfFiles-2:
            for _ in range(20):
                res.append(img)
    res=np.asarray(res)
    # res.reshape(())
    print(res.shape)
    res=res.astype(np.uint8)
    return res,img.shape[0],img.shape[1],0,min(end-start,len(os.listdir(path))-1)

def read_images_cube(path,start,end):
    img, img_width, img_height, startNum, endNum = read_images(path, start, end)
    x=img.shape[0]
    y=img.shape[1]
    z=img.shape[2]
    l=max(x,y,z)
    x=math.ceil((l-x)/2)
    y = math.ceil((l - y) / 2)
    z = math.ceil((l - z) / 2)
    try:
        img=np.pad(img,((x,x),(y,y),(z,z)),'constant')
    except Exception as e:
        print(str(e))
    # img=np.flip(img,0)
    return img,img.shape[0],img.shape[1],0,img.shape[2]


if __name__=="__main__":
    path = r'/Users/liaoxiaoqing/Downloads/carck_detect_system-master/precombust'
    read_images(path,1,5)