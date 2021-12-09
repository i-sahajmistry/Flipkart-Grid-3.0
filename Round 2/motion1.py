from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target=0
condition=0

def move_bot(location, destination, destNo, dictionary, letter):
    global stop, then, s, laut_jao,  target, condition
    cx, cy = location[0][4]
    shortestAngle, intHeadingDeg = getAngle(location[0], destination[target], laut_jao)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 1:
            s = 0
            stop = 0
    # Mumbai Delhi Kolkata code

    if letter in ['M', 'D', 'K', 'C', 'B', 'H']:
        if(laut_jao == 0):
            if(cy < destination[target][1] and condition < 1):
                target = 0
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward")

            elif(intHeadingDeg < 80 and condition < 2 and letter in ['C', 'B', 'H']):
                dictionary = clockwise(dictionary, 1, 0)
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -80 and condition < 2 and letter in ['M', 'D', 'K']):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx < destination[target][0] and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward-1")
                condition = 2

            elif(cx < destination[target][0] and condition < 3 and letter in ['M', 'D', 'K']):
                target = 1
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward-1")
                condition = 2

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                target = 0
                condition = 3

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx > (destination[target][0])  and condition < 4 and letter in ['C', 'B', 'H']):
                target = 0
                dictionary = backward(shortestAngle, dictionary, 1, 1)
                print("backward-1")
                condition = 3

            elif(cx < (destination[target][0])  and condition < 4 and letter in ['M', 'D', 'K']):
                target = 0
                dictionary = backward(shortestAngle, dictionary, 1, 1)
                print("backward-1")
                condition = 3

            elif(intHeadingDeg > 10  and condition < 5 and letter in ['C', 'B', 'H']):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("anticlockwise")
                target = 2
                condition = 4

            elif(intHeadingDeg < -10  and condition < 5 and letter in ['M', 'D', 'K']):
                dictionary = clockwise(dictionary, 1, 0)
                print("clockwise")
                target = 2
                condition = 4

            elif(cy >destination[target][1] and condition < 6):
                target = 2
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward to IS 1")
                condition = 5

            else:
                laut_jao = 0
                stop = 1
                destNo = destNo+1
                target = 0
                dictionary = pause(dictionary, 1, 0)
                condition = 0
    

    # code for going to Pune, Ahemdabad , Jaipur
    else:
        if(laut_jao ==0):

            if(cy< destination[target][1] and condition < 1):
                target=0
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward")
                
            elif(intHeadingDeg<80 and condition < 2):
                dictionary = clockwise(dictionary, 1, 0)
                print("clockwise")
                target=1
                condition=1

            elif(cx> destination[target][0] and condition < 3):
                target=1
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward-1")
                condition=2

            elif(intHeadingDeg >10 and condition < 4):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("anticlockwise-1")
                target=2
                condition=3

            elif(cy<destination[target][1] and condition < 5):
                target=2
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward-2")
                condition=4
            
            elif(intHeadingDeg>-80 and condition < 6):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("anticlockwise-2")
                target=2
                condition=5

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                condition=6

        # returning from pune, ahmedabad , and jaipur
        else:
            if(intHeadingDeg < -10 and condition < 7):
                print("clockwise-2")
                dictionary = clockwise(dictionary, 1, 1)
                target=1
                condition=6

            elif(cy>destination[target][1] and condition < 8):
                target=1
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward-2")
                condition=7

            elif(intHeadingDeg <80 and condition < 9):
                dictionary = clockwise(dictionary, 1, 0)
                print("clockwise-1")
                target=0
                condition=8

            elif(cx<destination[target][0] and condition < 10):
                target=0
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward-1")
                condition=9

            elif(intHeadingDeg >10 and condition < 11):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("anticlockwise")
                target=3
                condition=10

            elif(cy > 63 and condition < 12):
                target=3
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward")
                condition=11

            else:
                laut_jao = 0
                stop = 1
                target=0
                destNo = destNo+1
                dictionary = pause(dictionary, 1, 0)
                condition=0
    
    return dictionary, destNo