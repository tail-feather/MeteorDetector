import json
import typing

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QAbstractButton
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QDialogButtonBox
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QWidget

from .ui.configdialog import Ui_ConfigDialog


class Config:
    def __init__(self, input_threshold: float = 127,
                 area_threshold: float = 0.0001, buffer_ratio: float = 0.01,
                 line_threshold: float = 100):
        self.input_threshold = input_threshold
        self.input_maxvalue = 255
        self.area_threshold = area_threshold
        self.buffer_ratio = buffer_ratio
        self.line_threshold = line_threshold

    def clone(self):
        return Config(
            input_threshold=self.input_threshold,
            area_threshold=self.area_threshold,
            buffer_ratio=self.buffer_ratio,
            line_threshold=self.line_threshold
        )

    def load(self, filepath: str):
        data = json.load(open(filepath))
        if type(data) is not dict:
            return
        self.input_threshold = data.get("input", {}).get("threshold", 127)
        self.input_maxvalue = data.get("input", {}).get("maxvalue", 255)
        self.area_threshold = data.get("area", {}).get("threshold", 0.0001)
        self.buffer_ratio = data.get("area", {}).get("buffer", 0.01)
        self.line_threshold = data.get("line", {}).get("threshold", 100)

    def save(self, filepath: str):
        config = {
            "input": {
                "threshold": self.input_threshold,
                "maxvalue": self.input_maxvalue,
            },
            "area": {
                "threshold": self.area_threshold,
                "buffer": self.buffer_ratio,
            },
            "line": {
                "threshold": self.line_threshold,
            },
        }
        with open(filepath, "w") as fp:
            json.dump(config, fp)

    def reset(self):
        init = Config()
        self.input_threshold = init.input_threshold
        self.input_maxvalue = init.input_maxvalue
        self.area_threshold = init.area_threshold
        self.buffer_ratio = init.buffer_ratio
        self.line_threshold = init.line_threshold


class ConfigDialog(QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)
        self.saveButton = QPushButton(self.tr("Save"))
        self.loadButton = QPushButton(self.tr("Load"))
        self.ui.buttonBox.addButton(self.saveButton, QDialogButtonBox.ActionRole)
        self.ui.buttonBox.addButton(self.loadButton, QDialogButtonBox.ActionRole)
        resetButton = self.ui.buttonBox.button(QDialogButtonBox.Reset)
        self.saveButton.clicked.connect(self.saveConfig)
        self.loadButton.clicked.connect(self.loadConfig)
        resetButton.clicked.connect(self.reset)
        self.config = Config()
        self.updateUi()

    def updateUi(self, config: typing.Optional[Config]=None):
        """
        Config -> UI
        """
        if config is None:
            config = self.config
        self.ui.spinBox_threshold_threshold.setValue(config.input_threshold)
        self.ui.spinBox_threshold_maxvalue.setValue(config.input_maxvalue)
        self.ui.doubleSpinBox_fillarea_areathreshold.setValue(config.area_threshold * 100)
        self.ui.doubleSpinBox_fillarea_fillbuffer.setValue(config.buffer_ratio * 100)
        self.ui.doubleSpinBox_meteordetection_linethreshold.setValue(config.line_threshold)

    def updateConfig(self):
        """
        UI -> Config
        """
        self.config.input_threshold = self.ui.spinBox_threshold_threshold.value()
        self.config.input_maxvalue = self.ui.spinBox_threshold_maxvalue.value()
        self.config.area_threshold = self.ui.doubleSpinBox_fillarea_areathreshold.value() / 100  # % -> ratio
        self.config.buffer_ratio = self.ui.doubleSpinBox_fillarea_fillbuffer.value() / 100  # % -> ratio
        self.config.line_threshold = self.ui.doubleSpinBox_meteordetection_linethreshold.value()

    def getConfig(self):
        return self.config

    @Slot()
    def loadConfig(self):
        filepath, _ = QFileDialog.getOpenFileName(self, self.tr("Open config"), "", self.tr("Config.json(*.json)"))
        if not filepath:
            return
        self.config.load(filepath)
        self.updateUi()

    @Slot()
    def saveConfig(self):
        filepath, _ = QFileDialog.getSaveFileName(self, self.tr("Save config"), "", self.tr("Config.json(*.json)"))
        if not filepath:
            return
        if not filepath.lower().endswith(".json"):
            filepath += ".json"
        self.updateConfig()
        self.config.save(filepath)
        QMessageBox.information(self, self.tr("Saved"), self.tr("Saved: {}").format(filepath))

    @Slot()
    def reset(self):
        self.updateUi(Config())
