import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sympy.solvers import solve
from sympy import Symbol
import os

class CrackPoint:
    def __init__(self,pointList,z):
        self.points=[]
        for i in pointList:
            self.points.append((i[0][0],i[0][1],z))
    def findFarthest(self):
        self.farthestPoint=[]
        farthestLength=0
        temp=[]
        for i in self.points:
            for j in self.points:
                if (i[0]-j[0])**2+(i[1]-j[1])**2>farthestLength:
                    farthestLength=(i[0]-j[0])**2+(i[1]-j[1])**2
                    temp.append(i)
                    temp.append(j)
        self.farthestPoint.append(temp[-2])
        self.farthestPoint.append(temp[-1])

class CrackPointCloud:
    def __init__(self):
        self.pointCloud=[]

    def addPoint(self,points:CrackPoint):
        for i in points:
            self.pointCloud.append(i)

    def solve_tuoyuan(x, y):
        x0, y0 = x.mean(), y.mean()
        D1 = np.array([(x - x0) ** 2, (x - x0) * (y - y0), (y - y0) ** 2]).T
        D2 = np.array([x - x0, y - y0, np.ones(y.shape)]).T
        S1 = np.dot(D1.T, D1)
        S2 = np.dot(D1.T, D2)
        S3 = np.dot(D2.T, D2)
        T = -1 * np.dot(np.linalg.inv(S3), S2.T)
        M = S1 + np.dot(S2, T)
        M = np.array([M[2] / 2, -M[1], M[0] / 2])
        lam, eigen = np.linalg.eig(M)
        cond = 4 * eigen[0] * eigen[2] - eigen[1] ** 2
        A1 = eigen[:, cond > 0]
        A = np.vstack([A1, np.dot(T, A1)]).flatten()
        A3 = A[3] - 2 * A[0] * x0 - A[1] * y0
        A4 = A[4] - 2 * A[2] * y0 - A[1] * x0
        A5 = A[5] + A[0] * x0 ** 2 + A[2] * y0 ** 2 + A[1] * x0 * y0 - A[3] * x0 - A[4] * y0
        A[3] = A3
        A[4] = A4
        A[5] = A5
        return A
