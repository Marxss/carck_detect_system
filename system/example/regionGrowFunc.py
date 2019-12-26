import numpy as np
from otsu import otsu_threshold

def get_nbhd(pt, checked, shape):
    # Handle borders.
    imin = max(pt[0] - 1, 0)
    imax = min(pt[0] + 1, shape[0] - 1)
    jmin = max(pt[1] - 1, 0)
    jmax = min(pt[1] + 1, shape[1] - 1)
    kmin = max(pt[2] - 1, 0)
    kmax = min(pt[2] + 1, shape[2] - 1)
    nbhd=[]
    for i in range(imin,imax+1):
        for j in range(jmin,jmax+1):
            for k in range(kmin,kmax+1):
                if not checked[(i,j,k)]:
                    nbhd.append((i,j,k))
                    checked[(i,j,k)]=True
    return nbhd

def grow(img, seed, t):
    """
    img: ndarray, ndim=3
        An image volume.

    seed: tuple, len=3
        Region growing starts from this point.
    t: int
        The image neighborhood radius for the inclusion criteria.
    """
    # img=otsu_threshold(img)
    seg = np.zeros(img.shape, dtype=np.uint8)
    # seg=np.copy(img)
    print(img.max(),img.min(),img.shape,img.dtype)
    seg[:,:,:]=150
    checked = np.zeros(img.shape, dtype=np.bool)
    print(checked.min(),checked.max(),checked.dtype)
    seg[seed] = 50
    checked[seed] = True
    needs_check = get_nbhd(seed, checked, img.shape)
    findNum=0
    while len(needs_check) > 0:
        pt = needs_check.pop()
        # print(pt)
        # Its possible that the point was already checked and was
        # put in the needs_check stack multiple times.

        # Handle borders.
        imin = max(pt[0] - t, 0)
        imax = min(pt[0] + t, img.shape[0])
        jmin = max(pt[1] - t, 0)
        jmax = min(pt[1] + t, img.shape[1])
        kmin = max(pt[2] - t, 0)
        kmax = min(pt[2] + t, img.shape[2])
        # if img[imin:imax, jmin:jmax, kmin:kmax].mean()<150:
        if img[pt] < 120:
            # Include the voxel in the segmentation and
            # add its neighbors to be checked.
            seg[pt] = 0
            findNum+=1
            needs_check+=get_nbhd(pt, checked, img.shape)
        if len(needs_check)%10000==0:
            print(len(needs_check),"--",findNum)

    # seg[0:35, 0:35, 0:35] = 50+30
    # seg[25:55, 25:55, 25:55] = 100+30
    # seg[45:74, 45:74, 45:74] = 150+30
    print(checked.min(), checked.max(), checked.dtype)
    print(seg.max(), seg.min(), img.shape,seg.dtype)
    return seg.astype(np.uint8)

