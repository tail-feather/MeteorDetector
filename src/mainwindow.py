import os
import shutil

import cv2

from PySide2.QtCore import Qt
from PySide2.QtCore import Slot
from PySide2.QtCore import QEvent
from PySide2.QtCore import QFileInfo
from PySide2.QtCore import QMetaObject
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import QObject
from PySide2.QtCore import QThread
from PySide2.QtGui import QColor
from PySide2.QtGui import QImage
from PySide2.QtGui import QPen
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QGraphicsPixmapItem
from PySide2.QtWidgets import QGraphicsScene
from PySide2.QtWidgets import QTreeView
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QProgressBar


from .configdialog import ConfigDialog
from . import detector
from .event import JPEGFilesDragAndDropFilter
from .model import JPEGFileListModel
from .ui.mainwindow import Ui_MainWindow
from .worker import FileCopyWorker
from .worker import MeteorDetectWorker


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = ConfigDialog()
        # model & view
        self.imageListModel = JPEGFileListModel()
        self.ui.treeView.setModel(self.imageListModel)
        self.dndFilter = JPEGFilesDragAndDropFilter()
        self.ui.treeView.installEventFilter(self.dndFilter)
        # status
        self.progressBar = QProgressBar(self.ui.statusbar)
        self.progressBar.setValue(0)
        self.ui.statusbar.addWidget(self.progressBar)
        # workers
        self.detectorThread = QThread(self)
        self.detectorWorker = None
        self.fileCopyThread = QThread(self)
        self.fileCopyWorker = None
        # image view
        self.hideDetected = False
        self.currentImagePath = None
        self.temp = None

    def closeEvent(self, event):
        if self.detectorThread.isRunning():
            self.detectorThread.exit()
            self.detectorThread.wait()
        if self.fileCopyThread.isRunning():
            self.fileCopyThread.exit()
            self.fileCopyThread.wait()
        # TODO: ask continue
        event.accept()

    @Slot()
    def on_actionExit_triggered(self):
        self.close()

    @Slot()
    def on_actionAdd_triggered(self):
        filelist, _ = QFileDialog.getOpenFileNames(self, self.tr("Add JPEG files"), "", self.tr("JPEG (*.jpg *.jpeg);;All Files(*.*)"))
        if not filelist:
            return
        self.imageListModel.addFiles(filelist)

    @Slot()
    def on_actionClear_triggered(self):
        self.imageListModel.clear()

    @Slot()
    def on_actionConfig_triggered(self):
        self.config.updateUi()
        self.config.show()
        if self.config.exec_() == QDialog.Accepted:
            self.config.updateConfig()
            self.showImage()

    @Slot()
    def on_actionRun_triggered(self):
        if self.detectorWorker is not None:
            # already running
            return
        filelist = self.imageListModel.fileList()
        if not filelist:
            return
        self.detectorWorker = MeteorDetectWorker(filelist, self.config.getConfig())
        self.detectorWorker.initializeProgress.connect(self.progressBar.setRange)
        self.detectorWorker.updateProgress.connect(self.progressBar.setValue)
        self.detectorWorker.updateContext.connect(self.detectorWorker_updateContext)
        self.detectorWorker.done.connect(self.detectorWorker_done)
        self.detectorWorker.error.connect(self.worker_error)
        self.detectorWorker.moveToThread(self.detectorThread)
        self.detectorThread.start()
        QMetaObject.invokeMethod(self.detectorWorker, "run")

    @Slot(str, tuple, list, list)
    def detectorWorker_updateContext(self, filepath: str, shape: tuple, filled: list, lines: list):
        self.imageListModel.updateContext(filepath, shape, filled, lines)

    @Slot()
    def detectorWorker_done(self):
        self.detectorThread.exit()
        self.detectorThread.wait()
        detected = self.detectorWorker.detected_list
        del self.detectorWorker
        self.detectorWorker = None
        QMessageBox.information(self, self.tr("Done"), self.tr("{} images detected.").format(len(detected)))

    @Slot()
    def on_actionExport_triggered(self):
        if self.fileCopyWorker is not None:
            # already running
            return
        dirname = QFileDialog.getExistingDirectory(self, self.tr("Export directory"))
        if not dirname:
            return
        highlighted = self.imageListModel.getHighlighted()
        if not highlighted:
            QMessageBox.warning(self, self.tr("Not highlighted"), self.tr("There is nothing to write out."))
            return
        self.fileCopyWorker = FileCopyWorker(highlighted, dirname)
        self.fileCopyWorker.initializeProgress.connect(self.progressBar.setRange)
        self.fileCopyWorker.updateProgress.connect(self.progressBar.setValue)
        self.fileCopyWorker.done.connect(self.fileCopyWorker_done)
        self.fileCopyWorker.error.connect(self.worker_error)
        self.fileCopyWorker.moveToThread(self.fileCopyThread)
        self.fileCopyThread.start()
        QMetaObject.invokeMethod(self.fileCopyWorker, "run")

    @Slot()
    def fileCopyWorker_done(self):
        self.fileCopyThread.exit()
        self.fileCopyThread.wait()
        del self.fileCopyWorker
        self.fileCopyWorker = None
        QMessageBox.information(self, self.tr("Done"), self.tr("File exported."))

    @Slot(bool)
    def on_actionHideDetected_triggered(self, checked: bool):
        self.hideDetected = checked
        self.showImage()

    @Slot(str)
    def worker_error(self, message: str):
        print(message)

    @Slot()
    def on_actionAboutQt_triggered(self):
        QApplication.aboutQt()

    @Slot(QModelIndex)
    def on_treeView_activated(self, index: QModelIndex):
        filepath = self.imageListModel.at(index.sibling(index.row(), 0))
        self.currentImagePath = filepath
        self.showImage()

    def showImage(self):
        image = self.loadImage(self.currentImagePath)
        if not image:
            return
        item = QGraphicsPixmapItem(QPixmap.fromImage(image))
        scene = QGraphicsScene()
        scene.addItem(item)
        context = self.imageListModel.getContext(self.currentImagePath)
        if not self.hideDetected and context is not None:
            shape, contours, lines = context
            contourPen = QPen(QColor(0xff, 0x00, 0x00), 1)
            for cnt in contours:
                cnt = [x[0] for x in cnt]
                x0, y0 = cnt[0]
                for x, y in cnt[1:]:
                    scene.addLine(x0, y0, x, y, contourPen)
                    x0, y0 = x, y
            linePen = QPen(QColor(0x00, 0xff, 0x00), 3)
            if lines:
                for line in lines[0]:
                    x0, y0, x1, y1 = line
                    scene.addLine(x0, y0, x1, y1, linePen)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(item.boundingRect(), Qt.KeepAspectRatio)

    def loadImage(self, filepath: str):
        if not filepath:
            return None
        if not os.path.exists(filepath):
            return None
        config = self.config.getConfig()
        if self.ui.radioButtonImageThreshold.isChecked():
            # threshold image
            img = detector.load_binary(filepath, config.input_threshold, config.input_maxvalue)
            height, width = img.shape
            self.temp = img.flatten()
            return QImage(self.temp, width, height, QImage.Format_Grayscale8)
        elif self.ui.radioButtonImageFilled.isChecked():
            # filled-image
            img = detector.load_binary(filepath, config.input_threshold, config.area_threshold)
            area_contours = detector.detect_area(img)
            boundingRect = None
            if area_contours:
                img = detector.fill_area(img, area_contours, color=0)
            height, width = img.shape
            self.temp = img.flatten()
            return QImage(self.temp, width, height, width, QImage.Format_Grayscale8)
        # original (default) case
        return QImage(filepath)

    @Slot(bool)
    def on_radioButtonImageOriginal_clicked(self, checked: bool = False):
        self.showImage()

    @Slot(bool)
    def on_radioButtonImageThreshold_clicked(self, checked: bool = False):
        self.showImage()

    @Slot(bool)
    def on_radioButtonImageFilled_clicked(self, checked: bool = False):
        self.showImage()
