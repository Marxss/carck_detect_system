import cv2
import numpy as np
import math


def gray_scale(image):
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rows, cols = image.shape
    flat_gray = image.reshape((cols * rows,)).tolist()
    A = min(flat_gray)
    B = max(flat_gray)
    print('A = %d,B = %d' % (A, B))
    output = np.uint8(255 / (B - A) * (image - A) + 0.5)
    return output

def my_gray_scale(image,T,M):
    copy=image.copy()
    print('T = %d,M = %d' % (T, M))
    for i in range(copy.shape[0]):
        for j in range(copy.shape[1]):
            if copy[i,j]>T:
                copy[i, j]=np.uint8(255)
            if copy[i,j]<M:
                copy[i, j]=np.uint8(0)

    return copy

# 高斯模板
def imgGaussian(sigma):
    img_h = img_w = 2 * sigma + 1
    gaussian_mat = np.zeros((img_h, img_w))
    # max_probability=np.exp(-0.5 * (0 ** 2 + 0 ** 2) / (sigma ** 2))
    for x in range(-sigma, sigma + 1):
        for y in range(-sigma, sigma + 1):
            probability=np.exp(-0.5 * (x ** 2 + y ** 2) / (sigma ** 2))
            gaussian_mat[x + sigma][y + sigma] =255*(1-probability/1)

    return gaussian_mat

# 计算相似系数矩阵
def cal_similarity_coefficient_mat(img,model,bins,sigma):
    copy = img.copy()
    print(model)
    model_hist, model_bin = np.histogram(model.ravel(), bins**2, [0, 256])
    print(model_hist)
    for i in range(sigma,img.shape[0]-sigma):
        for j in range(sigma,img.shape[1]-sigma):
            hist, bin = np.histogram(copy[i-sigma:i+sigma,j-sigma:j+sigma].ravel(), bins**2, [0, 256])
            # print(hist)
            copy[i,j]=np.sum(np.sqrt(model_hist*hist))
    return copy



if __name__=="__main__":
    img = cv2.imread("0-00203.bmp")
    # print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('original_image', img)
    dst_Gauss = cv2.GaussianBlur(img, (3,3), 0) #高斯模糊
    cv2.imshow("Gaussian_Blur", dst_Gauss)
    retval, dst_OSTU = cv2.threshold(dst_Gauss, 0, 255, cv2.THRESH_OTSU)  #方法选择为THRESH_OTSU
    # for line in dst_OSTU:
    #     for i in line:
    #         if i!=0 and i!=255:
    #             print(i)
    cv2.imshow("THRESH_OTSU", dst_OSTU)
    # cv2.imshow("OTSU", dst_OSTU)
    print("threshole:",retval)
    dst_gray = my_gray_scale(dst_Gauss,retval,10)
    cv2.imshow("gray_scale",dst_gray)
    # print(dst_OSTU==dst_gray)
    # for i in range(512):
    #     for j in range(512):
    #         if dst_OSTU[i][j]!=dst_gray[i][j]:
    #             print(1)
    # print(imgGaussian(6))

    #高斯模板
    # similarity_coefficient_mat=cal_similarity_coefficient_mat(dst_gray,imgGaussian(6),4,6)
    # cv2.imshow("similarity_coefficient_mat", similarity_coefficient_mat)
    # retval_2, dst_OSTU_2 = cv2.threshold(similarity_coefficient_mat, 0, 255, cv2.THRESH_OTSU) #方法选择为THRESH_OTSU
    # similarity_coefficient_mat_2 = my_gray_scale(similarity_coefficient_mat, retval_2, 10)
    # cv2.imshow("similarity_coefficient_mat_2", similarity_coefficient_mat_2)
    # # cv2.imshow("similarity_coefficient_mat", gray_scale(similarity_coefficient_mat))

    #形态学操作
    size=16
    # kernel = np.ones((size, size), np.uint8)
    kernel=np.zeros((size,size),np.uint8)
    for i in range(size):
        if i!=0 and i!=size-1:
            kernel[i][i-1]=1
            kernel[i][i] = 1
            kernel[i][i+1] = 1
        elif i==0:
            kernel[i][i + 1] = 1
            kernel[i][i] = 1
        else:
            kernel[i][i - 1] = 1
            kernel[i][i] = 1
    kernel=np.rot90(kernel)
    
    # erosion = cv2.erode(dst_gray, kernel)
    # dilation = cv2.dilate(erosion, kernel, iterations=1)
    erosion1 = cv2.erode(dst_gray, kernel)
    # cv2.imshow("erosion", erosion)
    dilation1 = cv2.dilate(erosion1, kernel, iterations=1)
    # cv2.imshow("dilation", dilation)
    cv2.imshow("first", dilation1)

    kernel = np.ones((size, size), np.uint8)

#第二轮膨胀腐蚀--------------------------------------------------
    kernel = np.zeros((size, size), np.uint8)
    for i in range(size):
        if i != 0 and i != size - 1:
            kernel[i][i - 1] = 1
            kernel[i][i] = 1
            kernel[i][i + 1] = 1
        elif i == 0:
            kernel[i][i + 1] = 1
            kernel[i][i] = 1
        else:
            kernel[i][i - 1] = 1
            kernel[i][i] = 1

    # erosion = cv2.erode(dst_gray, kernel)
    # dilation = cv2.dilate(erosion, kernel, iterations=1)
    erosion2 = cv2.erode(dilation1, kernel)
    # cv2.imshow("erosion", erosion2)
    dilation2 = cv2.dilate(erosion2, kernel, iterations=1)
    # cv2.imshow("dilation", dilation2)

#第三轮膨胀腐蚀（上下卷积核）--------------------------------------------------
    size3=10
    kernel = np.ones((size3, size3), np.uint8)
    erosion3= cv2.erode(dilation1, kernel,iterations=1)
    cv2.imshow("erosion", erosion3)
    dilation3 = cv2.dilate(erosion3, kernel, iterations=1)
    # kernel = np.ones((1, 4), np.uint8)
    # dilation3 = cv2.erode(dilation3, kernel, iterations=1)
    print(dilation3)
    print(img)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if dilation3[i][j]<20:
                print(img[i][j])
                img[i][j]=0
                # img[i][j+1] = 0
                # img[i][j-1] = 0
                # print('1')

    cv2.imshow("output", img)
    cv2.imshow("dilation", dilation3)
    cv2.imwrite('preprocess.bmp',dilation3)


cv2.waitKey(0)
cv2.destroyAllWindows()