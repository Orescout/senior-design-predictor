from ChainLinkDetector import ChainLinkDetector
from Processor import Processor
from JsonConstructor import JsonConstructor
from Camera import Camera


import cv2

# PART 0: INITIALIZATION (outside of loop - happens once)
detector = ChainLinkDetector(model="yoloV5_model_medium.pt")
camera = Camera()

# PART I: CAMERA

# Take a photo
camera.

# Store the photo



# PART II: PROCESSING

# Read the photo
image = cv2.imread("image.png")

# Use YOLO to get locations of chain links
bounding_boxes = detector.detect_chainlinks(image, preview=True, save=False)

# Process bounding boxes to get valuable information
processor = Processor(image, bounding_boxes)
chain_direction_o_clock = processor.estimate_chain_direction(preview=True, save=False)
number_of_chainlinks = processor.get_number_of_chainlinks()


# PART III: SEND DATA

# Prep JSON to send
JSON = JsonConstructor(number_of_chainlinks, chain_direction_o_clock).get_json(printit=True)

# Send data
# TODO: Send data to JD.

print("---------------------------------------- Completed.")