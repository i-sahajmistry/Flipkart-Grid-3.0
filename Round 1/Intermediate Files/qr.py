import cv2
import cv2.aruco as aruco
import numpy as np
import os


def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    arucoDict = aruco.Dictionary_get(key)

    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)
    # print(bbox)
    # print(rejected)
    print()
    center = []
    if draw:
        aruco.drawDetectedMarkers(img, bbox)
        if len(bbox) != 0:
            bbox = bbox[0][0]
            # print(bbox)
            center.append([(int(bbox[0][0]) + int(bbox[2][0]))//2, (int(bbox[0][1]) + int(bbox[2][1]))//2])

    return [bbox, ids, center]


def arAug(bbox, ids, imgAug, drawId=True):
    pass


def main():
    vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:
        success, frame = vid.read()
        arucoDetected = detectMarker(frame)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()