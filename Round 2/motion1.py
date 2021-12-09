from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target=0
condition=0

def move_bot(location, destination, destNo, dictionary):
    global stop, then, s, laut_jao,  target, condition
    cx, cy = location[0][4]
    shortestAngle, intHeadingDeg = getAngle(location[0], destination[target], laut_jao)
    print(target, "****", shortestAngle, "****", intHeadingDeg , "****", laut_jao)
    # print("destination", destination)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 1:
            s = 0
            stop = 0
    # Mumbai Delhi Kolkata code

    print("\n","\n")
    if destination[-2][0] > 826:
        if(laut_jao == 0):
            if(cy < destination[target][1] and condition<1):
                target=0
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward")

            elif(intHeadingDeg > -85 and condition < 2):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("left-rotate")
                condition=1

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                condition=2


        else:
            #returning from mumbai, Delhi Kolkata
            if(intHeadingDeg < -30 and condition < 3):
                print("right-rotate")
                dictionary = clockwise(dictionary, 1, 1)
                target=1
                condition=2

            elif(cy > 63 and condition < 4):
                target=1
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward")
                condition=3

            else:
                laut_jao = 0
                stop = 1
                target=0
                destNo = destNo+1
                dictionary = pause(dictionary, 1, 0)
                condition=4
    
    #  Chennai, Bengaluru , Hyderebad
    elif(destination[-2][0] > 650):
        if(laut_jao == 0):
            if(cy < destination[target][1] and intHeadingDeg < 30  and condition < 1):
                target=0
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward", cx, destination[target][0])

            elif(intHeadingDeg < 30  and condition < 2):
                dictionary = clockwise(dictionary, 1, 0)
                print("right-rotate")
                target=1
                condition=1

            elif(cx > destination[target][0] and condition < 3):
                target =1
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("right-move")
                condition=2

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                target=0
                condition=3

        # returning from Chennai Bengaluru , Hyderebad
        else:

            if(cx < 833 and condition < 4):
                target=0
                dictionary = backward(shortestAngle, dictionary, 1, 1)
                print("left-move(backward)")
                condition=3

            elif(intHeadingDeg > 30 and condition < 5):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("left-rotate")
                target=2
                condition=4

            elif(cy > 63 and condition < 6):
                target=2
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward to IS 1")
                condition=5

            else:
                laut_jao = 0
                stop = 1
                destNo = destNo+1
                target=0
                condition=0
                dictionary = pause(dictionary, 1, 0)
    

    # code for going to Pune, Ahemdabad , Jaipur
    else:
        if(laut_jao ==0):

            if(cy< destination[target][1] and condition < 1):
                target=0
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward -1")
                
            elif(intHeadingDeg<30 and condition < 2):
                dictionary = clockwise(dictionary, 1, 0)
                print("right-rotate -1")
                target=1
                condition=1

            elif(cx> destination[target][0] and condition < 3):
                target=1
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("right-move(forward) -1")
                condition=2

            elif(intHeadingDeg >30 and condition < 4):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("left-rotate-1")
                target=2
                condition=3

            elif(cy<destination[target][1] and condition < 5):
                target=2
                dictionary = forward(shortestAngle, dictionary, 1, 0)
                print("forward-2")
                condition=4
            
            elif(intHeadingDeg>-85 and condition < 6):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("left-rotate-2")
                target=2
                condition=5

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                condition=6

        # returning from pune, ahmedabad , and jaipur
        else:
            if(intHeadingDeg < -30 and condition < 7):
                print("right-rotate-2")
                dictionary = clockwise(dictionary, 1, 1)
                target=1
                condition=6

            elif(cy>destination[target][1] and condition < 8):
                target=1
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward-1")
                condition=7

            elif(intHeadingDeg <30 and condition < 9):
                dictionary = clockwise(dictionary, 1, 0)
                print("right-rotate-3")
                target=0
                condition=8

            elif(cx<destination[target][0] and condition < 10):
                target=0
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("left-move(backward)-1")
                condition=9

            elif(intHeadingDeg >30 and condition < 11):
                dictionary = anticlockwise(dictionary, 1, 0)
                print("left-rotate -3")
                target=3
                condition=10

            elif(cy > 63 and condition < 12):
                target=3
                dictionary = backward(shortestAngle, dictionary, 1, 0)
                print("backward-2")
                condition=11

            else:
                laut_jao = 0
                stop = 1
                target=0
                destNo = destNo+1
                dictionary = pause(dictionary, 1, 0)
                condition=0
    
    return dictionary, destNo