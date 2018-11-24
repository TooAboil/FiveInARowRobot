import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
while 1:
    # get a frame
    ret, frame = cap.read()
    if (not ret) | (not frame.any()):
        print('False')
        continue
    else:
        frame = frame[280:1000, 280:1000]
        # show a frame
        cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

# cap = cv2.VideoCapture(1)
# while 1:
#     # get a frame
#     ret, frame = cap.read()
#     # show a frame
#     cv2.imshow("capture", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()
