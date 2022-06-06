'''
@Author  : 1180300204-陶冶
@File    : 06.robot.py
@Software: IntelliJ IDEA
'''

import cv2
from PoseModule import PoseDetector
import serial
import time

cap = cv2.VideoCapture(0)

detector = PoseDetector()

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)
    # print(lmList[12][1:3])
    # angle = detector.findAngle(img, 16, 14, 12)
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, 16, 14, 12)
        # Right Arm
        # angle = detector.findAngle(img, 15, 13, 11)

        # print(angle)
        # arduino.write(int(angle))

        angle = str(int(angle))
        # ca = str(int(angle/10)*10)
        # ca = str(round(2*int(angle)/10)*5)
        print(angle)
        arduino.write(bytes(angle, 'utf-8'))
        # time.sleep(0.1)


    # img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)