import cv2
import numpy as np
import HandTrackModule as htm
import time
import autopy
import mouse
import keyboard

wCam, hCam = 640, 480
frameR = 100
frameH = 100
smoothening = 7

time_list = [0, 0, 0, 0, 0, 0, 0]
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
agg_hScr_hCam = hScr / hCam
agg_x, agg_y, agg_finger = 0, 0, 0
cyay = 0
finger_move = 1
agg_length = 0
bbox = []

def finger_point_print(img, N, xlist, ylist):
    for i in N:
        cv2.circle(img, (xlist[i], ylist[i]), 15, (255, 0, 255), cv2.FILLED)

def while_module():
    cv2.namedWindow("Image")
    global agg_finger, click_z, click_z2, mouse_click_check, plocX, plocY, agg_x, agg_y, clocY, finger_move, bbox, frameR, frameH
    success, img = cap.read()
    if success:
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            xlist, ylist = [lmList[8][1], lmList[12][1], lmList[16][1], lmList[20][1], lmList[4][1]], [lmList[8][2], lmList[12][2], lmList[16][2], lmList[20][2], lmList[4][2]]
            z1 = lmList[8][3]
            z2 = lmList[12][3]

            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameH), (wCam - frameR, hCam - detector.h_cut),
                          (255, 0, 255), 2)
            cv2.line(img, (1, hCam - detector.h_cut), (wCam - 1, hCam - detector.h_cut), (255, 0, 0), 3)
            x3 = np.interp(xlist[0], (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(ylist[0], (frameH, hCam - detector.h_cut), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            if fingers == 21:
                if agg_finger == 1:
                    mouse.click("left")
                elif time_list[6] == 1 and (agg_x != (wScr-clocX) or agg_y - clocY != 5):
                    autopy.mouse.move(wScr - clocX, clocY)
                agg_x, agg_y = (wScr - clocX), clocY
                plocX, plocY = clocX, clocY
                finger_point_print(img, [0,4], xlist, ylist)
                agg_finger = fingers

            elif fingers == 22:
                if agg_finger == 21:
                    if time_list[6] == 0:
                        mouse.press("left")
                        time_list[6] = 1
                finger_point_print(img, [0, 4], xlist, ylist)
                agg_finger = fingers

            elif fingers == 31:
                if detector.length < 50:
                    if agg_finger == 2:
                        mouse.click("right")
                finger_point_print(img, [0, 1, 4], xlist, ylist)
                agg_finger = fingers

            elif fingers == 51:
                if agg_finger == 4 and detector.alllength > 130:
                    keyboard.press_and_release('ctrl + shift + z')
                    keyboard.press_and_release('ctrl + y')
                    keyboard.press_and_release('alt + right')
                    mouse_click_check = 1
                finger_point_print(img, list(range(len(xlist))), xlist, ylist)
                agg_finger = fingers

            elif fingers == 1:
                if agg_finger == 21:
                    if time_list[6] == 1:
                        mouse.release("left")
                        time_list[6] = 0
                if agg_x != (wScr-clocX) and agg_y != clocY:
                    autopy.mouse.move(wScr - clocX, clocY)
                agg_x, agg_y = (wScr - clocX), clocY
                cv2.circle(img, (xlist[0], ylist[0]), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
                agg_finger = fingers

            elif fingers == 23:
                if agg_x != (wScr-clocX) and agg_y != clocY:
                    mouse.drag(agg_x, agg_y, (wScr - clocX), clocY)
                agg_x, agg_y = (wScr - clocX), clocY
                cv2.circle(img, (xlist[0], ylist[0]), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
                agg_finger = fingers


            elif fingers == 2:
                cyay = -0.19 if bbox[1] - 20 >= clocY else 0.19 if bbox[3] + 20 <= clocY else (clocY - agg_y)
                if cyay != 0 and detector.length > 50:
                    try:
                        time_list[3] = (time.gmtime(time.time()).tm_sec - time_list[2] ) * 1.5
                    except:
                        pass
                if detector.length < 50:
                    time_list[3] = 0
                if cyay == 0:
                    time_list[1] = time.gmtime(time.time()).tm_sec
                if time_list[3] > 0 and (time.gmtime(time.time()).tm_sec - time_list[1] == 1):
                    mouse.wheel((cyay * time_list[3]) / 400)
                    time_list[3] -= 1
                else:
                    time_list[1] = time.gmtime(time.time()).tm_sec
                finger_point_print(img, [0, 1], xlist, ylist)
                plocX, plocY = clocX, clocY
                agg_finger = fingers
                agg_y = clocY

            elif fingers == 3:
                if (mouse_click_check == 0) and (detector.alllength < 80):
                    keyboard.press_and_release('ctrl + z')
                    keyboard.press_and_release('alt + left')
                    mouse_click_check = 1
                else:
                    mouse_click_check = 0
                if (time_list[5] == 1) and (agg_y - clocY > 3) and (detector.alllength > 80):
                    keyboard.press('win')
                    keyboard.press_and_release('tab')
                    keyboard.release('win')
                    time_list[5] = 0
                finger_point_print(img, [0, 1, 2], xlist, ylist)
                agg_finger = fingers
                agg_y = clocY

            elif fingers == 32:
                finger_point_print(img, [0, 1, 2], xlist, ylist)
                agg_finger = fingers
                agg_y = clocY
                time_list[5] = 1

            elif fingers == 4:
                frameR = 0
                frameH = 0
                if agg_finger != 4:
                    finger_move = 0
                    time_list[4] = 1
                elif time_list[4] == 1:
                    if finger_move == 0:
                        if (clocX - agg_x > 1 and detector.alllength < 130):
                            keyboard.press('ctrl + win')
                            keyboard.press_and_release('right')
                            keyboard.release('ctrl + win')
                            time_list[4] = 0
                        elif (clocX - agg_x < -1 and detector.alllength < 130):
                            keyboard.press('ctrl + win')
                            keyboard.press_and_release('left')
                            keyboard.release('ctrl + win')
                            time_list[4] = 0
                        finger_move = 1
                elif detector.alllength > 130:
                    time_list[4] = 1
                finger_point_print(img, list(range(len(xlist)-1)), xlist, ylist)
                plocX, plocY = clocX, clocY
                agg_finger = fingers
                agg_x = clocX
            if fingers != 4:
                frameR = 100
                frameH = 100
            if (agg_finger == 21 or agg_finger == 22) and fingers != agg_finger:
                mouse.release("left")
            if (agg_finger == 21) and fingers != agg_finger:
                time_list[6] = 0
            click_z, click_z2 = z1, z2
        img = cv2.flip(img, 1)
        cTime = time.time()
        fps = 1 / (cTime - time_list[0]) if (cTime - time_list[0]) != 0 else 1
        time_list[0] = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        return img

def h_cut_setting():
    if len(bbox) >= 4 :
        detector.h_cut = abs(bbox[3] - bbox[1]) if abs(detector.h_cut - abs(bbox[3] - bbox[1])) != detector.h_cut else detector.h_cut

def opencv_all_delete():
    print("delete")
    if cv2.waitKey(1) :
        cv2.destroyAllWindows()
