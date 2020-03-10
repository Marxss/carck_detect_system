import os
import cv2
import numpy as np

def getImagePathListFromRoot(root,shuffle=False):
    pathList=[]
    for dirPath, dirNames, fileNames in os.walk(root):
        for file in fileNames:
            if file.split('.')[-1].lower() in {'bmp', 'png', 'jpg', 'jpeg' }:
                imagePath = os.path.join(dirPath, file)
                pathList.append(imagePath)
            if shuffle:
                np.random.shuffle(pathList)
    return pathList

def makeVideo():
    path = '.'
    #filelist = os.listdir(path)
    filelist = getImagePathListFromRoot( path, True )
    filelist=sorted(filelist)
    print(filelist)

    fps = 3 #视频每秒1帧
    size = (640*2, 512*2) #需要转为视频的图片的尺寸,  可以使用cv2.resize()进行修改

    video = cv2.VideoWriter("precombust.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)   #视频保存在当前目录下, 格式为 motion-jpeg codec，图片颜色失真比较小

    for item in filelist:
        print(item)
        if item.endswith('.png'):
            img = cv2.imread(item)
            video.write(img)

    video.release()
    cv2.destroyAllWindows()
    print('Video has been made.')

makeVideo()
