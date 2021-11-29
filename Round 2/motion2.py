from utils import getAngle
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
    print(target, "****", shortestAngle, "****", intHeadingDeg)
    # print("destination", destination)

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
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward")

            elif(intHeadingDeg < 30 and condition < 2):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate")
                condition = 1

            else:
                dictionary['bot2'] = f'01100000001'
                laut_jao = 1
                condition = 2

        # returning from pune, ahmedabad ,jaipur
        else:
            if(intHeadingDeg > 10 and condition < 3):
                print("left-rotate")
                dictionary['bot2'] = f'01101301300'
                target = 1
                condition = 2

            elif(cy > 53 and condition < 4):
                target = 1
                condition = 3
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180

                h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'0101{h2}{h1}0'
                print("backward")

            else:
                laut_jao = 0
                condition = 0
                target = 0
                dictionary['bot2'] = f'10010000000'
                stop = 1
                destNo2 = destNo2+1

    #  going to Chennai, Bengaluru , Hyderebad
    elif(destination[-2][0] < 826):
        if(laut_jao == 0):
            if(cy < destination[target][1] and intHeadingDeg < 30 and condition < 1):
                target = 0
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward", cx, destination[target][0])

            elif(intHeadingDeg > -85  and condition < 2):
                dictionary['bot2'] = f'01101101100'
                print("left-rotate")
                target = 1
                condition = 1

            elif(cx < destination[target][0] and condition < 3):
                target = 1
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 2)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 2)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("left-move")
                condition = 2

            else:
                dictionary['bot2'] = f'10010000001'
                laut_jao = 1
                target = 0
                condition = 3

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx > 64  and condition < 4):
                target = 0
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1 = str(max(0, min(255, 100 + int((shortestAngle)))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'0101{h2}{h1}0'
                print("right-move(backward)")
                condition = 3

            elif(intHeadingDeg < -10  and condition < 5):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate")
                target = 2
                condition = 4

            elif(cy > 53  and condition < 6):
                target = 2
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'0101{h2}{h1}0'
                print("backward to IS 2")
                condition = 5

            else:
                laut_jao = 0
                stop = 1
                destNo2 = destNo2+1
                target = 0
                dictionary['bot2'] = f'10010000000'
                condition = 0

    else:
        if(destination[-2][1] < 400):
    # code for going to mumbai, delhi
            if(laut_jao == 0):
            
                if(cy < destination[target][1] and condition < 1):
                    target = 0
                    h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                    h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward -1")

                elif(intHeadingDeg > -85 and condition < 2):
                    dictionary['bot2'] = f'01101101100'
                    print("left-rotate -1")
                    target = 1
                    condition = 1

                elif(cx < destination[target][0] and condition < 3):
                    target = 1
                    h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                    h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("left-move(forward) -1")
                    condition = 2

                elif(intHeadingDeg < -20 and condition < 4 and letter == "D"):
                    dictionary['bot2'] = f'10011101100'
                    print("right-rotate-1")
                    target = 1
                    condition = 3

                elif((intHeadingDeg > -170 and intHeadingDeg < 100)  and condition < 4 and letter == "M"):
                    dictionary['bot2'] = f'01101101100'
                    print("left-rotate -1")
                    target = 1
                    condition = 3

                else:
                    dictionary['bot2'] = f'01100000001'
                    laut_jao = 1
                    condition = 4

            # returning from mumbai
            else:
                if(intHeadingDeg > -80 and condition < 5 and letter == "D"):
                    print("left-rotate-2")
                    dictionary['bot2'] = f'01101301300'
                    target = 0
                    condition = 4

                elif(intHeadingDeg >-85 and condition < 5 and letter == "M"):
                    dictionary['bot2'] = f'10011101100'
                    print("right-rotate-1")
                    target = 0
                    condition = 4

                elif(cx > destination[target][0] and condition < 6):
                    target = 0
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180

                    h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                    h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("left-move(backward)-1")
                    condition = 5

                elif(intHeadingDeg < -20 and  condition < 7):
                    dictionary['bot2'] = f'10011101100'
                    print("right-rotate -3")
                    target = 2
                    condition = 6

                elif(cy > 53 and condition < 8):
                    target = 2
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180

                    h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                    h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward-2")
                    condition = 7

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary['bot2'] = f'10010000000'
                    condition = 0

        # going to Kolkata
        else:
            if(laut_jao == 0):

                if(cy < destination[target][1] and condition < 1):
                    target = 0
                    h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                    h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward -1")

                elif(intHeadingDeg > -85 and condition < 2):
                    dictionary['bot2'] = f'01101101100'
                    print("left-rotate -1")
                    target = 1
                    condition = 1

                elif(cx < destination[target][0] and condition < 3):
                    target = 1
                    h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                    h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("left-move(forward) -1")
                    condition = 2

                elif(intHeadingDeg < -20 and condition < 4 and cy>200):
                    dictionary['bot2'] = f'10011101100'
                    print("right-rotate-1")
                    target = 2
                    condition = 3

                elif(cy < destination[target][1] and condition < 5):
                    target = 2
                    h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                    h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'1010{h2}{h1}0'
                    print("forward-2")
                    condition = 4

                elif(intHeadingDeg <5 and condition < 6):
                    dictionary['bot2'] = f'10011101100'
                    print("right-rotate-2")
                    target = 2
                    condition = 5

                else:
                    dictionary['bot2'] = f'01100000001'
                    laut_jao = 1
                    condition = 6

            # returning from kolkATA
            else:
                if(intHeadingDeg > 10 and condition < 7 and cy>200):
                    print("left-rotate-2")
                    dictionary['bot2'] = f'01101301300'
                    target = 1
                    condition = 6

                elif(cy > destination[target][1] and condition < 8):
                    target = 1

                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180

                    h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                    h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward-1")
                    condition = 7

                elif(intHeadingDeg > -85 and condition < 9):
                    dictionary['bot2'] = f'01101101100'
                    print("left-rotate-3")
                    target = 0
                    condition = 8

                elif(cx > destination[target][0] and condition < 10):
                    target = 0
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180

                    h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                    h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("left-move(backward)-1")
                    condition = 9

                elif(intHeadingDeg < 20 and condition < 11):
                    dictionary['bot2'] = f'10011101100'
                    print("right-rotate -3")
                    target = 3
                    condition = 10

                elif(cy > 53 and condition < 12):
                    target = 3
                    sidha_laut = 1
                    if(shortestAngle < 0):
                        shortestAngle += 180
                    else:
                        shortestAngle -= 180

                    h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                    h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                    h1 = '0'*(3-len(h1)) + h1
                    h2 = '0'*(3-len(h2)) + h2
                    dictionary['bot2'] = f'0101{h2}{h1}0'
                    print("backward-2")
                    condition = 11

                else:
                    laut_jao = 0
                    stop = 1
                    target = 0
                    destNo2 = destNo2+1
                    dictionary['bot2'] = f'10010000000'
                    condition = 0
                

    return dictionary, destNo2
