# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(799, 463)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionReset = QAction(MainWindow)
        self.actionReset.setObjectName(u"actionReset")
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        self.actionClear = QAction(MainWindow)
        self.actionClear.setObjectName(u"actionClear")
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName(u"actionRun")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionAboutQt = QAction(MainWindow)
        self.actionAboutQt.setObjectName(u"actionAboutQt")
        self.actionConfig = QAction(MainWindow)
        self.actionConfig.setObjectName(u"actionConfig")
        self.actionHideDetected = QAction(MainWindow)
        self.actionHideDetected.setObjectName(u"actionHideDetected")
        self.actionHideDetected.setCheckable(True)
        self.actionHideDetected.setChecked(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.treeView = QTreeView(self.splitter)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setDragEnabled(False)
        self.treeView.setDragDropMode(QAbstractItemView.DropOnly)
        self.treeView.setDefaultDropAction(Qt.IgnoreAction)
        self.splitter.addWidget(self.treeView)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = QGraphicsView(self.widget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButtonImageOriginal = QRadioButton(self.widget)
        self.radioButtonImageOriginal.setObjectName(u"radioButtonImageOriginal")
        self.radioButtonImageOriginal.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButtonImageOriginal)

        self.radioButtonImageThreshold = QRadioButton(self.widget)
        self.radioButtonImageThreshold.setObjectName(u"radioButtonImageThreshold")

        self.horizontalLayout.addWidget(self.radioButtonImageThreshold)

        self.radioButtonImageFilled = QRadioButton(self.widget)
        self.radioButtonImageFilled.setObjectName(u"radioButtonImageFilled")

        self.horizontalLayout.addWidget(self.radioButtonImageFilled)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.widget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 799, 28))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuImage = QMenu(self.menubar)
        self.menuImage.setObjectName(u"menuImage")
        self.menuProc = QMenu(self.menubar)
        self.menuProc.setObjectName(u"menuProc")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuProc.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuImage.addAction(self.actionAdd)
        self.menuImage.addAction(self.actionClear)
        self.menuProc.addAction(self.actionConfig)
        self.menuProc.addAction(self.actionRun)
        self.menuProc.addAction(self.actionExport)
        self.menuProc.addAction(self.actionHideDetected)
        self.menuHelp.addAction(self.actionAboutQt)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MeteorDetector", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionReset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.actionClear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.actionRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
#if QT_CONFIG(shortcut)
        self.actionRun.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionAboutQt.setText(QCoreApplication.translate("MainWindow", u"AboutQt", None))
        self.actionConfig.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.actionHideDetected.setText(QCoreApplication.translate("MainWindow", u"HideDetected", None))
        self.radioButtonImageOriginal.setText(QCoreApplication.translate("MainWindow", u"Original", None))
        self.radioButtonImageThreshold.setText(QCoreApplication.translate("MainWindow", u"Threshold", None))
        self.radioButtonImageFilled.setText(QCoreApplication.translate("MainWindow", u"Filled", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuImage.setTitle(QCoreApplication.translate("MainWindow", u"Image", None))
        self.menuProc.setTitle(QCoreApplication.translate("MainWindow", u"Proc", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

