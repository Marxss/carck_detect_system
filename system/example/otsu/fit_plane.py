import numpy as np

def fit_plane(xs,ys,zs):

    # do fit
    tmp_A = []
    tmp_b = []
    for i in range(len(xs)):
        tmp_A.append([xs[i], ys[i], 1])
        tmp_b.append(zs[i])
    b = np.matrix(tmp_b).T
    A = np.matrix(tmp_A)
    fit = (A.T * A).I * A.T * b
    errors = b - A * fit
    residual = np.linalg.norm(errors)

    print("solution:")
    print("%f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
    print("errors:")
    print(errors)
    print("residual:")
    print(residual)

    return fit