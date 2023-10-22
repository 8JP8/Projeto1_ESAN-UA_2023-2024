from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.QtGui import QIcon
from modules import code_v1
import cv2
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

currentvideopath = ""

def ImageProcessor(img_filepath, frame):

    # Process each image in the test_images folder
    if os.path.isfile(img_filepath):
        try:
            frame = code_v1.detect_and_classify_apples(frame, "image")
            return (True, frame)
        except:
            return(False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(img_filepath)}'.")
    else:
        return(False, f"Erro: Imagem '{os.path.basename(img_filepath)}' não encontrada.")
        

def VideoProcessor(vd_filepath, frame):
    if (currentvideopath == "") or (currentvideopath != vd_filepath):
        if os.path.isfile(vd_filepath):
            cap = cv2.VideoCapture(vd_filepath)
            if not cap.isOpened():
                return (False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(vd_filepath)}'.")
            else:
                newframe = code_v1.detect_and_classify_apples(frame, "video")
                return (True, newframe)
        else:
            return (False, f"Erro: Vídeo '{os.path.basename(vd_filepath)}' não encontrado.")
    else:
        try:
            newframe = code_v1.detect_and_classify_apples(frame, "video")
            return (True, newframe)
        except:
            return(False, f"Erro: Não foi possível abrir o ficheiro '{os.path.basename(vd_filepath)}'.")
        
def CameraProcessor(self, inputframe):
    # Detect and classify apples and update the frame
    try:
        frame = code_v1.detect_and_classify_apples(inputframe, "camera")
    except:
        return(False, f"Erro: O processamento de frames falhou.")
    return (True, frame)