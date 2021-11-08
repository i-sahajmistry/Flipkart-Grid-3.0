import cv2
import cv2.aruco as aruco
import numpy as np
import imutils
import time 
import math
from math import atan2, degrees
import json
import os

index=1
bot=[[1],[2],[3],[4]]


location={i: [[0, 0] for j in range(5)] for i in range(4)}
arr = [[[110, 108], [598, 765]], [[112, 39], [670, 766]], [[1306, 28], [747, 763]], [[1310, 102], [825, 765]]]
def displacement(x, y, a, b):
    disp = abs(((x - a) ** 2 + (y - b) ** 2) ** (1 / 2))
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
index=0
cx,cy=width,height
px,py=100,150
laut_jao=0
l=0
k=0
degs=0
while True:

    tX = arr[l][index][0]
    tY = arr[l][index][1]
    success, frame = vid.read()
    pts1 = np.float32([[74, 68], [1193, 47], [7, 644], [1272, 664]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))
    
    arucoDetected = detectMarker(frame)
    center=location[l][4]
    if not arucoDetected[0] == []:
        g, b = location[l][1], location[l][2]
        cxg, cyg = g
        cxb, cyb = b
        cx, cy = cxb, cyb
        dx, dy = g[0] - b[0], g[1] - b[1]
    # disp = displacement(location[l][4][0], location[l][4][1], tX, tY)
  
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
    if intHeadingDeg>180:
        intHeadingDeg=intHeadingDeg-360


    dx = center[0] - tX
    dy = center[1] - tY

    if tX >= center[0] and tY <= center[1]:
        rads = atan2(dy,dx)
        degs = degrees(rads)
        degs = degs - 90
    # Quad II -- Good
    elif tX >= center[0] and tY >= center[1]:
        rads = atan2(dx,dy)
        degs = degrees(rads)
        degs = (degs * -1)
    # Quad III
    elif tX <= center[0] and tY >= center[1]:
        rads = atan2(dx,-dy)
        degs = degrees(rads)
        degs = degs + 180 
        # degs = 3
    elif tX <= center[0] and tY <= center[1]:
        rads = atan2(dx,-dy)
        degs = degrees(rads) + 180
        # degs = 4
    if degs>180:
        degs=degs-360
            
    # if(index>3):
    #     degs=degs+90
    #     intHeadingDeg=intHeadingDeg-90

    shortestAngle =degs - intHeadingDeg
    if shortestAngle > 180:
        shortestAngle -= 360
    
    if shortestAngle < -180:
        shortestAngle += 360
    
    
    


    # h1 = str(max(0, h - int(shortestAngle)))
    # h2 = str(max(0, min(255, h + int(shortestAngle))))
    # h = str(max(0, h))
    
    # h = '0'*(3-len(h)) + h
    # h1 = '0'*(3-len(h1)) + h1
    # h2 = '0'*(3-len(h2)) + h2
    # print(shortestAngle,"👀👀👀👀")
    # if shortestAngle <= 10 and shortestAngle >= -10:
    #     tranx = 3
    #     dictionary = {'func': f'1010{h}{h}'}
    #     print ("Forward")
    # elif shortestAngle >= 1:
    #     tranx = 2
        
    #     print ("Turn Right")
    #     dictionary = {'func': f'1010{h1}{h2}'}
    # elif shortestAngle < 1:
    #     tranx = 4
    #     dictionary = {'func': f'1010{h2}{h1}'}
    #     print ("Turn Left")
    # print(degs,intHeadingDeg,center,shortestAngle)


    agl=intHeadingDeg + k
    # print(agl, cx, cy)
    h = 100
    print(tX,tY,index)



    if laut_jao==0:
        
        if cy>py and k == 0:

            h1 = str(min(100, cy))
            h2 = str(min(120, cy+20))

            h1 = '0'*(3-len(h1)) + h1
            h2 = '0'*(3-len(h2)) + h2
            

            print(h1, h2, (cy - py) // 3)
            dictionary = {'func': f'0101070070','l':l}
            # dictionary = {'func': f'0101{h2}{h1}','l':l}
            print ("Forward")
        elif agl > 20:
            dictionary = {'func': f'0110090090','l':l} 
        elif cx < 150-80:
            print("stop")
            dictionary = {'func': '0000000000','l':l}
            k=0
            laut_jao=1
            index=1

        elif cx < 250-80:
            h1 = str(max(0, min(255, 40)))
            h2 = str(max(0, min(255, 70)))
            h1 = '0'*(3-len(h1)) + h1
            h2 = '0'*(3-len(h2)) + h2
            dictionary = {'func': f'0101{h2}{h1}','l':l}
            
        else:
            k=90
            print("Left")   
            h1 = str(max(0, min(255, 40 + int(shortestAngle * 2))))
            h2 = str(max(0, min(255, 70 - int(shortestAngle * 2))))
            # h = str(max(0, h))
            # h = '0'*(3-len(h)) + h
            h1 = '0'*(3-len(h1)) + h1
            h2 = '0'*(3-len(h2)) + h2
            dictionary = {'func': f'0101{h2}{h1}','l':l}


    else:
        if cx <  550: 
            
            h1 = (min(70, (cx - px // 6)  ))
            h2 = (min(40, (cx - px // 6)))

            h1=str(max(0,h1))
            h2=str(max(0,h2))            
            
            h1 = '0'*(3-len(h1)) + h1
            h2 = '0'*(3-len(h2)) + h2
            dictionary = {'func': f'1010060040','l':l}
            print (" backrward")


              
        elif agl < -25 :
            print("rotate")
            dictionary = {'func': f'1001125125','l':l}
        
        elif cy>640:
            print("stop")
            dictionary = {'func': f'0000000000','l':l} 
            laut_jao=0
            index = 0
        
        else:
            k = 0
            # h1=str(40)
            # h2=str(70)
            h1 = str(max(0, min(255, 40)))# - int(4* shortestAngle))))
            h2 = str(max(0, min(255, 70)))# + int(4 * shortestAngle))))
            h1 = '0'*(3-len(h1)) + h1
            h2 = '0'*(3-len(h2)) + h2
            dictionary = {'func': f'1010{h1}{h2}','l':l}
            print ("straight back")



    json_object = json.dumps(dictionary, indent=4)
    print(json_object)
    with open("data.json", "w") as file:
        file.write(json_object)
    for i in arr[l]:
        frame = cv2.circle(frame, (i[0], i[1]), 7, (0, 255, 0), -1)

    # frame = cv2.line(frame,(cxb, cyb),  (tX, tY), (255, 255, 0), 2)
    frame = cv2.circle(frame, location[l][4], 7, (0, 255, 0), -1)
    cv2.imshow('frame', frame)
    cv2.waitKey(10)
    # if cv2.waitKey(0) == ord('q'):
    #     break