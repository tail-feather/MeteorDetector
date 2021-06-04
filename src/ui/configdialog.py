# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        if not ConfigDialog.objectName():
            ConfigDialog.setObjectName(u"ConfigDialog")
        ConfigDialog.resize(371, 304)
        self.gridLayout = QGridLayout(ConfigDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_threshold = QGroupBox(ConfigDialog)
        self.groupBox_threshold.setObjectName(u"groupBox_threshold")
        self.formLayout = QFormLayout(self.groupBox_threshold)
        self.formLayout.setObjectName(u"formLayout")
        self.label_threshold_threshold = QLabel(self.groupBox_threshold)
        self.label_threshold_threshold.setObjectName(u"label_threshold_threshold")
        self.label_threshold_threshold.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_threshold_threshold)

        self.spinBox_threshold_threshold = QSpinBox(self.groupBox_threshold)
        self.spinBox_threshold_threshold.setObjectName(u"spinBox_threshold_threshold")
        self.spinBox_threshold_threshold.setMaximum(255)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spinBox_threshold_threshold)

        self.label_threshold_maxvalue = QLabel(self.groupBox_threshold)
        self.label_threshold_maxvalue.setObjectName(u"label_threshold_maxvalue")
        self.label_threshold_maxvalue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_threshold_maxvalue)

        self.spinBox_threshold_maxvalue = QSpinBox(self.groupBox_threshold)
        self.spinBox_threshold_maxvalue.setObjectName(u"spinBox_threshold_maxvalue")
        self.spinBox_threshold_maxvalue.setMaximum(255)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinBox_threshold_maxvalue)


        self.gridLayout.addWidget(self.groupBox_threshold, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.gridLayout.addWidget(self.buttonBox, 0, 1, 3, 1)

        self.groupBox_fillarea = QGroupBox(ConfigDialog)
        self.groupBox_fillarea.setObjectName(u"groupBox_fillarea")
        self.formLayout_2 = QFormLayout(self.groupBox_fillarea)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_fillarea_areathreshold = QLabel(self.groupBox_fillarea)
        self.label_fillarea_areathreshold.setObjectName(u"label_fillarea_areathreshold")
        self.label_fillarea_areathreshold.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_fillarea_areathreshold)

        self.doubleSpinBox_fillarea_areathreshold = QDoubleSpinBox(self.groupBox_fillarea)
        self.doubleSpinBox_fillarea_areathreshold.setObjectName(u"doubleSpinBox_fillarea_areathreshold")
        self.doubleSpinBox_fillarea_areathreshold.setDecimals(2)
        self.doubleSpinBox_fillarea_areathreshold.setMaximum(100.000000000000000)
        self.doubleSpinBox_fillarea_areathreshold.setValue(0.010000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_fillarea_areathreshold)

        self.label_fillarea_fillbuffer = QLabel(self.groupBox_fillarea)
        self.label_fillarea_fillbuffer.setObjectName(u"label_fillarea_fillbuffer")
        self.label_fillarea_fillbuffer.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_fillarea_fillbuffer)

        self.doubleSpinBox_fillarea_fillbuffer = QDoubleSpinBox(self.groupBox_fillarea)
        self.doubleSpinBox_fillarea_fillbuffer.setObjectName(u"doubleSpinBox_fillarea_fillbuffer")
        self.doubleSpinBox_fillarea_fillbuffer.setDecimals(1)
        self.doubleSpinBox_fillarea_fillbuffer.setMaximum(5.000000000000000)
        self.doubleSpinBox_fillarea_fillbuffer.setValue(1.100000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_fillarea_fillbuffer)


        self.gridLayout.addWidget(self.groupBox_fillarea, 1, 0, 1, 1)

        self.groupBox = QGroupBox(ConfigDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout_3 = QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_meteordetection_linethreshold = QLabel(self.groupBox)
        self.label_meteordetection_linethreshold.setObjectName(u"label_meteordetection_linethreshold")
        self.label_meteordetection_linethreshold.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_meteordetection_linethreshold)

        self.doubleSpinBox_meteordetection_linethreshold = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_meteordetection_linethreshold.setObjectName(u"doubleSpinBox_meteordetection_linethreshold")
        self.doubleSpinBox_meteordetection_linethreshold.setDecimals(1)
        self.doubleSpinBox_meteordetection_linethreshold.setMaximum(1000.000000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_meteordetection_linethreshold)


        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)


        self.retranslateUi(ConfigDialog)
        self.buttonBox.accepted.connect(ConfigDialog.accept)
        self.buttonBox.rejected.connect(ConfigDialog.reject)

        QMetaObject.connectSlotsByName(ConfigDialog)
    # setupUi

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QCoreApplication.translate("ConfigDialog", u"Config", None))
        self.groupBox_threshold.setTitle(QCoreApplication.translate("ConfigDialog", u"cv2.threshold", None))
        self.label_threshold_threshold.setText(QCoreApplication.translate("ConfigDialog", u"Threshold:", None))
        self.label_threshold_maxvalue.setText(QCoreApplication.translate("ConfigDialog", u"MaxValue:", None))
        self.groupBox_fillarea.setTitle(QCoreApplication.translate("ConfigDialog", u"FillArea", None))
        self.label_fillarea_areathreshold.setText(QCoreApplication.translate("ConfigDialog", u"AreaThreshold:", None))
        self.doubleSpinBox_fillarea_areathreshold.setSuffix(QCoreApplication.translate("ConfigDialog", u"%", None))
        self.label_fillarea_fillbuffer.setText(QCoreApplication.translate("ConfigDialog", u"FillBuffer:", None))
        self.doubleSpinBox_fillarea_fillbuffer.setSuffix(QCoreApplication.translate("ConfigDialog", u"x", None))
        self.groupBox.setTitle(QCoreApplication.translate("ConfigDialog", u"MeteorDetection", None))
        self.label_meteordetection_linethreshold.setText(QCoreApplication.translate("ConfigDialog", u"LineThreshold:", None))
        self.doubleSpinBox_meteordetection_linethreshold.setSuffix(QCoreApplication.translate("ConfigDialog", u"px", None))
    # retranslateUi

