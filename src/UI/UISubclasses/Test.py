from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from src.UI.GeneratedUI import NewTestUI,Stress_Properties, Benchmark_Properties
from src.UI.UISubclasses import Debug, Report
from src.main.MainComponents.DNSPing import DNSPing
from src.main.MainComponents.DNSTest import ValidTest, RandomTest, BlockedTest
from src.main.MainComponents.LocalStorage import AppStorage
from src.main.MainComponents.notifications import send_notification


class Test(QtWidgets.QMainWindow, NewTestUI.Ui_MainWindow):
    DOMAIN_DEFAULT_AMT_STR = '50'
    INSTANCE_DEFAULT_AMT_STR = '0'

    def __init__(self, local_storage: AppStorage, parent = None):
        super(Test, self).__init__(parent)
        self.setupUi(self)

        self.storage = local_storage
        self.nameserver_data = self.storage.get_nameservers()

        self._valid_data = self.storage.get_valid_domains()
        self._random_data = self.storage.get_random_domains()
        self._blocked_data = self.storage.get_blocked_domains()

        self.pushButton.clicked.connect(self.ping)
        self.pushButton_2.clicked.connect(self.benchmark)
        self.pushButton_3.clicked.connect(self.stress)
        self.pushButton_4.clicked.connect(self.both)

        self._all_cur_text = []

    def _update_window(self, worker):
        while worker.running:
            cur_text = self.storage.cur_string
            if cur_text not in self._all_cur_text and len(cur_text) != 0:
                self._all_cur_text.append(cur_text)
                self.textBrowser.append(cur_text)
                QtGui.QGuiApplication.processEvents()

    def openMain(self, MainWindow):
        MainWindow.close()

    def openReport(self, purpose:str):
        self.storage.cur_test_state = False
        try:

            send_notification("Finished {}!".format(purpose + "ing"), "Please check the app :smug:")

        except AttributeError:
            pass
        try:
            if len(self.storage.get_server_down_nameservers()) != 0:
                self.dbg = Debug.Debug(self.storage)
                self.dbg.show()
        except Exception as e:
            print(e)

        self.result_storage = self.storage.copy_results()
        if len(self.storage.get_nameservers()) - len(self.storage.get_server_down_nameservers()) != 0:
            self.rp_ = Report.Report(self.storage, purpose)
            self.rp_.show()
        else:
            self.storage.clear_server_down_nameservers()

    def secondAction(self, purpose, data, stress_instance):
        valid_test, random_test, blocked_test = data
        if len(self.storage.get_nameservers()) - len(self.storage.get_server_down_nameservers()) != 0:
            self.rp = Report.Report(self.storage,purpose)
            self.rp.show()

        self.textBrowser.clear()
        QtGui.QGuiApplication.processEvents()
        self._all_cur_text.clear()

        self.worker_2 = WorkerTest([valid_test, random_test, blocked_test], self.storage, stress_instance)
        self.worker_2.start()
        self.worker_2.finished.connect(lambda: self.openReport('stress'))
        self._update_window(self.worker_2)

    def ping(self):
        if self.storage.has_pinged and len(self.storage.pinged_ns) == len(self.storage.get_nameservers()):
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('You have already pinged the nameservers.')
            self.error_dialog.exec_()
        else:
            send_notification("Started pinging!", "Please wait")

            self.ping_worker = WorkerPing(self.nameserver_data, self.storage)
            self.ping_worker.start()
            self.ping_worker.finished.connect(self.post_ping)
            self._update_window(self.ping_worker)

    def post_ping(self):
        send_notification('Finished pinging', 'Please check the app')

    def benchmark(self):
        if not self.storage.has_pinged:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please ping before testing.')
            self.error_dialog.exec_()
        else:
            anotherRunning = self.storage.cur_test_state
            if anotherRunning:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Warning')
                self.error_dialog.showMessage('Please wait for other process to complete.')
                self.error_dialog.exec_()
            else:
                self.storage.reset()
                self.storage.cur_string = ""
                self.storage.cur_test_state = True
                self.dialog_b = Dialog(self.storage)
                self.bench_props_ui = Benchmark_Properties.Ui_Dialog()
                self.bench_props_ui.setupUi(self.dialog_b)
                self.bench_props_ui.buttonBox.accepted.connect(
                    lambda: self.accept_bench(self.bench_props_ui.lineEdit.text(), self.dialog_b))
                self.bench_props_ui.buttonBox.rejected.connect(self.reject)
                self.dialog_b.show()

    def reject(self):
        self.storage.cur_test_state = False

    def _start_bench(self, no_domains):
        self.storage.modify_config('domains_used', no_domains)
        self.storage.modify_config('instance_count', [1,1,1])

        valid_test, random_test, blocked_test = self.modify_data(self.storage.get_config()['domains_used'])

        send_notification('Start benching', 'Please wait')

        self.worker_b = WorkerTest([valid_test, random_test, blocked_test],
                                       self.storage, [1, 1, 1])
        self.worker_b.start()
        self.worker_b.finished.connect(lambda: self.openReport('benchmark'))
        self._update_window(self.worker_b)

    def accept_bench(self, text, dialog):
        self.textBrowser.clear()
        QtGui.QGuiApplication.processEvents()
        self._all_cur_text.clear()
        text = text.strip().replace(" ","")
        if len(text) == 0:
            text = self.DOMAIN_DEFAULT_AMT_STR
        if self._verify_input(text):
            self._start_bench(int(text))
        else:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please type a number.')
            self.error_dialog.exec_()
            dialog.show()

    def modify_data(self, required_number):
        if required_number == 0:
            return [],[],[]
        else:
            valid_data = self._valid_data.copy()
            random_data = self._random_data.copy()
            blocked_data = self._blocked_data.copy()

            if len(self._valid_data) < required_number and len(self._valid_data) != 0:
                valid_data = self._mod(self._valid_data, required_number)
            else:
                valid_data = valid_data[:required_number]
            if len(self._random_data) < required_number and len(self._random_data) != 0:
                random_data = self._mod(self._random_data, required_number)
            else:
                random_data = random_data[:required_number]
            if len(self._blocked_data) < required_number and len(self._blocked_data) != 0:
                blocked_data = self._mod(self._blocked_data, required_number)
            else:
                blocked_data = blocked_data[:required_number]
            return valid_data, random_data, blocked_data

    def _mod(self, mod_list:list, req_num):
        # So now we are duplicating the list.
        # First, let's see the number of times I need to multiply this list
        mul_times = req_num // len(mod_list)
        mod = req_num % len(mod_list)
        mod_list_copy = mod_list.copy()
        new_mod_list = mod_list.copy()

        if mul_times == 1:
            if mod != 0:
                new_mod_list.extend(mod_list_copy[: mod])
        else:
            for t in range(mul_times - 1):
                new_mod_list.extend(mod_list_copy)
            if mod != 0:
                new_mod_list.extend(mod_list_copy[:mod])

        return new_mod_list

    def stress(self):
        if not self.storage.has_pinged:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please ping before testing.')
            self.error_dialog.exec_()
        else:
            anotherRunning = self.storage.cur_test_state
            if anotherRunning:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Warning')
                self.error_dialog.showMessage('Please wait for other process to complete.')
                self.error_dialog.exec_()
            else:
                self.storage.reset()
                self.storage.cur_string = ""
                self.storage.cur_test_state = True
                self.dialog_s = Dialog(self.storage)
                self.stress_props_ui = Stress_Properties.Ui_Dialog()
                self.stress_props_ui.setupUi(self.dialog_s)
                self.stress_props_ui.buttonBox.accepted.connect(
                    lambda: self.accept_stress(self.stress_props_ui.validEdit.text(),
                                               self.stress_props_ui.RandomEdit.text(),
                                               self.stress_props_ui.BlockedEdit.text(),
                                               self.stress_props_ui.DomainEdit.text(),
                                               self.dialog_s))
                self.stress_props_ui.buttonBox.rejected.connect(self.reject)
                self.dialog_s.show()

    def _verify_input(self, txt):
        return len(txt) != 0 and txt.isdigit()

    def accept_stress(self, valid_ic_txt, random_ic_txt, blocked_ic_txt, domain_amt_txt, dialog):
        self.textBrowser.clear()
        QtGui.QGuiApplication.processEvents()
        self._all_cur_text.clear()
        if len(valid_ic_txt) == 0:
            valid_ic_txt = self.INSTANCE_DEFAULT_AMT_STR
        if len(random_ic_txt) == 0:
            random_ic_txt = self.INSTANCE_DEFAULT_AMT_STR
        if len(blocked_ic_txt) == 0:
            blocked_ic_txt = self.INSTANCE_DEFAULT_AMT_STR
        if len(domain_amt_txt) == 0:
            domain_amt_txt = self.DOMAIN_DEFAULT_AMT_STR

        valid_ic_txt = valid_ic_txt.strip().replace(" ","")
        random_ic_txt = random_ic_txt.strip().replace(" ", "")
        blocked_ic_txt = blocked_ic_txt.strip().replace(" ", "")
        domain_amt_txt = domain_amt_txt.strip().replace(" ", "")

        if self._verify_input(valid_ic_txt) and self._verify_input(random_ic_txt) and self._verify_input(blocked_ic_txt) and self._verify_input(domain_amt_txt):
            self.storage.modify_config('domains_used', int(domain_amt_txt))
            self.storage.modify_config('instance_count', [int(valid_ic_txt), int(random_ic_txt), int(blocked_ic_txt)])

            valid_test, random_test, blocked_test = self.modify_data(self.storage.get_config()['domains_used'])

            self.instance_count = self.storage.get_config()['instance_count']

            try:
                send_notification("Start stressing", "Please wait")
            except AttributeError:
                pass

            self.worker_s = WorkerTest([valid_test, random_test, blocked_test],
                                   self.storage, self.instance_count)
            self.worker_s.start()
            self.worker_s.finished.connect(lambda: self.openReport('stress'))
            self._update_window(self.worker_s)
        else:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please type a number for the number of domains and instances')
            self.error_dialog.exec_()
            dialog.show()

    def both(self):
        if not self.storage.has_pinged:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please ping before testing.')
            self.error_dialog.exec_()
        else:
            anotherRunning = self.storage.cur_test_state
            if anotherRunning:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Warning')
                self.error_dialog.showMessage('Please wait for other process to complete.')
                self.error_dialog.exec_()
            else:
                self.storage.reset()
                self.storage.cur_string = ""
                self.storage.cur_test_state = True
                self.dialog_both = Dialog(self.storage)
                self.both_props_ui = Stress_Properties.Ui_Dialog()
                self.both_props_ui.setupUi(self.dialog_both)
                self.both_props_ui.buttonBox.accepted.connect(
                    lambda: self.accept_both(self.both_props_ui.validEdit.text(),
                                             self.both_props_ui.RandomEdit.text(),
                                             self.both_props_ui.BlockedEdit.text(),
                                             self.both_props_ui.DomainEdit.text(),
                                             self.dialog_both))
                self.both_props_ui.buttonBox.rejected.connect(self.reject)
                self.dialog_both.show()

    def accept_both(self, valid_ic_txt, random_ic_txt, blocked_ic_txt, domain_amt_txt, dialog):
        self.textBrowser.clear()
        QtGui.QGuiApplication.processEvents()
        self._all_cur_text.clear()
        if len(valid_ic_txt) == 0:
            valid_ic_txt = self.INSTANCE_DEFAULT_AMT_STR
        if len(random_ic_txt) == 0:
            random_ic_txt = self.INSTANCE_DEFAULT_AMT_STR
        if len(blocked_ic_txt) == 0:
            blocked_ic_txt = self.INSTANCE_DEFAULT_AMT_STR
        if len(domain_amt_txt) == 0:
            domain_amt_txt = self.DOMAIN_DEFAULT_AMT_STR

        valid_ic_txt = valid_ic_txt.strip().replace(" ", "")
        random_ic_txt = random_ic_txt.strip().replace(" ", "")
        blocked_ic_txt = blocked_ic_txt.strip().replace(" ", "")
        domain_amt_txt = domain_amt_txt.strip().replace(" ", "")

        if self._verify_input(valid_ic_txt) and self._verify_input(random_ic_txt) and self._verify_input(blocked_ic_txt) and self._verify_input(domain_amt_txt):
            self.storage.modify_config('domains_used', int(domain_amt_txt))

            self.storage.modify_config('instance_count', [int(valid_ic_txt), int(random_ic_txt), int(blocked_ic_txt)])

            valid_test, random_test, blocked_test = self.modify_data(self.storage.get_config()['domains_used'])

            self.instance_count = self.storage.get_config()['instance_count']

            try:
                send_notification('Starting both tests','Please wait')
            except AttributeError:
                pass

            self.worker_both_1 = WorkerTest([valid_test, random_test, blocked_test],
                                   self.storage, [1,1,1])
            self.worker_both_1.start()
            self._update_window(self.worker_both_1)
            self.worker_both_1.finished.connect(lambda: self.secondAction('benchmark', [valid_test, random_test, blocked_test], self.instance_count))
        else:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please type a number for the number of domains and instances')
            self.error_dialog.exec_()
            dialog.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.storage.cur_test_state:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle('Warning')
            self.error_dialog.showMessage('Please wait until the test is completed.')
            self.error_dialog.exec_()
            a0.ignore()
        else:
            a0.accept()


class WorkerPing(QtCore.QThread):
    def __init__(self, ns, storage):
        super(WorkerPing, self).__init__()

        self.ns = ns
        self.storage = storage
        self.running = True

    def run(self):
        self.storage.pinged_ns = DNSPing(self.ns, self.storage)
        self.storage.has_pinged = True
        self.running = False



class WorkerTest(QtCore.QThread):
    def __init__(self, data_list, storage, inst_count_list):
        super(WorkerTest, self).__init__()

        self.valid_data = data_list[0]
        self.random_data = data_list[1]
        self.blocked_data = data_list[2]
        self.storage = storage
        self.inst_count_list = inst_count_list
        self.running = True

    def run(self):
        self.storage.cur_test_state = True
        valid_inst = self.inst_count_list[0]
        random_inst = self.inst_count_list[1]
        block_inst = self.inst_count_list[2]

        pinged_inst = self.storage.pinged_ns

        valid_test = ValidTest(pinged_inst, self.valid_data, self.storage, valid_inst)
        random_test = RandomTest(pinged_inst, self.random_data, self.storage, random_inst)
        block_test = BlockedTest(pinged_inst, self.blocked_data, self.storage, block_inst)

        thread_1 = Thread(target = valid_test.run)
        thread_2 = Thread(target = random_test.run)
        thread_3 = Thread(target = block_test.run)
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_1.join()
        thread_2.join()
        thread_3.join()

        self.running = False


class Dialog(QtWidgets.QDialog):
    def __init__(self, storage:AppStorage):
        super(Dialog, self).__init__()
        self.storage = storage

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() != QtCore.Qt.Key_Escape:
            a0.accept()
        else:
            a0.ignore()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.storage.cur_test_state = False
        a0.accept()
