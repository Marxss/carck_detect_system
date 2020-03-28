import cv2
import numpy as np
def initialize(width, height, x_center, y_center, radius):
    phi = np.zeros((width,height)).astype(np.uint8)
    for i in range(width):
        for j in range(height):
            I = -np.sqrt((i - x_center)**2 + (j - y_center)**2) +radius
            if I>=0:
                phi[i, j]=200
            elif I>-1:
                phi[i, j] = 128
    # phi[10:20,10:200]=10
    return phi

product=initialize(360,360,180,180,100)
# product=np.zeros((256,256))


cv2.imshow("1p",product)
cv2.waitKey(0)


cv2.imwrite("0.jpg",product)
