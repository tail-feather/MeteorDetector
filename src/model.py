import typing

import cv2

from PySide2.QtCore import Qt
from PySide2.QtCore import QAbstractItemModel
from PySide2.QtCore import QFileInfo
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import QObject
from PySide2.QtCore import QUrl
from PySide2.QtGui import QColor
from PySide2.QtGui import QPalette


class FetchObject:
    """
    FetchObject
    ===========
    implementation of fetchMore
    """

    # size per fetch
    FETCHSIZE = 250

    def __init__(self, size: int):
        """
        :param size: maximum size
        """
        self.size = size

    def canFetchMore(self) -> bool:
        """
        :return: status of can fetch more
        """
        return self.fetched < self.size

    def extend(self, size: int) -> None:
        """
        :param size: extend size
        """
        self.size += size

    def fetchSize(self, more: int=FETCHSIZE) -> int:
        """
        :param more: size of fetch
        :return: size of after fetched
        """
        remainder = self.size - self.fetched
        return min(more, remainder)

    def fetchMore(self, more: int=FETCHSIZE) -> None:
        """
        :param more: size of fetch
        """
        itemsToFetch = self.fetchSize(more)
        self.fetched += itemsToFetch

    @property
    def fetched(self) -> int:
        """
        :return: fetched size
        """
        return self._fetched

    @fetched.setter
    def fetched(self, fetched: int) -> None:
        """
        :param fetched: fetched size
        """
        self._fetched = min(fetched, self.size)

    @property
    def size(self) -> int:
        """
        :return: maximum size
        """
        return self._size

    @size.setter
    def size(self, size: int) -> None:
        """
        :param size: maximum size
        """
        self._size = size
        self.fetched = 0


class AbstractItemModel(QAbstractItemModel):
    def __init__(self, parent: QObject=None):
        """
        :param parent: parent QObject
        """
        super().__init__(parent)
        self.row = None
        self.column = None

    def canFetchMore(self, parent: QModelIndex=QModelIndex()) -> bool:
        """
        :param parent: parent index
        :return: status of can fetch more
        """
        # check if source has been set
        if self.row is None or self.column is None:
            return False
        return self.row.canFetchMore() or self.column.canFetchMore()

    def fetchMore(self, parent: QModelIndex=QModelIndex()) -> None:
        """
        :param parent: parent index
        """
        # check if source has been set
        if self.row is None or self.column is None:
            return
        # row side
        if self.row.canFetchMore():
            itemsToFetch = self.row.fetchSize()
            self.beginInsertRows(QModelIndex(),
                                 self.row.fetched,
                                 self.row.fetched + itemsToFetch - 1)
            self.row.fetchMore(itemsToFetch)
            self.endInsertRows()
        # column side
        if self.column.canFetchMore():
            itemsToFetch = self.column.fetchSize()
            self.beginInsertColumns(QModelIndex(),
                                    self.column.fetched,
                                    self.column.fetched + itemsToFetch - 1)
            self.column.fetchMore(itemsToFetch)
            self.endInsertColumns()

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def columnCount(self, parent: QModelIndex=QModelIndex()) -> int:
        """
        :param parent: parent index
        :return: size of column
        """
        if self.column is None:
            return 0
        return self.column.fetched

    def rowCount(self, parent: QModelIndex=QModelIndex()) -> int:
        """
        :param parent: parent index
        :return: size of row
        """
        if self.row is None:
            return 0
        return self.row.fetched

    def realColumnCount(self, parent: QModelIndex=QModelIndex()) -> int:
        """
        :param parent: parent index
        :return: size of maximum column
        """
        if self.column is None:
            return 0
        return self.column.size

    def realRowCount(self, parent: QModelIndex=QModelIndex()) -> int:
        """
        :param parent: parent index
        :return: size of maximum row
        """
        if self.row is None:
            return 0
        return self.row.size

    def setItemSize(self, row: int, column: int) -> None:
        """
        .. note::
           must be call between beginResetModel() and endResetModel()
        :param row: size of maximum row
        :param column: size of maximum column
        """
        self.row = FetchObject(row)
        self.column = FetchObject(column)

    def resetFetch(self) -> None:
        """
        .. note::
           must be call between beginResetModel() and endResetModel()
        """
        self.row = None
        self.column = None



HIGHLIGHT_COLOR_LIGHT = 0xbef5cb
HIGHLIGHT_COLOR_DARK = 0x3fb950
DEFAULT_COLOR = 0xffffff


class JPEGFileListModel(AbstractItemModel):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self._fileList = []
        self.highlighted = set()
        self.context = {}
        self.column = FetchObject(3)
        self.palette = QPalette()
        self.isLightMode = self.palette.window().color().lightness() > 127

    def fileList(self) -> list[str]:
        return self._fileList

    def setFileList(self, fileList: list[str]) -> None:
        self.beginResetModel()
        self._fileList = fileList
        self.setItemSize(len(self._fileList), 3)
        self.endResetModel()

    def addUrls(self, urls: list[QUrl]) -> None:
        temp = []
        for url in urls:
            filepath = url.toLocalFile()
            info = QFileInfo(filepath)
            if info.suffix().lower() not in ["jpg", "jpeg"]:
                # not JPEG
                continue
            temp.append(filepath)
        if not temp:
            # no JPEG
            return
        self.addFiles(temp)

    def addFiles(self, files: list[str]) -> None:
        fileList = self.fileList()
        row = self.rowCount()
        temp = []
        for filepath in files:
            if filepath in fileList:
                # already exist
                continue
            temp.append(filepath)

        if not temp:
            return

        head = len(self._fileList)
        last = head + len(temp) - 1
        self.beginInsertRows(QModelIndex(), head, last)
        self._fileList.extend(temp)
        if self.row is None:
            self.row = FetchObject(len(temp))
        else:
            self.row.extend(len(temp))
        self.endInsertRows()

    def rowCount(self, parent: QModelIndex=QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return super().rowCount(parent)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return super().headerData(section, orientation, role)
        if section == 0:
            return self.tr("FilePath")
        elif section == 1:
            return self.tr("FilledRatio")
        elif section == 2:
            return self.tr("LineCount")
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        row = index.row()
        if row >= len(self._fileList):
            return super().data(index, role)
        if role == Qt.BackgroundRole:
            if row < 0 or row >= len(self._fileList):
                # return default
                return super().data(index, role)
            filepath = self._fileList[row]
            if filepath in self.highlighted:
                if self.isLightMode:
                    return QColor(HIGHLIGHT_COLOR_LIGHT)
                else:
                    return QColor(HIGHLIGHT_COLOR_DARK)
            else:
                return self.palette.base().color()
        elif role == Qt.DisplayRole:
            column = index.column()
            filepath = self._fileList[row]
            if column == 0:
                # FilePath
                info = QFileInfo(filepath)
                return info.fileName()
            elif column == 1:
                # FilledRatio
                if filepath not in self.context:
                    return ""
                height, width = self.context[filepath][0]
                contours = self.context[filepath][1]
                area = width * height
                filled = sum(cv2.contourArea(x) / area for x in contours)
                return "{:0.4f}".format(filled)
            elif index.column() == 2:
                # LineCount
                if filepath not in self.context:
                    return ""
                lines = self.context[filepath][2]
                if lines is None:
                    return ""
                return str(len(lines))
        return None

    def at(self, index: QModelIndex):
        if index.column() != 0:
            return None
        return self.fileList()[index.row()]

    def clear(self):
        self.setFileList([])
        self.clearHighlight()

    def clearHighlight(self):
        self.highlighted = set()
        self.context = {}
        fileList = self.fileList()
        if fileList:
            begin = self.index(0, 0)
            end = self.index(len(fileList), 0)
            self.dataChanged.emit(begin, end, [Qt.BackgroundRole])

    def updateContext(self, filepath: str, shape: tuple, filled: list, lines: list):
        print(filepath, shape)
        self.context[filepath] = (shape, filled, lines)
        if lines:
            self.highlighted.add(filepath)
        else:
            self.highlighted.discard(filepath)
        self._updateContext(filepath)

    def getContext(self, filepath: str) -> typing.Optional[tuple[tuple, list, list]]:
        if filepath not in self.context:
            return None
        return self.context[filepath]

    def _updateContext(self, filepath: str):
        fileList = self.fileList()
        if filepath not in fileList:
            return
        i = fileList.index(filepath)
        begin = self.index(i, 0)
        end = self.index(i, 2)
        role = [Qt.DisplayRole, Qt.BackgroundRole]
        self.dataChanged.emit(begin, end, role)

    def highlight(self, filepath: str):
        self.highlighted.add(filepath)
        self._updateHighlight(filepath, True)

    def unhighlight(self, filepath: str):
        self.highlighted.discard(filepath)
        self._updateHighlight(filepath, False)

    def _updateHighlight(self, filepath: str, highlight: bool):
        fileList = self.fileList()
        if filepath not in fileList:
            return
        i = fileList.index(filepath)
        begin = self.index(i, 0)
        end = self.index(i, 2)
        self.dataChanged.emit(begin, end, [Qt.BackgroundRole])
