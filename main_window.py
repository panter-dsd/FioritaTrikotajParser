# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'


from PyQt4 import QtCore, QtGui
import urllib

from page_parser import PageParser
from love_bunny_parser import LoveBunnyParser

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)

        self._paste_button = QtGui.QPushButton("Paste url")
        self._paste_button.clicked.connect(self.on_paste)

        self._url_edit = QtGui.QLineEdit(self)
        self._url_edit.editingFinished.connect(self.work)

        self._text_view = QtGui.QPlainTextEdit(self)

        self._image = QtGui.QLabel(self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._paste_button)
        layout.addWidget(self._url_edit)
        layout.addWidget(self._text_view)
        layout.addWidget(self._image)

        central_widget = QtGui.QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self._love_bunny = None

    def on_paste(self):
        self._url_edit.setText(QtGui.QApplication.clipboard().text())
        self.work()

    def work(self):
        url = self._url_edit.text()
        if "fiorita-trikotaj.ru" in url:
            self._work_fiorita(url)

        if "optom.love-bunny.ru" in url:
            self._work_love_bunny(url)

    def _work_fiorita(self, url: str):
        page_parser = PageParser(url)
        self._text_view.clear()
        self._text_view.appendPlainText(page_parser.page_url())
        self._text_view.appendPlainText(page_parser.extract_name())
        self._text_view.appendPlainText("Состав: "
                                        + page_parser.extract_description())

        color_string = ", ".join(page_parser.extract_colors())
        self._text_view.appendPlainText("Цвет: " + color_string)

        sizes_string = ", ".join(page_parser.extract_sizes())
        self._text_view.appendPlainText("Размер: " + sizes_string)

        self._text_view.appendPlainText("Цена: "
                                        + page_parser.extract_price()
                                        + "р.")
        QtGui.QApplication.clipboard().setText(self._text_view.toPlainText())

    def _work_love_bunny(self, url):
        if not self._love_bunny:
            self._love_bunny = LoveBunnyParser(url)
            self._love_bunny.finished.connect(self._parse_love_bunny)
        else:
            self._love_bunny.set_url(url)

    def _parse_love_bunny(self):
        self._text_view.clear()
        self._text_view.appendPlainText(self._love_bunny.page_url())
        self._text_view.appendPlainText(self._love_bunny.extract_name())
        print(self._love_bunny.extract_sizes())
        sizes_string = ", ".join(self._love_bunny.extract_sizes())
        self._text_view.appendPlainText("Размер: " + sizes_string)

        self._text_view.appendPlainText("Цена: "
                                        + self._love_bunny.extract_price()
                                        + "р.")
        QtGui.QApplication.clipboard().setText(self._text_view.toPlainText())

        print("!!!" + self._love_bunny.extract_image_url())
        with urllib.request.urlopen(self._love_bunny.extract_image_url()) as f:
            image_data = f.read()
            if image_data:
                image = QtGui.QImage()
                image.loadFromData(image_data, "JPG")
                QtGui.QApplication.clipboard().setImage(image)
                image = image.scaledToHeight(100, QtCore.Qt.SmoothTransformation)
                self._image.setPixmap(QtGui.QPixmap.fromImage(image))
