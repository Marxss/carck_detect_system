# -coding-:-utf8-
"""
Author: Victoria
E-mail: wyvictoria1@gmail.com
Date: 9/3/2017
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy.ndimage as nd
from read_images import read_images
import math
import datetime
import cv2

def CV_once(img, LSF, time_step, mu,nu, v, lambda1, lambda2, epison):
    # time_setp:步长
    # epison:计算粒度，越小越精密
    # mu:周长系数
    # v:减去常数项
    Drc = (epison / math.pi) / (epison * epison + LSF * LSF)  #LSF离零水平集越远，作用力越小
    Hea = 0.5 * (1 + (2 / math.pi) * np.arctan(LSF / epison))
    s1 = Hea * img
    s2 = (1 - Hea) * img
    s3 = 1 - Hea
    C1 = s1.sum() / Hea.sum()
    C2 = s2.sum() / s3.sum()
    CVterm = Drc * (-1 * (img - C1) * (img - C1) + 1 * (img - C2) * (img - C2))

    Iz, Iy, Ix = np.gradient(LSF)
    s = np.sqrt(Ix * Ix + Iy * Iy + Iz*Iz)
    Nx = Ix / (s + 0.000001)
    Ny = Iy / (s + 0.000001)
    Nz= Iz/(s+0.000001)
    Nxz, Nxy, Nxx = np.gradient(Nx)
    Nyz, Nyy, Nyx = np.gradient(Ny)
    Nzz, Nzy, Nzx = np.gradient(Nz)
    cur = Nxx + Nyy + Nzz
    Length = nu * Drc * cur

    Lap = cv2.Laplacian(LSF, -1)
    penalty = mu * (Lap - cur)

    LSF = LSF + time_step * (CVterm+Length+penalty)
    print("CVterm:",CVterm.sum(),"  maxNum:",LSF.max(),"  minNum:",LSF.min())

    return LSF

def CV(img, LSF, max_iter, time_step, mu, v, lambda1, lambda2, epison):

    for iter in range(max_iter):
        LSF=CV_once(img, LSF, time_step, mu, v, lambda1, lambda2, epison)

    return LSF



def acwe(Img, phi0, max_iter, time_step, mu, v, lambda1, lambda2, epison):
    """
    Input:
	    Img: array_like, the input gray image[0,255]
	    phi: nparray, the initial curve function(level set function)
	    max_iter: int, the max number of iterations
	    time_step: float, learning rate
	    mu: coefficiency of  length term
	    v: coefficiency of  area term
	    lambda1, lambda2: coefficiency of "fitting" term(Image energy)
    """
    print(time_step, mu, v, lambda1, lambda2)
    phi = phi0

    for iter in range(max_iter):
        idx = np.flatnonzero(np.logical_and(phi <= 21.5, phi >= -21.5))
        # print(idx)
        if len(idx) > 0:
            print('iteration: {0}   len(idx): {1}'.format(iter+1,len(idx)))
            phi = NeumannBoundCond(phi)
            Heaviside = 0.5 * (1 + 2 / np.pi * (np.arctan(phi / epison)))
            delta = (epison / np.pi) / (epison ** 2 + phi ** 2)
            """
            Only update the neighbor of curve
            """
            # Internal force
            length_term = curvature_central(phi)
            # Image force
            inside_idx = np.flatnonzero(phi >= 0)
            outside_idx = np.flatnonzero(phi < 0)
            """c1 = np.mean(Img.flat[inside_idx]) #mean value inside curve
            c2 = np.mean(Img.flat[outside_idx]) #mean value outside curve"""
            c1 = np.sum(Img.flat[inside_idx]) / (len(inside_idx) + 0.00001)  # exterior mean
            c2 = np.sum(Img.flat[outside_idx]) / (len(outside_idx) + 0.00001)  # interior mean
            print("c1:{}, c2:{}".format(c1, c2))
            image_force = - lambda1 * (Img.flat[idx] - c1) ** 2 + lambda2 * (Img.flat[idx] - c2) ** 2
            print("image_force", np.max(image_force))
            gradient = delta.flat[idx] * (mu * length_term.flat[idx] - v + image_force / np.max(image_force))

            phi.flat[idx] = time_step * gradient
            print("phi:{}".format(np.max(phi)))

    return phi


def NeumannBoundCond(f):
    """
    Change function f to satisfy Neumann Boundary Condition
    """
    g = f
    # 8 corner
    g[0, 0,0] = g[2, 2,0]
    g[0, -1,0] = g[2, -3,0]
    g[-1, 0,0] = g[-3, 2,0]
    g[-1, -1,0] = g[-3, -3,0]
    g[0, 0, -1] = g[2, 2, -1]
    g[0, -1, -1] = g[2, -3, -1]
    g[-1, 0, -1] = g[-3, 2, -1]
    g[-1, -1, -1] = g[-3, -3, -1]
    # # first row and last row
    # g[0, 1:-1,0] = g[2, 1:-1,0]
    # g[0, 1:-1, -1] = g[2, 1:-1, -1]
    # g[-1, 1:-1,0] = g[-3, 1:-1,0]
    # g[-1, 1:-1, -1] = g[-3, 1:-1, -1]
    # # first column and last column
    # g[1:-1, 0,0] = g[1:-1, 2,0]
    # g[1:-1, 0, -1] = g[1:-1, 2, -1]
    # g[1:-1, -1,0] = g[1:-1, -3,0]
    # g[1:-1, -1, -1] = g[1:-1, -3, -1]
    # #
    # g[0,0, 1:-1] = g[2,0, 1:-1]
    # g[0, 0, 1:-1] = g[2, 0, 1:-1]
    # g[0, 0, 1:-1] = g[2, 0, 1:-1]
    # g[0, 0, 1:-1] = g[2, 0, 1:-1]
    return g


def curvature_central(phi):
    """
    Compute divergence in equation(9) by definition of divergence rather the discretization of divergence mentioned in paper.
    """
    phi_x, phi_y, phi_z = np.gradient(phi)
    """if np.max(phi_x) > 1e10 or np.max(phi_y) > 1e10:
	    raise Exception("oooooops!")
    """
    norm_gradient = np.sqrt(phi_x ** 2 + phi_y ** 2 + phi_z**2 + 1e-10)
    nxx, _, _ = np.gradient(phi_x / norm_gradient)
    _, nyy, _ = np.gradient(phi_y / norm_gradient)
    _, _, nzz = np.gradient(phi_z / norm_gradient)
    return (nxx + nyy + nzz)


def gradient(f):
    """
    Compute gradient of f.
    Input:
	    f: array_like.
    Output:
	    fx:  fx[i, j] = (f[i, j+1] - f[i, j-1]) / 2, special in boundary
	    fy:  fy[i, j] = (f[i+1, j] - f[i-1, j]) / 2
    """
    fx = f
    fy = f
    fz=f
    x,y,z = f.shape
    fx[:, 0] = f[:, 1] - f[:, 0]
    fx[:, -1] = f[:, -1] - f[:, -2]
    fy[0, :] = f[1, :] - f[0, :]
    fy[-1, :] = f[-1, :] - f[-2, :]
    for j in range(1, y - 1):
        fx[:, j] = (f[:, j + 1] - f[:, j - 1]) / 2.0
    for i in range(1, x - 1):
        fy[i, :] = (f[i + 1, :] - f[i - 1, :]) / 2.0
    return fx, fy


# Displays the image with curve superimposed
def show_curve_and_phi(fig, Img, phi, color):
    fig.axes[0].cla()
    fig.axes[0].imshow(Img, cmap='gray')
    fig.axes[0].contour(phi, 0, colors=color)
    fig.axes[0].set_axis_off()
    # plt.draw()

    fig.axes[1].cla()
    fig.axes[1].imshow(phi)
    fig.axes[1].set_axis_off()
    # plt.draw()

    plt.pause(0.001)


def initialize(x,y,z, x_center, y_center, z_center,radius):
    start = datetime.datetime.now()
    print("initialize start: {}".format(start))
    phi = np.zeros((x,y,z),dtype=np.float32)
    for i in range(x):
        for j in range(y):
            for k in range(z):
                phi[i, j,k] = -np.sqrt((i - x_center) ** 2 + (j - y_center) ** 2 + (k - z_center) ** 2) + radius
    # phi[3:23,3:23,3:23]=1
    end = datetime.datetime.now()
    print("initialize end: {}".format(end))
    print("initialize (start-end): {}".format(end-start))
    return phi


if __name__ == "__main__":
    path = r'D:\carck_detect_system\engine'
    startNum=0
    endNum=999
    img, img_width, img_height, startNum, endNum = read_images(path, startNum, endNum)
    # initialize phi
    x,y,z = img.shape
    r=20
    phi0 = initialize(x,y,z, x_center=r, y_center=r, z_center=r, radius=r-2)

    acwe(img, phi0, max_iter=100, time_step=0.1, mu=0.1, v=0.1, lambda1=1, lambda2=1, epison=1)



















