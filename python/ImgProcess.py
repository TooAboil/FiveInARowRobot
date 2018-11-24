import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImgStatus:
    """
    存储当前图像的状态。其属性包括：
    上一时刻处理完成的图像的RGB数组；
    **当前时刻原始图像RGB数组（输入）；
    当前时刻原始图像二值数组；
    **当前图像角点坐标；
    当前图像透视变换后图像；
    图像相减结果；
    是否识别出“X”；
    “X”外接圆圆心；
    其方法包括：
    最大轮廓查找；
    透视校正，坐标映射；
    图像相减，判断是否有“X”；
    计算“X”外接圆圆心，并将当前图像存储到上一时刻图像属性项中；
    """

    def __init__(self, now_rgb):
        # 当前时刻原始图像二值数组
        self.now = now_rgb
        self.old = []  # 上一时刻处理完成的图像的二值数组
        self.trans = []  # 当前图像透视变换后图像；
        self.flag = 0  # 是否识别出“X”
        self.centre = [0, 0]  # “X”中心所在坐标
        self.m = []  # 透视变换矩阵
        self.shadow = 0  # 判断是否有遮挡，0为无遮挡，1为有遮挡，2为有“X”
        self.opening = []

    def trans_matrix(self):
        canny = binary_canny(self.now)
        self.m = perspective_matrix(canny)

    def transform(self):
        self.trans = cv2.warpPerspective(self.now, self.m, (500, 500))

    # 遮挡识别
    def shadow_recog(self):
        self.opening = sub_open(self)
        # 计算像素平均值
        average = np.mean(self.opening)
        if average > (225/10):
            self.shadow = 1
        elif abs(average) > 0.5:
            self.shadow = 2

    # X字母识别
    def cord_recog(self):
        if self.shadow == 2:
            # plt.imshow(self.opening), plt.title('opening')
            # plt.show()
            # 计算像素点中心
            coordination = []
            for i in range(np.size(self.opening, 0)):
                for j in range(np.size(self.opening, 1)):
                    if self.opening[i][j] != 0:
                        coordination.append([i, j])
            core = np.mean(coordination, 0)
            self.centre = [int(core[0] / 50), int(core[1] / 50)]
        else:
            print("error in shadow recognizing and coordination recognizing")


# 将图像转化为灰度图
def gray_process(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# 将图像进行canny边缘识别
def binary_canny(img):
    n = np.array(img)
    if n.ndim > 2:
        gray = gray_process(img)  # 把输入图像灰度化
    else:
        gray = img
    img_new = cv2.Canny(gray, 70, 110)  # 二值化
    return img_new


# 将图像二值化
def binary_gray(img):
    n = np.array(img)
    if n.ndim > 2:
        gray = gray_process(img)  # 把输入图像灰度化
    else:
        gray = img
    h, w = gray.shape[:2]
    m = np.reshape(gray, [1, w*h])
    mean = m.sum()/(w*h)
    ret, binary = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    return binary


# 将图像反相
def reverse(img):
    n = np.array(img)
    if n.ndim > 2:
        gray = gray_process(img)  # 把输入图像灰度化
    else:
        gray = img
    size = (np.size(gray, 0), np.size(gray, 1))
    iimg = np.zeros(size, dtype=np.int8)
    for i in range(np.size(gray, 0)):
        for j in range(np.size(gray, 1)):
            iimg[i][j] = 255 - gray[i][j]
    return iimg


#  生成透视变换矩阵
def perspective_matrix(img):
    # 直线识别
    lines = cv2.HoughLines(img, 1, np.pi / 180, 130)

    # 对直线的斜率进行分类
    feature = [[], []]
    theta25 = np.zeros((2, 2))
    for line in lines:
        rho, theta = line[0]
        if theta > np.pi / 2:
            feature[0].append(theta)
        else:
            feature[1].append(theta)
    a = np.array(feature[0])
    theta25[0][0] = np.mean(a) - np.pi / 9
    theta25[0][1] = np.mean(a) + np.pi / 9
    a = np.array(feature[1])
    theta25[1][0] = np.mean(a) - np.pi / 9
    theta25[1][1] = np.mean(a) + np.pi / 9

    # 查找边缘线
    edge = np.zeros((4, 2))
    for line in lines:
        rho, theta = line[0]
        thetapy = np.float64(theta)
        if (thetapy > theta25[0][0]) & (thetapy < theta25[0][1]):
            if edge[0][0] == 0 or edge[0][0] > rho:
                edge[0] = [rho, theta]
            if edge[2][0] == 0 or edge[2][0] < rho:
                edge[2] = [rho, theta]
        elif (thetapy > theta25[1][0]) & (thetapy < theta25[1][1]):
            if edge[1][0] == 0 or edge[1][0] > rho:
                edge[1] = [rho, theta]
            if edge[3][0] == 0 or edge[3][0] < rho:
                edge[3] = [rho, theta]

    # 求两两直线交点
    vertex = np.zeros((4, 2))
    for i in range(3):
        temp = edge[i][0] / np.sin(edge[i][1]) - edge[i + 1][0] / np.sin(edge[i + 1][1])
        vertex[i][0] = temp / (1 / np.tan(edge[i][1]) - 1 / np.tan(edge[i + 1][1]))
        vertex[i][1] = edge[i][0] / np.sin(edge[i][1]) - vertex[i][0] / np.tan(edge[i][1])
    i = 3
    temp = edge[i][0] / np.sin(edge[i][1]) - edge[0][0] / np.sin(edge[0][1])
    vertex[i][0] = temp / (1 / np.tan(edge[i][1]) - 1 / np.tan(edge[0][1]))
    vertex[i][1] = edge[i][0] / np.sin(edge[i][1]) - vertex[i][0] / np.tan(edge[i][1])

    # 对原始图像应用四点透视变换，以获得纸张的俯视图
    pts1 = np.float32(vertex)
    pts2 = np.float32([[500, 0], [0, 0], [0, 500], [500, 500]])
    # 生成透视变换矩阵
    m = cv2.getPerspectiveTransform(pts1, pts2)
    return m


# 透视矫正
def perspective_transformation(img,m):
    # 进行透视变换
    return cv2.warpPerspective(img, m, (500, 500))


# 将图像求逆、相减，然后开运算
def sub_open(status):
    # 将图像求逆后相减
    trans = reverse(status.trans)
    old = reverse(status.old)
    sub = cv2.subtract(old, trans)
    # 将相减后的图像二值化
    sub2 = sub
    sub_bin = np.zeros((np.size(sub2, 0), np.size(sub2, 1)), dtype=np.uint8)
    for i in range(np.size(sub2, 0)):
        for j in range(np.size(sub2, 1)):
            if sub2[i][j] > 50:
                sub_bin[i][j] = 255
            else:
                sub_bin[i][j] = 0
    # 开运算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义结构元素
    opening = cv2.morphologyEx(sub_bin, cv2.MORPH_OPEN, kernel)
    opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
    opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
    # plt.subplot(221), plt.imshow(sub), plt.title('sub')
    # plt.subplot(222), plt.imshow(old), plt.title('old')
    # plt.subplot(223), plt.imshow(trans), plt.title('trans')
    # plt.subplot(224), plt.imshow(opening), plt.title('opening')
    # plt.show()
    return opening
