import cv2
import mediapipe as mp
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

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    detector = handdetect()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findhand(img)
        lmList = detector.findpos(img)
        if len(lmList) != 0:
            print(lmList[8])
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == "__main__":
    main()

cv2.destroyAllWindows()
