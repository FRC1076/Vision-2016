import cv2
import numpy as np

img = cv2.imread('Software/Vision/Images/2016-01-23 15-51-32.997.jpg',cv2.IMREAD_COLOR)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([75,70,70])
upper_green = np.array([95,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green)

res = cv2.bitwise_and(img, img, mask = mask)

#se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
#se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
#mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se1)
#mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

#mask = np.dstack([mask, mask, mask]) / 255
#out = img * mask
kernel = np.ones((5,5),np.uint8)

opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

edges = cv2.Canny(mask,100,200)
cv2.imshow('image',img)
cv2.imshow('mask', mask)
cv2.imshow('res', res)
#cv2.imshow('out', out)
cv2.imshow('edges', edges)
imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(res, contours, -1, (0,255,0), 3)
def sq_distance_to_point(x0, y0):
	def distance(pt):
		x, y = pt[0]
		dx, dy = x - x0, y - y0
		return dx*dx + dy*dy
	return distance

def midpoint(p1, p2):
	print p1
	x1, y1 = p1[0]
	x2, y2 = p2[0]
	return (x1 + x2)/2, (y1 + y2)/2

cnt = contours[0]
upper_left = min(cnt, key=sq_distance_to_point(0, 0))
upper_right = min(cnt, key=sq_distance_to_point(640, 0))
bottom_left = min(cnt, key=sq_distance_to_point(0, 480))
bottom_right = min(cnt, key=sq_distance_to_point(640, 480))
midpoint = midpoint(upper_left, upper_right)
midX, midY = midpoint
#print midX
#print midY
#print midpoint
#print upper_left
#print upper_right
#print bottom_left
#print bottom_right
#print len(contours)
#print cnt
M = cv2.moments(cnt)
#print M
area = cv2.contourArea(cnt)
print area
perimeter = cv2.arcLength(cnt,True)
#print perimeter

ratio = perimeter * perimeter / area
#print ratio

dst = cv2.cornerHarris(mask,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.5*dst.max()]=[0,0,255]
cv2.imshow('dst', img)
cv2.imshow('opening', opening)
cv2.imshow('closing', closing)
#print dst
#cv2.imshow('dst',img)

#leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
#rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
#topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
#bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

#print leftmost
#print rightmost
#print topmost
#print bottommost

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img)
    cv2.destroyAllWindows()