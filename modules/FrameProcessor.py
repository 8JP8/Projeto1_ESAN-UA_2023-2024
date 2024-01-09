from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.QtGui import QIcon
import cv2
import os
import numpy as np
import configparser

# ============ MODULES ============
import modules.code_v1 as code_v1
import modules.MathFunctions as MathFunctions
import modules.LEDControl as LEDControl
from main import update_config_value
# ============= \\-// =============

config = configparser.ConfigParser()
config.read('config.ini')  # Replace 'config.ini' with the path to your configuration file

currentvideopath = ""
calibration_inprogress = False
APPLYFILTERS = config.getboolean('FILTER_CONFIG', 'APPLY_FILTERS')
USE_CAMERA_CALIBRATION = config.getboolean('CAMERA_CONFIG', 'USE_CAMERA_CALIBRATION')
CHESSBOARD_INTERSECTION_LINES = config.getint('CAMERA_CONFIG', 'CHESSBOARD_INTERSECTION_LINES')
CHESSBOARD_INTERSECTION_COLUMNS = config.getint('CAMERA_CONFIG', 'CHESSBOARD_INTERSECTION_COLUMNS')
DRAW_CALIBRATION_LINES = config.getboolean('CAMERA_CONFIG', 'DRAW_CALIBRATION_LINES')

def ImageProcessor(img_filepath, frame, detectionmode, categorizationmode, threshold1, threshold2, filter, customdetectionfilter):
    if os.path.isfile(img_filepath):
        if cv2.imread(img_filepath) is not None:
            frame = code_v1.detect_and_classify_apples(frame, "image", detectionmode, categorizationmode, threshold1, threshold2, None, customdetectionfilter)
            if APPLYFILTERS and filter!=None:
                frame = ApplyFilters(frame, filter)
            return (True, frame)
        else:
            return(False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(img_filepath)}'.")
    else:
        return(False, f"Erro: Imagem '{os.path.basename(img_filepath)}' não encontrada.")
        

def VideoProcessor(vd_filepath, frame, detectionmode, categorizationmode, threshold1, threshold2, filter, customdetectionfilter):
    if (currentvideopath == "") or (currentvideopath != vd_filepath):
        if os.path.isfile(vd_filepath):
            cap = cv2.VideoCapture(vd_filepath)
            if not cap.isOpened():
                return (False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(vd_filepath)}'.")
            else:
                newframe = code_v1.detect_and_classify_apples(frame, "video", detectionmode, categorizationmode, threshold1, threshold2, None, customdetectionfilter)
                if APPLYFILTERS and filter!=None:
                    newframe = ApplyFilters(newframe, filter)
                return (True, newframe)
        else:
            return (False, f"Erro: Vídeo '{os.path.basename(vd_filepath)}' não encontrado.")
    else:
        try:
            newframe = code_v1.detect_and_classify_apples(frame, "video", detectionmode, categorizationmode, threshold1, threshold2, None, customdetectionfilter)
            if APPLYFILTERS and filter!=None:
                newframe = ApplyFilters(newframe, filter)
            return (True, newframe)
        except:
            return(False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(vd_filepath)}'.")
        
def CameraProcessor(inputframe, detectionmode, categorizationmode, threshold1, threshold2, filter, customdetectionfilter):
    calibresult = cameracalibrationprocessor(inputframe)
    if calibresult != None:
        inputframe = calibresult[1]
    # Detect and classify apples and update the frame
    try:
        frame = code_v1.detect_and_classify_apples(inputframe, "camera", detectionmode, categorizationmode, threshold1, threshold2, calibresult, customdetectionfilter)  
    except Exception as e:
        print(e)
        frame = inputframe
        #return(False, f"Erro: O processamento de frames falhou.")
    return (True, frame)

def ApplyFilters(imageframe, guifvalues):
    # Check if it's a 3-channel image (BGR)
    # Handle different channel formats (e.g., grayscale)
    # You might want to convert to BGR or handle differently based on your use case.
    hsv = cv2.cvtColor(imageframe, cv2.COLOR_BGR2HSV)
    # add/subtract saturation and value
    h, s, v = cv2.split(hsv)
    h = shift_channel(h, guifvalues.hue_addsub)
    s = shift_channel(s, guifvalues.sat_addsub)
    v = shift_channel(v, guifvalues.val_addsub)
    hsv = cv2.merge([h, s, v])
    # Set minimum and maximum HSV values to display
    lower = np.array([guifvalues.minhue, guifvalues.minsat, guifvalues.minval])
    upper = np.array([guifvalues.maxhue, guifvalues.maxsat, guifvalues.maxval])
    # Apply the thresholds
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(hsv, hsv, mask=mask)
    # kernelsizes
    kernel = np.ones((guifvalues.kernelsize, guifvalues.kernelsize), np.uint8)
    kernelsize = (int(guifvalues.blurkernelsize),int(guifvalues.blurkernelsize))
    # put gaussianblur
    gaussianblur = cv2.GaussianBlur(result, kernelsize, guifvalues.gaussianblur)
    # convert back to BGR for imshow() to display it properly
    img = cv2.cvtColor(gaussianblur, cv2.COLOR_HSV2BGR)
    if guifvalues.enablecanny:
        dilated_image = cv2.dilate(img, kernel, iterations=guifvalues.cannydilate)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=guifvalues.cannyerode)
        # canny edge detection
        result = cv2.Canny(eroded_image, guifvalues.canny1, guifvalues.canny2)
        # Apply output dilation and erosion to the grayscale image
        output_dilated_image = cv2.dilate(result, kernel, iterations=guifvalues.output_dilate)
        output_eroded_image = cv2.erode(output_dilated_image, kernel, iterations=guifvalues.output_erode)
        # convert single channel image back to BGR
        img = cv2.cvtColor(output_eroded_image, cv2.COLOR_GRAY2BGR)
    elif guifvalues.enablesobel:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, kernel, scale=1)
        y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, kernel, scale=1)
        absx = cv2.convertScaleAbs(x)
        absy = cv2.convertScaleAbs(y)
        edge = cv2.addWeighted(absx, 0.5, absy, 0.5, 0)
        # Apply output dilation and erosion to the grayscale image
        output_dilated_image = cv2.dilate(edge, kernel, iterations=guifvalues.output_dilate)
        output_eroded_image = cv2.erode(output_dilated_image, kernel, iterations=guifvalues.output_erode)
        # convert single channel image back to BGR
        img = cv2.cvtColor(output_eroded_image, cv2.COLOR_GRAY2BGR)
    elif guifvalues.enablelaplace:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=guifvalues.kernelsize)
        # Apply output dilation and erosion to the grayscale image
        output_dilated_image = cv2.dilate(laplacian, kernel, iterations=guifvalues.output_dilate)
        output_eroded_image = cv2.erode(output_dilated_image, kernel, iterations=guifvalues.output_erode)
        # Convert from 64-bit float to 8-bit unsigned integer
        output_eroded_image = cv2.convertScaleAbs(output_eroded_image)
        # convert single channel image back to BGR
        img = cv2.cvtColor(output_eroded_image, cv2.COLOR_GRAY2BGR)

    return img

def ApplyInputFilters(imageframe, guifvalues):
    hsv = cv2.cvtColor(imageframe, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h = shift_channel(h, guifvalues.hue_addsub)
    s = shift_channel(s, guifvalues.sat_addsub)
    v = shift_channel(v, guifvalues.val_addsub)
    hsv = cv2.merge([h, s, v])
    lower = np.array([guifvalues.minhue, guifvalues.minsat, guifvalues.minval])
    upper = np.array([guifvalues.maxhue, guifvalues.maxsat, guifvalues.maxval])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(hsv, hsv, mask=mask)
    kernel = np.ones((guifvalues.kernelsize, guifvalues.kernelsize), np.uint8)
    kernelsize = (int(guifvalues.blurkernelsize),int(guifvalues.blurkernelsize))
    gaussianblur = cv2.GaussianBlur(result, kernelsize, guifvalues.gaussianblur)
    img = cv2.cvtColor(gaussianblur, cv2.COLOR_HSV2BGR)
    if guifvalues.dilate_erode_pre_apply:
        dilated_image = cv2.dilate(img, kernel, iterations=guifvalues.dilate1)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=guifvalues.erode1)
        dilated_image = cv2.dilate(eroded_image, kernel, iterations=guifvalues.dilate2)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=guifvalues.erode2)
        return eroded_image
    else:
        return img

# CAMERA CALIBRATION
def calibratecamerabool(bool):
    global calibration_inprogress
    calibration_inprogress = bool
def calibratecamera(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = MathFunctions.CalibrateCamera(gray, frame, CHESSBOARD_INTERSECTION_LINES, CHESSBOARD_INTERSECTION_COLUMNS, DRAW_CALIBRATION_LINES)
    return output

def cameracalibrationprocessor(frameoriginal):
    if USE_CAMERA_CALIBRATION:
        if calibration_inprogress:
            calibresult = calibratecamera(frameoriginal)
            if calibresult[0]:
                update_calibdata_in_configfile(calibresult)
                return calibresult
        else:
            intrinsmat = inistring_to_arrayoffloats(config.get('CALIBRATION_DATA', 'intrinsMat'))
            distcoeffs = inistring_to_arrayoffloats(config.get('CALIBRATION_DATA', 'distcoeffs'))
            rvecs = inistring_to_arrayoffloats(config.get('CALIBRATION_DATA', 'rvecs'))
            tvecs = inistring_to_arrayoffloats(config.get('CALIBRATION_DATA', 'tvecs'))
            imgoriginaxis = inistring_to_arrayoffloats(config.get('CALIBRATION_DATA', 'imgoriginaxis'))
            imgoutercorners = inistring_to_arrayoffloats(config.get('CALIBRATION_DATA', 'imgoutercorners'))
            return (True, frameoriginal, intrinsmat, distcoeffs, rvecs, tvecs, imgoriginaxis, imgoutercorners)
    else:
        return None
    
def update_calibdata_in_configfile(calibdata):
    update_config_value('CALIBRATION_DATA', 'intrinsmat', array_to_ini_string(calibdata[2]))
    update_config_value('CALIBRATION_DATA', 'distcoeffs', array_to_ini_string(calibdata[3]))
    update_config_value('CALIBRATION_DATA', 'rvecs', array_to_ini_string(calibdata[4]))
    update_config_value('CALIBRATION_DATA', 'tvecs', array_to_ini_string(calibdata[5]))
    update_config_value('CALIBRATION_DATA', 'imgoriginaxis', array_to_ini_string(calibdata[6]))
    update_config_value('CALIBRATION_DATA', 'imgoutercorners', array_to_ini_string(calibdata[7]))

def array_to_ini_string(array, delimiter=','):
    if not isinstance(array, (list, np.ndarray)):
        raise ValueError("Input must be a list or numpy.ndarray.")
    array_string = delimiter.join(map(str, array.ravel()))
    return array_string

def inistring_to_arrayoffloats(array_string, delimiter=',', dtype=float):
    # Split the string by the delimiter and convert elements to the specified data type
    elements = array_string.split(delimiter)
    array = [dtype(element) for element in elements]
    return np.array(array, dtype=np.float32)


# apply adjustments to an HSV channel
# https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
def shift_channel(c, amount):
    if amount > 0:
        lim = 255 - amount
        c[c >= lim] = 255
        c[c < lim] += amount
    elif amount < 0:
        amount = -amount
        lim = amount
        c[c <= lim] = 0
        c[c > lim] -= amount
    return c