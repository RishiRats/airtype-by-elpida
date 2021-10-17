from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

import webbrowser
import cv2
import mediapipe as mp
import numpy as np 
import os
import copy

class handdetect():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tip=[4,8,12,16,20]
    def findhand(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    def findpos(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return self.lmList
    
    def fingerup(self):
        finger = []
        if self.lmList[self.tip[0]][1]<self.lmList[self.tip[0]-1][1]:
            finger.append(1)
        else:
            finger.append(0)
        for id in range(1,5):
            if self.lmList[self.tip[id]][2]<self.lmList[self.tip[id]-2][2]:
                finger.append(1)
            else:
                finger.append(0)                   
        return finger




global h, w, flag_clear
def main():
    flag_clear = False
    flp = "all_sources/PRO"
    myl = os.listdir(flp)
    overlaylist = []
    for impath in myl : 
        myimg = cv2.imread(f'{flp}/{impath}')
        overlaylist.append(myimg)
    header = overlaylist[0]
    DC = (0,0,255)
    TH = 25
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3,1280)
    cap.set(4,720)
    detect = handdetect(detectionCon=0.85)
    Ap,Bp = 0,0
    Imgc = np.zeros((720,1280,3),np.uint8)
    success, frame = cap.read()
    cv2.imshow("Frame", frame)
    while cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) >= 1:
        success, frame = cap.read()
        new_frame = copy.copy(frame)
        frame = detect.findhand(frame)
        (h, w) = frame.shape[:2]
        lml = detect.findpos(frame,draw=False)
        if len(lml)!=0:
            Ap,Bp = 0,0
            A1,B1 = lml[8][1:]
            A2,B2 = lml[12][1:]
            fingers = detect.fingerup()
            if fingers[1] and fingers[2]:
                if B1<115:
                    if 1000<A1<1100:
                        #frame = copy.copy(new_frame)
                        (h, w) = frame.shape[:2]
                        #cv2.circle(frame, (w//2, h//2), TH, (0, 0, 0), cv2.FILLED)
                        DC = (0,0,0)
                        #break
                        flag_clear = True
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
            #print("Drawing circles")
            if Ap==0 and Bp==0:
                Ap,Bp=A1,B1
            if flag_clear:
                cv2.line(frame,(Ap,Bp),(A1,B1),DC,10000)
                cv2.line(Imgc,(Ap,Bp),(A1,B1),DC,10000)
                flag_clear = False
            else:
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
        #k = cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
            break
        #print(cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE))
        #while cv2.getWindowProperty('Frame', 0) >= 0:
            #keyCode = cv2.waitKey(1)
        #print(keyCode)
        #if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
                #break 
    cap.release()
    cv2.destroyAllWindows()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("all_sources/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def core():
    window.destroy()
    main()


webbrowser.open("https://dev-elpida.netlify.app/")

window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    320.0,
    360.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    320.0,
    360.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    961.0,
    212.0,
    image=image_image_3
)

canvas.create_text(
    917.0,
    685.0,
    anchor="nw",
    text="Mail us:",
    fill="#00CFFF",
    font=("Comfortaa Bold", 18 * -1)
)

canvas.create_text(
    1005.0,
    685.0,
    anchor="nw",
    text=" dev.elpida@gmail.com",
    fill="#000000",
    font=("Comfortaa Bold", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: core(),
    relief="flat"
)
button_1.place(
    x=810.0,
    y=474.0,
    width=312.0,
    height=94.0
)
window.resizable(False, False)
window.title('AIRTYPE By Elpida')
window.mainloop()