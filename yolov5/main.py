from ChainLinkDetector import ChainLinkDetector
from Processor import Processor
from JsonConstructor import JsonConstructor
from Camera import Camera
from Communicator import Communicator

import os
import argparse
import cv2
import keyboard
import threading

def key_listener():
    global keyboard_exit_pressed
    keyboard.wait('any')
    keyboard_exit_pressed = True
    print("Keyboard key was pressed. Stopping program.")

def main():
    
    # PART 0: INITIALIZATION (outside of loop - happens once at start)
    detector = ChainLinkDetector(model="yoloV5_model_medium.pt", window_size=(300, 300))
    camera = Camera()
    communicator = Communicator()

    try:
        monitor_loop(detector, camera, communicator)

    except Exception as e:
        print("Something went wrong: ", e)

    finally:
        # PART FINALE: WINDING THINGS DOWN (outside of loop - happens once at end)
        camera.close()
        print("---------------------------------------- ALL COMPLETED.")


def monitor_loop(detector, camera, communicator):
    for i in range(10):
        print("--------------------------------------------")
        print("                                            ")

        # Check if keyboard command to exit has been entered. Then exit loop.
        if keyboard_exit_pressed:
            break
        
        # Creating default values for data to send
        number_of_chainlinks = 0
        chain_direction_oclock = -1

        # PART I: CAMERA
    
        # Take a photo
        image = camera.getFrame(save=True)
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # Replace photo, for debugging purposes (when you don't have a chain)
        # image = cv2.imread("image.png")
        print(image.shape) # (618, 480, 3)
        print("1/3 Done (Taking a photo from camera)")

        if image is None:
            print("Image was not read properly.")
            continue
        else:
            # PART II: PROCESSING

            # Use YOLO to get locations of chain links
            bounding_boxes = detector.detect_chainlinks(image, preview=True, save=True)
            print('bounding box: ', bounding_boxes)
            
            if bounding_boxes.shape[0] > 2:
                # Process bounding boxes to get valuable information
                processor = Processor(image, bounding_boxes)
                chain_direction_oclock = processor.estimate_chain_direction(preview=False, save=True)
                number_of_chainlinks = processor.get_number_of_chainlinks()
                print("2/3 Done (Processing photo)")


        # PART III: SEND DATA

        # Prep JSON to send
        # JSON = JsonConstructor(number_of_chainlinks, chain_direction_oclock).get_json(printit=True)

        # Send data
        msg = "Ylinks: " + str(number_of_chainlinks)
        communicator.send(msg)
        print("3/3 Done (Sending JSON data to LoRa)")


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Take pictures, process and send data")
    parser.add_argument('--arg1', type=int, help='description of arg1')
    args = parser.parse_args()
    

    # Set flag for stopping program
    keyboard_exit_pressed = False
    # Call main function
    os.chdir("/home/nvidia/Desktop/senior-design-predictor/yolov5/")
    main()
