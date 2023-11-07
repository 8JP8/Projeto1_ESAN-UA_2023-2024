import math
import numpy as np
import cv2

#old not accurate conversion
def pixels_to_cm(pixels, camera_height_cm, field_of_view_degrees, camera_distance_cm):
    field_of_view_radians = math.radians(field_of_view_degrees)
    cm_per_pixel = (2 * camera_distance_cm * math.tan(field_of_view_radians / 2)) / camera_height_cm
    centimeters = pixels * cm_per_pixel
    return centimeters

############################################################################################
# Section: Single Camera 3D Positioning
############################################################################################ 

def CalibrateCamera(searchFrame,drawFrame,intersecLines,intersecCols,draw):
    # Subpixel criteria
    subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((intersecLines*intersecCols,3), np.float32)
    objp[:,:2] = np.mgrid[0:intersecLines,0:intersecCols].T.reshape(-1,2)
    calibObjPoints = []
    calibImgPoints = []
    ret, corners = cv2.findChessboardCornersSB(searchFrame, (intersecLines,intersecCols), cv2.CALIB_CB_LARGER + cv2.CALIB_CB_MARKER)
    if ret:
        calibObjPoints.append(objp)
        corners2 = cv2.cornerSubPix(searchFrame,corners, (11,11), (-1,-1), subpix_criteria)
        calibImgPoints.append(corners2)
        if draw:
            cv2.drawChessboardCorners(drawFrame, (intersecLines,intersecCols), corners2, ret)
            for index, crn in enumerate(corners2):
                cv2.putText(drawFrame,str(index),(int(crn[0][0]),int(crn[0][1])),cv2.FONT_HERSHEY_COMPLEX,0.5,(127,127,127),1)
        ret, intrinsMat, distCoeffs, rVecs, tVecs = cv2.calibrateCamera(calibObjPoints, calibImgPoints, searchFrame.shape[::-1], None, None)    
        if ret:
            #intrinsMat, ROIR =cv2.getOptimalNewCameraMatrix(intrinsMat,distCoeffs,searchFrame.shape[::-1], 1)
            rVecs = rVecs[0]
            tVecs = tVecs[0]
            originAxis = np.float32([[0,0,0], [1,0,0], [0,1,0], [0,0,-1]])
            chessHeight = float(intersecLines - 1)
            chesWidth = float(intersecCols - 1)
            outerCorners = np.float32([[0,0,0], [0.3,0,0], [0,0.3,0],
                                    [chessHeight,0,0], [chessHeight-0.3,0,0], [chessHeight,0.3,0],
                                    [0,chesWidth,0], [0.3,chesWidth,0], [0,chesWidth-0.3,0],
                                    [chessHeight,chesWidth,0], [chessHeight-0.3,chesWidth,0], [chessHeight,chesWidth-0.3,0]])
            imgOriginAxis, jac = cv2.projectPoints(originAxis, rVecs, tVecs, intrinsMat, distCoeffs)
            imgOuterCorners, jac = cv2.projectPoints(outerCorners, rVecs, tVecs, intrinsMat, distCoeffs) 
            extMatrix=intrinsMat.dot(np.hstack((cv2.Rodrigues(rVecs)[0],tVecs)))
            return True, drawFrame, intrinsMat, distCoeffs, rVecs, tVecs, imgOriginAxis, imgOuterCorners
        else:
            return False, 0, 0, 0, 0, 0, 0, 0
    else:
        return False, 0, 0, 0, 0, 0, 0, 0

    

def calculate_apple_width_in_mm(apple_quadrants, sensor_width_mm, intrinsMat, distCoeffs, rVecs, tVecs, apple_Z, square_size):
    # Use cv2.solvePnP with SOLVEPNP_P3P to estimate rotation and translation vectors
    intrinsMat = np.array([[intrinsMat[0],intrinsMat[1],intrinsMat[2]],[intrinsMat[3],intrinsMat[4],intrinsMat[5]],[intrinsMat[6],intrinsMat[7],intrinsMat[8]]],dtype=np.float32) 
    undistorted_points = cv2.undistortPoints(apple_quadrants, intrinsMat, distCoeffs)
    extMatrix=intrinsMat.dot(np.hstack((cv2.Rodrigues(rVecs,tVecs))))
    # Project the object points (same as image points) onto the image
    image_points = UnProject(apple_quadrants, extMatrix, apple_Z, square_size)

    # Calculate the width of the object in pixels
    width_pixels1 = np.linalg.norm(image_points[2] - image_points[0])
    width_pixels2 = np.linalg.norm(image_points[3] - image_points[1])
    width_pixels = (width_pixels1+width_pixels2)/2

    # Calculate pixel-to-mm conversion factor using the sensor width
    pixel_to_mm = sensor_width_mm / intrinsMat[0, 2]

    # Convert the width measurement to real-world units (millimeters)
    width_mm = width_pixels * pixel_to_mm
    
    return width_mm

#Unproject Points Function to Give points coordinates in the real world based on the reference point.
def UnProject(imgPoints, extMatrix, Z, sqSize):
    positions = []
    for imgPoint in imgPoints:
        pos = np.linalg.inv(np.hstack((extMatrix[:,0:2],np.array([[-1*imgPoint[0]],[-1*imgPoint[1]],[-1]])))).dot((-Z*extMatrix[:,2]-extMatrix[:,3]))
        pos[0] *=  sqSize
        pos[1] *=  sqSize
        pos[2] = Z
        positions.append(pos)
    return positions


'''
# Sample values for testing
apple_corners = np.array([
                            [0, 0],
                            [1, 0],
                            [0, 1],
                            [3, 1]
                        ], dtype=np.float32)
sensor_width_mm = 35.9  # Replace with your camera's sensor width
intrinsMat = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32)  # Replace with actual intrinsMat
distCoeffs = np.array([0.1, -0.2, 0.01, 0.001, 0.05], dtype=np.float32)  # Replace with actual distCoeffs
rVecs = np.array([0.1, 0.2, -0.3], dtype=np.float32)  # Replace with actual rVecs
tVecs = np.array([1.0, -2.0, 3.0], dtype=np.float32)  # Replace with actual tVecs

# Call the function
width_mm = calculate_apple_width_in_mm(apple_corners, sensor_width_mm, intrinsMat, distCoeffs, rVecs, tVecs)

print("Width of the apple in millimeters:", width_mm)
'''