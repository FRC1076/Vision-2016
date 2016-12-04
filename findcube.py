# Code to find Cube for the WAPUR challenge and send range and heading information via UDP
# python findcube.py 127.0.0.1 interactive

from __future__ import division

import numpy as np
import cv2
import sys
import logging
import time
import colorsys
import json
import socket
from udp_channels import UDPChannel
from sensor_message import RobotMessage, RobotTargetMessage
from image_grabber import ImageGrabber


grabbing = False
tx_udp = True
if "interactive" in sys.argv:
    im_show = True
    sliders = True
    printer = True
    wait = False
else:
    im_show = False
    sliders = False
    printer = False
    wait = False

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s',filename="/var/log/vision.log")
logger = logging.getLogger(__name__)

grabber = ImageGrabber(logger, grab_period=1, grab_limit=1300)

lower_h = 61
lower_s = 20
lower_v = 0
upper_h = 69
upper_s = 217
upper_v = 255


FIELD_OF_VIEW = 65
fps_stats = []

# finds the distance between 2 points
def distance_between_points(p1, p2):
    x1, y1 = p1[0]
    x2, y2 = p2[0]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
  
def distance_to_point(x0, y0):
    def distance(pt):
        x, y = pt[0]
        dx, dy = x - x0, y - y0
        return (dx*dx + dy*dy)**0.5;
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

# tests if the area of the contour is within 2 values
def area_test(cnt, width, height):
    #return width*height*0.005 < area(cnt) < width*height*0.02
    return area(cnt) > MIN_AREA

def aspect_ratio(cnt):
    # finds the diagonal extreme of the contour
    upper_left = min(cnt, key=distance_to_point(0, 0))
    upper_right = min(cnt, key=distance_to_point(width, 0))
    bottom_left = min(cnt, key=distance_to_point(0, height))
    bottom_right = min(cnt, key=distance_to_point(width, height))
    avg_height = (bottom_left[0][1] - upper_left[0][1] + bottom_right[0][1] - upper_right[0][1])/2
    avg_width  = (upper_right[0][0] - upper_left[0][0] + bottom_right[0][0] - bottom_left[0][0])/2
    #print "aspect_ratio:", avg_height, avg_width, avg_height / avg_width;
    #print cnt
    if avg_width <> 0:
        return abs(avg_height / avg_width)
    else:
        return 0
 
# determines the degrees of the cube off from the middle
def find_heading(cnt, width, height):
    # finds the diagonal extremes of the contour
    upper_left = min(cnt, key=distance_to_point(0, 0))
    upper_right = min(cnt, key=distance_to_point(width, 0))
    bottom_left = min(cnt, key=distance_to_point(0, width))
    bottom_right = min(cnt, key=distance_to_point(width, height))

    #finds the midpoint
    midpoint_upper = midpoint(upper_left, upper_right)
    midpoint_bottom = midpoint(bottom_left, bottom_right)
    upX, upY = midpoint_upper
    botX, botY = midpoint_bottom
    mid = (upX + botX)/2, (upY + botY)/2
    midX, midY = mid
    pixel_distance = midX - width/2
    heading = ((FIELD_OF_VIEW/2.0) * pixel_distance)/(width/2)
    return int(heading)

# determines the distance of the cube from the robot in inches
# width is the number of pixels our image is wide
# height is the number of pixels our image is tall
# note the cube is 8x8x8 inches

def find_distance(cnt, width, height):
    # find the diagonal extremes of the contour
    upper_left = min(cnt, key=distance_to_point(0, 0))
    upper_right = min(cnt, key=distance_to_point(width, 0))
    bottom_left = min(cnt, key=distance_to_point(0, height))
    bottom_right = min(cnt, key=distance_to_point(width, height))

    # finds the left and right X values
    bottom_leftX, bottom_leftY = bottom_left[0]
    bottom_rightX, bottom_rightY = bottom_right[0]
    if bottom_leftY > bottom_rightY:
        pixel_height = bottom_leftY - bottom_rightY
    else:
        pixel_height = bottom_rightY - bottom_leftY
    pixel_width = abs(bottom_rightX - bottom_leftX)
    #FIELD_OF_VIEW = 65
    distance = 100
    if (distance >= 0 and distance < 9999):
        return int(distance)
    else:
        print "Fail find_distance:", pixel_height, pixel_width, pixel_distance, width, distance
        return 9999

def nothing(x):
    pass

# sets the video capture
cap = cv2.VideoCapture(-1)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320);
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240);
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)

if sliders:
    # creates slider windows
    lower = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('lower')
    upper = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('upper')

    # creates the rgb trackbars
    cv2.createTrackbar('H','lower',0,255,nothing)
    cv2.createTrackbar('S','lower',0,255,nothing)
    cv2.createTrackbar('V','lower',0,255,nothing)
    cv2.createTrackbar('H','upper',0,255,nothing)
    cv2.createTrackbar('S','upper',0,255,nothing)
    cv2.createTrackbar('V','upper',0,255,nothing)

    cv2.setTrackbarPos('H', 'lower', lower_h)
    cv2.setTrackbarPos('S', 'lower', lower_s)
    cv2.setTrackbarPos('V', 'lower', lower_v)
    cv2.setTrackbarPos('H', 'upper', upper_h)
    cv2.setTrackbarPos('S', 'upper', upper_s)
    cv2.setTrackbarPos('V', 'upper', upper_v)

# sets up UDP sender
if len(sys.argv) > 1:
   ip = sys.argv[1]
else:
   ip = '10.10.76.2'


channel = UDPChannel(remote_ip=ip, remote_port=5880,
                     local_ip='0.0.0.0', local_port=5888, timeout_in_seconds=0.001)

while (1):
    try:
        robot_data, robot_address = channel.receive_from()
        print("YIKES!",robot_data)
        message_from_robot = RobotMessage(robot_data)
        if ((message_from_robot.sender == 'robot') and
            (message_from_robot.message == 'target')):
            set_thresholds(message_from_robot.color)
            logger.info("Robot changed target color to %s",message_from_robot.color)
            logger.info("Start grabbing images NOW!")
            grabbing = True
    except socket.timeout as e:
        logger.info("Timed out waiting for color setting: %s",e)
        
    k = cv2.waitKey(10) & 0xFF
    if k == 27: # Exit when the escape key is hit
        break
    start_time = time.time()
    # captures each frame individually
    ret, frame = cap.read()
    frame = cv2.imread('cube-green.jpeg')
    height, width, channels = frame.shape

    if im_show:
        cv2.imshow('source', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # converts frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if sliders:
        # lower hsv values
        lower_h = cv2.getTrackbarPos('H','lower')
        lower_s = cv2.getTrackbarPos('S','lower')
        lower_v = cv2.getTrackbarPos('V','lower')

        # upper rgb values
        upper_h = cv2.getTrackbarPos('H','upper')
        upper_s = cv2.getTrackbarPos('S','upper')
        upper_v = cv2.getTrackbarPos('V','upper')

    # range of HSV color values
    lower_green = np.array([lower_h, lower_s, lower_v])
    upper_green = np.array([upper_h, upper_s, upper_v])

    # creates a bw image using the above range of values
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # sets the dilation and erosion factor
    kernel = np.ones((5,5),np.uint8)
    dots = np.ones((5,5),np.uint8)
    # erodes and dilates the image
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, dots)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, dots)
    # dilates and erodes the image
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    if im_show:
        cv2.imshow('inRange', mask)

    # uses mask to create a color image within the range values
    res = cv2.bitwise_and(frame, frame, mask = mask)

    # creates a grayscale image of just the edges of shape
    edges = cv2.Canny(mask, 100, 200)

    # finds contours
    imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 0, 255, 0)
    if im_show:
        cv2.imshow('thresh', thresh)
    cv2.waitKey(1)
    contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # tests the contours and determines which ones are cubes
    num_of_contours = len(contours)
    shapes = [False]*num_of_contours
    # fills in the boolean array of whether or not a shape is a U
    count = 0
    num_of_Cube = 0
    for contour in contours:
        count += 1
        is_aspect_ok = (0.7 < aspect_ratio(contour) < 3)
        is_area_ok = (2000 < cv2.contourArea(contour) < 20000)
        if (False == is_area_ok):
            print "Fail area:", cv2.contourArea(contour), "Contour:", count + 1, " of ", len(contours)
            continue;  # jump to bottom of for loop
        if (False == is_aspect_ok):
            print "Fail aspect ratio:", aspect_ratio(contour), "Contour:", count + 1, " of ", len(contours)
            continue;  # jump to bottom of for loop
        num_of_Cube += 1
         # transmit heading data
         # Find the heading of this cube
        heading = find_heading(contour, width, height)
        # determines the distance of this cube
        distance = find_distance(contour, width, height)
        data = {
           "sender" : "vision",
           "range" : distance,
           "heading" : heading,
           "message" : "range and heading",
           "status" : "ok",
        }
        message = json.dumps(data)
        # sends the message
        if tx_udp:
            channel.send_to(message)
            if printer:
                print "Tx:" + message
        logger.info(message)
    
    if num_of_Cube == 0:
        data = {
           "sender" : "vision",
           "message" : "range and heading",
           "status" : "no target",
        }
        message = json.dumps(data)
        if tx_udp:
            channel.send_to(message)
            if printer:
                print "Tx:" + message
            logging.info(message)
    if grabbing:
        grabber.grab(frame, message)

    time.sleep(.1)
    if wait:
        if not im_show:
            cv2.namedWindow('waitkey placeholder')
        k = cv2.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            break
