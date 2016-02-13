import numpy as np
import argparse
import cv2

def nothing(x):
	pass

img = cv2.imread('Software/Vision/Images/2016-01-23 16-06-42.285.jpg', cv2.IMREAD_UNCHANGED)
if img is None:
	print("Image not found")
	exit(1)
cv2.namedWindow('image')

cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

original = img[:]
while(1):
	cv2.imshow('image', img)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

	r = cv2.getTrackbarPos('R', 'image')
	g = cv2.getTrackbarPos('G', 'image')
	b = cv2.getTrackbarPos('B', 'image')
	s = cv2.getTrackbarPos(switch,'image')

	if s == 0:
		img[:] = original
		pass
	else:
		img[:] = fn(original, r, g, b)
		pass

cv2.destroyAllWindows()