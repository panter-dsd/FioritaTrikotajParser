# -*- coding: utf-8 -*-

__author__ = 'konnov@simicon.com'

import json

from PyQt4 import QtCore, QtGui, QtWebKit
import vk
import requests
import re


class Vkontakte(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._image_data = bytes()

        client_id = "4856961"
        scopes = "photos,friends,groups,stats"

        self._web_view = QtWebKit.QWebView()
        self._web_view.setUrl(
            QtCore.QUrl("https://oauth.vk.com/authorize?"
                        + "client_id=" + client_id
                        + "&scope=" + scopes
                        + "&redirect_uri=https://oauth.vk.com/blank.html"
                        + "&display=page"
                        + "&v=5.0"
                        + "&response_type=token")
        )
        self._web_view.show()
        self._web_view.loadFinished.connect(self._try_read_token)

        self._group_edit = QtGui.QComboBox(self)
        self._group_edit.activated.connect(self._on_group_changed)

        self._album_edit = QtGui.QComboBox(self)

        self._upload_photo_button = QtGui.QPushButton("Upload", self)
        self._upload_photo_button.clicked.connect(self._upload_photo_to_selected_album)

        self._comment_edit = QtGui.QPlainTextEdit(self)

        self._image_preview = QtGui.QLabel(self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._group_edit)
        layout.addWidget(self._album_edit)
        layout.addWidget(self._upload_photo_button)
        layout.addWidget(self._comment_edit)
        layout.addWidget(self._image_preview)

        self.setLayout(layout)

    def set_comment(self, comment: str):
        self._comment_edit.setPlainText(comment)

    def set_image(self, image_data: bytes):
        self._image_data = image_data

        image = QtGui.QImage()
        image.loadFromData(image_data, "JPG")
        image = image.scaledToWidth(
            self._image_preview.width(), QtCore.Qt.SmoothTransformation
        )
        self._image_preview.setPixmap(QtGui.QPixmap.fromImage(image))

    def _try_read_token(self):
        url = self._web_view.url().toString()
        token = re.findall("access_token=(\w+)", url)
        if token:
            self._web_view.hide()
            self._web_view.deleteLater()
            self._connect_to_vk(token)

    def _connect_to_vk(self, token):
        self._vkapi = vk.API(app_id="4856961", access_token=token)
        self._load_groups()

    def _load_groups(self):
        value = self._vkapi.groups.get(extended=1)
        for item in value["items"]:
            self._group_edit.addItem(item["name"], item["id"])

        self._group_edit.setCurrentIndex(-1)

    def _on_group_changed(self, index):
        self._album_edit.clear()

        group = self._group_edit.itemData(index)
        albums = self._vkapi.photos.getAlbums(group_id=group)
        for album in albums["items"]:
            self._album_edit.addItem(album["title"], album["id"])

        self._album_edit.setCurrentIndex(-1)

    def _group_id(self):
        return self._group_edit.itemData(self._group_edit.currentIndex())

    def _album_id(self):
        return self._album_edit.itemData(self._album_edit.currentIndex())

    def _get_upload_url(self):
        upload_url = self._vkapi.photos.getUploadServer(
            album_id=self._album_id(), group_id=self._group_id()
        )["upload_url"]
        print(upload_url)
        return upload_url

    def _upload_photo_to_selected_album(self):
        upload_url = self._get_upload_url()
        if upload_url:
            params = self._upload_photo(upload_url)
            print(params)
            self._vkapi.photos.save(album_id=self._album_id(),
                                    group_id=self._group_id(),
                                    server=params["server"],
                                    photos_list=params["photos_list"],
                                    hash=params["hash"],
                                    caption=self._comment_edit.toPlainText())


    def _upload_photo(self, url):
        response = requests.post(url, files={'file': ("image.jpg", self._image_data)})
        return json.loads(response.text)
