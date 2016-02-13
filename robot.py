import cv2
import numpy as np

# different image files to load for testing
images = [""]*20
images[0] = 'Software/Vision/Images/2016 Test.jpg'
images[1] = 'Software/Vision/Images/2016-01-23 15-50-41.261.jpg'
images[2] = 'Software/Vision/Images/2016-01-23 15-51-32.997.jpg'
images[3] = 'Software/Vision/Images/2016-01-23 16-00-17.509.jpg'
images[4] = 'Software/Vision/Images/2016-01-23 16-00-41.869.jpg'
images[5] = 'Software/Vision/Images/2016-01-23 16-03-04.461.jpg'
images[6] = 'Software/Vision/Images/2016-01-23 16-03-30.212.jpg'
images[7] = 'Software/Vision/Images/2016-01-23 16-04-55.181.jpg'
images[8] = 'Software/Vision/Images/2016-01-23 16-05-11.179.jpg'
images[9] = 'Software/Vision/Images/2016-01-23 16-05-26.825.jpg'
images[10] = 'Software/Vision/Images/2016-01-23 16-06-42.285.jpg'
images[11] = 'Software/Vision/Images/2016-01-23 16-07-07.969.jpg'
images[12] = 'Software/Vision/Images/2016-01-23 16-07-23.035.jpg'
images[13] = 'Software/Vision/Images/2016-01-23 16-09-25.260.jpg'
images[14] = 'Software/Vision/Images/2016-01-23 16-09-52.884.jpg'
images[15] = 'Software/Vision/Images/2016-01-23 16-10-06.156.jpg'
images[16] = 'Software/Vision/Images/2016-01-23 16-11-41.644.jpg'
images[17] = 'Software/Vision/Images/2016-01-23 16-11-59.575.jpg'
images[18] = 'Software/Vision/Images/2016-01-23 16-12-11.103.jpg'
images[19] = 'Software/Vision/Images/GreenTape1.png'

img = cv2.imread(images[6],cv2.IMREAD_COLOR) #loads the image file

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #converts images from BGR to hsv

#range of HSV color values
lower_green = np.array([75,70,70])
upper_green = np.array([95,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green) #creates a grayscale image using the above range of values

res = cv2.bitwise_and(img, img, mask = mask) #uses mask to create a color image within the range values

edges = cv2.Canny(mask,100,200) #creates a grayscale image of just the edges of shape

#finds contours
imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#finds the squared distance to point
def sq_distance_to_point(x0, y0):
	def distance(pt):
		x, y = pt[0]
		dx, dy = x - x0, y - y0
		return dx*dx + dy*dy
	return distance

#finds the midpoint of 2 points
def midpoint(p1, p2):
	x1, y1 = p1[0]
	x2, y2 = p2[0]
	return (x1 + x2)/2, (y1 + y2)/2

cnt = contours[0] #assigns a specific contour to be the U (should be replaced by contour test)

#finds the extreme corners of the contour
upper_left = min(cnt, key=sq_distance_to_point(0, 0))
upper_right = min(cnt, key=sq_distance_to_point(640, 0))
bottom_left = min(cnt, key=sq_distance_to_point(0, 480))
bottom_right = min(cnt, key=sq_distance_to_point(640, 480))

midpoint = midpoint(upper_left, upper_right) #finds the midpoint
midX, midY = midpoint #unpacks the x, y values of the midpoint

M = cv2.moments(cnt) #finds moments of the contour
area = cv2.contourArea(cnt) #finds the area of the contour
perimeter = cv2.arcLength(cnt,True) #finds the perimeter of the contour
ratio = perimeter*perimeter / area #finds the ratio of perimeter squared to area

#outputs different images
cv2.imshow('image',img)
cv2.imshow('mask', mask)
cv2.imshow('edges', edges)

#waits for the ESc key to exit
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
