# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

import urllib

from PyQt4 import QtCore, QtGui, QtWebKit

from fiorita_trikotaj_parser import FioritaTrikotajParser
from love_bunny_parser import LoveBunnyParser
from magok_parser import MagokParser
from giftman_parser import GiftmanParser
from sima_land_parser import SimaLandParser
from magdayana_parser import MagdayanaParser
from vkontakte import Vkontakte
from upload_dialog import UploadDialog
from settings_dialog import SettingsDialog
from application_settings import ApplicationSettings


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__(None)

        self.setWindowTitle("Joint purchases assistant")

        self._application_settings = ApplicationSettings()

        self._web_view = QtWebKit.QWebView(self)

        self._url_edit = QtGui.QLineEdit(self)
        self._url_edit.returnPressed.connect(
            lambda: self._web_view.setUrl(
                QtCore.QUrl.fromUserInput(self._url_edit.text())
            )
        )

        self._web_view.loadStarted.connect(self._on_page_load_started)
        self._web_view.loadFinished.connect(self._on_page_load_finished)

        self._load_progress = QtGui.QProgressBar()
        self._load_progress.setVisible(False)
        self._load_progress.setRange(0, 100)
        self._web_view.loadProgress.connect(
            self._load_progress.setValue
        )

        self._vk = Vkontakte(self)
        self._web_view.setUrl(QtCore.QUrl(self._vk.auth_url()))

        right_layout = QtGui.QVBoxLayout()
        right_layout.addWidget(self._web_view)
        right_layout.addWidget(self._load_progress)

        central_widget = QtGui.QWidget(self)
        central_widget.setLayout(right_layout)

        self.setCentralWidget(central_widget)

        self._parsers = [
            FioritaTrikotajParser(),
            LoveBunnyParser(),
            MagokParser(),
            GiftmanParser(),
            SimaLandParser(),
            MagdayanaParser()
        ]

        self._init_main_menu()
        self._init_browser_toolbar()
        self._init_vk_toolbar()

    def _init_main_menu(self):
        self._main_menu = QtGui.QMenuBar(self)
        self.setMenuBar(self._main_menu)

        self._main_menu.addMenu(self._make_presets_menu())
        self._main_menu.addMenu(self._make_tools_menu())

    def _make_presets_menu(self):
        menu = QtGui.QMenu("Presets", self)

        for parser in self._parsers:
            action = menu.addAction(parser.name())
            action.setProperty("url", parser.main_url())

            action.triggered.connect(
                lambda: self._web_view.setUrl(
                    QtCore.QUrl(self.sender().property("url"))
                )
            )

        return menu

    def _make_tools_menu(self):
        menu = QtGui.QMenu("Tools", self)

        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self._settings)

        return menu

    def _init_browser_toolbar(self):
        self._browser_toolbar = QtGui.QToolBar("Browser bar", self)
        self.addToolBar(self._browser_toolbar)
        self.addToolBarBreak()

        self._browser_toolbar.addActions(
            [
                self._web_view.page().action(QtWebKit.QWebPage.Back),
                self._web_view.page().action(QtWebKit.QWebPage.Stop)
            ]
        )

        self._browser_toolbar.addWidget(self._url_edit)

    def _init_vk_toolbar(self):
        self._vk_toolbar = QtGui.QToolBar("VK toolbar", self)
        self.addToolBar(self._vk_toolbar)

        self._vk_toolbar.addWidget(QtGui.QLabel("Group", self))
        self._vk_toolbar.addWidget(self._vk.group_edit())
        self._vk.group_edit().setSizePolicy(QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Preferred)
        self._vk_toolbar.addSeparator()

        self._vk_toolbar.addWidget(QtGui.QLabel("Album", self))
        self._vk_toolbar.addWidget(self._vk.album_edit())
        self._vk.album_edit().setSizePolicy(QtGui.QSizePolicy.Expanding,
                                            QtGui.QSizePolicy.Preferred)
        self._vk_toolbar.addSeparator()

        upload_action = self._vk.upload_action()
        upload_action.triggered.connect(self._upload)
        self._vk_toolbar.addAction(upload_action)

    def _upload(self):
        dialog = UploadDialog(self)
        dialog.set_comment(self._vk.comment())
        dialog.set_image(self._vk.image())

        if dialog.exec():
            self._vk.set_comment(dialog.comment())
            self._vk.set_image(dialog.image())
            try:
                self._vk.upload_photo_to_selected_album()
            except Exception:
                QtGui.QMessageBox.critical(
                    self,
                    "VK",
                    "Upload timeout error",
                )
                QtCore.QTimer.singleShot(0, self._upload)

    def __update_url_edit(self):
        url = self._web_view.url().toString()
        if "oauth.vk.com" in url:
            self._url_edit.clear()
        else:
            self._url_edit.setText(url)

    def _on_page_load_started(self):
        self.__update_url_edit()
        self._url_edit.setEnabled(False)
        self._load_progress.setVisible(True)
        self._vk.set_upload_enabled(False)

    def _on_page_load_finished(self):
        self._url_edit.setEnabled(True)
        self._load_progress.setVisible(False)

        url = self._web_view.url().toString()
        self.__update_url_edit()

        if not self._vk.is_auth():
            self._try_set_login()
            if self._vk.try_read_token(url):
                self._web_view.setUrl(QtCore.QUrl())
                self._url_edit.clear()

        self.work(url)
        self._vk.set_upload_enabled(True)

    def work(self, url: str):
        if self._parsers[0].can_parse(url):
            self._work_fiorita()

        if self._parsers[1].can_parse(url):
            self._work_love_bunny()

        if self._parsers[2].can_parse(url):
            self._work_magok()

        if self._parsers[3].can_parse(url):
            self._work_giftman()

        if self._parsers[4].can_parse(url):
            self._work_sima_land()

        if self._parsers[5].can_parse(url):
            self._work_magdayana()

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

        image_url = page_parser.extract_main_image_url()
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

        image_url = page_parser.extract_main_image_url()
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
            comment.append("Минимум: %s шт" % minimum_order_quantity)
        self._vk.set_comment("\n".join(comment))

        image_url = page_parser.extract_main_image_url()
        if image_url:
            self._download_image(image_url)

    def _work_giftman(self):
        page_parser = self._parsers[3]
        page_parser.set_page_url(self._web_view.url().toString())
        page_parser.set_page_source(self._web_view.page().mainFrame().toHtml())

        comment = []
        comment.append(page_parser.page_url())
        comment.append(page_parser.extract_name())

        comment.append("Цена: %s р." % page_parser.extract_price())

        self._vk.set_comment("\n".join(comment))

        image_url = page_parser.extract_main_image_url()
        if image_url:
            self._download_image(image_url)

    def _work_sima_land(self):
        page_parser = self._parsers[4]
        page_parser.set_page_url(self._web_view.url().toString())
        page_parser.set_page_source(self._web_view.page().mainFrame().toHtml())

        comment = []
        comment.append(page_parser.page_url())
        comment.append(page_parser.extract_name())

        comment.append("Цена: %s р." % page_parser.extract_price())

        minimum_order_quantity = page_parser.extract_minimum_order_quantity()
        if minimum_order_quantity > 1:
            comment.append("Минимум: %s шт" % minimum_order_quantity)

        self._vk.set_comment("\n".join(comment))

        image_url = page_parser.extract_main_image_url()
        if image_url:
            self._download_image(image_url)

    def _work_magdayana(self):
        page_parser = self._parsers[5]
        page_parser.set_page_url(self._web_view.url().toString())
        page_parser.set_page_source(self._web_view.page().mainFrame().toHtml())

        comment = []
        comment.append(page_parser.extract_name())

        comment.append("Цена: %s р." % page_parser.extract_price())

        sizes = page_parser.extract_sizes()
        if sizes:
            comment.append("Размер: " + ",".join(sizes))

        self._vk.set_comment("\n".join(comment))

        image_url = page_parser.extract_main_image_url()
        if image_url:
            self._download_image(image_url)

    def _download_image(self, url):
        with urllib.request.urlopen(url) as f:
            image_data = f.read()
            if image_data:
                self._vk.set_image(image_data)

    def _settings(self):
        dialog = SettingsDialog(self._application_settings, self)
        dialog.exec()

    def _try_set_login(self):
        url = "https://oauth.vk.com/authorize"
        if self._web_view.url().toString().startswith(url):
            current_frame = self._web_view.page().mainFrame()
            email_element = current_frame.findFirstElement("input[name=email]")
            email_element.setAttribute("value",
                                       self._application_settings.login())
            pass_element = current_frame.findFirstElement("input[name=pass]")
            pass_element.setAttribute("value",
                                      self._application_settings.password())