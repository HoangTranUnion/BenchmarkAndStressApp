# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\remin\PycharmProjects\BenchmarkAndStressApp\AppResources\NewMain.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from src.UI import TempTest, NewDomainUI, NameserverMain, NewTestUI
from src.main.MainComponents.LocalStorage import LocalStorage


class Ui_MainWindow(object):
    def __init__(self, local_storage: LocalStorage):
        self.storage = local_storage

    def openWindow(self, widget):
        self.window = QtWidgets.QMainWindow()
        self.ui = widget.Ui_MainWindow(self.storage)
        self.ui.setupUi(self.window)
        self.window.show()

    def openTest(self):
        self.window = TestWindow(self.storage)
        self.ui = NewTestUI.Ui_MainWindow(self.storage)
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(392, 382)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 250, 291, 81))
        self.pushButton_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_4.clicked.connect(self.openTest)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 140, 291, 81))
        self.pushButton_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_2.clicked.connect(lambda: self.openWindow(NewDomainUI))

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 30, 291, 81))
        self.pushButton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(lambda: self.openWindow(NameserverMain))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Benchmark"))
        self.pushButton_4.setText(_translate("MainWindow", "Test"))
        self.pushButton_2.setText(_translate("MainWindow", "Domains"))
        self.pushButton.setText(_translate("MainWindow", "Nameservers"))


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