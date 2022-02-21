import cv2
import socket
import threading
from utils import *
import motion1
import motion2
import time

dictionary = {'bot0': '10100000000', 'bot1': '10100000000', 'bot2': '10100000000', 'bot3': '10100000000'}
startTime = 0

def cvFunc():
    global dictionary, startTime
    induct = read_data()
    destNo1 = 0
    destNo2 = 0
    port = [0,1]
    newBotEntry = 0

    location = {i: [[0, 0] for j in range(5)] for i in range(0, 8)}
    # print(location[0][4][0])
    # print(induct[1][0][2])
    destination = [{
                    'M':[[855,144], [870, 167], [870,20]],
                    'D':[[855,322], [865, 343], [855,20]],
                    'K':[[855,495], [868, 516], [855,20]],
                    'C':[[855,144], [845, 155], [865,20]],
                    'B':[[855,322], [848, 333], [865,20]],
                    'H':[[855,495], [853, 506], [865,20]],
                    'P':[[855, 71], [635, 90], [880,25]],
                    'A':[[855, 71], [495, 100], [495, 325], [880,25]],
                    'J':[[855, 71], [495, 100], [495, 507], [880,25]]},
                    
                   {
                    'P':[[840,178], [824,249], [807,36]],
                    'A':[[830,385], [825,453], [807,36]],
                    'J':[[832,605], [820,684], [807,36]],
                    'C':[[833,178], [849,228], [807,36]],
                    'B':[[830,385], [847,452], [807,36]],
                    'H':[[832,605], [845,685], [807,36]],
                    'M':[[832,270], [1127,334], [807,36]],
                    'D':[[832,270], [1128,353], [807,36]],
                    'K':[[832,270], [1199,344], [1279,647], [807,36]]}]

    vid = cv2.VideoCapture(2)
    vid.set(3, 1420)
    vid.set(4, 1420)

    while True:
        _, frame = vid.read()

        location = detectMarker(
            frame, location, markerSize=4, totalMarker=50, draw=True)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,induct[0][destNo1][2],(location[0][4][0], location[0][4][1]), font, 1.0, (0,0,0),3 )
        cv2.putText(frame,induct[1][destNo2][2],(location[1][4][0], location[1][4][1]), font, 0.8, (0,0,0),3 )
        corners = [location[i][4] for i in range(4, 8)]
        frame = warp(frame, corners)
        print("BOT1 -", induct[0][destNo1][1], location[port[0]][4], end=" ")
        if 10<location[port[0]][4][0]<600:
            newBotEntry = 1
            if(port[0]==1 and port[1]!=3):
                port[0]=3
            else:
                port[0]=1

        dictionary, destNo1 = motion1.move_bot(
        location, destination[0][induct[0][destNo1][1]], destNo1, dictionary, induct[0][destNo1][1], port[0], destination, newBotEntry)

        if 10<location[port[1]][4][0]<600:
            newBotEntry = 1
            if(port[1]==3 and port[0]!=2):
                port[1]=2
            else:
                port[1]=3

        print("BOT2 -", induct[1][destNo2][1], location[port[1]][4], end=" ")
        dictionary, destNo2 = motion2.move_bot(
            location, destination[1][induct[1][destNo2][1]], destNo2, dictionary, induct[1][destNo2][1], port[1], destination, newBotEntry)
        collision(location,dictionary,induct[1][destNo2][1])

        if startTime:
            seconds = round (time.time()-startTime,0)
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            seconds = '0' * (2-len(str(seconds))) + str(seconds)
            minutes = '0' * (2-len(str(minutes))) + str(minutes)
            text = f'Time: {minutes}:{seconds}'
            if int(minutes) >= 10:
                text = f'Time: 10:00'
                dictionary = {'bot0': '10100000000', 'bot1': '10100000000', 'bot2': '10100000000', 'bot3': '10100000000'}
        else:
            text = 'Time: 00:00'
        cv2.putText(frame,text, (500, 65), font, 1.0, (0, 0, 0), 3) # add text on frame
        # cv2.putText(frame,text, (600, 165), font, 1.0, (0, 0, 0), 3) # add text on frame
        # loc1 = (location[1][4][0], location[1][4][1])
        # print(loc1)
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
        client.send(bytes(dictionary['bot0'], encoding='utf8'))
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
        client.send(bytes(dictionary['bot1'], encoding='utf8'))
        client.close()


socketThread = threading.Thread(target=socketFunc1)
socketThread.start()

socketThread = threading.Thread(target=socketFunc2)
socketThread.start()

cvThread = threading.Thread(target=cvFunc)
cvThread.start()
