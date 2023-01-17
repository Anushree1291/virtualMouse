'''Importing Modules'''
import cv2
import mediapipe as mp
import time
import math
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector

'''Declaring Variables'''
wscr, hscr = pyautogui.size()
wcam, hcam = 640, 480
length=0
pTime=0
cTime=0
smoothing=2
plocx,plocy = 0, 0
clocx,clocy = 0, 0
lmList = []
finger = []
tipIds=[4, 8, 12, 16, 20]


cap = cv2.VideoCapture(0)

mpHands =mp.solutions.hands
hands=mpHands.Hands()
mpDraw =mp.solutions.drawing_utils


while True:
    sucess ,img =cap.read()
    img=cv2.flip(img,1)
    imgRGB=cv2.cvtColor(img ,cv2.COLOR_BGR2RGB)
    results=hands.process(img)
    if results.multi_hand_landmarks:
        myHand=results.multi_hand_landmarks[-1]
        for handLms in results.multi_hand_landmarks:
            for id ,lm in enumerate(myHand.landmark):
                h, w , c =img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
            if len(lmList)!=0:
                x1,y1=lmList[8][1:]
                x2,y2=lmList[12][1:]
            if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                finger.append(0)
            else:
                finger.append(1)
            for ids in range(1,5,):
                if lmList[tipIds[ids]][2]<lmList[tipIds[ids]-2][2]:
                    finger.append(1)
                else:
                    finger.append(0)
            print(finger)
            cv2.rectangle(img,(100,100), (wcam-100 , hcam-100),(255,0,255),3)
            if finger[1]==1 and finger[2]==0:
                x3=np.interp(x1,(100,wcam-100),(0,wscr))
                y3=np.interp(y1,(100,hcam-100),(0,hscr))
                clocx=plocx+(x3-plocx) / smoothing
                clocy=plocy+(y3-plocy) / smoothing
                pyautogui.moveTo(clocx,clocy)
                cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
                plocx,plocy=clocx,clocy
            if finger[0]==0 and (finger[1]==1 and finger[2]==1 and finger[3]==1 and finger[4]==1) :
                pyautogui.scroll(10)
            if (finger[0]==0 and finger[4]==0) and (finger[1]==1 and finger[2]==1 and finger[3]==1) :
                pyautogui.scroll(-10)
            if finger[1]==1 and finger[2]==1:
                a1,b1=lmList[8][1:]
                a2,b2=lmList[12][1:]
                length=math.hypot(a2-a1,b2-b1)
                if length < 30:
                    pyautogui.click()
                    cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            if ((finger[1]==1 and finger[4]==1) and (finger[0]==0 and finger[2]==0 and finger[3]==0)):
                pyautogui.click(button='Right')
            finger=[]
            lmList=[]
            mpDraw.draw_landmarks(img , handLms,mpHands.HAND_CONNECTIONS)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image" , img)
    cv2.waitKey(1)