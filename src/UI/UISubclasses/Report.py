from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from src.UI.GeneratedUI import ReportUI
from src.main.MainComponents.LocalStorage import AppStorage
from src.main.MainComponents.CalculateResults import calculate_res
import datetime
import os
import xlwt
from settings import ROOT_FOLDER


class Report(QtWidgets.QMainWindow, ReportUI.Ui_MainWindow):
    def __init__(self, storage: AppStorage, purpose, parent = None):
        try:
            super(Report, self).__init__(parent)
            self.setupUi(self)

            self.storage = storage
            self.purpose = purpose
            self.err_ns = self.storage.get_server_down_nameservers()
            data: dict = self.storage.get_test_results()
            self.reporting_data = self.cal(data)
            self.ns_info = self.storage.get_nameserver_types()
            self.pushButton.clicked.connect(lambda: self.save_result(self))

            self._setup_table_view()

            self.report_saved = False
        except Exception as e:
            print(e)

    def cal(self,data):
        reports = data[0]
        records = data[1]
        ret_results = {}
        for domain in reports:
            ret_results[domain] = calculate_res(reports[domain], records[domain])
        return ret_results

    def _setup_table_view(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(len(list(self.reporting_data.keys())) + 1 - len(self.err_ns))

        self.nameserver_type_sorted = dict(sorted(self.ns_info.items(), key=lambda x: x[1], reverse=True))
        self.data_sorted = dict(sorted(self.reporting_data.items(),
                                       key=lambda x: (self.nameserver_type_sorted[x[0]], self.reporting_data[x[0]][2])))

        # Setting up the labels for the columns.
        self.tableWidget.setItem(0, 0, QTableWidgetItem('URL/IP'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Type"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Max (ms)'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Min (ms)'))
        self.tableWidget.setItem(0, 4, QTableWidgetItem('Avg (ms)'))
        self.tableWidget.setItem(0, 5, QTableWidgetItem('Std (ms)'))

        # Now setting up the content of the table.
        offset = 0
        for url_pos in range(len(self.data_sorted.keys())):
            link = list(self.data_sorted.keys())[url_pos]
            if link in self.err_ns:
                offset += 1
            else:
                max_, min_, avg_, std_ = self.reporting_data[link]
                self.tableWidget.setItem(url_pos + 1 - offset, 0, QTableWidgetItem(link))
                self.tableWidget.setItem(url_pos + 1 - offset, 1, QTableWidgetItem(self.nameserver_type_sorted[link]))
                self.tableWidget.setItem(url_pos + 1 - offset, 2, QTableWidgetItem('{:.2f}'.format(max_)))
                self.tableWidget.setItem(url_pos + 1 - offset, 3, QTableWidgetItem('{:.2f}'.format(min_)))
                self.tableWidget.setItem(url_pos + 1 - offset, 4, QTableWidgetItem('{:.2f}'.format(avg_)))
                self.tableWidget.setItem(url_pos + 1 - offset, 5, QTableWidgetItem('{:.2f}'.format(std_)))

    def save_result(self, MainWindow):
        folder_selection = QtWidgets.QFileDialog.getExistingDirectory()

        if len(folder_selection) != 0:
            cur_day = datetime.date.today().strftime("%Y%m%d")

            cur_time = datetime.datetime.now().strftime('%H%M%S')
            report_file = "Report_{}_{}_{}.xls".format(self.purpose, cur_day, cur_time)
            full_report_dir = os.path.join(folder_selection, report_file)

            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet("Report")

            sheet1.write(0, 0, 'URL / IP')
            sheet1.write(0, 1, 'Type')
            sheet1.write(0, 2, 'Max (ms)')
            sheet1.write(0, 3, 'Min (ms)')
            sheet1.write(0, 4, 'Avg (ms)')
            sheet1.write(0, 5, 'Std (ms)')

            offset = 0
            for url_pos in range(len(self.data_sorted.keys())):
                link = list(self.data_sorted.keys())[url_pos]
                if link in self.err_ns:
                    offset += 1
                else:
                    max_, min_, avg_, std_ = self.reporting_data[link]
                    sheet1.write(url_pos + 1 - offset, 0, link)
                    sheet1.write(url_pos + 1 - offset, 1, self.nameserver_type_sorted[link])
                    sheet1.write(url_pos + 1 - offset, 2, max_)
                    sheet1.write(url_pos + 1 - offset, 3, min_)
                    sheet1.write(url_pos + 1 - offset, 4, avg_)
                    sheet1.write(url_pos + 1 - offset, 5, std_)


            wb.save(full_report_dir)
            self.report_saved = True
            MainWindow.close()

    def closeEvent(self, a0):
        if not self.report_saved:
            quit_msg = "Do you want to save the report before exiting?"
            reply = QtWidgets.QMessageBox.question(self, 'Message',
                                                   quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.save_result(self)
                a0.ignore()
            else:
                a0.accept()
        else:
            a0.accept()
