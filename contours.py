import numpy as np
import cv2

img = cv2.imread('Software/Vision/Images/2016-01-23 16-05-26.825.jpg',cv2.IMREAD_COLOR)
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contours, -1, (0,255,0), 3)
cnt = contours[0]
M = cv2.moments(cnt)
#print M
area = cv2.contourArea(cnt)
print area
cv2.imshow('image',img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([75,70,70])
upper_green = np.array([95,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green)

res = cv2.bitwise_and(img, img, mask = mask)

edges = cv2.Canny(mask,100,200)
cv2.imshow('edges', edges)