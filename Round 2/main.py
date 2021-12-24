import cv2
import numpy as np
import socket
import threading
from utils import *
import motion1
import motion2
import time

dictionary = {'bot1': '10100000000', 'bot2': '10100000000'}

def cvFunc():
    global dictionary
    induct = read_data()
    destNo1 = 0
    destNo2 = 0
    port = [0, 1]

    location = {i: [[0, 0] for j in range(5)] for i in range(0, 8)}
    destination = [{
                    'M':[[862,144], [850, 167], [875,20]],
                    'D':[[862,322], [855, 343], [875,20]],
                    'K':[[862,495], [860, 516], [875,20]],
                    'C':[[862,144], [850, 155], [875,20]],
                    'B':[[862,322], [850, 333], [875,20]],
                    'H':[[862,495], [860, 506], [875,20]],
                    'P':[[840, 71], [640, 100], [875,25]],
                    'A':[[850, 71], [524, 115], [510, 325], [875,25]],
                    'J':[[850, 71], [524, 115], [505, 507], [875,25]]},
                    
                   {
                    'P':[[690,158], [673,177], [660,24]],
                    'A':[[690,345], [673,348], [660,24]],
                    'J':[[690,523], [673,533], [660,24]],
                    'C':[[690,168], [695,175], [660,24]],
                    'B':[[690,345], [695,350], [660,24]],
                    'H':[[690,523], [695,535], [660,24]],
                    'M':[[690,286], [940,265], [635,24]],
                    'D':[[690,246], [940,265], [635,24]],
                    'K':[[690,286], [1034,235], [1030,499], [635,24]]}]

    vid = cv2.VideoCapture(2)
    vid.set(3, 1420)
    vid.set(4, 800)

    while True:
        then = time.time()
        _, frame = vid.read()
        now = time.time()
        print(now - then)

        location = detectMarker(
            frame, location, markerSize=4, totalMarker=50, draw=True)

        corners = [location[i][4] for i in range(4, 8)]
        frame = warp(frame, corners)
        print("BOT1 -", induct[0][destNo1][1], location[port[0]][4], end=" ")
        dictionary, destNo1 = motion1.move_bot(
            location, destination[0][induct[0][destNo1][1]], destNo1, dictionary, induct[0][destNo1][1], port[0])

        # print("BOT2 -", induct[1][destNo2][1], location[port[1]][4], end=" ")
        # dictionary, destNo2 = motion2.move_bot(
        #     location, destination[1][induct[1][destNo2][1]], destNo2, dictionary, induct[1][destNo2][1], port[1])
        # collision(location,dictionary,induct[1][destNo2][1])
        print(dictionary, "\n")

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


def socketFunc1():
    global dictionary
    port = 1111
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)
    while True:
        client, addr = s.accept()
        client.settimeout(10)
        print("BOT1 - ", dictionary['bot1'])
        client.send(bytes(dictionary['bot1'], encoding='utf8'))
        client.close()


def socketFunc2():
    global dictionary
    port = 3333
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)

    while True:
        client, addr = s.accept()
        client.settimeout(10)
        print("BOT2 - ", dictionary['bot2'])
        client.send(bytes(dictionary['bot2'], encoding='utf8'))
        client.close()


socketThread = threading.Thread(target=socketFunc1)
socketThread.start()

socketThread = threading.Thread(target=socketFunc2)
socketThread.start()

cvThread = threading.Thread(target=cvFunc)
cvThread.start()
