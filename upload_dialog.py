# -*- coding: utf-8 -*-

__author__ = "panter.dsd@gmail.com"

from PyQt4 import QtCore, QtGui


class UploadDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._comment_edit = QtGui.QPlainTextEdit(self)

        self._image_preview = QtGui.QLabel(self)

        self._button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )

        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self._comment_edit)
        top_layout.addWidget(self._image_preview)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self._button_box)
        self.setLayout(layout)

    def comment(self):
        return self._comment_edit.toPlainText()

    def set_comment(self, comment: str):
        self._comment_edit.setPlainText(comment)

    def image(self):
        return self._image

    def set_image(self, image_data: bytes):
        self._image = image_data
        image = QtGui.QImage()

        if image.loadFromData(image_data, "JPG"):
            image = image.scaledToWidth(
                100, QtCore.Qt.SmoothTransformation
            )
            self._image_preview.setPixmap(QtGui.QPixmap.fromImage(image))