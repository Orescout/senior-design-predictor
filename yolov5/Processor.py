import numpy as np
import cv2
from sklearn.linear_model import RANSACRegressor
import os
from PIL import Image
import datetime

class Processor:
    def __init__(self, raw_image, bounding_boxes):
        self.raw_image = raw_image
        self.bounding_boxes = bounding_boxes
    
    def estimate_chain_direction(self, save=False, preview=False):
        """
        Draws a straight line that approximately goes through most center points of the bounding boxes in an image.
        Args: None
        Returns:
            angle: the degrees that the anchor is facing at.
        """
        
        # convert boxes to center coordinates
        centers = [(int((x1 + x2) / 2), int((y1 + y2) / 2)) for x1, y1, x2, y2, conf, cl in self.bounding_boxes]
        centers = np.array(centers)
        x = centers[:, 0]
        y = centers[:, 1]
        
        # Regression with RANSAC
        ransac = RANSACRegressor(min_samples=2)
        ransac.fit(x.reshape(-1, 1), y)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)
        line_X = np.arange(x.min(), x.max())[:, np.newaxis]
        line_y_ransac = ransac.predict(line_X)
        
        # Construct line
        line_point_1 = (int(line_X[0]), int(line_y_ransac[0]))
        line_point_2 = (int(line_X[-1]), int(line_y_ransac[-1]))
        new_image = self.raw_image.copy()
        cv2.line(new_image, line_point_1, line_point_2, (0, 255, 0), 2)
        
        angle  = self.__find_angle(line_point_1[0], line_point_1[1], line_point_2[0], line_point_2[1]) # Get angle from [-90, 90]
        angle = angle if angle >= 0 else angle + 180 # make from [0, 360]
        
        # Save picture and display it
        current_date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = f"{os.getcwd()}/data_chain_direction_oclock/{current_date_time}.png"
        cv2.imwrite(output_path, new_image)
        
        if preview:
            img = Image.open(output_path)
            img.show()
        
        # If an output path is not provided, delete image.
        if not save:
            os.remove(output_path)
        
        return np.round(angle, 2)
    
    
    def __find_angle(self, x1, y1, x2, y2):
        rise = y2 - y1
        run = x2 - x1
        angle = np.arctan(rise / run)
        angle = np.rad2deg(angle)
        return angle

    def get_number_of_chainlinks(self):
        return self.bounding_boxes.shape[0]