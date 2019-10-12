import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def cal_box_proportion(box):
    length=math.sqrt((box[0][0]-box[1][0])**2 + (box[0][1]-box[1][1])**2)+3
    width=math.sqrt((box[1][0]-box[2][0])**2 + (box[1][1]-box[2][1])**2)+3
    res1=length/width
    if(res1>=1):
        return res1
    return width/length

def nothing(x):
    pass

cv2.namedWindow('res',flags=0)
cv2.createTrackbar('max','res',0,500,nothing)
cv2.createTrackbar('min','res',0,500,nothing)
maxVal=200
minVal=100
# plt.ion()




while(1):
    if cv2.waitKey(20) & 0xFF == 27:
        break

    img = cv2.imread("0-00203.bmp")
    plt.subplot(221)
    plt.imshow(img)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    maxVal = cv2.getTrackbarPos('min', 'res')
    minVal = cv2.getTrackbarPos('max', 'res')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if minVal < maxVal:
        canny = cv2.Canny(gray, minVal, maxVal)
        plt.subplot(222)
        plt.imshow(canny,cmap='gray')
        plt.title('Canny Image'), plt.xticks([]), plt.yticks([])
    else:
        canny = cv2.Canny(gray, minVal, maxVal)
        # (r, g, b) = cv2.split(canny)
        # canny = cv2.merge([b, g, r])
        plt.subplot(222)
        plt.imshow(canny)
        plt.title('Canny Image'), plt.xticks([]), plt.yticks([])

    # ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    image, contours, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    crack_proportion=1
    crack_box=1
    crack_index=-1
    for i,c in enumerate(contours):
        # find minimum area
        rect = cv2.minAreaRect(c)
        # calculate coordinates of the minimum area rectangle
        box = cv2.boxPoints(rect)
        # normalize coordinates to integers
        box = np.int0(box)

        current_proportion=cal_box_proportion(box)
        if(current_proportion>crack_proportion):
            crack_proportion=current_proportion
            crack_box=box
            crack_index=i

    # draw contours
    cv2.drawContours(img, [crack_box], 0, (0, 0, 255), 1)
    print(crack_index)
    print(len(contours[crack_index]))
    print(type(contours[crack_index]))
    # print(contours[crack_index])
    for i in contours[crack_index]:
        print(i[0])
    print([crack_box])

    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

    plt.subplot(223)
    plt.imshow(img)
    plt.title('Contours Image'), plt.xticks([]), plt.yticks([])
    plt.show()

    cv2.waitKey()

cv2.destroyAllWindows()