import numpy as np
import cv2

lower_h = lower_s = lower_v = 0
upper_h = upper_s = upper_v = 255


def nothing(x):
    pass

# creates the trackbars
cv2.namedWindow('mask')
cv2.createTrackbar('HL','mask',0,255,nothing)
cv2.createTrackbar('HU','mask',0,255,nothing)
cv2.createTrackbar('SL','mask',0,255,nothing)
cv2.createTrackbar('SU','mask',0,255,nothing)
cv2.createTrackbar('VL','mask',0,255,nothing)
cv2.createTrackbar('VU','mask',0,255,nothing)

cv2.setTrackbarPos('HL', 'mask', lower_h)
cv2.setTrackbarPos('HU', 'mask', upper_h)
cv2.setTrackbarPos('SL', 'mask', lower_s)
cv2.setTrackbarPos('SU', 'mask', upper_s)
cv2.setTrackbarPos('VL', 'mask', lower_v)
cv2.setTrackbarPos('VU', 'mask', upper_v)

img = cv2.imread('cube-green.jpeg', cv2.IMREAD_COLOR)

cv2.imshow('ImageOriginal',img)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

while (1):
	lower_h = cv2.getTrackbarPos('HL','mask')
	lower_s = cv2.getTrackbarPos('SL','mask')
	lower_v = cv2.getTrackbarPos('VL','mask')
	upper_h = cv2.getTrackbarPos('HU','mask')
	upper_s = cv2.getTrackbarPos('SU','mask')
	upper_v = cv2.getTrackbarPos('VU','mask')
	lower_hsv = np.array([lower_h,lower_s,lower_v])
	upper_hsv = np.array([upper_h,upper_s,upper_v])
	#print "lower_hsv", lower_hsv, "upper_hsv", upper_hsv
	mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
	
	cv2.imshow('mask', mask)
	
	edges = cv2.Canny(mask, 100, 200)
	#area = cv2.contourArea(edges)
    # Test comment
	cv2.imshow('edges', edges)
	if 27 == cv2.waitKey(10):  #27 = escape key
		break
