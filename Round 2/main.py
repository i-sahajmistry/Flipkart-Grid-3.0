import cv2
import numpy as np
from utils import *

vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
vid.set(3, 1420)
vid.set(4, 1420)

height = 750
width = 750
(centerX, centerY) = (width // 2, height // 2)

location = {i: [[0, 0] for j in range(5)] for i in range(46, 50)}    
location[1] = [[0, 0] for j in range(5)]

des1=[[1196,201],[1204,412],[1209,629]]


while True:
    _, frame = vid.read()


    detectMarker(frame, location, markerSize=4, totalMarker=50, draw=True)
    corners = [location[46][4], location[47][4], location[49][4], location[48][4]]
    pts1 = np.float32(corners)
    pts2 = np.float32([[680,25], [width+680, 25], [0+680, height+25], [width+680, height+25]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))

    M = cv2.getRotationMatrix2D((centerX, centerY), 90, 1.0)
    frame = cv2.warpAffine(frame, M, (width, height))

    detectMarker(frame, location, markerSize=4, totalMarker=50, draw=True)
    
    print(location[1][4])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

