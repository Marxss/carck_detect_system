import os
import cv2
import sys
from tqdm import tqdm

path="gear_CT_slices\\"
outPath="xiangpi\\"
for filename in tqdm(os.listdir(path)):
    # print(filename)
    background_img = cv2.imread(path+filename)
    #cv2.imshow("Image",background_img)
    background_img=cv2.resize(background_img,(512, 512), interpolation = cv2.INTER_CUBIC)
    background_img = cv2.cvtColor(background_img,cv2.COLOR_BGR2GRAY)
    h=background_img.shape[0]
    w=background_img.shape[1]
    for i in range(h):
        for j in range(w):
            background_img[i][j]=255-background_img[i][j]

    newFileName=filename.replace(".jpg",".bmp")
    cv2.imwrite(outPath+newFileName, background_img)

# background_img=cv2.imread("F:\\xiangpi\\0000.jpg")
# print(background_img)
# background_img=cv2.resize(background_img,(2*512, 2*512), interpolation = cv2.INTER_CUBIC)
# background_img = cv2.cvtColor(background_img,cv2.COLOR_BGR2GRAY)
# cv2.imwrite("150.bmp", background_img)