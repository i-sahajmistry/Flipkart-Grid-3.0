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
    destination = [{
        # 'M':[[828,149], [833, 160], [841,40]],
        'M':[[862,144], [865, 155], [875,32]],
        
                    # 'D':[[827,311], [833, 330], [841,40]],
                    'D':[[862,322], [868, 333], [875,37]],
                    # 'K':[[829,477], [843, 500], [841,40]],
                    'K':[[862,495], [879, 506], [875,38]],
                    # 'C':[[828,149], [820, 190], [841,40]],
                    'C':[[862,144], [842, 155], [875,38]],
                    # 'B':[[827,311], [820, 360], [841,40]],
                    'B':[[862,322], [846, 333], [875,38]],
                    # 'H':[[829,477], [800, 530], [841,40]],
                    'H':[[862,495], [853, 506], [875,38]],
                    # 'P':[[834, 95], [504, 110], [508, 174], [841,40]],
                    'P':[[874, 91], [524, 98], [525, 507], [875,38]],
                    # 'A':[[834, 95], [504, 110], [508, 337], [841,40]],
                    'A':[[874, 91], [524, 98], [525, 334], [875,38]],
                    # 'J':[[834, 95], [504, 110], [508, 512], [841,40]]},
                    'J':[[874, 91], [524, 98], [525, 163], [875,38]]},
                    
                   {
                    #    'P':[[656,152], [632,151], [659,34]],
                       'P':[[669,158], [666,163], [659,34]],
                    # 'A':[[659,312], [633,323], [659,34]],
                    'A':[[670,326], [666,337], [659,34]],
                    # 'J':[[661,486], [633,489], [659,34]],
                    'J':[[672,505], [666,4516], [659,34]],
                    # 'C':[[656,152], [679,170], [659,34]],
                    'C':[[669,153], [699,162], [659,34]],
                    # 'B':[[659,312], [676,342], [659,34]],
                    'B':[[669,321], [698,334], [659,34]],
                    # 'H':[[661,486], [680,509], [659,34]],
                    'H':[[669,500], [703,510], [659,34]],
                    # 'M':[[682,262], [853,264], [659,34]],
                    'M':[[702,252], [915,245], [659,34]],
                    # 'D':[[683,274], [870,294], [659,34]],
                    'D':[[702,252], [919,282], [659,34]],
                    # 'K':[[682,262], [979,294], [980,494], [659,34]]}]
                    'K':[[702,252], [1014,283], [1029,499], [659,34]]}]

    vid = cv2.VideoCapture(0)
    vid.set(3, 1420)
    vid.set(4, 800)

    while True:
        _, frame = vid.read()

        location = detectMarker(
            frame, location, markerSize=4, totalMarker=50, draw=True)

        corners = [location[i][4] for i in range(4, 8)]
        frame = warp(frame, corners)
        # print("BOT1 -", induct[0][destNo1][1], location[0][4], end=" ")
        dictionary, destNo1 = motion1.move_bot(
            location, destination[0][induct[0][destNo1][1]], destNo1, dictionary, induct[0][destNo1][1])

        print("BOT2 -", induct[1][destNo2][1], location[1][4], end=" ")
        dictionary, destNo2 = motion2.move_bot(
            location, destination[1][induct[1][destNo2][1]], destNo2, dictionary, induct[1][destNo2][1])
        print(dictionary)
        collision(location,dictionary,induct[1][destNo2][1])

        # print(dictionary, "\n")

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
    port = 2222
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
# main coordinates 833,199 first move , second turn 639,199,
