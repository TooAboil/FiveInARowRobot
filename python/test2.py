import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


path = os.getcwd() + '\\testing-corp\\'
img = cv2.imdecode(np.fromfile(path + '06.BMP', dtype=np.uint8), cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 50, 110)
# cv2.imshow("直线", canny)
# cv2.waitKey(0)
# ret, binary = cv2.threshold(canny, 45, 255, cv2.THRESH_BINARY)

# 直线识别
lines = cv2.HoughLines(canny, 1, np.pi/180, 110)
# 找出边界直线
edge = np.zeros((4, 2))
for line in lines:
    rho, theta = line[0]
    if theta > np.pi/2:
        if edge[0][0] == 0 or edge[0][0] > rho:
            edge[0] = [rho, theta]
        if edge[2][0] == 0 or edge[2][0] < rho:
            edge[2] = [rho, theta]
    else:
        if edge[1][0] == 0 or edge[1][0] > rho:
            edge[1] = [rho, theta]
        if edge[3][0] == 0 or edge[3][0] < rho:
            edge[3] = [rho, theta]
print(edge)

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
print(vertex)

# # 绘图，用于调试参数
# for i in range(4):
#     rho, theta = edge[i]
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a * rho
#     y0 = b * rho
#     x1 = int(x0 + 1000 * (-b))
#     y1 = int(y0 + 1000 * a)
#     x2 = int(x0 - 1000 * (-b))
#     y2 = int(y0 - 1000 * a)
#     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
# cv2.imshow("直线", img)
# cv2.waitKey(0)

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

# image, contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours = sorted(contours, key=cv2.contourArea, reverse=True)
# #
# # # for c in contours:
# # #     # 近似轮廓
# # #     peri = cv2.arcLength(c, True)
# # #     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
# # #     # 如果我们的近似轮廓有四个点，则确定找到了纸
# # #     if len(approx) == 4:
# # #         docCnt = approx
# # #         break
# #
# cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
# cv2.imshow("img", img)
# cv2.waitKey(0)


#
# path = os.getcwd() + '\\testing-corp\\'
# img = cv2.imdecode(np.fromfile(path + 'test.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
# ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
# # cv2.namedWindow("Image")
# # cv2.imshow("Image", binary)
#
# image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# # # 提取轮廓
# # cnts = hierarchy[1]
# # print(contours)
# # # 打印返回值，这是一个元组
# # print(type(h))
# # # 打印轮廓类型，这是个列表
# # print(type(h[1]))
# # # 查看轮廓数量
# # print(len(contours))
#
# # 画出轮廓：temp是白色幕布，contours是轮廓，-1表示全画，然后是颜色，厚度
# cv2.drawContours(binary, contours, -1, (0, 0, 255), 3)
# cv2.imshow("img", binary)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()