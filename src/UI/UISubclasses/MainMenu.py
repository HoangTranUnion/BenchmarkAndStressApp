from PyQt5 import QtCore, QtGui, QtWidgets

from src.UI.GeneratedUI import NewDomainUI, NameserverMain, NewTestUI, NewMain
from src.main.MainComponents.LocalStorage import LocalStorage


class MainMenu(QtWidgets.QMainWindow, NewMain.Ui_MainWindow):
    def __init__(self, storage):
        QtWidgets.QMainWindow.__init__(self)
        self.storage = storage
        # Set up the user interface from Designer.
        self.setupUi(self)

        self.pushButton_4.clicked.connect(self.openTest)
        self.pushButton_2.clicked.connect(lambda: self.openWindow(NewDomainUI))
        self.pushButton.clicked.connect(lambda: self.openWindow(NameserverMain))

    def openWindow(self, widget):
        self.window = QtWidgets.QMainWindow()
        # self.ui = widget.Ui_MainWindow(self.storage)
        self.ui.setupUi(self.window)
        self.window.show()

    def openTest(self):
        self.window = TestWindow(self.storage)
        # self.ui = NewTestUI.Ui_MainWindow(self.storage)
        self.ui.setupUi(self.window)
        self.window.show()



class TestWindow(QtWidgets.QMainWindow):
    def __init__(self, storage:LocalStorage):
        super(TestWindow, self).__init__()
        self.storage = storage

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.storage.cur_test_state:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please wait until the test is completed.')
            self.error_dialog.exec_()
            a0.ignore()
        else:
            a0.accept()
