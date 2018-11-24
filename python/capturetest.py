import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
import os


cameraCapture = cv2.VideoCapture(1)
cameraCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cameraCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
ret, img = cameraCapture.read()
img = img[280:1000, 280:1000]

# img = cv2.imdecode(np.fromfile(os.getcwd() + "\\testing-camera\\09.jpg", dtype=np.uint8), cv2.IMREAD_UNCHANGED)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 70, 110)
cv2.imshow("canny", canny)
# cv2.imencode('.jpg', canny)[1].tofile(os.getcwd() + "\\canny边缘识别.jpg")
ret, binary = cv2.threshold(canny, 45, 255, cv2.THRESH_BINARY)

# 直线识别
lines = cv2.HoughLines(canny, 1, np.pi/180, 130)

# 绘出所有识别出的直线，用于调试
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0+1000*(-b))
    y1 = int(y0+1000*(a))
    x2 = int(x0-1000*(-b))
    y2 = int(y0-1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow("直线", img)
cv2.imencode('.jpg',img)[1].tofile(os.getcwd() + "\\直线识别.jpg")

# 对直线的斜率进行分类
feature = [[], []]
theta25 = np.zeros((2, 2))
for line in lines:
    rho, theta = line[0]
    if theta > np.pi/2:
        feature[0].append(theta)
    else:
        feature[1].append(theta)
a = np.array(feature[0])
theta25[0][0] = np.mean(a) - np.pi/9
theta25[0][1] = np.mean(a) + np.pi/9
a = np.array(feature[1])
theta25[1][0] = np.mean(a) - np.pi/9
theta25[1][1] = np.mean(a) + np.pi/9
# print(theta25)
# print(type(theta25))
# print(theta25[0][0])
# print(type(theta25[0][0]))

# 查找边缘线
edge = np.zeros((4, 2))
for line in lines:
    rho, theta = line[0]
    thetapy = np.float64(theta)
    # print(thetapy > theta25[0][0])
    # print(type(thetapy > theta25[0][0]))
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
# print(edge)

# 求两两直线交点
vertex = np.zeros((4, 2))
for i in range(3):
    temp = edge[i][0]/np.sin(edge[i][1]) - edge[i+1][0]/np.sin(edge[i+1][1])
    vertex[i][0] = temp / (1 / np.tan(edge[i][1]) - 1 / np.tan(edge[i+1][1]))
    vertex[i][1] = edge[i][0] / np.sin(edge[i][1]) - vertex[i][0] / np.tan(edge[i][1])
i = 3
temp = edge[i][0]/np.sin(edge[i][1]) - edge[0][0]/np.sin(edge[0][1])
vertex[i][0] = temp / (1 / np.tan(edge[i][1]) - 1 / np.tan(edge[0][1]))
vertex[i][1] = edge[i][0] / np.sin(edge[i][1]) - vertex[i][0] / np.tan(edge[i][1])
# print(vertex)

# 绘图，用于调试参数
for i in range(4):
    rho, theta = edge[i]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
cv2.imshow("选择后直线", img)


# 对原始图像应用四点透视变换，以获得纸张的俯视图
pts1 = np.float32(vertex)
pts2 = np.float32([[500, 0], [0, 0], [0, 500], [500, 500]])
# 生成透视变换矩阵
m = cv2.getPerspectiveTransform(pts1, pts2)
# 进行透视变换
dst = cv2.warpPerspective(img, m, (500, 500))
# cv2.imshow("图像", dst)
# cv2.waitKey(0)
plt.subplot(121), plt.imshow(img), plt.title('input')
plt.subplot(122), plt.imshow(dst), plt.title('output')
plt.show()
