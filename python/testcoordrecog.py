import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import ImgProcess as ip

# img = cv2.imdecode(np.fromfile(os.getcwd() + "\\testing-camera\\02.jpg", dtype=np.uint8), cv2.IMREAD_UNCHANGED)


img2 = cv2.imdecode(np.fromfile(os.getcwd() + "\\testing-camera\\02.jpg", dtype=np.uint8), cv2.IMREAD_UNCHANGED)
canny2 = ip.binary_canny(img2)
m = ip.perspective_matrix(canny2)
bst2 = cv2.warpPerspective(img2, m, (500, 500))
iimg2 = ip.reverse(bst2)
cv2.imencode('.jpg', iimg2)[1].tofile(os.getcwd() + "\\反相.jpg")


cameraCapture = cv2.VideoCapture(1)
cameraCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cameraCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
ret, img = cameraCapture.read()
img = img[280:1000, 280:1000]

canny = ip.binary_canny(img)
bst = cv2.warpPerspective(img, m, (500, 500))
# gamma = ip.gamma_process(bst)
binary = ip.binary_gray(bst)
# binary2 = ip.binary_gray(gamma)
iimg = ip.reverse(bst)
cv2.imshow('img', img)
cv2.imshow('bst', bst)
cv2.imshow('binary', binary)
# cv2.imshow('binary2', binary2)
cv2.imshow('iimg', iimg)
# cv2.imshow('gamma',gamma)

cv2.imencode('.jpg', iimg)[1].tofile(os.getcwd() + "\\反相.jpg")

sub = cv2.subtract(iimg2, iimg)
cv2.imencode('.jpg', sub)[1].tofile(os.getcwd() + "\\像素相减.jpg")

plt.subplot(131), plt.imshow(iimg), plt.title('input')
plt.subplot(132), plt.imshow(iimg2), plt.title('output')
plt.subplot(133), plt.imshow(sub), plt.title('sub')
plt.show()
# cv2.imshow("sub", sub)
sub2 = sub
sub_bin = np.zeros((np.size(sub2, 0), np.size(sub2, 1)), dtype=np.uint8)
for i in range(np.size(sub2, 0)):
    for j in range(np.size(sub2, 1)):
        if sub2[i][j] > 50:
            sub_bin[i][j] = 255
        else:
            sub_bin[i][j] = 0
cv2.imshow("sub_bin", sub_bin)
cv2.imencode('.jpg', sub_bin)[1].tofile(os.getcwd() + "\\像素相减二值化.jpg")

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义结构元素
opening = cv2.morphologyEx(sub_bin, cv2.MORPH_OPEN, kernel)  # 开运算
cv2.imshow("opening", opening)
cv2.imencode('.jpg', opening)[1].tofile(os.getcwd() + "\\开运算.jpg")
# cv2.waitKey(0)

average = np.mean(opening)
if average > (225 / 10):
    print("遮挡")
elif abs(average) > 1:
    print("有X")

coordination = []
for i in range(np.size(opening, 0)):
    for j in range(np.size(opening, 1)):
        if opening[i][j] != 0:
            coordination.append([i, j])

core = np.mean(coordination, 0)
print(int(core[0]/50))
print(int(core[1]/50))
cv2.waitKey(0)

