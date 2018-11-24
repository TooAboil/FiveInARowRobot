import cv2
import os


cameraCapture = cv2.VideoCapture(1)
cameraCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cameraCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
ret, img = cameraCapture.read()
img = img[280:1000, 280:1000]
cv2.imencode('.jpg',img)[1].tofile(os.getcwd() + "\\testing-camera\\02.jpg")