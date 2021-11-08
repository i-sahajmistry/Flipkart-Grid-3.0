import cv2
import cv2.aruco as aruco
import numpy as np
import imutils
import json
from qr import detectMarker


def angle(a, b, c):
    ang = degrees(atan2(c[1] - b[1], c[0] - b[0]) - atan2(a[1] - b[1], a[0] - b[0]))
    return ang


def displacement(x, y, a, b):
    disp = abs(((x - a) ** 2 + (y - b) ** 2) ** (1 / 2))
    return disp

def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    arucoDict = aruco.Dictionary_get(key)

    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    center = None
    if draw:
        aruco.drawDetectedMarkers(img, bbox)
        if len(bbox) != 0:
            center = []
            for i in bbox:
                box = i[0]
                center.append([(int(box[0][0]) + int(box[2][0]))//2, (int(box[0][1]) + int(box[2][1]))//2])

    return [bbox, ids, center]


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)


cx, cy = 0, 0
py = 150

while True:
    _, frame = cap.read()

    arucoDetected = detectMarker(frame)
    center = arucoDetected[2]
    if center is not None:
        for i in center:
            frame = cv2.circle(frame, i, 7, (0, 255, 0), -1)
            cx, cy = i

    #h = min(100, (cy - py) // 4)
    h = int((cy - py) // 2)
    print(f'h = {h}')
    h = str(max(50, h))
    h = '0'*(3-len(h)) + h
    print(cx,cy)

    if cy <= 240 and cx > 240:
        dictionary = {'func': '1010040150'}
    elif cy > py:
        dictionary = {'func': f'1010{h}{h}'}
    elif 50<=cx<=240:
        dictionary = {'func': f'1010{h}{h}'}
    else:
        dictionary = {'func': '0000000000'}


    json_object = json.dumps(dictionary, indent=4)
    print(json_object)
    with open("data.json", "w") as file:
        file.write(json_object)


    cv2.imshow("result", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
