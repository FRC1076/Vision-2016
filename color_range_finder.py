import sys
import numpy as np
import cv2

# This is a simple program to return a range of HSV color values from a set
# of BGR color values that can be used as a range to isolate a certain color
# (like retroreflective tape)
blue = int(input("What is the blue value? "))
green = int(input("What is the green value? "))
red = int(input("What is the red value? "))

color = np.uint8([[[blue, green, red]]])
hsv_from_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
hue = hsv_from_color[0][0][0]

print("Lower: " + str(hue - 15) + ", 100, 100")
print("Upper: " + str(hue + 15) + ", 255, 255")