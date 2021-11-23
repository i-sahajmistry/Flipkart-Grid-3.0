from utils import getAngle
import time

s = 0
then = 0
stop = 0
laut_jao = 0
target=0
con2=0
con3=0
con4=0
con5=0
con6=0 
con7=0

def move_bot(location, destination, destNo2, dictionary):
    global stop, then, s, laut_jao, target,con2,con3, con4, con5,con6,con7
    cx, cy = location[1][4]
    shortestAngle, intHeadingDeg = getAngle(location[1], destination[target], laut_jao)
    print(target, "****", shortestAngle, "****", intHeadingDeg)
    # print("destination", destination)

    if stop == 1:
        now = time.time()
        if s == 0:
            then = time.time()
            s = 1
        elif now - then > 1:
            s = 0
            stop = 0

    # PUNE,AHMEDABAD,JAIPUR 

    print("\n","\n")
    if destination[-2][0] < 650:
        if(laut_jao == 0):
            
            if(cy < destination[target][1] and con2==0):
                target=0
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward")

            elif(intHeadingDeg <30):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate")
                con2=1

            else:
                dictionary['bot2'] = f'01100000001'
                laut_jao = 1
                con2=0

        #returning from pune, ahmedabad ,jaipur
        else:
            if(intHeadingDeg >10 and con2==0):
                print("left-rotate")
                dictionary['bot2'] = f'01101301300'
                target=1

            elif(cy > 53):
                target=1
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
                con2=1

            else:
                laut_jao = 0
                stop = 1
                target=0
                destNo2 = destNo2+1
                dictionary['bot2'] = f'10010000000'
                con2=0
    
    #  Chennai, Bengaluru , Hyderebad
    elif(destination[-2][0] < 826):
        if(laut_jao == 0):
            if(cy < destination[target][1] and intHeadingDeg < 30 and con2==0 and con3==0):
                target=0
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward", cx, destination[target][0])

            elif(intHeadingDeg >-85 and con3==0):
                dictionary['bot2'] = f'01101101100'
                print("left-rotate")
                target=1
                con2=1

            elif(cx < destination[target][0]):
                target =1
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 2)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 2)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("left-move")
                con3=1

            else:
                dictionary['bot2'] = f'10010000001'
                laut_jao = 1
                target=0
                con2=0
                con3=0

        # returning from Chennai Bengaluru , Hyderebad
        else:
            if(cx > 640 and con2==0 and con3==0):
                target=0
                if(shortestAngle < 0):
                    shortestAngle += 180
                else:
                    shortestAngle -= 180
                h1 = str(max(0, min(255, 100 + int((shortestAngle) ))))
                h2 = str(max(0, min(255, 100 - int((shortestAngle) ))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'0101{h2}{h1}0'
                print("right-move(backward)")

            elif(intHeadingDeg <-10 and con3==0):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate")
                target=2
                con2=1

            elif(cy > 53):
                target=2
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
                con3=1

            else:
                laut_jao = 0
                stop = 1
                destNo2 = destNo2+1
                target=0
                dictionary['bot2'] = f'10010000000'
                con2=0
                con3=0
    

    # code for going to mumbai, delhi , kolkata
    else:
        if(laut_jao ==0):

            if(cy< destination[target][1] and con2==0 and con3==0 and con4==0 and con5==0 and con6==0):
                target=0
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward -1")
                
            elif(intHeadingDeg>-85 and con3==0 and con4==0 and con5==0 and con6==0):
                dictionary['bot2'] = f'01101101100'
                print("left-rotate -1")
                target=1
                con2=1
            elif(cx< destination[target][0] and con4==0 and con5==0 and con6==0 ):
                target=1
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("left-move(forward) -1")
                con3=1
            elif(intHeadingDeg <-20 and con5==0 and con6==0 ):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate-1")
                target=2
                con4=1
            elif(cy<destination[target][1] and con6==0 ):
                target=2
                h1 = str(max(0, min(255, 100 - int((shortestAngle * 5)))))
                h2 = str(max(0, min(255, 100 + int((shortestAngle * 5)))))
                h1 = '0'*(3-len(h1)) + h1
                h2 = '0'*(3-len(h2)) + h2
                dictionary['bot2'] = f'1010{h2}{h1}0'
                print("forward-2")
                con5=1
            
            elif(intHeadingDeg<30 ):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate-2")
                target=2
                con6=1


            else:
                dictionary['bot2'] = f'01100000001'
                laut_jao = 1
                con2=0
                con3=0
                con4=0
                con5=0
                con6=0 
                con7=0

        # returning from pune, ahmedabad , and jaipur
        else:
            if(intHeadingDeg >30 and con2==0 and con3==0 and con4==0 and con5==0 and con6==0):
                print("left-rotate-2")
                dictionary['bot2'] = f'01101301300'
                target=1
            elif(cy>destination[target][1] and con3==0 and con4==0 and con5==0 and con6==0):
                target=1

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
                con2=1
            elif(intHeadingDeg >-85 and con4==0 and con5==0 and con6==0):
                dictionary['bot2'] = f'01101101100'
                print("left-rotate-3")
                target=0
                con3=1
            elif(cx>destination[target][0] and con5==0 and con6==0):
                target=0
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
                con4=1
            elif(intHeadingDeg <20 and con6==0 ):
                dictionary['bot2'] = f'10011101100'
                print("right-rotate -3")
                target=3
                con5=1
            elif(cy > 53):
                target=3
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
                con6=1

            else:
                laut_jao = 0
                stop = 1
                target=0
                destNo2 = destNo2+1
                dictionary['bot2'] = f'10010000000'
                con2=0
                con3=0
                con4=0
                con5=0
                con6=0 
                con7=0

    return dictionary, destNo2



            







