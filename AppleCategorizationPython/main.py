from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QDialog, QWidget, QTabWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap, QIcon, QCloseEvent, QAction, QKeySequence, QShortcut
import numpy as np
import threading
import subprocess
import time
import os
import sys
import cv2
import configparser

# ============ MODULES ============
from modules import FrameProcessor
from modules import code_v1
# ============= \\-// =============

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read('config.ini')  # Replace 'config.ini' with the path to your configuration file


# CONFIG GLOBAL VARIABLES
USE_TWO_CAMERAS = config.getboolean('CAMERA_CONFIG', 'USE_TWO_CAMERAS')
CAMERA_INDEX_LEFT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_LEFT')    # Camera index for the left camera (if using two cameras)
CAMERA_INDEX_RIGHT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_RIGHT')

class MyApp(QMainWindow):                     #GUI CLASS
    def __init__(self):                       # CONSTRUCTOR
        super (MyApp, self).__init__()
        loadUi('ui/app.ui', self)
        app.setWindowIcon(QIcon('ui/icons/apple.ico'))
        self.pid = QApplication.applicationPid()
        
        # ============ INICIALIZAÇÃO COM OS VALORES DA CONFIG ============
        self.threshold1_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threshold1_value'))
        self.threshold2_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threshold2_value'))
        self.mode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'mode_value'))
        self.detectionmode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'detectionmode_value'))
        self.categorizationmode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'categorizationmode_value'))
        self.cam2_RADIOBT.setChecked(config.getboolean('CAMERA_CONFIG', 'use_two_cameras'))
        # ============================= \\-// ============================

        # ============ BINDS ============
        self.upload_BT.clicked.connect(self.load_file)
        self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+I"))
        self.start_BT.clicked.connect(self.start_cameracapture)
        self.colorfilters_BT.clicked.connect(self.colorfilters_open)
        self.actionOpen_Upload.setShortcuts([QKeySequence.fromString("Ctrl+O"), QKeySequence.fromString("Ctrl+A")])
        self.actionOpen_Upload.triggered.connect(self.load_file)
        self.actionSave_Output_File.triggered.connect(self.save_file)
        self.actionSave_Output_File.setShortcuts([QKeySequence.fromString("Ctrl+S"), QKeySequence.fromString("Ctrl+G")])
        self.action_small_view.triggered.connect(self.small_vw)
        self.action_big_view.triggered.connect(self.big_vw)
        self.action_small_view.setShortcut("Ctrl+Left")
        self.action_big_view.setShortcut("Ctrl+Right")
        self.action_restartprogram.triggered.connect(self.restartprogram)
        #self.menuLogs.aboutToShow.connect(self.logs_open)
        #self.shortcut = QShortcut(QKeySequence('Ctrl+L'), self)
        #self.shortcut.activated.connect(self.logs_open) 
        self.action_logs_open.triggered.connect(self.logs_open)
        self.action_logs_export.triggered.connect(self.logs_save)
        self.action_logs_open.setShortcut("Ctrl+L")
        self.action_logs_export.setShortcut("Ctrl+Shift+L")
        self.menuInfo.aboutToShow.connect(self.info_open)
        self.threshold1_SLIDER.valueChanged.connect(self.update_config)
        self.threshold2_SLIDER.valueChanged.connect(self.update_config)
        self.mode_COMBOBOX.currentIndexChanged.connect(self.update_config)
        self.detectionmode_COMBOBOX.currentIndexChanged.connect(self.update_config)
        self.categorizationmode_COMBOBOX.currentIndexChanged.connect(self.update_config)
        self.cam1_RADIOBT.toggled.connect(self.update_config)
        self.cam2_RADIOBT.toggled.connect(self.update_config)
        # Create shortcuts to move up and down in the tabs
        shortcut_up = QKeySequence.fromString("Ctrl+Up")
        shortcut_down = QKeySequence.fromString("Ctrl+Down")
        # Connect the shortcuts to custom slot functions
        self.createShortcut(shortcut_up, self.moveTabUp)
        self.createShortcut(shortcut_down, self.moveTabDown)
        # ============ \\-// ============
        self.videoplaying = False
        self.camopen = False
        self.thread_stop_flag = False
        self.filename = str()
        # ============ \\-// ============

    def createShortcut(self, key_sequence, slot_function):
        shortcut = key_sequence
        action = QAction(self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot_function)
        self.addAction(action)

    def moveTabUp(self):
        current_index = self.big_view_tabwidget.currentIndex()
        new_index = (current_index + 1) % self.big_view_tabwidget.count()
        self.big_view_tabwidget.setCurrentIndex(new_index)

    def moveTabDown(self):
        current_index = self.big_view_tabwidget.currentIndex()
        new_index = current_index - 1 if current_index > 0 else self.big_view_tabwidget.count() - 1
        self.big_view_tabwidget.setCurrentIndex(new_index)

    def load_file(self): #FUNCTION TO OPEN THE IMAGE SELECTOR AND SELECT THE IMAGE
        if self.videoplaying:
            self.show_warning("Está a ser processado vídeo: Carregue PARAR (Ctrl+P) ou feche a App.")
        else:
            self.filename = QFileDialog.getOpenFileName(
                filter = "Ficheiros Suportados (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.pbm *.pgm *.ppm *.xbm *.xpm *.sr *.webp *.avi *.mov *.mp4 *.mkv *.wmv *.flv *.3gp *.asf *.mpg *.rm);;Ficheiros de Imagem (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.pbm *.pgm *.ppm *.xbm *.xpm *.sr *.webp);;Ficheiros de Vídeo (*.avi *.mov *.mp4 *.mkv *.wmv *.flv *.3gp *.asf *.mpg *.rm);;Todos os Ficheiros (*)")[0]
            if len(self.filename)!=0:
                self.image = cv2.imread(self.filename)
                if self.image is not None:
                    self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
                    image = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2RGB)
                    self.set_image(image)
                else:
                    print("Processamento de Frames Iniciado")
                    threading.Thread(target=self.video_processing_thread, args=(self.filename,)).start()
    
    def set_image(self, image): #FUNCTION TO PUT THE INPUT IMAGE IN THE FRAME
            if len(self.filename)!=0:
                # ============= OLD RESIZE CODE TO FIT THE IMAGE ============ →→→→→→→→→→→→  frame = imutils.resize(image, width=self.inputframe_1.width, height=self.inputframe_1.height)
                # ========= CALCULATIONS TO KEEP IMAGE ASPECT RATIO =========
                width_scalei = int(self.inputframe_1.width()) / image.shape[1]
                height_scalei = int(self.inputframe_1.height()) / image.shape[0]
                scalei = min(width_scalei, height_scalei)
                framei = cv2.resize(image, (int(image.shape[1] * scalei), int(image.shape[0] * scalei)))
                # ======== CALCULATIONS TO KEEP IMAGE ASPECT RATIO 2 ========
                width_scale2i = int(self.inputframe_3.width()) / image.shape[1]
                height_scale2i = int(self.inputframe_3.height()) / image.shape[0]
                scale2i = min(width_scale2i, height_scale2i)
                frame2i = cv2.resize(image, (int(image.shape[1] * scale2i), int(image.shape[0] * scale2i)))
                # ====================== CENTER THE IMAGE ====================== 
                emptyframei = np.full((self.inputframe_1.height(), self.inputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                x_offseti = (self.inputframe_1.width() - framei.shape[1]) // 2
                y_offseti = (self.inputframe_1.height() - framei.shape[0]) // 2
                emptyframei[y_offseti:y_offseti+framei.shape[0], x_offseti:x_offseti+framei.shape[1]] = framei       # Paste the resized image onto the empty frame
                # ====================== CENTER THE IMAGE ====================== 
                emptyframe2i = np.full((self.inputframe_3.height(), self.inputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                x_offset2i = (self.inputframe_3.width() - frame2i.shape[1]) // 2
                y_offset2i = (self.inputframe_3.height() - frame2i.shape[0]) // 2
                emptyframe2i[y_offset2i:y_offset2i+frame2i.shape[0], x_offset2i:x_offset2i+frame2i.shape[1]] = frame2i
                # ==================== CONVERT IMAGE FORMAT ====================
                # ======================= UPDATE THE GUI =======================
                imagef = QImage(emptyframei, emptyframei.shape[1],emptyframei.shape[0], emptyframei.strides[0],QImage.Format.Format_RGB888)
                imagef2 = QImage(emptyframe2i, emptyframe2i.shape[1],emptyframe2i.shape[0], emptyframe2i.strides[0],QImage.Format.Format_RGB888)
                self.inputframe_1.setPixmap(QPixmap.fromImage(imagef))
                self.inputframe_3.setPixmap(QPixmap.fromImage(imagef2))
                # =========================== \\--// ===========================
                processedimage = FrameProcessor.ImageProcessor(self.filename, image, self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value())
                if not processedimage[0]:
                    self.show_warning(processedimage[1])
                else:
                    # ===================== CENTER THE IMAGE =====================
                    framepi = cv2.resize(processedimage[1], (framei.shape[1], framei.shape[0]))
                    framep2i = cv2.resize(processedimage[1], (frame2i.shape[1], frame2i.shape[0]))
                    emptyframepi = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframepi[y_offseti:y_offseti+framei.shape[0], x_offseti:x_offseti+framei.shape[1]] = framepi                      # Paste the resized image onto the empty frame
                    emptyframep2i = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                    emptyframep2i[y_offset2i:y_offset2i+frame2i.shape[0], x_offset2i:x_offset2i+frame2i.shape[1]] = framep2i                 # Paste the resized image onto the empty frame
                    # Paste the resized image onto the empty frame
                    # ======================== UPDATE THE GUI ========================
                    imagepi = QImage(emptyframepi, emptyframepi.shape[1],emptyframepi.shape[0], emptyframepi.strides[0],QImage.Format.Format_RGB888)
                    imagep2i = QImage(emptyframep2i, emptyframep2i.shape[1],emptyframep2i.shape[0], emptyframep2i.strides[0],QImage.Format.Format_RGB888)
                    self.outputframe_1.setPixmap(QPixmap.fromImage(imagepi))
                    self.outputframe_3.setPixmap(QPixmap.fromImage(imagep2i))
                    # ============================ \\--// ============================
        

    # ======= START AND CLOSE FUNCTIONS =======  
    def restartprogram(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    def closeEvent(self, event: QCloseEvent):
        self.thread_stop_flag = True
        self.colorfilters = ColorFilters()
        self.colorfilters.close() #close filters widget when mainwindow closes
    def video_processing_thread(self, filename):
        self.set_video(filename)
    def cameracapture_to_gui_thread(self):
        self.cameracapture_to_gui()
    # ========================== \\--// ==========================
     
    def set_video(self, video):
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            self.show_warning("Falha ao abrir o ficheiro de vídeo.")
            return
        # Getting video informations for progressbar
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Create a VideoCapture object
        while not self.thread_stop_flag:
            self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+P"))
            ret, frame = cap.read()
            if not ret:
                break  # Break the loop at the end of the video
            self.videoplaying = True #bool to stop uploads while playing
            # Getting video informations for progressbar
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            progress = (current_frame / self.total_frames) * 100
            self.progressBar.setValue(int(progress))
            # Calculate the scale and apply resizing
            self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2RGB)
            processoriginalquality = frame
            width_scale = int(self.inputframe_1.width()) / frame.shape[1]
            height_scale = int(self.inputframe_1.height()) / frame.shape[0]
            scale = min(width_scale, height_scale)
            frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))
            #Calculate the scale and apply resizing 2
            width_scale2 = int(self.inputframe_3.width()) / frame.shape[1]
            height_scale2 = int(self.inputframe_3.height()) / frame.shape[0]
            scale2 = min(width_scale2, height_scale2)
            frame2 = cv2.resize(frame, (int(frame.shape[1] * scale2), int(frame.shape[0] * scale2)))
            # Center the image
            emptyframe = np.full((self.inputframe_1.height(), self.inputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
            x_offset = (self.inputframe_1.width() - frame.shape[1]) // 2
            y_offset = (self.inputframe_1.height() - frame.shape[0]) // 2
            emptyframe[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
            # Center the image 2
            emptyframe2 = np.full((self.inputframe_3.height(), self.inputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
            x_offset2 = (self.inputframe_3.width() - frame2.shape[1]) // 2
            y_offset2 = (self.inputframe_3.height() - frame2.shape[0]) // 2
            emptyframe2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = frame2
            # Convert image format
            image = QImage(emptyframe, emptyframe.shape[1], emptyframe.shape[0], emptyframe.strides[0], QImage.Format.Format_RGB888)
            image2 = QImage(emptyframe2, emptyframe2.shape[1], emptyframe2.shape[0], emptyframe2.strides[0], QImage.Format.Format_RGB888)
            # Update the GUI
            self.inputframe_1.setPixmap(QPixmap.fromImage(image))
            self.inputframe_3.setPixmap(QPixmap.fromImage(image2))
            
            #frame processing
            processor_result = FrameProcessor.VideoProcessor(video, processoriginalquality, self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value())
            if not processor_result[0]:
                self.show_warning(processor_result[1])
            else:
                # Ensure that processedvideoframe has the same dimensions as the target area
                processedvideoframe = cv2.resize(processor_result[1], (frame.shape[1], frame.shape[0]))
                processedvideoframe2 = cv2.resize(processor_result[1], (frame2.shape[1], frame2.shape[0]))
                # Create an empty frame with the target dimensions
                emptyframep = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
                emptyframep2 = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
                # Paste the resized frame onto the target area in emptyframep
                emptyframep[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = processedvideoframe
                emptyframep2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = processedvideoframe2
                # Convert image format
                videoframep = QImage(emptyframep, emptyframep.shape[1], emptyframep.shape[0], emptyframep.strides[0], QImage.Format.Format_RGB888)
                videoframep2 = QImage(emptyframep2, emptyframep2.shape[1], emptyframep2.shape[0], emptyframep2.strides[0], QImage.Format.Format_RGB888)
                # Update the GUI
                self.outputframe_1.setPixmap(QPixmap.fromImage(videoframep))
                self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep2))
        self.start_BT.setText("INICIAR\n(Ctrl+I)")
        self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+I"))
        self.videoplaying = False
        self.thread_stop_flag = False
        
    def start_cameracapture(self):
        if self.videoplaying:
            self.thread_stop_flag = True #STOP VIDEO PLAYBACK / CAMERA PLAYBACK
            if  self.camopen:
                self.camopen = False
            self.start_BT.setText("INICIAR\n(Ctrl+I)")
            self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+I"))
        else:
            #Camera Test
            # Try to access the default camera (usually the built-in webcam)
            if USE_TWO_CAMERAS:
                self.cap_left = cv2.VideoCapture(CAMERA_INDEX_LEFT)
                self.cap_right = cv2.VideoCapture(CAMERA_INDEX_RIGHT)
                return self.cap_left, self.cap_right
            else:
                self.camera = cv2.VideoCapture(0)  # 0 represents the default camera
            # Check if the camera was opened successfully
            if self.camera.isOpened():
                self.camopen = True
                self.start_BT.setText("PARAR\n(Ctrl+P)")
                self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+P"))
                print("Processamento de Frames Iniciado")
                threading.Thread(target=self.cameracapture_to_gui_thread).start() #Updates the gui with camera feed
            
    def cameracapture_to_gui(self):
        # Create a VideoCapture object
        while not self.thread_stop_flag:
            if USE_TWO_CAMERAS:
                self.camera=self.cap_left.read()
                ret_left, frame_left = self.cap_left.read()
                ret_right, frame_right = self.cap_right.read()
                # Calculate the scale and apply resizing
                self.hsv_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2HSV)
                frame = cv2.cvtColor(self.hsv_left, cv2.COLOR_HSV2RGB)
                self.hsv_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2HSV)
                frame_right = cv2.cvtColor(self.hsv_right, cv2.COLOR_HSV2RGB)
                if not ret_left or not ret_right:
                    break
            else:
                ret, frame = self.camera.read()
                # Calculate the scale and apply resizing
                self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                frame = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2RGB)
                if not ret:
                    break
            self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+P"))
            if not ret:
                break  # Break the loop at the end of the video
            self.videoplaying = True #bool to stop uploads while playing
            #############################################################
            width_scale = int(self.inputframe_1.width()) / frame.shape[1]
            height_scale = int(self.inputframe_1.height()) / frame.shape[0]
            scale = min(width_scale, height_scale)
            frameoriginal = frame
            frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))
            #Calculate the scale and apply resizing 2
            width_scale2 = int(self.inputframe_3.width()) / frame.shape[1]
            height_scale2 = int(self.inputframe_3.height()) / frame.shape[0]
            scale2 = min(width_scale2, height_scale2)
            frame2 = cv2.resize(frame, (int(frame.shape[1] * scale2), int(frame.shape[0] * scale2)))
            # Center the image
            emptyframe = np.full((self.inputframe_1.height(), self.inputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
            x_offset = (self.inputframe_1.width() - frame.shape[1]) // 2
            y_offset = (self.inputframe_1.height() - frame.shape[0]) // 2
            # Center the image 2
            emptyframe2 = np.full((self.inputframe_3.height(), self.inputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
            x_offset2 = (self.inputframe_3.width() - frame2.shape[1]) // 2
            y_offset2 = (self.inputframe_3.height() - frame2.shape[0]) // 2
            if USE_TWO_CAMERAS:
                frameoriginal2 = frame_right
                frame3 = cv2.resize(frame_right, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))
                frame4 = cv2.resize(frame_right, (int(frame.shape[1] * scale2), int(frame.shape[0] * scale2)))
                #paste frames in empyframes
                emptyframe3 = emptyframe
                emptyframe4 = emptyframe2
                emptyframe[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
                emptyframe2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = frame2
                emptyframe3[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame3
                emptyframe4[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = frame4
                # Convert image format
                image = QImage(emptyframe, emptyframe.shape[1], emptyframe.shape[0], emptyframe.strides[0], QImage.Format.Format_RGB888)
                image2 = QImage(emptyframe2, emptyframe2.shape[1], emptyframe2.shape[0], emptyframe2.strides[0], QImage.Format.Format_RGB888)
                image3 = QImage(emptyframe3, emptyframe.shape[1], emptyframe.shape[0], emptyframe.strides[0], QImage.Format.Format_RGB888)
                image4 = QImage(emptyframe4, emptyframe2.shape[1], emptyframe2.shape[0], emptyframe2.strides[0], QImage.Format.Format_RGB888)
                # Update the GUI
                self.inputframe_1.setPixmap(QPixmap.fromImage(image))
                self.inputframe_3.setPixmap(QPixmap.fromImage(image2))
                self.inputframe_2.setPixmap(QPixmap.fromImage(image3))
                self.inputframe_4.setPixmap(QPixmap.fromImage(image4))
                # Frame processing
                processor_result = FrameProcessor.CameraProcessor(self, frameoriginal, self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value())
                processor_result2 = FrameProcessor.CameraProcessor(self, frameoriginal2, self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value())
                if not processor_result[0] or not processor_result2[0]:
                    self.show_warning(processor_result[1])
                else:
                    # Ensure that processedvideoframe has the same dimensions as the target area
                    processedvideoframe = cv2.resize(processor_result[1], (frame.shape[1], frame.shape[0]))
                    processedvideoframe2 = cv2.resize(processor_result[1], (frame2.shape[1], frame2.shape[0]))
                    processedvideoframe3 = cv2.resize(processor_result2[1], (frame.shape[1], frame.shape[0]))
                    processedvideoframe4 = cv2.resize(processor_result2[1], (frame2.shape[1], frame2.shape[0]))
                    # Create an empty frame with the target dimensions
                    emptyframep3, emptyframep = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
                    emptyframep4, emptyframep2 = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
                    # Paste the resized frame onto the target area in emptyframep
                    emptyframep[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = processedvideoframe
                    emptyframep2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = processedvideoframe2
                    emptyframep3[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = processedvideoframe3
                    emptyframep4[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = processedvideoframe4
                    # Convert image format
                    videoframep = QImage(emptyframep, emptyframep.shape[1], emptyframep.shape[0], emptyframep.strides[0], QImage.Format.Format_RGB888)
                    videoframep2 = QImage(emptyframep2, emptyframep2.shape[1], emptyframep2.shape[0], emptyframep2.strides[0], QImage.Format.Format_RGB888)
                    videoframep3 = QImage(emptyframep3, emptyframep.shape[1], emptyframep.shape[0], emptyframep.strides[0], QImage.Format.Format_RGB888)
                    videoframep4 = QImage(emptyframep4, emptyframep2.shape[1], emptyframep2.shape[0], emptyframep2.strides[0], QImage.Format.Format_RGB888)
                    # Update the GUI
                    self.outputframe_1.setPixmap(QPixmap.fromImage(videoframep))
                    self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep2))
                    self.outputframe_2.setPixmap(QPixmap.fromImage(videoframep3))
                    self.outputframe_4.setPixmap(QPixmap.fromImage(videoframep4))
            else:
                emptyframe[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
                emptyframe2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = frame2
                image = QImage(emptyframe, emptyframe.shape[1], emptyframe.shape[0], emptyframe.strides[0], QImage.Format.Format_RGB888)
                image2 = QImage(emptyframe2, emptyframe2.shape[1], emptyframe2.shape[0], emptyframe2.strides[0], QImage.Format.Format_RGB888)
                self.inputframe_1.setPixmap(QPixmap.fromImage(image))
                self.inputframe_3.setPixmap(QPixmap.fromImage(image2))
                processor_result = FrameProcessor.CameraProcessor(self, frame, self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value())

                if not processor_result[0]:
                    self.show_warning(processor_result[1])
                else:
                    # Ensure that processedvideoframe has the same dimensions as the target area
                    processedvideoframe = cv2.resize(processor_result[1], (frame.shape[1], frame.shape[0]))
                    processedvideoframe2 = cv2.resize(processor_result[1], (frame2.shape[1], frame2.shape[0]))
                    # Create an empty frame with the target dimensions
                    emptyframep = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
                    emptyframep2 = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
                    # Paste the resized frame onto the target area in emptyframep
                    emptyframep[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = processedvideoframe
                    emptyframep2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = processedvideoframe2
                    # Convert image format
                    videoframep = QImage(emptyframep, emptyframep.shape[1], emptyframep.shape[0], emptyframep.strides[0], QImage.Format.Format_RGB888)
                    videoframep2 = QImage(emptyframep2, emptyframep2.shape[1], emptyframep2.shape[0], emptyframep2.strides[0], QImage.Format.Format_RGB888)
                    # Update the GUI
                    self.outputframe_1.setPixmap(QPixmap.fromImage(videoframep))
                    self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep2))

        self.start_BT.setText("INICIAR\n(Ctrl+I)")
        self.start_BT.setShortcut(QKeySequence.fromString("Ctrl+I"))
        self.videoplaying = False
        self.thread_stop_flag = False
        # Release the camera when you're done
        self.camera.release()

    def small_vw(self):
        self.stackedWidget.setCurrentIndex(0)
        self.resize(771, 584)
    def big_vw(self):
        self.stackedWidget.setCurrentIndex(1)
        self.resize(771, 584)
    def save_file(self, filepath):
        savefile_dialog_path, _ = QFileDialog.getSaveFileName(self, "Guardar", "", "All Files (*);;Text Files (*.txt)")
        if savefile_dialog_path:
            # Copy a file  to the chosen path
            with open(filepath, "rb") as src_file, open(savefile_dialog_path, "wb") as dest_file:
                dest_file.write(src_file.read())

    def logs_save(self):
        savefile_dialog_path, _ = QFileDialog.getSaveFileName(self, "Guardar Ficheiro de Logs", "", "All Files (*);;Text Files (*.txt)")
        if savefile_dialog_path:
            # Copy logs file to the chosen path
            source_file = config.get('LOGS_CONFIG', 'LOGS_FILE_PATH')
            with open(source_file, "rb") as src_file, open(savefile_dialog_path, "wb") as dest_file:
                dest_file.write(src_file.read())

    def logs_open(self):
        file_path = config.get('LOGS_CONFIG', 'LOGS_FILE_PATH')
        if sys.platform.startswith('win'):
            os.startfile(file_path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', file_path])
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', file_path])
        else:
            print("Unsupported operating system: Cannot open the file.")
    
    def colorfilters_open(self):    
        self.colorfilters = ColorFilters()
        self.colorfilters.show()

    def info_open(self):    
        info_dialog = AboutDialog()
        info_dialog.exec()
    
    def update_config(self):
        config.set('DETECTION_CONFIG', 'threshold1_value', str(self.threshold1_SLIDER.value()))
        config.set('DETECTION_CONFIG', 'threshold2_value', str(self.threshold2_SLIDER.value()))
        config.set('DETECTION_CONFIG', 'mode_value', str(self.mode_COMBOBOX.currentIndex()))
        config.set('DETECTION_CONFIG', 'detectionmode_value', str(self.detectionmode_COMBOBOX.currentIndex()))
        config.set('DETECTION_CONFIG', 'categorizationmode_value', str(self.categorizationmode_COMBOBOX.currentIndex()))
        config.set('CAMERA_CONFIG', 'use_two_cameras', str(self.cam2_RADIOBT.isChecked()))
        
        # Save the changes
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    
    # =========================== ALERTS ===========================
    def show_warning(self, msg):
        self.show_alert("Aviso", msg, QMessageBox.Icon.Warning)

    def show_error(self, msg):
        self.show_alert("Erro", msg, QMessageBox.Icon.Critical)

    def show_info(self, msg):
        self.show_alert("Informação", msg, QMessageBox.Icon.Information)

    # ===============================================================
    def show_alert(self, title, msg, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowIcon(QIcon('ui/icons/apple.ico'))
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setIcon(icon)  # Use QMessageBox.Icon.Warning for a warning icon
        msg_box.exec()

# =========================== \\---// ===========================
class ColorFilters(QWidget):
    def __init__(self):
        super().__init__()
        # Load the widget UI file
        loadUi('ui/filters.ui', self)

        #Initialize the Values from the Config File
        self.minhue_slider.setValue(config.getint('FILTER_CONFIG','min_hue'))
        self.minhue_slider.setValue(config.getint('FILTER_CONFIG','max_hue'))
        self.minsat_slider.setValue(config.getint('FILTER_CONFIG','min_saturation'))
        self.maxsat_slider.setValue(config.getint('FILTER_CONFIG','max_saturation'))
        self.minval_slider.setValue(config.getint('FILTER_CONFIG','min_value'))
        self.maxval_slider.setValue(config.getint('FILTER_CONFIG','max_value'))
        self.sataddsub_slider.setValue(config.getint('FILTER_CONFIG','saturation_multiplier'))
        self.valaddsub_slider.setValue(config.getint('FILTER_CONFIG','value_multiplier'))
        self.kernelsize_slider.setValue(config.getint('FILTER_CONFIG','kernelsize'))
        self.erodelter_slider.setValue(config.getint('FILTER_CONFIG','erode'))
        self.dilatelter_slider.setValue(config.getint('FILTER_CONFIG','dilate'))
        self.canny1_slider.setValue(config.getint('FILTER_CONFIG','canny_1'))
        self.canny2_slider.setValue(config.getint('FILTER_CONFIG','canny_2'))
        self.spinboxupdate()

        # Refresh when Changed
        self.reset_bt.clicked.connect(self.reset)
        self.close_bt.clicked.connect(self.close_widget)
        self.minhue_slider.valueChanged.connect(self.spinboxupdate)
        self.minsat_slider.valueChanged.connect(self.spinboxupdate)
        self.minval_slider.valueChanged.connect(self.spinboxupdate)
        self.maxhue_slider.valueChanged.connect(self.spinboxupdate)
        self.maxsat_slider.valueChanged.connect(self.spinboxupdate)
        self.maxval_slider.valueChanged.connect(self.spinboxupdate)
        self.sataddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.valaddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.kernelsize_slider.valueChanged.connect(self.spinboxupdate)
        self.erodelter_slider.valueChanged.connect(self.spinboxupdate)
        self.dilatelter_slider.valueChanged.connect(self.spinboxupdate)
        self.canny1_slider.valueChanged.connect(self.spinboxupdate)
        self.canny2_slider.valueChanged.connect(self.spinboxupdate)

        self.minhue_spinbox.valueChanged.connect(self.sliderupdate)
        self.minsat_spinbox.valueChanged.connect(self.sliderupdate)
        self.minval_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxhue_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxsat_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxval_spinbox.valueChanged.connect(self.sliderupdate)
        self.sataddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.valaddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.kernelsize_spinbox.valueChanged.connect(self.sliderupdate)
        self.erodelter_spinbox.valueChanged.connect(self.sliderupdate)
        self.dilatelter_spinbox.valueChanged.connect(self.sliderupdate)
        self.canny1_spinbox.valueChanged.connect(self.sliderupdate)
        self.canny2_spinbox.valueChanged.connect(self.spinboxupdate)

    def sliderupdate(self):
        self.minhue_slider.setValue(self.minhue_spinbox.value())
        self.minsat_slider.setValue(self.minsat_spinbox.value())
        self.minval_slider.setValue(self.minval_spinbox.value())
        self.maxhue_slider.setValue(self.maxhue_spinbox.value())
        self.maxsat_slider.setValue(self.maxsat_spinbox.value())
        self.maxval_slider.setValue(self.maxval_spinbox.value())
        self.sataddsub_slider.setValue(self.sataddsub_spinbox.value())
        self.valaddsub_slider.setValue(self.valaddsub_spinbox.value())
        self.kernelsize_slider.setValue(self.kernelsize_spinbox.value())
        self.erodelter_slider.setValue(self.erodelter_spinbox.value())
        self.dilatelter_slider.setValue(self.dilatelter_spinbox.value())
        self.canny1_slider.setValue(self.canny1_spinbox.value())
        self.canny2_slider.setValue(self.canny2_spinbox.value())
        self.updateconfigfiltervalues()

    def spinboxupdate(self):
        self.minhue_spinbox.setValue(self.minhue_slider.value())
        self.minsat_spinbox.setValue(self.minsat_slider.value())
        self.minval_spinbox.setValue(self.minval_slider.value())
        self.maxhue_spinbox.setValue(self.maxhue_slider.value())
        self.maxsat_spinbox.setValue(self.maxsat_slider.value())
        self.maxval_spinbox.setValue(self.maxval_slider.value())
        self.sataddsub_spinbox.setValue(self.sataddsub_slider.value())
        self.valaddsub_spinbox.setValue(self.valaddsub_slider.value())
        self.kernelsize_spinbox.setValue(self.kernelsize_slider.value())
        self.erodelter_spinbox.setValue(self.erodelter_slider.value())
        self.dilatelter_spinbox.setValue(self.dilatelter_slider.value())
        self.canny1_spinbox.setValue(self.canny1_slider.value())
        self.canny2_spinbox.setValue(self.canny2_slider.value())
        self.updateconfigfiltervalues()

    def updateconfigfiltervalues(self):
        config.set('FILTER_CONFIG', 'min_hue', str(self.minhue_slider.value()))
        config.set('FILTER_CONFIG', 'max_hue', str(self.maxhue_slider.value()))
        config.set('FILTER_CONFIG', 'min_saturation', str(self.minsat_slider.value()))
        config.set('FILTER_CONFIG', 'max_saturation', str(self.maxsat_slider.value()))
        config.set('FILTER_CONFIG', 'min_value', str(self.minval_slider.value()))
        config.set('FILTER_CONFIG', 'max_saturation', str(self.maxval_slider.value()))
        config.set('FILTER_CONFIG', 'saturation_multiplier', str(self.sataddsub_slider.value()))
        config.set('FILTER_CONFIG', 'value_multiplier', str(self.valaddsub_slider.value()))
        config.set('FILTER_CONFIG', 'kernelsize', str(self.kernelsize_slider.value()))
        config.set('FILTER_CONFIG', 'erode', str(self.erodelter_slider.value()))
        config.set('FILTER_CONFIG', 'dilate', str(self.dilatelter_slider.value()))
        config.set('FILTER_CONFIG', 'canny_1', str(self.canny1_slider.value()))
        config.set('FILTER_CONFIG', 'canny_2', str(self.canny2_slider.value()))

         # Save the changes
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    # returns an HSV filter object based on the control GUI values and Canny edge filter object based on the control GUI values
    def getfiltervalues(self):
        
        filter.minhue = self.minhue_slider.value()
        filter.minsat = self.minsat_slider.value()
        filter.minval = self.minval_slider.value()
        filter.maxhue = self.maxhue_slider.value()
        filter.maxsat = self.maxsat_slider.value()
        filter.maxval = self.maxval_slider.value()
        filter.sat_addsub = self.sataddsub_slider.value()
        filter.val_addsub = self.valaddsub_slider.value()
        filter.kernelsize = self.kernelsize_slider.value()
        filter.erode = self.erodelter_slider.value()
        filter.dilate = self.dilatelter_slider.value()
        filter.canny1 = self.canny1_slider.value()
        filter.canny2 = self.canny2_slider.value()

        return filter
    
    def reset(self):
        self.minhue_slider.setValue(0)
        self.minhue_slider.setValue(179)
        self.minsat_slider.setValue(0)
        self.maxsat_slider.setValue(255)
        self.minval_slider.setValue(0)
        self.maxval_slider.setValue(255)
        self.sataddsub_slider.setValue(0)
        self.valaddsub_slider.setValue(0)
        self.kernelsize_slider.setValue(1)
        self.erodelter_slider.setValue(1)
        self.dilatelter_slider.setValue(1)
        self.canny1_slider.setValue(0)
        self.canny2_slider.setValue(0)
        self.spinboxupdate()
    
    def close_widget(self):
        self.close()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informações")
        self.setMinimumWidth(300)  # Adjust the width as needed

        # Create a label for the image
        image_label = QLabel()
        pixmap = QPixmap("ui/icons/apple.png")  # Replace with the path to your image

        # Resize the image
        #new_width = 200  # Adjust the width as needed
        #new_height = 150  # Adjust the height as needed
        #pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)

        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a paragraph to explain the keys
        keys_paragraph = QLabel(
            "Key Shortcuts:\n\n"
            "Iniciar/Parar - Ctrl+I ou Ctrl+P\n"
            "Abrir/Carregar - Ctrl+O ou Ctrl+A\n"
            "Guardar - Ctrl+S ou Ctrl+G\n"
            "Vista Pequena - Ctrl+Left\n"
            "Vista Grande - Ctrl+Right\n"
            "Ver Logs - Ctrl+L\n"
            "Exportar Logs - Ctrl+Shift+L"
        )

        # Add the copyright text
        copyright_text = QLabel("Copyright © JBC 2023")
        copyright_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(keys_paragraph)
        layout.addWidget(copyright_text)

        # Add the "OK" button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)


 # Save the changes
with open('config.ini', 'w') as config_file:
    config.write(config_file)

# ========== CONSTRUCTOR ==========   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    cfwidget = ColorFilters()
    my_app.show()
    sys.exit(app.exec())
# ============= \\-// =============