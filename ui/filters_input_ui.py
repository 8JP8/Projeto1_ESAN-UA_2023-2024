# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filters_input.ui'
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
        Form.resize(414, 602)
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
        self.addsubsat_lb = QLabel(Form)
        self.addsubsat_lb.setObjectName(u"addsubsat_lb")
        sizePolicy1.setHeightForWidth(self.addsubsat_lb.sizePolicy().hasHeightForWidth())
        self.addsubsat_lb.setSizePolicy(sizePolicy1)
        self.addsubsat_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_7.addWidget(self.addsubsat_lb)

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
        self.addsubsat_lb_2 = QLabel(Form)
        self.addsubsat_lb_2.setObjectName(u"addsubsat_lb_2")
        sizePolicy1.setHeightForWidth(self.addsubsat_lb_2.sizePolicy().hasHeightForWidth())
        self.addsubsat_lb_2.setSizePolicy(sizePolicy1)
        self.addsubsat_lb_2.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_8.addWidget(self.addsubsat_lb_2)

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

        self.horizontalSpacer_34 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

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
        self.kernelsize_slider.setEnabled(True)
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
        self.kernelsize_spinbox.setEnabled(True)
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
        self.dilate1_lb = QLabel(Form)
        self.dilate1_lb.setObjectName(u"dilate1_lb")
        sizePolicy1.setHeightForWidth(self.dilate1_lb.sizePolicy().hasHeightForWidth())
        self.dilate1_lb.setSizePolicy(sizePolicy1)
        self.dilate1_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_15.addWidget(self.dilate1_lb)

        self.horizontalSpacer_27 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_27)

        self.dilate1_slider = QSlider(Form)
        self.dilate1_slider.setObjectName(u"dilate1_slider")
        self.dilate1_slider.setEnabled(True)
        self.dilate1_slider.setMinimum(1)
        self.dilate1_slider.setMaximum(10)
        self.dilate1_slider.setPageStep(1)
        self.dilate1_slider.setValue(1)
        self.dilate1_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_15.addWidget(self.dilate1_slider)

        self.horizontalSpacer_28 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_28)

        self.dilate1_spinbox = QSpinBox(Form)
        self.dilate1_spinbox.setObjectName(u"dilate1_spinbox")
        self.dilate1_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.dilate1_spinbox.sizePolicy().hasHeightForWidth())
        self.dilate1_spinbox.setSizePolicy(sizePolicy2)
        self.dilate1_spinbox.setMinimumSize(QSize(47, 0))
        self.dilate1_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.dilate1_spinbox.setMinimum(1)
        self.dilate1_spinbox.setMaximum(10)

        self.horizontalLayout_15.addWidget(self.dilate1_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.erode1_lb = QLabel(Form)
        self.erode1_lb.setObjectName(u"erode1_lb")
        sizePolicy1.setHeightForWidth(self.erode1_lb.sizePolicy().hasHeightForWidth())
        self.erode1_lb.setSizePolicy(sizePolicy1)
        self.erode1_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_12.addWidget(self.erode1_lb)

        self.horizontalSpacer_21 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_21)

        self.erode1_slider = QSlider(Form)
        self.erode1_slider.setObjectName(u"erode1_slider")
        self.erode1_slider.setEnabled(True)
        self.erode1_slider.setMinimum(1)
        self.erode1_slider.setMaximum(10)
        self.erode1_slider.setPageStep(1)
        self.erode1_slider.setValue(1)
        self.erode1_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_12.addWidget(self.erode1_slider)

        self.horizontalSpacer_22 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_22)

        self.erode1_spinbox = QSpinBox(Form)
        self.erode1_spinbox.setObjectName(u"erode1_spinbox")
        self.erode1_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.erode1_spinbox.sizePolicy().hasHeightForWidth())
        self.erode1_spinbox.setSizePolicy(sizePolicy2)
        self.erode1_spinbox.setMinimumSize(QSize(47, 0))
        self.erode1_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.erode1_spinbox.setMinimum(1)
        self.erode1_spinbox.setMaximum(10)

        self.horizontalLayout_12.addWidget(self.erode1_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.dilate2_lb = QLabel(Form)
        self.dilate2_lb.setObjectName(u"dilate2_lb")
        sizePolicy1.setHeightForWidth(self.dilate2_lb.sizePolicy().hasHeightForWidth())
        self.dilate2_lb.setSizePolicy(sizePolicy1)
        self.dilate2_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_20.addWidget(self.dilate2_lb)

        self.horizontalSpacer_39 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_39)

        self.dilate2_slider = QSlider(Form)
        self.dilate2_slider.setObjectName(u"dilate2_slider")
        self.dilate2_slider.setEnabled(True)
        self.dilate2_slider.setMinimum(1)
        self.dilate2_slider.setMaximum(10)
        self.dilate2_slider.setPageStep(1)
        self.dilate2_slider.setValue(1)
        self.dilate2_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_20.addWidget(self.dilate2_slider)

        self.horizontalSpacer_40 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_40)

        self.dilate2_spinbox = QSpinBox(Form)
        self.dilate2_spinbox.setObjectName(u"dilate2_spinbox")
        self.dilate2_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.dilate2_spinbox.sizePolicy().hasHeightForWidth())
        self.dilate2_spinbox.setSizePolicy(sizePolicy2)
        self.dilate2_spinbox.setMinimumSize(QSize(47, 0))
        self.dilate2_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.dilate2_spinbox.setMinimum(1)
        self.dilate2_spinbox.setMaximum(10)

        self.horizontalLayout_20.addWidget(self.dilate2_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.erode2_lb = QLabel(Form)
        self.erode2_lb.setObjectName(u"erode2_lb")
        sizePolicy1.setHeightForWidth(self.erode2_lb.sizePolicy().hasHeightForWidth())
        self.erode2_lb.setSizePolicy(sizePolicy1)
        self.erode2_lb.setMinimumSize(QSize(82, 0))

        self.horizontalLayout_21.addWidget(self.erode2_lb)

        self.horizontalSpacer_41 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_41)

        self.erode2_slider = QSlider(Form)
        self.erode2_slider.setObjectName(u"erode2_slider")
        self.erode2_slider.setEnabled(True)
        self.erode2_slider.setMinimum(1)
        self.erode2_slider.setMaximum(10)
        self.erode2_slider.setPageStep(1)
        self.erode2_slider.setValue(1)
        self.erode2_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_21.addWidget(self.erode2_slider)

        self.horizontalSpacer_42 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_42)

        self.erode2_spinbox = QSpinBox(Form)
        self.erode2_spinbox.setObjectName(u"erode2_spinbox")
        self.erode2_spinbox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.erode2_spinbox.sizePolicy().hasHeightForWidth())
        self.erode2_spinbox.setSizePolicy(sizePolicy2)
        self.erode2_spinbox.setMinimumSize(QSize(47, 0))
        self.erode2_spinbox.setInputMethodHints(Qt.ImhDigitsOnly)
        self.erode2_spinbox.setMinimum(1)
        self.erode2_spinbox.setMaximum(10)

        self.horizontalLayout_21.addWidget(self.erode2_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.dilate_erode_apply_lb = QLabel(Form)
        self.dilate_erode_apply_lb.setObjectName(u"dilate_erode_apply_lb")
        sizePolicy1.setHeightForWidth(self.dilate_erode_apply_lb.sizePolicy().hasHeightForWidth())
        self.dilate_erode_apply_lb.setSizePolicy(sizePolicy1)

        self.horizontalLayout_16.addWidget(self.dilate_erode_apply_lb)

        self.horizontalSpacer_29 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_29)

        self.pre_apply_radiobt = QRadioButton(Form)
        self.pre_apply_radiobt.setObjectName(u"pre_apply_radiobt")
        self.pre_apply_radiobt.setLayoutDirection(Qt.LeftToRight)
        self.pre_apply_radiobt.setAutoRepeat(False)
        self.pre_apply_radiobt.setAutoExclusive(False)

        self.horizontalLayout_16.addWidget(self.pre_apply_radiobt)

        self.horizontalSpacer_30 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_30)

        self.post_apply_radiobt = QRadioButton(Form)
        self.post_apply_radiobt.setObjectName(u"post_apply_radiobt")
        self.post_apply_radiobt.setEnabled(True)
        self.post_apply_radiobt.setAutoExclusive(False)

        self.horizontalLayout_16.addWidget(self.post_apply_radiobt)

        self.horizontalSpacer_31 = QSpacerItem(13, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_31)


        self.verticalLayout.addLayout(self.horizontalLayout_16)

        self.verticalSpacer_4 = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.verticalSpacer_5 = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer_5)

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
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Controlo de Filtros [Entrada]", None))
        self.title_lb.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Filtros de Entrada</span> [Tempo Real]</p></body></html>", None))
        self.minhue_lb.setText(QCoreApplication.translate("Form", u"Min Hue", None))
        self.maxhue_lb.setText(QCoreApplication.translate("Form", u"Max Hue", None))
        self.minsat_lb.setText(QCoreApplication.translate("Form", u"Min Saturation", None))
        self.maxsat_lb.setText(QCoreApplication.translate("Form", u"Max Saturation", None))
        self.minval_lb.setText(QCoreApplication.translate("Form", u"Min Value", None))
        self.maxval_lb.setText(QCoreApplication.translate("Form", u"Max Value", None))
        self.hueaddsub_lb.setText(QCoreApplication.translate("Form", u"\u00b1 Hue", None))
        self.addsubsat_lb.setText(QCoreApplication.translate("Form", u"\u00b1 Saturation", None))
        self.addsubsat_lb_2.setText(QCoreApplication.translate("Form", u"\u00b1 Value", None))
        self.blurkernelsize_lb.setText(QCoreApplication.translate("Form", u"Blur KernelSize", None))
        self.gaussianblue_lb.setText(QCoreApplication.translate("Form", u"Gaussian Blur", None))
        self.kernelsize_lb.setText(QCoreApplication.translate("Form", u"KernelSize", None))
        self.dilate1_lb.setText(QCoreApplication.translate("Form", u"Dilate 1", None))
        self.erode1_lb.setText(QCoreApplication.translate("Form", u"Erode 1", None))
        self.dilate2_lb.setText(QCoreApplication.translate("Form", u"Dilate 2", None))
        self.erode2_lb.setText(QCoreApplication.translate("Form", u"Erode 2", None))
        self.dilate_erode_apply_lb.setText(QCoreApplication.translate("Form", u"Dilate/Erode", None))
        self.pre_apply_radiobt.setText(QCoreApplication.translate("Form", u"Pr\u00e9-Aplicar", None))
        self.post_apply_radiobt.setText(QCoreApplication.translate("Form", u"P\u00f3s-Aplicar", None))
        self.reset_bt.setText(QCoreApplication.translate("Form", u"Repor", None))
        self.close_bt.setText(QCoreApplication.translate("Form", u"Fechar", None))
    # retranslateUi

