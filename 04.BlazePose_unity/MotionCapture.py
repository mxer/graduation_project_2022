'''
@Author  : 1180300204-陶冶
@File    : 05.MotionCapture.py
@Software: IntelliJ IDEA
'''

import cv2
from PoseModule import PoseDetector
import socket

cap = cv2.VideoCapture(0)
detector = PoseDetector()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)
    
    data = []

    if bboxInfo:
        lmString = ''
        # print(lmList)
        for lm in lmList:
            lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
        data.append(lmString)
        # print(str(data))
        sock.sendto(str.encode(str(data)), serverAddressPort)

    # img = cv2.resize(img, (0, 0), None, 0.35, 0.35)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)



    # if key == ord('s'):
    #     with open("AnimationFile.txt", 'w') as f:
    #         f.writelines(["%s\n" % item for item in posList])