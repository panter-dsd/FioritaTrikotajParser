# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

import sys

from PyQt4 import QtGui

from main_window import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()

if __name__ == "__main__":
    main()