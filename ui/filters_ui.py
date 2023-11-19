# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filters.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(414, 720)
        Form.setMinimumSize(QSize(280, 0))
        icon = QIcon()
        icon.addFile(u"icons/colour.ico", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.title_lb = QLabel(Form)
        self.title_lb.setObjectName(u"title_lb")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.title_lb.sizePolicy().hasHeightForWidth())
        self.title_lb.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        self.title_lb.setFont(font)
        self.title_lb.setLayoutDirection(Qt.LeftToRight)
        self.title_lb.setStyleSheet(u"font: 12pt \"MS Shell Dlg 2\";")
        self.title_lb.setTextFormat(Qt.AutoText)
        self.title_lb.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_lb)

        self.verticalSpacer_2 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.minhue_lb = QLabel(Form)
        self.minhue_lb.setObjectName(u"minhue_lb")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.minhue_lb.sizePolicy().hasHeightForWidth())
        self.minhue_lb.setSizePolicy(sizePolicy1)
        self.minhue_lb.setMinimumSize(QSize(82, 0))
        self.minhue_lb.setScaledContents(False)
        self.minhue_lb.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.minhue_lb)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.minhue_slider = QSlider(Form)
        self.minhue_slider.setObjectName(u"minhue_slider")
        self.minhue_slider.setMaximum(179)
        self.minhue_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.minhue_slider)

        self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_12)

        self.minhue_spinbox = QSpinBox(Form)
        self.minhue_spinbox.setObjectName(u"minhue_spinbox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.minhue_spinbox.sizePolicy().hasHeightForWidth())
        self.minhue_spinbox.setSizePolicy(sizePolicy2)
        self.minhue_spinbox.setMinimumSize(QSize(47, 0))
        self.minhue_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.minhue_spinbox.setMinimum(0)
        self.minhue_spinbox.setMaximum(179)
        self.minhue_spinbox.setValue(0)

        self.horizontalLayout.addWidget(self.minhue_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.maxhue_lb = QLabel(Form)
        self.maxhue_lb.setObjectName(u"maxhue_lb")
        sizePolicy1.setHeightForWidth(self.maxhue_lb.sizePolicy().hasHeightForWidth())
        self.maxhue_lb.setSizePolicy(sizePolicy1)
        self.maxhue_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_4.addWidget(self.maxhue_lb)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.maxhue_slider = QSlider(Form)
        self.maxhue_slider.setObjectName(u"maxhue_slider")
        self.maxhue_slider.setMaximum(179)
        self.maxhue_slider.setValue(179)
        self.maxhue_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.maxhue_slider)

        self.horizontalSpacer_9 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.maxhue_spinbox = QSpinBox(Form)
        self.maxhue_spinbox.setObjectName(u"maxhue_spinbox")
        sizePolicy2.setHeightForWidth(self.maxhue_spinbox.sizePolicy().hasHeightForWidth())
        self.maxhue_spinbox.setSizePolicy(sizePolicy2)
        self.maxhue_spinbox.setMinimumSize(QSize(47, 0))
        self.maxhue_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.maxhue_spinbox.setMinimum(0)
        self.maxhue_spinbox.setMaximum(179)
        self.maxhue_spinbox.setValue(179)

        self.horizontalLayout_4.addWidget(self.maxhue_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.minsat_lb = QLabel(Form)
        self.minsat_lb.setObjectName(u"minsat_lb")
        sizePolicy1.setHeightForWidth(self.minsat_lb.sizePolicy().hasHeightForWidth())
        self.minsat_lb.setSizePolicy(sizePolicy1)
        self.minsat_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_2.addWidget(self.minsat_lb)

        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.minsat_slider = QSlider(Form)
        self.minsat_slider.setObjectName(u"minsat_slider")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.minsat_slider.sizePolicy().hasHeightForWidth())
        self.minsat_slider.setSizePolicy(sizePolicy3)
        self.minsat_slider.setMaximum(255)
        self.minsat_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.minsat_slider)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_11)

        self.minsat_spinbox = QSpinBox(Form)
        self.minsat_spinbox.setObjectName(u"minsat_spinbox")
        sizePolicy2.setHeightForWidth(self.minsat_spinbox.sizePolicy().hasHeightForWidth())
        self.minsat_spinbox.setSizePolicy(sizePolicy2)
        self.minsat_spinbox.setMinimumSize(QSize(47, 0))
        self.minsat_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.minsat_spinbox.setMinimum(0)
        self.minsat_spinbox.setMaximum(255)

        self.horizontalLayout_2.addWidget(self.minsat_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.maxsat_lb = QLabel(Form)
        self.maxsat_lb.setObjectName(u"maxsat_lb")
        sizePolicy1.setHeightForWidth(self.maxsat_lb.sizePolicy().hasHeightForWidth())
        self.maxsat_lb.setSizePolicy(sizePolicy1)
        self.maxsat_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_5.addWidget(self.maxsat_lb)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.maxsat_slider = QSlider(Form)
        self.maxsat_slider.setObjectName(u"maxsat_slider")
        self.maxsat_slider.setMaximum(255)
        self.maxsat_slider.setValue(255)
        self.maxsat_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_5.addWidget(self.maxsat_slider)

        self.horizontalSpacer_8 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_8)

        self.maxsat_spinbox = QSpinBox(Form)
        self.maxsat_spinbox.setObjectName(u"maxsat_spinbox")
        sizePolicy2.setHeightForWidth(self.maxsat_spinbox.sizePolicy().hasHeightForWidth())
        self.maxsat_spinbox.setSizePolicy(sizePolicy2)
        self.maxsat_spinbox.setMinimumSize(QSize(47, 0))
        self.maxsat_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.maxsat_spinbox.setMinimum(0)
        self.maxsat_spinbox.setMaximum(255)
        self.maxsat_spinbox.setValue(255)

        self.horizontalLayout_5.addWidget(self.maxsat_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.minval_lb = QLabel(Form)
        self.minval_lb.setObjectName(u"minval_lb")
        sizePolicy1.setHeightForWidth(self.minval_lb.sizePolicy().hasHeightForWidth())
        self.minval_lb.setSizePolicy(sizePolicy1)
        self.minval_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_3.addWidget(self.minval_lb)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.minval_slider = QSlider(Form)
        self.minval_slider.setObjectName(u"minval_slider")
        self.minval_slider.setMaximum(255)
        self.minval_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.minval_slider)

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_10)

        self.minval_spinbox = QSpinBox(Form)
        self.minval_spinbox.setObjectName(u"minval_spinbox")
        sizePolicy2.setHeightForWidth(self.minval_spinbox.sizePolicy().hasHeightForWidth())
        self.minval_spinbox.setSizePolicy(sizePolicy2)
        self.minval_spinbox.setMinimumSize(QSize(47, 0))
        self.minval_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.minval_spinbox.setMinimum(0)
        self.minval_spinbox.setMaximum(255)

        self.horizontalLayout_3.addWidget(self.minval_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.maxval_lb = QLabel(Form)
        self.maxval_lb.setObjectName(u"maxval_lb")
        self.maxval_lb.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.maxval_lb.sizePolicy().hasHeightForWidth())
        self.maxval_lb.setSizePolicy(sizePolicy1)
        self.maxval_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_6.addWidget(self.maxval_lb)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.maxval_slider = QSlider(Form)
        self.maxval_slider.setObjectName(u"maxval_slider")
        self.maxval_slider.setMaximum(255)
        self.maxval_slider.setValue(255)
        self.maxval_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.maxval_slider)

        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)

        self.maxval_spinbox = QSpinBox(Form)
        self.maxval_spinbox.setObjectName(u"maxval_spinbox")
        sizePolicy2.setHeightForWidth(self.maxval_spinbox.sizePolicy().hasHeightForWidth())
        self.maxval_spinbox.setSizePolicy(sizePolicy2)
        self.maxval_spinbox.setMinimumSize(QSize(47, 0))
        self.maxval_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.maxval_spinbox.setMinimum(0)
        self.maxval_spinbox.setMaximum(255)
        self.maxval_spinbox.setValue(255)

        self.horizontalLayout_6.addWidget(self.maxval_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.hueaddsub_lb = QLabel(Form)
        self.hueaddsub_lb.setObjectName(u"hueaddsub_lb")
        sizePolicy1.setHeightForWidth(self.hueaddsub_lb.sizePolicy().hasHeightForWidth())
        self.hueaddsub_lb.setSizePolicy(sizePolicy1)
        self.hueaddsub_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_10.addWidget(self.hueaddsub_lb)

        self.horizontalSpacer_37 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_37)

        self.hueaddsub_slider = QSlider(Form)
        self.hueaddsub_slider.setObjectName(u"hueaddsub_slider")
        self.hueaddsub_slider.setMinimum(-179)
        self.hueaddsub_slider.setMaximum(179)
        self.hueaddsub_slider.setValue(0)
        self.hueaddsub_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.hueaddsub_slider)

        self.horizontalSpacer_38 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_38)

        self.hueaddsub_spinbox = QSpinBox(Form)
        self.hueaddsub_spinbox.setObjectName(u"hueaddsub_spinbox")
        sizePolicy2.setHeightForWidth(self.hueaddsub_spinbox.sizePolicy().hasHeightForWidth())
        self.hueaddsub_spinbox.setSizePolicy(sizePolicy2)
        self.hueaddsub_spinbox.setMinimumSize(QSize(47, 0))
        self.hueaddsub_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.hueaddsub_spinbox.setMinimum(-179)
        self.hueaddsub_spinbox.setMaximum(179)

        self.horizontalLayout_10.addWidget(self.hueaddsub_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.sataddsub_lb = QLabel(Form)
        self.sataddsub_lb.setObjectName(u"sataddsub_lb")
        sizePolicy1.setHeightForWidth(self.sataddsub_lb.sizePolicy().hasHeightForWidth())
        self.sataddsub_lb.setSizePolicy(sizePolicy1)
        self.sataddsub_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_7.addWidget(self.sataddsub_lb)

        self.horizontalSpacer_13 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_13)

        self.sataddsub_slider = QSlider(Form)
        self.sataddsub_slider.setObjectName(u"sataddsub_slider")
        self.sataddsub_slider.setMinimum(-255)
        self.sataddsub_slider.setMaximum(255)
        self.sataddsub_slider.setValue(0)
        self.sataddsub_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_7.addWidget(self.sataddsub_slider)

        self.horizontalSpacer_14 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_14)

        self.sataddsub_spinbox = QSpinBox(Form)
        self.sataddsub_spinbox.setObjectName(u"sataddsub_spinbox")
        sizePolicy2.setHeightForWidth(self.sataddsub_spinbox.sizePolicy().hasHeightForWidth())
        self.sataddsub_spinbox.setSizePolicy(sizePolicy2)
        self.sataddsub_spinbox.setMinimumSize(QSize(47, 0))
        self.sataddsub_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.sataddsub_spinbox.setMinimum(-255)
        self.sataddsub_spinbox.setMaximum(255)

        self.horizontalLayout_7.addWidget(self.sataddsub_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.valaddsub_lb = QLabel(Form)
        self.valaddsub_lb.setObjectName(u"valaddsub_lb")
        sizePolicy1.setHeightForWidth(self.valaddsub_lb.sizePolicy().hasHeightForWidth())
        self.valaddsub_lb.setSizePolicy(sizePolicy1)
        self.valaddsub_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_8.addWidget(self.valaddsub_lb)

        self.horizontalSpacer_17 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_17)

        self.valaddsub_slider = QSlider(Form)
        self.valaddsub_slider.setObjectName(u"valaddsub_slider")
        self.valaddsub_slider.setMinimum(-255)
        self.valaddsub_slider.setMaximum(255)
        self.valaddsub_slider.setValue(0)
        self.valaddsub_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.valaddsub_slider)

        self.horizontalSpacer_18 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_18)

        self.valaddsub_spinbox = QSpinBox(Form)
        self.valaddsub_spinbox.setObjectName(u"valaddsub_spinbox")
        sizePolicy2.setHeightForWidth(self.valaddsub_spinbox.sizePolicy().hasHeightForWidth())
        self.valaddsub_spinbox.setSizePolicy(sizePolicy2)
        self.valaddsub_spinbox.setMinimumSize(QSize(47, 0))
        self.valaddsub_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.valaddsub_spinbox.setMinimum(-255)
        self.valaddsub_spinbox.setMaximum(255)

        self.horizontalLayout_8.addWidget(self.valaddsub_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.blurkernelsize_lb = QLabel(Form)
        self.blurkernelsize_lb.setObjectName(u"blurkernelsize_lb")
        sizePolicy1.setHeightForWidth(self.blurkernelsize_lb.sizePolicy().hasHeightForWidth())
        self.blurkernelsize_lb.setSizePolicy(sizePolicy1)
        self.blurkernelsize_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_18.addWidget(self.blurkernelsize_lb)

        self.horizontalSpacer_35 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_35)

        self.blurkernelsize_slider = QSlider(Form)
        self.blurkernelsize_slider.setObjectName(u"blurkernelsize_slider")
        self.blurkernelsize_slider.setEnabled(True)
        self.blurkernelsize_slider.setMinimum(1)
        self.blurkernelsize_slider.setMaximum(31)
        self.blurkernelsize_slider.setPageStep(1)
        self.blurkernelsize_slider.setValue(1)
        self.blurkernelsize_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_18.addWidget(self.blurkernelsize_slider)

        self.horizontalSpacer_36 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_36)

        self.blurkernelsize_spinbox = QSpinBox(Form)
        self.blurkernelsize_spinbox.setObjectName(u"blurkernelsize_spinbox")
        self.blurkernelsize_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.blurkernelsize_spinbox.sizePolicy().hasHeightForWidth())
        self.blurkernelsize_spinbox.setSizePolicy(sizePolicy2)
        self.blurkernelsize_spinbox.setMinimumSize(QSize(47, 0))
        self.blurkernelsize_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.blurkernelsize_spinbox.setMinimum(1)
        self.blurkernelsize_spinbox.setMaximum(31)
        self.blurkernelsize_spinbox.setSingleStep(2)
        self.blurkernelsize_spinbox.setDisplayIntegerBase(10)

        self.horizontalLayout_18.addWidget(self.blurkernelsize_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.gaussianblue_lb = QLabel(Form)
        self.gaussianblue_lb.setObjectName(u"gaussianblue_lb")
        sizePolicy1.setHeightForWidth(self.gaussianblue_lb.sizePolicy().hasHeightForWidth())
        self.gaussianblue_lb.setSizePolicy(sizePolicy1)
        self.gaussianblue_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_17.addWidget(self.gaussianblue_lb)

        self.horizontalSpacer_33 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_33)

        self.gaussianblur_slider = QSlider(Form)
        self.gaussianblur_slider.setObjectName(u"gaussianblur_slider")
        self.gaussianblur_slider.setEnabled(True)
        self.gaussianblur_slider.setMinimum(0)
        self.gaussianblur_slider.setMaximum(255)
        self.gaussianblur_slider.setValue(0)
        self.gaussianblur_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_17.addWidget(self.gaussianblur_slider)

        self.horizontalSpacer_34 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_34)

        self.gaussianblur_spinbox = QSpinBox(Form)
        self.gaussianblur_spinbox.setObjectName(u"gaussianblur_spinbox")
        self.gaussianblur_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.gaussianblur_spinbox.sizePolicy().hasHeightForWidth())
        self.gaussianblur_spinbox.setSizePolicy(sizePolicy2)
        self.gaussianblur_spinbox.setMinimumSize(QSize(47, 0))
        self.gaussianblur_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.gaussianblur_spinbox.setMinimum(0)
        self.gaussianblur_spinbox.setMaximum(255)

        self.horizontalLayout_17.addWidget(self.gaussianblur_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.kernelsize_lb = QLabel(Form)
        self.kernelsize_lb.setObjectName(u"kernelsize_lb")
        sizePolicy1.setHeightForWidth(self.kernelsize_lb.sizePolicy().hasHeightForWidth())
        self.kernelsize_lb.setSizePolicy(sizePolicy1)
        self.kernelsize_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_11.addWidget(self.kernelsize_lb)

        self.horizontalSpacer_19 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_19)

        self.kernelsize_slider = QSlider(Form)
        self.kernelsize_slider.setObjectName(u"kernelsize_slider")
        self.kernelsize_slider.setEnabled(False)
        self.kernelsize_slider.setMinimum(1)
        self.kernelsize_slider.setMaximum(31)
        self.kernelsize_slider.setPageStep(1)
        self.kernelsize_slider.setValue(1)
        self.kernelsize_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_11.addWidget(self.kernelsize_slider)

        self.horizontalSpacer_20 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_20)

        self.kernelsize_spinbox = QSpinBox(Form)
        self.kernelsize_spinbox.setObjectName(u"kernelsize_spinbox")
        self.kernelsize_spinbox.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.kernelsize_spinbox.sizePolicy().hasHeightForWidth())
        self.kernelsize_spinbox.setSizePolicy(sizePolicy2)
        self.kernelsize_spinbox.setMinimumSize(QSize(47, 0))
        self.kernelsize_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.kernelsize_spinbox.setMinimum(1)
        self.kernelsize_spinbox.setMaximum(31)

        self.horizontalLayout_11.addWidget(self.kernelsize_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.cannydilate_lb = QLabel(Form)
        self.cannydilate_lb.setObjectName(u"cannydilate_lb")
        sizePolicy1.setHeightForWidth(self.cannydilate_lb.sizePolicy().hasHeightForWidth())
        self.cannydilate_lb.setSizePolicy(sizePolicy1)
        self.cannydilate_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_15.addWidget(self.cannydilate_lb)

        self.horizontalSpacer_27 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_27)

        self.cannydilate_slider = QSlider(Form)
        self.cannydilate_slider.setObjectName(u"cannydilate_slider")
        self.cannydilate_slider.setEnabled(False)
        self.cannydilate_slider.setMinimum(1)
        self.cannydilate_slider.setMaximum(10)
        self.cannydilate_slider.setPageStep(1)
        self.cannydilate_slider.setValue(1)
        self.cannydilate_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_15.addWidget(self.cannydilate_slider)

        self.horizontalSpacer_28 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_28)

        self.cannydilate_spinbox = QSpinBox(Form)
        self.cannydilate_spinbox.setObjectName(u"cannydilate_spinbox")
        self.cannydilate_spinbox.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.cannydilate_spinbox.sizePolicy().hasHeightForWidth())
        self.cannydilate_spinbox.setSizePolicy(sizePolicy2)
        self.cannydilate_spinbox.setMinimumSize(QSize(47, 0))
        self.cannydilate_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.cannydilate_spinbox.setMinimum(1)
        self.cannydilate_spinbox.setMaximum(10)

        self.horizontalLayout_15.addWidget(self.cannydilate_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.cannyerode_lb = QLabel(Form)
        self.cannyerode_lb.setObjectName(u"cannyerode_lb")
        sizePolicy1.setHeightForWidth(self.cannyerode_lb.sizePolicy().hasHeightForWidth())
        self.cannyerode_lb.setSizePolicy(sizePolicy1)
        self.cannyerode_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_12.addWidget(self.cannyerode_lb)

        self.horizontalSpacer_21 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_21)

        self.cannyerode_slider = QSlider(Form)
        self.cannyerode_slider.setObjectName(u"cannyerode_slider")
        self.cannyerode_slider.setEnabled(False)
        self.cannyerode_slider.setMinimum(1)
        self.cannyerode_slider.setMaximum(10)
        self.cannyerode_slider.setPageStep(1)
        self.cannyerode_slider.setValue(1)
        self.cannyerode_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_12.addWidget(self.cannyerode_slider)

        self.horizontalSpacer_22 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_22)

        self.cannyerode_spinbox = QSpinBox(Form)
        self.cannyerode_spinbox.setObjectName(u"cannyerode_spinbox")
        self.cannyerode_spinbox.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.cannyerode_spinbox.sizePolicy().hasHeightForWidth())
        self.cannyerode_spinbox.setSizePolicy(sizePolicy2)
        self.cannyerode_spinbox.setMinimumSize(QSize(47, 0))
        self.cannyerode_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.cannyerode_spinbox.setMinimum(1)
        self.cannyerode_spinbox.setMaximum(10)

        self.horizontalLayout_12.addWidget(self.cannyerode_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.canny1_lb = QLabel(Form)
        self.canny1_lb.setObjectName(u"canny1_lb")
        sizePolicy1.setHeightForWidth(self.canny1_lb.sizePolicy().hasHeightForWidth())
        self.canny1_lb.setSizePolicy(sizePolicy1)
        self.canny1_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_14.addWidget(self.canny1_lb)

        self.horizontalSpacer_25 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_25)

        self.canny1_slider = QSlider(Form)
        self.canny1_slider.setObjectName(u"canny1_slider")
        self.canny1_slider.setEnabled(False)
        self.canny1_slider.setMinimum(0)
        self.canny1_slider.setMaximum(255)
        self.canny1_slider.setValue(0)
        self.canny1_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_14.addWidget(self.canny1_slider)

        self.horizontalSpacer_26 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_26)

        self.canny1_spinbox = QSpinBox(Form)
        self.canny1_spinbox.setObjectName(u"canny1_spinbox")
        self.canny1_spinbox.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.canny1_spinbox.sizePolicy().hasHeightForWidth())
        self.canny1_spinbox.setSizePolicy(sizePolicy2)
        self.canny1_spinbox.setMinimumSize(QSize(47, 0))
        self.canny1_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.canny1_spinbox.setMinimum(0)
        self.canny1_spinbox.setMaximum(255)

        self.horizontalLayout_14.addWidget(self.canny1_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.canny2_lb = QLabel(Form)
        self.canny2_lb.setObjectName(u"canny2_lb")
        sizePolicy1.setHeightForWidth(self.canny2_lb.sizePolicy().hasHeightForWidth())
        self.canny2_lb.setSizePolicy(sizePolicy1)
        self.canny2_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_13.addWidget(self.canny2_lb)

        self.horizontalSpacer_23 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_23)

        self.canny2_slider = QSlider(Form)
        self.canny2_slider.setObjectName(u"canny2_slider")
        self.canny2_slider.setEnabled(False)
        self.canny2_slider.setMinimum(0)
        self.canny2_slider.setMaximum(255)
        self.canny2_slider.setValue(0)
        self.canny2_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_13.addWidget(self.canny2_slider)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_24)

        self.canny2_spinbox = QSpinBox(Form)
        self.canny2_spinbox.setObjectName(u"canny2_spinbox")
        self.canny2_spinbox.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.canny2_spinbox.sizePolicy().hasHeightForWidth())
        self.canny2_spinbox.setSizePolicy(sizePolicy2)
        self.canny2_spinbox.setMinimumSize(QSize(47, 0))
        self.canny2_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.canny2_spinbox.setMinimum(0)
        self.canny2_spinbox.setMaximum(255)

        self.horizontalLayout_13.addWidget(self.canny2_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.output_dilate_lb_2 = QLabel(Form)
        self.output_dilate_lb_2.setObjectName(u"output_dilate_lb_2")
        sizePolicy1.setHeightForWidth(self.output_dilate_lb_2.sizePolicy().hasHeightForWidth())
        self.output_dilate_lb_2.setSizePolicy(sizePolicy1)
        self.output_dilate_lb_2.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_20.addWidget(self.output_dilate_lb_2)

        self.horizontalSpacer_39 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_39)

        self.output_dilate_slider = QSlider(Form)
        self.output_dilate_slider.setObjectName(u"output_dilate_slider")
        self.output_dilate_slider.setEnabled(True)
        self.output_dilate_slider.setMinimum(1)
        self.output_dilate_slider.setMaximum(10)
        self.output_dilate_slider.setPageStep(1)
        self.output_dilate_slider.setValue(1)
        self.output_dilate_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_20.addWidget(self.output_dilate_slider)

        self.horizontalSpacer_40 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_40)

        self.output_dilate_spinbox = QSpinBox(Form)
        self.output_dilate_spinbox.setObjectName(u"output_dilate_spinbox")
        self.output_dilate_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.output_dilate_spinbox.sizePolicy().hasHeightForWidth())
        self.output_dilate_spinbox.setSizePolicy(sizePolicy2)
        self.output_dilate_spinbox.setMinimumSize(QSize(47, 0))
        self.output_dilate_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.output_dilate_spinbox.setMinimum(1)
        self.output_dilate_spinbox.setMaximum(10)

        self.horizontalLayout_20.addWidget(self.output_dilate_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.output_erode_lb_2 = QLabel(Form)
        self.output_erode_lb_2.setObjectName(u"output_erode_lb_2")
        sizePolicy1.setHeightForWidth(self.output_erode_lb_2.sizePolicy().hasHeightForWidth())
        self.output_erode_lb_2.setSizePolicy(sizePolicy1)
        self.output_erode_lb_2.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_21.addWidget(self.output_erode_lb_2)

        self.horizontalSpacer_41 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_41)

        self.output_erode_slider = QSlider(Form)
        self.output_erode_slider.setObjectName(u"output_erode_slider")
        self.output_erode_slider.setEnabled(True)
        self.output_erode_slider.setMinimum(1)
        self.output_erode_slider.setMaximum(10)
        self.output_erode_slider.setPageStep(1)
        self.output_erode_slider.setValue(1)
        self.output_erode_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_21.addWidget(self.output_erode_slider)

        self.horizontalSpacer_42 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_42)

        self.output_erode_spinbox = QSpinBox(Form)
        self.output_erode_spinbox.setObjectName(u"output_erode_spinbox")
        self.output_erode_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.output_erode_spinbox.sizePolicy().hasHeightForWidth())
        self.output_erode_spinbox.setSizePolicy(sizePolicy2)
        self.output_erode_spinbox.setMinimumSize(QSize(47, 0))
        self.output_erode_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.output_erode_spinbox.setMinimum(1)
        self.output_erode_spinbox.setMaximum(10)

        self.horizontalLayout_21.addWidget(self.output_erode_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.canny2_lb_2 = QLabel(Form)
        self.canny2_lb_2.setObjectName(u"canny2_lb_2")
        sizePolicy1.setHeightForWidth(self.canny2_lb_2.sizePolicy().hasHeightForWidth())
        self.canny2_lb_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_16.addWidget(self.canny2_lb_2)

        self.horizontalSpacer_29 = QSpacerItem(15, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_29)

        self.canny_radiobt = QRadioButton(Form)
        self.canny_radiobt.setObjectName(u"canny_radiobt")
        self.canny_radiobt.setLayoutDirection(Qt.LeftToRight)
        self.canny_radiobt.setAutoRepeat(False)
        self.canny_radiobt.setAutoExclusive(False)

        self.horizontalLayout_16.addWidget(self.canny_radiobt)

        self.horizontalSpacer_30 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_30)

        self.sobel_radiobt = QRadioButton(Form)
        self.sobel_radiobt.setObjectName(u"sobel_radiobt")
        self.sobel_radiobt.setEnabled(True)
        self.sobel_radiobt.setAutoExclusive(False)

        self.horizontalLayout_16.addWidget(self.sobel_radiobt)

        self.horizontalSpacer_31 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_31)

        self.laplace_radiobt = QRadioButton(Form)
        self.laplace_radiobt.setObjectName(u"laplace_radiobt")
        self.laplace_radiobt.setEnabled(True)
        self.laplace_radiobt.setAutoExclusive(False)

        self.horizontalLayout_16.addWidget(self.laplace_radiobt)

        self.horizontalSpacer_32 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_32)


        self.verticalLayout.addLayout(self.horizontalLayout_16)

        self.verticalSpacer_4 = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.reset_bt = QPushButton(Form)
        self.reset_bt.setObjectName(u"reset_bt")

        self.horizontalLayout_9.addWidget(self.reset_bt)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_15)

        self.horizontalSpacer_16 = QSpacerItem(40, 18, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_16)

        self.close_bt = QPushButton(Form)
        self.close_bt.setObjectName(u"close_bt")

        self.horizontalLayout_9.addWidget(self.close_bt)


        self.verticalLayout.addLayout(self.horizontalLayout_9)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Controlo de Filtros", None))
        self.title_lb.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Filtros de Sa\u00edda</span> [Tempo Real]</p></body></html>", None))
        self.minhue_lb.setText(QCoreApplication.translate("Form", u"Min Hue", None))
        self.maxhue_lb.setText(QCoreApplication.translate("Form", u"Max Hue", None))
        self.minsat_lb.setText(QCoreApplication.translate("Form", u"Min Saturation", None))
        self.maxsat_lb.setText(QCoreApplication.translate("Form", u"Max Saturation", None))
        self.minval_lb.setText(QCoreApplication.translate("Form", u"Min Value", None))
        self.maxval_lb.setText(QCoreApplication.translate("Form", u"Max Value", None))
        self.hueaddsub_lb.setText(QCoreApplication.translate("Form", u"\u00b1 Hue", None))
        self.sataddsub_lb.setText(QCoreApplication.translate("Form", u"\u00b1 Saturation", None))
        self.valaddsub_lb.setText(QCoreApplication.translate("Form", u"\u00b1 Value", None))
        self.blurkernelsize_lb.setText(QCoreApplication.translate("Form", u"Blur KernelSize", None))
        self.gaussianblue_lb.setText(QCoreApplication.translate("Form", u"Gaussian Blur", None))
        self.kernelsize_lb.setText(QCoreApplication.translate("Form", u"KernelSize", None))
        self.cannydilate_lb.setText(QCoreApplication.translate("Form", u"Canny Dilate", None))
        self.cannyerode_lb.setText(QCoreApplication.translate("Form", u"Canny Erode", None))
        self.canny1_lb.setText(QCoreApplication.translate("Form", u"Min Canny", None))
        self.canny2_lb.setText(QCoreApplication.translate("Form", u"Max Canny", None))
        self.output_dilate_lb_2.setText(QCoreApplication.translate("Form", u"Output Dilate", None))
        self.output_erode_lb_2.setText(QCoreApplication.translate("Form", u"Output Erode", None))
        self.canny2_lb_2.setText(QCoreApplication.translate("Form", u"Contornos", None))
        self.canny_radiobt.setText(QCoreApplication.translate("Form", u"Canny", None))
        self.sobel_radiobt.setText(QCoreApplication.translate("Form", u"Sobel", None))
        self.laplace_radiobt.setText(QCoreApplication.translate("Form", u"Laplace", None))
        self.reset_bt.setText(QCoreApplication.translate("Form", u"Repor", None))
        self.close_bt.setText(QCoreApplication.translate("Form", u"Fechar", None))
    # retranslateUi

