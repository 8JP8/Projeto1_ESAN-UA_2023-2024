# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QLCDNumber, QLabel, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QStackedWidget, QTabWidget,
    QTextBrowser, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(771, 586)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(771, 366))
        MainWindow.setMaximumSize(QSize(771, 586))
        font = QFont()
        font.setStyleStrategy(QFont.PreferDefault)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"icons/apple.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionOpen_Upload = QAction(MainWindow)
        self.actionOpen_Upload.setObjectName(u"actionOpen_Upload")
        icon1 = QIcon()
        icon1.addFile(u"icons/62917openfilefolder_109270.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_Upload.setIcon(icon1)
        self.actionSave_Output_File = QAction(MainWindow)
        self.actionSave_Output_File.setObjectName(u"actionSave_Output_File")
        icon2 = QIcon()
        icon2.addFile(u"icons/ic_save_128_28731.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave_Output_File.setIcon(icon2)
        self.action_small_view = QAction(MainWindow)
        self.action_small_view.setObjectName(u"action_small_view")
        icon3 = QIcon()
        icon3.addFile(u"icons/zoomout_zoom_search_find_1530.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_small_view.setIcon(icon3)
        self.action_big_view = QAction(MainWindow)
        self.action_big_view.setObjectName(u"action_big_view")
        icon4 = QIcon()
        icon4.addFile(u"icons/zoomin_zoom_search_find_1531.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_big_view.setIcon(icon4)
        self.action_restartprogram = QAction(MainWindow)
        self.action_restartprogram.setObjectName(u"action_restartprogram")
        icon5 = QIcon()
        icon5.addFile(u"icons/79699_panel_restart_system_icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_restartprogram.setIcon(icon5)
        self.action_logs_open = QAction(MainWindow)
        self.action_logs_open.setObjectName(u"action_logs_open")
        icon6 = QIcon()
        icon6.addFile(u"icons/documentediting_editdocuments_text_documentedi_2820.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_logs_open.setIcon(icon6)
        self.action_logs_export = QAction(MainWindow)
        self.action_logs_export.setObjectName(u"action_logs_export")
        icon7 = QIcon()
        icon7.addFile(u"icons/File_Explorer_23583.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_logs_export.setIcon(icon7)
        self.actionSave_Frame = QAction(MainWindow)
        self.actionSave_Frame.setObjectName(u"actionSave_Frame")
        icon8 = QIcon()
        icon8.addFile(u"icons/icons8-picture-96.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave_Frame.setIcon(icon8)
        self.action_calibratecamera = QAction(MainWindow)
        self.action_calibratecamera.setObjectName(u"action_calibratecamera")
        icon9 = QIcon()
        icon9.addFile(u"icons/webcam.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_calibratecamera.setIcon(icon9)
        self.action_settings_open = QAction(MainWindow)
        self.action_settings_open.setObjectName(u"action_settings_open")
        icon10 = QIcon()
        icon10.addFile(u"icons/Settings-icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.action_settings_open.setIcon(icon10)
        self.action_operatorview = QAction(MainWindow)
        self.action_operatorview.setObjectName(u"action_operatorview")
        icon11 = QIcon()
        icon11.addFile(u"icons/online-service.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_operatorview.setIcon(icon11)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.settingsgroup = QGroupBox(self.centralwidget)
        self.settingsgroup.setObjectName(u"settingsgroup")
        self.settingsgroup.setGeometry(QRect(10, 10, 641, 90))
        self.settingsgroup.setLocale(QLocale(QLocale.Portuguese, QLocale.Portugal))
        self.cam1_RADIOBT = QRadioButton(self.settingsgroup)
        self.cam1_RADIOBT.setObjectName(u"cam1_RADIOBT")
        self.cam1_RADIOBT.setGeometry(QRect(555, 35, 71, 21))
        self.cam1_RADIOBT.setChecked(True)
        self.cam2_RADIOBT = QRadioButton(self.settingsgroup)
        self.cam2_RADIOBT.setObjectName(u"cam2_RADIOBT")
        self.cam2_RADIOBT.setEnabled(True)
        self.cam2_RADIOBT.setGeometry(QRect(555, 57, 81, 21))
        self.mode_COMBOBOX = QComboBox(self.settingsgroup)
        self.mode_COMBOBOX.addItem("")
        self.mode_COMBOBOX.setObjectName(u"mode_COMBOBOX")
        self.mode_COMBOBOX.setGeometry(QRect(10, 50, 81, 24))
        self.threshold1_SLIDER = QSlider(self.settingsgroup)
        self.threshold1_SLIDER.setObjectName(u"threshold1_SLIDER")
        self.threshold1_SLIDER.setGeometry(QRect(379, 33, 151, 21))
        self.threshold1_SLIDER.setMaximum(100)
        self.threshold1_SLIDER.setValue(30)
        self.threshold1_SLIDER.setOrientation(Qt.Horizontal)
        self.threshold1_SLIDER.setInvertedAppearance(False)
        self.threshold1_SLIDER.setInvertedControls(False)
        self.threshold1_SLIDER.setTickPosition(QSlider.TicksBothSides)
        self.threshold1_SLIDER.setTickInterval(10)
        self.threshold2_SLIDER = QSlider(self.settingsgroup)
        self.threshold2_SLIDER.setObjectName(u"threshold2_SLIDER")
        self.threshold2_SLIDER.setGeometry(QRect(379, 60, 151, 21))
        self.threshold2_SLIDER.setMouseTracking(False)
        self.threshold2_SLIDER.setFocusPolicy(Qt.StrongFocus)
        self.threshold2_SLIDER.setAcceptDrops(False)
        self.threshold2_SLIDER.setAutoFillBackground(False)
        self.threshold2_SLIDER.setMaximum(100)
        self.threshold2_SLIDER.setValue(30)
        self.threshold2_SLIDER.setSliderPosition(30)
        self.threshold2_SLIDER.setTracking(True)
        self.threshold2_SLIDER.setOrientation(Qt.Horizontal)
        self.threshold2_SLIDER.setTickPosition(QSlider.TicksBothSides)
        self.threshold2_SLIDER.setTickInterval(10)
        self.thlb1 = QLabel(self.settingsgroup)
        self.thlb1.setObjectName(u"thlb1")
        self.thlb1.setGeometry(QRect(330, 33, 41, 16))
        self.thlb1.setLayoutDirection(Qt.LeftToRight)
        self.thlb2 = QLabel(self.settingsgroup)
        self.thlb2.setObjectName(u"thlb2")
        self.thlb2.setGeometry(QRect(330, 60, 41, 16))
        self.detectionmode_COMBOBOX = QComboBox(self.settingsgroup)
        self.detectionmode_COMBOBOX.addItem("")
        self.detectionmode_COMBOBOX.addItem("")
        self.detectionmode_COMBOBOX.addItem("")
        self.detectionmode_COMBOBOX.setObjectName(u"detectionmode_COMBOBOX")
        self.detectionmode_COMBOBOX.setGeometry(QRect(100, 50, 81, 24))
        self.modoslb = QLabel(self.settingsgroup)
        self.modoslb.setObjectName(u"modoslb")
        self.modoslb.setGeometry(QRect(10, 30, 49, 16))
        self.modoslb_2 = QLabel(self.settingsgroup)
        self.modoslb_2.setObjectName(u"modoslb_2")
        self.modoslb_2.setGeometry(QRect(100, 30, 51, 16))
        self.modoslb_3 = QLabel(self.settingsgroup)
        self.modoslb_3.setObjectName(u"modoslb_3")
        self.modoslb_3.setGeometry(QRect(190, 30, 91, 16))
        self.categorizationmode_COMBOBOX = QComboBox(self.settingsgroup)
        self.categorizationmode_COMBOBOX.addItem("")
        self.categorizationmode_COMBOBOX.addItem("")
        self.categorizationmode_COMBOBOX.setObjectName(u"categorizationmode_COMBOBOX")
        self.categorizationmode_COMBOBOX.setGeometry(QRect(190, 50, 121, 24))
        self.colorfilters_BT = QPushButton(self.settingsgroup)
        self.colorfilters_BT.setObjectName(u"colorfilters_BT")
        self.colorfilters_BT.setGeometry(QRect(541, 7, 101, 23))
        icon12 = QIcon()
        icon12.addFile(u"icons/colour.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.colorfilters_BT.setIcon(icon12)
        self.upload_BT = QPushButton(self.centralwidget)
        self.upload_BT.setObjectName(u"upload_BT")
        self.upload_BT.setGeometry(QRect(660, 16, 101, 24))
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 110, 753, 455))
        self.stackedWidget.setLayoutDirection(Qt.LeftToRight)
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet(u"")
        self.small_view = QWidget()
        self.small_view.setObjectName(u"small_view")
        self.input_groupbox = QGroupBox(self.small_view)
        self.input_groupbox.setObjectName(u"input_groupbox")
        self.input_groupbox.setGeometry(QRect(0, -3, 368, 448))
        self.inputframe_1 = QLabel(self.input_groupbox)
        self.inputframe_1.setObjectName(u"inputframe_1")
        self.inputframe_1.setGeometry(QRect(0, 20, 368, 207))
        self.inputframe_1.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.inputframe_2 = QLabel(self.input_groupbox)
        self.inputframe_2.setObjectName(u"inputframe_2")
        self.inputframe_2.setGeometry(QRect(0, 240, 368, 207))
        self.inputframe_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.output_groupbox = QGroupBox(self.small_view)
        self.output_groupbox.setObjectName(u"output_groupbox")
        self.output_groupbox.setGeometry(QRect(383, -3, 368, 448))
        self.outputframe_1 = QLabel(self.output_groupbox)
        self.outputframe_1.setObjectName(u"outputframe_1")
        self.outputframe_1.setGeometry(QRect(0, 20, 368, 207))
        self.outputframe_1.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.outputframe_2 = QLabel(self.output_groupbox)
        self.outputframe_2.setObjectName(u"outputframe_2")
        self.outputframe_2.setGeometry(QRect(0, 240, 368, 207))
        self.outputframe_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.stackedWidget.addWidget(self.small_view)
        self.output_groupbox.raise_()
        self.input_groupbox.raise_()
        self.big_view = QWidget()
        self.big_view.setObjectName(u"big_view")
        self.big_view_tabwidget = QTabWidget(self.big_view)
        self.big_view_tabwidget.setObjectName(u"big_view_tabwidget")
        self.big_view_tabwidget.setGeometry(QRect(0, -1, 752, 444))
        self.big_view_tabwidget.setStyleSheet(u"border-right-color: rgba(255, 255, 255, 0);\n"
"border-bottom-color: rgba(255, 255, 255, 0);")
        self.input1_tab = QWidget()
        self.input1_tab.setObjectName(u"input1_tab")
        self.inputframe_3 = QLabel(self.input1_tab)
        self.inputframe_3.setObjectName(u"inputframe_3")
        self.inputframe_3.setGeometry(QRect(-1, -1, 752, 423))
        self.inputframe_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.big_view_tabwidget.addTab(self.input1_tab, "")
        self.output1_tab = QWidget()
        self.output1_tab.setObjectName(u"output1_tab")
        self.outputframe_3 = QLabel(self.output1_tab)
        self.outputframe_3.setObjectName(u"outputframe_3")
        self.outputframe_3.setGeometry(QRect(-1, -1, 752, 423))
        self.outputframe_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.big_view_tabwidget.addTab(self.output1_tab, "")
        self.input2_tab = QWidget()
        self.input2_tab.setObjectName(u"input2_tab")
        self.inputframe_4 = QLabel(self.input2_tab)
        self.inputframe_4.setObjectName(u"inputframe_4")
        self.inputframe_4.setGeometry(QRect(-1, -1, 752, 423))
        self.inputframe_4.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.big_view_tabwidget.addTab(self.input2_tab, "")
        self.output2_tab = QWidget()
        self.output2_tab.setObjectName(u"output2_tab")
        self.outputframe_4 = QLabel(self.output2_tab)
        self.outputframe_4.setObjectName(u"outputframe_4")
        self.outputframe_4.setGeometry(QRect(-1, -1, 752, 423))
        self.outputframe_4.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.big_view_tabwidget.addTab(self.output2_tab, "")
        self.stackedWidget.addWidget(self.big_view)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.counts_groupbox = QGroupBox(self.page)
        self.counts_groupbox.setObjectName(u"counts_groupbox")
        self.counts_groupbox.setGeometry(QRect(0, -3, 231, 111))
        self.Slot_LCD = QLCDNumber(self.counts_groupbox)
        self.Slot_LCD.setObjectName(u"Slot_LCD")
        self.Slot_LCD.setGeometry(QRect(100, 20, 111, 41))
        self.Slot_LCD.setFrameShape(QFrame.NoFrame)
        self.Slot_Label = QLabel(self.counts_groupbox)
        self.Slot_Label.setObjectName(u"Slot_Label")
        self.Slot_Label.setGeometry(QRect(10, 20, 211, 41))
        font1 = QFont()
        font1.setPointSize(8)
        self.Slot_Label.setFont(font1)
        self.Slot_Label.setFrameShape(QFrame.Box)
        self.DetectedApples_Label = QLabel(self.counts_groupbox)
        self.DetectedApples_Label.setObjectName(u"DetectedApples_Label")
        self.DetectedApples_Label.setGeometry(QRect(10, 60, 211, 41))
        self.DetectedApples_Label.setFont(font1)
        self.DetectedApples_Label.setFrameShape(QFrame.Box)
        self.DetectedApples_LCD = QLCDNumber(self.counts_groupbox)
        self.DetectedApples_LCD.setObjectName(u"DetectedApples_LCD")
        self.DetectedApples_LCD.setGeometry(QRect(100, 60, 111, 41))
        self.DetectedApples_LCD.setFrameShape(QFrame.NoFrame)
        self.Slot_Label.raise_()
        self.DetectedApples_Label.raise_()
        self.DetectedApples_LCD.raise_()
        self.Slot_LCD.raise_()
        self.categories_groupbox = QGroupBox(self.page)
        self.categories_groupbox.setObjectName(u"categories_groupbox")
        self.categories_groupbox.setGeometry(QRect(0, 117, 231, 151))
        self.BigApples_LCD = QLCDNumber(self.categories_groupbox)
        self.BigApples_LCD.setObjectName(u"BigApples_LCD")
        self.BigApples_LCD.setGeometry(QRect(100, 20, 111, 41))
        self.BigApples_LCD.setFrameShape(QFrame.NoFrame)
        self.BigApples_Label = QLabel(self.categories_groupbox)
        self.BigApples_Label.setObjectName(u"BigApples_Label")
        self.BigApples_Label.setGeometry(QRect(10, 20, 211, 41))
        self.BigApples_Label.setFont(font1)
        self.BigApples_Label.setFrameShape(QFrame.Box)
        self.SmallApples_LCD_2 = QLabel(self.categories_groupbox)
        self.SmallApples_LCD_2.setObjectName(u"SmallApples_LCD_2")
        self.SmallApples_LCD_2.setGeometry(QRect(10, 60, 211, 41))
        self.SmallApples_LCD_2.setFont(font1)
        self.SmallApples_LCD_2.setFrameShape(QFrame.Box)
        self.SmallApples_LCD = QLCDNumber(self.categories_groupbox)
        self.SmallApples_LCD.setObjectName(u"SmallApples_LCD")
        self.SmallApples_LCD.setGeometry(QRect(100, 60, 111, 41))
        self.SmallApples_LCD.setStyleSheet(u"")
        self.SmallApples_LCD.setFrameShape(QFrame.NoFrame)
        self.BadApples_Label = QLabel(self.categories_groupbox)
        self.BadApples_Label.setObjectName(u"BadApples_Label")
        self.BadApples_Label.setGeometry(QRect(10, 100, 211, 41))
        self.BadApples_Label.setFont(font1)
        self.BadApples_Label.setFrameShape(QFrame.Box)
        self.BadApples_LCD = QLCDNumber(self.categories_groupbox)
        self.BadApples_LCD.setObjectName(u"BadApples_LCD")
        self.BadApples_LCD.setGeometry(QRect(100, 100, 111, 41))
        self.BadApples_LCD.setStyleSheet(u"")
        self.BadApples_LCD.setFrameShape(QFrame.NoFrame)
        self.BigApples_Label.raise_()
        self.SmallApples_LCD_2.raise_()
        self.SmallApples_LCD.raise_()
        self.BadApples_Label.raise_()
        self.BadApples_LCD.raise_()
        self.BigApples_LCD.raise_()
        self.detectionoutputs_groupbox = QGroupBox(self.page)
        self.detectionoutputs_groupbox.setObjectName(u"detectionoutputs_groupbox")
        self.detectionoutputs_groupbox.setGeometry(QRect(383, -3, 368, 447))
        self.outputframe_5 = QLabel(self.detectionoutputs_groupbox)
        self.outputframe_5.setObjectName(u"outputframe_5")
        self.outputframe_5.setGeometry(QRect(0, 20, 368, 207))
        self.outputframe_5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.outputframe_6 = QLabel(self.detectionoutputs_groupbox)
        self.outputframe_6.setObjectName(u"outputframe_6")
        self.outputframe_6.setGeometry(QRect(0, 239, 368, 207))
        self.outputframe_6.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid grey;")
        self.control_groupbox = QGroupBox(self.page)
        self.control_groupbox.setObjectName(u"control_groupbox")
        self.control_groupbox.setGeometry(QRect(240, -3, 134, 111))
        self.reset_BT = QPushButton(self.control_groupbox)
        self.reset_BT.setObjectName(u"reset_BT")
        self.reset_BT.setGeometry(QRect(10, 20, 114, 81))
        self.reset_BT.setStyleSheet(u"")
        self.log_groupbox = QGroupBox(self.page)
        self.log_groupbox.setObjectName(u"log_groupbox")
        self.log_groupbox.setGeometry(QRect(0, 278, 374, 166))
        self.Log_textBrowser = QTextBrowser(self.log_groupbox)
        self.Log_textBrowser.setObjectName(u"Log_textBrowser")
        self.Log_textBrowser.setGeometry(QRect(0, 20, 374, 146))
        self.Log_textBrowser.setFrameShape(QFrame.Box)
        self.Log_textBrowser.setFrameShadow(QFrame.Sunken)
        self.statistics_groupbox = QGroupBox(self.page)
        self.statistics_groupbox.setObjectName(u"statistics_groupbox")
        self.statistics_groupbox.setGeometry(QRect(240, 117, 134, 151))
        self.AverageDiameter_TextEdit = QTextEdit(self.statistics_groupbox)
        self.AverageDiameter_TextEdit.setObjectName(u"AverageDiameter_TextEdit")
        self.AverageDiameter_TextEdit.setGeometry(QRect(10, 45, 114, 31))
        self.AverageDiameter_TextEdit.setLayoutDirection(Qt.LeftToRight)
        self.AverageDiameter_TextEdit.setInputMethodHints(Qt.ImhMultiLine)
        self.AverageDiameter_TextEdit.setFrameShape(QFrame.Box)
        self.AverageDiameter_TextEdit.setFrameShadow(QFrame.Plain)
        self.AverageDiameter_TextEdit.setReadOnly(True)
        self.AverageDiameter_Label = QLabel(self.statistics_groupbox)
        self.AverageDiameter_Label.setObjectName(u"AverageDiameter_Label")
        self.AverageDiameter_Label.setGeometry(QRect(10, 20, 111, 20))
        self.AverageDiameter_Label.setAlignment(Qt.AlignCenter)
        self.FalsePositives_TextEdit = QTextEdit(self.statistics_groupbox)
        self.FalsePositives_TextEdit.setObjectName(u"FalsePositives_TextEdit")
        self.FalsePositives_TextEdit.setGeometry(QRect(10, 110, 114, 31))
        self.FalsePositives_TextEdit.setLayoutDirection(Qt.LeftToRight)
        self.FalsePositives_TextEdit.setFrameShape(QFrame.Box)
        self.FalsePositives_TextEdit.setFrameShadow(QFrame.Plain)
        self.FalsePositives_TextEdit.setReadOnly(True)
        self.FalsePositives_TextEdit.setOverwriteMode(False)
        self.FalsePositives_TextEdit.setAcceptRichText(True)
        self.FalsePositives_Label = QLabel(self.statistics_groupbox)
        self.FalsePositives_Label.setObjectName(u"FalsePositives_Label")
        self.FalsePositives_Label.setGeometry(QRect(10, 85, 111, 20))
        self.FalsePositives_Label.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.page)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(-1, 0, 773, 5))
        self.progressBar.setStyleSheet(u"")
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        self.progressBar.setTextVisible(False)
        self.nextframe_BT = QPushButton(self.centralwidget)
        self.nextframe_BT.setObjectName(u"nextframe_BT")
        self.nextframe_BT.setGeometry(QRect(660, 47, 101, 24))
        self.start_BT = QPushButton(self.centralwidget)
        self.start_BT.setObjectName(u"start_BT")
        self.start_BT.setGeometry(QRect(660, 47, 101, 54))
        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.raise_()
        self.settingsgroup.raise_()
        self.upload_BT.raise_()
        self.progressBar.raise_()
        self.nextframe_BT.raise_()
        self.start_BT.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 771, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menu_logs = QMenu(self.menuTools)
        self.menu_logs.setObjectName(u"menu_logs")
        self.menu_logs.setIcon(icon6)
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName(u"menuInfo")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        self.menuFile.addAction(self.actionOpen_Upload)
        self.menuFile.addAction(self.actionSave_Output_File)
        self.menuFile.addAction(self.actionSave_Frame)
        self.menuTools.addAction(self.menu_logs.menuAction())
        self.menuTools.addAction(self.action_settings_open)
        self.menuTools.addAction(self.action_calibratecamera)
        self.menuTools.addAction(self.action_restartprogram)
        self.menu_logs.addSeparator()
        self.menu_logs.addAction(self.action_logs_open)
        self.menu_logs.addAction(self.action_logs_export)
        self.menuView.addAction(self.action_small_view)
        self.menuView.addAction(self.action_big_view)
        self.menuView.addAction(self.action_operatorview)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)
        self.big_view_tabwidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Categoriza\u00e7\u00e3o de Ma\u00e7\u00e3s", None))
        self.actionOpen_Upload.setText(QCoreApplication.translate("MainWindow", u"Abrir Arquivo (Ctrl+A)", None))
        self.actionSave_Output_File.setText(QCoreApplication.translate("MainWindow", u"Guardar Arquivo (Ctrl+G)", None))
        self.action_small_view.setText(QCoreApplication.translate("MainWindow", u"Vista Pequena (Ctrl+Esquerda)", None))
        self.action_big_view.setText(QCoreApplication.translate("MainWindow", u"Vista Grande (Ctrl+Direita)", None))
        self.action_restartprogram.setText(QCoreApplication.translate("MainWindow", u"Reiniciar App (Ctrl+Shift+R)", None))
        self.action_logs_open.setText(QCoreApplication.translate("MainWindow", u"Abrir Ficheiro de Logs (Ctrl+L)", None))
        self.action_logs_export.setText(QCoreApplication.translate("MainWindow", u"Exportar Logs (Ctrl+Shift+L)", None))
        self.actionSave_Frame.setText(QCoreApplication.translate("MainWindow", u"Guardar Frame (Ctrl+F)", None))
        self.action_calibratecamera.setText(QCoreApplication.translate("MainWindow", u"Calibrar C\u00e2mara (Ctrl+Shift+C)", None))
        self.action_settings_open.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o (Ctrl+D)", None))
        self.action_settings_open.setIconText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o", None))
        self.action_operatorview.setText(QCoreApplication.translate("MainWindow", u"Vista de Operador (Ctrl+End)", None))
        self.settingsgroup.setTitle(QCoreApplication.translate("MainWindow", u"Defini\u00e7\u00f5es", None))
        self.cam1_RADIOBT.setText(QCoreApplication.translate("MainWindow", u"1 C\u00e2mara", None))
        self.cam2_RADIOBT.setText(QCoreApplication.translate("MainWindow", u"2 C\u00e2maras", None))
        self.mode_COMBOBOX.setItemText(0, QCoreApplication.translate("MainWindow", u"OpenCV", None))

        self.mode_COMBOBOX.setCurrentText(QCoreApplication.translate("MainWindow", u"OpenCV", None))
        self.mode_COMBOBOX.setProperty("placeholderText", QCoreApplication.translate("MainWindow", u"OpenCV", None))
        self.thlb1.setText(QCoreApplication.translate("MainWindow", u"Limite 1", None))
        self.thlb2.setText(QCoreApplication.translate("MainWindow", u"Limite 2", None))
        self.detectionmode_COMBOBOX.setItemText(0, QCoreApplication.translate("MainWindow", u"YOLO_V4", None))
        self.detectionmode_COMBOBOX.setItemText(1, QCoreApplication.translate("MainWindow", u"YOLO_V4 TINY", None))
        self.detectionmode_COMBOBOX.setItemText(2, QCoreApplication.translate("MainWindow", u"Custom", None))

        self.detectionmode_COMBOBOX.setCurrentText(QCoreApplication.translate("MainWindow", u"YOLO_V4", None))
        self.detectionmode_COMBOBOX.setProperty("placeholderText", QCoreApplication.translate("MainWindow", u"YOLO_V4", None))
        self.modoslb.setText(QCoreApplication.translate("MainWindow", u"Modo:", None))
        self.modoslb_2.setText(QCoreApplication.translate("MainWindow", u"Dete\u00e7\u00e3o:", None))
        self.modoslb_3.setText(QCoreApplication.translate("MainWindow", u"Categoriza\u00e7\u00e3o:", None))
        self.categorizationmode_COMBOBOX.setItemText(0, QCoreApplication.translate("MainWindow", u"Tensorflow - Keras", None))
        self.categorizationmode_COMBOBOX.setItemText(1, QCoreApplication.translate("MainWindow", u"Custom", None))

        self.categorizationmode_COMBOBOX.setCurrentText(QCoreApplication.translate("MainWindow", u"Tensorflow - Keras", None))
        self.categorizationmode_COMBOBOX.setProperty("placeholderText", QCoreApplication.translate("MainWindow", u"Tensorflow-Keras", None))
        self.colorfilters_BT.setText(QCoreApplication.translate("MainWindow", u" FILTROS (F)", None))
#if QT_CONFIG(shortcut)
        self.colorfilters_BT.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.upload_BT.setText(QCoreApplication.translate("MainWindow", u"ABRIR (A)", None))
        self.input_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Input", None))
        self.inputframe_1.setText("")
        self.inputframe_2.setText("")
        self.output_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
        self.outputframe_1.setText("")
        self.outputframe_2.setText("")
        self.inputframe_3.setText("")
        self.big_view_tabwidget.setTabText(self.big_view_tabwidget.indexOf(self.input1_tab), QCoreApplication.translate("MainWindow", u"Input1", None))
        self.outputframe_3.setText("")
        self.big_view_tabwidget.setTabText(self.big_view_tabwidget.indexOf(self.output1_tab), QCoreApplication.translate("MainWindow", u"Ouput1", None))
        self.inputframe_4.setText("")
        self.big_view_tabwidget.setTabText(self.big_view_tabwidget.indexOf(self.input2_tab), QCoreApplication.translate("MainWindow", u"Input2", None))
        self.outputframe_4.setText("")
        self.big_view_tabwidget.setTabText(self.big_view_tabwidget.indexOf(self.output2_tab), QCoreApplication.translate("MainWindow", u"Output2", None))
        self.counts_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Contagem", None))
        self.Slot_Label.setText(QCoreApplication.translate("MainWindow", u"Slot do Tapete:", None))
        self.DetectedApples_Label.setText(QCoreApplication.translate("MainWindow", u"Ma\u00e7\u00e3s Detetadas:", None))
        self.categories_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Categorias Detetadas", None))
        self.BigApples_Label.setText(QCoreApplication.translate("MainWindow", u"Ma\u00e7\u00e3s Grandes:", None))
        self.SmallApples_LCD_2.setText(QCoreApplication.translate("MainWindow", u"Ma\u00e7\u00e3s Pequenas:", None))
        self.BadApples_Label.setText(QCoreApplication.translate("MainWindow", u"Ma\u00e7\u00e3s Defeituosas:", None))
        self.detectionoutputs_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Output de Dete\u00e7\u00e3o", None))
        self.outputframe_5.setText("")
        self.outputframe_6.setText("")
        self.control_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Controlo", None))
        self.reset_BT.setText(QCoreApplication.translate("MainWindow", u"REINICIAR\n"
"(Ctrl+R)", None))
        self.log_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.statistics_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Estat\u00edsticas", None))
        self.AverageDiameter_TextEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.AverageDiameter_Label.setText(QCoreApplication.translate("MainWindow", u"Di\u00e2metro M\u00e9dio:", None))
        self.FalsePositives_TextEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.FalsePositives_Label.setText(QCoreApplication.translate("MainWindow", u"Falsos Positivos", None))
        self.nextframe_BT.setText(QCoreApplication.translate("MainWindow", u"CONGELAR (C)", None))
        self.start_BT.setText(QCoreApplication.translate("MainWindow", u"INICIAR (I)", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Ficheiro", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Ferramentas", None))
        self.menu_logs.setTitle(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.menuInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"Ver", None))
    # retranslateUi

