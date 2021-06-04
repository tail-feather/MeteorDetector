import io
import os
import shutil
import traceback

from PySide2.QtCore import Signal
from PySide2.QtCore import Slot
from PySide2.QtCore import QObject

from .configdialog import Config
from .detector import detect_meteor


class Worker(QObject):

    initializeProgress = Signal(int, int)
    updateProgress = Signal(int)

    done = Signal()
    aborted = Signal()
    message = Signal(str)
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)


class FileCopyWorker(Worker):
    def __init__(self, filelist: list[str], dest: str, parent=None):
        super().__init__(parent)
        self.filelist = filelist
        self.dest = dest

    @Slot()
    def run(self):
        self.initializeProgress.emit(0, len(self.filelist))
        for i, filepath in enumerate(self.filelist, 1):
            self.updateProgress.emit(i)
            if not os.path.exists(filepath):
                continue
            dstpath = os.path.join(self.dest, os.path.basename(filepath))
            try:
                shutil.copyfile(filepath, dstpath)
            except OSError:
                pass
        self.done.emit()


class MeteorDetectWorker(Worker):

    updateContext = Signal(str, tuple, list, list)

    def __init__(self, filelist: list[str], config: Config, parent=None):
        super().__init__(parent)
        self.filelist = filelist
        self.config = config
        self.detected_list = []

    @Slot()
    def run(self):
        self.initializeProgress.emit(0, len(self.filelist))
        for i, filepath in enumerate(self.filelist, 1):
            self.updateProgress.emit(i)
            if not os.path.exists(filepath):
                continue
            try:
                lines, contours, shape = detect_meteor(
                    filepath,
                    input_threshold=self.config.input_threshold,
                    input_maxvalue=self.config.input_maxvalue,
                    area_threshold=self.config.area_threshold,
                    buffer_ratio=self.config.buffer_ratio,
                    line_threshold=self.config.line_threshold
                )
                self.updateContext.emit(filepath, shape, contours, lines)
            except:
                buf = io.StringIO()
                traceback.print_exc(file=buf)
                buf.seek(0)
                message = buf.read()
                self.error.emit(message)
            if lines is not None:
                self.detected_list.append(filepath)
        self.done.emit()
