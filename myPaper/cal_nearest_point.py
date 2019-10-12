import math

def cal_nearest_point(point_A,point_B):
    return math.sqrt((point_A[0]-point_B[0])**2+(point_A[1]-point_B[1])**2)

def cal_nearest_points(cloud_A,cloud_B):
    min=9999999
    for A in cloud_A:
        for B in cloud_B:
            # print(A[0], B[0])
            if cal_nearest_point(A[0],B[0])<min:
                min=cal_nearest_point(A[0],B[0])
    return min