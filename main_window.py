# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

import urllib

from PyQt4 import QtCore, QtGui, QtWebKit

from presets_widget import PresetsWidget
from fiorita_trikotaj_parser import FioritaTrikotajParser
from love_bunny_parser import LoveBunnyParser
from vkontakte import Vkontakte


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__(None)

        self._web_view = QtWebKit.QWebView(self)

        self._url_edit = QtGui.QLineEdit(self)
        self._url_edit.returnPressed.connect(
            lambda: self._web_view.setUrl(
                QtCore.QUrl.fromUserInput(self._url_edit.text())
            )
        )

        self._web_view.loadStarted.connect(self._on_page_load_started)
        self._web_view.loadFinished.connect(self._on_page_load_finished)

        self._presets_widget = PresetsWidget(self)
        self._presets_widget.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum
        )
        self._presets_widget.activated.connect(
            lambda url: self._web_view.setUrl(
                QtCore.QUrl(url)
            )
        )

        self._load_progress = QtGui.QProgressBar()
        self._load_progress.setVisible(False)
        self._load_progress.setRange(0, 100)
        self._web_view.loadProgress.connect(
            self._load_progress.setValue
        )

        self._vk = Vkontakte(self)
        self._vk.setMaximumWidth(200)

        left_layout = QtGui.QVBoxLayout()
        left_layout.addWidget(self._vk)

        right_layout = QtGui.QVBoxLayout()
        right_layout.addWidget(self._url_edit)
        right_layout.addWidget(self._presets_widget)
        right_layout.addWidget(self._web_view)
        right_layout.addWidget(self._load_progress)

        layout = QtGui.QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        central_widget = QtGui.QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def _on_page_load_started(self):
        self._url_edit.setText(self._web_view.url().toString())
        self._url_edit.setEnabled(False)
        self._load_progress.setVisible(True)

    def _on_page_load_finished(self):
        self._url_edit.setEnabled(True)
        self._load_progress.setVisible(False)

        self.work(self._web_view.url().toString())

    def work(self, url: str):
        if "fiorita-trikotaj.ru" in url:
            self._work_fiorita()

        if "optom.love-bunny.ru" in url:
            self._work_love_bunny()

    def _work_fiorita(self):
        page_parser = FioritaTrikotajParser()
        page_parser.set_page_source(
            self._web_view.page().mainFrame().toHtml()
        )

        comment = []
        comment.append(self._web_view.url().toString())

        comment.append(page_parser.extract_name())
        comment.append("Состав: " + page_parser.extract_description())

        color_string = ", ".join(page_parser.extract_colors())
        comment.append("Цвет: " + color_string)

        sizes_string = ", ".join(page_parser.extract_sizes())
        comment.append("Размер: " + sizes_string)

        comment.append("Цена: "
                       + page_parser.extract_price()
                       + "р.")
        self._vk.set_comment("\n".join(comment))

    def _work_love_bunny(self):
        love_bunny = LoveBunnyParser()
        love_bunny.set_page_source(self._web_view.page().mainFrame().toHtml())

        comment = []
        comment.append(love_bunny.extract_name())

        sizes_string = ", ".join(love_bunny.extract_sizes())
        comment.append("Размер: " + sizes_string)

        comment.append("Цена: "
                       + love_bunny.extract_price()
                       + "р.")
        self._vk.set_comment("\n".join(comment))

        with urllib.request.urlopen(love_bunny.extract_image_url()) as f:
            image_data = f.read()
            if image_data:
                self._vk.set_image(image_data)