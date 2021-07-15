from PyQt5 import QtCore, QtWidgets

from src.UI.GeneratedUI import NameserverMain, SetNameserver
from src.UI.UISubclasses.AddNameservers import AddNameservers
from src.main.MainComponents.LocalStorage import LocalStorage


class Nameserver(QtWidgets.QMainWindow, NameserverMain.Ui_MainWindow):
    def __init__(self, storage: LocalStorage, parent = None):
        super(Nameserver, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage
        self.nameserver_data = self.storage.get_nameservers()

        if len(self.nameserver_data) != 0:
            self.listWidget.addItems(self.nameserver_data)

        self.pushButton.clicked.connect(self.openWindow)
        self.pushButton_2.clicked.connect(self.removeItem)
        self.pushButton_3.clicked.connect(self.removeAll)
        self.pushButton_5.clicked.connect(self.openDialog)

    def openWindow(self):
        self.window = AddNameservers()
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.pushButton.clicked.connect(lambda: self.addContent(self.window.lineEdit.text()))
        self.window.exec_()

    def openDialog(self):
        if len(self.listWidget.selectedItems()) == 0:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please choose a nameserver to be edited.')
            self.error_dialog.exec_()
        elif len(self.listWidget.selectedItems()) > 1:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please choose only one nameserver to be edited.')
            self.error_dialog.exec_()
        else:
            self.dialog = QtWidgets.QDialog()
            self.ui = SetNameserver.Ui_Dialog()
            self.ui.setupUi(self.dialog)
            self.ui.lineEdit_2.setText(self.listWidget.selectedItems()[0].text())
            self.ui.buttonBox.accepted.connect(lambda: self.modifyContent(self.dialog, self.ui.lineEdit_2.text()))
            self.dialog.exec_()

    def addContent(self, content):
        content_list = content.split(";")
        for c in content_list:
            stripped_content = c.strip()
            if len(stripped_content) != 0:
                cur_data = self.storage.get_nameservers()
                if stripped_content not in cur_data:
                    self.listWidget.addItem(stripped_content)
                    self.storage.add_nameserver(stripped_content)
        self.window.close()

    def modifyContent(self, dialog, content):
        dialog.close()
        content = content.replace(" ", "")
        if len(content) != 0:
            selected = self.listWidget.selectedItems()[0]
            self.storage.modify_nameserver(selected.text(), content)
            self.refresh()

    def refresh(self):
        self.listWidget.clear()
        self.nameserver_data = self.storage.get_nameservers()
        self.listWidget.addItems(self.nameserver_data)

    def removeItem(self):
        if len(self.listWidget.selectedItems()) == 0:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please choose a nameserver to be removed.')
            self.error_dialog.exec_()
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))
            self.storage.remove_nameserver(item.text())

    def removeAll(self):
        self.listWidget.clear()
        self.storage.remove_all_nameservers()