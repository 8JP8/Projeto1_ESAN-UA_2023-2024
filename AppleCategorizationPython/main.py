from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTabWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QApplication, QGridLayout, QPushButton, QStyle, QWidget, QMenu
from PyQt6.QtGui import QImage, QPixmap, QIcon, QCloseEvent, QAction, QKeySequence, QShortcut
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import threading
import shutil
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

class MyApp(QMainWindow):
    def __init__(self):
        super (MyApp, self).__init__()
        loadUi('app.ui', self)
        app.setWindowIcon(QIcon('apple.ico'))
        self.pid = QApplication.applicationPid()
        
        # ============ INICIALIZAÇÃO COM OS VALORES DA CONFIG ============
        self.threashold1_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threashold1_value'))
        self.threashold2_SLIDER.setValue(config.getint('DETECTION_CONFIG', 'threashold2_value'))
        self.mode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'mode_value'))
        self.detectionmode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'detectionmode_value'))
        self.categorizationmode_COMBOBOX.setCurrentIndex(config.getint('DETECTION_CONFIG', 'categorizationmode_value'))
        self.cam2_RADIOBT.setChecked(config.getboolean('CAMERA_CONFIG', 'use_two_cameras'))
        # ============================= \\-// ============================

        # ============ BINDS ============
        self.upload_BT.clicked.connect(self.load_file)
        self.start_BT.setShortcut("Ctrl+Enter")
        self.start_BT.clicked.connect(self.start)
        self.actionOpen_Upload.setShortcuts([QKeySequence.fromString("Ctrl+O"), QKeySequence.fromString("Ctrl+A")])
        self.actionOpen_Upload.triggered.connect(self.load_file)
        self.actionSave_Output_File.triggered.connect(self.save_file)
        self.actionSave_Output_File.setShortcuts([QKeySequence.fromString("Ctrl+S"), QKeySequence.fromString("Ctrl+G")])
        self.action_small_view.triggered.connect(self.small_vw)
        self.action_big_view.triggered.connect(self.big_vw)
        self.action_small_view.setShortcut("Ctrl+Left")
        self.action_big_view.setShortcut("Ctrl+Right")
        #self.menuLogs.aboutToShow.connect(self.logs_open)
        #self.shortcut = QShortcut(QKeySequence('Ctrl+L'), self)
        #self.shortcut.activated.connect(self.logs_open) 
        self.action_Logs.triggered.connect(self.logs_open)
        self.action_exportLogs.triggered.connect(self.logs_save)
        self.action_Logs.setShortcut("Ctrl+L")
        self.action_exportLogs.setShortcut("Ctrl+Shift+L")
        self.menuHelp.aboutToShow.connect(self.help_open)
        self.threashold1_SLIDER.valueChanged.connect(self.update_config)
        self.threashold2_SLIDER.valueChanged.connect(self.update_config)
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
        self.thread_stop_flag = False
        self.filename = str()

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
            self.show_warning("Está a ser processado vídeo: Carregue PARAR (Ctrl+Enter) ou feche a App.")
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
                width_scale = int(self.inputframe_1.width()) / image.shape[1]
                height_scale = int(self.inputframe_1.height()) / image.shape[0]
                scale = min(width_scale, height_scale)
                frame = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
                # ======== CALCULATIONS TO KEEP IMAGE ASPECT RATIO 2 ========
                width_scale2 = int(self.inputframe_3.width()) / image.shape[1]
                height_scale2 = int(self.inputframe_3.height()) / image.shape[0]
                scale2 = min(width_scale2, height_scale2)
                frame2 = cv2.resize(image, (int(image.shape[1] * scale2), int(image.shape[0] * scale2)))
                # ====================== CENTER THE IMAGE ====================== 
                emptyframe = np.full((self.inputframe_1.height(), self.inputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                x_offset = (self.inputframe_1.width() - frame.shape[1]) // 2
                y_offset = (self.inputframe_1.height() - frame.shape[0]) // 2
                emptyframe[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = frame        # Paste the resized image onto the empty frame
                # ====================== CENTER THE IMAGE ====================== 
                emptyframe2 = np.full((self.inputframe_3.height(), self.inputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                x_offset2 = (self.inputframe_3.width() - frame2.shape[1]) // 2
                y_offset2 = (self.inputframe_3.height() - frame2.shape[0]) // 2
                emptyframe2[y_offset2:y_offset2+frame2.shape[0], x_offset2:x_offset2+frame2.shape[1]] = frame2 
                # ==================== CONVERT IMAGE FORMAT ====================
                # ======================= UPDATE THE GUI =======================
                image = QImage(emptyframe, emptyframe.shape[1],emptyframe.shape[0], emptyframe.strides[0],QImage.Format.Format_RGB888)
                image2 = QImage(emptyframe2, emptyframe2.shape[1],emptyframe2.shape[0], emptyframe2.strides[0],QImage.Format.Format_RGB888)
                self.inputframe_1.setPixmap(QPixmap.fromImage(image))
                self.inputframe_3.setPixmap(QPixmap.fromImage(image2))
                # =========================== \\--// ===========================
                processedimage = FrameProcessor.ImageProcessor(self.filename, frame)
                if not processedimage[0]:
                    self.show_warning(processedimage[1])
                else:
                    # ===================== CENTER THE IMAGE =====================
                    emptyframep = np.full((self.outputframe_1.height(), self.outputframe_1.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframep[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = processedimage[1]                        # Paste the resized image onto the empty frame
                    emptyframep2 = np.full((self.outputframe_3.height(), self.outputframe_3.width(), 3), (255, 255, 255), dtype=np.uint8) # Create an empty frame with the frame dimensions
                    emptyframep2[y_offset2:y_offset2+frame2.shape[0], x_offset2:x_offset2+frame2.shape[1]] = processedimage[1]                        # Paste the resized image onto the empty frame
                    # Paste the resized image onto the empty frame
                    # ======================== UPDATE THE GUI ========================
                    imagep = QImage(emptyframep, emptyframep.shape[1],emptyframep.shape[0], emptyframep.strides[0],QImage.Format.Format_RGB888)
                    imagep2 = QImage(emptyframep2, emptyframep2.shape[1],emptyframep2.shape[0], emptyframep2.strides[0],QImage.Format.Format_RGB888)
                    self.outputframe_1.setPixmap(QPixmap.fromImage(imagep))
                    self.outputframe_3.setPixmap(QPixmap.fromImage(imagep2))
                    # ============================ \\--// ============================
     
    # ======= VIDEO PROCESSING THREAD START AND CLOSE CODE =======  
    def closeEvent(self, event: QCloseEvent):
        self.thread_stop_flag = True
        super().closeEvent(event)
    def video_processing_thread(self, filename):
        self.set_video(filename)
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
            self.start_BT.setText("PARAR")
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
            processor_result = FrameProcessor.VideoProcessor(video, processoriginalquality)
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
        self.start_BT.setText("INICIAR")
        self.videoplaying = False
        
    def start(self):
        if self.videoplaying:
            self.thread_stop_flag = True #STOP VIDEO PLAYBACK / CAMERA PLAYBACK
        else:
            #Camera Test
            # Try to access the default camera (usually the built-in webcam)
            camera = cv2.VideoCapture(0)  # 0 represents the default camera
            # Check if the camera was opened successfully
            if camera.isOpened():
                code_v1.initialize_camera()
            # Release the camera when you're done
            camera.release()
            
        
    def small_vw(self):
        self.stackedWidget.setCurrentIndex(0)
        self.resize(771, 584)
    def big_vw(self):
        self.stackedWidget.setCurrentIndex(1)
        self.resize(771, 584)
    def save_file(self):
        return  #não implementado
    def logs_save(self):    
        return  #não implementado
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
    
    def help_open(self):    
        return #não implementado
    
    def update_config(self):

        config.set('DETECTION_CONFIG', 'threashold1_value', str(self.threashold1_SLIDER.value()))
        config.set('DETECTION_CONFIG', 'threashold2_value', str(self.threashold2_SLIDER.value()))
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
        msg_box.setWindowIcon(QIcon('apple.ico'))
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setIcon(icon)  # Use QMessageBox.Icon.Warning for a warning icon
        msg_box.exec()

# =========================== \\---// ===========================

 # Save the changes
with open('config.ini', 'w') as config_file:
    config.write(config_file)

# ========== CONSTRUCTOR ==========   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec())
# ============= \\-// =============