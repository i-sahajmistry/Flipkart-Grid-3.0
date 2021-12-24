from utils import *
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target=0
condition=0
goupto = {'M': 130, 'D':300 ,'K':487, 'C':130, 'B':300, 'H':487, 'P':300, 'A': 300, 'J':475 }

def move_bot(location, destination, destNo, dictionary, letter, port):
    global stop, then, s, laut_jao,  target, condition
    cx, cy = location[port][4]
    shortestAngle, intHeadingDeg = getAngle(location[port], destination[target], laut_jao)

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
            if(cy < goupto[letter] and condition < 1):
                target = 0
                h1 = str(max(0, min(180, 90 - int(shortestAngle * 4))))
                h2 = str(max(0, min(180, 90 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("forward")

            elif(intHeadingDeg < 60 and condition < 2 and letter in ['C', 'B', 'H']):
                dictionary['bot1'] = '10011201200'
                print("clockwise")
                target = 1
                condition = 1

            elif(intHeadingDeg > -60 and condition < 2 and letter in ['M', 'D', 'K']):
                dictionary['bot1'] = '01101151150'
                print("anticlockwise")
                target = 1
                condition = 1

            elif(cx > destination[target][0] and condition < 3 and letter in ['C', 'B', 'H']):
                target = 1
                h1 = str(max(0, min(180, 100 - int((intHeadingDeg-90) * 3))))
                h2 = str(max(0, min(180, 90 + int((intHeadingDeg-90) * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("RIGHT-forward-1")
                condition = 2

            elif(cx < destination[target][0] and condition < 3 and letter in ['M', 'D', 'K']):
                target = 1
                h1 = str(max(0, min(180, 100 - int((intHeadingDeg+90) * 3))))
                h2 = str(max(0, min(180, 90 + int((intHeadingDeg+90) * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("LEFT-forward-1")
                condition = 2

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                target = 0
                condition = 3

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx < 850  and condition < 4 and letter in ['C', 'B', 'H']):
                target = 0
                dictionary['bot1'] = f'01010700701'
                print("LEFT-backward-1")
                condition = 3

            elif(cx > 865  and condition < 4 and letter in ['M', 'D', 'K']):
                target = 0
                dictionary['bot1'] = f'01010700701'
                print("RIGHT-backward-1")
                condition = 3

            elif(intHeadingDeg > 30  and condition < 5 and letter in ['C', 'B', 'H']):
                dictionary['bot1'] = '01101151150'
                print("anticlockwise")
                target = 2
                condition = 4

            elif(intHeadingDeg < -30  and condition < 5 and letter in ['M', 'D', 'K']):
                dictionary['bot1'] = '10011151150'
                print("clockwise")
                target = 2
                condition = 4

            elif(cy >40  and condition < 6):
                target = 2
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(180, 75 - int(shortestAngle * 4))))
                h1 = str(max(0, min(180, 75 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}0'
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
                h1 = str(max(0, min(180, 90 - int(shortestAngle * 1.5))))
                h2 = str(max(0, min(180, 80 + int(shortestAngle * 1.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("forward")
                
            elif(intHeadingDeg<70 and condition < 2):
                dictionary['bot1'] = '10011201200'
                print("clockwise")
                target=1
                condition=1

            elif(cx > 640 and condition < 3 and letter == 'P'):
                target=1
                h1 = str(max(0, min(180, 90 - int(shortestAngle * 4))))
                h2 = str(max(0, min(180, 80 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("forward-1")
                condition=2

            elif(cx> 590 and condition < 3 and letter != 'P'):
                target=1
                h1 = str(max(0, min(180, 90 - int(shortestAngle * 4))))
                h2 = str(max(0, min(180, 80 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("forward-1")
                condition=2

            elif(intHeadingDeg > 20 and condition < 4 and letter == 'P'):
                dictionary['bot1'] = '01101101100'
                print("anticlockwise-1")
                target=2
                condition=3

            elif(cy<goupto[letter] and condition < 5 and letter != 'P'):
                target=2
                h1 = str(max(0, min(180, 90 - int(shortestAngle * 3))))
                h2 = str(max(0, min(180, 80 + int(shortestAngle * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'1010{h2}{h1}0'
                print("forward-2")
                condition=4
            
            elif(intHeadingDeg>-80 and condition < 6 and letter != 'P'):
                dictionary['bot1'] = '01101151150'
                print("anticlockwise-2")
                target=2
                condition=5

            else:
                dictionary = pause(dictionary, 1, 1)
                laut_jao = 1
                condition=6

        # returning from pune, ahmedabad , and jaipur
        else:
            if(intHeadingDeg < -10 and condition < 7 and letter != 'P'):
                print("clockwise-2")
                dictionary['bot1'] = '10011201201'
                target=1
                condition=6

            elif(cy > 170 and condition < 8 and letter != 'P'):
                target=1
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(180, 80 - int(shortestAngle * 3))))
                h1 = str(max(0, min(180, 80 + int(shortestAngle * 3))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}0'
                print("backward-2")
                condition=7

            elif(intHeadingDeg <70 and condition < 9 and letter == 'P'):
                dictionary['bot1'] = '10011151150'
                print("clockwise-1")
                target=0
                condition=8

            elif(cx < 850 and condition < 10):
                target=0
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(180, 80 - int(shortestAngle * 4.5))))
                h1 = str(max(0, min(180, 80 + int(shortestAngle * 4.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}0'
                print("backward-1")
                condition=9

            elif(intHeadingDeg >20 and condition < 11):
                dictionary['bot1'] = '01101151150'
                print("anticlockwise")
                target=2
                condition=10

            elif(cy > 45 and condition < 12):
                if letter == 'P':
                    target = 2
                else:
                    target = 3
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h2 = str(max(0, min(180, 80 - int(shortestAngle * 1.5))))
                h1 = str(max(0, min(180, 80 + int(shortestAngle * 1.5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot1'] = f'0101{h2}{h1}0'
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