import cv2
import time
try:
    from  Queue import  Queue
except ModuleNotFoundError:
    from  queue import  Queue

import  threading

class FrameReader(threading.Thread):
    queues = []
    _running = True
    camera = None
    def __init__(self, camera, name):
        threading.Thread.__init__(self)
        self.name = name
        self.camera = camera
 
    def run(self):
        while self._running:
            _, frame = self.camera.read()
            while self.queues:
                queue = self.queues.pop()
                queue.put(frame)
    
    def addQueue(self, queue):
        self.queues.append(queue)

    def getFrame(self, timeout = None):
        queue = Queue(1)
        self.addQueue(queue)
        return queue.get(timeout = timeout)

    def stop(self):
        self._running = False