import cv2
import threading
import numpy as np
import time
import pyautogui
import math
#https://www.gameflare.com/online-game/table-tennis-pro/
vs = cv2.VideoCapture(0)

ub = np.array([171,113,45])
lb = np.array([87,0,0])

def translate(sensor_val, in_from, in_to, out_from, out_to):
    out_range = out_to - out_from
    in_range = in_to - in_from
    in_val = sensor_val - in_from
    val=(float(in_val)/in_range)*out_range
    out_val = out_from+val
    return out_val

def nothing(x):
    pass

cv2.namedWindow("Control")

cv2.createTrackbar("L-H","Control",0,180,nothing)
cv2.createTrackbar("L-S","Control",0,255,nothing)
cv2.createTrackbar("L-V","Control",0,255,nothing)
cv2.createTrackbar("U-H","Control",0,180,nothing)
cv2.createTrackbar("U-S","Control",0,255,nothing)
cv2.createTrackbar("U-V","Control",0,255,nothing)
x,y = pyautogui.size()
print(x,y)

_,f = vs.read()
print(f.shape)
#x ->width
#y->height

height, width,_ = f.shape
last_cx = 0
last_cy = 0

while True:
    
    _,f = vs.read()
    f = cv2.resize(f, (x,y), interpolation = cv2.INTER_AREA)
    f = cv2.flip(f,1)
    cpy = f.copy()
    
    
    hsv = cv2.cvtColor(cpy, cv2.COLOR_BGR2HSV)
    '''
    lh = cv2.getTrackbarPos("L-H","Control")
    ls = cv2.getTrackbarPos("L-S","Control")
    lv = cv2.getTrackbarPos("L-V","Control")
    uh = cv2.getTrackbarPos("U-H","Control")
    us = cv2.getTrackbarPos("U-S","Control")
    uv = cv2.getTrackbarPos("U-V","Control")
    '''
    
    #mask1 = cv2.inRange(hsv,(lh,ls,lv),(uh,us,uv))
    mask1 = cv2.inRange(hsv,(88,223,0),(180,255,255))
    

    #mask1 = cv2.inRange(hsv,lb,ub)
    
    #=======================

    
    mx,my = pyautogui.position()

    
    #=======================
    
    cnts, hierarchy = cv2.findContours(mask1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0:
        pass
    else:
        segmented = max(cnts, key=cv2.contourArea)
        M = cv2.moments(segmented)
        
        try:
            cx = round(M['m10'] / M['m00'])
            cy = round(M['m01'] / M['m00'])
        except:
            pass
        '''
        for p in segmented:
            cx += p[0][0]
            cy += p[0][1]
            #cv2.drawContours(cpy, [p], -1, (0, 255, 0), 2)
        cx = int(cx/len(segmented))
        cy = int(cy/len(segmented))
        '''
        #cv2.circle(cpy, (cx, cy), 7, (255, 255, 255), -1)

        

        if(math.sqrt((cx-last_cx)**2 + (cy-last_cy)**2 ) > 15 ):
            pyautogui.moveTo(cx, cy, duration=0.01)
            
        
        last_cx = cx
        last_cy = cy

    
    cv2.imshow("nf", cv2.resize(cpy, (300,300), interpolation = cv2.INTER_AREA))
    cv2.imshow("new mask", cv2.resize(mask1, (300,300), interpolation = cv2.INTER_AREA))
    
    
    
    

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        time.sleep(5)
    
    elif k%256 == 32:
        # ESC pressed
        print("Space hit, closing...")
        break

    
    



cv2.destroyAllWindows()

































