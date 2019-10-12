import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from imagePreprocess_Function import fusion_crack
from cal_nearest_point import cal_nearest_points

def cal_box_proportion(box):
    length=math.sqrt((box[0][0]-box[1][0])**2 + (box[0][1]-box[1][1])**2)+3
    width=math.sqrt((box[1][0]-box[2][0])**2 + (box[1][1]-box[2][1])**2)+3
    res1=length/width
    if(res1>=1):
        return res1
    return width/length

def nothing(x):
    pass

# cv2.namedWindow('res')
# cv2.createTrackbar('max','res',0,255,nothing)
img = cv2.imread("0-00203.bmp")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# fusion_crack(img,3,1,0)
# plt.subplot(111)
# plt.imshow(img,cmap="gray")
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.show()
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(img,100,300)
plt.subplot(122)
cv2.imshow("canny",canny)
# ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
image, contours, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
crack_proportion=1
crack_box=1
crack_index=-1
crack_points=1
setIn=set()
for i,c in enumerate(contours):
    # find minimum area
    rect = cv2.minAreaRect(c)
    # print(i,":",c)
    # calculate coordinates of the minimum area rectangle
    box = cv2.boxPoints(rect)
    # normalize coordinates to integers
    box = np.int0(box)

    current_proportion=cal_box_proportion(box)
    if(current_proportion>crack_proportion):
        crack_proportion=current_proportion
        crack_box=box
        crack_index=i
        crack_points=c
        setIn.clear()
        setIn.add(i)
print(len(setIn))
for _ in range(20):
    for i,c in enumerate(contours):
        if i in setIn:
            continue
        if len(crack_points)/len(c)>2 and cal_nearest_points(c,crack_points)<15:
            crack_points=np.vstack((crack_points,c))
            setIn.add(i)
    print(_+1,':',len(setIn))
rect = cv2.minAreaRect(crack_points)
box = cv2.boxPoints(rect)
crack_box = np.int0(box)







# draw contours
img = cv2.imread("0-00203.bmp")
cv2.drawContours(img, [crack_box], 0, (0, 0, 255), 1)
print(crack_index)
print(len(contours[crack_index]))
print(type(contours[crack_index]))
# print(contours[crack_index])
# for i in contours[crack_index]:
#     print(i[0])
print([crack_box])


cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
cv2.imshow("contours", img)
cv2.waitKey()
cv2.destroyAllWindows()