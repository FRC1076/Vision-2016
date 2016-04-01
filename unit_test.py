import cv2
import logging
from time import sleep
from image_grabber import ImageGrabber

logging.basicConfig(level=logging.INFO,filename="/var/log/vision.log")
logger = logging.getLogger(__name__)

def test_image_grabber():
    """
    This is just a photo-booth type of demo
    It does not really pass/fail.  You need to check
    in the folder and see if it captures 4 or 5 images.
    And that it writes to the log file.
    INFO:unit_test:Call 5: captured image to camera_capture_001.jpg, result was [Result is 4]
    INFO:unit_test:Call 10: captured image to camera_capture_002.jpg, result was [Result is 9]
    INFO:unit_test:Call 15: captured image to camera_capture_003.jpg, result was [Result is 14]
    INFO:unit_test:Call 20: captured image to camera_capture_004.jpg, result was [Result is 19]
    """
    cap = cv2.VideoCapture(-1)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320);
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240);
    cap.set(cv2.cv.CV_CAP_PROP_FPS, 30)

    ig = ImageGrabber(logger, 5, 5)

    for i in range(40):
        # get an image
        ret, frame = cap.read()

        result = "Result is {:d}".format(i)
        ig.grab(frame, result)

        sleep(1)



    
