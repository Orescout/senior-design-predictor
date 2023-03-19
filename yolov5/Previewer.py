import cv2
import time
try:
    from  Queue import  Queue
except ModuleNotFoundError:
    from  queue import  Queue

import  threading

class Previewer(threading.Thread):
    window_name = "PopeEye Live Camera Feed"
    _running = True
    camera = None
    def __init__(self, camera, name):
        threading.Thread.__init__(self)
        self.name = name
        self.camera = camera
    
    def run(self):
        self._running = True
        while self._running:
            cv2.imshow(self.window_name, self.camera.getFrame(2000))
            keyCode = cv2.waitKey(16) & 0xFF
        cv2.destroyWindow(self.window_name)

    def start_preview(self):
        self.start()
    def stop_preview(self):
        self._running = False