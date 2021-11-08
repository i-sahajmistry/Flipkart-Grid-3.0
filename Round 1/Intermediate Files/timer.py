
import cv2
cap = cv2.VideoCapture(0)

import time
starttime=time.time()

while True:
    
    ret, frame = cap.read()  # read frame/image one by one    
        



    font = cv2.FONT_HERSHEY_SIMPLEX  #font to apply on text
    cv2.putText(frame,f'time: {str(round (time.time()-starttime,3))}', (50, 50), font, 1, (0, 150, 255), 2) # add text on frame
    



    key = cv2.waitKey(1)  # wait till key press 
    if key == ord("q"):  # exit loop on 'q' key press
        break
        
cap.release() # release video capture object
cv2.destroyAllWindows()  # destroy all frame windows