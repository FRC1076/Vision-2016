import cv2
import numpy as np

# Capture video frame
def get_frame(cap, scaling_factor = 0.5):
    ret, frame = cap.read()
    # Resize frame
    frame = cv2.resize(frame, None, fx= scaling_factor, fy=scaling_factor, interpolation= cv2.INTER_AREA)
    return frame

if __name__ == '__main__':
    # Create video cap
    cap = cv2.VideoCapture(0)
    # Create the background subtractor object
    bgSub = cv2.BackgroundSubtractorMOG()
    # Learning rate (higher value = shower learning rate)
    history = 100
    # Stop when escape is pressed
    while True:
        frame = get_frame(cap, 0.5)
        # Subtract from input using background
        mask = bgSub.apply(frame, learningRate=1.0/history)
        # Convert from gray to BGR
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.imshow("Video (original)", frame)
        cv2.imshow("Filtered", mask & frame)
        # Scan for escape pressing
        c= cv2.waitKey(10)
        if c==27:
            break
    cap.release()
    cv2.destroyAllWindows()