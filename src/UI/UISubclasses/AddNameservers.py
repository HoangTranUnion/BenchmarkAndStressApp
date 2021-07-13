from PyQt5 import QtCore, QtGui, QtWidgets

from src.UI.GeneratedUI.AddNameserver_Dialog import Ui_Dialog
from src.main.MainComponents.extract_domain import ExtractDomain


class AddNameservers(QtWidgets.QDialog, Ui_Dialog):
    '''
        A subclass Dialog of the AddNameserver_Dialog.
        '''
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.lineEdit.setMaxLength(10000000)
        self.pushButton_2.clicked.connect(self.selectFiles)

    def selectFiles(self):
        fileNames, _ = QtWidgets.QFileDialog.getOpenFileNames()
        data_string = ''
        for file in fileNames:
            data = ExtractDomain.get_all_data(file)
            data_string += ';'.join(data)
        self.lineEdit.setText(data_string)