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
secondReplce = 0
conditionReplace=0

w, wx, wy = 0, 0, 0

goupto = {'P': 195, 'A':390 ,'J':633, 'C':190, 'B':390, 'H':633 }

def move_bot(location, destination, destNo2, dictionary, letter, port,ids, allDestinations, newBotEntry):
    global stop, then, s, laut_jao, target, condition, sec, wall, checkStop, servo, servoTime, w, wx, wy, t, secondReplce, conditionReplace
    position = location[port][4]
    cx, cy = position
    shortestAngle, intHeadingDeg = getAngle(location[port], destination[target], laut_jao)

# //***********************************************************************************************************************//
                                        # Replacement of bot 2 code started
# //***********************************************************************************************************************//

    if(newBotEntry==1):
        laut_jao = 1
        if(port==ids[3]):
            secondReplce=2
        else:
            secondReplce=0
                
        if(port!=ids[1] and secondReplce!=2):
          
            if(intHeadingDeg > -60 and conditionReplace<1):
                print("anticlockwise-1")
                dictionary[f'bot{port}'] = f'0110090090{servo}'
                target = 0
                conditionReplace = 0

           
            elif(cx > 860 and conditionReplace<2):
                shortestAngle, intHeadingDeg = getAngle(location[port], (825, 800), laut_jao)
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1, h2 = getSpeeds(target, destination, position)
                h1 = str(max(0, min(240, h1 + int(shortestAngle * 2.5))))
                h2 = str(max(0, min(240, h2 - int(shortestAngle * 2.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                print("backward-1")
                conditionReplace = 1


            elif(intHeadingDeg < -30 and conditionReplace<3):
                dictionary[f'bot{port}'] = f'1001090090{servo}'
                print("clockwise-1")
                target = 0
                conditionReplace = 2

            else:
                secondReplce=1

        if(secondReplce==2 or secondReplce==1):
            if(cy > goupto['P'] + 20):
                target = 2
                if(secondReplce==2):
                    shortestAngle, intHeadingDeg = getAngle(location[port], (840,150), laut_jao)
                else:
                    shortestAngle, intHeadingDeg = getAngle(location[port], (800,150), laut_jao)
                    
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1, h2 = getSpeeds(target, destination, position)
                h1 = str(max(0, min(240, h1 + int(shortestAngle * 4))))
                h2 = str(max(0, min(240, h2 - int(shortestAngle * 4))))
                
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
                h1 = str(max(0, min(240, h1 + int(shortestAngle * 2))))
                h2 = str(max(0, min(240, h2 - int(shortestAngle * 2))))
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
                dictionary = pause(dictionary, port, servo)
                secondReplce=0
                conditionReplace=0
                newBotEntry=0
                condition=0


   

# //***********************************************************************************************************************//
                                    # GOING TO P A J C B H
# //***********************************************************************************************************************//

    elif stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 0.5:
            s = 0
            stop = 0

    # going to C,B,H,P,A,J

    elif letter in ['P', 'A', 'J', 'C', 'B', 'H']:
        if(laut_jao == 0):
            if(cy < goupto['P'] and condition < 1):
                target = 0
                h1, h2 = getSpeeds(target, destination, position)
                shortestAngle, intHeadingDeg = getAngle(location[port], (832, 210), laut_jao)
                h1 = str(max(0, min(240, h1 - int(shortestAngle * 4))))
                h2 = str(max(0, min(240, h2 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2

                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                
                print("forward-M")
            
            elif(cy < goupto['A'] and condition < 1 and letter in ['A', 'J', 'B', 'H']):
                target = 0
                h1, h2 = getSpeeds(target, destination, position)
                shortestAngle, intHeadingDeg = getAngle(location[port], (845, 405), laut_jao)
                h1 = str(max(0, min(240, h1 - int(shortestAngle * 7))))
                h2 = str(max(0, min(240, h2 + int(shortestAngle * 7))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2

                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                
                print("forward-D")
            
            elif(cy < goupto[letter] and condition < 1 and letter in ['J', 'H']):


                target = 0
                h1, h2 = getSpeeds(target, destination, position)
                h1 = str(max(0, min(240, h1 - int(shortestAngle * 5))))
                h2 = str(max(0, min(240, h2 + int(shortestAngle * 5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                print("forward-Other")

            elif(intHeadingDeg < 60 and condition < 2 and letter in ['P', 'A', 'J']):
                dictionary[f'bot{port}'] = f'1001090090{servo}'
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -60 and condition < 2 and letter == 'H'):
                dictionary[f'bot{port}'] = f'0110090090{servo}'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -60 and condition < 2 and letter in ['C', 'B']):
                dictionary[f'bot{port}'] = f'0110090090{servo}'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx > destination[target][0] and condition < 3 and letter in ['P', 'A', 'J']):
                target = 1
                h1 = str(max(0, min(240, 90 + int((intHeadingDeg - 90) * 1))))
                h2 = str(max(0, min(240, 90 - int((intHeadingDeg - 90) * 1))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                print("RIGHT-forward-1")
                condition = 2

            elif(cx < destination[target][0] - 5 and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                h1 = str(max(0, min(240, 80 - int((intHeadingDeg + 90) * 1))))
                h2 = str(max(0, min(240, 80 + int((intHeadingDeg + 90) * 1))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                print("LEFT-forward-1")
                condition = 2

            else:
                dictionary = pause(dictionary, port, 1)
                servo = 1
                servoTime = time.time()
                laut_jao = 1
                target = 0
                condition = 3

# //***********************************************************************************************************************//
                                    # RETURNING FROM P A J C B H
# //***********************************************************************************************************************//

        else:
            if(cx > 840  and condition < 4 and letter in 'CBH'):
                target = 0
                h1 = str(max(0, min(240, 80 - int((intHeadingDeg + 90) * 0.5))))
                h2 = str(max(0, min(240, 80 + int((intHeadingDeg + 90) * 0.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                print("backward-1")
                condition = 3

            elif(cx < 815  and condition < 4 and letter in 'AJ'):
                target = 0
                h1 = str(max(0, min(240, 80 - int((intHeadingDeg - 90) * 0.5))))
                h2 = str(max(0, min(240, 80 + int((intHeadingDeg - 90) * 0.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                print("backward-1")
                condition = 3

            elif(intHeadingDeg < -30  and condition < 5):
                dictionary[f'bot{port}'] = f'1001090090{servo}'
                print("clockwise", intHeadingDeg)
                target = 2
                condition = 4

            

            # elif(intHeadingDeg > 20  and condition < 5):
            elif(intHeadingDeg > 30  and condition < 5):
                condition = 4
                dictionary[f'bot{port}'] = f'0110090090{servo}'
                print("anticlockwise", intHeadingDeg)
                target = 2  


            # elif(intHeadingDeg > 30  and condition < 5 and letter in 'P'):
            #     condition = 4
            #     dictionary[f'bot{port}'] = f'0110090090{servo}'
            #     print("anticlockwise", intHeadingDeg)
            #     target = 2
                
                          

            elif(cy > goupto['P'] + 60 and condition < 6 and letter in ['A', 'J', 'B', 'H']):
                target = 2
                if(port==2):
                    shortestAngle, intHeadingDeg = getAngle(location[port], (815,150), laut_jao)
                else:
                    shortestAngle, intHeadingDeg = getAngle(location[port], (840,150), laut_jao)

                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1, h2 = getSpeeds(target, destination, position)
                h1 = str(max(0, min(240, h1 + int(shortestAngle * 4))))
                h2 = str(max(0, min(240, h2 - int(shortestAngle * 4))))
                
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
                h1 = str(max(0, min(240, h1 + int(shortestAngle * 3))))
                h2 = str(max(0, min(240, h2 - int(shortestAngle * 3))))
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
                dictionary = pause(dictionary, port, servo)
                condition = 0
# //***********************************************************************************************************************//
                                    # GOING TO M D
# //***********************************************************************************************************************//  
    else:
        if(letter in "MD"):
            if(laut_jao == 0):

                if(cy < 290 and condition < 1):
                    target = 0
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 - int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 + int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward")

                elif(intHeadingDeg > -50 and condition < 2):
                    dictionary[f'bot{port}'] = f'01100900900'
                    print("anticlockwise")
                    target = 1
                    condition = 1

                elif(cx < 1120 and condition < 2 and letter in 'MD'):
                    target = 1
                    h1,h2= getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 - int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 + int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward-1")
                    condition = 1

                elif(intHeadingDeg < -70 and condition < 3 and letter == "D"):
                    dictionary[f'bot{port}'] = f'1001090090{servo}'
                    print("clockwise-1")
                    target = 1
                    condition = 2

                elif((intHeadingDeg > -160 and intHeadingDeg < 100)  and condition < 3 and letter == "M"):
                    dictionary[f'bot{port}'] = f'0110090090{servo}'
                    print("anticlockwise-1")
                    target = 1
                    condition = 2

                elif(cy > 328 and condition < 4 and letter == 'M'):
                    if intHeadingDeg < 0:
                        intHeadingDeg += 180
                    else:
                        intHeadingDeg -= 180
                    h1 = str(max(0, min(240, 80 + int(intHeadingDeg * 1))))
                    h2 = str(max(0, min(240, 70 - int(intHeadingDeg * 1))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    condition = 3

                elif(cy < 356 and condition < 4 and letter == 'D'):
                    h1 = str(max(0, min(240, 80 + int(intHeadingDeg * 1))))
                    h2 = str(max(0, min(240, 70 - int(intHeadingDeg * 1))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    condition = 3

                else:
                    servo = 1
                    servoTime = time.time()
                    dictionary = pause(dictionary, port, servo)
                    laut_jao = 1
                    condition = 3
# //***********************************************************************************************************************//
                                    # RETURNING FROM M D
# //***********************************************************************************************************************//
            else:
                if cy < 328 and condition < 4 and letter == 'M':
                    dictionary[f'bot{port}'] = f'01010800801'
                    condition = 3

                elif cy > 355 and condition < 4 and letter == 'D':
                    dictionary[f'bot{port}'] = f'01010800801'
                    condition = 3

                elif(intHeadingDeg > -60 and condition < 5 and letter == "D"):
                    print("anticlockwise-1")
                    dictionary[f'bot{port}'] = f'0110100100{servo}'
                    target = 0
                    condition = 4

                elif(intHeadingDeg > -110 and condition < 5 and letter == "M"):
                    dictionary[f'bot{port}'] = f'1001100100{servo}'
                    print("clockwise-1")
                    target = 0
                    condition = 4

                elif(cx > 850 and condition < 6):
                    target = 0
                    shortestAngle, intHeadingDeg = getAngle(location[port], destination[target], laut_jao)
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 + int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 - int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward-1")
                    condition = 5

                elif(intHeadingDeg < -50 and  condition < 7):
                    dictionary[f'bot{port}'] = f'10011001000'
                    print("clockwise")
                    target = 2
                    condition = 6

                elif(cy > 45 and condition < 8):
                    target = 2
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 + int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 - int(shortestAngle * 3))))
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
                    dictionary = pause(dictionary, port, 0)
                    condition = 0

# //***********************************************************************************************************************//
                                    # GOING TO K
# //***********************************************************************************************************************//  
        else:
            if(laut_jao == 0):

                if(cy < 290 and condition < 1):
                    target = 0
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 - int(shortestAngle * 4))))
                    h2 = str(max(0, min(240, h2 + int(shortestAngle * 4))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward")

                elif(intHeadingDeg > -30 and condition < 2):
                    dictionary[f'bot{port}'] = f'01100900900'
                    print("anticlockwise")
                    target = 1
                    condition = 1

                elif(cx < 1220 and condition < 3):
                    target = 1
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 - int(shortestAngle * 4))))
                    h2 = str(max(0, min(240, h2 + int(shortestAngle * 4))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("forward-1")
                    condition = 2

                elif(intHeadingDeg < -40 and condition < 4 ):
                    dictionary[f'bot{port}'] = f'1001090090{servo}'
                    print("clockwise-1")
                    target = 1
                    condition = 3

                elif(cy < 660 and condition < 5):
                    target = 2
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 - int(shortestAngle * 4))))
                    h2 = str(max(0, min(240, h2 + int(shortestAngle * 4))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print('forward-2')
                    condition = 4

                elif(intHeadingDeg <45 and condition < 6):
                    dictionary[f'bot{port}'] = f'10011001000'
                    print("clockwise-2")
                    target = 2
                    condition = 5

                elif(cx > 1275  and condition < 7):
                    target = 0
                    h1 = str(max(0, min(240, 130 + int((intHeadingDeg - 90) * 3))))
                    h2 = str(max(0, min(240, 130 - int((intHeadingDeg - 90) * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'1010{h2}{h1}{servo}'
                    print("backward-1")
                    condition = 6

                else:
                    servo = 1
                    dictionary = pause(dictionary, port, servo)
                    laut_jao = 1
                    
                    servoTime = time.time()
                    condition = 5
# //***********************************************************************************************************************//
                                    # RETURNING FROM K
# //***********************************************************************************************************************//  
            else:
                if(cx < 1275  and condition < 6):
                    target = 0
                    dictionary[f'bot{port}'] = f'0101100100{servo}'
                    print("backward-1")
                    condition = 5

                elif(intHeadingDeg > 30 and condition < 7 and cy>200):
                    print("anticlockwise-2")
                    dictionary[f'bot{port}'] = f'0110100100{servo}'
                    target = 1
                    condition = 6

                elif(cy > 370 and condition < 8):
                    target = 1
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 + int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 - int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward-2")
                    condition = 7

                elif(intHeadingDeg > -25 and condition < 9 ):
                    print("anticlockwise-1")
                    dictionary[f'bot{port}'] = f'0110090090{servo}'
                    target = 0
                    condition = 8

                elif(cx > 830 and condition < 10):
                    target = 0
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 + int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 - int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward-1")
                    condition = 9



                elif(intHeadingDeg < -70 and  condition < 11):
                    dictionary[f'bot{port}'] = f'10011201200'
                    print("clockwise")
                    target = 2
                    condition = 10

                elif(cy > 45 and condition < 12):
                    target = 3
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180
                    h1, h2 = getSpeeds(target, destination, position)
                    h1 = str(max(0, min(240, h1 + int(shortestAngle * 3))))
                    h2 = str(max(0, min(240, h2 - int(shortestAngle * 3))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary[f'bot{port}'] = f'0101{h2}{h1}{servo}'
                    print("backward")
                    condition = 11

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary = pause(dictionary, port, {servo})
                    condition = 0

    if servo == 1 and time.time() - servoTime > 1:
        servo = 0
                
# //***********************************************************************************************************************//
                                    # WALL COLLISION
# //***********************************************************************************************************************//  
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
        if len(checkStop) > 20:
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

    return dictionary, destNo2, newBotEntry
