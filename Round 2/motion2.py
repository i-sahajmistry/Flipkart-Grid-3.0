from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target = 0
condition = 0
sec = 0
wall = 0
checkStop = []
servo = 0
servoTime = 0
w, wx, wy = 0, 0, 0

goupto = {'P': 155, 'A':390 ,'J':613, 'C':130, 'B':300, 'H':477 }

def move_bot(location, destination, destNo2, dictionary, letter, port, allDestinations, newBotEntry):
    global stop, then, s, laut_jao, target, condition, sec, wall, checkStop, servo, servoTime, w, wx, wy, t
    position = location[port][4]
    cx, cy = position
    shortestAngle, intHeadingDeg = getAngle(location[port], destination[target], laut_jao)


    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 0.5:
            s = 0
            stop = 0


    elif letter in ['P', 'A', 'J', 'C', 'B', 'H']:
        if(laut_jao == 0):
            if(cy < goupto[letter] and condition < 1):
                h1, h2 = getSpeeds(target, destination, position)
                if cy < 100:
                    h1 = str(max(0, min(180, h1 - int(shortestAngle * 2))))
                    h2 = str(max(0, min(180, h2 + int(shortestAngle * 2))))
                elif letter == 'J':    
                    h1 = str(max(0, min(180, h1 - int(shortestAngle * 6))))
                    h2 = str(max(0, min(180, h2 + int(shortestAngle * 6))))
                else:
                    h1 = str(max(0, min(180, h1 - int(shortestAngle * 4))))
                    h2 = str(max(0, min(180, h2 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                print("forward")
                target = 0

            elif(intHeadingDeg < 60 and condition < 2 and letter in ['P', 'A', 'J']):
                dictionary[f'bot{port}'] = f'1001100100{servo}'
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -60 and condition < 2 and letter == 'H'):
                dictionary[f'bot{port}'] = f'0110090090{servo}'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -70 and condition < 2 and letter in ['C', 'B']):
                dictionary[f'bot{port}'] = f'0110110110{servo}'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx > destination[target][0] and condition < 3 and letter in ['P', 'A', 'J']):
                target = 1
                h1 = str(max(0, min(180, 90 + int((intHeadingDeg - 90) * 2.5))))
                h2 = str(max(0, min(180, 90 - int((intHeadingDeg - 90) * 2.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                print("RIGHT-forward-1")
                condition = 2

            elif(cx < destination[target][0] and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                h1 = str(max(0, min(180, 80 - int((intHeadingDeg + 90) * 2.5))))
                h2 = str(max(0, min(180, 100 + int((intHeadingDeg + 90) * 2.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                print("LEFT-forward-1")
                condition = 2

            else:
                dictionary = pause(dictionary, 2, 1)
                servo = 1
                servoTime = time.time()
                laut_jao = 1
                target = 0
                condition = 3

        else:
            if(cx > 690  and condition < 4 and letter in 'CBH'):
                target = 0
                dictionary[f'bot{port}'] = f'0101070070{servo}'
                print("backward-1")
                condition = 3

            elif(cx < 673  and condition < 4 and letter == 'PAJ'):
                target = 0
                dictionary[f'bot{port}'] = f'0101070070{servo}'
                print("backward-1")
                condition = 3

            # elif(cx < 673  and condition < 4 and letter in 'AJ'):
            #     target = 0
            #     if(shortestAngle < 0):
            #         shortestAngle += 180
            #     else:
            #         shortestAngle -= 180
            #     h2 = str(max(0, min(180, 70 - int(shortestAngle * 0))))
            #     h1 = str(max(0, min(180, 70 + int(shortestAngle * 0))))
            #     h1 = '0'*(3-len(h1)) + h1
            #     h2 = '0'*(3-len(h2)) + h2
            #     dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
            #     print("backward-1")
            #     condition = 3

            elif(intHeadingDeg < -40  and condition < 5):
                dictionary[f'bot{port}'] = f'1001090090{servo}'
                print("clockwise", intHeadingDeg)
                target = 2
                condition = 4

            elif(intHeadingDeg > 40  and condition < 5):
                dictionary[f'bot{port}'] = f'0110090090{servo}'
                print("anticlockwise", intHeadingDeg)
                target = 2
                condition = 4

            elif(cy > goupto['P'] + 60 and condition < 6 and letter in ['A', 'J', 'B', 'H']):
                target = 2
                shortestAngle, intHeadingDeg = getAngle(location[port], (795,178), laut_jao)
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                print(shortestAngle, "👀👀👀👀")
                h1, h2 = getSpeeds(target, destination, position)
                h1 = str(max(0, min(180, h1 + int(shortestAngle * 0))))
                h2 = str(max(0, min(180, h2 - int(shortestAngle * 0))))
                
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                print("backward to IS 2")
                condition = 5

            elif(cy > 45 and condition < 6):
                target = 2
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1, h2 = getSpeeds(target, destination, position)
                h1 = str(max(0, min(150, h1 + int(shortestAngle * 0))))
                h2 = str(max(0, min(180, h2 - int(shortestAngle * 0))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                print("backward")
                condition = 5

            else:
                laut_jao = 0
                stop = 1
                destNo2 = destNo2+1
                target = 0
                dictionary = pause(dictionary, 2, servo)
                condition = 0
   
    else:
        if(destination[-2][1] < 400):
    # code for going to mumbai, delhi   
            if(laut_jao == 0):
            
                if(cy < 155 and condition < 1):
                    target = 0
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward")

                # elif(intHeadingDeg > -80 and condition < 2):
                #     dictionary[f'bot{port}'] = f'01101201200'
                #     print("anticlockwise")
                #     target = 1
                #     condition = 1

                elif(cx < 900 and condition < 2):
                    target = 1
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward-1")
                    condition = 1

                elif(intHeadingDeg < -60 and condition < 3 and letter == "D"):
                    dictionary[f'bot{port}'] = f'1001110110{servo}'
                    print("clockwise-1")
                    target = 1
                    condition = 2

                elif((intHeadingDeg > -160 and intHeadingDeg < 100)  and condition < 3 and letter == "M"):
                    dictionary[f'bot{port}'] = f'0110110110{servo}'
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
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    condition = 3

                elif(cy < 272 and condition < 4 and letter == 'D'):
                    h1 = str(max(0, min(180, 80 + int(intHeadingDeg * 3))))
                    h2 = str(max(0, min(180, 70 - int(intHeadingDeg * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    condition = 3

                else:
                    servo = 1
                    servoTime = time.time()
                    dictionary = pause(dictionary, 2, servo)
                    laut_jao = 1
                    condition = 3

            # returning from mumbai
            else:
                if cy < 255 and condition < 4 and letter == 'M':
                    dictionary[f'bot{port}'] = f'01010800801'
                    condition = 3

                elif(intHeadingDeg > -40 and condition < 5 and letter == "D"):
                    print("anticlockwise-1")
                    dictionary[f'bot{port}'] = f'0110110110{servo}'
                    target = 0
                    condition = 4

                elif(intHeadingDeg >-100 and condition < 5 and letter == "M"):
                    dictionary[f'bot{port}'] = f'1001110110{servo}'
                    print("clockwise-1")
                    target = 0
                    condition = 4

                elif(cx > 770 and condition < 6):
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
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward-1")
                    condition = 5

                # elif(intHeadingDeg < -10 and  condition < 7):
                #     dictionary[f'bot{port}'] = f'10011201200'
                #     print("clockwise")
                #     target = 2
                #     condition = 6

                elif(cy > 45 and condition < 8):
                    target = 2
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    print(shortestAngle)
                    h2 = str(max(0, min(180, 70 - int(shortestAngle * 3.5))))
                    h1 = str(max(0, min(180, 95 + int(shortestAngle * 3.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
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

                if(cy < 155 and condition < 1):
                    target = 0
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward")

                elif(cx < 885 and condition < 2):
                    target = 1
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward-1")
                    condition = 1

                elif(cy < 475 and condition < 4):
                    target = 2
                    h1 = str(max(0, min(180, 80 - int(shortestAngle * 2.5))))
                    h2 = str(max(0, min(180, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print('forward-2')
                    condition = 3

                elif(intHeadingDeg <65 and condition < 6):
                    dictionary[f'bot{port}'] = f'10011001000'
                    print("clockwise-2")
                    target = 2
                    condition = 5

                elif(cx > 1031  and condition < 7):
                    target = 0
                    h1 = str(max(0, min(180, 80 + int((intHeadingDeg - 90) * 2.5))))
                    h2 = str(max(0, min(180, 80 - int((intHeadingDeg - 90) * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("backward-1")
                    condition = 6

                else:
                    dictionary = pause(dictionary, 2, servo)
                    laut_jao = 1
                    servo = 1
                    servoTime = time.time()
                    condition = 5

            # returning from kolkATA
            else:
                if(cx < 1035  and condition < 6):
                    target = 0
                    dictionary[f'bot{port}'] = f'0101070070{servo}'
                    print("backward-1")
                    condition = 5

                elif(intHeadingDeg > 30 and condition < 7 and cy>200):
                    print("anticlockwise-2")
                    dictionary[f'bot{port}'] = f'0110100100{servo}'
                    target = 1
                    condition = 6

                elif(cy > 360 and condition < 8):
                    target = 1
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h2 = str(max(0, min(200, 70 - int(shortestAngle * 2.5))))
                    h1 = str(max(0, min(200, 70 + int(shortestAngle * 2.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward-2")
                    condition = 7

                elif(cx > 770 and condition < 9):
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
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward-1")
                    condition = 8

                # elif(intHeadingDeg < -10 and  condition < 7):
                #     dictionary[f'bot{port}'] = f'10011201200'
                #     print("clockwise")
                #     target = 2
                #     condition = 6

                elif(cy > 45 and condition < 10):
                    target = 3
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    print(shortestAngle)
                    h2 = str(max(0, min(180, 70 - int(shortestAngle * 3.5))))
                    h1 = str(max(0, min(180, 95 + int(shortestAngle * 3.5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward")
                    condition = 9

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary = pause(dictionary, 2, {servo})
                    condition = 0

    if servo == 1 and time.time() - servoTime > 1:
        servo = 0
                
    if wall == 1:
        print(w)
        if w == 1 or w == 2 or target == len(destination)-1:
            if laut_jao == 0:
                dictionary[f'bot{port}'] = f'0101070070{servo}'
            else:
                dictionary[f'bot{port}'] = f'1010070070{servo}'
        elif w == 3:
            if laut_jao == 0:
                dictionary[f'bot{port}'] = f'0101220030{servo}'
            else:
                dictionary[f'bot{port}'] = f'1010220030{servo}'
        elif w == 4:
            if laut_jao == 0:
                dictionary[f'bot{port}'] = f'0101030220{servo}'
            else:
                dictionary[f'bot{port}'] = f'1010030220{servo}'
        else:
            w = 1

        if displacement(location[0][4][0], location[0][4][1], cx, cy) < 60:
            t = 2.2

        now = time.time()
        if now-sec > t and w not in  [3, 4]:
            wall = 0
            checkStop = []
        elif now-sec > t - 0.7:
            wall = 0
            checkStop = []
            
    elif wall == 0 and (checkStop == [] or displacement(checkStop[0][0], checkStop[0][1], cx, cy) < 10):
        checkStop.append([cx, cy])
        t = 1.5
        if len(checkStop) > 25:
            if displacement(wx, wy, cx, cy) < 10:
                w += 1
            else:
                w = 1
                wx, wy = cx, cy
            wall = 1
            sec = time.time()

    else:
        checkStop = []
        w = 1

    return dictionary, destNo2
