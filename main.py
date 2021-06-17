import cv2
import numpy as np
import HandTrackModule as htm
import time
import autopy
import mouse
import keyboard

wCam, hCam = 640, 480
frameR = 100
smoothening = 7

loop = 0
pTime = 0
s_time = 0
c_time = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
click_z, click_z2 = 0, 0

mouse_click_check = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
inclination = detector.inclination_data
wScr, hScr = autopy.screen.size()
agg_x, agg_y, agg_finger = 0, 0, 0
cyay = 0
finger_move = 1
agg_length = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        xlist, ylist = [lmList[8][1], lmList[12][1], lmList[16][1], lmList[20][1], lmList[4][1]], [lmList[8][2], lmList[12][2], lmList[16][2], lmList[20][2], lmList[4][2]]
        z1 = lmList[8][3]
        z2 = lmList[12][3]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        print(fingers)
        if fingers == 21:
            if agg_finger == 1:
                mouse.click("left")
                mouse_click_check = 1
            elif (click_z - z1 > 0.034 and click_z - z1 < 0.2 and mouse_click_check == 0) and (mouse_click_check == 0):
                mouse.click("left")
                mouse_click_check = 1
            elif (click_z - z1 < 0.03):
                if mouse_click_check == 1:
                    mouse_click_check = 0
            cv2.circle(img, (xlist[0], ylist[0]), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (xlist[4], ylist[4]), 15, (255, 0, 255), cv2.FILLED)
            agg_finger = fingers
            agg_length = detector.length

        elif fingers == 31:
            if detector.length < 50:
                if agg_finger == 2:
                    mouse.click("right")
                    print(click_z, z1)
                    mouse_click_check = 1
            cv2.circle(img, (xlist[0], ylist[0]), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (xlist[1], ylist[1]), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (xlist[4], ylist[4]), 15, (255, 0, 255), cv2.FILLED)
            agg_finger = fingers

        elif fingers == 51:
            if agg_finger == 4:
                keyboard.press_and_release('ctrl + shift + z')
                keyboard.press_and_release('ctrl + y')
                keyboard.press_and_release('alt + right')
                mouse_click_check = 1
            elif (click_z - z1 > 0.03 and click_z - z1 < 0.2 and mouse_click_check == 0) and (mouse_click_check == 0):
                keyboard.press_and_release('ctrl + shift + z')
                keyboard.press_and_release('ctrl + y')
                keyboard.press_and_release('alt + right')
                mouse_click_check = 1
            elif (click_z - z1 < 0.03):
                if mouse_click_check == 1:
                    mouse_click_check = 0
            for id, i in enumerate(xlist):
                cv2.circle(img, (i, ylist[id]), 15, (255, 0, 255), cv2.FILLED)
            agg_finger = fingers

        elif fingers == 1:
            x3 = np.interp(xlist[0], (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(ylist[0], (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            print(wScr-clocX, clocY, z1, click_z, mouse_click_check)
            if agg_x != (wScr-clocX) and agg_y != clocY:
                try:
                    autopy.mouse.move(wScr - clocX, clocY)
                except:
                    pass
            agg_x, agg_y = (wScr - clocX), clocY
            cv2.circle(img, (xlist[0], ylist[0]), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            agg_finger = fingers

        elif fingers == 2:
            x3 = np.interp(xlist[0], (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(ylist[0], (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            cyay = -0.19 if bbox[1] - 20 >= clocY else 0.19 if bbox[3] + 20 <= clocY else (clocY - agg_y)
            if cyay != 0 and detector.length > 50:
                try:
                    print(clocY, agg_y, cyay / 20, detector.length)
                    #mouse.wheel(clocY/100)
                    loop = (time.gmtime(time.time()).tm_sec - c_time) * 1.5
                except:
                    pass
            if detector.length < 50:
                loop = 0
            if cyay == 0:
                c_time = time.gmtime(time.time()).tm_sec
            for id, i in enumerate(xlist):
                if id < 2:
                    cv2.circle(img, (i, ylist[id]), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            agg_finger = fingers
            agg_y = clocY

        elif fingers == 3:
            if agg_finger != fingers:
                keyboard.press_and_release('ctrl + z')
                keyboard.press_and_release('alt + left')
                mouse_click_check = 1
            elif (click_z - z1 > 0.03 and click_z - z1 < 0.2 and mouse_click_check == 0) and (mouse_click_check == 0):
                keyboard.press_and_release('ctrl + z')
                keyboard.press_and_release('alt + left')
                mouse_click_check = 1
            elif (click_z - z1 < 0.03):
                if mouse_click_check == 1:
                    mouse_click_check = 0
            cv2.circle(img, (xlist[0], ylist[0]), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (xlist[1], ylist[1]), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (xlist[2], ylist[2]), 15, (255, 0, 255), cv2.FILLED)
            agg_finger = fingers

        elif fingers == 4:
            if agg_finger != 4:
                finger_move = 0
            x3 = np.interp(xlist[0], (frameR, wCam - frameR), (0, wScr))
            clocX = plocX + (x3 - plocX) / smoothening
            if agg_finger != 4:
                agg_x = clocX
            if (clocX - agg_x > 200 and finger_move == 0):
                keyboard.press_and_release('ctrl + win + left')
                print("<", clocX, agg_x)
                fingers = 1
                finger_move = 1
            elif (clocX - agg_x < -200 and finger_move == 0):
                keyboard.press_and_release('ctrl + win + right')
                print(">", clocX, agg_x)
                fingers = 1
                finger_move = 1
            for id, i in enumerate(xlist):
                if id < 4:
                    cv2.circle(img, (i, ylist[id]), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            agg_finger = fingers
        click_z, click_z2 = z1, z2
    if loop > 0 and (time.gmtime(time.time()).tm_sec-s_time == 1):
        #mouse.wheel(clocY / 100)
        print("Wheel check", cyay, loop)
        print("Wheel", cyay*loop)
        mouse.wheel((cyay*loop)/400)
        loop -= 1
    else:
        s_time = time.gmtime(time.time()).tm_sec
    img = cv2.flip(img, 1)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()