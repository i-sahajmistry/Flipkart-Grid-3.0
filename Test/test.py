import cv2
import numpy as np
import imutils
import json

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1420)
cap.set(4, 800)
px = 725
py = 290
fx = 1156 

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 60, 0])
    upper_blue = np.array([121, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 100:
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)

            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print(cx, " ", cy)
            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "blue", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)
            if cy > py:
                dictionary = {'func': 'F'}
            else:
                dictionary = {'func': 'P'}

            json_object = json.dumps(dictionary, indent=4)
            print(json_object)
            with open("data.json", "w") as file:
                file.write(json_object)


    cv2.imshow("result", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()