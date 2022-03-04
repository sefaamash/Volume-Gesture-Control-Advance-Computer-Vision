import time
import numpy as np
import HandTrackingModule as htm
import math
import cv2
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #using pycaw for audio video volume control
from ctypes import cast, POINTER

widthcam, heicam=640,480
address="https://192.168.1.100:8080/video"
cap=cv2.VideoCapture(address)
cap.set(3,widthcam)
cap.set(4,heicam)
pTime = 0 #previous time
detector=htm.handDetector()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    #reading teh captured video frame by frame
    frame,img=cap.read()
    #finding hands
    img=detector.findHands(img)
    #now geting position
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
            print(lmlist[4],lmlist[8])# we r getting only thumb tip(4) and index finger tip(8)
            x1,y1=lmlist[4][1],lmlist[4][2]
            x2,y2=lmlist[8][1],lmlist[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)#CIRCLE OF CENTRE OF LINE BETWEEN POINTS
            #lENGTH OF LINE BETWEEN THUMB AND FINGER TIP
            length = math.hypot(x2 - x1, y2 - y1)
            if length <50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            #our hand range is frm 50-300 now we convert that to our vol range
            #volume range -65-0 -65 is low and 0 is high when we squeeze our finger it will be -65 and fully exand then 0
            vol=np.interp(length,[50,300],[minVol,maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            print(int(length),vol)
            volume.SetMasterVolumeLevel(vol, None)
            #MAKING VOLUME BAR
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    
    
    cTime=time.time() #This will give us current time
    fps=1/(cTime-pTime) #to know framerate per second we subtract current - previous and divede by 1
    pTime=cTime  
    cv2.putText(img,str(int(fps)),(50,70),cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 0, 0), 3) 
    #to show the image 
    cv2.imshow("Image",img)
    cv2.waitKey(1)#It delays until keys are pressed






