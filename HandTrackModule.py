import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.inclination_data = 0

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            check = 1 if len(self.results.multi_hand_landmarks) > 2 else 0
            myHand = self.results.multi_hand_landmarks[check]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy, lm.z])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

        return self.lmList, bbox

    def distense(self, a, b):
        x1, y1 = self.lmList[a][1], self.lmList[a][2]
        x2, y2 = self.lmList[b][1], self.lmList[b][2]

        self.length = math.hypot(x2 - x1, y2 - y1)

    def inclination(self, a, b):
        x1, y1 = self.lmList[a][1], self.lmList[a][2]
        x2, y2 = self.lmList[b][1], self.lmList[b][2]
        self.inclination_data = int((y1-y2)/(x1-x2)) if x1-x2 != 0 else 0

    def fingersUp(self):
        fingers = 0
        for id in range(1, 5):
            if (self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 1][2]):
                if id == 1:
                    fingers = 1
                if id == 2:
                    fingers = 2 if fingers >= 1 else 0
                    self.distense(self.tipIds[1], self.tipIds[2])
                if id == 3:
                    fingers = 3 if fingers >= 2 else 0
                if id == 4:
                    fingers = 4 if fingers >= 3 else 0
        if fingers < 2 and (self.lmList[self.tipIds[1]][2] < self.lmList[self.tipIds[1] - 1][2]):
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers = 21
                self.distense(self. tipIds[0], self.tipIds[1])
        elif fingers == 2:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 2][1]:
                fingers = 31
        elif fingers == 4:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 2][1]:
                fingers = 51
        elif self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 2][1]:
            fingers = 5
        return fingers
