import cv2
import numpy as np
from utils import *
from motion import *

induct = read_data()[0]
destNo = 0
laut_jao=0

dictionary = {'bot1': '10100000000', 'bot2': '10100000000'}

location = {i: [[0, 0] for j in range(5)] for i in range(0, 50)}
destination = [{'M': [1196, 201], 'D':[1204, 412], 'K':[1209, 629]}]

vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
vid.set(3, 1420)
vid.set(4, 1420)

while True:
    _, frame = vid.read()

    location = detectMarker(frame, location, markerSize=4,totalMarker=50, draw=True)
    corners = [location[i][4] for i in range(46, 50)]
    frame = warp(frame, corners)

    move_bot(location, destination[0]['M'],laut_jao)#[induct[destNo][1]])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
