# Inspired from https://github.com/ArduCAM/Jetson_IMX519_Focus_Example/blob/master/JetsonCamera.py

from Previewer import Previewer
from FrameReader import FrameReader

from PIL import Image
import cv2
import os
import datetime
try:
    from  Queue import  Queue
except ModuleNotFoundError:
    from  queue import  Queue


class Camera(object):
    frame_reader = None
    cap = None
    previewer = None
    capture_width = None
    capture_height = None
    framerate = None
    flip_method = None
    display_width = None
    display_height = None
    
    # Initialize camera object
    def __init__(self, capture_width=1280, capture_height=720, display_width=640, display_height=360,
                 framerate=60, flip_method=0):
        self.capture_width = capture_width
        self.capture_height = capture_height
        self.framerate = framerate
        self.flip_method = flip_method
        self.display_width = display_width
        self.display_height = display_height
        self.open_camera()
        
    def gstreamer_pipeline(self):
        return (
                "nvarguscamerasrc ! "
                "video/x-raw(memory:NVMM), "
                "width=(int)%d, height=(int)%d, "
                "format=(string)NV12, framerate=(fraction)%d/1 ! "
                "nvvidconv flip-method=%d ! "
                "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
                "videoconvert ! "
                "video/x-raw, format=(string)BGR ! appsink"
                % (
                    self.capture_width,
                    self.capture_height,
                    self.framerate,
                    self.flip_method,
                    self.display_width,
                    self.display_height,
                )
            )

    # Start camera
    def open_camera(self):
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera!")
        
        print("Camera ON: ", self.cap)
        
        if self.frame_reader == None:
            self.frame_reader = FrameReader(self.cap, "")
            self.frame_reader.daemon = True
            self.frame_reader.start()
            
        self.previewer = Previewer(self.frame_reader, "")

    def getFrame(self, preview=False, save=False, timeout=None):
        # Capture the photo
        image = self.frame_reader.getFrame(timeout)
        
        # Save image
        current_date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = f"{os.getcwd()}/data_raw_camera/{current_date_time}.png"
        cv2.imwrite(output_path, image)
        
        # Display image
        if preview:
            img = Image.open(output_path)
            img.show()
        
        # If we don't want to save, delete
        if not save:
            os.remove(output_path)
        
        return image

    def start_preview(self):
        self.previewer.daemon = True
        self.previewer.start_preview()

    def stop_preview(self):
        self.previewer.stop_preview()
        self.previewer.join()
    
    def close(self):
        self.frame_reader.stop()
        self.cap.release()
