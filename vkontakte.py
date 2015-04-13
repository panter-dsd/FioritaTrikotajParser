# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

import json
import re

from PyQt4 import QtCore, QtGui
import vk
import requests


class Vkontakte(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_auth = False

        self._image_data = bytes()
        self._image = None

        self._group_edit = QtGui.QComboBox(parent)
        self._group_edit.activated.connect(self._on_group_changed)
        self._group_edit.activated.connect(lambda: self.set_upload_enabled())

        self._album_edit = QtGui.QComboBox(parent)
        self._album_edit.activated.connect(lambda: self.set_upload_enabled())

        self._upload_action = QtGui.QAction("Upload", parent)

    def group_edit(self):
        return self._group_edit

    def album_edit(self):
        return self._album_edit

    def upload_action(self):
        return self._upload_action

    def comment(self):
        return self._comment

    def set_comment(self, text: str):
        self._comment = text

    def image(self):
        return self._image_data

    def set_image(self, image: bytes):
        self._image_data = image

    def set_upload_enabled(self, is_enabled=True):
        self._upload_action.setEnabled(
            (
                is_enabled
                and (self._group_edit.currentIndex() >= 0)
                and (self._album_edit.currentIndex() >= 0)
            )
        )

    @staticmethod
    def auth_url():
        client_id = "4856961"
        scopes = "photos,friends,groups,stats"

        return QtCore.QUrl("https://oauth.vk.com/authorize?"
                           + "client_id=" + client_id
                           + "&scope=" + scopes
                           + "&redirect_uri=https://oauth.vk.com/blank.html"
                           + "&display=page"
                           + "&v=5.0"
                           + "&response_type=token")

    def is_auth(self):
        return self._is_auth

    def try_read_token(self, url: str) -> bool:
        token = re.findall("access_token=(\w+)", url)
        if token:
            self._connect_to_vk(token)
            self._is_auth = True

        return self._is_auth

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

    def upload_photo_to_selected_album(self):
        upload_url = self._get_upload_url()
        if upload_url:
            params = self._upload_photo(upload_url)
            print(params)
            self._vkapi.photos.save(album_id=self._album_id(),
                                    group_id=self._group_id(),
                                    server=params["server"],
                                    photos_list=params["photos_list"],
                                    hash=params["hash"],
                                    caption=self._comment)


    def _upload_photo(self, url):
        response = requests.post(url, files={
            'file': ("image.jpg", self._image_data)})
        return json.loads(response.text)
