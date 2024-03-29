import cv2
import numpy as np
import os
import argparse
import configparser
from ast import literal_eval

config = configparser.ConfigParser()
   
class Filterobject:
    def __init__(self):
        self.values = {}
    
def config_color_ranges():

    config.read('config.ini')  # Replace 'config.ini' with the path to your configuration file
    # Defining the color ranges to be filtered.
    low_apple_red = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'low_apple_red'))
    high_apple_red = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'high_apple_red'))
    low_apple_red_2 = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'low_apple_red_2'))
    high_apple_red_2 = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'high_apple_red_2'))
    low_apple_golden = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'low_apple_golden'))
    high_apple_golden = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'high_apple_golden'))
    low_apple_green = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'low_apple_green'))
    high_apple_green = literal_eval(config.get('CUSTOM_DETECTION_CONFIG', 'high_apple_green'))
    return (low_apple_red, high_apple_red, low_apple_red_2, high_apple_red_2, low_apple_golden, high_apple_golden, low_apple_green, high_apple_green)

def convert_hsv_inputs(inputarray):
    # Calculate the converted values
    hue = inputarray[0] / 2
    saturation = inputarray[1] / 100 * 255
    value = inputarray[2] / 100 * 255

    # Return a new tuple with the converted values
    return (hue, saturation, value)

# Function to check if a circle is inside another circle with tolerance
def is_circle_inside_another(circles, new_circle, tolerance=10):
    for circle in circles:
        if abs(circle[0] - new_circle[0]) < tolerance and abs(circle[1] - new_circle[1]) < tolerance and circle[2] > new_circle[2]:
            return True
    return False

def detect(src_img, type, customdetectionfilter):
    if customdetectionfilter is None:
        print("Erro: Falha ao carregar os filtros.")
        return ("Erro", "filtros")
    else:
        color_ranges = config_color_ranges()
        image = src_img.copy()
        #cv2.imwrite("Original image.png", src_img)
        if type == "test_type":
            image_hsv = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)
        else:
            image_hsv = cv2.cvtColor(src_img, cv2.COLOR_RGB2HSV)

        mask_red = cv2.inRange(image_hsv, convert_hsv_inputs(color_ranges[0]), convert_hsv_inputs(color_ranges[1]))
        mask_red_raw = cv2.inRange(image_hsv, convert_hsv_inputs(color_ranges[2]), convert_hsv_inputs(color_ranges[3]))
        mask_golden = cv2.inRange(image_hsv, convert_hsv_inputs(color_ranges[4]), convert_hsv_inputs(color_ranges[5]))
        mask_green = cv2.inRange(image_hsv, convert_hsv_inputs(color_ranges[6]), convert_hsv_inputs(color_ranges[7]))
        mask = mask_red + mask_red_raw + mask_golden + mask_green
        kernel = np.ones((customdetectionfilter.kernelsize, customdetectionfilter.kernelsize), np.uint8)
        if customdetectionfilter.dilate_erode_post_apply or type == "test_type":
            dilated_image = cv2.dilate(mask, kernel, iterations=customdetectionfilter.dilate1)
            eroded_image = cv2.erode(dilated_image, kernel, iterations=customdetectionfilter.erode1)
            dilated2_image = cv2.dilate(eroded_image, kernel, iterations=customdetectionfilter.dilate2)
            eroded2_image = cv2.erode(dilated2_image, kernel, iterations=customdetectionfilter.erode2)
            filteredimage = eroded2_image
        else:
            filteredimage = mask
        
        cnts, _ = cv2.findContours(filteredimage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c_num = 0
        circles = []

        for i, c in enumerate(cnts):
            # Draw a circle enclosing the object
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if r > 100 and not is_circle_inside_another(circles, (x, y, r)):
                c_num += 1
                circles.append((x, y, r))
                cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
                cv2.putText(image, "#{}".format(c_num), (int(x) - 18, int(y-28)), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)     
            
        '''
        # Calculate the histogram
        hist = cv2.calcHist([image_hsv], [0], None, [181], [0, 181])

        # Calculate the histogram
        hist2 = cv2.calcHist([image_hsv], [1], None, [256], [0, 256])

        # Calculate the histogram
        hist3 = cv2.calcHist([image_hsv], [2], None, [256], [0, 256])

        # Plot the histogram
        plt.hist(hist, bins=181, range=(0, 181))
        plt.title('Image Histogram')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.show()

        # Plot the histogram
        plt.hist(hist2, bins=256, range=(0, 256))
        plt.title('Image Histogram')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.show()

        # Plot the histogram
        plt.hist(hist3, bins=256, range=(0, 256))
        plt.title('Image Histogram')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.show()

        '''
        if type == "test_type":
            cv2.imshow("Original image", src_img)
            cv2.imshow("Detected Apples", image)
            cv2.imshow("HSV Image", image_hsv)
            cv2.imshow("Mask Image", mask)
            cv2.imshow("Eroded image", filteredimage)
            '''
            cv2.imwrite("Original image.png", src_img)
            cv2.imwrite("Detected Apples.png", image)
            cv2.imwrite("HSV Image.png", image_hsv)
            cv2.imwrite("Mask Image.png", mask)
            cv2.imwrite("Eroded image.png", filteredimage)
            '''
            cv2.waitKey(0)
        else:
            return (image, circles)
        
if __name__ == '__main__':
    src_img = cv2.imread("C:/Users/JP/Downloads/image-asset.jpeg")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config.read('../config.ini')  # Replace 'config.ini' with the path to your configuration file
    customdetectionfilter = Filterobject()
    customdetectionfilter.minhue = config.getint('FILTER_CONFIG','inputfilters_min_hue')
    customdetectionfilter.maxhue = config.getint('FILTER_CONFIG','inputfilters_max_hue')
    customdetectionfilter.minsat = config.getint('FILTER_CONFIG','inputfilters_min_saturation')
    customdetectionfilter.maxsat = config.getint('FILTER_CONFIG','inputfilters_max_saturation')
    customdetectionfilter.minval = config.getint('FILTER_CONFIG','inputfilters_min_value')
    customdetectionfilter.maxval = config.getint('FILTER_CONFIG','inputfilters_max_value')
    customdetectionfilter.hue_addsub = config.getint('FILTER_CONFIG','inputfilters_hue_modifier')
    customdetectionfilter.sat_addsub = config.getint('FILTER_CONFIG','inputfilters_saturation_modifier')
    customdetectionfilter.val_addsub = config.getint('FILTER_CONFIG','inputfilters_value_modifier')
    customdetectionfilter.gaussianblur = config.getint('FILTER_CONFIG','inputfilters_gaussian_blur')
    customdetectionfilter.blurkernelsize = config.getint('FILTER_CONFIG', 'inputfilters_blur_kernelsize')
    customdetectionfilter.kernelsize = config.getint('FILTER_CONFIG','inputfilters_kernelsize')
    customdetectionfilter.erode1 = config.getint('FILTER_CONFIG','inputfilters_erode1')
    customdetectionfilter.dilate1 = config.getint('FILTER_CONFIG','inputfilters_dilate1')
    customdetectionfilter.erode2 = config.getint('FILTER_CONFIG', 'inputfilters_erode2')
    customdetectionfilter.dilate2 = config.getint('FILTER_CONFIG', 'inputfilters_dilate2')
    customdetectionfilter.dilate_erode_post_apply = config.getboolean('FILTER_CONFIG', 'inputfilters_post-apply_dilate_and_erode')
    # ======================== \\-// ========================
    detect(src_img, "test_type", customdetectionfilter)
