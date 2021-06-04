from PySide2.QtCore import QEvent
from PySide2.QtCore import QFileInfo
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QListView


class JPEGFilesDragAndDropFilter(QObject):
    """
    JPEGファイルドラッグ＆ドロップイベントフィルター
    """

    def eventFilter(self, obj: QListView, event: QEvent):
        """
        QObject::installEventFilter で設定したオブジェクトのイベントが流れてくる
        """
        if event.type() == QEvent.DragEnter:
            mimeData = event.mimeData()
            if not mimeData.hasUrls():
                event.ignore()
                return True
            for url in mimeData.urls():
                if not url.isLocalFile():
                    continue
                info = QFileInfo(url.toLocalFile())
                if info.suffix().lower() in ["jpg", "jpeg"]:
                    event.accept()
                    return True
            event.ignore()
            return True
        elif event.type() == QEvent.Drop:
            mimeData = event.mimeData()
            if not mimeData.hasUrls():
                return True
            model = obj.model()
            model.addUrls(mimeData.urls())
            return True
        return super().eventFilter(obj, event)
