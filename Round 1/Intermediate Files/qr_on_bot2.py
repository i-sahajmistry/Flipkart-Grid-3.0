import cv2
import cv2.aruco as aruco
import numpy as np
import imutils
import time 
import math
from math import atan2, degrees
import json
import os

cx, cy = 0, 0
px, py = 110, 200

index=1
bot=[[1],[2],[3],[4]]


location={i: [[0, 0] for j in range(5)] for i in range(4)}

def displacement(x, y, a, b):
    disp = abs(((x - a) * 2 + (y - b) * 2) ** (1 / 2))
    return disp

def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # imgGray = cv2.flip(imgGray,1)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    arucoDict = aruco.Dictionary_get(key)

    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)

    if draw:
        aruco.drawDetectedMarkers(img, bbox)


    if ids is not None:
            
        for i in range(len(ids)):

            # print(ids[i][0], bbox[i][0])
            coordinates = [[int(j[0]), int(j[1])] for j in bbox[i][0]]
            coordinates.append([(int(bbox[i][0][0][0]) + int(bbox[i][0][2][0]))//2, (int(bbox[i][0][0][1]) + int(bbox[i][0][2][1]))//2])

            location[ids[i][0]]=coordinates
    #         print(location)     
    # print(location)
    return [location]




vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
vid.set(3,1420)
vid.set(4,800)

change = 0
width = 1420
height = 800    




cxg, cyg = 1420, 800
cxb, cyb = 1420, 800
dx, dy = 0, 1
index=1
l=0
k = 0

degs=0
while True:
    success, frame = vid.read()
    pts1 = np.float32([[74, 68], [1193, 47], [7, 644], [1272, 664]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))
    
    arucoDetected = detectMarker(frame)
    center=location[l][4]
    cx=center[0]
    cy=center[1]

    if not arucoDetected[0] == []:
        g, b = location[l][1], location[l][2]
        cxg, cyg = g
        cxb, cyb = b
        dx, dy = g[0] - b[0], g[1] - b[1]



    if cxg >= cxb and cyg <= cyb:
        rads = atan2(dy,dx)
        intHeadingDeg = degrees(rads)
        intHeadingDeg = intHeadingDeg - 90
    # Quad II -- Good
    elif cxg >= cxb and cyg >= cyb:
        rads = atan2(dx,dy)
        intHeadingDeg = degrees(rads)
        intHeadingDeg = (intHeadingDeg * -1)
    # Quad III
    elif cxg <= cxb and cyg >= cyb:
        rads = atan2(dx,-dy)
        intHeadingDeg = degrees(rads)
        intHeadingDeg = intHeadingDeg + 180 
        # degs = 3
    elif cxg <= cxb and cyg <= cyb:
        rads = atan2(dx,-dy)
        intHeadingDeg = degrees(rads) + 180
 
        # degs = 4
    
    print(cx, cy)
    agl=intHeadingDeg + k
    if cy > py: 
        h = min(60, (cy - py // 6))

        
        h1 = str(min(30, (cy - py // 6)))
        h2 = str(min(60, (cy - py // 6)))
        h = str(max(0, h))
        
        h = '0'*(3-len(h)) + h
        h1 = '0'*(3-len(h1)) + h1
        h2 = '0'*(3-len(h2)) + h2
        dictionary = {'func': f'0101{h2}{h1}'}
        print ("Forward")
    # elif -20 < agl < 20:
    #     h = min(60, (cx - py // 6))

        
    #     h1 = str(min(30, (cx - py // 6)))
    #     h2 = str(min(60, (cx - py // 6)))
    #     h = str(max(0, h))
        
    #     h = '0'*(3-len(h)) + h
    #     h1 = '0'*(3-len(h1)) + h1
    #     h2 = '0'*(3-len(h2)) + h2

    elif agl > 35 and k == 90:
        # h1 = str(max(0, 110-int(abs(90-agl))))
        # h1 = '0'*(3-len(h1)) + h1

        # h2=str(max(0,110-int(abs(90-agl))))
        # h2 = '0'*(3-len(h2)) + h2
        dictionary = {'func': f'0110125125'} 
    else:
        k = 90
        dictionary = {'func': '0000000000'}

    json_object = json.dumps(dictionary, indent=4)
    print(json_object)
    with open("data.json", "w") as file:
        file.write(json_object)

    # frame = cv2.line(frame,(cxb, cyb),  (tX, tY), (255, 255, 0), 2)
    frame = cv2.circle(frame, location[l][4], 7, (0, 255, 0), -1)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break