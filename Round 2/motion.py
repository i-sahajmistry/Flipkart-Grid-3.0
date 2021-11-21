from utils import getAngle
import time

s = 0
then = 0
stop = 0
laut_jao = 0
sidha_laut = 0


def move_bot(location, destination, destNo, dictionary):
    global stop, then, s, laut_jao, sidha_laut
    cx, cy = location[1][4]
    shortestAngle, intHeadingDeg = getAngle(location[1], destination, laut_jao)
    print(shortestAngle, "****", intHeadingDeg)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 1:
            s = 0
            stop = 0

    if destination[0] > 826:
        if(laut_jao == 0):
            if(cy < destination[1]):
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'bot1': f'1010{h2}{h1}0'}
                print("forward")

            elif(intHeadingDeg > -85):
                dictionary = {'bot1': f'01101101100'}
                print("rotate")

            else:
                # original  dictionary = {'bot1': f'10011301301'}
                dictionary = {'bot1': f'10010000001'}

                laut_jao = 1

        else:
            if(intHeadingDeg < -30 and sidha_laut == 0):
                print("anti- rotate")

                dictionary = {'bot1': f'10011301301'}

            elif(cy > 53):
                sidha_laut = 1
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'bot1': f'0101{h2}{h1}0'}
                print("backward")

            else:
                laut_jao = 0
                stop = 1
                destNo = destNo+1
                dictionary = {'bot1': f'10010000000'}

    elif(destination[0] > 650):
        if(laut_jao == 0):
            if(cy < destination[1]):
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'bot1': f'1010{h2}{h1}0'}
                print("forward")

            elif(intHeadingDeg < 85):
                dictionary = {'bot1': f'10011101100'}
                print("rotate")

            elif(cx > destination[0]):
                h1 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'bot1': f'1010{h2}{h1}0'}
                print("right")

            else:
                # original  dictionary = {'bot1': f'10011301301'}
                dictionary = {'bot1': f'10010000001'}
                laut_jao = 1

        else:
            if(cx < 833):
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'bot1': f'0101{h2}{h1}0'}
                print("backward")

            elif(intHeadingDeg > 10):
                dictionary = {'bot1': f'10011101100'}
                print("rotate")

            elif(cy > 53):
                sidha_laut = 1
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1 = str(max(0, min(255, 100 + int((shortestAngle) * 5))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle) * 5))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'bot1': f'0101{h2}{h1}0'}
                print("backward")

            else:
                laut_jao = 0
                stop = 1
                destNo = destNo+1
                dictionary = {'bot1': f'10010000000'}

        # if(laut_jao == 0):
        #     if(cy < destination[1]):
        #         h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
        #         h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
        #         h1 = '0'*(3-len(h1)) + h1
        #         h2 = '0'*(3-len(h2)) + h2
        #         dictionary = {'bot1': f'1010{h2}{h1}0'}
        #         print("forward")

        #     elif(intHeadingDeg < 85):
        #         dictionary = {'bot1': f'10011101100'}
        #         print("rotate")

        #     else:
        #         # original  dictionary = {'bot1': f'10011301301'}
        #         dictionary = {'bot1': f'01100000001'}

        #         laut_jao = 1

        # else:
        #     if(intHeadingDeg < 30 and sidha_laut==0):
        #         print("anti- rotate")

        #         dictionary = {'bot1': f'01101301301'}

            # elif(cy > 53):
            #     sidha_laut=1
            #     if(shortestAngle < 0):
            #         shortestAngle+=180
            #     else:
            #         shortestAngle-=180
            #     h1 = str(max(0, min(255, 100 + int((shortestAngle )* 5))))
            #     h2 = str(max(0, min(255, 100 - int((shortestAngle )* 5))))
            #     h1 = '0'*(3-len(h1)) + h1
            #     h2 = '0'*(3-len(h2)) + h2
            #     dictionary = {'bot1': f'0101{h2}{h1}0'}
            #     print("backward")

            # else:
            #     laut_jao = 0
            #     stop = 1
            #     destNo = destNo+1
            #     dictionary = {'bot1': f'10010000000'}

    return dictionary, destNo
