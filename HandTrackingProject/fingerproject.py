import cv2
import mediapipe as mp
import time
import os
import HandTrackingModule as htm
widthcam, heicam=640,480
address="https://192.168.1.101:8080/video"
cap=cv2.VideoCapture(address)
cap.set(3,widthcam)
cap.set(4,heicam)
pTime=0
detector = htm.handDetector()
tipIds = [4, 8, 12, 16, 20]
while True:
    #reading teh captured video frame by frame
    frame,img=cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] & lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] & lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
        
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
    cTime=time.time() #This will give us current time
    fps=1/(cTime-pTime) #to know framerate per second we subtract current - previous and divede by 1
    pTime=cTime  
    cv2.putText(img,str(int(fps)),(50,70),cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 0, 0), 3) 
    #to show the image 
    cv2.imshow("Image",img)
    cv2.waitKey(1)#It delays until keys are pressed

