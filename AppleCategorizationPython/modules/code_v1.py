import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
import configparser
import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============= VARS =============

# Criar objeto de configuração e ler o ficheiro
config = configparser.ConfigParser()
config.read('../config.ini')

output_dir = '../outputs'
os.makedirs(output_dir, exist_ok=True)

global USE_TWO_CAMERAS,CAMERA_INDEX_LEFT,CAMERA_INDEX_RIGHT,CAMERA_PRESENT,PIXEL_SEPARATION,DIAMETER_SEPARATION, DETECTIONMODE_VALUE, CATEGORIZATIONMODE_VALUE

# Variable Configuration
USE_TWO_CAMERAS = config.get('CAMERA_CONFIG', 'USE_TWO_CAMERAS')       # Set to True if using two cameras for stereo vision
CAMERA_INDEX_LEFT = config.get('CAMERA_CONFIG', 'CAMERA_INDEX_LEFT')    # Camera index for the left camera (if using two cameras)
CAMERA_INDEX_RIGHT = config.get('CAMERA_CONFIG', 'CAMERA_INDEX_RIGHT')   # Camera index for the right camera (if using two cameras)
THREASHOLD_1 = config.getint('DETECTION_CONFIG', 'THREASHOLD1_VALUE')
THREASHOLD_2 = config.getint('DETECTION_CONFIG', 'THREASHOLD1_VALUE')

# Define separation values for small and big apples (in pixels or actual diameter)
PIXEL_SEPARATION = config.get('CAMERA_CONFIG', 'PIXEL_SEPARATION')              # Placeholder value for pixel-related separation
DIAMETER_SEPARATION = config.get('CAMERA_CONFIG', 'DIAMETER_SEPARATION')          # Placeholder value for actual diameter separation (in cm)

DETECTIONMODE_VALUE = config.get('DETECTION_CONFIG', 'DETECTIONMODE_VALUE')  
CATEGORIZATIONMODE_VALUE = config.get('DETECTION_CONFIG', 'CATEGORIZATIONMODE_VALUE')

if DETECTIONMODE_VALUE == '-1': DETECTIONMODE_VALUE = '0'
if CATEGORIZATIONMODE_VALUE == '-1': CATEGORIZATIONMODE_VALUE = '0'

#Debug
cap_left = None
cap_right = None
cap = None
LOG_FILE_PATH = "../" + config.get('LOGS_CONFIG', 'LOGS_FILE_PATH')

# ============ \\--// ============



# Function to initialize the camera
def initialize_camera():
    if USE_TWO_CAMERAS:
        cap_left = cv2.VideoCapture(CAMERA_INDEX_LEFT)
        cap_right = cv2.VideoCapture(CAMERA_INDEX_RIGHT)
        return cap_left, cap_right
    else:
        cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify a camera index
        return cap


# Load the class names from coco.names
with open(config.get('DEPENDENCIES_CONFIG', 'MODEL_'+DETECTIONMODE_VALUE+'_NAMES_FILE_PATH'), 'r') as file:
    class_names = file.read().strip().split('\n')

# Initialize the Keras model for apple classification
model = load_model(config.get('DEPENDENCIES_CONFIG', 'MODEL_'+CATEGORIZATIONMODE_VALUE+'_CATEGORIZATION_FILE_PATH'))
# Load Identification Model YOLO configuration and weights
net = cv2.dnn.readNet(config.get('DEPENDENCIES_CONFIG', 'MODEL_'+DETECTIONMODE_VALUE+'_WEIGHTS_FILE_PATH'), config.get('DEPENDENCIES_CONFIG', 'MODEL_'+DETECTIONMODE_VALUE+'_WEIGHTS_CFG_PATH'))

# Function to calculate the intersection over union (IoU) between two bounding boxes
def calculate_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    x5 = max(x1, x3)
    y5 = max(y1, y3)
    x6 = min(x2, x4)
    y6 = min(y2, y4)

    intersection_area = max(0, x6 - x5 + 1) * max(0, y6 - y5 + 1)

    box1_area = (x2 - x1 + 1) * (y2 - y1 + 1)
    box2_area = (x4 - x3 + 1) * (y4 - y3 + 1)

    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou

# Function to determine apple type (Big, Small, Bad)
def determine_apple_type(pixel_caliber, diameter, THREASHOLD_2):
    if THREASHOLD_2 > 0.02:
        return "Bad Apple"
    elif USE_TWO_CAMERAS:
        if diameter > DIAMETER_SEPARATION:
            return "Big Apple"
        else:
            return "Small Apple"
    else:
        if pixel_caliber > PIXEL_SEPARATION:
            return "Big Apple"
        else:
            return "Small Apple"

# Function to perform apple detection and classification
def detect_and_classify_apples(frame, type):
    UpdateConfigValues()
    height, width, _ = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    layer_names = net.getUnconnectedOutLayersNames()
    detections = net.forward(layer_names)

    apple_boxes = []
    apple_certainties = []
    apple_diameters = []

    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            THREASHOLD_1 = scores[class_id]

            # Check if the class name is 'apple'
            if THREASHOLD_1 > 0 and class_names[class_id] == 'apple':
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                area = w * h

                overlapping = False
                for (prev_x, prev_y, prev_w, prev_h), _, _ in zip(apple_boxes, apple_certainties, apple_diameters):
                    iou = calculate_iou((prev_x, prev_y, prev_x + prev_w, prev_y + prev_h), (x, y, x + w, y + h))

                    if iou > 0.3:
                        overlapping = True
                        break

                if not overlapping:
                    apple = frame[y:y + h, x:x + w]

                    if apple.shape[0] > 0 and apple.shape[1] > 0:
                        if apple.shape[0] != 100 or apple.shape[1] != 100:
                           apple = cv2.resize(apple, (100, 100))

                        apple = img_to_array(apple)
                        apple = preprocess_input(apple)
                        apple = np.expand_dims(apple, axis=0)

                        prediction = model.predict(apple)

                        THREASHOLD_2 = prediction[0][0]

                        if USE_TWO_CAMERAS:
                            # Perform stereo vision processing here (calculate diameter based on stereo images)
                            # Placeholder values:
                            pixel_caliber = PIXEL_SEPARATION
                            diameter = DIAMETER_SEPARATION
                        else:
                            # Use single camera processing here (calculate diameter based on single image)
                            # Placeholder values:
                            pixel_caliber = w  # Use the pixel width as pixel_caliber
                            diameter = pixel_caliber

                        # Determine apple type
                        apple_type = determine_apple_type(pixel_caliber, diameter, THREASHOLD_2)

                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Log the apple's data
                        with open(LOG_FILE_PATH, 'a') as log2:
                            log2.write(f"{timestamp},{apple_type},{diameter}\n")

                        apple_boxes.append((x, y, w, h))
                        apple_certainties.append(THREASHOLD_2)
                        apple_diameters.append(diameter)

                        # Draw text in the center of the detected apple
                        if USE_TWO_CAMERAS:
                            text = f"Diameter: {diameter}px | {apple_type}"
                        else:
                            text = f"Diameter: {pixel_caliber}px | {apple_type}"
                        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                        text_x = x + (w - text_size[0]) // 2
                        text_y = y + (h + text_size[1]) // 2
                        if THREASHOLD_2 > 0.02:
                            color = (0, 0, 255)  # Red if rotten THREASHOLD_2 > 0.2
                        else:
                            color = (0, 255, 0)  # Green otherwise
                        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                        # Draw a circle around the object contour
                        cv2.circle(frame, (center_x, center_y), int((w + h) / 4), color, 2)

    return frame


########################################################
roi = None
apple_count = 0

# Log file setup
with open(LOG_FILE_PATH, 'w') as log:
    log.write("Timestamp,Type,Diameter\n")
    
def CameraProcessor():
    UpdateConfigValues()
    while True:
        if USE_TWO_CAMERAS:
            ret_left, frame_left = cap_left.read()
            ret_right, frame_right = cap_right.read()
            if not ret_left or not ret_right:
                break
            # Perform stereo vision processing here (calculate diameter based on stereo images)
            # Placeholder values:
            pixel_caliber = PIXEL_SEPARATION
            diameter = DIAMETER_SEPARATION
        else:
            ret, frame = cap.read()
            if not ret:
                break
            # Use single camera processing here (calculate diameter based on single image)
            # Placeholder values:
            pixel_caliber = PIXEL_SEPARATION
            diameter = DIAMETER_SEPARATION

        if roi is None:
            roi = frame.copy()

        # Resize input frame before feeding it to the object detection model
        #frame = cv2.resize(frame, (1000, 1000))

        # Detect and classify apples and update the frame
        frame = detect_and_classify_apples(frame)

        if USE_TWO_CAMERAS:
            # Draw stereo vision lines (for visualization)
            cv2.line(frame_left, (0, int(frame_left.shape[0] / 2)), (frame_left.shape[1], int(frame_left.shape[0] / 2)),
                    (0, 0, 255), 2)
            cv2.line(frame_right, (0, int(frame_right.shape[0] / 2)), (frame_right.shape[1], int(frame_right.shape[0] / 2)),
                    (0, 0, 255), 2)
            cv2.imshow('Left Camera', frame_left)
            cv2.imshow('Right Camera', frame_right)
        else:
            cv2.imshow('Apple Sorting and Detection', frame)


        # Exit the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Read ConfigValues Function
def UpdateConfigValues():

    USE_TWO_CAMERAS = config.getboolean('CAMERA_CONFIG', 'USE_TWO_CAMERAS')
    CAMERA_INDEX_LEFT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_LEFT')
    CAMERA_INDEX_RIGHT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_RIGHT')
    THREASHOLD_1 = config.getint('DETECTION_CONFIG', 'THREASHOLD1_VALUE')
    THREASHOLD_2 = config.getint('DETECTION_CONFIG', 'THREASHOLD1_VALUE')

    # Define separation values for small and big apples (in pixels or actual diameter)
    PIXEL_SEPARATION = config.get('CAMERA_CONFIG', 'PIXEL_SEPARATION')              # Placeholder value for pixel-related separation
    DIAMETER_SEPARATION = config.get('CAMERA_CONFIG', 'DIAMETER_SEPARATION')          # Placeholder value for actual diameter separation (in cm)

    DETECTIONMODE_VALUE = config.get('DETECTION_CONFIG', 'DETECTIONMODE_VALUE')  
    CATEGORIZATIONMODE_VALUE = config.get('DETECTION_CONFIG', 'CATEGORIZATIONMODE_VALUE')   

    return USE_TWO_CAMERAS, CAMERA_INDEX_LEFT, CAMERA_INDEX_RIGHT, THREASHOLD_1, THREASHOLD_2, PIXEL_SEPARATION, DIAMETER_SEPARATION, DETECTIONMODE_VALUE, CATEGORIZATIONMODE_VALUE

# Clean up
if USE_TWO_CAMERAS:
    if cap_left:
        cap_left.release()
    if cap_right:
        cap_right.release()
else:
    if cap:
        cap.release()
