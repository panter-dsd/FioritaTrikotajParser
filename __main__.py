# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

import sys

from PyQt4 import QtGui, QtWebKit, QtCore
from main_window import MainWindow
from page_parser import PageParser
from love_bunny_parser import LoveBunnyParser


def test_page_parser():
    pp = PageParser("http://fiorita-trikotaj.ru/bluzki-i-vodolazki/vodolazka-FV-2042-babochka-106")
    print(pp.extract_name())
    print(pp.extract_colors())


def test_love_bunny_parser():
    lbp = LoveBunnyParser(str())
    with open("/var/tmp/untitled.html", "r") as f:
        lbp.set_page_source(f.read())
    print(lbp.extract_name())
    print(lbp.extract_sizes())
    print(lbp.extract_price())


def main():
    app = QtGui.QApplication(sys.argv)
    #test_love_bunny_parser()
    #return 0
    window = MainWindow()
    window.show()

    return app.exec()

if __name__ == "__main__":
    main()