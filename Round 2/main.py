import cv2
import socket
import threading
from utils import *
import motion1
import motion2
import time

dictionary = {'bot1': '10100000000', 'bot2': '10100000000'}
startTime = 0

def cvFunc():
    global dictionary, startTime
    induct = read_data()
    destNo1 = 0
    destNo2 = 0
    port = [0, 1]

    location = {i: [[0, 0] for j in range(5)] for i in range(0, 8)}
    destination = [{
                    'M':[[855,144], [865, 167], [865,20]],
                    'D':[[855,322], [865, 343], [855,20]],
                    'K':[[855,495], [865, 516], [855,20]],
                    'C':[[855,144], [845, 155], [865,20]],
                    'B':[[855,322], [845, 333], [865,20]],
                    'H':[[855,495], [850, 506], [865,20]],
                    'P':[[840, 71], [640, 100], [875,25]],
                    'A':[[850, 71], [514, 115], [515, 325], [875,25]],
                    'J':[[850, 71], [514, 115], [505, 507], [875,25]]},
                    
                   {
                    'P':[[690,158], [673,177], [655,24]],
                    'A':[[690,345], [673,348], [655,24]],
                    'J':[[690,523], [673,533], [655,24]],
                    'C':[[690,168], [695,175], [655,24]],
                    'B':[[680,345], [695,350], [655,24]],
                    'H':[[680,523], [695,535], [655,24]],
                    'M':[[690,246], [940,265], [635,24]],
                    'D':[[690,246], [940,265], [635,24]],
                    'K':[[690,246], [1034,250], [1015,499], [635,24]]}]

    vid = cv2.VideoCapture(0)
    vid.set(3, 1420)
    vid.set(4, 800)
    then = time.time()

    while True:
        _, frame = vid.read()

        location = detectMarker(
            frame, location, markerSize=4, totalMarker=50, draw=True)

        corners = [location[i][4] for i in range(4, 8)]
        frame = warp(frame, corners)
        print("BOT1 -", induct[0][destNo1][1], location[port[0]][4], end=" ")
        dictionary, destNo1 = motion1.move_bot(
            location, destination[0][induct[0][destNo1][1]], destNo1, dictionary, induct[0][destNo1][1], port[0])
        now = time.time()
        print(now - then)

        print("BOT2 -", induct[1][destNo2][1], location[port[1]][4], end=" ")
        dictionary, destNo2 = motion2.move_bot(
            location, destination[1][induct[1][destNo2][1]], destNo2, dictionary, induct[1][destNo2][1], port[1])
        collision(location,dictionary,induct[1][destNo2][1])

        font = cv2.FONT_HERSHEY_SIMPLEX
        if startTime:
            seconds = round (time.time()-startTime,0)
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            seconds = '0' * (2-len(str(seconds))) + str(seconds)
            minutes = '0' * (2-len(str(minutes))) + str(minutes)
            text = f'Time: {minutes}:{seconds}'
            if int(minutes) >= 10:
                text = f'Time: 10:00'
                dictionary = {'bot1': '10100000000', 'bot2': '10100000000'}
        else:
            text = 'Time: 00:00'
        cv2.putText(frame,text, (500, 65), font, 1.0, (0, 0, 0), 3) # add text on frame

        print(dictionary, "\n")

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


def socketFunc1():
    global dictionary, startTime
    port = 1111
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)

    while True:
        client, addr = s.accept()
        if not startTime:
            startTime = time.time()
        client.settimeout(10)
        # print("BOT1 - ", dictionary['bot1'])
        client.send(bytes(dictionary['bot1'], encoding='utf8'))
        client.close()


def socketFunc2():
    global dictionary, startTime
    port = 2222
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)

    while True:
        client, addr = s.accept()
        if not startTime:
            startTime = time.time()
        client.settimeout(10)
        # print("BOT2 - ", dictionary['bot2'])
        client.send(bytes(dictionary['bot2'], encoding='utf8'))
        client.close()


socketThread = threading.Thread(target=socketFunc1)
socketThread.start()

socketThread = threading.Thread(target=socketFunc2)
socketThread.start()

cvThread = threading.Thread(target=cvFunc)
cvThread.start()
