import cv2
import numpy as np


def gray_scale(image):
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rows, cols = image.shape
    flat_gray = image.reshape((cols * rows,)).tolist()
    A = min(flat_gray)
    B = max(flat_gray)
    print('A = %d,B = %d' % (A, B))
    output = np.uint8(255 / (B - A) * (image - A) + 0.5)
    return output


def my_gray_scale(image, T, M):
    copy = image.copy()
    print('T = %d,M = %d' % (T, M))
    for i in range(copy.shape[0]):
        for j in range(copy.shape[1]):
            if copy[i, j] > T:
                copy[i, j] = np.uint8(255)
            if copy[i, j] < M:
                copy[i, j] = np.uint8(0)

    return copy


# 高斯模板
def imgGaussian(sigma):
    img_h = img_w = 2 * sigma + 1
    gaussian_mat = np.zeros((img_h, img_w))
    # max_probability=np.exp(-0.5 * (0 ** 2 + 0 ** 2) / (sigma ** 2))
    for x in range(-sigma, sigma + 1):
        for y in range(-sigma, sigma + 1):
            probability = np.exp(-0.5 * (x ** 2 + y ** 2) / (sigma ** 2))
            gaussian_mat[x + sigma][y + sigma] = 255 * (1 - probability / 1)

    return gaussian_mat

def fusion_crack(img,hight,width,threshold):
    dst_Gauss = cv2.GaussianBlur(img, (3, 3), 0)  # 高斯模糊
    # cv2.imshow("Gaussian_Blur", dst_Gauss)
    retval, dst_OSTU = cv2.threshold(dst_Gauss, 0, 255, cv2.THRESH_OTSU)  # 方法选择为THRESH_OTSU
    # cv2.imshow("THRESH_OTSU", dst_OSTU)
    # cv2.imshow("OTSU", dst_OSTU)
    # print("threshole:", retval)
    dst_gray = my_gray_scale(dst_Gauss, retval, 10)
    # cv2.imshow("gray_scale", dst_gray)
    kernel = np.ones((hight, width), np.uint8)
    erosion = cv2.erode(dst_gray, kernel)
    # dilation = cv2.dilate(erosion, kernel, iterations=1)
    h=len(img)
    w=len(img[0])
    for i in range(h):
        for j in range(w):
            if erosion[i][j]!=dst_gray[i][j]:
                img[i][j]=0


if __name__ == "__main__":
    img = cv2.imread("0-00203.bmp")
    # print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('original_image', img)
    fusion_crack(img,15,2,0)
    cv2.imshow('fusion_crack', img)

    cv2.waitKey()
    cv2.destroyAllWindows()