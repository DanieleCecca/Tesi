import cv2
import tensorflow as tf
import numpy as np
from website.controllers.utils.constants import *

class Movenet:
    
    def __init__(self):
        
        # Initialize the TFLite interpreter
        self.interpreter = tf.lite.Interpreter(model_path="D:\\tesi\\notebook\lite-model_movenet_singlepose_thunder_3.tflite")
        self.interpreter.allocate_tensors()
        
    def movenet(self,input_image):
        input_image = tf.cast(input_image, dtype = tf.float32)
            
        # Setup input and output
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        
        # Make Predictions
        self.interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])
        
        return keypoints_with_scores
    
    def init_crop_region(self,image_height, image_width):
        """Defines the default crop region.

        The function provides the initial crop region (pads the full image from both
        sides to make it a square image) when the algorithm cannot reliably determine
        the crop region from the previous frame.
        """
        if image_width > image_height:
            box_height = image_width / image_height
            box_width = 1.0
            y_min = (image_height / 2 - image_width / 2) / image_height
            x_min = 0.0
        else:
            box_height = 1.0
            box_width = image_height / image_width
            y_min = 0.0
            x_min = (image_width / 2 - image_height / 2) / image_width

        return {
            'y_min': y_min,
            'x_min': x_min,
            'y_max': y_min + box_height,
            'x_max': x_min + box_width,
            'height': box_height,
            'width': box_width
        }
  
 
    def torso_visible(self,keypoints):
        """Checks whether there are enough torso keypoints.

        This function checks whether the model is confident at predicting one of the
        shoulders/hips which is required to determine a good crop region.
        """
        return ((keypoints[0, 0, KEYPOINT_DICT['left_hip'], 2] >
                MIN_CROP_KEYPOINT_SCORE or
                keypoints[0, 0, KEYPOINT_DICT['right_hip'], 2] >
                MIN_CROP_KEYPOINT_SCORE) and
                (keypoints[0, 0, KEYPOINT_DICT['left_shoulder'], 2] >
                MIN_CROP_KEYPOINT_SCORE or
                keypoints[0, 0, KEYPOINT_DICT['right_shoulder'], 2] >
                MIN_CROP_KEYPOINT_SCORE))     

    def determine_torso_and_body_range(self,keypoints, target_keypoints, center_y, center_x):
        """Calculates the maximum distance from each keypoints to the center location.

        The function returns the maximum distances from the two sets of keypoints:
        full 17 keypoints and 4 torso keypoints. The returned information will be
        used to determine the crop size. See determineCropRegion for more detail.
        """
        torso_joints = ['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip']
        max_torso_yrange = 0.0
        max_torso_xrange = 0.0
        for joint in torso_joints:
            dist_y = abs(center_y - target_keypoints[joint][0])
            dist_x = abs(center_x - target_keypoints[joint][1])
            if dist_y > max_torso_yrange:
                max_torso_yrange = dist_y
            if dist_x > max_torso_xrange:
                max_torso_xrange = dist_x

        max_body_yrange = 0.0
        max_body_xrange = 0.0
        for joint in KEYPOINT_DICT.keys():
            if keypoints[0, 0, KEYPOINT_DICT[joint], 2] < MIN_CROP_KEYPOINT_SCORE:
                continue
            dist_y = abs(center_y - target_keypoints[joint][0]);
            dist_x = abs(center_x - target_keypoints[joint][1]);
            if dist_y > max_body_yrange:
                max_body_yrange = dist_y

            if dist_x > max_body_xrange:
                max_body_xrange = dist_x

        return [max_torso_yrange, max_torso_xrange, max_body_yrange, max_body_xrange]
    
    
    def determine_crop_region(self,keypoints, image_height,image_width):
        """Determines the region to crop the image for the model to run inference on.

        The algorithm uses the detected joints from the previous frame to estimate
        the square region that encloses the full body of the target person and
        centers at the midpoint of two hip joints. The crop size is determined by
        the distances between each joints and the center point.
        When the model is not confident with the four torso joint predictions, the
        function returns a default crop which is the full image padded to square.
        """
        target_keypoints = {}
        for joint in KEYPOINT_DICT.keys():
            target_keypoints[joint] = [
            keypoints[0, 0, KEYPOINT_DICT[joint], 0] * image_height,
            keypoints[0, 0, KEYPOINT_DICT[joint], 1] * image_width
            ]

        if self.torso_visible(keypoints):
            center_y = (target_keypoints['left_hip'][0] +
                        target_keypoints['right_hip'][0]) / 2;
            center_x = (target_keypoints['left_hip'][1] +
                        target_keypoints['right_hip'][1]) / 2;

            (max_torso_yrange, max_torso_xrange,
            max_body_yrange, max_body_xrange) = self.determine_torso_and_body_range(
                keypoints, target_keypoints, center_y, center_x)

            crop_length_half = np.amax(
                [max_torso_xrange * 1.9, max_torso_yrange * 1.9,
                max_body_yrange * 1.2, max_body_xrange * 1.2])

            tmp = np.array(
                [center_x, image_width - center_x, center_y, image_height - center_y])
            crop_length_half = np.amin(
                [crop_length_half, np.amax(tmp)]);

            crop_corner = [center_y - crop_length_half, center_x - crop_length_half];

            if crop_length_half > max(image_width, image_height) / 2:
                return self.init_crop_region(image_height, image_width)
            else:
                crop_length = crop_length_half * 2;
            return {
                'y_min': crop_corner[0] / image_height,
                'x_min': crop_corner[1] / image_width,
                'y_max': (crop_corner[0] + crop_length) / image_height,
                'x_max': (crop_corner[1] + crop_length) / image_width,
                'height': (crop_corner[0] + crop_length) / image_height -
                    crop_corner[0] / image_height,
                'width': (crop_corner[1] + crop_length) / image_width -
                    crop_corner[1] / image_width
            }
        else:
            return self.init_crop_region(image_height, image_width)

    def crop_and_resize(self,image, crop_region, crop_size):
        """Crops and resize the image to prepare for the model input."""
        boxes=[[crop_region['y_min'], crop_region['x_min'],
                crop_region['y_max'], crop_region['x_max']]]
        output_image = tf.image.crop_and_resize(
            image, box_indices=[0], boxes=boxes, crop_size=crop_size)
        return output_image


    def run_inference(self,movenet, image, crop_region, crop_size):
        """Runs model inferece on the cropped region.

        The function runs the model inference on the cropped region and updates the
        model output to the original image coordinate system.
        """
        image_height, image_width, _ = image.shape
        input_image = self.crop_and_resize(
            tf.expand_dims(image, axis=0), crop_region, crop_size=crop_size)
        # Run model inference.
        keypoints_with_scores = movenet(input_image)
        # Update the coordinates.
        for idx in range(17):
            keypoints_with_scores[0, 0, idx, 0] = (
                crop_region['y_min'] * image_height +
                crop_region['height'] * image_height *
                keypoints_with_scores[0, 0, idx, 0]) / image_height
            keypoints_with_scores[0, 0, idx, 1] = (
                crop_region['x_min'] * image_width +
                crop_region['width'] * image_width *
                keypoints_with_scores[0, 0, idx, 1]) / image_width
        return keypoints_with_scores

    def draw_keypoints(self,frame, keypoints, threshold):  
        y, x, c = frame.shape
        # Denormalize the coordinates : multiply the normalized coordinates by the input_size(width,height)
        denormalized_coordinates = np.squeeze(np.multiply(keypoints, [y,x,1]))
        # Iterate through the points
        for keypoint in denormalized_coordinates:
            # Unpack the keypoint values : y, x, confidence score
            keypoint_y, keypoint_x, keypoint_confidence = keypoint
            if keypoint_confidence > threshold:
        
                cv2.circle(
                    img=frame, 
                    center=(int(keypoint_x), int(keypoint_y)), 
                    radius=3, 
                    color=(255,0,0),
                    thickness=-1
                )
    def draw_edges(self,denormalized_coordinates,keypoints, frame, edges_colors, threshold):
        
        y,x,c = frame.shape
        denormalized_coordinates = np.squeeze(np.multiply(keypoints, [y,x,1]))
        # Iterate through the edges 
        for edge, color in edges_colors.items():
            # Get the dict value associated to the actual edge
            p1, p2 = edge
            # Get the points
            y1, x1, confidence_1 = denormalized_coordinates[p1]
            y2, x2, confidence_2 = denormalized_coordinates[p2]
            # Draw the line from point 1 to point 2, the confidence > threshold
            if (confidence_1 > threshold) & (confidence_2 > threshold):      
                cv2.line(
                    img=frame, 
                    pt1=(int(x1), int(y1)),
                    pt2=(int(x2), int(y2)), 
                    color=color, 
                    thickness=1, 
                    lineType=cv2.LINE_AA # Gives anti-aliased (smoothed) line which looks great for curves
                )
            
    def draw_skeleton(self,frame, keypoints_with_scores, threshold):
            self.draw_keypoints(frame , keypoints_with_scores, threshold)
            self.draw_edges(frame,keypoints_with_scores, frame, EDGE_COLORS, threshold)
        

    def extract_keypoints(self,keypoints_with_scores):
        pose = []
        i=0
        while i < len(keypoints_with_scores[0][0][:]):
            #row che sarà composta da x y e confidence dell' i-esimo keypoint/joint
            row = np.array([keypoints_with_scores[0][0][i][0], keypoints_with_scores[0][0][i][1], keypoints_with_scores[0][0][i][2]])
            pose.append(row)
            i+=1
        #redo il vettore a 1D
        pose = np.array(pose).flatten()
        return pose