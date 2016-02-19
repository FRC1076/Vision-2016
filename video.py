from __future__ import division

import numpy as np
import cv2
import sys
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FIELD_OF_VIEW = 65

# finds the distance between 2 points
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

# finds the area of a contour
def area(cnt):
    return cv2.contourArea(cnt)

# finds the perimeter of a contour
def perimeter(cnt):
    return cv2.actLength(cnt, True)

# tests five eighths down the center of the object is not part 
# of the object, insuring it's a U shape
def five_eighths_test(cnt, img, width, height):
    # finds the diagonal extreme of the contour
    upper_left = min(cnt, key=sq_distance_to_point(0, 0))
    upper_right = min(cnt, key=sq_distance_to_point(width, 0))
    bottom_left = min(cnt, key=sq_distance_to_point(0, height))
    bottom_right = min(cnt, key=sq_distance_to_point(width, height))

    # finds height of the U
    left_height = distance_between_points(upper_left, bottom_left)
    right_height = distance_between_points(upper_right, bottom_right)
    height = (left_height + right_height)/2

    # finds the midpoint
    upper_mid = midpoint(upper_left, upper_right)
    # unpacks the x, y values of the midpoint
    midX, midY = upper_mid

    # actually tests each point along the five-eighths from the top line
    testX = midX
    testY = midY + 0.625*height
    testpoint = testX, testY
    return (img[midY:testY, testX] == 0).all()

# tests if the area of the contour is within 2 values
def area_test(cnt, width, height):
    return width*height*0.0001 < area(cnt) < width*height*0.015

# determines the degrees of the U off from the middle
def find_heading(cnt, width, height):
    # finds the diagonal extremes of the contour
    upper_left = min(cnt, key=sq_distance_to_point(0, 0))
    upper_right = min(cnt, key=sq_distance_to_point(width, 0))
    bottom_left = min(cnt, key=sq_distance_to_point(0, height))
    bottom_right = min(cnt, key=sq_distance_to_point(width, height))

    #finds the midpoint
    midpoint_upper = midpoint(upper_left, upper_right)
    midpoint_bottom = midpoint(bottom_left, bottom_right)
    upX, upY = midpoint_upper
    botX, botY = midpoint_bottom
    mid = (upX + botX)/2, (upY + botY)/2
    midX, midY = mid
    pixel_distance = midX - width/2
    return ((FIELD_OF_VIEW/2.0) * pixel_distance)/(width/2)

# determines the distance of the U from the robot in inches (NOTE!!! NOT ACCURATE)
def find_distance(cnt, width, height):
    # find the diagonal extremes of the contour
    upper_left = min(cnt, key=sq_distance_to_point(0, 0))
    upper_right = min(cnt, key=sq_distance_to_point(width, 0))
    bottom_left = min(cnt, key=sq_distance_to_point(0, height))
    bottom_right = min(cnt, key=sq_distance_to_point(width, height))

    # finds the left and right X values
    bottom_leftX, bottom_leftY = bottom_left[0]
    bottom_rightX, bottom_rightY = bottom_right[0]
    if bottom_leftY > bottom_rightY:
        pixel_height = bottom_leftY - bottom_rightY
    else:
        pixel_height = bottom_rightY - bottom_leftY
    pixel_width = abs(bottom_rightX - bottom_leftX)
    pixel_distance = (pixel_width**2 + pixel_height**2)**0.5
    return ((17.25/(pixel_distance/width))**2 - 6724)**0.5

#sets the video capture
cap = cv2.VideoCapture(0)

while True:
    # captures each frame individually
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # converts frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # range of HSV color values
    lower_green = np.array([75, 70, 70])
    upper_green = np.array([95, 255, 255])

    # creates a grayscale image using the above range of values
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # sets the dilation and erosion factor
    kernel = np.ones((3,3),np.uint8)
    # erodes and dilates the image
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # dilates and erodes the image
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # uses mask to create a color image within the range values
    res = cv2.bitwise_and(frame, frame, mask = mask)

    # creates a grayscale image of just the edges of shape
    edges = cv2.Canny(mask, 100, 200)

    # finds contours
    imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sets up UDP sender
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = '172.16.1.227'
    port = 5880
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # tests the contours and determines which ones are U's
    num_of_contours = len(contours)
    shapes = [False]*num_of_contours
    count = 0
    for contour in contours:
        passes_five_eighths = five_eighths_test(contour, mask, width, height)
        passes_area = area_test(contour, width, height)
        if passes_five_eighths and passes_area:
            shapes[count] = True
        count += 1
    num_of_U = 0
    x_values = [0]*num_of_contours
    for shape in shapes:
        if shape:
            num_of_U += 1
    count = 0
    if num_of_U > 1:
        for contour in contours:
            coordinate = min(contour, key=sq_distance_to_point(0, height))
            x_coor, y_coor = coordinate[0]
            if shapes[count]:
                x_values[count] = x_coor
            else:
                x_values[count] = 10000
            count += 1
    x_values.sort()
    targetX = x_values[0]
    count = 0
    for contour in contours:
        passes_five_eighths = five_eighths_test(contour, mask, width, height)
        passes_area = area_test(contour, width, height)
        logger.debug("5/8 %s", passes_five_eighths)
        logger.debug("Area: %s", passes_area)
        logger.debug("Area: %f", area(contour))
        if passes_five_eighths and passes_area:
            logger.debug("True")
            shapes[count] = True
            label_point = min(contour, key=sq_distance_to_point(width, height))
            labelX, labelY = label_point[0]
            heading = find_heading(contour, width, height)
            distance = find_distance(contour, width, height)
            if num_of_U == 0:
                message = "VStatus=NO TARGET"
            elif num_of_U == 1:
                font = cv2.FONT_HERSHEY_PLAIN
                status = "OK"
                message = "VTD={:.02f}, VTH={:.02f}, VStatus=".format(distance, heading) + status
            elif num_of_U == 2:
                font = cv2.FONT_HERSHEY_PLAIN
                coordinate = min(contour, key=sq_distance_to_point(0, height))
                x_coor, y_coor = coordinate[0]
                if targetX == x_coor:
                    status = "LEFT"
                else:
                    status = "RIGHT"
                message = "VTD={:.02f}, VTH={:.02f}, VStatus=".format(distance, heading) + status
            else:
                message = "VStatus=TOO MANY TARGETS"
            sock.sendto(message, (ip, port))
            cv2.putText(edges, message, (labelX, labelY), font, 1.0, (255, 255, 255), 1, False)
        count += 1

    # displays the frame with labels
    cv2.imshow('edges', edges)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
        break