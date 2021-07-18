from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

from src.UI.GeneratedUI import Debug_Dialog
from src.main.MainComponents.LocalStorage import AppStorage


class Debug(QtWidgets.QDialog, Debug_Dialog.Ui_Dialog):
    '''
    A subclass Dialog of the Debug_Dialog.
    '''
    def __init__(self, storage: AppStorage):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.storage = storage
        self.err_ns = self.storage.get_server_down_nameservers()
        self.unres_doms = self.storage.get_unresolved_domains()
        self.rand_res = self.storage.get_random_resolved()
        self.move(100,100)

        for ns in self.err_ns:
            self.textBrowser.append("Cannot connect to {}".format(ns))
            self.textBrowser.append('')
            QtGui.QGuiApplication.processEvents()

        for dom_type in self.unres_doms:
            if len(self.unres_doms[dom_type]) != 0:
                self.textBrowser.append("Unable to resolve these {} domains:".format(dom_type))
                for dom in self.unres_doms[dom_type]:
                    self.textBrowser.append(dom)
                self.textBrowser.append('')
                QtGui.QGuiApplication.processEvents()

        if len(self.rand_res) != 0:
            self.textBrowser.append("These random domains were resolved:")
            for ran in self.rand_res:
                self.textBrowser.append(ran)
            QtGui.QGuiApplication.processEvents()

