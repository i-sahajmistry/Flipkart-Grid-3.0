import csv
import os
from math import atan2, degrees

import cv2
import cv2.aruco as aruco
import numpy as np
import pandas as pd

from config.definitions import ROOT_DIR

height = 750
width = 750
(centerX, centerY) = (width // 2, height // 2)
flag = 0
colDict = []

def read_data():
    df = pd.read_csv(os.path.join(ROOT_DIR, 'csv', 'bot1.csv'))
    columns_titles = ["Induct Station", "Destination", "Shipment"]
    df=df.reindex(columns=columns_titles)
    induct = [np.array(df)]
    # induct=np.array(induct)
    df = pd.read_csv(os.path.join(ROOT_DIR, 'csv', 'bot2.csv'))
    df=df.reindex(columns=columns_titles)
    induct.append(np.array(df))
    # print(induct)    
    
    return induct

def detectMarker(img, location, markerSize=4, totalMarker=50, draw=True):
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
    return location


def warp(frame, corners):
    pts1 = np.float32(corners)
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))
    M = cv2.getRotationMatrix2D((centerX, centerY), 90, 1.0)
    frame = cv2.warpAffine(frame, M, (width, height))
    return frame


def getSpeeds(target, destination, postiton):
    dist = displacement(destination[target][0], destination[target][1], postiton[0], postiton[1])
    print(dist)
    h1 = int(max(min(100, dist//2.3), 40))
    h2 = int(max(min(100, dist//2.3), 40))
    return h1, h2


def getAngle(location, destination, laut_jao):
    
    tX, tY = destination
    center = location[4]
    g, b = location[1], location[2]
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
    
    if intHeadingDeg > 0:
        intHeading = intHeadingDeg - 180
    else:
        intHeading = intHeadingDeg + 180

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
    elif shortestAngle < -180:
        shortestAngle += 360

    return [shortestAngle, intHeading]


def anticlockwise(dictionary, bot_no, servo):
    dictionary[f'bot{bot_no}'] = f'0110120120{servo}'
    return dictionary

def clockwise(dictionary, bot_no, servo):
    dictionary[f'bot{bot_no}'] = f'1001120120{servo}'
    return dictionary

def pause(dictionary, bot_no, servo):
    dictionary[f'bot{bot_no}'] = f'1010000000{servo}'
    return dictionary

def displacement(x, y, a, b):
    disp = abs(((x - a) ** 2 + (y - b) ** 2) ** (1 / 2))
    return disp

def collision(location,dictionary,letter):
    global flag, colDict
    distance=displacement(location[0][4][0],location[0][4][1],location[1][4][0],location[1][4][1])
    if(distance>130):
        flag = 0
        return

    if flag:
        dictionary[colDict[0]] = colDict[1]

    flag = 1
    if(letter in ['M','D','K']):
        dist1=displacement(location[0][4][0],location[0][4][1], 833, 264)
        dist2=displacement(location[1][4][0],location[1][4][1], 833, 264)
        if(dist1>dist2):
            dictionary['bot1'] = f'10010000000'
            colDict = ['bot1', dictionary['bot1']]
        else:
            dictionary['bot2'] = f'10010000000'
            colDict = ['bot2', dictionary['bot2']]

    else:
        dist1=displacement(location[0][4][0],location[0][4][1], 670, 79)
        dist2=displacement(location[1][4][0],location[1][4][1], 670, 79)
        if(dist1>dist2):
            dictionary['bot1'] = f'10010000000'
            colDict = ['bot1', dictionary['bot1']]
        else:
            dictionary['bot2'] = f'10010000000'    
            colDict = ['bot2', dictionary['bot2']]

