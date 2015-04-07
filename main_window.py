# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

import urllib

from PyQt4 import QtCore, QtGui, QtWebKit

from presets_widget import PresetsWidget
from fiorita_trikotaj_parser import FioritaTrikotajParser
from love_bunny_parser import LoveBunnyParser
from magok_parser import MagokParser
from vkontakte import Vkontakte


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__(None)

        self._web_view = QtWebKit.QWebView(self)

        self._url_edit = QtGui.QLineEdit(self)
        self._url_edit.setText(
            "http://optom.love-bunny.ru/shop/2784/desc/kurtka-stegannaja-krasnaja")
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
        self._web_view.setUrl(QtCore.QUrl(self._vk.auth_url()))

        right_layout = QtGui.QVBoxLayout()
        right_layout.addWidget(self._url_edit)
        right_layout.addWidget(self._presets_widget)
        right_layout.addWidget(self._web_view)
        right_layout.addWidget(self._load_progress)

        self._right_widget = QtGui.QWidget(self)
        self._right_widget.setLayout(right_layout)

        self._splitter = QtGui.QSplitter(self)
        self._splitter.addWidget(self._vk)
        self._splitter.addWidget(self._right_widget)

        self.setCentralWidget(self._splitter)

        self._parsers = [
            FioritaTrikotajParser(),
            LoveBunnyParser(),
            MagokParser()
        ]

    def _on_page_load_started(self):
        self._url_edit.setText(self._web_view.url().toString())
        self._url_edit.setEnabled(False)
        self._load_progress.setVisible(True)

    def _on_page_load_finished(self):
        self._url_edit.setEnabled(True)
        self._load_progress.setVisible(False)

        url = self._web_view.url().toString()
        self._url_edit.setText(url)

        if not self._vk.is_auth():
            if self._vk.try_read_token(url):
                self._web_view.setUrl(QtCore.QUrl())
                self._url_edit.clear()

        self.work(url)

    def work(self, url: str):
        if self._parsers[0].can_parse(url):
            self._work_fiorita()

        if self._parsers[1].can_parse(url):
            self._work_love_bunny()

        if self._parsers[2].can_parse(url):
            self._work_magok()

    def _work_fiorita(self):
        page_parser = self._parsers[0]
        page_parser.set_page_url(self._web_view.url().toString())
        page_parser.set_page_source(
            self._web_view.page().mainFrame().toHtml()
        )

        comment = []
        comment.append(page_parser.page_url())

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

        image_url = page_parser.extract_image_url()
        if image_url:
            self._download_image(image_url)

    def _work_love_bunny(self):
        page_parser = self._parsers[1]
        page_parser.set_page_url(self._web_view.url().toString())
        page_parser.set_page_source(self._web_view.page().mainFrame().toHtml())

        comment = []
        comment.append(page_parser.extract_name())

        sizes_string = ", ".join(page_parser.extract_sizes())
        comment.append("Размер: " + sizes_string)

        comment.append("Цена: "
                       + page_parser.extract_price()
                       + "р.")
        self._vk.set_comment("\n".join(comment))

        image_url = page_parser.extract_image_url()
        if image_url:
            self._download_image(image_url)

    def _work_magok(self):
        page_parser = self._parsers[2]
        page_parser.set_page_url(self._web_view.url().toString())
        page_parser.set_page_source(self._web_view.page().mainFrame().toHtml())

        comment = []
        comment.append(page_parser.page_url())
        comment.append(page_parser.extract_name())

        comment.append("Цена: %s р." % page_parser.extract_price())

        minimum_order_quantity = page_parser.extract_minimum_order_quantity()
        if minimum_order_quantity > 1:
            comment.append("Фасовка: %s шт" % minimum_order_quantity)
        self._vk.set_comment("\n".join(comment))

        image_url = page_parser.extract_image_url()
        if image_url:
            self._download_image(image_url)

    def _download_image(self, url):
        with urllib.request.urlopen(url) as f:
            image_data = f.read()
            if image_data:
                self._vk.set_image(image_data)