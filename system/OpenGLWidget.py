from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from myPaper.OPENGL.readData import *
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])*20  # 视景体的left/right/bottom/top/near/far六个面
SCALE_K = np.array([1.0, 1.0, 1.0])  # 模型缩放比例
EYE = np.array([0.0, 0.0, 2.0])  # 眼睛的位置（默认z轴的正方向）
LOOK_AT = np.array([0.0, 0.0, 0.0])  # 瞄准方向的参考点（默认在坐标原点）
EYE_UP = np.array([0.0, 1.0, 0.0])  # 定义对观察者而言的上方（默认y轴的正方向）
WIN_W, WIN_H = 750, 750  # 保存窗口宽度和高度的变量
LEFT_IS_DOWNED = False  # 鼠标左键被按下
MOUSE_X, MOUSE_Y = 0, 0  # 考察鼠标位移量时保存的起始位置

class OpenGLWidget(QGLWidget):


    def getposture(self):
        global EYE, LOOK_AT

        dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
        if dist > 0:
            phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
            theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
        else:
            phi = 0.0
            theta = 0.0

        return dist, phi, theta

    def initializeGL(self):
        self.grabKeyboard()
        # self.showFullScreen()
        DIST, PHI, THETA = self.getposture()  # 眼睛与观察目标之间的距离、仰角、方位角
        glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置画布背景色。注意：这里必须是4个参数
        glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
        glDepthFunc(GL_LEQUAL)  # 设置深度测试函数（GL_LEQUAL只是选项之一）

        mat_specular= [1.0, 1.0, 1.0, 1.0]

        mat_shininess = [100.0]

        light_position = [5.0, 5.0, 5.0, 1.0] # 点光源 #
        light_position = [0.0, 0.0, 50.0, 0.0] # 无限远模拟平行光

        white_light = [1.0, 1.0, 1.0, 1.0]

        model_ambient = [0.1, 0.1, 0.1, 1.0]

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH) # 为场景中的物体定义材料属性：如何反射光线（材料环境、散射、镜面颜色、光泽度）
        # glLightModeli(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)# 这个表示模型的正面接受环境光和散射光，你可以修改这两个参数
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular) # 使用镜面材质颜色
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess) # 使用光泽度
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)#指定混合函数

        glLightfv(GL_LIGHT0, GL_POSITION, light_position) # 定义光源的位置
        glLightfv(GL_LIGHT0, GL_DIFFUSE, white_light) # 定义散射光为白色
        glLightfv(GL_LIGHT0, GL_SPECULAR, white_light) # 定义镜面光为白色
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, model_ambient) # 光照模型参数：全局环境光

        glEnable(GL_COLOR_MATERIAL)#启动颜色材料模式
        glEnable(GL_LIGHTING) # 驱动光源
        glEnable(GL_LIGHT0) # 启动特定光源
        glEnable(GL_BLEND) #开启透明模式
        glEnable(GL_DEPTH_TEST)# 启用深度检测




    def paintGL(self):
        global IS_PERSPECTIVE, VIEW
        global EYE, LOOK_AT, EYE_UP
        global SCALE_K
        global WIN_W, WIN_H

        # 清除屏幕及深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 设置投影（透视投影）
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if WIN_W > WIN_H:
            if IS_PERSPECTIVE:
                glFrustum(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
            else:
                glOrtho(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            if IS_PERSPECTIVE:
                glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
            else:
                glOrtho(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])

        # 设置模型视图
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 几何变换
        glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])

        # 设置视点
        gluLookAt(EYE[0], EYE[1], EYE[2], LOOK_AT[0], LOOK_AT[1], LOOK_AT[2], EYE_UP[0], EYE_UP[1], EYE_UP[2])

        # 设置视口
        glViewport(0, 0, WIN_W, WIN_H)

        # ---------------------------------------------------------------
        # glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）
        #
        # # 以红色绘制x轴
        # glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
        # glVertex3f(-0.8, 0.0, 0.0)  # 设置x轴顶点（x轴负方向）
        # glVertex3f(0.8, 0.0, 0.0)  # 设置x轴顶点（x轴正方向）
        #
        # # 以绿色绘制y轴
        # glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
        # glVertex3f(0.0, -0.8, 0.0)  # 设置y轴顶点（y轴负方向）
        # glVertex3f(0.0, 0.8, 0.0)  # 设置y轴顶点（y轴正方向）
        #
        # # 以蓝色绘制z轴
        # glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
        # glVertex3f(0.0, 0.0, -0.8)  # 设置z轴顶点（z轴负方向）
        # glVertex3f(0.0, 0.0, 0.8)  # 设置z轴顶点（z轴正方向）
        #
        # glEnd()  # 结束绘制线段

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        glDisable(GL_LIGHTING)
        # ---------------------------------------------------------------
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) #线框模式显示
        glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴负半区）
        glColor4f(1.0, 0.0, 0.0, 1)  # 设置当前颜色为红色不透明
        vertexs, vnorms = readData('crack.STL')
        for i in range(len(vnorms)):
            glNormal3fv(vnorms[i])
            glVertex3fv(vertexs[3 * i])
            glVertex3fv(vertexs[3 * i + 1])
            glVertex3fv(vertexs[3 * i + 2])
        glEnd()  # 结束绘制三角形
        glPopMatrix()

        # ---------------------------------------------------------------
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴负半区）
        glColor4f(0.0, 1.0, 0.0, 0.5)  # 设置当前颜色为红色不透明
        vertexs, vnorms = readData('gear.stl')
        for i in range(len(vnorms)):
            glNormal3fv(vnorms[i])
            glVertex3fv(vertexs[3 * i])
            glVertex3fv(vertexs[3 * i+1])
            glVertex3fv(vertexs[3 * i+2])
        glEnd()  # 结束绘制三角形
        glPopMatrix()
        #-------------------------------------绘制直线
        # glPushMatrix()
        # glTranslatef(0.0, 0.0, -5.0)
        # glBegin(GL_QUADS)#绘制四边形
        # glColor4f(0.0, 1.0, 0.0, 0.5)
        # glVertex3f(0, 0, 0)
        # glVertex3f(95, 0, 0)
        # glVertex3f(95, 95, 0)
        # glVertex3f(0, 95, 0)
        # glEnd()
        # glPopMatrix()
        # ---------------------------------------------------------------

        self.swapBuffers()  # 切换缓冲区，以显示绘制内容

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glDepthMask(GL_TRUE)

    def resizeGL(self,w, h):
        # global WIN_W, WIN_H
        #
        # WIN_W, WIN_H = width, height
        # glutPostRedisplay()

        #视口变换
        glViewport(0, 0,w,h)
        #投影变换
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0,w /h, 0.1, 10000.0)
        #视图变换
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # def mousePressEvent(self, *args, **kwargs):
    #     print(args.__str__())
    #     # print(kwargs)

    def mouseclick(self,button, state, x, y):
        global SCALE_K
        global LEFT_IS_DOWNED
        global MOUSE_X, MOUSE_Y

        MOUSE_X, MOUSE_Y = x, y
        if button == GLUT_LEFT_BUTTON:
            LEFT_IS_DOWNED = state == GLUT_DOWN
        elif button == 3:
            SCALE_K *= 1.05
            glutPostRedisplay()
        elif button == 4:
            SCALE_K *= 0.95
            glutPostRedisplay()

    # def mousePressEvent(self, *args, **kwargs):
    #     self.setMouseTracking(True)
    # def mouseReleaseEvent(self, *args, **kwargs):
    #     self.setMouseTracking(False)
    def mouseMoveEvent(self,event):
        print("mousemotion")
        s=event.windowPos()

        x=s.x()
        y=s.y()
        global LEFT_IS_DOWNED
        global EYE, EYE_UP
        global MOUSE_X, MOUSE_Y
        global DIST, PHI, THETA
        global WIN_W, WIN_H

        if LEFT_IS_DOWNED:
            dx = MOUSE_X - x
            dy = y - MOUSE_Y
            MOUSE_X, MOUSE_Y = x, y

            PHI += 2 * np.pi * dy / WIN_H
            PHI %= 2 * np.pi
            THETA += 2 * np.pi * dx / WIN_W
            THETA %= 2 * np.pi
            r = DIST * np.cos(PHI)

            EYE[1] = DIST * np.sin(PHI)
            EYE[0] = r * np.sin(THETA)
            EYE[2] = r * np.cos(THETA)

            if 0.5 * np.pi < PHI < 1.5 * np.pi:
                EYE_UP[1] = -1.0
            else:
                EYE_UP[1] = 1.0

            # glutPostRedisplay()
            self.updateGL()


    def keyPressEvent(self, QKeyEvent):
        global DIST, PHI, THETA
        global EYE, LOOK_AT, EYE_UP
        global IS_PERSPECTIVE, VIEW

        scale=100
        key=QKeyEvent.key()
        print(str(key),Qt.Key_Enter)
        if key in [Qt.Key_X, Qt.Key_S,Qt.Key_Y, Qt.Key_T,Qt.Key_Z, Qt.Key_A]:
            if key == Qt.Key_X:  # 瞄准参考点 x 减小
                LOOK_AT[0] -= 0.01*scale
            elif key == Qt.Key_S:  # 瞄准参考 x 增大
                LOOK_AT[0] += 0.01*scale
            elif key == Qt.Key_Y:  # 瞄准参考点 y 减小
                LOOK_AT[1] -= 0.01*scale
            elif key == Qt.Key_T:  # 瞄准参考点 y 增大
                LOOK_AT[1] += 0.01*scale
            elif key == Qt.Key_Z:  # 瞄准参考点 z 减小
                LOOK_AT[2] -= 0.01*scale
            elif key == Qt.Key_A:  # 瞄准参考点 z 增大
                LOOK_AT[2] += 0.01*scale

            DIST, PHI, THETA = self.getposture()
            # glutPostRedisplay()
            self.paintGL()
        elif key == Qt.Key_Enter-1:  # 回车键，视点前进
            EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
            DIST, PHI, THETA = self.getposture()
            # glutPostRedisplay()
            self.paintGL()
        elif key == Qt.Key_Backspace:  # 退格键，视点后退
            EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
            DIST, PHI, THETA = self.getposture()
            # glutPostRedisplay()
            self.paintGL()
        elif key == Qt.Key_Space:  # 空格键，切换投影模式
            IS_PERSPECTIVE = not IS_PERSPECTIVE
            # glutPostRedisplay()
            self.paintGL()


if __name__ == "__main__":
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(WIN_W, WIN_H)
    glutInitWindowPosition(300, 200)
    glutCreateWindow(b'gear')

    init()  # 初始化画布
    glutDisplayFunc(draw)  # 注册回调函数draw()
    glutReshapeFunc(reshape)  # 注册响应窗口改变的函数reshape()
    glutMouseFunc(mouseclick)  # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(mousemotion)  # 注册响应鼠标拖拽的函数mousemotion()
    glutKeyboardFunc(keydown)  # 注册键盘输入的函数keydown()

    glutMainLoop()  # 进入glut主循环