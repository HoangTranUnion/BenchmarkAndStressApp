from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from src.UI.GeneratedUI import AddDomains_Dialog
from src.main.MainComponents.extract_domain import ExtractDomain


class AddDomains(QDialog, AddDomains_Dialog.Ui_AddDomains):
    '''
    A subclass Dialog of the AddDomains_Dialog.
    '''
    def __init__(self):
        QDialog.__init__(self)
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