import pandas as pd
import cv2
import cv2.aruco as aruco
import numpy as np
from math import atan2, degrees

height = 750
width = 750
(centerX, centerY) = (width // 2, height // 2)

def read_data():
    df = pd.read_csv('/home/neeraj/Robosapians/Round 2/dat.csv', usecols=['Induct Station', 'Destination'])
    induct = [np.array(df[:141]), np.array(df[141:])]
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

    # if center[0]>tX and center[1]<tY:
    #     rads=atan2(center[0]-tX,tY-center[1])
    #     degs=degrees(rads)
    
    # elif center[0]<tX and center[1]<tY:
    #     rads=atan2(tX-center[0],tY-center[1])
    #     degs=degrees(rads)
    # elif center[0]<tX and center[1]>tY:
    #     rads=atan2(tX-center[0],center[1]-tY)
    #     degs=degrees(rads)
    # else:
    #     rads=atan2(center[0]-tX,center[1]-tY)
    #     degs=degrees(rads)


    if degs > 180:
        degs = degs-360

    # print("degrees-> ",degs)
    # print("Tx ",tX,"TY", tY,"centre 0" ,center[0], "center 1", center[1])

    shortestAngle = degs - intHeadingDeg
    if shortestAngle > 180:
        shortestAngle -= 360
    elif shortestAngle < -180:
        shortestAngle += 360
    # print(shortestAngle)

    return [shortestAngle, intHeading]