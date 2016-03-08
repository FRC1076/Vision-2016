from __future__ import division

import cv2
import numpy as np

# different image files to load for testing
images = [
    '2016 Test.jpg',
    '2016-01-23 15-50-41.261.jpg',
    '2016-01-23 15-51-32.997.jpg',
    '2016-01-23 16-00-17.509.jpg',
    '2016-01-23 16-00-41.869.jpg',
    '2016-01-23 16-03-04.461.jpg',
    '2016-01-23 16-03-30.212.jpg',
    '2016-01-23 16-04-55.181.jpg',
    '2016-01-23 16-05-11.179.jpg',
    '2016-01-23 16-05-26.825.jpg',
    '2016-01-23 16-06-42.285.jpg',
    '2016-01-23 16-07-07.969.jpg',
    '2016-01-23 16-07-23.035.jpg',
    '2016-01-23 16-09-25.260.jpg',
    '2016-01-23 16-09-52.884.jpg',
    '2016-01-23 16-10-06.156.jpg',
    '2016-01-23 16-11-41.644.jpg',
    '2016-01-23 16-11-59.575.jpg',
    '2016-01-23 16-12-11.103.jpg',
    'GreenTape1.png',
]
images = ['../Images/' + img for img in images]

img = cv2.imread(images[6],cv2.IMREAD_COLOR) # loads the image file

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converts images from BGR to hsv

# range of HSV color values
lower_green = np.array([75,70,70])
upper_green = np.array([95,255,255])

mask = cv2.inRange(hsv, lower_green, upper_green) # creates a grayscale image using the above range of values
cv2.imshow('initial', mask)

kernel = np.ones((3,3),np.uint8)
# erodes and dilates the image
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
# dilates and erodes the image
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
cv2.imshow('final', mask)

res = cv2.bitwise_and(img, img, mask = mask) # uses mask to create a color image within the range values

edges = cv2.Canny(mask,100,200) # creates a grayscale image of just the edges of shape

# finds contours
imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

def distance_between_points(p1, p2):
    x1, y1 = p1[0]
    x2, y2 = p2[0]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# finds the squared distance to point
def sq_distance_to_point(x0, y0):
    def distance(pt):
        x, y = pt[0]
        dx, dy = x - x0, y - y0
        return dx*dx + dy*dy
    return distance

# finds the midpoint of 2 points
def midpoint(p1, p2):
    x1, y1 = p1[0]
    x2, y2 = p2[0]
    return (x1 + x2)/2, (y1 + y2)/2

def area(cnt):
    return cv2.contourArea(cnt)

def perimeter(cnt):
    return cv2.actLength(cnt,True)

def five_eighths_test(cnt, img):
    # finds the diagonal extreme of the contour
    upper_left = min(cnt, key=sq_distance_to_point(0, 0))
    upper_right = min(cnt, key=sq_distance_to_point(640, 0))
    bottom_left = min(cnt, key=sq_distance_to_point(0, 480))
    bottom_right = min(cnt, key=sq_distance_to_point(640, 480))

    # finds height of the U
    left_height = distance_between_points(upper_left, bottom_left)
    right_height = distance_between_points(upper_right, bottom_right)
    height = (left_height + right_height)/2

    # finds the midpoint
    upper_mid = midpoint(upper_left, upper_right)
    # unpacks the x, y values of the midpoint
    midX, midY = upper_mid

    testX = midX
    testY = midY + (5/8)*height
    testpoint = testX, testY
    return (img[midY:testY, testX] == 0).all()

def area_test(cnt):
    return 400 < area(cnt) < 2500

#print len(contours)
for contour in contours:
    if five_eighths_test(contour, mask) and area_test(contour):
        label_point = min(contour, key=sq_distance_to_point(640, 480))
        labelX, labelY = label_point[0]
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(edges,"True",(labelX,labelY), font, 1.0, (255,255,255), 1, False)

def slope_test(cnt, img, width, height):
    # finds the diagonal extreme of the contour
    upper_left = min(cnt, key=sq_distance_to_point(0, 0))
    upper_right = min(cnt, key=sq_distance_to_point(width, 0))
    bottom_left = min(cnt, key=sq_distance_to_point(0, height))
    bottom_right = min(cnt, key=sq_distance_to_point(width, height))

    # finds half the width of the tape
    left_height = distance_between_points(upper_left, bottom_left)
    right_height = distance_between_points(upper_right, bottom_right)
    if left_height > right_height:
        height = 0.0833333333*left_height
    else:
        height = 0.0833333333*right_height

    #finds the slope of the bottom points
    bottom_leftX, bottom_leftY = bottom_left[0]
    bottom_rightX, bottom_rightY = bottom_right[0]
    slope = (bottom_leftY - bottom_rightY)/(bottom_leftX - bottom_rightX)

    test_point = bottom_leftX + height, bottom_leftY - height
    testX, testY = test_point
    final_point = bottom_rightX - height, bottom_rightY - height
    finalX, finalY = final_point

    width = finalX - testX
    lower_slope_tests = [False]*width
    count = 0
    while count < width - 1:
        lower_slope_tests[count] = img[slope*count + testY, testX + count] > 0
        count += 1

    tolerance = width*0.1
    count = 0
    bad_data = 0
    while count < width - 1:
        if not lower_slope_tests[count]:
            bad_data += 1
        count += 1
    if bad_data < tolerance:
        return True
    return False

def empty_test(cnt, img, width, height):
    # finds the diagonal extreme of the contour
    upper_left = min(cnt, key=sq_distance_to_point(0, 0))
    upper_right = min(cnt, key=sq_distance_to_point(width, 0))
    bottom_left = min(cnt, key=sq_distance_to_point(0, height))
    bottom_right = min(cnt, key=sq_distance_to_point(width, height))

    # finds half the width of the tape
    left_height = distance_between_points(upper_left, bottom_left)
    right_height = distance_between_points(upper_right, bottom_right)
    if left_height > right_height:
        height = 0.0833333333*left_height
    else:
        height = 0.0833333333*right_height

    #finds the slope of the bottom points
    bottom_leftX, bottom_leftY = bottom_left[0]
    bottom_rightX, bottom_rightY = bottom_right[0]
    slope = (bottom_leftY - bottom_rightY)/(bottom_leftX - bottom_rightX)

    test_point = bottom_leftX + height, bottom_leftY - height
    testX, testY = test_point
    print test_point
    print img[testY, testX]

    test_point = bottom_leftX + 3*height, bottom_leftY - 3*height
    testX, testY = test_point
    final_point = bottom_rightX - 3*height, bottom_rightY - 3*height
    finalX, finalY = final_point

    width = finalX - testX

    # finds height of the U
    left_height = distance_between_points(upper_left, bottom_left)
    right_height = distance_between_points(upper_right, bottom_right)
    U_height = (5/8)*(left_height + right_height)/2

    test_pixels = [False]*(width*U_height)

    place = 0
    while place < (width-1)*U_height:
        X = 0
        Y = 0
        while X < width - 1:
            mask[slope*X + testY - Y, testX + X] = 1
            test_pixels[place] = img[slope*X + testY - Y, testX + X] == 0
            X += 1
            place += 1
        Y += 1
    return test_pixels

cnt = contours[1] # assigns a specific contour to be the U (should be replaced by contour test)

empty_test(cnt, mask, 640, 480)

# finds the diagonal extreme of the contour
upper_left = min(cnt, key=sq_distance_to_point(0, 0))
upper_right = min(cnt, key=sq_distance_to_point(640, 0))
bottom_left = min(cnt, key=sq_distance_to_point(0, 480))
bottom_right = min(cnt, key=sq_distance_to_point(640, 480))

midpoint = midpoint(upper_left, upper_right) # finds the midpoint
midX, midY = midpoint # unpacks the x, y values of the midpoint

M = cv2.moments(cnt) # finds moments of the contour
area = cv2.contourArea(cnt) # finds the area of the contour
perimeter = cv2.arcLength(cnt,True) # finds the perimeter of the contour

# outputs different images
cv2.imshow('image',img)
cv2.imshow('mask', mask)
cv2.imshow('edges', edges)

# waits for the ESc key to exit
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
