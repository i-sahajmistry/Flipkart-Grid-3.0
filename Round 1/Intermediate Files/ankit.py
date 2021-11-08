import json
import math
import os
import socket
import time
from math import atan2, degrees
import threading
import cv2
import cv2 as cv
import cv2.aruco as aruco
import imutils
import numpy as np


dictionary = {'func': '1010000000', 'l': 3}
starttime = time.time()
endtime = 0
time_start = False
   

def cvfunc():
    global dictionary, time_start, starttime, endtime

    index = 1
    bot = [[1], [2], [3], [4]]

    location = {i: [[0, 0] for j in range(5)] for i in range(-1, 4)}    
    arr = [[[570, 120], [115, 145], [560, 130], [520, 737]], 
           [[550, 130], [120, 85], [540, 120], [610, 730]], 
           [[700, 120], [1315, 40], [821, 120], [680, 737]], 
           [[761, 180], [1315, 120], [781, 130], [775, 747]]]
    for i in range(4):
        location[i][4] = arr[i][3]
# 1270, 120 
    def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
        arucoDict = aruco.Dictionary_get(key)

        arucoParam = aruco.DetectorParameters_create()
        bbox, ids, rejected = aruco.detectMarkers(
            imgGray, arucoDict, parameters=arucoParam)

        if draw:
            aruco.drawDetectedMarkers(img, bbox)

        if ids is not None:

            for i in range(len(ids)):

                coordinates = [[int(j[0]), int(j[1])] for j in bbox[i][0]]
                coordinates.append([(int(bbox[i][0][0][0]) + int(bbox[i][0][2][0])) //
                                   2, (int(bbox[i][0][0][1]) + int(bbox[i][0][2][1]))//2])

                location[ids[i][0]] = coordinates
        return [location]

    def getAngle(cxb, cyb, cxg, cyg, dx, dy, tX, tY, location):
        center = location[l][4]
        if not arucoDetected[0] == []:
            g, b = location[l][1], location[l][2]
            cxg, cyg = g
            cxb, cyb = b
            cx, cy = cxb, cyb
            dx, dy = g[0] - b[0], g[1] - b[1]

        if cxg >= cxb and cyg <= cyb:
            rads = atan2(dy, dx)
            intHeadingDeg = degrees(rads)
            intHeadingDeg = intHeadingDeg - 90

        elif cxg >= cxb and cyg >= cyb:
            rads = atan2(dx, dy)
            intHeadingDeg = degrees(rads)
            intHeadingDeg = (intHeadingDeg * -1)

        elif cxg <= cxb and cyg >= cyb:
            rads = atan2(dx, -dy)
            intHeadingDeg = degrees(rads)
            intHeadingDeg = intHeadingDeg + 180

        elif cxg <= cxb and cyg <= cyb:
            rads = atan2(dx, -dy)
            intHeadingDeg = degrees(rads) + 180

        if intHeadingDeg > 180:
            intHeadingDeg = intHeadingDeg-360

        dx = center[0] - tX
        dy = center[1] - tY

        if tX >= center[0] and tY <= center[1]:
            rads = atan2( dy, dx)
            degs = degrees(rads)
            degs = degs - 90

        elif tX >= center[0] and tY >= center[1]:
            rads = atan2(dx, dy)
            degs = degrees(rads)
            degs = (degs * -1)

        elif tX <= center[0] and tY >= center[1]:
            rads = atan2(dx, -dy)
            degs = degrees(rads)
            degs = degs + 180

        elif tX <= center[0] and tY <= center[1]:
            rads = atan2(dx, -dy)
            degs = degrees(rads) + 180

        if degs > 180:
            degs = degs-360

        shortestAngle = degs - intHeadingDeg
        if shortestAngle > 180:
            shortestAngle -= 360

        if shortestAngle < -180:
            shortestAngle += 360
        return [shortestAngle, intHeadingDeg, cx, cy]

    vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    vid.set(3, 1420)
    vid.set(4, 800)

    width = 1420
    height = 800

    stop = 0
    s = 0

    then = 0

    # array=[[580,747],[588,117],[109,132]9
    py = [[150, 630], [190, 700], [240, 670], [280, 675]]   
    px = [[145, 545], [140, 425], [1260, 895], [1260, 931]]

    cxg, cyg = 598, 765
    cxb, cyb = 598, 765
    dx, dy = 0, 1
    cx, cy = 598, 765

    index = 0
    laut_jao = 0
    degs = 0
    l = 3
    k = 0

    while True:
        multiply = 14
        max_speed=255
        rpm1 = 255
        rpm2 = 255
        if l == 0:
            rpm1 = 80
            rpm2= 80
            multiply = 1.5
        if l==1:
            rpm1 = 255
            rpm2= 255

            # max_speed=120

            
        tX = arr[l][index][0]
        tY = arr[l][index][1]

        success, frame = vid.read() 

        pts1 = np.float32([[74, 68], [1193, 47], [7, 644], [1272, 664]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        frame = cv2.warpPerspective(frame, matrix, (width, height))

        arucoDetected = detectMarker(frame)
        center = location[l][4]

        shortestAngle, intHeadingDeg, cx, cy = getAngle(
            cxb, cyb, cxg, cyg, dx, dy, tX, tY, location)
        agl = intHeadingDeg + k


        # print(cx, cy)


        if stop == 1:
            now = time.time()
            if s == 0:
                then = time.time()
                s = 1
            elif now - then > 0.1 :
                s = 0
                stop = 0

        elif stop == 2:

            dictionary = {'func': f'0000000000', 'l': l}
            now = time.time()
            dictionary = {'func': f'0000000000', 'l': l}
            if s == 0:
                then = time.time()
                s = 1

            elif now - then > 0.4:
                s = 0
                stop = 0

            print("stop", dictionary, now - then)

        elif stop == 3:
            dictionary = {'func': f'0000000000', 'l': 0}
            l = 0

        else:
    
            if laut_jao == 0:
                if(l == 0 or l == 1):
                    if cy > py[l][0] and k == 0:
                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'1010{h2}{h1}', 'l': l}
                        # print(shortestAngle)
                        print("Forward")

                    elif agl > 20 and l == 0:
    
                        dictionary = {'func': f'01100690690', 'l': l}
                        print("rotate")

                    elif cx < px[l][0]:
                        print("stop")
                        dictionary = {'func': '00000000001', 'l': l}
                        k = 0
                        laut_jao = 1
                        index = 2
                        stop = 1

                    else:
                        index = 1
                        k = 90

                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'1010{h2}{h1}', 'l': l}
                        # dictionary = {'func': f'1010100100','l':l}
                        print("Left")
                else:
                    if cy > py[l][0] and k == 0:
                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'1010{h2}{h1}', 'l': l}
                        # print(shortestAngle)
                        print("Forward")

                    elif agl < -20 and l == 0:
    
                        dictionary = {'func': f'10011601600', 'l': l}
                        print("rotate")

                    elif cx > px[l][0]:
                        dictionary = {'func': '00000000001', 'l': l}
                        k = 0
                        laut_jao = 1
                        index = 2
                        stop = 1

                    else:
                        index = 1

                        k = -90
                        print(cy,py[l][0])

                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'1010{h2}{h1}', 'l': l}
                        # dictionary = {'func': f'1010100100','l':l}
                        print("Left")

            else:
                if(l == 0 or l == 1):
                    if cx < px[l][1] and cy < 500:

                        # print("💖",shortestAngle)
                        if shortestAngle < 0:
                            shortestAngle += 180
                        else:
                            shortestAngle -= 180
                        # print("✨",shortestAngle)
                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'0101{h1}{h2}', 'l': l}
                        # dictionary = {'func': f'0101080080','l':l}
                        # print("🌹", dictionary)
                        print("Backwards")

                    elif agl < -15 and l == 0:
                        index = 2
                        dictionary = {'func': f'10010660660', 'l': l}
                        print("rotate")

                    elif cy > py[l][1]:
                        print("stop")
                        dictionary = {'func': f'0000000000', 'l': l}
                        l -= 1
                        laut_jao = 0
                        index = 0
                        stop = 2
                    else:
                        k = 0
                        index = 3

                        if shortestAngle < 0:
                            shortestAngle += 180
                        else:
                            shortestAngle -= 180

                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'0101{h1}{h2}', 'l': l}
                        print("straight back")

                else:
                    if cx > px[l][1] and cy < 500:

                        # print("💖",shortestAngle)
                        if shortestAngle < 0:
                            shortestAngle += 180
                        else:
                            shortestAngle -= 180
                        # print("✨",shortestAngle)
                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'0101{h1}{h2}', 'l': l}
                        # dictionary = {'func': f'0101080080','l':l}
                        # print("🌹", dictionary)
                        print("Backwards")

                    elif agl > 30 and l == 0:
                        index = 2
 
                        dictionary = {'func': f'01100650650', 'l': l}
                        print("rotate")

                    elif cy > py[l][1]:
                        print("stop")
                        dictionary = {'func': f'0000000000', 'l': l}
                        l -= 1
                        laut_jao = 0
                        index = 0
                        stop = 2
                    else:
                        k = 0
                        index = 3

                        if shortestAngle < 0:
                            shortestAngle += 180
                        else:
                            shortestAngle -= 180

                        h1 = str(max(0, min(max_speed, rpm1 - int(shortestAngle * multiply))))
                        h2 = str(max(0, min(max_speed, rpm2 + int(shortestAngle * multiply))))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'0101{h1}{h2}', 'l': l}
                        print("straight back")
        if l == -1:
            dictionary = {'func': f'0000000000', 'l': 0}
            endtime = time.time()
            stop = 3
            continue

            # print(dictionary)
        for j in arr[l]:
            frame = cv2.circle(frame, (j[0], j[1]), 7, (0, 255, 0), -1)
        frame = cv2.circle(frame, location[l][4], 7, (0, 255, 0), -1)

        font = cv2.FONT_HERSHEY_SIMPLEX  #font to apply on text
        if endtime:
            cv2.putText(frame,f'Time: {str(round (endtime-starttime,3))}', (100, 650), font, 1.35, (0, 0, 0), 3) # add text on frame
        elif time_start:
            cv2.putText(frame,f'Time: {str(round (time.time()-starttime,3))}', (100, 650), font, 1.35, (0, 0, 0), 3) # add text on frame
        else:
            cv2.putText(frame,f'Time: 0.000', (100, 650), font, 1.35, (0, 0, 0), 3) # add text on frame


        cv2.imshow('frame', frame)
        cv2.waitKey(10)
        now = time.time()
    


def socketfunc():
    
    global dictionary, time_start, starttime, endtime

    ports = [1238, 1235, 1236, 1237]
    s = []
    for i in range(4):
        s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        s[i].bind(('0.0.0.0', ports[i]))
        s[i].listen(0)
    index = 3
    while True:
        then = time.time()
        client, addr = s[index].accept()
        if not time_start:
            time_start = True
            starttime = time.time()
        client.settimeout(10)
        y = dictionary
        print(y)
        client.send(bytes(y['func'], encoding='utf8'))
        index = y['l']
        client.close()

        now = time.time()
        # print(y, "s", now - then)


socketThread = threading.Thread(target=socketfunc)
socketThread.start()

cvThread = threading.Thread(target=cvfunc)
cvThread.start()