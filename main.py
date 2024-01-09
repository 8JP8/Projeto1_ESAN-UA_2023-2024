from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QDialog, QWidget, QTabWidget,  QVBoxLayout, QGraphicsDropShadowEffect, QSizePolicy, QLCDNumber
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, Qt, QPropertyAnimation, QSize, QTimer, QThread, QMetaObject, Q_ARG
from PyQt6.QtGui import QImage, QPixmap, QIcon, QCloseEvent, QAction, QKeySequence, QShortcut, QPalette, QColor, QMovie, QGuiApplication
import numpy as np
import threading
import subprocess
import datetime
import time
import os
import sys
import cv2
import configparser
import tempfile

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read('config.ini')  # Replace 'config.ini' with the path to your configuration file

#Global Variables
calib_camera_enabled = False
loadingcompleted = False
log_file_content = None
global USE_TWO_CAMERAS

# CONFIG GLOBAL VARIABLES
USE_TWO_CAMERAS = config.getboolean('CAMERA_CONFIG', 'USE_TWO_CAMERAS')
CAMERA_INDEX_LEFT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_LEFT')    # Camera index for the left camera (if using two cameras)
CAMERA_INDEX_RIGHT = config.getint('CAMERA_CONFIG', 'CAMERA_INDEX_RIGHT')
DETECTIONMODE = config.getint('DETECTION_CONFIG', 'DETECTIONMODE_VALUE')
MICROCONTROLLER_PORT = config.get("IO_CONFIG", "microcontroller_port")

def imports():
    # ============ IMPORTS ============
    loading_splash.loading_label.setText("A Carregar: Modelos")
    global FrameProcessor, AppleIndexation, LOG_FILE_PATH  # Make these variables global
    import modules.FrameProcessor as FrameProcessor
    from modules.code_v1 import LOG_FILE_PATH
    import modules.AppleIndexation as AppleIndexation
    loading_splash.loading_label.setText("A Carregar: UI")
    # ============= \\-// =============

class MyApp(QMainWindow):                     # GUI CLASS
    def __init__(self):                       # CONSTRUCTOR
        super (MyApp, self).__init__()
        loadUi('ui/app.ui', self)
        self.icon = QIcon('ui/icons/apple.ico')
        app.setWindowIcon(self.icon)
        self.configpath = 'config.ini'

        # ============ INICIALIZAÇÃO COM OS VALORES DA CONFIG ============
        self.mode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'mode_value'))
        self.detectionmode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'detectionmode_value'))
        self.categorizationmode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'categorizationmode_value'))
        self.cam2_RADIOBT.setChecked(config.getboolean('CAMERA_CONFIG', 'use_two_cameras'))
        if DETECTIONMODE in [-1, 0, 1]:
            self.threshold1_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threshold1_value'))
            self.threshold2_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threshold2_value'))
        elif DETECTIONMODE == 2:
            self.threshold1_SLIDER.setValue(config.getint('CUSTOM_DETECTION_CONFIG', 'threshold1_value'))
            self.threshold2_SLIDER.setValue(config.getint('CUSTOM_DETECTION_CONFIG', 'threshold2_value'))
        # ============================= \\-// ============================

        # ============ BINDS ============
        self.upload_BT.clicked.connect(self.load_file)
        self.start_BT.setShortcut(QKeySequence.fromString("I"))
        self.start_BT.clicked.connect(self.start_cameracapture)
        self.upload_BT.setShortcut(QKeySequence.fromString("A"))
        self.reset_BT.setShortcut(QKeySequence.fromString("Ctrl+R"))
        self.reset_BT.clicked.connect(self.resetapplecount)
        self.nextframe_BT.clicked.connect(self.nextframe)
        self.colorfilters_BT.clicked.connect(self.colorfilters_open)
        self.colorfilters_BT.setShortcut(QKeySequence.fromString("F"))
        self.actionOpen_Upload.setShortcuts([QKeySequence.fromString("Ctrl+O"), QKeySequence.fromString("Ctrl+A")])
        self.actionOpen_Upload.triggered.connect(self.load_file)
        self.actionSave_Output_File.triggered.connect(self.save_file)
        self.actionSave_Output_File.setShortcuts([QKeySequence.fromString("Ctrl+S"), QKeySequence.fromString("Ctrl+G")])
        self.actionSave_Frame.triggered.connect(self.save_frame)
        self.actionSave_Frame.setShortcut("Ctrl+F")
        self.action_small_view.triggered.connect(self.small_vw)
        self.action_big_view.triggered.connect(self.big_vw)
        self.action_operatorview.triggered.connect(self.operator_vw)
        self.action_small_view.setShortcut("Ctrl+Left")
        self.action_big_view.setShortcut("Ctrl+Right")
        self.action_operatorview.setShortcuts([QKeySequence.fromString("Ctrl+End"), QKeySequence.fromString("Ctrl+1")])
        self.action_calibratecamera.triggered.connect(self.calibratecamera)
        self.action_calibratecamera.setShortcut("Ctrl+Shift+C")
        self.action_restartprogram.triggered.connect(self.restartprogram)
        self.action_restartprogram.setShortcut("Ctrl+Shift+R")
        #self.menuLogs.aboutToShow.connect(self.logs_open)
        #self.shortcut = QShortcut(QKeySequence('Ctrl+L'), self)
        #self.shortcut.activated.connect(self.logs_open) 
        self.action_settings_open.triggered.connect(self.settings_open)
        self.action_settings_open.setShortcut("Ctrl+D")
        self.action_logs_open.triggered.connect(self.logs_open)
        self.action_logs_export.triggered.connect(self.logs_save)
        self.action_logs_open.setShortcut("Ctrl+L")
        self.action_logs_export.setShortcut("Ctrl+Shift+L")
        self.menuInfo.aboutToShow.connect(self.info_open)
        self.threshold1_SLIDER.valueChanged.connect(self.update_config)
        self.threshold2_SLIDER.valueChanged.connect(self.update_config)
        self.mode_COMBOBOX.currentIndexChanged.connect(self.update_config)
        self.detectionmode_COMBOBOX.currentIndexChanged.connect(self.detectionmode_changed)
        self.categorizationmode_COMBOBOX.currentIndexChanged.connect(self.update_config)
        self.cam1_RADIOBT.toggled.connect(self.update_config)
        self.cam2_RADIOBT.toggled.connect(self.update_config)
        # Create shortcuts to move up and down in the tabs
        shortcut_up = QKeySequence.fromString("Ctrl+Up")
        shortcut_down = QKeySequence.fromString("Ctrl+Down")
        # Connect the shortcuts to custom slot functions
        self.createShortcut(shortcut_up, self.moveTabUp)
        self.createShortcut(shortcut_down, self.moveTabDown)
        # Other Things
        self.AverageDiameter_TextEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.FalsePositives_TextEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # ============ \\-// ============
        self.videoplaying = False
        self.camopen = False
        self.thread_stop_flag = False
        self.stop_recording_tag = False
        self.filename = str()
        self.showframescontinuously = True
        global currentimageframe
        global currentimageframe2
        global videoplaying
        currentimageframe = None
        currentimageframe2 = None
        self.video_writer = None
        self.video_writer2 = None
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
            self.show_warning("Está a ser processado vídeo: Carregue PARAR (P) ou feche a App.")
        else:
            self.filename = QFileDialog.getOpenFileName(
                filter = "Ficheiros Suportados (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.pbm *.pgm *.ppm *.xbm *.xpm *.sr *.webp *.avi *.mov *.mp4 *.mkv *.wmv *.flv *.3gp *.asf *.mpg *.rm);;Ficheiros de Imagem (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.pbm *.pgm *.ppm *.xbm *.xpm *.sr *.webp);;Ficheiros de Vídeo (*.avi *.mov *.mp4 *.mkv *.wmv *.flv *.3gp *.asf *.mpg *.rm);;Todos os Ficheiros (*)")[0]
            if len(self.filename)!=0:
                self.image = cv2.imread(self.filename)
                if self.image is not None:
                    self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
                    image = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2RGB)
                    self.set_image(image)
                    self.current_type = "image"
                else:
                    print("Processamento de Frames Iniciado")
                    self.nextframe_BT.setShortcut(QKeySequence.fromString("N"))
                    threading.Thread(target=self.video_processing_thread, args=(self.filename,)).start()
    
    def set_image(self, image): #FUNCTION TO PUT THE INPUT IMAGE IN THE FRAME
            if len(self.filename)!=0:
                with open(LOG_FILE_PATH, 'a') as log:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log.write(f"{timestamp} - Processamento de imagem iniciado\n")
                # ============= OLD RESIZE CODE TO FIT THE IMAGE ============ →→→→→→→→→→→→  frame = imutils.resize(image, width=self.inputframe_1.width, height=self.inputframe_1.height)
                self.progressBar.setValue(100) #RESET PROGRESSBAR
                #Preview the input filters
                image = FrameProcessor.ApplyInputFilters(image, customdetectionfilter)
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
                if self.detectionmode_COMBOBOX.currentIndex() in [-1, 0, 1, 2]:
                    processedimage = FrameProcessor.ImageProcessor(self.filename, image, self.detectionmode_COMBOBOX.currentIndex(), self.categorizationmode_COMBOBOX.currentIndex(), self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value(), filter, customdetectionfilter)
                    if not processedimage[0]:
                        self.show_warning(processedimage[1])
                    else:
                        # get current frame and save it as a variable
                        imagewithfilters = FrameProcessor.ApplyFilters(processedimage[1], filter)
                        self.currentframesaver(imagewithfilters)
                        # ===================== CENTER THE IMAGE =====================
                        framepi = cv2.resize(imagewithfilters, (framei.shape[1], framei.shape[0]))
                        framep2i = cv2.resize(imagewithfilters, (frame2i.shape[1], frame2i.shape[0]))
                        emptyframepi = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                        emptyframepi[y_offseti:y_offseti+framei.shape[0], x_offseti:x_offseti+framei.shape[1]] = framepi                      # Paste the resized image onto the empty frame
                        emptyframep2i = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                        emptyframep2i[y_offset2i:y_offset2i+frame2i.shape[0], x_offset2i:x_offset2i+frame2i.shape[1]] = framep2i                 # Paste the resized image onto the empty frame
                        # Paste the resized image onto the empty frame
                        # ======================== UPDATE THE GUI ========================
                        imagepi = QImage(emptyframepi, emptyframepi.shape[1],emptyframepi.shape[0], emptyframepi.strides[0],QImage.Format.Format_RGB888)
                        imagep2i = QImage(emptyframep2i, emptyframep2i.shape[1],emptyframep2i.shape[0], emptyframep2i.strides[0],QImage.Format.Format_RGB888)
                        self.outputframe_1.setPixmap(QPixmap.fromImage(imagepi))
                        self.outputframe_5.setPixmap(QPixmap.fromImage(imagepi))
                        self.outputframe_3.setPixmap(QPixmap.fromImage(imagep2i))
                        # ============================ \\--// ============================
                else:
                    imagewithfilters = FrameProcessor.ApplyFilters(image, filter)
                    self.currentframesaver(imagewithfilters)
                    framepf = cv2.resize(imagewithfilters, (framei.shape[1], framei.shape[0]))
                    framep2f = cv2.resize(imagewithfilters, (frame2i.shape[1], frame2i.shape[0]))
                    emptyframepf = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframepf[y_offseti:y_offseti+framei.shape[0], x_offseti:x_offseti+framei.shape[1]] = framepf                      # Paste the resized image onto the empty frame
                    emptyframep2f = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                    emptyframep2f[y_offset2i:y_offset2i+frame2i.shape[0], x_offset2i:x_offset2i+frame2i.shape[1]] = framep2f                # Paste the resized image onto the empty frame
                    # Paste the resized image onto the empty frame
                    # ======================== UPDATE THE GUI ========================
                    imagepf = QImage(emptyframepf, emptyframepf.shape[1],emptyframepf.shape[0], emptyframepf.strides[0],QImage.Format.Format_RGB888)
                    imagep2f = QImage(emptyframep2f, emptyframep2f.shape[1],emptyframep2f.shape[0], emptyframep2f.strides[0],QImage.Format.Format_RGB888)
                    self.outputframe_1.setPixmap(QPixmap.fromImage(imagepf))
                    self.outputframe_5.setPixmap(QPixmap.fromImage(imagepf))
                    self.outputframe_3.setPixmap(QPixmap.fromImage(imagep2f))

        

    # ======= START AND CLOSE FUNCTIONS =======  
    def restartprogram(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    def calibratecamera(self):
        global calib_camera_enabled
        if not self.camopen:
            self.show_warning('Inicie a captura da câmara para calibrar.')
        else:
            if calib_camera_enabled:
                FrameProcessor.calibratecamerabool(False)
                calib_camera_enabled = False
                self.action_calibratecamera.setText('Calibrar Câmara (Ctrl+Shift+C)')
            else:
                FrameProcessor.calibratecamerabool(True)
                calib_camera_enabled = True
                self.action_calibratecamera.setText('Parar Calibração (Ctrl+Shift+C)')
    def closeEvent(self, event: QCloseEvent):
        self.thread_stop_flag = True
        self.stop_recording_tag = True
        self.colorfilters = ColorFilters()
        self.colorfilters.close() #close filters widget when mainwindow closes
        self.inputfilters = InputFilters()
        self.inputfilters.close() #close filters widget when mainwindow closes
    def video_processing_thread(self, filename):
        self.set_video(filename)
    def cameracapture_to_gui_thread(self):
        self.cameracapture_to_gui()
    def recording_thread(self):
        self.frame_record()
    # ========================== \\--// ==========================
     
    def set_video(self, video):
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            self.show_warning("Falha ao abrir o ficheiro de vídeo.")
        else:
            self.start_stop_recording("stop")
            self.start_stop_recording("start")
            self.modify_startbutton("parar")
            # Getting video informations for progressbar
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Create a VideoCapture object
            with open(LOG_FILE_PATH, 'a') as log:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{timestamp} - Processamento de vídeo iniciado\n")
            while not self.thread_stop_flag:
                ret, frame = cap.read()
                if not ret:
                    break  # Break the loop at the end of the video
                self.videoplaying = True #bool to stop uploads while playing
                global videoplaying
                videoplaying = self.videoplaying
                # Getting video informations for progressbar
                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                progress = (current_frame / self.total_frames) * 100
                self.progressBar.setValue(int(progress))
                #Preview the input filters
                frame = FrameProcessor.ApplyInputFilters(frame, customdetectionfilter)
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
                
                if self.detectionmode_COMBOBOX.currentIndex() in [-1, 0, 1, 2]:
                    #frame processing
                    processor_result = FrameProcessor.VideoProcessor(video, processoriginalquality, self.detectionmode_COMBOBOX.currentIndex(), self.categorizationmode_COMBOBOX.currentIndex(), self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value(), filter, customdetectionfilter)
                    if not processor_result[0]:
                        self.show_warning(processor_result[1])
                    else:
                        # Ensure that processedvideoframe has the same dimensions as the target area
                        imagewithfilters = FrameProcessor.ApplyFilters(processor_result[1], filter)
                        processedvideoframe = cv2.resize(imagewithfilters, (frame.shape[1], frame.shape[0]))
                        processedvideoframe2 = cv2.resize(imagewithfilters, (frame2.shape[1], frame2.shape[0]))
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
                        if self.showframescontinuously or self.nextframebool:
                            self.outputframe_1.setPixmap(QPixmap.fromImage(videoframep))
                            self.outputframe_5.setPixmap(QPixmap.fromImage(videoframep))
                            self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep2))
                            self.currentframesaver(processor_result[1]) #Save latest frame in a variable
                            self.nextframebool = False
                else:
                    # Update the GUI
                    imagewithfilters = FrameProcessor.ApplyFilters(processoriginalquality, filter)
                    framepf = cv2.resize(imagewithfilters, (frame.shape[1], frame.shape[0]))
                    framep2f = cv2.resize(imagewithfilters, (frame2.shape[1], frame2.shape[0]))
                    emptyframepf = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframepf[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = framepf                      # Paste the resized image onto the empty frame
                    emptyframep2f = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                    emptyframep2f[y_offset2:y_offset2+frame2.shape[0], x_offset2:x_offset2+frame2.shape[1]] = framep2f                # Paste the resized image onto the empty frame
                    # Paste the resized image onto the empty frame
                    # ======================== UPDATE THE GUI ========================
                    imagepf = QImage(emptyframepf, emptyframepf.shape[1],emptyframepf.shape[0], emptyframepf.strides[0],QImage.Format.Format_RGB888)
                    imagep2f = QImage(emptyframep2f, emptyframep2f.shape[1],emptyframep2f.shape[0], emptyframep2f.strides[0],QImage.Format.Format_RGB888)
                    if self.showframescontinuously or self.nextframebool:
                        self.outputframe_1.setPixmap(QPixmap.fromImage(imagepf))
                        self.outputframe_5.setPixmap(QPixmap.fromImage(imagepf))
                        self.outputframe_3.setPixmap(QPixmap.fromImage(imagep2f))
                        self.currentframesaver(imagewithfilters) #Save latest frame in a variable
                        self.nextframebool = False


            self.modify_startbutton("iniciar")
            self.videoplaying = False
            self.thread_stop_flag = False
            self.start_stop_recording("stop")

    def update_operatordisplay(self):
        slot_count, apples = AppleIndexation.get_apple_data()

        # Display apple count in QLCDNumber
        self.Slot_LCD.display(slot_count)

        # Parse apple list and count by types
        big_apple_count = small_apple_count = bad_apple_count = false_positives = diameter_sum = 0
        last_slot = -1
        for slot_count, apple_type, diameter in apples:
            if slot_count != last_slot:
                if apple_type == "Grande":
                    big_apple_count += 1
                    diameter_sum += diameter
                elif apple_type == "Pequena":
                    small_apple_count += 1
                    diameter_sum += diameter
                elif apple_type == "Defeituosa":
                    bad_apple_count += 1
                    diameter_sum += diameter
                slot_count += 1
            else:
                #keep only one detection per slot
                false_positives += 1 #add the false positive

        # Update QLCDNumber with counts
        self.BigApples_LCD.display(big_apple_count)
        self.SmallApples_LCD.display(small_apple_count)
        self.BadApples_LCD.display(bad_apple_count)
        total_apple_count = big_apple_count + small_apple_count + bad_apple_count
        self.DetectedApples_LCD.display(big_apple_count+small_apple_count+bad_apple_count)
        WorkerThread.set_initial_values(self, false_positives, diameter_sum / total_apple_count if total_apple_count != 0 else 0.0)  

    def start_operator_ui_thread(self):
        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.update_operator_ui)
        self.worker_thread.start()

    def update_operator_ui(self, false_positives, average_diameter):
        self.FalsePositives_TextEdit.setHtml(f"<div align='center'>{false_positives}</div>")
        self.AverageDiameter_TextEdit.setHtml(f"<div align='center'>{average_diameter}</div>")

        #print("updated")
        #Updates with LogFile
        try:
            with open(LOG_FILE_PATH, 'r') as file:
                content = file.read()
                if content != log_file_content:
                    self.Log_textBrowser.setPlainText(str(content))
        except Exception as e:
            self.Log_textBrowser.setPlainText(f"Erro de Leitura do Ficheiro de Log: {str(e)}") 
            print(f"Erro de Leitura do Ficheiro de Log: {str(e)}") 

    def start_cameracapture(self):
        self.start_operator_ui_thread()
        import modules.LEDControl as LEDControl
            
        self.nextframe_BT.setText("CONGELAR (C)")
        self.nextframe_BT.setShortcut("C")
        if self.videoplaying and self.showframescontinuously:
            self.thread_stop_flag = True #STOP VIDEO PLAYBACK / CAMERA PLAYBACK
            if  self.camopen:
                self.camopen = False
            self.modify_startbutton("iniciar")
            self.start_stop_recording("stop")
            #LED Control
            defaultbrightness = config.getint("IO_CONFIG", "light_default_intensity")
            if config.getboolean("IO_CONFIG", "use_lights"):
                try:
                    LEDControl.control_led_strip(MICROCONTROLLER_PORT, 0, 0, 0)
                except:
                    self.show_error(f"Erro: Foi atingido o tempo limite de resposta do Microcontrolador\nVerifique se está conectado e o endereço da porta é o {MICROCONTROLLER_PORT}.")

        else:
            #LED Control
            defaultbrightness = config.getint("IO_CONFIG", "light_default_intensity")
            if config.getboolean("IO_CONFIG", "use_lights"):
                try:
                    LEDControl.control_led_strip(MICROCONTROLLER_PORT, defaultbrightness, defaultbrightness, defaultbrightness)
                except:
                    self.show_error(f"Erro: Foi atingido o tempo limite de resposta do Microcontrolador\nVerifique se está conectado e o endereço da porta é o {MICROCONTROLLER_PORT}.")
            if not self.showframescontinuously:
                self.showframescontinuously = True
                self.start_BT.setText("PARAR (P)")
                self.start_BT.setShortcut("P")
            else:
                self.progressBar.setValue(100) #RESET PROGRESSBAR
                #Camera Test
                # Try to access the default camera (usually the built-in webcam)
                if USE_TWO_CAMERAS:
                    self.cap_left = cv2.VideoCapture(CAMERA_INDEX_LEFT)
                    self.cap_right = cv2.VideoCapture(CAMERA_INDEX_RIGHT)
                    # Check if the camera was opened successfully
                    if self.cap_left.isOpened() and self.cap_right.isOpened():
                        self.camopen = True
                else:
                    self.camera = cv2.VideoCapture(0)  # 0 represents the default camera
                    # Check if the camera was opened successfully
                    if self.camera.isOpened():
                        self.camopen = True
                if self.camopen:
                    self.modify_startbutton("parar")
                    print("Processamento de Frames Iniciado")
                    threading.Thread(target=self.cameracapture_to_gui_thread).start() #Updates the gui with camera feed


    def cameracapture_to_gui(self):
        # Create a VideoCapture object
        self.start_stop_recording("start")
        with open(LOG_FILE_PATH, 'a') as log:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"{timestamp} - Processamento de câmara iniciado\n")
        while not self.thread_stop_flag:
            if USE_TWO_CAMERAS:
                try:
                    self.camera = self.cap_left
                    ret_left, frame_left = self.cap_left.read()
                    ret_right, frame_right = self.cap_right.read()
                except:
                    self.show_error("Erro: Câmara não disponível.")
                #Preview the input filters
                frame_left = FrameProcessor.ApplyInputFilters(frame_left, customdetectionfilter)
                frame_right = FrameProcessor.ApplyInputFilters(frame_right, customdetectionfilter)
                # Calculate the scale and apply resizing
                self.hsv_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2HSV)
                frame = frame_left = cv2.cvtColor(self.hsv_left, cv2.COLOR_HSV2RGB)
                self.hsv_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2HSV)
                frame_right = cv2.cvtColor(self.hsv_right, cv2.COLOR_HSV2RGB)
                if not ret_left or not ret_right:
                    break
            else:
                try:
                    ret, frame = self.camera.read()
                except:
                    self.show_warning("Erro: Câmara não disponível.")
                #Preview the input filters
                frame = FrameProcessor.ApplyInputFilters(frame, customdetectionfilter)
                # Calculate the scale and apply resizing
                self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                frame = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2RGB)
                if not ret:
                    break
            self.videoplaying = True #bool to stop uploads while playing
            #############################################################
            width_scale = int(self.inputframe_1.width()) / frame.shape[1]
            height_scale = int(self.inputframe_1.height()) / frame.shape[0]
            scale = min(width_scale, height_scale)
            frameoriginal = frame                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            frame = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale))) #small
            #Calculate the scale and apply resizing 2
            width_scale2 = int(self.inputframe_3.width()) / frameoriginal.shape[1]
            height_scale2 = int(self.inputframe_3.height()) / frameoriginal.shape[0]
            scale2 = min(width_scale2, height_scale2)
            frame2 = cv2.resize(frameoriginal, (int(frameoriginal.shape[1] * scale2), int(frameoriginal.shape[0] * scale2))) #big
            # Center the image
            emptyframe = np.full((self.inputframe_1.height(), self.inputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
            x_offset = (self.inputframe_1.width() - frame.shape[1]) // 2
            y_offset = (self.inputframe_1.height() - frame.shape[0]) // 2
            # Center the image 2
            emptyframe2 = np.full((self.inputframe_3.height(), self.inputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
            x_offset2 = (self.inputframe_3.width() - frame2.shape[1]) // 2
            y_offset2 = (self.inputframe_3.height() - frame2.shape[0]) // 2
            if USE_TWO_CAMERAS:
                if self.detectionmode_COMBOBOX.currentIndex() in [-1, 0, 1, 2]:
                    # Resizing for inputframe2 and inputframe4
                    frameoriginal2 = frame_right
                    frame3 = cv2.resize(frameoriginal2, (int(frameoriginal2.shape[1] * scale), int(frameoriginal2.shape[0] * scale))) #small2
                    frame4 = cv2.resize(frameoriginal2, (int(frameoriginal2.shape[1] * scale2), int(frameoriginal2.shape[0] * scale2))) #big2
                    # Paste Frames in EmptyFrames
                    emptyframe3 = np.full((self.inputframe_2.height(), self.inputframe_2.width(), 3), (255, 255, 255), dtype=np.uint8)
                    emptyframe4 = np.full((self.inputframe_4.height(), self.inputframe_4.width(), 3), (255, 255, 255), dtype=np.uint8)
                    emptyframe[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame #small
                    emptyframe2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = frame2 #big
                    emptyframe3[y_offset:y_offset + frame3.shape[0], x_offset:x_offset + frame3.shape[1]] = frame3 #small2
                    emptyframe4[y_offset2:y_offset2 + frame4.shape[0], x_offset2:x_offset2 + frame4.shape[1]] = frame4 #big2
                    # Convert image format
                    image = QImage(emptyframe, emptyframe.shape[1], emptyframe.shape[0], emptyframe.strides[0], QImage.Format.Format_RGB888)
                    image2 = QImage(emptyframe2, emptyframe2.shape[1], emptyframe2.shape[0], emptyframe2.strides[0], QImage.Format.Format_RGB888)
                    image3 = QImage(emptyframe3, emptyframe3.shape[1], emptyframe3.shape[0], emptyframe3.strides[0], QImage.Format.Format_RGB888)
                    image4 = QImage(emptyframe4, emptyframe4.shape[1], emptyframe4.shape[0], emptyframe4.strides[0], QImage.Format.Format_RGB888)
                    # Update the GUI
                    self.inputframe_1.setPixmap(QPixmap.fromImage(image))
                    self.inputframe_2.setPixmap(QPixmap.fromImage(image3))
                    self.inputframe_3.setPixmap(QPixmap.fromImage(image2))
                    self.inputframe_4.setPixmap(QPixmap.fromImage(image4))
                    # Frame processing
                    processor_result = FrameProcessor.CameraProcessor(frameoriginal, self.detectionmode_COMBOBOX.currentIndex(), self.categorizationmode_COMBOBOX.currentIndex(), self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value(), filter, customdetectionfilter)
                    processor_result2 = FrameProcessor.CameraProcessor(frameoriginal2, self.detectionmode_COMBOBOX.currentIndex(), self.categorizationmode_COMBOBOX.currentIndex(), self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value(), filter, customdetectionfilter)
                    if not processor_result[0] or not processor_result2[0]:
                        self.show_warning(processor_result[1])
                    else:
                        imagewithfilters = FrameProcessor.ApplyFilters(processor_result[1], filter)
                        imagewithfilters2 = FrameProcessor.ApplyFilters(processor_result2[1], filter)
                        # Ensure that processedvideoframe has the same dimensions as the target area
                        processedvideoframe = cv2.resize(imagewithfilters, (frame.shape[1], frame.shape[0]))
                        processedvideoframe2 = cv2.resize(imagewithfilters2, (frame.shape[1], frame.shape[0]))
                        processedvideoframe3 = cv2.resize(imagewithfilters, (frame2.shape[1], frame2.shape[0]))
                        processedvideoframe4 = cv2.resize(imagewithfilters2, (frame2.shape[1], frame2.shape[0]))
                        # Create an empty frame with the target dimensions
                        emptyframep = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
                        emptyframep2 = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8)
                        emptyframep3 = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
                        emptyframep4 = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)
                        # Paste the resized frame onto the target area in emptyframep
                        emptyframep[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = processedvideoframe
                        emptyframep2[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = processedvideoframe2
                        emptyframep3[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = processedvideoframe3
                        emptyframep4[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = processedvideoframe4
                        # Convert image format
                        videoframep = QImage(emptyframep, emptyframep.shape[1], emptyframep.shape[0], emptyframep.strides[0], QImage.Format.Format_RGB888)
                        videoframep2 = QImage(emptyframep2, emptyframep2.shape[1], emptyframep2.shape[0], emptyframep2.strides[0], QImage.Format.Format_RGB888)
                        videoframep3 = QImage(emptyframep3, emptyframep3.shape[1], emptyframep3.shape[0], emptyframep3.strides[0], QImage.Format.Format_RGB888)
                        videoframep4 = QImage(emptyframep4, emptyframep4.shape[1], emptyframep4.shape[0], emptyframep4.strides[0], QImage.Format.Format_RGB888)
                        # Update the GUI
                        if self.showframescontinuously or self.nextframebool:
                            self.outputframe_1.setPixmap(QPixmap.fromImage(videoframep))
                            self.outputframe_5.setPixmap(QPixmap.fromImage(videoframep))
                            self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep3))
                            self.outputframe_2.setPixmap(QPixmap.fromImage(videoframep2))
                            self.outputframe_6.setPixmap(QPixmap.fromImage(videoframep2))
                            self.outputframe_4.setPixmap(QPixmap.fromImage(videoframep4))
                            self.currentframesaver(processor_result[1])  #Save latest frame in a variable
                            self.currentframesaver2(processor_result2[1])  #Save latest frame in a variable
                            self.nextframebool = False                        
                else:
                    calibframereturn = FrameProcessor.cameracalibrationprocessor(frameoriginal)
                    if calibframereturn != None:
                        inputframe = calibframereturn[1]
                    else:
                        inputframe = frameoriginal
                    imagewithfilters = FrameProcessor.ApplyFilters(inputframe, filter)
                    imagewithfilters2 = FrameProcessor.ApplyFilters(frameoriginal2, filter)
                    framepf = cv2.resize(imagewithfilters, (frame.shape[1], frame.shape[0]))
                    framep2f = cv2.resize(imagewithfilters, (frame2.shape[1], frame2.shape[0]))
                    framep3f = cv2.resize(imagewithfilters2, (frame.shape[1], frame.shape[0]))
                    framep4f = cv2.resize(imagewithfilters2, (frame2.shape[1], frame2.shape[0]))
                    emptyframepf = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframepf[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = framepf                      # Paste the resized image onto the empty frame
                    emptyframep2f = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                    emptyframep2f[y_offset2:y_offset2+frame2.shape[0], x_offset2:x_offset2+frame2.shape[1]] = framep2f                # Paste the resized image onto the empty frame
                    emptyframep3f = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframep3f[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = framep3f                      # Paste the resized image onto the empty frame
                    emptyframep4f = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                    emptyframep4f[y_offset2:y_offset2+frame2.shape[0], x_offset2:x_offset2+frame2.shape[1]] = framep4f                # Paste the resized image onto the empty frame
                    # Paste the resized image onto the empty frame
                    # ======================== UPDATE THE GUI ========================
                    videoframepf = QImage(emptyframepf, emptyframepf.shape[1], emptyframepf.shape[0], emptyframepf.strides[0], QImage.Format.Format_RGB888)
                    videoframep2f = QImage(emptyframep2f, emptyframep2f.shape[1], emptyframep2f.shape[0], emptyframep2f.strides[0], QImage.Format.Format_RGB888)
                    videoframep3f = QImage(emptyframep3f, emptyframepf.shape[1], emptyframepf.shape[0], emptyframepf.strides[0], QImage.Format.Format_RGB888)
                    videoframep4f = QImage(emptyframep4f, emptyframep2f.shape[1], emptyframep2f.shape[0], emptyframep2f.strides[0], QImage.Format.Format_RGB888)
                    if self.showframescontinuously or self.nextframebool:
                        self.outputframe_1.setPixmap(QPixmap.fromImage(videoframepf))
                        self.outputframe_5.setPixmap(QPixmap.fromImage(videoframepf))
                        self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep3f))
                        self.outputframe_2.setPixmap(QPixmap.fromImage(videoframep2f))
                        self.outputframe_6.setPixmap(QPixmap.fromImage(videoframep2f))
                        self.outputframe_4.setPixmap(QPixmap.fromImage(videoframep4f))
                        self.currentframesaver(imagewithfilters)  #Save latest frame in a variable
                        self.currentframesaver(imagewithfilters2)  #Save latest frame in a variable
                        self.nextframebool = False
            else:
                emptyframe[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
                emptyframe2[y_offset2:y_offset2 + frame2.shape[0], x_offset2:x_offset2 + frame2.shape[1]] = frame2
                image = QImage(emptyframe, emptyframe.shape[1], emptyframe.shape[0], emptyframe.strides[0], QImage.Format.Format_RGB888)
                image2 = QImage(emptyframe2, emptyframe2.shape[1], emptyframe2.shape[0], emptyframe2.strides[0], QImage.Format.Format_RGB888)
                self.inputframe_1.setPixmap(QPixmap.fromImage(image))
                self.inputframe_3.setPixmap(QPixmap.fromImage(image2))
                
                if self.detectionmode_COMBOBOX.currentIndex() in [-1, 0, 1, 2]:
                    processor_result = FrameProcessor.CameraProcessor(frameoriginal, self.detectionmode_COMBOBOX.currentIndex(), self.categorizationmode_COMBOBOX.currentIndex(), self.threshold1_SLIDER.value(), self.threshold2_SLIDER.value(), filter, customdetectionfilter)
                    if not processor_result[0]:
                        self.show_warning(processor_result[1])
                    else:
                        imagewithfilters = FrameProcessor.ApplyFilters(processor_result[1], filter)
                        # Ensure that processedvideoframe has the same dimensions as the target area
                        processedvideoframe = cv2.resize(imagewithfilters, (frame.shape[1], frame.shape[0]))
                        processedvideoframe2 = cv2.resize(imagewithfilters, (frame2.shape[1], frame2.shape[0]))
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
                        if self.showframescontinuously or self.nextframebool:
                            self.outputframe_1.setPixmap(QPixmap.fromImage(videoframep))
                            self.outputframe_5.setPixmap(QPixmap.fromImage(videoframep))
                            self.outputframe_3.setPixmap(QPixmap.fromImage(videoframep2))
                            self.currentframesaver(processor_result[1])  #Save latest frame in a variable
                            self.nextframebool = False
                else:
                    calibframereturn = FrameProcessor.cameracalibrationprocessor(frameoriginal)
                    if calibframereturn != None:
                        inputframe = calibframereturn[1]
                    else:
                        inputframe = frameoriginal
                    # Update the GUI
                    imagewithfilters = FrameProcessor.ApplyFilters(inputframe, filter)
                    framepf = cv2.resize(imagewithfilters, (frame.shape[1], frame.shape[0]))
                    framep2f = cv2.resize(imagewithfilters, (frame2.shape[1], frame2.shape[0]))
                    emptyframepf = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframepf[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = framepf                      # Paste the resized image onto the empty frame
                    emptyframep2f = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8)  # Create an empty frame with the frame dimensions
                    emptyframep2f[y_offset2:y_offset2+frame2.shape[0], x_offset2:x_offset2+frame2.shape[1]] = framep2f                # Paste the resized image onto the empty frame
                    # Paste the resized image onto the empty frame
                    # ======================== UPDATE THE GUI ========================
                    imagepf = QImage(emptyframepf, emptyframepf.shape[1],emptyframepf.shape[0], emptyframepf.strides[0],QImage.Format.Format_RGB888)
                    imagep2f = QImage(emptyframep2f, emptyframep2f.shape[1],emptyframep2f.shape[0], emptyframep2f.strides[0],QImage.Format.Format_RGB888)
                    if self.showframescontinuously or self.nextframebool:
                        self.outputframe_1.setPixmap(QPixmap.fromImage(imagepf))
                        self.outputframe_5.setPixmap(QPixmap.fromImage(imagepf))
                        self.outputframe_3.setPixmap(QPixmap.fromImage(imagep2f))
                        self.currentframesaver(imagewithfilters)   #Save latest frame in a variable
                        self.nextframebool = False
            #Update OPERATOR UI
            self.update_operatordisplay()
        
        self.modify_startbutton("iniciar")
        self.videoplaying = False
        videoplaying = False
        self.thread_stop_flag = False
        # Release the camera when you're done
        if USE_TWO_CAMERAS:
            self.cap_left.release()
            self.cap_right.release()
        else:
            self.camera.release()
        self.start_stop_recording("stop")

    def currentframesaver(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.currentimageframe = pixmap
        global currentimageframe
        currentimageframe = pixmap
    def currentframesaver2(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.currentimageframe2 = pixmap
        global currentimageframe2
        currentimageframe2 = pixmap

    def small_vw(self):
        self.stackedWidget.setCurrentIndex(0)
        self.resize(771, 586)
    def big_vw(self):
        self.stackedWidget.setCurrentIndex(1)
        self.resize(771, 586)
    def operator_vw(self):
        self.stackedWidget.setCurrentIndex(2)
        self.resize(771, 586)

    def resetapplecount(self):
        AppleIndexation.reset_apple_list()
        

    def save_frame(self):
        if currentimageframe != None:
            # Get pixel data from the QPixmap
            savefile_dialog_path, _ = QFileDialog.getSaveFileName(self, "Guardar", "", "Ficheiros de Imagem (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.pbm *.pgm *.ppm *.xbm *.xpm *.sr *.webp);;All Files (*)")
            if savefile_dialog_path:
                pixmap = currentimageframe
                if not pixmap.isNull():
                    try:
                        pixmap.save(savefile_dialog_path)
                        self.show_info(f"Imagem Guardada: {savefile_dialog_path}")
                    except Exception as e:
                        self.show_error(f"Erro ao Guardar a Imagem: {str(e)}")
                else:
                    self.show_error(f"Erro: Não pode gravar uma imagem em branco.")
                if USE_TWO_CAMERAS:
                    savefile_dialog_path2, _ = QFileDialog.getSaveFileName(self, "Guardar 2º", "", "Ficheiros de Imagem (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.pbm *.pgm *.ppm *.xbm *.xpm *.sr *.webp);;All Files (*)")
                    if savefile_dialog_path2:
                        pixmap2 = currentimageframe2
                        if not pixmap2.isNull():
                            try:
                                pixmap2.save(savefile_dialog_path2)
                                self.show_info(f"Imagem 2 Guardada: {savefile_dialog_path2}")
                            except Exception as e:
                                self.show_error(f"Erro ao Guardar a 2ª Imagem: {str(e)}")
                        else:
                            self.show_error(f"Erro: Não pode gravar uma imagem em branco.")
        else:
            self.show_warning("Erro: Comece uma captura de câmara ou abra um ficheiro.")

    def save_file(self):
        if not self.videoplaying and not self.camopen:
            self.save_frame()
        else:
            self.save_video()

    def save_video(self):
        if self.video_writer is not None:
            self.video_writer.release()

        # Open a file dialog to choose save location and format
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Guardar Vídeo")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setNameFilter("Ficheiros de Vídeo (*.avi *.mp4 *.mkv *.mov);;Todos os Ficheiros (*)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted and self.video_writer != None:
            save_path = file_dialog.selectedFiles()[0]
            _, file_extension = os.path.splitext(save_path)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Default to AVI format

            if file_extension.lower() == '.mp4':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            elif file_extension.lower() == '.mkv':
                fourcc = cv2.VideoWriter_fourcc(*'X264')
            elif file_extension.lower() == '.mov':
                fourcc = cv2.VideoWriter_fourcc(*'X264')

            # Change the codec of the existing VideoWriter
            self.video_writer.set(cv2.CAP_PROP_FOURCC, fourcc)

            if os.path.exists(self.temp_filename):
                if os.path.exists(save_path):
                    os.remove(save_path)
                os.rename(self.temp_filename, save_path)
                self.show_info(f"Video Guardado: {save_path}")
            else:
                self.show_error(f"Erro de Gravação: Ficheiro Temporário '{self.temp_filename}' não encontrado.")
            if os.path.exists(self.temp_filename):
                os.remove(self.temp_filename)

        elif self.video_writer == None:
            self.show_warning("Erro: Comece uma captura de câmara ou abra um ficheiro.")

        if USE_TWO_CAMERAS:
            # Open a file dialog to choose save location and format
            file_dialog2 = QFileDialog(self)
            file_dialog2.setWindowTitle("Guardar Vídeo 2")
            file_dialog2.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            file_dialog2.setFileMode(QFileDialog.FileMode.AnyFile)
            file_dialog2.setNameFilter("Ficheiros de Vídeo (*.avi *.mp4 *.mkv *.mov);;Todos os Ficheiros (*)")

            if file_dialog2.exec() == QFileDialog.DialogCode.Accepted and self.video_writer2 != None:
                save_path2 = file_dialog2.selectedFiles()[0]
                _, file_extension = os.path.splitext(save_path2)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Default to AVI format

                if file_extension.lower() == '.mp4':
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                elif file_extension.lower() == '.mkv':
                    fourcc = cv2.VideoWriter_fourcc(*'X264')
                elif file_extension.lower() == '.mov':
                    fourcc = cv2.VideoWriter_fourcc(*'X264')

                # Change the codec of the existing VideoWriter
                self.video_writer2.set(cv2.CAP_PROP_FOURCC, fourcc)

                if os.path.exists(self.temp_filename2):
                    if os.path.exists(save_path2):
                        os.remove(save_path2)
                    os.rename(self.temp_filename2, save_path2)
                    self.show_info(f"Video Guardado: {save_path2}")
                else:
                    self.show_error(f"Erro de Gravação: Ficheiro Temporário '{self.temp_filename2}' não encontrado.")
                if os.path.exists(self.temp_filename2):
                    os.remove(self.temp_filename2)

            elif self.video_writer2 == None:
                self.show_warning("Erro: Comece uma captura de câmara ou abra um ficheiro.")

        self.start_stop_recording("reload")

    def frame_record(self):
        frame_interval = 1 / self.framerate  # Calculate the desired frame interval
        while not self.stop_recording_tag:
            start_time = time.time()

            if currentimageframe is not None:
                frame = currentimageframe.toImage().convertToFormat(QImage.Format.Format_RGB888)
                frame = frame.scaled(self.resolution[0],self.resolution[1])
                ptr = frame.bits()
                ptr.setsize(frame.sizeInBytes())                 
                frame = np.array(ptr).reshape(frame.height(), frame.width(), 3)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if self.last_frame_time is not None:
                    time_elapsed = time.time() - self.last_frame_time
                    if time_elapsed < frame_interval:
                        sleep_time = frame_interval - time_elapsed
                        time.sleep(sleep_time)

                self.video_writer.write(frame)
                self.last_frame_time = time.time()
                self.frame_index += 1

            if USE_TWO_CAMERAS and currentimageframe2 is not None:
                frame2 = currentimageframe2.toImage().convertToFormat(QImage.Format.Format_RGB888)
                frame2 = frame2.scaled(self.resolution[0],self.resolution[1])
                ptr2 = frame2.bits()
                ptr2.setsize(frame2.sizeInBytes())                 
                frame2 = np.array(ptr2).reshape(frame2.height(), frame2.width(), 3)
                frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)

                if self.last_frame_time is not None:
                    time_elapsed = time.time() - self.last_frame_time
                    if time_elapsed < frame_interval:
                        sleep_time = frame_interval - time_elapsed
                        time.sleep(sleep_time)

                self.video_writer2.write(frame2)

            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < frame_interval:
                sleep_time = frame_interval - elapsed_time
                time.sleep(sleep_time)

    def start_stop_recording(self, state):
        self.framerate = 60 #fps
        self.resolution = (1440, 1080)
        if state == "start":
            self.frame_index = 0
            self.stop_recording_tag = False  # Reset the stop_recording_tag

            # Create a temporary video file
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            #self.temp_filename = os.path.join(temp_dir, f"temp_video_{timestamp}.avi")
            self.temp_filename = os.path.join(temp_dir, f"temp_video.avi")
            self.temp_filename2 = os.path.join(temp_dir, f"temp_video2.avi")

            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(self.temp_filename, self.fourcc, self.framerate, self.resolution)
            if USE_TWO_CAMERAS:
                self.video_writer2 = cv2.VideoWriter(self.temp_filename2, self.fourcc, self.framerate, self.resolution)

            self.last_frame_time = time.time()
            threading.Thread(target=self.recording_thread).start()  # Start frame recording

        elif state == "reload":
            self.frame_index = 0
            self.stop_recording_tag = False  # Reset the stop_recording_tag

            # Create a temporary video file
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            #self.temp_filename = os.path.join(temp_dir, f"temp_video_{timestamp}.avi")
            self.temp_filename = os.path.join(temp_dir, "temp_video.avi")
            self.temp_filename2 = os.path.join(temp_dir, "temp_video2.avi")

            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer.open(self.temp_filename, self.fourcc, self.framerate, self.resolution)
            if USE_TWO_CAMERAS:
                self.video_writer2.open(self.temp_filename2, self.fourcc, self.framerate, self.resolution)

        else:
            self.stop_recording_tag = True


    def logs_save(self):
        savefile_dialog_path, _ = QFileDialog.getSaveFileName(self, "Guardar Ficheiro de Logs", "", "Ficheiro de Texto (*.txt);;Todos os Ficheiros (*)")
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
            self.show_error("Erro: OS não suportado.")

    def settings_open(self):
        config_path = "config.ini"
        if sys.platform.startswith('win'):
            os.startfile(config_path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', config_path])
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', config_path])
        else:
            self.show_error("Erro: OS não suportado.")
    
    def colorfilters_open(self):  
        os.chdir(os.path.dirname(os.path.abspath(__file__))) 
        try:
            self.colorfilters = ColorFilters()
            self.colorfilters.show()
            self.inputfilters = InputFilters()
            self.inputfilters.show()
        except UILoadingException as exp:
            MyApp.show_error(self, str(exp))

    def info_open(self):    
        info_dialog = AboutDialog()
        info_dialog.exec()

    def detectionmode_changed(self):
        '''
        try:
            self.inputfilters = InputFilters()
            self.inputfilters.close() #close filters if opened-
        except:
            pass
        '''
        if self.detectionmode_COMBOBOX.currentIndex() in [-1, 0, 1]:
            self.threshold1_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threshold1_value'))
            self.threshold2_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threshold2_value'))
        elif self.detectionmode_COMBOBOX.currentIndex() == 2:
            self.threshold1_SLIDER.setValue(config.getint('CUSTOM_DETECTION_CONFIG', 'threshold1_value'))
            self.threshold2_SLIDER.setValue(config.getint('CUSTOM_DETECTION_CONFIG', 'threshold2_value'))
        self.update_config()
    
    def update_config(self):
        global USE_TWO_CAMERAS
        if self.detectionmode_COMBOBOX.currentIndex() in [-1, 0, 1]:
            config.set('DETECTION_CONFIG', 'threshold1_value', str(self.threshold1_SLIDER.value()))
            config.set('DETECTION_CONFIG', 'threshold2_value', str(self.threshold2_SLIDER.value()))
        elif self.detectionmode_COMBOBOX.currentIndex() == 2:
            config.set('CUSTOM_DETECTION_CONFIG', 'threshold1_value', str(self.threshold1_SLIDER.value()))
            config.set('CUSTOM_DETECTION_CONFIG', 'threshold2_value', str(self.threshold2_SLIDER.value()))
        config.set('DETECTION_CONFIG', 'mode_value', str(self.mode_COMBOBOX.currentIndex()))
        config.set('DETECTION_CONFIG', 'detectionmode_value', str(self.detectionmode_COMBOBOX.currentIndex()))
        config.set('DETECTION_CONFIG', 'categorizationmode_value', str(self.categorizationmode_COMBOBOX.currentIndex()))
        config.set('CAMERA_CONFIG', 'use_two_cameras', str(self.cam2_RADIOBT.isChecked()))
        USE_TWO_CAMERAS = self.cam2_RADIOBT.isChecked()

        
        # Save the changes
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    
    # =========================== ALERTS ===========================
    def show_warning(self, msg):
        MyApp.show_alert(self, "Aviso", msg, QMessageBox.Icon.Warning)

    def show_error(self, msg):
        MyApp.show_alert(self, "Erro", msg, QMessageBox.Icon.Critical)

    def show_info(self, msg):
        MyApp.show_alert(self, "Informação", msg, QMessageBox.Icon.Information)

    # ===============================================================
    def show_alert(self, title, msg, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowIcon(self.icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setIcon(icon)  # Use QMessageBox.Icon.Warning for a warning icon
        msg_box.exec()

    def modify_startbutton(self, state):
        if state == "parar":
            self.start_BT.setText("PARAR (P)")
            self.start_BT.setShortcut(QKeySequence.fromString("P"))
            self.start_BT.setFixedSize(101, 24)
            self.start_BT.move(660, 77)
        else:
            self.start_BT.setText("INICIAR (I)")
            self.start_BT.setShortcut(QKeySequence.fromString("I"))
            self.start_BT.setFixedSize(101, 54)
            self.start_BT.move(660, 47)

        #meter animação de transição, ou não6

    def nextframe(self):
        if not self.videoplaying and not self.camopen:
            self.show_warning("Erro: Comece uma captura de câmara ou abra um vídeo.")
            self.nextframe_BT.setShortcut("")
        self.nextframe_BT.setText("NEXT FRAME (N)")
        self.nextframe_BT.setShortcut("N")
        self.showframescontinuously = False
        self.nextframebool = True 
        self.start_BT.setText("RETOMAR (R)")
        self.start_BT.setShortcut("R")

def update_config_value(tab, var, val):
    config.set(tab, var, val)

    # Save the changes
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

class WorkerThread(QThread):
    update_signal = pyqtSignal(int, float)

    def __init__(self):
        super().__init__()
        self.false_positives = 0
        self.average_diameter = 0.0

    def set_initial_values(self, false_positives, average_diameter):
        self.false_positives = false_positives
        self.average_diameter = average_diameter

    def run(self):
        # Simulate some work in the background
        while True:
            # Update UI with the current values
            self.update_signal.emit(self.false_positives, self.average_diameter)
            self.sleep(100)  # Simulate some processing time

# =========================== \\---// ===========================
class Filter:
    def __init__(self):
        self.values = {}

class ColorFilters(QWidget):
    def __init__(self):
        super().__init__()
        app.setWindowIcon(QIcon('ui/icons/apple.ico'))
        #Load UI File
        try:
            loadUi(os.path.abspath('ui/filters.ui'), self)
        except Exception as uiexp:
            raise UILoadingException("Erro: Falha de carregamento da UI dos filtros, tente novamente.") from uiexp
            return
        
        screen_center = QGuiApplication.primaryScreen().availableGeometry().center()
        self.move(int(screen_center.x() + 796 / 2), int(screen_center.y() - self.height() / 2))
        '''
        if DETECTIONMODE == 2:
            self.title_lb.setText('<html><head/><body><p><span style=" font-weight:600;">Filtros de Saída</span> [Tempo Real]</p></body></html>')
            self.setWindowTitle("Controlo de Filtros [Saída]")
        '''
        #Initialize the Values from the Config File
        self.minhue_slider.setValue(config.getint('FILTER_CONFIG','min_hue'))
        self.maxhue_slider.setValue(config.getint('FILTER_CONFIG','max_hue'))
        self.minsat_slider.setValue(config.getint('FILTER_CONFIG','min_saturation'))
        self.maxsat_slider.setValue(config.getint('FILTER_CONFIG','max_saturation'))
        self.minval_slider.setValue(config.getint('FILTER_CONFIG','min_value'))
        self.maxval_slider.setValue(config.getint('FILTER_CONFIG','max_value'))
        self.hueaddsub_slider.setValue(config.getint('FILTER_CONFIG','hue_modifier'))
        self.sataddsub_slider.setValue(config.getint('FILTER_CONFIG','saturation_modifier'))
        self.valaddsub_slider.setValue(config.getint('FILTER_CONFIG','value_modifier'))
        self.blurkernelsize_slider.setValue(config.getint('FILTER_CONFIG','blur_kernelsize'))
        self.gaussianblur_slider.setValue(config.getint('FILTER_CONFIG','gaussian_blur'))
        self.kernelsize_slider.setValue(config.getint('FILTER_CONFIG','kernelsize'))
        self.cannyerode_slider.setValue(config.getint('FILTER_CONFIG','canny_erode'))
        self.cannydilate_slider.setValue(config.getint('FILTER_CONFIG','canny_dilate'))
        self.canny1_slider.setValue(config.getint('FILTER_CONFIG','canny_1'))
        self.canny2_slider.setValue(config.getint('FILTER_CONFIG','canny_2'))
        self.output_erode_slider.setValue(config.getint('FILTER_CONFIG','output_erode'))
        self.output_dilate_slider.setValue(config.getint('FILTER_CONFIG','output_dilate'))

        self.minhue_spinbox.setValue(config.getint('FILTER_CONFIG','min_hue'))
        self.maxhue_spinbox.setValue(config.getint('FILTER_CONFIG','max_hue'))
        self.minsat_spinbox.setValue(config.getint('FILTER_CONFIG','min_saturation'))
        self.maxsat_spinbox.setValue(config.getint('FILTER_CONFIG','max_saturation'))
        self.minval_spinbox.setValue(config.getint('FILTER_CONFIG','min_value'))
        self.maxval_spinbox.setValue(config.getint('FILTER_CONFIG','max_value'))
        self.hueaddsub_slider.setValue(config.getint('FILTER_CONFIG','hue_modifier'))
        self.sataddsub_spinbox.setValue(config.getint('FILTER_CONFIG','saturation_modifier'))
        self.valaddsub_spinbox.setValue(config.getint('FILTER_CONFIG','value_modifier'))
        self.blurkernelsize_spinbox.setValue(config.getint('FILTER_CONFIG','blur_kernelsize'))
        self.gaussianblur_spinbox.setValue(config.getint('FILTER_CONFIG','gaussian_blur'))
        self.kernelsize_spinbox.setValue(config.getint('FILTER_CONFIG','kernelsize'))
        self.cannyerode_spinbox.setValue(config.getint('FILTER_CONFIG','canny_erode'))
        self.cannydilate_spinbox.setValue(config.getint('FILTER_CONFIG','canny_dilate'))
        self.canny1_spinbox.setValue(config.getint('FILTER_CONFIG','canny_1'))
        self.canny2_spinbox.setValue(config.getint('FILTER_CONFIG','canny_2'))
        self.output_erode_spinbox.setValue(config.getint('FILTER_CONFIG','output_erode'))
        self.output_dilate_spinbox.setValue(config.getint('FILTER_CONFIG','output_dilate'))

        self.canny_radiobt.setChecked(config.getboolean('FILTER_CONFIG','canny_edge_enabled'))
        self.sobel_radiobt.setChecked(config.getboolean('FILTER_CONFIG','sobel_enabled'))
        self.laplace_radiobt.setChecked(config.getboolean('FILTER_CONFIG','laplace_enabled'))
        self.updatefiltervalues()
        self.enable_gui_controls()

        # Refresh when Changed
        self.reset_bt.clicked.connect(self.reset_values)
        self.close_bt.clicked.connect(self.close_widget)
        self.canny_radiobt.toggled.connect(self.cannyactivated)
        self.sobel_radiobt.toggled.connect(self.sobelactivated)
        self.laplace_radiobt.toggled.connect(self.laplaceactivated)

        self.minhue_slider.valueChanged.connect(self.spinboxupdate)
        self.minsat_slider.valueChanged.connect(self.spinboxupdate)
        self.minval_slider.valueChanged.connect(self.spinboxupdate)
        self.maxhue_slider.valueChanged.connect(self.spinboxupdate)
        self.maxsat_slider.valueChanged.connect(self.spinboxupdate)
        self.maxval_slider.valueChanged.connect(self.spinboxupdate)
        self.hueaddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.sataddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.valaddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.blurkernelsize_slider.valueChanged.connect(self.spinboxupdate)
        self.gaussianblur_slider.valueChanged.connect(self.spinboxupdate)
        self.kernelsize_slider.valueChanged.connect(self.spinboxupdate)
        self.cannyerode_slider.valueChanged.connect(self.spinboxupdate)
        self.cannydilate_slider.valueChanged.connect(self.spinboxupdate)
        self.canny1_slider.valueChanged.connect(self.spinboxupdate)
        self.canny2_slider.valueChanged.connect(self.spinboxupdate)
        self.output_erode_slider.valueChanged.connect(self.spinboxupdate)
        self.output_dilate_slider.valueChanged.connect(self.spinboxupdate)

        self.minhue_spinbox.valueChanged.connect(self.sliderupdate)
        self.minsat_spinbox.valueChanged.connect(self.sliderupdate)
        self.minval_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxhue_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxsat_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxval_spinbox.valueChanged.connect(self.sliderupdate)
        self.hueaddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.sataddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.valaddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.blurkernelsize_spinbox.valueChanged.connect(self.sliderupdate)
        self.gaussianblur_spinbox.valueChanged.connect(self.sliderupdate)
        self.kernelsize_spinbox.valueChanged.connect(self.sliderupdate)
        self.cannyerode_spinbox.valueChanged.connect(self.sliderupdate)
        self.cannydilate_spinbox.valueChanged.connect(self.sliderupdate)
        self.canny1_spinbox.valueChanged.connect(self.sliderupdate)
        self.canny2_spinbox.valueChanged.connect(self.sliderupdate)
        self.output_erode_spinbox.valueChanged.connect(self.sliderupdate)
        self.output_dilate_spinbox.valueChanged.connect(self.sliderupdate)

    def sliderupdate(self):
        self.minhue_slider.setValue(self.minhue_spinbox.value())
        self.minsat_slider.setValue(self.minsat_spinbox.value())
        self.minval_slider.setValue(self.minval_spinbox.value())
        self.maxhue_slider.setValue(self.maxhue_spinbox.value())
        self.maxsat_slider.setValue(self.maxsat_spinbox.value())
        self.maxval_slider.setValue(self.maxval_spinbox.value())
        self.blurkernelsize_slider.setValue(self.blurkernelsize_spinbox.value())
        self.gaussianblur_slider.setValue(self.gaussianblur_spinbox.value())
        self.hueaddsub_slider.setValue(self.hueaddsub_spinbox.value())
        self.sataddsub_slider.setValue(self.sataddsub_spinbox.value())
        self.valaddsub_slider.setValue(self.valaddsub_spinbox.value())
        self.kernelsize_slider.setValue(self.kernelsize_spinbox.value())
        self.cannyerode_slider.setValue(self.cannyerode_spinbox.value())
        self.cannydilate_slider.setValue(self.cannydilate_spinbox.value())
        self.canny1_slider.setValue(self.canny1_spinbox.value())
        self.canny2_slider.setValue(self.canny2_spinbox.value())
        self.output_erode_slider.setValue(self.output_erode_spinbox.value())
        self.output_dilate_slider.setValue(self.output_dilate_spinbox.value())
        self.sliderupdate_kernelsize()
        self.updateconfigfiltervalues()

    def spinboxupdate(self):
        self.minhue_spinbox.setValue(self.minhue_slider.value())
        self.minsat_spinbox.setValue(self.minsat_slider.value())
        self.minval_spinbox.setValue(self.minval_slider.value())
        self.maxhue_spinbox.setValue(self.maxhue_slider.value())
        self.maxsat_spinbox.setValue(self.maxsat_slider.value())
        self.maxval_spinbox.setValue(self.maxval_slider.value())
        self.blurkernelsize_spinbox.setValue(self.blurkernelsize_slider.value())
        self.gaussianblur_spinbox.setValue(self.gaussianblur_slider.value())
        self.hueaddsub_spinbox.setValue(self.hueaddsub_slider.value())
        self.sataddsub_spinbox.setValue(self.sataddsub_slider.value())
        self.valaddsub_spinbox.setValue(self.valaddsub_slider.value())
        self.kernelsize_spinbox.setValue(self.kernelsize_slider.value())
        self.cannyerode_spinbox.setValue(self.cannyerode_slider.value())
        self.cannydilate_spinbox.setValue(self.cannydilate_slider.value())
        self.canny1_spinbox.setValue(self.canny1_slider.value())
        self.canny2_spinbox.setValue(self.canny2_slider.value())
        self.output_erode_spinbox.setValue(self.output_erode_slider.value())
        self.output_dilate_spinbox.setValue(self.output_dilate_slider.value())
        self.spinboxupdate_kernelsize()
        self.updateconfigfiltervalues()

    def sliderupdate_kernelsize(self):
        if (self.blurkernelsize_spinbox.value()%2)==0: #check if is pair
            self.blurkernelsize_spinbox.setValue(self.blurkernelsize_spinbox.value()+1) #if pair add 1
        self.blurkernelsize_slider.setValue(self.blurkernelsize_spinbox.value()) #set slider value
        if (self.sobel_radiobt.isChecked() or self.laplace_radiobt.isChecked()) and ((self.kernelsize_spinbox.value()%2)==0): #if sobel or laplace make the values odd too
            self.kernelsize_spinbox.setValue(self.kernelsize_spinbox.value()+1) #if pair add 1
        self.kernelsize_slider.setValue(self.kernelsize_spinbox.value()) #set slider value

    def spinboxupdate_kernelsize(self):
        if (self.blurkernelsize_slider.value()%2)==0: #check if is pair
            self.blurkernelsize_slider.setValue(self.blurkernelsize_slider.value()+1) #if pair add 1
        self.blurkernelsize_spinbox.setValue(self.blurkernelsize_slider.value()) #set spinbox value
        if (self.sobel_radiobt.isChecked() or self.laplace_radiobt.isChecked()) and ((self.kernelsize_slider.value()%2)==0): #if sobel or laplace make the values odd too
            self.kernelsize_slider.setValue(self.kernelsize_slider.value()+1) #if pair add 1
        self.kernelsize_spinbox.setValue(self.kernelsize_slider.value()) #set spinbox value

    def cannyactivated(self, checked):
        if checked:
            self.sobel_radiobt.setChecked(False)
            self.laplace_radiobt.setChecked(False)
        self.updateconfigfiltervalues()
        self.spinboxupdate_kernelsize()
    def sobelactivated(self, checked):
        if checked:
            self.canny_radiobt.setChecked(False)
            self.laplace_radiobt.setChecked(False)
        self.updateconfigfiltervalues()
        self.spinboxupdate_kernelsize()
    def laplaceactivated(self, checked):
        if checked:
            self.canny_radiobt.setChecked(False)
            self.sobel_radiobt.setChecked(False)
        self.updateconfigfiltervalues()
        self.spinboxupdate_kernelsize()
        
    def updateconfigfiltervalues(self):
        update_config_value('FILTER_CONFIG', 'min_hue', str(self.minhue_slider.value()))
        update_config_value('FILTER_CONFIG', 'max_hue', str(self.maxhue_slider.value()))
        update_config_value('FILTER_CONFIG', 'min_saturation', str(self.minsat_slider.value()))
        update_config_value('FILTER_CONFIG', 'max_saturation', str(self.maxsat_slider.value()))
        update_config_value('FILTER_CONFIG', 'min_value', str(self.minval_slider.value()))
        update_config_value('FILTER_CONFIG', 'max_value', str(self.maxval_slider.value()))
        update_config_value('FILTER_CONFIG', 'blur_kernelsize', str(self.blurkernelsize_slider.value()))
        update_config_value('FILTER_CONFIG', 'gaussian_blur', str(self.gaussianblur_slider.value()))
        update_config_value('FILTER_CONFIG', 'hue_modifier', str(self.hueaddsub_slider.value()))
        update_config_value('FILTER_CONFIG', 'saturation_modifier', str(self.sataddsub_slider.value()))
        update_config_value('FILTER_CONFIG', 'value_modifier', str(self.valaddsub_slider.value()))
        update_config_value('FILTER_CONFIG', 'kernelsize', str(self.kernelsize_slider.value()))
        update_config_value('FILTER_CONFIG', 'canny_erode', str(self.cannyerode_slider.value()))
        update_config_value('FILTER_CONFIG', 'canny_dilate', str(self.cannydilate_slider.value()))
        update_config_value('FILTER_CONFIG', 'canny_1', str(self.canny1_slider.value()))
        update_config_value('FILTER_CONFIG', 'canny_2', str(self.canny2_slider.value()))
        update_config_value('FILTER_CONFIG', 'canny_edge_enabled', str(self.canny_radiobt.isChecked()))
        update_config_value('FILTER_CONFIG', 'sobel_enabled', str(self.sobel_radiobt.isChecked()))
        update_config_value('FILTER_CONFIG', 'laplace_enabled', str(self.laplace_radiobt.isChecked()))
        update_config_value('FILTER_CONFIG', 'output_erode', str(self.output_erode_slider.value()))
        update_config_value('FILTER_CONFIG', 'output_dilate', str(self.output_dilate_slider.value()))
        self.updatefiltervalues()
        #self.saveconfigfile(config)


    # returns an HSV filter object based on the control GUI values and Canny edge filter object based on the control GUI values
    def updatefiltervalues(self):
        global filter
        filter = Filter()
        filter.enablecanny = self.canny_radiobt.isChecked()
        filter.enablesobel = self.sobel_radiobt.isChecked()
        filter.enablelaplace = self.laplace_radiobt.isChecked()
        filter.minhue = self.minhue_slider.value()
        filter.minsat = self.minsat_slider.value()
        filter.minval = self.minval_slider.value()
        filter.maxhue = self.maxhue_slider.value()
        filter.maxsat = self.maxsat_slider.value()
        filter.maxval = self.maxval_slider.value()
        filter.hue_addsub = self.hueaddsub_slider.value()
        filter.sat_addsub = self.sataddsub_slider.value()
        filter.val_addsub = self.valaddsub_slider.value()
        filter.blurkernelsize = self.blurkernelsize_slider.value()
        filter.gaussianblur = self.gaussianblur_slider.value()
        filter.kernelsize = self.kernelsize_slider.value()
        filter.cannyerode = self.cannyerode_slider.value()
        filter.cannydilate = self.cannydilate_slider.value()
        filter.canny1 = self.canny1_slider.value()
        filter.canny2 = self.canny2_slider.value()
        filter.output_erode = self.output_erode_slider.value()
        filter.output_dilate = self.output_dilate_slider.value()
        self.enable_gui_controls()

        return filter
    
    def enable_gui_controls(self):
        if filter.enablecanny or self.canny_radiobt.isChecked():
            self.kernelsize_slider.setEnabled(True)
            self.kernelsize_spinbox.setEnabled(True)
            self.cannyerode_slider.setEnabled(True)
            self.cannyerode_spinbox.setEnabled(True)
            self.cannydilate_slider.setEnabled(True)
            self.cannydilate_spinbox.setEnabled(True)
            self.canny1_slider.setEnabled(True)
            self.canny1_spinbox.setEnabled(True)
            self.canny2_slider.setEnabled(True)
            self.canny2_spinbox.setEnabled(True)
            self.output_erode_slider.setEnabled(True)
            self.output_erode_spinbox.setEnabled(True)
            self.output_dilate_slider.setEnabled(True)
            self.output_dilate_spinbox.setEnabled(True)
        elif filter.enablesobel or self.sobel_radiobt.isChecked():
            self.kernelsize_slider.setEnabled(True)
            self.kernelsize_spinbox.setEnabled(True)
            self.output_erode_slider.setEnabled(True)
            self.output_erode_spinbox.setEnabled(True)
            self.output_dilate_slider.setEnabled(True)
            self.output_dilate_spinbox.setEnabled(True)
            self.cannyerode_slider.setEnabled(False)
            self.cannyerode_spinbox.setEnabled(False)
            self.cannydilate_slider.setEnabled(False)
            self.cannydilate_spinbox.setEnabled(False)
            self.canny1_slider.setEnabled(False)
            self.canny1_spinbox.setEnabled(False)
            self.canny2_slider.setEnabled(False)
            self.canny2_spinbox.setEnabled(False)
        elif filter.enablelaplace or self.laplace_radiobt.isChecked():
            self.kernelsize_slider.setEnabled(True)
            self.kernelsize_spinbox.setEnabled(True)
            self.output_erode_slider.setEnabled(True)
            self.output_erode_spinbox.setEnabled(True)
            self.output_dilate_slider.setEnabled(True)
            self.output_dilate_spinbox.setEnabled(True)
            self.cannyerode_slider.setEnabled(False)
            self.cannyerode_spinbox.setEnabled(False)
            self.cannydilate_slider.setEnabled(False)
            self.cannydilate_spinbox.setEnabled(False)
            self.canny1_slider.setEnabled(False)
            self.canny1_spinbox.setEnabled(False)
            self.canny2_slider.setEnabled(False)
            self.canny2_spinbox.setEnabled(False)
        else:
            self.kernelsize_slider.setEnabled(False)
            self.kernelsize_spinbox.setEnabled(False)
            self.cannyerode_slider.setEnabled(False)
            self.cannyerode_spinbox.setEnabled(False)
            self.cannydilate_slider.setEnabled(False)
            self.cannydilate_spinbox.setEnabled(False)
            self.canny1_slider.setEnabled(False)
            self.canny1_spinbox.setEnabled(False)
            self.canny2_slider.setEnabled(False)
            self.canny2_spinbox.setEnabled(False)
            self.output_erode_slider.setEnabled(False)
            self.output_erode_spinbox.setEnabled(False)
            self.output_dilate_slider.setEnabled(False)
            self.output_dilate_spinbox.setEnabled(False)


    def reset_values(self):
        self.minhue_slider.setValue(0)
        self.maxhue_slider.setValue(179)
        self.minsat_slider.setValue(0)
        self.maxsat_slider.setValue(255)
        self.minval_slider.setValue(0)
        self.maxval_slider.setValue(255)
        self.hueaddsub_slider.setValue(0)
        self.sataddsub_slider.setValue(0)
        self.valaddsub_slider.setValue(0)
        self.blurkernelsize_slider.setValue(1)
        self.gaussianblur_slider.setValue(0)
        self.kernelsize_slider.setValue(1)
        self.cannyerode_slider.setValue(1)
        self.cannydilate_slider.setValue(1)
        self.canny1_slider.setValue(0)
        self.canny2_slider.setValue(255)
        self.canny_radiobt.setChecked(False)
        self.sobel_radiobt.setChecked(False)
        self.laplace_radiobt.setChecked(False)
        self.output_erode_slider.setValue(1)
        self.output_dilate_slider.setValue(1)
        self.spinboxupdate()
        #self.saveconfigfile(config)

    def saveconfigfile(self, config):
        if os.getcwd().endswith('modules'):
            cfgpath = '../config.ini'
        else:
            cfgpath = 'config.ini'
         # Save the changes
        with open(cfgpath, 'w') as config_file:
            config.write(config_file)
        
    
    def close_widget(self):
        self.close()

class UILoadingException(Exception):
    def __init__(self, message="Failed to load UI"):
        self.message = message
        super().__init__(self.message)

class InputFilters(QWidget):
    def __init__(self):
        super().__init__()
        # Load the widget UI file
        try:
            loadUi(os.path.abspath('ui/filters_input.ui'), self)
        except Exception as uiexp:
            raise UILoadingException("Erro: Falha de carregamento da UI, tente novamente.") from uiexp
            return

        screen_center = QGuiApplication.primaryScreen().availableGeometry().center()
        self.move(int(screen_center.x() -1622 / 2), int(screen_center.y() - self.height() / 2))

        #Initialize the Values from the Config File
        self.minhue_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_min_hue'))
        self.maxhue_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_max_hue'))
        self.minsat_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_min_saturation'))
        self.maxsat_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_max_saturation'))
        self.minval_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_min_value'))
        self.maxval_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_max_value'))
        self.hueaddsub_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_hue_modifier'))
        self.sataddsub_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_saturation_modifier'))
        self.valaddsub_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_value_modifier'))
        self.blurkernelsize_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_blur_kernelsize'))
        self.gaussianblur_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_gaussian_blur'))
        self.kernelsize_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_kernelsize'))
        self.erode1_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_erode1'))
        self.dilate1_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_dilate1'))
        self.erode2_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_erode2'))
        self.dilate2_slider.setValue(config.getint('FILTER_CONFIG','inputfilters_dilate2'))

        self.minhue_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_min_hue'))
        self.maxhue_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_max_hue'))
        self.minsat_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_min_saturation'))
        self.maxsat_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_max_saturation'))
        self.minval_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_min_value'))
        self.maxval_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_max_value'))
        self.hueaddsub_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_hue_modifier'))
        self.sataddsub_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_saturation_modifier'))
        self.valaddsub_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_value_modifier'))
        self.blurkernelsize_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_blur_kernelsize'))
        self.gaussianblur_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_gaussian_blur'))
        self.kernelsize_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_kernelsize'))
        self.erode1_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_erode1'))
        self.dilate1_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_dilate1'))
        self.erode2_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_erode2'))
        self.dilate2_spinbox.setValue(config.getint('FILTER_CONFIG','inputfilters_dilate2'))

        self.pre_apply_radiobt.setChecked(config.getboolean('FILTER_CONFIG', 'inputfilters_pre-apply_dilate_and_erode'))
        self.post_apply_radiobt.setChecked(config.getboolean('FILTER_CONFIG', 'inputfilters_post-apply_dilate_and_erode'))

        if config.getint('DETECTION_CONFIG', "DETECTIONMODE_VALUE") != 2:
            self.post_apply_radiobt.setChecked(False)
            self.pre_apply_radiobt.setChecked(True)

        self.updateinputfiltervalues()
        self.enable_gui_controls()

        # Refresh when Changed
        self.reset_bt.clicked.connect(self.reset_values)
        self.close_bt.clicked.connect(self.close_widget)
        self.pre_apply_radiobt.toggled.connect(self.updateconfigfiltervalues)
        self.post_apply_radiobt.toggled.connect(self.updateconfigfiltervalues)

        self.minhue_slider.valueChanged.connect(self.spinboxupdate)
        self.minsat_slider.valueChanged.connect(self.spinboxupdate)
        self.minval_slider.valueChanged.connect(self.spinboxupdate)
        self.maxhue_slider.valueChanged.connect(self.spinboxupdate)
        self.maxsat_slider.valueChanged.connect(self.spinboxupdate)
        self.maxval_slider.valueChanged.connect(self.spinboxupdate)
        self.hueaddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.sataddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.valaddsub_slider.valueChanged.connect(self.spinboxupdate)
        self.blurkernelsize_slider.valueChanged.connect(self.spinboxupdate)
        self.gaussianblur_slider.valueChanged.connect(self.spinboxupdate)
        self.kernelsize_slider.valueChanged.connect(self.spinboxupdate)
        self.erode1_slider.valueChanged.connect(self.spinboxupdate)
        self.dilate1_slider.valueChanged.connect(self.spinboxupdate)
        self.erode2_slider.valueChanged.connect(self.spinboxupdate)
        self.dilate2_slider.valueChanged.connect(self.spinboxupdate)

        self.minhue_spinbox.valueChanged.connect(self.sliderupdate)
        self.minsat_spinbox.valueChanged.connect(self.sliderupdate)
        self.minval_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxhue_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxsat_spinbox.valueChanged.connect(self.sliderupdate)
        self.maxval_spinbox.valueChanged.connect(self.sliderupdate)
        self.hueaddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.sataddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.valaddsub_spinbox.valueChanged.connect(self.sliderupdate)
        self.blurkernelsize_spinbox.valueChanged.connect(self.sliderupdate)
        self.gaussianblur_spinbox.valueChanged.connect(self.sliderupdate)
        self.kernelsize_spinbox.valueChanged.connect(self.sliderupdate)
        self.erode1_spinbox.valueChanged.connect(self.sliderupdate)
        self.dilate1_spinbox.valueChanged.connect(self.sliderupdate)
        self.erode2_spinbox.valueChanged.connect(self.sliderupdate)
        self.dilate2_spinbox.valueChanged.connect(self.sliderupdate)

    def sliderupdate(self):
        self.minhue_slider.setValue(self.minhue_spinbox.value())
        self.minsat_slider.setValue(self.minsat_spinbox.value())
        self.minval_slider.setValue(self.minval_spinbox.value())
        self.maxhue_slider.setValue(self.maxhue_spinbox.value())
        self.maxsat_slider.setValue(self.maxsat_spinbox.value())
        self.maxval_slider.setValue(self.maxval_spinbox.value())
        self.blurkernelsize_slider.setValue(self.blurkernelsize_spinbox.value())
        self.gaussianblur_slider.setValue(self.gaussianblur_spinbox.value())
        self.hueaddsub_slider.setValue(self.hueaddsub_spinbox.value())
        self.sataddsub_slider.setValue(self.sataddsub_spinbox.value())
        self.valaddsub_slider.setValue(self.valaddsub_spinbox.value())
        self.kernelsize_slider.setValue(self.kernelsize_spinbox.value())
        self.erode1_slider.setValue(self.erode1_spinbox.value())
        self.dilate1_slider.setValue(self.dilate1_spinbox.value())
        self.erode2_slider.setValue(self.erode2_spinbox.value())
        self.dilate2_slider.setValue(self.dilate2_spinbox.value())
        self.sliderupdate_kernelsize()
        self.updateconfigfiltervalues()

    def spinboxupdate(self):
        self.minhue_spinbox.setValue(self.minhue_slider.value())
        self.minsat_spinbox.setValue(self.minsat_slider.value())
        self.minval_spinbox.setValue(self.minval_slider.value())
        self.maxhue_spinbox.setValue(self.maxhue_slider.value())
        self.maxsat_spinbox.setValue(self.maxsat_slider.value())
        self.maxval_spinbox.setValue(self.maxval_slider.value())
        self.blurkernelsize_spinbox.setValue(self.blurkernelsize_slider.value())
        self.gaussianblur_spinbox.setValue(self.gaussianblur_slider.value())
        self.hueaddsub_spinbox.setValue(self.hueaddsub_slider.value())
        self.sataddsub_spinbox.setValue(self.sataddsub_slider.value())
        self.valaddsub_spinbox.setValue(self.valaddsub_slider.value())
        self.kernelsize_spinbox.setValue(self.kernelsize_slider.value())
        self.erode1_spinbox.setValue(self.erode1_slider.value())
        self.dilate1_spinbox.setValue(self.dilate1_slider.value())
        self.erode2_spinbox.setValue(self.erode2_slider.value())
        self.dilate2_spinbox.setValue(self.dilate2_slider.value())
        self.spinboxupdate_kernelsize()
        self.updateconfigfiltervalues()

    def sliderupdate_kernelsize(self):
        if (self.blurkernelsize_spinbox.value()%2)==0: #check if is pair
            self.blurkernelsize_spinbox.setValue(self.blurkernelsize_spinbox.value()+1) #if pair add 1
        self.blurkernelsize_slider.setValue(self.blurkernelsize_spinbox.value()) #set slider value
        self.kernelsize_slider.setValue(self.kernelsize_spinbox.value()) #set slider value

    def spinboxupdate_kernelsize(self):
        if (self.blurkernelsize_slider.value()%2)==0: #check if is pair
            self.blurkernelsize_slider.setValue(self.blurkernelsize_slider.value()+1) #if pair add 1
        self.blurkernelsize_spinbox.setValue(self.blurkernelsize_slider.value()) #set spinbox value
        self.kernelsize_spinbox.setValue(self.kernelsize_slider.value()) #set spinbox value

        
    def updateconfigfiltervalues(self):
        update_config_value('FILTER_CONFIG', 'inputfilters_min_hue', str(self.minhue_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_max_hue', str(self.maxhue_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_min_saturation', str(self.minsat_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_max_saturation', str(self.maxsat_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_min_value', str(self.minval_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_max_value', str(self.maxval_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_blur_kernelsize', str(self.blurkernelsize_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_gaussian_blur', str(self.gaussianblur_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_hue_modifier', str(self.hueaddsub_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_saturation_modifier', str(self.sataddsub_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_value_modifier', str(self.valaddsub_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_kernelsize', str(self.kernelsize_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_erode1', str(self.erode2_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_dilate1', str(self.dilate2_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_erode2', str(self.erode2_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_dilate2', str(self.dilate2_slider.value()))
        update_config_value('FILTER_CONFIG', 'inputfilters_pre-apply_dilate_and_erode', str(self.pre_apply_radiobt.isChecked()))
        update_config_value('FILTER_CONFIG', 'inputfilters_post-apply_dilate_and_erode', str(self.post_apply_radiobt.isChecked()))
        self.updateinputfiltervalues()
        self.enable_gui_controls()
        #self.saveconfigfile(config)

    def enable_gui_controls(self):
        if config.getint('DETECTION_CONFIG', "DETECTIONMODE_VALUE") == 2:
            self.post_apply_radiobt.setEnabled(True)
            '''
            self.kernelsize_slider.setEnabled(True)
            self.kernelsize_spinbox.setEnabled(True)
            self.dilate1_slider.setEnabled(True)
            self.dilate1_spinbox.setEnabled(True)
            self.erode1_slider.setEnabled(True)
            self.erode1_spinbox.setEnabled(True)
            self.dilate2_slider.setEnabled(True)
            self.dilate2_spinbox.setEnabled(True)
            self.erode2_slider.setEnabled(True)
            self.erode2_spinbox.setEnabled(True)
            '''
        else:
            self.post_apply_radiobt.setEnabled(False)
            '''
            self.kernelsize_slider.setEnabled(False)
            self.kernelsize_spinbox.setEnabled(False)
            self.dilate1_slider.setEnabled(False)
            self.dilate1_spinbox.setEnabled(False)
            self.erode1_slider.setEnabled(False)
            self.erode1_spinbox.setEnabled(False)
            self.dilate2_slider.setEnabled(False)
            self.dilate2_spinbox.setEnabled(False)
            self.erode2_slider.setEnabled(False)
            self.erode2_spinbox.setEnabled(False)
            '''


    def reset_values(self):
        self.minhue_slider.setValue(0)
        self.maxhue_slider.setValue(179)
        self.minsat_slider.setValue(0)
        self.maxsat_slider.setValue(255)
        self.minval_slider.setValue(0)
        self.maxval_slider.setValue(255)
        self.hueaddsub_slider.setValue(0)
        self.sataddsub_slider.setValue(0)
        self.valaddsub_slider.setValue(0)
        self.gaussianblur_slider.setValue(0)
        self.blurkernelsize_slider.setValue(0)
        self.kernelsize_slider.setValue(1)
        self.erode1_slider.setValue(1)
        self.dilate1_slider.setValue(1)
        self.erode2_slider.setValue(1)
        self.dilate2_slider.setValue(1)
        self.pre_apply_radiobt.setChecked(False)
        self.post_apply_radiobt.setChecked(True)
        self.spinboxupdate()
        #self.saveconfigfile(config)
        

    def saveconfigfile(self, config):
        cfgpath = 'config.ini'
         # Save the changes
        with open(cfgpath, 'w') as config_file:
            config.write(config_file)
        
    def updateinputfiltervalues(self):
        config.read('config.ini')  # Replace 'config.ini' with the path to your configuration file
        global customdetectionfilter
        customdetectionfilter = Filter()
        customdetectionfilter.minhue = self.minhue_slider.value()
        customdetectionfilter.minsat = self.minsat_slider.value()
        customdetectionfilter.minval = self.minval_slider.value()
        customdetectionfilter.maxhue = self.maxhue_slider.value()
        customdetectionfilter.maxsat = self.maxsat_slider.value()
        customdetectionfilter.maxval = self.maxval_slider.value()
        customdetectionfilter.hue_addsub = self.hueaddsub_slider.value()
        customdetectionfilter.sat_addsub = self.sataddsub_slider.value()
        customdetectionfilter.val_addsub = self.valaddsub_slider.value()
        customdetectionfilter.blurkernelsize = self.blurkernelsize_slider.value()
        customdetectionfilter.gaussianblur = self.gaussianblur_slider.value()
        customdetectionfilter.kernelsize = self.kernelsize_slider.value()
        customdetectionfilter.erode1 = self.erode1_slider.value()
        customdetectionfilter.dilate1 = self.dilate1_slider.value()
        customdetectionfilter.erode2 = self.erode2_slider.value()
        customdetectionfilter.dilate2 = self.dilate2_slider.value()
        customdetectionfilter.dilate_erode_pre_apply = self.pre_apply_radiobt.isChecked()
        customdetectionfilter.dilate_erode_post_apply = self.post_apply_radiobt.isChecked()

        return customdetectionfilter
    
    def close_widget(self):
        self.close()

#####################################################################################################

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setWindowTitle("Informações")
        #self.setMinimumWidth(405)  # Adjust the width as needed

        # Create a label for the image
        image_label = QLabel()
        pixmap = QPixmap("ui/icons/apple.png")  # Replace with the path to your image

        # Resize the image
        #new_width = 200  # Adjust the width as needed
        #new_height = 150  # Adjust the height as needed
        #pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)

        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the title and description text
        title_text = QLabel("<b>CATEGORIZAÇÃO DE MAÇÃS</b>")
        title_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_text = QLabel("Esta aplicação separa maçãs entre GRANDES, PEQUENAS e DEFEITUOSAS.\n")
        description_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a paragraph to explain the keys
        keys_title = QLabel("<b>– Atalhos de Teclado:</b>")
        keys_paragraph = QLabel(
            "Iniciar/Parar - I ou P\n"
            "Congelar Frame - C\n"
            "Próximo Frame - N\n"
            "Retomar Vídeo/Captura - R\n"
            "Abrir/Carregar - Ctrl+O, Ctrl+A ou A\n"
            "Guardar - Ctrl+S ou Ctrl+G\n"
            "Guardar Frame - Ctrl+F\n"
            "Vista Pequena - Ctrl+Left\n"
            "Vista Grande - Ctrl+Right\n"
            "Vista Grande - Separador Seguinte - Ctrl+Up\n"
            "Vista Grande - Separador Anterior - Ctrl+Down\n"
            "Vista de Operador - Ctrl+End\n"
            "Reiniciar Contagem - Ctrl+R\n"
            "Calibrar Câmara - Ctrl+Shift+C\n"
            "Abrir Configuração - Ctrl+D\n"
            "Ver Logs - Ctrl+L\n"
            "Exportar Logs - Ctrl+Shift+L\n"
            "Reiniciar App - Ctrl+Shift+R"
        )
        keys_paragraph.setWordWrap(True)  # Enable word wrapping for long lines

        # Add the copyright text
        copyright_text = QLabel("Copyright © JBC 2023")
        copyright_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(title_text)
        layout.addWidget(description_text)
        layout.addWidget(keys_title)
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

# ==== INICIALIZAÇÃO INICIAL DOS VALORES DOS FILTROS ====
global filter
filter = Filter()
filter.minhue = config.getint('FILTER_CONFIG','min_hue')
filter.maxhue = config.getint('FILTER_CONFIG','max_hue')
filter.minsat = config.getint('FILTER_CONFIG','min_saturation')
filter.maxsat = config.getint('FILTER_CONFIG','max_saturation')
filter.minval = config.getint('FILTER_CONFIG','min_value')
filter.maxval = config.getint('FILTER_CONFIG','max_value')
filter.hue_addsub = config.getint('FILTER_CONFIG','hue_modifier')
filter.sat_addsub = config.getint('FILTER_CONFIG','saturation_modifier')
filter.val_addsub = config.getint('FILTER_CONFIG','value_modifier')
filter.gaussianblur = config.getint('FILTER_CONFIG','gaussian_blur')
filter.blurkernelsize = config.getint('FILTER_CONFIG', 'blur_kernelsize')
filter.kernelsize = config.getint('FILTER_CONFIG','kernelsize')
filter.cannyerode = config.getint('FILTER_CONFIG','canny_erode')
filter.cannydilate = config.getint('FILTER_CONFIG','canny_dilate')
filter.canny1 = config.getint('FILTER_CONFIG','canny_1')
filter.canny2 = config.getint('FILTER_CONFIG','canny_2')
filter.enablecanny = config.getboolean('FILTER_CONFIG','canny_edge_enabled')
filter.enablesobel = config.getboolean('FILTER_CONFIG', 'sobel_enabled')
filter.enablelaplace = config.getboolean('FILTER_CONFIG', 'laplace_enabled')
filter.output_erode = config.getint('FILTER_CONFIG', 'output_erode')
filter.output_dilate = config.getint('FILTER_CONFIG', 'output_dilate')
# ======================== \\-// ========================
# ==== INICIALIZAÇÃO INICIAL DOS VALORES DOS FILTROS ====
global customdetectionfilter
customdetectionfilter = Filter()
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
customdetectionfilter.dilate_erode_pre_apply = config.getboolean('FILTER_CONFIG', 'inputfilters_pre-apply_dilate_and_erode')
customdetectionfilter.dilate_erode_post_apply = config.getboolean('FILTER_CONFIG', 'inputfilters_post-apply_dilate_and_erode')
# ======================== \\-// ========================

# SplashScreen class
class SplashScreen(QMainWindow):
    def __init__(self, text="A Carregar: Dependências"):
        super().__init__()
        self.setWindowIcon(QIcon('ui/icons/apple.ico'))
        self.setStyleSheet("background-color: rgb(255,255,255);")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        central_widget = QWidget()
        central_widget.setStyleSheet("border: 5px solid black;")
        central_widget.setContentsMargins(10, 6, 10, 6)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_label = QLabel("Categorização de Maçãs", self)
        text_label.setStyleSheet("font-size: 24pt; color: black; font-weight: bold; text-align: center; border: None;")
        layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

        gif_label = QLabel(self)
        gif_label.setStyleSheet("border: None;")
        movie = QMovie("ui/icons/gif.gif")
        gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(gif_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.loading_label = QLabel(text, self)
        self.loading_label.setStyleSheet("font-size: 8pt; color: black; text-align: center; border: None;")
        layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignCenter)

        spacer = QLabel(self)
        spacer.setStyleSheet("border: None;")
        spacer.setFixedHeight(40)
        layout.addWidget(spacer, alignment=Qt.AlignmentFlag.AlignCenter)
        
        footer_label = QLabel("© JBC 2023", self)
        footer_label.setStyleSheet("font-size: 10pt; color: gray; text-align: center; border: None;")
        layout.addWidget(footer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.centerOnScreen()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor('#222222'))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def centerOnScreen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = int(round(screen_geometry.width()/2 - 200, 1))
        y = int(round(screen_geometry.height()/2 - 206, 1))
        self.move(x, y)

        # Connect the worker to the SplashScreen
        self.worker = Worker()
        self.worker.finished.connect(self.on_worker_finished)

        # Start the worker
        self.worker.start()

    def on_worker_finished(self):
        # Close the splash screen when the worker finishes
        self.close()

class Worker(QThread):
    finished = pyqtSignal()

    def run(self):
        time.sleep(0.5)
        imports()
        time.sleep(0.5)
        self.finished.emit()

# ========== CONSTRUCTOR ==========   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_splash = SplashScreen()
    loading_splash.show()
    app.exec()
    app2 = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec())