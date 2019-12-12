import cv2
import numpy as np

def otsu_threshold(img:np.ndarray):
    output=np.zeros(img.shape,dtype=np.uint8)
    for i in range(img.shape[2]):
        ret,thr=cv2.threshold(img[:,:,i],0,255,cv2.THRESH_OTSU)
        # print(img[:,:,i].shape,img.dtype)
        # cv2.imshow(str(i), img[:,:,i])
        output[:, :, i]=thr.astype(np.float32)
    return output.astype(np.float32)
