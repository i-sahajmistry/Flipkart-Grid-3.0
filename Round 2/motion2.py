from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target = 0
condition = 0

def move_bot(location, destination, destNo2, dictionary, letter):
    global stop, then, s, laut_jao, target, condition
    cx, cy = location[1][4]
    shortestAngle, intHeadingDeg = getAngle(location[1], destination[target], laut_jao)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 0.5:
            s = 0
            stop = 0

    # going to PUNE,AHMEDABAD,JAIPUR

    if letter in ['P', 'A', 'J', 'C', 'B', 'H']:
        if(laut_jao == 0):
            if(cy < destination[target][1] and condition < 1):
                dictionary = forward(shortestAngle, dictionary, 2, 0)
                print("forward")
                target = 0

            elif(intHeadingDeg < 50 and condition < 2 and letter in ['P', 'A', 'J']):
                dictionary = clockwise(dictionary, 2, 0)
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -20 and condition < 2 and letter in ['C', 'B', 'H']):
                dictionary = anticlockwise(dictionary, 2, 0)
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx > destination[target][0] and condition < 3 and letter in ['P', 'A', 'J']):
                target = 1
                dictionary = forward(shortestAngle, dictionary, 2, 0)
                print("RIGHT-forward-1")
                condition = 2

            elif(cx < destination[target][0] and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                dictionary = forward(shortestAngle, dictionary, 2, 0)
                print("LEFT-forward-1")
                condition = 2

            else:
                dictionary = pause(dictionary, 2, 1)
                laut_jao = 1
                target = 0
                condition = 3

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx < (destination[target][0])  and condition < 4 and letter in ['P', 'A', 'J']):
                target = 0
                dictionary = backward(shortestAngle, dictionary, 2, 1)
                print("backward-1")
                condition = 3

            elif(cx > (destination[target][0])  and condition < 4 and letter in ['C', 'B', 'H']):
                target = 0
                dictionary = backward(shortestAngle, dictionary, 2, 1)
                print("backward-1")
                condition = 3

            elif(intHeadingDeg > 10  and condition < 5 and letter in ['P', 'A', 'J']):
                dictionary = anticlockwise(dictionary, 2, 0)
                print("anticlockwise")
                target = 2
                condition = 4

            elif(intHeadingDeg < -10  and condition < 5 and letter in ['C', 'B', 'H']):
                dictionary = clockwise(dictionary, 2, 0)
                print("clockwise")
                target = 2
                condition = 4

            elif(cy >destination[target][1] and condition < 6):
                target = 2
                dictionary = backward(shortestAngle, dictionary, 2, 0)
                print("backward")
                condition = 5

            else:
                laut_jao = 0
                stop = 1
                destNo2 = destNo2+1
                target = 0
                dictionary = pause(dictionary, 2, 0)
                condition = 0
   
    else:
        if(destination[-2][1] < 400):
    # code for going to mumbai, delhi
            if(laut_jao == 0):
            
                if(cy < destination[target][1] and condition < 1):
                    target = 0
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("forward")

                elif(intHeadingDeg > -80 and condition < 2):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("anticlockwise")
                    target = 1
                    condition = 1

                elif(cx < destination[target][0] and condition < 3):
                    target = 1
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("forward-1")
                    condition = 2

                elif(intHeadingDeg < -10 and condition < 4 and letter == "D"):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("clockwise-1")
                    target = 1
                    condition = 3

                elif((intHeadingDeg > -170 and intHeadingDeg < 100)  and condition < 4 and letter == "M"):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("anticlockwise-1")
                    target = 1
                    condition = 3

                else:
                    dictionary = pause(dictionary, 2, 1)
                    laut_jao = 1
                    condition = 4

            # returning from mumbai
            else:
                if(intHeadingDeg > -80 and condition < 5 and letter == "D"):
                    print("anticlockwise-1")
                    dictionary = anticlockwise(dictionary, 2, 1)
                    target = 0
                    condition = 4

                elif(intHeadingDeg >-80 and condition < 5 and letter == "M"):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("clockwise-1")
                    target = 0
                    condition = 4

                elif(cx > destination[target][0] and condition < 6):
                    target = 0
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward-1")
                    condition = 5

                elif(intHeadingDeg < -10 and  condition < 7):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("clockwise")
                    target = 2
                    condition = 6

                elif(cy > 53 and condition < 8):
                    target = 2
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward")
                    condition = 7

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary = pause(dictionary, 2, 0)
                    condition = 0

        # going to Kolkata
        else:
            if(laut_jao == 0):

                if(cy < destination[target][1] and condition < 1):
                    target = 0
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("forward")

                elif(intHeadingDeg > -80 and condition < 2):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("anticlockwise")
                    target = 1
                    condition = 1

                elif(cx < destination[target][0] and condition < 3):
                    target = 1
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("forward-1")
                    condition = 2

                elif(intHeadingDeg < -10 and condition < 4 and cy>200):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("clockwise-1")
                    target = 2
                    condition = 3

                elif(cy < destination[target][1] and condition < 5):
                    target = 2
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("forward-2")
                    condition = 4

                elif(intHeadingDeg <80 and condition < 6):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("clockwise-2")
                    target = 2
                    condition = 5

                else:
                    dictionary = pause(dictionary, 2, 1)
                    laut_jao = 1
                    condition = 6

            # returning from kolkATA
            else:
                if(intHeadingDeg > 10 and condition < 7 and cy>200):
                    print("anticlockwise-2")
                    dictionary = anticlockwise(dictionary, 2, 1)
                    target = 1
                    condition = 6

                elif(cy > destination[target][1] and condition < 8):
                    target = 1
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward-2")
                    condition = 7

                elif(intHeadingDeg > -80 and condition < 9):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("anticlockwise-1")
                    target = 0
                    condition = 8

                elif(cx > destination[target][0] and condition < 10):
                    target = 0
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward-1")
                    condition = 9

                elif(intHeadingDeg < 10 and condition < 11):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("clockwise")
                    target = 3
                    condition = 10

                elif(cy > 53 and condition < 12):
                    target = 3
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward")
                    condition = 11

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary = pause(dictionary, 2, 0)
                    condition = 0
                

    return dictionary, destNo2
