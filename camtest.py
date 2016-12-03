#import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480);
cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    # Display the resulting frame
    cv2.imshow('frame', frame)

	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

