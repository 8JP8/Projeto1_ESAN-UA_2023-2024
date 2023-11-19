import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
import configparser
import datetime
import os

# ============ MODULES ============
import modules.MathFunctions as MathFunctions
import modules.CustomDetection as customdetection
# ============= \\-// =============

# ============= VARS =============

# Criar objeto de configuração e ler o ficheiro
config = configparser.ConfigParser()
config.read('config.ini')
#output_dir = '../outputs'
#os.makedirs(output_dir, exist_ok=True)

global USE_TWO_CAMERAS,CAMERA_INDEX_LEFT,CAMERA_INDEX_RIGHT,PIXEL_SEPARATION,DIAMETER_SEPARATION, DETECTIONMODE_VALUE, CATEGORIZATIONMODE_VALUE

# Variable Configuration
USE_TWO_CAMERAS = config.getboolean('CAMERA_CONFIG', 'USE_TWO_CAMERAS')       # Set to True if using two cameras for stereo vision
CAMERA_INDEX_LEFT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_LEFT')    # Camera index for the left camera (if using two cameras)
CAMERA_INDEX_RIGHT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_RIGHT')   # Camera index for the right camera (if using two cameras)
CAMERA_CALC_DIAMETER = config.getboolean('CAMERA_CONFIG', 'CAMERA_CALC_DIAMETER')
CAMERA_HEIGHT = config.getfloat('CAMERA_CONFIG', 'CAMERA_HEIGHT')
CAMERA_DISTANCE = config.getfloat('CAMERA_CONFIG', 'CAMERA_DISTANCE')
CAMERA_FOV = config.getint('CAMERA_CONFIG', 'CAMERA_FOV')
FOCAL_LENGHT = config.getint('CAMERA_CONFIG', 'FOCAL_LENGHT')
SENSOR_WIDTH = config.getint('CAMERA_CONFIG', 'SENSOR_WIDTH')
SQUARE_SIZE = config.getfloat('CAMERA_CONFIG', 'SQUARE_SIZE')
APPLE_Z = config.getfloat('CAMERA_CONFIG', 'APPLE_Z')

# Define separation values for small and big apples (in pixels or actual diameter)
PIXEL_SEPARATION = config.getfloat('CAMERA_CONFIG', 'PIXEL_SEPARATION')              # Placeholder value for pixel-related separation
DIAMETER_SEPARATION = config.getfloat('CAMERA_CONFIG', 'DIAMETER_SEPARATION')          # Placeholder value for actual diameter separation (in cm)

DETECTIONMODE_VALUE = config.getint('DETECTION_CONFIG', 'DETECTIONMODE_VALUE')  
CATEGORIZATIONMODE_VALUE = config.getint('DETECTION_CONFIG', 'CATEGORIZATIONMODE_VALUE')

if DETECTIONMODE_VALUE == -1: DETECTIONMODE_VALUE = 0
if CATEGORIZATIONMODE_VALUE == -1: CATEGORIZATIONMODE_VALUE = 0

#Debug
cap_left = None
cap_right = None
cap = None
apple_count = None
roi = None
calibration_inprogress = False
LOG_FILE_PATH = config.get('LOGS_CONFIG', 'LOGS_FILE_PATH')

# ============ \\--// ============



# Load the class names from coco.names
try:
    with open(config.get('DEPENDENCIES_CONFIG', 'MODEL_'+DETECTIONMODE_VALUE+'_NAMES_FILE_PATH'), 'r') as file:
        class_names = file.read().strip().split('\n')

    # Initialize the Keras model for apple classification
    model = load_model(config.get('DEPENDENCIES_CONFIG', 'MODEL_'+CATEGORIZATIONMODE_VALUE+'_CATEGORIZATION_FILE_PATH'))
    # Load Identification Model YOLO configuration and weights
    net = cv2.dnn.readNet(config.get('DEPENDENCIES_CONFIG', 'MODEL_'+DETECTIONMODE_VALUE+'_WEIGHTS_FILE_PATH'), config.get('DEPENDENCIES_CONFIG', 'MODEL_'+DETECTIONMODE_VALUE+'_WEIGHTS_CFG_PATH'))
except:
    with open(config.get('DEPENDENCIES_CONFIG', 'MODEL_0_NAMES_FILE_PATH'), 'r') as file:
        class_names = file.read().strip().split('\n')

    # Initialize the Keras model for apple classification
    model = load_model(config.get('DEPENDENCIES_CONFIG', 'MODEL_0_CATEGORIZATION_FILE_PATH'))
    # Load Identification Model YOLO configuration and weights
    net = cv2.dnn.readNet(config.get('DEPENDENCIES_CONFIG', 'MODEL_0_WEIGHTS_FILE_PATH'), config.get('DEPENDENCIES_CONFIG', 'MODEL_0_WEIGHTS_CFG_PATH'))

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

    # Calculate the IoU
    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou

# Function to determine apple type (Big, Small, Bad)
def determine_apple_type(pixel_caliber, diameter, categorization_confidence, threshold2):
    if categorization_confidence >= threshold2:
        return "Bad Apple"
    elif categorization_confidence == -1:
        return "???"
    elif CAMERA_CALC_DIAMETER and not diameter == pixel_caliber:
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
def detect_and_classify_apples(frame, type, detectionmode, categorizationmode, threshold1, threshold2, calibresult):
    THRESHOLD_1 = threshold1
    THRESHOLD_2 = threshold2
    DETECTIONMODE_VALUE = detectionmode
    CATEGORIZATIONMODE_VALUE = categorizationmode
    categorization_confidence = -1

    apple_boxes = []
    apple_certainties = []
    apple_diameters = []
    apple_corners = []  # List to store apple corner coordinates
    
    height, width, _ = frame.shape

    if DETECTIONMODE_VALUE == 2:
        inputframe = frame
        result = customdetection.detect(inputframe, type)
        frame = result[0]
        circles = result[1]

        for apple in circles:
            x = apple[0]
            y = apple[1]
            r = apple[2]

            apple_quadrants = np.array([
                [x, y-r],
                [x-r, y],
                [x, y+r],
                [x+r, y]
            ], dtype=np.float32)

            apple = frame[int(y-r):int(y + r*2), int(x-r):int(x + r*2)]

            if CATEGORIZATIONMODE_VALUE == 0:

                if apple.shape[0] > 0 and apple.shape[1] > 0:
                    if apple.shape[0] != 100 or apple.shape[1] != 100:
                        apple = cv2.resize(apple, (100, 100))
                    apple = img_to_array(apple)
                    apple = preprocess_input(apple)
                    apple = np.expand_dims(apple, axis=0)

                    prediction = model.predict(apple)
                    categorization_confidence = prediction[0][0]
                    
            else:
                categorization_confidence = -1 
            

            if CAMERA_CALC_DIAMETER and (type == "camera"):
                #Get width information
                if calibresult != None and config.getboolean('CAMERA_CONFIG', 'USE_CAMERA_CALIBRATION'):
                    measuredwidth = MathFunctions.calculate_apple_width_in_mm(apple_quadrants, SENSOR_WIDTH, calibresult[2], calibresult[3], calibresult[4], calibresult[5], APPLE_Z, SQUARE_SIZE)
                    '''
                    while True:
                        Erro = APPLE_Z - measuredwidth/2
                        if abs(Erro) > 0.05:
                            if Erro < 0:
                                APPLE_Z+=Erro/2
                            else:
                                APPLE_Z-=Erro/2
                        else:
                            print("Erro:",Erro," Z:",APPLE_Z)
                            b
                        measuredwidth = MathFunctions.calculate_apple_width_in_mm(apple_quadrants, SENSOR_WIDTH, calibresult[2], calibresult[3], calibresult[4], calibresult[5], APPLE_Z, SQUARE_SIZE)
                    '''
                    diameter = round(measuredwidth, 2)
                else:
                    diameter = round(MathFunctions.pixels_to_cm(r, CAMERA_HEIGHT, CAMERA_FOV, CAMERA_DISTANCE))
            else:
                # Use single camera processing here (calculate diameter based on single image)
                # Placeholder values:
                diameter = r*2

            timestamp = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")

            apple_type = determine_apple_type(r*2, diameter, categorization_confidence, threshold2)
            # Log the apple's data
            with open(LOG_FILE_PATH, 'a') as log:
                if CAMERA_CALC_DIAMETER or type != 'camera':
                    log.write(f"{timestamp},{apple_type},{diameter}cm\n")
                else:
                    log.write(f"{timestamp},{apple_type},{round(r*2)}px\n")
            apple_boxes.append((x, y, r*2, r*2))
            apple_certainties.append(categorization_confidence)
            apple_diameters.append(diameter)
            
            # Draw text in the center of the detected apple
            if CAMERA_CALC_DIAMETER and (type == "camera"):
                text = f"Diametro: {diameter}cm | {apple_type}"
            else:
                text = f"Largura: {round(r*2,2)}px | {apple_type}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            text_x = int(x - text_size[0]/2)
            text_y = int(y + text_size[1]/2)
            if categorization_confidence >= THRESHOLD_2:
                color = (255, 0, 0)  # Red if rotten categorization_confidence > THRESHOLD_2
            else:
                color = (0, 255, 0)  # Green otherwise
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        else:
            return frame

    elif DETECTIONMODE_VALUE in [0, 1]:
        
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        layer_names = net.getUnconnectedOutLayersNames()
        detections = net.forward(layer_names)

        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                detection_confidence = scores[class_id]

                # Check if the class name is 'apple'
                if detection_confidence > THRESHOLD_1 and class_names[class_id] == 'apple':
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

                            categorization_confidence = prediction[0][0]

                            pixel_caliber = w  # Use the pixel width as pixel_caliber

                            # Store the corners of the detected apple
                            
                            apple_corners = np.array([
                                [x, y],
                                [x+w, y],
                                [x, y+h],
                                [x+w, y+h]
                            ], dtype=np.float32)

                            apple_quadrants = np.array([
                                [x+w/2, y],
                                [x, y+h/2],
                                [x+w/2, y+h],
                                [x+w, y+h/2]
                            ], dtype=np.float32)


                            if CAMERA_CALC_DIAMETER and (type == "camera"):
                                #Get width information
                                if calibresult != None and config.getboolean('CAMERA_CONFIG', 'USE_CAMERA_CALIBRATION'):
                                    #global APPLE_Z
                                    measuredwidth = MathFunctions.calculate_apple_width_in_mm(apple_quadrants, SENSOR_WIDTH, calibresult[2], calibresult[3], calibresult[4], calibresult[5], APPLE_Z, SQUARE_SIZE)
                                    '''
                                    while True:
                                        Erro = APPLE_Z - measuredwidth/2
                                        if abs(Erro) > 0.05:
                                            if Erro < 0:
                                                APPLE_Z+=Erro/2
                                            else:
                                                APPLE_Z-=Erro/2
                                        else:
                                            print("Erro:",Erro," Z:",APPLE_Z)
                                            break

                                        measuredwidth = MathFunctions.calculate_apple_width_in_mm(apple_quadrants, SENSOR_WIDTH, calibresult[2], calibresult[3], calibresult[4], calibresult[5], APPLE_Z, SQUARE_SIZE)
                                    '''
                                    diameter = round(measuredwidth, 2)
                                else:
                                    diameter = round(MathFunctions.pixels_to_cm(pixel_caliber, CAMERA_HEIGHT, CAMERA_FOV, CAMERA_DISTANCE), 2)

                            else:
                                # Use single camera processing here (calculate diameter based on single image)
                                # Placeholder values:
                                diameter = pixel_caliber

                            # Determine apple type
                            apple_type = determine_apple_type(pixel_caliber, diameter, categorization_confidence, threshold2)

                            timestamp = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")

                            # Log the apple's data
                            with open(LOG_FILE_PATH, 'a') as log:
                                if CAMERA_CALC_DIAMETER and (type == "camera"):
                                    log.write(f"{timestamp},{apple_type},{diameter}cm\n")
                                else:
                                    log.write(f"{timestamp},{apple_type},{pixel_caliber}px\n")
                            apple_boxes.append((x, y, w, h))
                            apple_certainties.append(categorization_confidence)
                            apple_diameters.append(diameter)
                            

                            # Draw text in the center of the detected apple
                            if CAMERA_CALC_DIAMETER:
                                text = f"Diametro: {diameter}cm | {apple_type}"
                            else:
                                text = f"Largura: {pixel_caliber}px | {apple_type}"
                            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                            text_x = x + (w - text_size[0]) // 2
                            text_y = y + (h + text_size[1]) // 2
                            if categorization_confidence > THRESHOLD_2:
                                color = (255, 0, 0)  # Red if rotten categorization_confidence > THRESHOLD_2
                            else:
                                color = (0, 255, 0)  # Green otherwise
                            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                            # Draw a circle around the object contour
                            cv2.circle(frame, (center_x, center_y), int((w + h) / 4), color, 2)

        else:
            return frame


# Log file setup
with open(LOG_FILE_PATH, 'w') as log:
    log.write("Timestamp,Type,Diameter\n")
    

# Read ConfigValues Function
def UpdateConfigValues():
    global USE_TWO_CAMERAS, CAMERA_INDEX_LEFT, CAMERA_INDEX_RIGHT, THRESHOLD_1, THRESHOLD_2, PIXEL_SEPARATION, DIAMETER_SEPARATION, DETECTIONMODE_VALUE, CATEGORIZATIONMODE_VALUE
    config.read('../config.ini')
    USE_TWO_CAMERAS = config.getboolean('CAMERA_CONFIG', 'USE_TWO_CAMERAS')
    CAMERA_INDEX_LEFT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_LEFT')
    CAMERA_INDEX_RIGHT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_RIGHT')
    THRESHOLD_1 = config.getint('DETECTION_CONFIG', 'threshold1_VALUE')/100
    THRESHOLD_2 = config.getint('DETECTION_CONFIG', 'threshold2_VALUE')/100

    # Define separation values for small and big apples (in pixels or actual diameter)
    PIXEL_SEPARATION = config.getfloat('CAMERA_CONFIG', 'PIXEL_SEPARATION')              # Placeholder value for pixel-related separation
    DIAMETER_SEPARATION = config.getfloat('CAMERA_CONFIG', 'DIAMETER_SEPARATION')          # Placeholder value for actual diameter separation (in cm)

    DETECTIONMODE_VALUE = config.getint('DETECTION_CONFIG', 'DETECTIONMODE_VALUE')  
    CATEGORIZATIONMODE_VALUE = config.getint('DETECTION_CONFIG', 'CATEGORIZATIONMODE_VALUE')   

    return USE_TWO_CAMERAS, CAMERA_INDEX_LEFT, CAMERA_INDEX_RIGHT, THRESHOLD_1, THRESHOLD_2, PIXEL_SEPARATION, DIAMETER_SEPARATION, DETECTIONMODE_VALUE, CATEGORIZATIONMODE_VALUE

# Clean up
if USE_TWO_CAMERAS:
    if cap_left:
        cap_left.release()
    if cap_right:
        cap_right.release()
else:
    if cap:
        cap.release()
