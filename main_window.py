# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'


from PyQt4 import QtCore, QtGui

from page_parser import PageParser


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)

        self._paste_button = QtGui.QPushButton("Paste url")
        self._paste_button.clicked.connect(self.on_paste)

        self._url_edit = QtGui.QLineEdit(self)
        self._url_edit.editingFinished.connect(self.work)

        self._text_view = QtGui.QPlainTextEdit(self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._paste_button)
        layout.addWidget(self._url_edit)
        layout.addWidget(self._text_view)

        central_widget = QtGui.QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def on_paste(self):
        self._url_edit.setText(QtGui.QApplication.clipboard().text())
        self.work()

    def work(self):
        page_parser = PageParser(self._url_edit.text())

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