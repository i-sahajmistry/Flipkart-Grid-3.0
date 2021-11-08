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


dictionary = {'func': '1010000000', 'l': 0}


def cvfunc():
    global dictionary

    index = 1
    bot = [[1], [2], [3], [4]]

    location = {i: [[0, 0] for j in range(5)] for i in range(4)}
    arr = [[[580, 140], [75,125], [580, 140], [550, 747]], [[580, 140], [178,49], [580, 140], [627, 744]], [
        [781, 160], [1345, 10], [781, 160], [747, 763]], [[781, 160], [1345, 81], [781, 160], [604,636]]]

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
        center=location[l][4]
        if not arucoDetected[0] == []:
            g, b = location[l][1], location[l][2]
            cxg, cyg = g
            cxb, cyb = b
            cx, cy = cxb, cyb
            dx, dy = g[0] - b[0], g[1] - b[1]
    
        if cxg >= cxb and cyg <= cyb:
            rads = atan2(dy,dx)
            intHeadingDeg = degrees(rads)
            intHeadingDeg = intHeadingDeg - 90

        elif cxg >= cxb and cyg >= cyb:
            rads = atan2(dx,dy)
            intHeadingDeg = degrees(rads)
            intHeadingDeg = (intHeadingDeg * -1)



        elif cxg <= cxb and cyg >= cyb:
            rads = atan2(dx,-dy)
            intHeadingDeg = degrees(rads)
            intHeadingDeg = intHeadingDeg + 180 

        elif cxg <= cxb and cyg <= cyb:
            rads = atan2(dx,-dy)
            intHeadingDeg = degrees(rads) + 180

        if intHeadingDeg>180:
            intHeadingDeg=intHeadingDeg-360

        dx = center[0] - tX
        dy = center[1] - tY

        if tX >= center[0] and tY <= center[1]:
            rads = atan2(dy,dx)
            degs = degrees(rads)
            degs = degs - 90

        elif tX >= center[0] and tY >= center[1]:
            rads = atan2(dx,dy)
            degs = degrees(rads)
            degs = (degs * -1)

        elif tX <= center[0] and tY >= center[1]:
            rads = atan2(dx,-dy)
            degs = degrees(rads)
            degs = degs + 180 

        elif tX <= center[0] and tY <= center[1]:
            rads = atan2(dx,-dy)
            degs = degrees(rads) + 180

        if degs>180:
            degs=degs-360

        shortestAngle =degs - intHeadingDeg
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

    # array=[[580,747],[588,117],[109,132]]
    py = [[140, 550], [140, 550], [140, 550], [140, 550]]
    px = [[71, 580], [71, 580], [1341, 781], [1341, 781]]

    cxg, cyg = 598, 765
    cxb, cyb = 598, 765
    dx, dy = 0, 1
    cx, cy = 598, 765

    index = 0
    laut_jao = 0
    degs = 0
    l = 0
    k = 0
    while True:
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

        print(cx, cy)
        # shortestAngle, index, laut_jao)

        if stop == 1:
            now = time.time()
            if s == 0:
                then = time.time()
                s = 1
            elif now - then > 5:
                s = 0
                stop = 0
            # print(now, then)
        # if stop==1:
        #     time.sleep(5)
        #     Stop = 0

        elif stop == 2:
            now = time.time()
            if s == 0:
                then = time.time()
                s = 1
            elif now - then > 2:
                s = 0
                stop = 0
            print(l,"🌹")

        else:

            if laut_jao == 0:
                if(l == 0 or l == 1):
                    if cy > py[l][0]+200 and k == 0:
                        h1 = str(max(0, 80 - int(shortestAngle * 4)))
                        h2 = str(max(0, 80 + int(shortestAngle * 4)))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'1010{h2}{h1}', 'l': l}
                        # print(shortestAngle)
                        print("Forward")

                    elif atan2(130-cy,60-cx)-5<agl <atan2(130-cy,60-cx)+5:
                        h1 = str(max(0, 80 - int(shortestAngle * 4)))
                        h2 = str(max(0, 80 + int(shortestAngle * 4)))

                        h1 = '0'*(3-len(h1)) + h1
                        h2 = '0'*(3-len(h2)) + h2
                        dictionary = {'func': f'1010{h2}{h1}', 'l': l}
                        # print(shortestAngle)
                        print("Forward")
                    elif cx < px[l][0]:
                        print("stop")
                        dictionary = {'func': '0000000000', 'l': l}
                        k = 0
                        laut_jao = 1
                        index = 2
                        stop = 1

                    else:
                        index = 1
                        k = 90

                        dictionary = {'func': f'1010090030', 'l': l}
                        # dictionary = {'func': f'1010100100','l':l}
                        print("Left")

        for i in arr[l]:
            frame = cv2.circle(frame, (i[0], i[1]), 7, (0, 255, 0), -1)

        frame = cv2.circle(frame, location[l][4], 7, (0, 255, 0), -1)
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
        now = time.time()        # print("c", now - then)


def socketfunc():

    global dictionary

    ports = [2345, 2346, 2347, 1241]
    s = []
    for i in range(1):
        s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        s[i].bind(('0.0.0.0', ports[i]))
        s[i].listen(0)
    index = 0
    while True:
        then = time.time()
        client, addr = s[index].accept()
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
