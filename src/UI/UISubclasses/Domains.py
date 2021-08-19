from PyQt5 import QtWidgets
import random

from src.UI.GeneratedUI import NewDomainUI, SetDomain, RemoveDifferentDomains, AddDifferentDomains, random_add, ShuffleDomains
from src.UI.UISubclasses.AddDomains import AddDomains
from src.main.MainComponents.LocalStorage import AppStorage
from src.main.MainComponents.randomizers import domain_random


class Domain(QtWidgets.QMainWindow, NewDomainUI.Ui_MainWindow):
    def __init__(self, storage: AppStorage, parent = None):
        super(Domain, self).__init__(parent)
        self.setupUi(self)

        self.storage = storage
        self.valid_data = self.storage.get_valid_domains()
        self.random_data = self.storage.get_random_domains()
        self.blocked_data = self.storage.get_blocked_domains()

        # avoid duplicates
        self.valid_data = self.filter(self.valid_data)
        self.random_data = self.filter(self.random_data)
        self.blocked_data = self.filter(self.blocked_data)

        if len(self.valid_data) != 0:
            self.ValidList.addItems(self.valid_data)

        if len(self.random_data) != 0:
            self.RandomList.addItems(self.random_data)

        if len(self.blocked_data) != 0:
            self.BlockList.addItems(self.blocked_data)

        self.pushButton.clicked.connect(self.addChoices)
        self.pushButton_5.clicked.connect(self.openDialog)
        self.pushButton_2.clicked.connect(self.removeItem)
        self.pushButton_3.clicked.connect(self.removeAll)

        self.pushButton_4.clicked.connect(self.shuffle)

    def filter(self, data_list):
        '''
        filters out the duplicate in the given list.
        :return:
        '''
        return list(dict.fromkeys(data_list))

    def _get_cur_selected(self):
        return {'valid': self.ValidList.selectedItems(), 'random': self.RandomList.selectedItems(),
                    'blocked': self.BlockList.selectedItems()}

    def addChoices(self):
        self.choice_ = QtWidgets.QDialog()
        self.choice_ui = AddDifferentDomains.Ui_Dialog()
        self.choice_ui.setupUi(self.choice_)
        self.choice_ui.pushButton.clicked.connect(lambda: self.openWindow('valid'))
        self.choice_ui.pushButton_2.clicked.connect(self.openRandom)
        self.choice_ui.pushButton_3.clicked.connect(lambda: self.openWindow('blocked'))
        self.choice_.exec_()

    def openWindow(self, chosen_section):
        self.window = AddDomains()
        self.window.pushButton.clicked.connect(lambda: self.addContent(self.window.lineEdit.text(), chosen_section))
        self.window.exec_()

    def openRandom(self):
        self.r_dialog = QtWidgets.QDialog()
        self.r_ui = random_add.Ui_Dialog()
        self.r_ui.setupUi(self.r_dialog)
        self.r_ui.buttonBox.accepted.connect(lambda: self.addRandom(self.r_ui.lineEdit.text(), self.r_dialog))
        self.r_dialog.exec_()

    def addRandom(self, text, dialog):
        dialog.close()
        if len(text) == 0 or not text.isdigit():
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please type a number')
            self.error_dialog.exec_()
        else:
            random_gen = domain_random(int(text))
            self.RandomList.addItems(random_gen)
            self.storage.add_domains(random_gen, 'random')

    def openDialog(self):
        selected = self._get_cur_selected()
        total_selected = sum([len(sel) for sel in selected.values()])
        sole_selected = {k:v for k,v in selected.items() if len(v) == 1}
        if total_selected == 0:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please choose a domain to be edited.')
            self.error_dialog.exec_()
        elif total_selected > 1:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please choose only one domain to be edited.')
            self.error_dialog.exec_()
        else:
            self.dialog = QtWidgets.QDialog()
            self.ui = SetDomain.Ui_Dialog()
            self.ui.setupUi(self.dialog)
            self.ui.lineEdit.setText(sole_selected[list(sole_selected.keys())[0]][0].text())
            self.ui.buttonBox.accepted.connect(
                lambda: self.modifyContent(self.dialog, self.ui.lineEdit.text(), sole_selected))
            self.dialog.exec_()

    def addContent(self, content, section):
        content_list = content.split(";")
        for c in content_list:
            c = c.replace(" ", "")
            if len(c) != 0:
                cur_data = self.storage.get_domain_by_section(section)
                if c not in cur_data:
                    if section == 'valid':
                        self.ValidList.addItem(c)
                        self.storage.add_valid_domain(c)
                    elif section == 'random':
                        self.RandomList.addItem(c)
                        self.storage.add_random_domain(c)
                    else:
                        self.BlockList.addItem(c)
                        self.storage.add_blocked_domain(c)
        self.window.close()

    def modifyContent(self, dialog, content, select_dict):
        dialog.close()
        content = content.replace(" ", "")
        key_to_change, val_to_change = list(select_dict.items())[0]
        if len(content) != 0:
            self.storage.modify_domain(key_to_change,val_to_change[0].text(), content)
        self.refresh(key_to_change)

    def refresh(self, key):
        if key == 'valid':
            self.ValidList.clear()
            self.valid_data = self.storage.get_valid_domains()
            self.ValidList.addItems(self.valid_data)
        elif key == 'random':
            self.RandomList.clear()
            self.random_data = self.storage.get_random_domains()
            self.RandomList.addItems(self.random_data)
        else:
            self.BlockList.clear()
            self.blocked_data = self.storage.get_blocked_domains()
            self.BlockList.addItems(self.blocked_data)

    def removeItem(self):
        selected = self._get_cur_selected()
        total_selected = sum([len(sel) for sel in selected.items()])
        if total_selected == 0:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please choose a domain to be removed.')
            self.error_dialog.exec_()
        for key in selected:
            if key == 'valid':
                for entry in selected[key]:
                    self.ValidList.takeItem(self.ValidList.row(entry))
                    self.storage.remove_domains(entry.text(),key)
            elif key == 'random':
                for entry in selected[key]:
                    self.RandomList.takeItem(self.RandomList.row(entry))
                    self.storage.remove_domains(entry.text(),key)
            else:
                for entry in selected[key]:
                    self.BlockList.takeItem(self.BlockList.row(entry))
                    self.storage.remove_domains(entry.text(),key)

    def removeAll(self):
        self.remove_dialog = QtWidgets.QDialog()
        self.remove_obj = RemoveDifferentDomains.Ui_Dialog()

        self.remove_obj.setupUi(self.remove_dialog)
        self.remove_obj.pushButton.clicked.connect(self.remove_valid)
        self.remove_obj.pushButton_2.clicked.connect(self.remove_random)
        self.remove_obj.pushButton_3.clicked.connect(self.remove_blocked)
        self.remove_dialog.exec_()

    def remove_valid(self):
        self.ValidList.clear()
        self.storage.remove_all_valid_domains()

    def remove_random(self):
        self.RandomList.clear()
        self.storage.remove_all_random_domains()

    def remove_blocked(self):
        self.BlockList.clear()
        self.storage.remove_all_blocked_domains()

    def shuffle(self):
        self.shuffle_dialog = QtWidgets.QDialog()
        self.shuffle_obj = ShuffleDomains.Ui_ShuffleChoice()

        self.shuffle_obj.setupUi(self.shuffle_dialog)
        self.shuffle_obj.shuffleValid.clicked.connect(self.shuffle_valid)
        self.shuffle_obj.shuffleRandom.clicked.connect(self.shuffle_random)
        self.shuffle_obj.shuffleBlocked.clicked.connect(self.shuffle_blocked)
        self.shuffle_dialog.exec_()

    def shuffle_valid(self):
        cur_valid_storage = self.storage.get_valid_domains()
        random.shuffle(cur_valid_storage)
        self.storage.remove_all_valid_domains()
        self.storage.add_valid_domains(cur_valid_storage)
        self.refresh('valid')

    def shuffle_random(self):
        cur_random_storage = self.storage.get_random_domains()
        random.shuffle(cur_random_storage)
        self.storage.remove_all_random_domains()
        self.storage.add_random_domains(cur_random_storage)
        self.refresh('random')

    def shuffle_blocked(self):
        cur_blocked_storage = self.storage.get_blocked_domains()
        random.shuffle(cur_blocked_storage)
        self.storage.remove_all_blocked_domains()
        self.storage.add_blocked_domains(cur_blocked_storage)
        self.refresh('blocked')
