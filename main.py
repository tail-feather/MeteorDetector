#!/usr/bin/env python3

import sys

py_major, py_minor, _, _, _ = sys.version_info
assert (py_major == 3 and py_minor >= 9) or py_major > 3, "Python 3.9+ required"


from PySide2.QtWidgets import QApplication

from src.mainwindow import MainWindow


def main(argv: list[str]) -> int:
    app = QApplication(argv)

    win = MainWindow()
    win.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
