# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\remin\PycharmProjects\BenchmarkAndStressApp\AppResources\AddDomains_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddDomains(object):
    def setupUi(self, AddDomains):
        AddDomains.setObjectName("AddDomains")
        AddDomains.resize(348, 160)
        self.lineEdit = QtWidgets.QLineEdit(AddDomains)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 331, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(AddDomains)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 331, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(AddDomains)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 100, 331, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(AddDomains)
        QtCore.QMetaObject.connectSlotsByName(AddDomains)

    def retranslateUi(self, AddDomains):
        _translate = QtCore.QCoreApplication.translate
        AddDomains.setWindowTitle(_translate("AddDomains", "Add Domains"))
        self.pushButton.setText(_translate("AddDomains", "Add Domain"))
        self.pushButton_2.setText(_translate("AddDomains", "Import Domains from Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddDomains = QtWidgets.QDialog()
    ui = Ui_AddDomains()
    ui.setupUi(AddDomains)
    AddDomains.show()
    sys.exit(app.exec_())
