import sys

import cv2
import numpy as np

#Get the reference contour from the image
def ref_contour(image):
    ref_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Change threshold if it's not finding correct contour or finding too many
    ret, thresh = cv2.threshold(ref_gray, 127, 255, 0)
    #Find all contours in image (within threshold)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    #Get required contour using an area ratio, ensuring only getting the non image
    #boundary contours
    for contour in contours:
        area = cv2.contourArea(contour)
        img_area = image.shape[0] * image.shape[1]
        if(0.05 < area/float(img_area) < 0.8):
            return contour
    #Get all contours
def get_contours(image):
    ref_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(ref_gray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1,2)
    return contours
if __name__ == '__main__' :
    #Reference image
    image1 = cv2.imread(sys.argv[1])
    #Image to look for spring within
    image2 = cv2.imread(sys.argv[2])
    #Get reference contour
    ref_contour = ref_contour(image1)
    #Get the reference contours from the spring image
    input_contours = get_contours(image2)

    closest_contour = input_contours[0]
    min_dist = sys.maxint
    #Finding the closest contour
    for contour in input_contours:
        #Looking 4 the closest shape
        ret = cv2.matchShapes(ref_contour, contour, 1, 0.0)
        if ret < min_dist:
            min_dist = ret
            closest_contour = contour
    cv2.drawContours(image2, [closest_contour], -1, (0,0,0), 3)
    cv2.imshow('Output', image2)
    cv2.waitKey()

