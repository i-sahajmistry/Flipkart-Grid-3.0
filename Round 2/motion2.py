from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target = 0
condition = 0

goupto = {'P': 130, 'A':300 ,'J':487, 'C':130, 'B':300, 'H':487 }

def move_bot(location, destination, destNo2, dictionary, letter, port):
    global stop, then, s, laut_jao, target, condition
    cx, cy = location[port][4]
    shortestAngle, intHeadingDeg = getAngle(location[port], destination[target], laut_jao)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 0.5:
            s = 0
            stop = 0


    if letter in ['P', 'A', 'J', 'C', 'B', 'H']:
        if(laut_jao == 0):
            if(cy < goupto[letter] and condition < 1):
                h1 = str(max(0, min(180, 110 - int(shortestAngle * 4))))
                h2 = str(max(0, min(180, 90 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward")
                target = 0

            elif(intHeadingDeg < 70 and condition < 2 and letter in ['P', 'A', 'J']):
                dictionary['bot2'] = f'10011201200'
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -70 and condition < 2 and letter in ['C', 'B', 'H']):
                dictionary['bot2'] = f'01101201200'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx > destination[target][0] and condition < 3 and letter in ['P', 'A', 'J']):
                target = 1
                h1 = str(max(0, min(180, 80 + int((intHeadingDeg - 90) * 2.5))))
                h2 = str(max(0, min(180, 80 - int((intHeadingDeg - 90) * 2.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("RIGHT-forward-1")
                condition = 2

            elif(cx < destination[target][0] and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                h1 = str(max(0, min(180, 80 - int((intHeadingDeg + 90) * 2.5))))
                h2 = str(max(0, min(180, 80 + int((intHeadingDeg + 90) * 2.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("LEFT-forward-1")
                condition = 2

            else:
                dictionary = pause(dictionary, 2, 1)
                laut_jao = 1
                target = 0
                condition = 3

        else:
            if(cx > 688  and condition < 4 and letter == 'CBH'):
                target = 0
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                dictionary['bot2'] = f'01010700701'
                print("backward-1")
                condition = 3

            elif(cx < 670  and condition < 4 and letter in 'P'):
                target = 0
                dictionary['bot2'] = f'01010700701'
                print("backward-1")
                condition = 3

            elif(cx < 673  and condition < 4 and letter in 'A'):
                target = 0
                dictionary['bot2'] = f'01010700701'
                print("backward-1")
                condition = 3

            elif(cx < 673  and condition < 4 and letter == 'J'):
                target = 0
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(180, 70 - int(shortestAngle * 0))))
                h1 = str(max(0, min(180, 70 + int(shortestAngle * 0))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'0101{h2}{h1}1'
                print("backward-1")
                condition = 3

            elif(intHeadingDeg < -30  and condition < 5):
                dictionary['bot2'] = f'10011201200'
                print("clockwise", intHeadingDeg)
                target = 2
                condition = 4

            elif(intHeadingDeg > 30  and condition < 5):
                dictionary['bot2'] = f'01101101100'
                print("anticlockwise", intHeadingDeg)
                target = 2
                condition = 4

            elif(cy > 50 and condition < 6):
                target = 2
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(180, 100 - int(shortestAngle * 3.5))))
                h1 = str(max(0, min(150, 70 + int(shortestAngle * 3.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'0101{h2}{h1}0'
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
            
                if(cy < 135 and condition < 1):
                    target = 0
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward")

                # elif(intHeadingDeg > -80 and condition < 2):
                #     dictionary['bot2'] = f'01101201200'
                #     print("anticlockwise")
                #     target = 1
                #     condition = 1

                elif(cx < 920 and condition < 2):
                    target = 1
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward-1")
                    condition = 1

                elif(intHeadingDeg < -60 and condition < 3 and letter == "D"):
                    dictionary['bot2'] = f'10011201200'
                    print("clockwise-1")
                    target = 1
                    condition = 2

                elif((intHeadingDeg > -160 and intHeadingDeg < 100)  and condition < 3 and letter == "M"):
                    dictionary['bot2'] = f'01101201200'
                    print("anticlockwise-1")
                    target = 1
                    condition = 2

                elif(cy > 255 and condition < 4 and letter == 'M'):
                    if intHeadingDeg < 0:
                        intHeadingDeg += 180
                    else:
                        intHeadingDeg -= 180
                    h1 = str(max(0, min(180, 80 + int(intHeadingDeg * 3))))
                    h2 = str(max(0, min(180, 70 - int(intHeadingDeg * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    condition = 3

                elif(cy < 272 and condition < 4 and letter == 'D'):
                    h1 = str(max(0, min(180, 80 + int(intHeadingDeg * 3))))
                    h2 = str(max(0, min(180, 70 - int(intHeadingDeg * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    condition = 3

                else:
                    dictionary = pause(dictionary, 2, 1)
                    laut_jao = 1
                    condition = 3

            # returning from mumbai
            else:
                # if cy > 265 and condition < 4:
                #     dictionary['bot2'] = f'01010800801'
                #     condition = 3

                if(intHeadingDeg > -40 and condition < 5 and letter == "D"):
                    print("anticlockwise-1")
                    dictionary['bot2'] = f'01101101100'
                    target = 0
                    condition = 4

                elif(intHeadingDeg >-100 and condition < 5 and letter == "M"):
                    dictionary['bot2'] = f'10011101100'
                    print("clockwise-1")
                    target = 0
                    condition = 4

                elif(cx > 785 and condition < 6):
                    target = 0
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    print(shortestAngle)
                    h2 = str(max(0, min(160, 90 - int(shortestAngle * 2.5))))
                    h1 = str(max(0, min(160, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward-1")
                    condition = 5

                # elif(intHeadingDeg < -10 and  condition < 7):
                #     dictionary['bot2'] = f'10011201200'
                #     print("clockwise")
                #     target = 2
                #     condition = 6

                elif(cy > 50 and condition < 8):
                    target = 2
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    print(shortestAngle)
                    h2 = str(max(0, min(180, 70 - int(shortestAngle * 3))))
                    h1 = str(max(0, min(180, 95 + int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
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

                if(cy < 135 and condition < 1):
                    target = 0
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward")

                elif(cx < 885 and condition < 2):
                    target = 1
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward-1")
                    condition = 1

                elif(cy < 470 and condition < 4):
                    target = 2
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print('forward-2')
                    condition = 3

                elif(intHeadingDeg <80 and condition < 6):
                    dictionary['bot2'] = f'10011001000'
                    print("clockwise-2")
                    target = 2
                    condition = 5

                else:
                    dictionary = pause(dictionary, 2, 1)
                    laut_jao = 1
                    condition = 6

            # returning from kolkATA
            else:
                if(intHeadingDeg > 30 and condition < 7 and cy>200):
                    print("anticlockwise-2")
                    dictionary['bot2'] = f'01101001001'
                    target = 1
                    condition = 6

                elif(cy > 370 and condition < 8):
                    target = 1
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h2 = str(max(0, min(200, 70 - int(shortestAngle * 2.5))))
                    h1 = str(max(0, min(200, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward-2")
                    condition = 7

                elif(cx > 785 and condition < 9):
                    target = 0
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    print(shortestAngle)
                    h2 = str(max(0, min(160, 90 - int(shortestAngle * 2.5))))
                    h1 = str(max(0, min(160, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward-1")
                    condition = 8

                # elif(intHeadingDeg < -10 and  condition < 7):
                #     dictionary['bot2'] = f'10011201200'
                #     print("clockwise")
                #     target = 2
                #     condition = 6

                elif(cy > 50 and condition < 10):
                    target = 3
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    print(shortestAngle)
                    h2 = str(max(0, min(180, 70 - int(shortestAngle * 3))))
                    h1 = str(max(0, min(180, 95 + int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward")
                    condition = 9

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary = pause(dictionary, 2, 0)
                    condition = 0
                

    return dictionary, destNo2
