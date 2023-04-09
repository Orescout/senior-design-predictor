import numpy as np
import cv2
import torch
import os
import sys
from contextlib import contextmanager
from PIL import Image
import datetime


class ChainLinkDetector:
    def __init__(self, model="yoloV5_model_medium.pt", window_size=(400, 400), window_step=(100, 100), path_to_model="/yolov5"):
        self.path_to_model = path_to_model
        self.window_size = window_size
        self.window_step = window_step
        self.object_detection_model = torch.load(model)
    
    # @contextmanager
    # def temporary_directory_change(self, path):
    #     original_cwd = os.getcwd()
    #     os.chdir(original_cwd + path)
    #     try:
    #         yield
    #     finally:
    #         os.chdir(original_cwd)

    # TODO: Parallelize this function
    def detect_chainlinks(self, image, preview=False, save=False):
        """
        Args:
        - image: a NumPy array representing the input image.

        Returns:
        - A NumPy array of bounding boxes in YOLOv5 format.
        """
        # Temporarily change directory
        # with self.temporary_directory_change(self.path_to_model):
        #     print(os.getcwd())
        # self.window_size[0] = min(self.window_size[0], image.shape[0])
        # self.window_size[1] = min(self.window_size[1], image.shape[1])
        print(self.window_size)
        # self.window_size = tuple(self.window_size)
        
        # Extract the shape of the input image.
        height, width, _ = image.shape
        # print('Image shape: ', image.shape)

        # Detect the bounding boxes for the window.
        detection_results = self.object_detection_model(image)
        bounding_boxes = detection_results.xyxy[0].numpy()
        
        if preview or save:
            self.__draw_bounding_boxes(image, bounding_boxes, preview, save)

        # Return the merged bounding boxes.
        return bounding_boxes


    def __draw_bounding_boxes(self, image, boxes, preview=False, save=False, colors=None, thickness=1, font_scale=0.2, font_thickness=1):
        """
        Draws bounding boxes on an image using the provided list of bounding boxes.

        Args:
        - image: a NumPy array representing the input image.
        - boxes: a NumPy array of bounding boxes in the format (xmin, ymin, xmax, ymax, confidence, class).
        - output_path: a string representing the path to the output image file. If not provided, the output image is not saved.
        - colors: a list of colors to use for each class label. If not provided, random colors will be used.
        - thickness: the thickness of the bounding box lines in pixels.
        - font_scale: the font scale to use for the class labels.
        - font_thickness: the thickness of the font lines in pixels.
        
        Returns:
        - A copy of the input image with the bounding boxes drawn on it.
        """
        # Convert the image to BGR format if it is in RGB format.
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # If colors are not provided, use random colors for each class label.
        if colors is None:
            classes = np.unique(boxes[:, 5]).astype(int)
            np.random.seed(42)
            colors = np.random.randint(0, 255, size=(len(classes), 3), dtype=np.uint8)

        # Draw the bounding boxes and class labels on a copy of the input image.
        output_image = image.copy()
        for box in boxes:
            xmin, ymin, xmax, ymax, confidence, label = box.astype(int)

            # Draw the bounding box.
            color = tuple(map(int, colors[label % len(colors)]))
            cv2.rectangle(output_image, (xmin, ymin), (xmax, ymax), color, thickness)
            # print(box)

            # Draw the class label.
            label_text = f"{label}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            cv2.rectangle(output_image, (xmin, ymin - label_size[1]), (xmin + label_size[0], ymin), color, cv2.FILLED)
            cv2.putText(output_image, label_text, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

        # Save picture and display it
        current_date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = f"{os.getcwd()}/data_bounding_boxes/{current_date_time}.png"
        cv2.imwrite(output_path, output_image)
        
        if preview:
            img = Image.open(output_path)
            img.show()
        
        # If an output path is not provided, delete image.
        if not save:
            os.remove(output_path)
