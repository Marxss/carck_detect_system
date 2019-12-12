import cv2
import numpy as np

img = cv2.imread("D:\\carck_detect_system\\myPaper\\gear_CT_slices\\0.bmp")
img= np.zeros(img.shape, dtype=np.uint8)
cv2.imwrite("black.bmp",img)