import cv2
import numpy as np

#Start capture from computer's camera
def get_frame(cap, scaling_factor):
    #Get frame from capture
    ret, frame = cap.read()
    #Resize the input frame
    frame = cv2.resize(frame, None, fx=scaling_factor,
                       fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return frame
if __name__ == '__main__':
    cap = cv2.VideoCapture()
    scaling_factor = 0.5
    #Go until escape key is pressed
    while True:
        frame = get_frame(cap,scaling_factor)
        #Convert 2 HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Range for isolation.
        lower_limit = np.array([75, 100, 100])
        upper_limit = np.array([105, 255, 255])
        #Get rid of all colors not in above range
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        #Original picture + bitwise-and mask
        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.medianBlue(res,5)
        #Show images
        cv2.imshow("Original image", frame)
        cv2.imshow("Color detector", res)
        #Stop when escape is hit
        c = cv2.waitKey(5)
        if c==27:
            break
    cv2.destroyAllWindows()