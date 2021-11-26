import cv2
import numpy as np
import socket
import threading
from utils import *
import motion1
import motion2

dictionary = {'bot1': '10100000000', 'bot2': '10100000000'}


def cvFunc():
    global dictionary
    induct = read_data()
    destNo1 = 0
    destNo2 = 0

    location = {i: [[0, 0] for j in range(5)] for i in range(0, 8)}
    destination = [{'M': [[833, 160], [830, 50]],
                    'D':[[833, 330], [830, 50]],
                    'K':[[833, 500], [830, 50]],
                    'C':[[833, 160], [800, 190], [830, 50]],
                    'B':[[833, 330], [800, 360], [830, 50]],
                    'H':[[833, 500], [800, 530], [830, 50]],
                    'P':[[834, 95], [504, 110], [508, 174], [830, 50]],
                    'A':[[834, 95], [504, 110], [508, 337], [830, 50]],
                    'J':[[834, 95], [504, 110], [508, 512], [830, 50]]},
                    
                    {'P': [[632,151], [631,40]],
                    'A':[[633,323], [631,40]],
                    'J':[[633,489], [631,40]],
                    'C':[[633,151], [679,170], [631,40]],
                    'B':[[633,323], [676,342], [631,40]],
                    'H':[[633,489], [680,509], [631,40]],
                    'M':[[632,117], [955,125], [632,130], [965,159], [631,40]],
                    'D':[[632,117], [955,125], [632,130], [969,320], [631,40]],
                    'K':[[632,117], [955,125], [632,130], [969,505], [631,40]]}]

    vid = cv2.VideoCapture(2)
    vid.set(3, 1420)
    vid.set(4, 800)

    while True:
        _, frame = vid.read()

        location = detectMarker(
            frame, location, markerSize=4, totalMarker=50, draw=True)

        corners = [location[i][4] for i in range(4, 8)]
        frame = warp(frame, corners)
        print(induct[0][destNo1][1], induct[1][destNo2][1])
        dictionary, destNo1 = motion1.move_bot(
            location, destination[0][induct[0][destNo1][1]], destNo1, dictionary)

        dictionary, destNo2 = motion2.move_bot(
            location, destination[1][induct[1][destNo2][1]], destNo2, dictionary)

        print(dictionary, location[1][4])

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


def socketFunc1():
    global dictionary
    port = 2222
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)
    while True:
        client, addr = s.accept()
        client.settimeout(10)
        print(dictionary)
        client.send(bytes(dictionary['bot1'], encoding='utf8'))
        client.close()


def socketFunc2():
    global dictionary
    port = 2222
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)

    while True:
        client, addr = s.accept()
        client.settimeout(10)
        print(dictionary)
        client.send(bytes(dictionary['bot2'], encoding='utf8'))
        client.close()


socketThread = threading.Thread(target=socketFunc1)
socketThread.start()

socketThread = threading.Thread(target=socketFunc2)
socketThread.start()

cvThread = threading.Thread(target=cvFunc)
cvThread.start()
# main coordinates 833,199 first move , second turn 639,199,
