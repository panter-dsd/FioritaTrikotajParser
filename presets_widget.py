# -*- coding: utf-8 -*-
__author__ = 'konnov@simicon.com'

from PyQt4 import QtCore, QtGui


class PresetsWidget(QtGui.QWidget):
    activated = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._presets = [
            QtGui.QCommandLinkButton(
                "Love bunny", "http://optom.love-bunny.ru/", self
            ),
            QtGui.QCommandLinkButton(
                "Fiorita trikotaj", "http://fiorita-trikotaj.ru/", self
            )
        ]

        for button in self._presets:
            button.clicked.connect(
                lambda: self.activated.emit(self.sender().description())
            )

        layout = QtGui.QHBoxLayout()
        for button in self._presets:
            layout.addWidget(button)

        self.setLayout(layout)