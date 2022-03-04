from unittest import result
import cv2
import mediapipe as mp
import time

address="https://192.168.1.101:8080/video"
cap=cv2.VideoCapture(address)

mpHands=mp.solutions.hands
hands=mpHands.Hands()#it has 4 parameter no ofhands,detection and tracking on basis of confidence if for eg detection confidence is less than 50% then it wll track and viceversa
 #it helps us to draw points which take lot of mathmetics and timeconsuming
mpDraw=mp.solutions.drawing_utils
 
pTime = 0 #previous time
cTime = 0  #currenttime
 
while True:
    #reading teh captured video frame by frame
    frame,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)#IMG OR VIDEO IS IN bgr form so we convert it to rgb or gray etc
    result=hands.process(imgRGB)
   #print(result.multi_hand_landmarks)#multi_hand_landmarks without it it will not detect hands and wehn we put it it will detect the hands
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
           #Now we get landmark numbers and id numbers its already in handlms.landmark we r just getting it
             for id, lm in enumerate(handlms.landmark):#enumerate() allows us to iterate through a sequence but it keeps track of both the index and the element. 
                print(id, lm) #each hand ieation has an id in that id there are x,y,z cordinates we will take x,y cordinates to get landmark of hands
                h, w, c = img.shape #first we check out height,width and channel of our image
                #now positions centrex,centre y, landmark.x * width and landmark.y * y to get cx,cy
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy) #to know which one is for landmark 1 or 2 so we also give id
                if id == 0:
                   cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
           #Drawing hands  (HAND_CONNECTIONS):This will draw the connections for us of hands
             mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)#we are drawing it on the actual bgr image
    cTime=time.time() #This will give us current time
    fps=1/(cTime-pTime) #to know framerate per second we subtract current - previous and divede by 1
    pTime=cTime         #then previous time becomes current time
    #to show text on our image or video
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3) 
    #to show the image 
    cv2.imshow("Image",img)
    cv2.waitKey(1)#It delays until keys are pressed
