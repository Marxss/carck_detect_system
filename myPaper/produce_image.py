import matplotlib.pyplot as plt
import numpy as np
import cv2
#ipython %matplotlib inline
from tqdm import tqdm
from random import randint

def crop(img):
    l=[]
    has=dict()
    for line in img:
        t=[]
        for index,item in enumerate(line):
            if item!=255:
                t.append(index)
            if item not in has.keys():
                has[item]=1
            else:
                has[item] += 1
        if t:
            l.append(sum(t)/len(t))
    x_average=int(sum(l)/len(l))
    print(x_average,has)
    img=img[0:888,x_average-444:x_average+444]
    #翻转二值
    for line in img:
        for index,item in enumerate(line):
            if line[index]>=220:
                line[index]=255-line[index]

    return img


gear_img = cv2.imread("gearM4X12.JPG",1)
gear_img = cv2.cvtColor(gear_img,cv2.COLOR_BGR2GRAY)
gear_img=crop(gear_img)
gear_img=cv2.copyMakeBorder(gear_img, 300, 300, 300, 300, cv2.BORDER_CONSTANT, value=(0, 0, 0))
background_img=cv2.imread("background2.bmp",1)
background_img=cv2.resize(background_img,(2*512, 2*512), interpolation = cv2.INTER_CUBIC)
background_img = cv2.cvtColor(background_img,cv2.COLOR_BGR2GRAY)
plt.subplot(131)
# plt.imshow(gear_img,cmap=plt.cm.gray)
plt.imshow(gear_img,cmap="gray")
plt.axis("off")
plt.subplot(132)
# orign_lenna_img = cv2.cvtColor(background_img,cv2.COLOR_BGR2RGB)
plt.imshow(background_img,cmap="gray")
plt.axis("off")

product=cv2.addWeighted(cv2.resize(gear_img, (1024,1024), interpolation=cv2.INTER_AREA), 0.8, background_img, 0.2, 0)
plt.subplot(133)
plt.imshow(product,cmap="gray")
plt.axis("off")
cv2.imwrite("product.bmp",product)
print(gear_img,background_img)

print(len(gear_img),len(gear_img[0]),len(background_img),len(background_img[0]))


#plt.show()


background_tmp=background_img
gear_img=cv2.resize(gear_img, (1024, 1024), interpolation=cv2.INTER_AREA)
for n in tqdm(range(150)):
    for i in range(len(background_tmp)):
        for j in range(len(background_tmp[i])):
            if background_img[i][j]>100:
                background_tmp[i][j]+=randint(-5,5)
    product = cv2.addWeighted(gear_img, 0.8, background_img,0.2, 0)
    #生成裂纹
    center_num=50
    skip=30
    if n in range(center_num-skip,center_num+skip):
        length=skip-abs(center_num-n)
        for i in range(length):
            product[753-i][421+i]=randint(0,10)


    fileName="gear_CT_slices\\"+str(n)+".bmp"
    cv2.imwrite(fileName, product)