from Previewer import Previewer
from FrameReader import FrameReader

import cv2
try:
    from  Queue import  Queue
except ModuleNotFoundError:
    from  queue import  Queue


class Camera(object):
    frame_reader = None
    cap = None
    previewer = None
    width = None
    height = None
    
    # Initialize camera object
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.open_camera()
        
    def gstreamer_pipeline(capture_width=1280, capture_height=720, display_width=640, display_height=360,
        framerate=60, flip_method=0):
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
                    capture_width,
                    capture_height,
                    framerate,
                    flip_method,
                    display_width,
                    display_height,
                )
            )

    # Start camera
    def open_camera(self):
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(flip_method=0, display_width=self.width, display_height=self.height), cv2.CAP_GSTREAMER)
        
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera!")
        
        if self.frame_reader == None:
            self.frame_reader = FrameReader(self.cap, "")
            self.frame_reader.daemon = True
            self.frame_reader.start()
            
        self.previewer = Previewer(self.frame_reader, "")

    def getFrame(self, timeout = None):
        return self.frame_reader.getFrame(timeout)

    def start_preview(self):
        self.previewer.daemon = True
        self.previewer.start_preview()

    def stop_preview(self):
        self.previewer.stop_preview()
        self.previewer.join()
    
    def close(self):
        self.frame_reader.stop()
        self.cap.release()