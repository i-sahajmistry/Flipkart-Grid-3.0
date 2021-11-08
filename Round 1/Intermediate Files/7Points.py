import cv2
import cv2.aruco as aruco
import threading
import numpy as np
import imutils
import time 
import socket
import math
from math import atan2, degrees
import json
import os

dictionary = {'func': '0000000000', 'l': 0}

index=1


location={i: [[0, 0] for j in range(5)] for i in range(4)}
arr = [[610,738], [620,450], [660,300], [670,180], [397,78], [218,105], [83,105]]

def displacement(x, y, a, b):
    disp = abs(((x - a) ** 2 + (y - b) ** 2) ** (1 / 2))
    return disp

def cvfunc():

    arr = [[610,738], [620,450], [660,300], [670,180], [397,78], [218,105], [83,105]]
    global dictionary


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
    tX = arr[index][0]
    tY = arr[index][1]

    degs=0
    while True:
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
            dx, dy = g[0] - b[0], g[1] - b[1]
        disp = displacement(location[l][4][0], location[l][4][1], arr[index][0], arr[index][1])

        if(change % 2 ==0):
            if(index<4):
                if (disp <= 25 or location[l][4][1]<arr[index][1]):
                    print("🙌🙌🙌🔥 achieved", arr[index])
                    

                    index = (index+1) % 7
                    tX = arr[index][0]
                    tY = arr[index][1]
            else:
                if (disp <= 25 or location[l][4][0] < arr[index][0]):
                    print("🙌🙌🙌🔥 achieved", arr[index])
                # dots = dots+1

                    if(index == 6):
                        change = change+1
                        arr = arr[::-1]
                        print("Goal reached🤳🐱‍🏍🐱‍🏍🐱‍🏍🐱‍🏍")
                        dictionary = {'func': f'0000000000'}
                        json_object = json.dumps(dictionary, indent=4)
                        print(json_object)
                        with open("data.json", "w") as file:
                            file.write(json_object)
                        time.sleep(10)
                        index = index+1

                    index = (index+1) % 7
                    tX = arr[index][0]
                    tY = arr[index][1]
            
        else:
            if(index < 4):
                if (disp <= 25 or location[l][4][0]> arr[index][0]):
                    print("🙌🙌🙌🔥 achieved", arr[index])

                    index = (index+1) % 7
                    tX = arr[index][0]
                    tY = arr[index][1]
            else:
                if (disp <= 25 or location[l][4][1]> arr[index][1]):
                    print("🙌🙌🙌🔥 achieved", arr[index])
                # dots = dots+1

                    if(index == 6):
                        change = change+1
                        if(change % 2 == 0):
                            l = int(change/2)
                        arr = arr[::-1]
                        index = index+1

                    index = (index+1) % 7
                    tX = arr[index][0]
                    tY = arr[index][1]

        # if(change%2==0):
        #     l=int(change/2)
            



        


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
        if(index < 4):
            h = min(60, (location[l][4][1] - tY))
        else:
            h = min(60, (location[l][4][0] - tX))


        h1 = str(max(0, h + 5*int(shortestAngle)))
        h2 = str(max(0, h - 5*int(shortestAngle)))
        h = str(max(0, h))
        
        h = '0'*(3-len(h)) + h
        h1 = '0'*(3-len(h1)) + h1
        h2 = '0'*(3-len(h2)) + h2
        print(shortestAngle,"👀👀👀👀")
        if shortestAngle <= 10 and shortestAngle >= -10:
            dictionary = {'func': f'1010{h}{h}', 'l': l}
            print ("Forward")
        elif shortestAngle >= 1:
            print ("Turn Right")
            dictionary = {'func': f'1010{h1}{h2}', 'l': l}
        elif shortestAngle < 1:
            tranx = 4
            dictionary = {'func': f'1010{h2}{h1}', 'l': l}
            print ("Turn Left")
        # print(degs,intHeadingDeg,center,shortestAngle)

        # json_object = json.dumps(dictionary, indent=4)
        # print(json_object)
        # with open("data.json", "w") as file:
        #     file.write(json_object)
        # for i in arr:
        #     frame = cv2.circle(frame, (i[0], i[1]), 7, (0, 255, 0), -1)

        # frame = cv2.line(frame,(cxb, cyb),  (tX, tY), (255, 255, 0), 2)
        frame = cv2.circle(frame, location[l][4], 7, (0, 255, 0), -1)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break


def socketfunc():

    global dictionary

    ports = [1234, 1239, 1240, 1241]
    s = []
    print('b')
    for i in range(4):
        s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        s[i].bind(('0.0.0.0', ports[i]))
        s[i].listen(0)
    index =0
    while True:
        print('a')
        client, addr = s[index].accept()
        client.settimeout(50)
        y = dictionary
        print(y)
        client.send(bytes(y['func'], encoding='utf8'))
        index=y['l']
        client.close()
 
socketThread = threading.Thread(target=socketfunc)
socketThread.start()

cvThread = threading.Thread(target=cvfunc)
cvThread.start()