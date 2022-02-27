import cv2
import socket
import threading
from utils import *
import motion0
import motion1
import motion2
import motion3
import time

dictionary = {'bot0': '10100000000', 'bot1': '10100000000', 'bot2': '10100000000', 'bot3': '10100000000'}
startTime = 0

def cvFunc():
    global dictionary, startTime
    induct = read_data()
    destNo1 = 0
    destNo2 = 0
    ids = [0, 3, 1, 2]
    port = [ids[0],ids[1]]
    newBotEntry = [0, 0]


    location = {i: [[0, 0] for j in range(5)] for i in range(0, 8)}
    destination = [{
                    'M':[[1080,220], [1060, 241], [1080,35]],
                    'D':[[1050,438], [1060, 462], [1080,35]],
                    'K':[[1050,669], [1060, 695], [1080,35]],
                    'C':[[1080,220], [1045, 247], [1080,35]],
                    'B':[[1050,438], [1045, 478], [1080,35]],
                    'H':[[1050,669], [1049, 702], [1080,35]],
                    'P':[[1079,124], [737,133], [1080,35]],
                    'A':[[1079,124], [614,140], [620,517], [1080,35]],
                    'J':[[1079,124], [614,140], [600,742], [1080,35]]},
                    
                   {
                    'P':[[850,290], [824,240], [810,0]],
                    'A':[[850,430], [825,453], [800,0]],
                    'J':[[850,705], [820,684], [800,0]],
                    'C':[[830,290], [849,228], [800,0]],
                    'B':[[830,430], [847,452], [800,0]],
                    'H':[[850,705], [845,685], [800,0]],
                    'M':[[850,338], [1150,330], [800,0]],
                    'D':[[850,338], [1150,330], [800,0]],
                    'K':[[850,338], [1294,322], [1300,727], [800,0]]}]

    vid = cv2.VideoCapture(2)
    vid.set(3, 1420)
    vid.set(4, 1420) 

    while True:
        
        _, frame = vid.read()
        
        

        location = detectMarker(
            frame, location, markerSize=4, totalMarker=50, draw=True)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,induct[0][destNo1][2],(location[0][4][0], location[0][4][1]), font, 0.7, (0,0,0),3 )
        cv2.putText(frame,induct[1][destNo2][2],(location[1][4][0], location[1][4][1]), font, 0.7, (0,0,0),3 )
        corners = [location[i][4] for i in range(4, 8)]
        frame = warp(frame, corners)
        print(f"BOT{port[0]} -", induct[0][destNo1][1], location[port[0]][4], end=" ")
        
        if 10<location[port[0]][4][0]<500:
            newBotEntry[0] = 1
            if(port[0]==ids[2] and port[1]!=ids[3]):
                port[0]=ids[3]
            else:
                port[0]=ids[2]

        if port[0] == 0 or port[0] == 2:
            dictionary, destNo1, newBotEntry[0] = motion0.move_bot(
                location, destination[0][induct[0][destNo1][1]], destNo1, dictionary, induct[0][destNo1][1], port[0], ids, destination, newBotEntry[0])
        else:
            dictionary, destNo1, newBotEntry[0] = motion1.move_bot(
                location, destination[0][induct[0][destNo1][1]], destNo1, dictionary, induct[0][destNo1][1], port[0], ids, destination, newBotEntry[0])

        # collision(location,dictionary,[induct[1][destNo1][1], induct[0][destNo2][1]], port)

        print(f"BOT{port[1]} -", induct[1][destNo2][1], location[port[1]][4], end=" ")

        if 10<location[port[1]][4][0]<500:
            newBotEntry[1] = 1
            if(port[1]==ids[3] and port[0]!=ids[2]):
                port[1]=ids[2]
            else:
                port[1]=ids[3]

        if port[1] == 3 or port[1] == 1:
            dictionary, destNo2, newBotEntry[1] = motion3.move_bot(
                location, destination[1][induct[1][destNo2][1]], destNo2, dictionary, induct[1][destNo2][1], port[1],ids,destination, newBotEntry[1])
        else:
            dictionary, destNo2, newBotEntry[1] = motion2.move_bot(
                location, destination[1][induct[1][destNo2][1]], destNo2, dictionary, induct[1][destNo2][1], port[1],ids,destination, newBotEntry[1])

        collision(location,dictionary,[induct[0][destNo1][1], induct[1][destNo2][1]], port)

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
        print("Total No. of Parcels Delivered: ", destNo1 + destNo2)
        cv2.putText(frame,text, (500, 65), font, 1.0, (0, 0, 0), 3) # add text on frame
        print(dictionary, "\n")

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


def socketFunc1():
    global dictionary, startTime
    port = 4444
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
    port = 1111
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

def socketFunc3():
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
        # print("BOT1 - ", dictionary['bot1'])
        client.send(bytes(dictionary['bot2'], encoding='utf8'))
        client.close()


def socketFunc4():
    global dictionary, startTime
    port = 3333
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(0)

    while True:
        client, addr = s.accept()
        if not startTime:
            startTime = time.time()
        client.settimeout(10)
        # print("BOT2 - ", dictionary['bot2'])
        client.send(bytes(dictionary['bot3'], encoding='utf8'))
        client.close()


socketThread = threading.Thread(target=socketFunc1)
socketThread.start()

socketThread = threading.Thread(target=socketFunc2)
socketThread.start()

socketThread = threading.Thread(target=socketFunc3)
socketThread.start()

socketThread = threading.Thread(target=socketFunc4)
socketThread.start()

cvThread = threading.Thread(target=cvFunc)
cvThread.start()
