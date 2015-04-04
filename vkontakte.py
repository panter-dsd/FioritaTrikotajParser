# -*- coding: utf-8 -*-
import json

__author__ = 'konnov@simicon.com'

from PyQt4 import QtGui
import vk
import requests
import re
import json


class Vkontakte(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._vkapi = vk.API(app_id="4856961",
                             user_login="xxx",
                             user_password="xxx",
                             access_token="dPwY2jTJ5Tpwe4ipMch4",
                             scope="photos,friends,groups,stats,wall,messages,ads,offline")

        self._groups = QtGui.QComboBox(self)
        self._groups.activated.connect(self._on_group_changed)

        self._albums = QtGui.QComboBox(self)
        self._albums.activated.connect(self._on_album_changed)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._groups)
        layout.addWidget(self._albums)

        self.setLayout(layout)

        self._load_groups()

    def _load_groups(self):
        value = self._vkapi.groups.get(extended=1)
        for item in value["items"]:
            self._groups.addItem(item["name"], item["id"])

        self._groups.setCurrentIndex(-1)

    def _on_group_changed(self, index):
        self._albums.clear()

        group = self._groups.itemData(index)
        albums = self._vkapi.photos.getAlbums(group_id=group)
        for album in albums["items"]:
            self._albums.addItem(album["title"], album["id"])

        self._albums.setCurrentIndex(-1)

    def _on_album_changed(self, index):
        album = self._albums.itemData(index)
        group = self._groups.itemData(index)
        try:
            upload_url = self._vkapi.photos.getUploadServer(album_id=album, group_id=group)["upload_url"]
        except:
            upload_url = str()
        print(upload_url)
        if upload_url:
            params = self._upload_photo(upload_url)
            self._vkapi.photos.save(album_id=album,
                                    group_id=group,
                                    server=params["server"],
                                    photos_list=params["photos_list"],
                                    hash=params["hash"],
                                    caption="my_first_photo")

    def _upload_photo(self, url):
        response = requests.post(url,
                                 files={'file': open('/home/panter/qwr1.png', 'rb')})

        return json.loads(response.text)
