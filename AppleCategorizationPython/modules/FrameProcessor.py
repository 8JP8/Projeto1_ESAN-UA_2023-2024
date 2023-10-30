from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.QtGui import QIcon
from modules import code_v1
import cv2
import os
import numpy as np
import configparser
os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read('../config.ini')  # Replace 'config.ini' with the path to your configuration file

currentvideopath = ""
applyfilters = config.getboolean('FILTER_CONFIG', 'apply_filters')

def ImageProcessor(img_filepath, frame, threshold1, threshold2, filter):
    if os.path.isfile(img_filepath):
        try:
            frame = code_v1.detect_and_classify_apples(frame, "image", threshold1, threshold2)
            if applyfilters and filter!=None:
                frame = ApplyFilters(frame, filter)
            return (True, frame)
        except:
            return(False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(img_filepath)}'.")
    else:
        return(False, f"Erro: Imagem '{os.path.basename(img_filepath)}' não encontrada.")
        

def VideoProcessor(vd_filepath, frame, threshold1, threshold2, filter):
    if (currentvideopath == "") or (currentvideopath != vd_filepath):
        if os.path.isfile(vd_filepath):
            cap = cv2.VideoCapture(vd_filepath)
            if not cap.isOpened():
                return (False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(vd_filepath)}'.")
            else:
                newframe = code_v1.detect_and_classify_apples(frame, "video", threshold1, threshold2)
                if applyfilters and filter!=None:
                    newframe = ApplyFilters(newframe, filter)
                return (True, newframe)
        else:
            return (False, f"Erro: Vídeo '{os.path.basename(vd_filepath)}' não encontrado.")
    else:
        try:
            newframe = code_v1.detect_and_classify_apples(frame, "video")
            if applyfilters and filter!=None:
                newframe = ApplyFilters(newframe, filter)
            return (True, newframe)
        except:
            return(False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(vd_filepath)}'.")
        
def CameraProcessor(self, inputframe, threshold1, threshold2, filter):
    # Detect and classify apples and update the frame
    try:
        frame = code_v1.detect_and_classify_apples(inputframe, "camera", threshold1, threshold2)
    except:
        try:
            frame = code_v1.detect_and_classify_apples(inputframe, "camera", threshold1, threshold2)
        except:
            try: #Try 3 times to display frames before giving error
                frame = code_v1.detect_and_classify_apples(inputframe, "camera", threshold1, threshold2)
            except:
                return(False, f"Erro: O processamento de frames falhou.")
    if applyfilters and filter!=None:
        frame = ApplyFilters(frame, filter)
    return (True, frame)

def ApplyFilters(imageframe, guifvalues):
    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    # convert image to HSV
    hsv = cv2.cvtColor(imageframe, cv2.COLOR_BGR2HSV)
    # add/subtract saturation and value
    h, s, v = cv2.split(hsv)
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
        eroded_image = cv2.erode(result, kernel, iterations=guifvalues.cannyerode)
        dilated_image = cv2.dilate(eroded_image, kernel, iterations=guifvalues.cannydilate)
        # canny edge detection
        result = cv2.Canny(dilated_image, guifvalues.canny1, guifvalues.canny2)
        # Apply output dilation and erosion to the grayscale image
        output_eroded_image = cv2.erode(result, kernel, iterations=guifvalues.output_erode)
        output_dilated_image = cv2.dilate(output_eroded_image, kernel, iterations=guifvalues.output_dilate)
        # convert single channel image back to BGR
        img = cv2.cvtColor(output_dilated_image, cv2.COLOR_GRAY2BGR)
    elif guifvalues.enablesobel:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, kernel, scale=1)
        y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, kernel, scale=1)
        absx = cv2.convertScaleAbs(x)
        absy = cv2.convertScaleAbs(y)
        edge = cv2.addWeighted(absx, 0.5, absy, 0.5, 0)
        # Apply output dilation and erosion to the grayscale image
        output_eroded_image = cv2.erode(edge, kernel, iterations=guifvalues.output_erode)
        output_dilated_image = cv2.dilate(output_eroded_image, kernel, iterations=guifvalues.output_dilate)
        # convert single channel image back to BGR
        img = cv2.cvtColor(output_dilated_image, cv2.COLOR_GRAY2BGR)
    elif guifvalues.enablelaplace:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=guifvalues.kernelsize)
        # Apply output dilation and erosion to the grayscale image
        output_eroded_image = cv2.erode(laplacian, kernel, iterations=guifvalues.output_erode)
        output_dilated_image = cv2.dilate(output_eroded_image, kernel, iterations=guifvalues.output_dilate)
        # Convert from 64-bit float to 8-bit unsigned integer
        output_dilated_image = cv2.convertScaleAbs(output_dilated_image)
        # convert single channel image back to BGR
        img = cv2.cvtColor(output_dilated_image, cv2.COLOR_GRAY2BGR)

    return img

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