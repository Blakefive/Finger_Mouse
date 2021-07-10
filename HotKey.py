from pynput.keyboard import Listener, Key, KeyCode
from threading import Thread
import main
import cv2

store = set()
check1 = set([Key.ctrl_l, Key.alt_l])
check2 = set([Key.right, Key.pause])
loop_check = 0
agg_time = 0

def program_run():
    global agg_time, loop_check
    while loop_check == 1:
        img = main.while_module()
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == 27:
            pass
    if loop_check == 0:
        main.opencv_all_delete()

print("start")
def handleKeyPress(key):
    global loop_check
    if (key == Key.ctrl_l) or (key == Key.alt_l):
        store.add(key)
        if store == check1:
            if loop_check == 1:
                print("check", loop_check)
                loop_check = 0
                program_run()
            elif loop_check == 0:
                print("check1", loop_check)
                loop_check = 1
                t2 = Thread(target=program_run)
                t2.start()
            print('Press: {}'.format(store))
    if (key == Key.right) or (key == Key.pause):
        store.add(key)
        if store == check2:
            main.h_cut_setting()

def handleKeyRelease(key):
    if key in store:
        store.remove(key)

def hotkey_def():
    with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
        listener.join()

t1 = Thread(target=hotkey_def)
t1.start()
t1.join()
