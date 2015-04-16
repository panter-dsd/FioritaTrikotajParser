# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"


from PyQt4 import QtCore, QtGui
from application_settings import ApplicationSettings

class SettingsDialog(QtGui.QDialog):
    def __init__(self, settings: ApplicationSettings, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")

        self._settings = settings

        self._login_edit = QtGui.QLineEdit(self._settings.login(), self)

        self._password_edit = QtGui.QLineEdit(self._settings.password(), self)
        self._password_edit.setEchoMode(QtGui.QLineEdit.Password)

        self._button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )

        self._button_box.accepted.connect(self._save_settings)
        self._button_box.rejected.connect(self.reject)

        login_password_layout = QtGui.QGridLayout()
        login_password_layout.addWidget(QtGui.QLabel("Login"), 0, 0)
        login_password_layout.addWidget(self._login_edit, 0, 1)
        login_password_layout.addWidget(QtGui.QLabel("Password"), 1, 0)
        login_password_layout.addWidget(self._password_edit, 1, 1)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(login_password_layout)
        main_layout.addWidget(self._button_box)
        self.setLayout(main_layout)

    def _save_settings(self):
        self._settings.set_login(self._login_edit.text())
        self._settings.set_password(self._password_edit.text())
        self._settings.save()
        self.accept()