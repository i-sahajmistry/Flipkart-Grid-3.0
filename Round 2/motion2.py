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
    shortestAngle, intHeadingDeg = getAngle(
        location[1], destination[target], laut_jao)
    print(cx," **",cy)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 0.5:
            s = 0
            stop = 0

    # going to PUNE,AHMEDABAD,JAIPUR

    elif destination[-2][0] < 650:
        if(laut_jao == 0):

            if(cy < destination[target][1] and condition < 1):
                target = 0
                dictionary = forward(shortestAngle, dictionary, 2, 0)
                print("forward")

            elif(intHeadingDeg < 75 and condition < 2):
                dictionary = clockwise(dictionary, 2, 0)
                print("right-rotate")
                condition = 1

            else:
                dictionary = pause(dictionary, 2, 1)
                laut_jao = 1
                condition = 2

        # returning from pune, ahmedabad ,jaipur
        else:
            if(intHeadingDeg > 10 and condition < 3):
                print("left-rotate")
                dictionary = anticlockwise(dictionary, 2, 1)
                target = 1
                condition = 2

            elif(cy > 53 and condition < 4):
                target = 1
                condition = 3
                dictionary = backward(shortestAngle, dictionary, 2, 0)
                print("backward")

            else:
                laut_jao = 0
                condition = 0
                target = 0
                dictionary = pause(dictionary, 2, 0)
                stop = 1
                destNo2 = destNo2+1

    #  going to Chennai, Bengaluru , Hyderebad
    elif(destination[-2][0] < 826):
        if(laut_jao == 0):
            if(cy < destination[target][1] and intHeadingDeg < 30 and condition < 1):
                target = 0
                dictionary = forward(shortestAngle, dictionary, 2, 0)
                print("forward", cx, destination[target][0])

            elif(intHeadingDeg > -70 and condition < 2):
                dictionary = anticlockwise(dictionary, 2, 0)
                # print("left-rotate")
                print("LEFT-ROTATE", cx,"---",cy, destination[target][0])
                target = 1
                condition = 1

            elif(cx < destination[target][0]-10 and condition < 3):
                target = 1
                dictionary = forward(shortestAngle, dictionary, 2, 0)
                print("left-move  ",cx, "-- ",destination[target][0]-10 )
                condition = 2

            else:
                dictionary = pause(dictionary, 2, 1)
                laut_jao = 1
                target = 0
                condition = 3

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx > (destination[target][0])  and condition < 4):
                target = 0
                dictionary = backward(shortestAngle, dictionary, 2, 1)
                print("right-move(backward)")
                print("destination is   ",destination[target][0] )


                condition = 3

            elif(intHeadingDeg < -10  and condition < 5):
                dictionary = clockwise(dictionary, 2, 0)
                print("right-rotate")
                target = 2
                condition = 4

            elif(cy >destination[target][1] and condition < 6):
                target = 2
                dictionary = backward(shortestAngle, dictionary, 2, 0)
                print("backward to IS 2")
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
                    print("forward -1")

                elif(intHeadingDeg > -85 and condition < 2):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("left-rotate -1")
                    target = 1
                    condition = 1

                elif(cx < destination[target][0] and condition < 3):
                    target = 1
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("left-move(forward) -1")
                    condition = 2

                elif(intHeadingDeg < -20 and condition < 4 and letter == "D"):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("right-rotate-1")
                    target = 1
                    condition = 3

                elif((intHeadingDeg > -170 and intHeadingDeg < 100)  and condition < 4 and letter == "M"):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("left-rotate -1")
                    target = 1
                    condition = 3

                else:
                    dictionary = pause(dictionary, 2, 1)
                    laut_jao = 1
                    condition = 4

            # returning from mumbai
            else:
                if(intHeadingDeg > -80 and condition < 5 and letter == "D"):
                    print("left-rotate-2")
                    dictionary = anticlockwise(dictionary, 2, 1)
                    target = 0
                    condition = 4

                elif(intHeadingDeg >-85 and condition < 5 and letter == "M"):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("right-rotate-1")
                    target = 0
                    condition = 4

                elif(cx > destination[target][0] and condition < 6):
                    target = 0

                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("left-move(backward)-1")
                    condition = 5

                elif(intHeadingDeg < -20 and  condition < 7):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("right-rotate -3")
                    target = 2
                    condition = 6

                elif(cy > 53 and condition < 8):
                    target = 2
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward-2")
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
                    print("forward -1")

                elif(intHeadingDeg > -85 and condition < 2):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("left-rotate -1")
                    target = 1
                    condition = 1

                elif(cx < destination[target][0] and condition < 3):
                    target = 1
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("left-move(forward) -1")
                    condition = 2

                elif(intHeadingDeg < -20 and condition < 4 and cy>200):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("right-rotate-1")
                    target = 2
                    condition = 3

                elif(cy < destination[target][1] and condition < 5):
                    target = 2
                    dictionary = forward(shortestAngle, dictionary, 2, 0)
                    print("forward-2")
                    condition = 4

                elif(intHeadingDeg <50 and condition < 6):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("right-rotate-2")
                    target = 2
                    condition = 5

                else:
                    dictionary = pause(dictionary, 2, 1)
                    laut_jao = 1
                    condition = 6

            # returning from kolkATA
            else:
                if(intHeadingDeg > 10 and condition < 7 and cy>200):
                    print("left-rotate-2")
                    dictionary = anticlockwise(dictionary, 2, 1)
                    target = 1
                    condition = 6

                elif(cy > destination[target][1] and condition < 8):
                    target = 1
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward-1")
                    condition = 7

                elif(intHeadingDeg > -85 and condition < 9):
                    dictionary = anticlockwise(dictionary, 2, 0)
                    print("left-rotate-3")
                    target = 0
                    condition = 8

                elif(cx > destination[target][0] and condition < 10):
                    target = 0
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("left-move(backward)-1")
                    condition = 9

                elif(intHeadingDeg < 20 and condition < 11):
                    dictionary = clockwise(dictionary, 2, 0)
                    print("right-rotate -3")
                    target = 3
                    condition = 10

                elif(cy > 53 and condition < 12):
                    target = 3
                    dictionary = backward(shortestAngle, dictionary, 2, 0)
                    print("backward-2")
                    condition = 11

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary = pause(dictionary, 2, 0)
                    condition = 0
                

    return dictionary, destNo2
