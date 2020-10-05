import cv2

import numpy as np
import cv2

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
	"""
	@brief      Overlays a transparant PNG onto another image using CV2
	
	@param      background_img    The background image
	@param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
	@param      x                 x location to place the top-left corner of our overlay
	@param      y                 y location to place the top-left corner of our overlay
	@param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
	
	@return     Background image with overlay on top
	"""
	
	bg_img = background_img.copy()
	
	
	if overlay_size is not None:
		img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

	# Extract the alpha mask of the RGBA image, convert to RGB 
	b,g,r,a = cv2.split(img_to_overlay_t)
	overlay_color = cv2.merge((b,g,r))
	
	# Apply some simple filtering to remove edge noise
	mask = cv2.medianBlur(a,5)

	h, w, _ = overlay_color.shape
	roi = bg_img[y:y+h, x:x+w]

	# Black-out the area behind the logo in our original ROI
	img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
	
	# Mask out the logo from the logo image.
	img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

	# Update the original image with our new ROI
	bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

	return bg_img


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
logo = cv2.imread('face.png')

def nothing(x):
    pass
cam = cv2.VideoCapture(0)

cv2.namedWindow("Control")
cv2.createTrackbar("arg1","Control",5,30,nothing)

while True:

    ret,frame = cam.read()
    frame = cv2.flip(frame,1)
    cpy = frame.copy()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    arg = cv2.getTrackbarPos("arg1","Control")
    face = face_cascade.detectMultiScale(frame,1.1,arg)
    

    for rect in face:
        x,y,w,h = rect
        
        cv2.rectangle(cpy,(x,y-30),(x+w,y+h+10),(0,255,0),2)
        
    
        
    cv2.imshow("test",cpy)


    k = cv2.waitKey(1)
    if(k==27):
        break


cam.release()
cv2.destroyAllWindows()
