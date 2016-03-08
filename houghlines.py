import cv2
import numpy as np

img = cv2.imread('Images/2016-01-23 16-06-42.285.jpg',cv2.IMREAD_UNCHANGED)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([75,70,70])
upper_green = np.array([95,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green)

res = cv2.bitwise_and(img, img, mask = mask)

edges = cv2.Canny(mask,100,200)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imshow('edges', edges)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img)
    cv2.destroyAllWindows()
minLineLength = 5
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines6.jpg',img)
