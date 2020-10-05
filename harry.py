import cv2
import time
import numpy as np


def nothing(x):
    pass
    
    
cam = cv2.VideoCapture(0)
i=0
_,oldframe = cam.read()
while(i<20):
    i+=1
    _,oldframe = cam.read()
oldframe = cv2.flip(oldframe,1)

print("Backgroung Capture Successfull!!")


#To Control the value of mask
cv2.namedWindow("Control")

cv2.createTrackbar("L-H","Control",0,180,nothing)
cv2.createTrackbar("L-S","Control",0,255,nothing)
cv2.createTrackbar("L-V","Control",0,255,nothing)
cv2.createTrackbar("U-H","Control",0,180,nothing)
cv2.createTrackbar("U-S","Control",0,255,nothing)
cv2.createTrackbar("U-V","Control",0,255,nothing)


while True:
    
    _,frame = cam.read()
    frame = cv2.flip(frame,1)
    cpy = frame.copy()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    frame = cv2.medianBlur(frame,5)
    
    
    lh = cv2.getTrackbarPos("L-H","Control")
    ls = cv2.getTrackbarPos("L-S","Control")
    lv = cv2.getTrackbarPos("L-V","Control")
    uh = cv2.getTrackbarPos("U-H","Control")
    us = cv2.getTrackbarPos("U-S","Control")
    uv = cv2.getTrackbarPos("U-V","Control")

    f = cv2.inRange(frame,(lh,ls,lv),(uh,us,uv))
    #f = cv2.inRange(frame,(91,53,0),(133,255,255))

    img = cv2.bitwise_and(cpy,cpy,mask =cv2.bitwise_not(f))
    cpy = cv2.bitwise_and(oldframe,oldframe,mask =f)
    final = cv2.add(img,cpy)
    
    #Comment Below After Getting the right value
    cv2.imshow("Mask", f)
    cv2.imshow("Harry Potter", final)
    cv2.imshow("CutOut Cloak",frame )
    #cv2.imshow("background",cpy )
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    
    




    






