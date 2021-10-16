import cv2
import mediapipe as mp
import numpy as np 
import os
import project as p
import copy
flp = "PRO"
myl = os.listdir(flp)
overlaylist = []
for impath in myl : 
    myimg = cv2.imread(f'{flp}/{impath}')
    overlaylist.append(myimg)
header = overlaylist[0]
DC = (0,0,255)
TH = 25
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detect = p.handdetect(detectionCon=0.85)
Ap,Bp = 0,0
Imgc = np.zeros((720,1280,3),np.uint8)
while True:
    success, frame = cap.read()
    new_frame = copy.copy(frame)
    frame = detect.findhand(frame)
    lml = detect.findpos(frame,draw=False)
    if len(lml)!=0:
        Ap,Bp = 0,0
        A1,B1 = lml[8][1:]
        A2,B2 = lml[12][1:]
        fingers = detect.fingerup()
        if fingers[1] and fingers[2]:
            if B1<115:
                if 1000<A1<1100:
                    frame = copy.copy(new_frame)
                    break
                elif 900<A1<1000:
                    DC = (0,0,255)
                elif 800<A1<900:
                    DC = (0,255,0)
                elif 700<A1<800:
                    DC = (0,255,255)
                elif 600<A1<700:
                    DC = (0,0,0)
                elif 500<A1<600:
                    TH = 10
                elif 400<A1<500:
                    TH = 15
                elif 300<A1<400:
                    TH = 20
                elif 200<A1<300:
                    TH = 25
            cv2.rectangle(frame,(A1,B1-TH),(A2,B2+TH),DC,cv2.FILLED)
        if fingers[1] and fingers[2] == False:
          cv2.circle(frame,(A1,B1),TH,DC,cv2.FILLED)
          if Ap==0 and Bp==0:
              Ap,Bp=A1,B1
          cv2.line(frame,(Ap,Bp),(A1,B1),DC,TH)
          cv2.line(Imgc,(Ap,Bp),(A1,B1),DC,TH)
          Ap,Bp=A1,B1
    Imgg = cv2.cvtColor(Imgc,cv2.COLOR_BGR2GRAY)
    _,Imgi = cv2.threshold(Imgg,50,255,cv2.THRESH_BINARY_INV)
    Imgi = cv2.cvtColor(Imgi,cv2.COLOR_GRAY2BGR)      
    frame = cv2.bitwise_and(frame,Imgi)
    frame = cv2.bitwise_or(frame,Imgc)
    frame[0:117,0:1280] = header
    frame = cv2.flip(frame, 1)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()