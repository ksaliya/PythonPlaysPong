import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui


def roi(img, vertices):
    mask = np.zeros_like(img)+255
    cv2.fillPoly(mask, [vertices], 0)
    masked = cv2.bitwise_and(img, mask)
    masked = cv2.bitwise_not(masked)
    return masked


def find_puck_coords(img):
    vertices = np.array([[230, 20], [370, 20], [370, 60], [230, 60]])
    img = roi(img, vertices)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    puck = detector.detect(img)

    try:
        puck_x = puck[0].pt[0]
        puck_y = puck[0].pt[1]
    except:
        puck_x = 0
        puck_y = 0

    return puck_x, puck_y


def find_paddle(img):
    vertices = np.array([[0, 0], [580, 0], [580, 500], [0, 500]])
    masked = roi(img, vertices)
    masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(masked, 127, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if len(c) == 8:
            paddle = c

    try:
        paddle_center = round((paddle[7][0][1] + paddle[0][0][1]) / 2)
    except:
        paddle_center = 0

    return paddle_center


def main():

    dir = 'up'
    while True:
        screen = np.array(ImageGrab.grab(bbox=(0, 90, 600, 590)))

        x, y = find_puck_coords(screen)
        p = find_paddle(screen)

        print('paddle = {0}, y = {1}'.format(p, y))

        if p != 0 and p > y and p > 40:
            # pyautogui.press('up', presses)
            pyautogui.keyUp('down')
            pyautogui.keyDown('up')
            dir = 'up'
            print('up')
        elif p != 0 and p < y and p < 450:
            # pyautogui.press('down', presses)
            pyautogui.keyUp('up')
            pyautogui.keyDown('down')
            dir = 'down'
            print('down')
        elif p == 0 and dir == 'up':
            # pyautogui.press('down', presses)
            pyautogui.keyUp('up')
            pyautogui.keyDown('down')
            dir = 'down'
            print('down')
        elif p == 0 and dir == 'down':
            # pyautogui.press('up', presses)
            pyautogui.keyUp('down')
            pyautogui.keyDown('up')
            dir = 'up'
            print('up')


# Simple countdown
def start():
    print('starting')
    for i in list(range(3))[::-1]:
        print(i + 1)
        time.sleep(1)


start()
main()
