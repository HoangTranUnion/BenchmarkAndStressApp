import sys

from PyQt5 import QtWidgets, QtGui

from src.UI.GeneratedUI import NewMain
from src.UI.UISubclasses import Nameserver, Domains, Test
from src.main.MainComponents.LocalStorage import AppStorage


class MainMenu(QtWidgets.QMainWindow, NewMain.Ui_MainWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(MainMenu, self).__init__(parent)
        self.storage = storage
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.pushButton_4.clicked.connect(self.openTest)
        self.pushButton.clicked.connect(self.openNameserverWindow)
        self.pushButton_2.clicked.connect(self.openDomainWindow)
        self._ns = Nameserver.Nameserver(self.storage)
        self._dm = Domains.Domain(self.storage)
        self._test = Test.Test(self.storage)

    def openNameserverWindow(self):
        if not self._ns.isVisible():
            if self._test.isVisible():
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Warning')
                self.error_dialog.showMessage('Please close the test menu')
                self.error_dialog.exec_()
            else:
                self._ns.show()

    def openDomainWindow(self):
        if not self._dm.isVisible():
            if self._test.isVisible():
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Warning')
                self.error_dialog.showMessage('Please close the test menu')
                self.error_dialog.exec_()
            else:
                self._dm.show()

    def openTest(self):
        if not self._test.isVisible():
            total_domain_amt = len(self.storage.get_valid_domains()) + len(self.storage.get_random_domains()) + len(self.storage.get_blocked_domains())
            if len(self.storage.get_nameservers()) == 0 or total_domain_amt == 0:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Warning')
                self.error_dialog.showMessage('Missing nameserver/domain. Please check your test inputs')
                self.error_dialog.exec_()
            else:
                self._test.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                           quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            a0.accept()
            sys.exit()
        else:
            a0.ignore()