from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target=0
condition=0
checkStop = []
wall = 0
sec = 0
servo = 0
servoTime = 0
w, wx, wy = 0, 0, 0
t = 0
goupto = {'M': 130, 'D':300 ,'K':487, 'C':130, 'B':300, 'H':487, 'P':300, 'A': 320, 'J':495 }

def move_bot(location, destination, destNo, dictionary, letter, port, allDestinations):
    global stop, then, s, laut_jao,  target, condition, checkStop, wall, sec, servo, servoTime, wx, wy, w, t
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
        dictionary['bot1'] = f'1010000000{servo}'

    elif stop == 0.5:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 0.25:
            s = 0
            stop = 0
    # Mumbai Delhi Kolkata code

    elif letter in ['M', 'D', 'K', 'C', 'B', 'H']:
        if(laut_jao == 0):
            if(cy < goupto['M'] and condition < 1):
                target = 0
                shortestAngle, intHeadingDeg = getAngle(location[port], allDestinations[0]['M'][0], laut_jao)
                h1 = str(max(0, min(255, 190 - int(shortestAngle * 4))))
                h2 = str(max(0, min(255, 190 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward-M")
            
            elif(cy < goupto[letter] and condition < 1 and letter in ['D', 'K', 'B', 'H']):
                target = 0
                h1 = str(max(0, min(255, 190 - int(shortestAngle * 4))))
                h2 = str(max(0, min(255, 190 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward-Other")

            elif(intHeadingDeg < 60 and condition < 2 and letter in ['C', 'B', 'H']):
                dictionary['bot1'] = f'1001120120{servo}'
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -60 and condition < 2 and letter in ['M', 'D', 'K']):
                dictionary['bot1'] = f'0110115115{servo}'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx > destination[target][0] and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                h1 = str(max(0, min(255, 190 - int((intHeadingDeg-90) * 3))))
                h2 = str(max(0, min(255, 190 + int((intHeadingDeg-90) * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("RIGHT-forward-1")
                condition = 2

            elif(cx < destination[target][0] and condition < 3 and letter in ['M', 'D', 'K']):
                target = 1
                h1 = str(max(0, min(255, 190 - int((intHeadingDeg+90) * 3))))
                h2 = str(max(0, min(255, 190 + int((intHeadingDeg+90) * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("LEFT-forward-1")
                condition = 2

            else:
                laut_jao = 1
                servo = 1
                stop = 0.5
                servoTime = time.time()
                target = 0
                condition = 3
                dictionary = pause(dictionary, 1, servo)

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx < 850  and condition < 4 and letter in ['C', 'B', 'H']):
                target = 0
                dictionary['bot1'] = f'0101070070{servo}'
                print("LEFT-backward-1")
                condition = 3

            elif(cx > 855  and condition < 4 and letter in ['M', 'D', 'K']):
                target = 0
                dictionary['bot1'] = f'0101070070{servo}'
                print("RIGHT-backward-1")
                condition = 3

            elif(intHeadingDeg > 30  and condition < 5 and letter in ['C', 'B', 'H']):
                dictionary['bot1'] = f'0110115115{servo}'
                print("anticlockwise")
                target = 2
                condition = 4

            elif(intHeadingDeg < -30  and condition < 5 and letter in ['M', 'D', 'K']):
                dictionary['bot1'] = f'1001115115{servo}'
                print("clockwise")
                target = 2
                condition = 4

            elif(cy > goupto['M'] + 60 and condition < 6 and letter in ['D', 'K', 'B', 'H']):
                target = 2
                shortestAngle, intHeadingDeg = getAngle(location[port], allDestinations[0]['M'][0], laut_jao)
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                if letter in 'KH':
                    h2 = str(max(0, min(255, 190 - int(shortestAngle * 9))))
                    h1 = str(max(0, min(255, 190 + int(shortestAngle * 9))))
                else:
                    h2 = str(max(0, min(255, 190 - int(shortestAngle * 6))))
                    h1 = str(max(0, min(255, 190 + int(shortestAngle * 6))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}{servo}'
                print("backward to IS 1")
                condition = 5

            elif(cy > 27  and condition < 6):
                target = 2
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(255, 190 - int(shortestAngle * 4))))
                h1 = str(max(0, min(255, 190 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}{servo}'
                print("backward to IS 1")
                condition = 5

            else:
                laut_jao = 0
                stop = 1
                destNo = destNo+1
                target = 0
                dictionary = pause(dictionary, 1, servo)
                condition = 0
    

    # code for going to Pune, Ahemdabad , Jaipur
    else:
        if(laut_jao ==0):

            if(cy< destination[target][1] and condition < 1):
                target=0
                h1 = str(max(0, min(255, 140 - int(shortestAngle * 1.5))))
                h2 = str(max(0, min(255, 140 + int(shortestAngle * 1.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward")
                
            elif(intHeadingDeg<70 and condition < 2):
                dictionary['bot1'] = f'1001120120{servo}'
                print("clockwise")
                target=1
                condition=1

            elif(cx > 640 and condition < 3 and letter == 'P'):
                target=1
                h1 = str(max(0, min(255, 140 - int(shortestAngle * 4))))
                h2 = str(max(0, min(255, 140 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward-1")
                condition=2

            elif(cx> 560 and condition < 3 and letter != 'P'):
                target=1
                h1 = str(max(0, min(255, 140 - int(shortestAngle * 4))))
                h2 = str(max(0, min(255, 140 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward-1")
                condition=2

            elif(intHeadingDeg > 20 and condition < 4 and letter == 'P'):
                dictionary['bot1'] = f'0110110110{servo}'
                print("anticlockwise-1")
                target=2
                condition=3

            elif(cy<goupto['A'] and condition < 5 and letter != 'P'):
                target=2
                if letter == 'J':
                    shortestAngle, intHeadingDeg = getAngle(location[port], allDestinations[0]['A'][2], laut_jao)
                h1 = str(max(0, min(255, 140 - int(shortestAngle * 3))))
                h2 = str(max(0, min(255, 140 + int(shortestAngle * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward-2")
                condition=4

            elif(cy<goupto['J'] and condition < 5 and letter == 'J'):
                target=2
                h1 = str(max(0, min(255, 140 - int(shortestAngle * 3))))
                h2 = str(max(0, min(255, 140 + int(shortestAngle * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}{servo}'
                print("forward-2")
                condition=4
            
            elif(intHeadingDeg>-80 and condition < 6 and letter != 'P'):
                dictionary['bot1'] = f'0110115115{servo}'
                print("anticlockwise-2")
                target=2
                condition=5

            elif(cy < 105 and condition < 7 and letter == 'P'):
                target = 0
                dictionary['bot1'] = f'1010070070{servo}'
                print("forward-3")
                condition = 6

            elif(cx < 517  and condition < 7 and letter in ['A', 'J']):
                target = 0
                dictionary['bot1'] = f'1010070070{servo}'
                print("forward-3")
                condition = 6

            else:
                laut_jao = 1
                servo = 1
                stop = 0.5
                dictionary = pause(dictionary, 1, servo)
                servoTime = time.time()
                condition=5

        # returning from pune, ahmedabad , and jaipur
        else:
            if(cx > 495  and condition < 6 and letter in ['A', 'J']):
                target = 0
                dictionary['bot1'] = f'0101070070{servo}'
                print("LEFT-backward-1")
                condition = 5
            
            elif(cy > 95  and condition < 6 and letter == 'P'):
                target = 0
                dictionary['bot1'] = f'0101070070{servo}'
                print("LEFT-backward-1")
                condition = 5

            elif(intHeadingDeg < -10 and condition < 7 and letter != 'P'):
                print("clockwise-2")
                dictionary['bot1'] = f'1001120120{servo}'
                target=1
                condition=6

            elif(cy > goupto['A'] + 50 and condition < 8 and letter == 'J'):
                target=1
                shortestAngle, intHeadingDeg = getAngle(location[port], allDestinations[0]['A'][2], laut_jao)
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(255, 140 - int(shortestAngle * 3))))
                h1 = str(max(0, min(255, 140 + int(shortestAngle * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}{servo}'
                print("backward-2")
                condition=7

            elif(cy > 150 and condition < 8 and letter != 'P'):
                target=1
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(255, 140 - int(shortestAngle * 3))))
                h1 = str(max(0, min(255, 140 + int(shortestAngle * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}{servo}'
                print("backward-2")
                condition=7

            elif(intHeadingDeg <70 and condition < 9 and letter == 'P'):
                dictionary['bot1'] = f'1001115115{servo}'
                print("clockwise-1")
                target=0
                condition=8

            elif(cx < 855 and condition < 10):
                target=0
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(200, 140 - int(shortestAngle * 4.5))))
                h1 = str(max(0, min(200, 140 + int(shortestAngle * 4.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}{servo}'
                print("backward-1")
                condition=9

            elif(intHeadingDeg >20 and condition < 11):
                dictionary['bot1'] = f'0110105105{servo}'
                print("anticlockwise")
                target=2
                condition=10

            elif(cy > 27 and condition < 12):
                if letter == 'P':
                    target = 2
                else:
                    target = 3
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(255, 140 - int(shortestAngle * 1.5))))
                h1 = str(max(0, min(255, 140 + int(shortestAngle * 1.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}{servo}'
                print("backward")
                condition=11

            else:
                laut_jao = 0
                stop = 1
                target=0
                destNo = destNo+1
                dictionary = pause(dictionary, 1, servo)
                condition=0

    if servo == 1 and time.time() - servoTime > 1:
        servo = 0
    
    if wall == 1:
        print(w)
        if w == 1 or w == 2 or target == len(destination)-1:
            if laut_jao == 0:
                dictionary['bot1'] = f'0101070070{servo}'
            else:
                dictionary['bot1'] = f'1010070070{servo}'
        elif w == 3:
            if laut_jao == 0:
                dictionary['bot1'] = f'0101220030{servo}'
            else:
                dictionary['bot1'] = f'1010220030{servo}'
        elif w == 4:
            if laut_jao == 0:
                dictionary['bot1'] = f'0101030220{servo}'
            else:
                dictionary['bot1'] = f'1010030220{servo}'
        else:
            w = 1
        
        if displacement(location[1][4][0], location[1][4][1], cx, cy) < 60:
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
            if displacement(wx, wy, cx, cy) < 20:
                w += 1
            else:
                w = 1
                wx, wy = cx, cy
            wall = 1
            sec = time.time()

    else:
        checkStop = []
        w = 1

    return dictionary, destNo