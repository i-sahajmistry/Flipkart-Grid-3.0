import cv2
import numpy as np
import imutils

import math
from math import atan2, degrees


# def angle(arr, arr2):

#     a = np.array([arr[0], arr[1], 0])
#     b = np.array([arr2[0], arr2[1], 0])
#     c = np.array([cx, cy, 0])

#     ba = a - b
#     bc = c - b

#     cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
#     angle = np.arccos(cosine_angle)
#     return np.degrees(angle)


def angle(a, b, c):
    ang = degrees(atan2(c[1] - b[1], c[0] - b[0]) - atan2(a[1] - b[1], a[0] - b[0]))
    return ang


def displacement(x, y, a, b):
    disp = abs(((x - a) ** 2 + (y - b) ** 2) ** (1 / 2))
    return disp


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1420)
cap.set(4, 800)

index = 1

arr = [
    [532, 614],
    [550, 415],
    [590, 270],
    [590, 140],
    [490, 108],
    [360, 105],
    [170, 130],
]

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([350, 55, 100])

    lower_green = np.array([40, 70, 80])
    upper_green = np.array([70, 255, 255])

    lower_red = np.array([0, 56, 100])
    upper_red = np.array([0, 100, 100])

    lower_blue = np.array([90, 60, 0])
    upper_blue = np.array([121, 255, 255])

    mask1 = cv2.inRange(hsv, lower_black, upper_black)
    mask2 = cv2.inRange(hsv, lower_green, upper_green)
    mask3 = cv2.inRange(hsv, lower_red, upper_red)
    mask4 = cv2.inRange(hsv, lower_blue, upper_blue)

    # cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnts1 = imutils.grab_contours(cnts1)

    # cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnts2 = imutils.grab_contours(cnts2)

    # cnts3 = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnts3 = imutils.grab_contours(cnts3)

    cnts4 = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts4 = imutils.grab_contours(cnts4)

    # for c in cnts1:
    #     area1=cv2.contourArea(c)
    #     if area1 > 5000:
    #         cv2.drawContours(frame,[c],-1,(0,255,0),3)

    #         M=cv2.moments(c)
    #         cx=int(M["m10"]/M["m00"])
    #         cy=int(M["m01"]/M["m00"])
    #         print(cx," ", cy)
    #         cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
    #         cv2.putText(frame,"yellow",(cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)
    # for c in cnts2:
    #     area2=cv2.contourArea(c)
    #     if area2 > 5000:
    #         cv2.drawContours(frame,[c],-1,(0,255,0),3)

    #         M=cv2.moments(c)
    #         cx=int(M["m10"]/M["m00"])
    #         cy=int(M["m01"]/M["m00"])
    #         print(cx," ", cy)
    #         cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
    #         cv2.putText(frame,"green",(cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)

    # for c in cnts3:
    #     area3=cv2.contourArea(c)
    #     if area3> 5000:
    #         cv2.drawContours(frame,[c],-1,(0,255,0),3)

    #         M=cv2.moments(c)
    #         cx=int(M["m10"]/M["m00"])
    #         cy=int(M["m01"]/M["m00"])
    #         print(cx," ", cy)
    #         cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
    #         cv2.putText(frame,"red",(cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),3)

    for c in cnts4:
        area4 = cv2.contourArea(c)
        if area4 > 50:
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)

            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # print(cx," ", cy)
            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(
                frame,
                "blue",
                (cx - 20, cy - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                2.5,
                (255, 255, 255),
                3,
            )

            ang = angle([550, 415], [532, 614], (cx, cy))
            print(ang)

            disp = displacement(cx, cy, arr[index][0], arr[index][1])
            # print(disp)

            if disp <= 25:
                print("🙌🙌🙌🔥 achieved", arr[index])
                index = (index + 1) % 6
    for i in arr:
        frame = cv2.circle(frame, (i[0], i[1]), 7, (0, 255, 0), -1)

    cv2.imshow("result", frame)

    k = cv2.waitKey(5)
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
