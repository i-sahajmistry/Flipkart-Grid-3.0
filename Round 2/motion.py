from utils import getAngle
import time

def move_bot(location, destination,laut_jao, stop):
    cx, cy = location[1][4]
    shortestAngle, intHeadingDeg = getAngle(location[1])

    if destination[0] > 1167:
        if(laut_jao == 0):
            if(cy < destination[1]):
                h1 = str(max(0, min(255, 100 - int(intHeadingDeg * 4))))
                h2 = str(max(0, min(255, 100 + int(intHeadingDeg * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'func': f'1010{h2}{h1}0'}

            elif(intHeadingDeg > -85):
                dictionary = {'func': f'01100700700'}

            else:
                dictionary = {'func': f'10010700701'}
                laut_jao = 1

        else:
            if(intHeadingDeg<-10):
                dictionary = {'func': f'10010700701'}
            
            elif(cy>73):
                h1 = str(max(0, min(255, 100 - int(shortestAngle * 4))))
                h2 = str(max(0, min(255, 100 + int(shortestAngle * 4))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary = {'func': f'0101{h2}{h1}2'}
            
            else:
                laut_jao=0
                stop=1
                dictionary = {'func': f'10010000000'}


