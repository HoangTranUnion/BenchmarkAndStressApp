from PyQt5 import QtCore, QtGui, QtWidgets

from src.UI.GeneratedUI import Debug_Dialog
from src.main.MainComponents.LocalStorage import LocalStorage


class Debug(QtWidgets.QDialog, Debug_Dialog.Ui_Dialog):
    def __init__(self, storage: LocalStorage):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.storage = storage
        self.err_ns = self.storage.get_server_down_nameservers()

        for ns in self.err_ns:
            self.textBrowser.append("Cannot connect to {}".format(ns))
            QtGui.QGuiApplication.processEvents()
