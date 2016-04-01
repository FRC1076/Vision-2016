from __future__ import print_function

import cv2
import logging

class ImageGrabber:
    def __init__(self, logger, grab_period=5, grab_limit=100):
        """
        Create a image grabber that grabs an image every
        grab_period calls.   Default is every 5th call.
        
        Usage:

        ig = ImageGrabber(logger, grab_period=5, grab_limit=50)

        while 1:
            ret, frame = cap.read()    # get image, for example

            process_image_to_extract_info(frame)

            if appropriate_to_grab:
                ig.grab(frame,log_message)
        """
        self.logger = logger
        self.grab_period=grab_period
        self.grab_limit=grab_limit
        self.file_index = 1
        self.call_index = 0

    def grab(self, image, log_result=None):
        """
        Export an image to a file every "period" calls.
        Log the filename and a message.  (with some result?)
        """
        self.call_index += 1
        if ((self.file_index < self.grab_limit) and
            (self.call_index % self.grab_period) == 0):
            filename = "camera_capture_{:03d}.jpg".format(self.file_index)
            cv2.imwrite(filename, image)
            if self.logger is not None:
                self.logger.info("Call %d: captured image to %s, result was [%s]",self.call_index,filename,log_result)
            self.file_index += 1
            
            
        
