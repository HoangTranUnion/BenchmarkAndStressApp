# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\remin\PycharmProjects\BenchmarkAndStressApp\AppResources\ReportUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from src.main.MainComponents.LocalStorage import LocalStorage
from src.main.MainComponents.CalculateResults import calculate_res
import datetime
import os
import xlwt
from settings import ROOT_FOLDER


class Ui_MainWindow(object):
    def __init__(self, storage: LocalStorage, purpose: str):
        self.storage = storage
        self.purpose = purpose
        self.err_ns = self.storage.get_server_down_nameservers()
        data :dict = self.storage.get_test_results()
        self.reporting_data = self.cal(data)
        self.ns_info = self.storage.get_nameserver_types()

    def cal(self,data):
        reports = data[0]
        records = data[1]
        ret_results = {}
        for domain in reports:
            ret_results[domain] = calculate_res(reports[domain], records[domain])
        return ret_results

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1011, 602)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.pushButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 60, 991, 521))
        self.tableView.setObjectName("tableView")

        self.tableView.setColumnCount(6)
        self.tableView.setRowCount(len(list(self.reporting_data.keys())) + 1 - len(self.err_ns))

        self.nameserver_type_sorted = dict(sorted(self.ns_info.items(), key=lambda x: x[1], reverse=True))
        self.data_sorted = dict(sorted(self.reporting_data.items(), key = lambda x: (self.nameserver_type_sorted[x[0]], self.reporting_data[x[0]][2])))

        # Setting up the labels for the columns.
        self.tableView.setItem(0, 0, QTableWidgetItem('URL/IP'))
        self.tableView.setItem(0, 1, QTableWidgetItem("Type"))
        self.tableView.setItem(0, 2, QTableWidgetItem('Max (ms)'))
        self.tableView.setItem(0, 3, QTableWidgetItem('Min (ms)'))
        self.tableView.setItem(0, 4, QTableWidgetItem('Avg (ms)'))
        self.tableView.setItem(0, 5, QTableWidgetItem('Std (ms)'))

        # Now setting up the content of the table.
        offset = 0
        for url_pos in range(len(self.data_sorted.keys())):
            link = list(self.data_sorted.keys())[url_pos]
            if link in self.err_ns:
                offset += 1
            else:
                max_, min_, avg_, std_ = self.reporting_data[link]
                self.tableView.setItem(url_pos + 1 - offset, 0, QTableWidgetItem(link))
                self.tableView.setItem(url_pos + 1 - offset, 1, QTableWidgetItem(self.nameserver_type_sorted[link]))
                self.tableView.setItem(url_pos + 1 - offset, 2, QTableWidgetItem('{:.2f}'.format(max_)))
                self.tableView.setItem(url_pos + 1 - offset, 3, QTableWidgetItem('{:.2f}'.format(min_)))
                self.tableView.setItem(url_pos + 1 - offset, 4, QTableWidgetItem('{:.2f}'.format(avg_)))
                self.tableView.setItem(url_pos + 1 - offset, 5, QTableWidgetItem('{:.2f}'.format(std_)))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Results_{}".format(self.purpose)))
        self.pushButton.setText(_translate("MainWindow", "Save Report"))
        self.pushButton.clicked.connect(lambda: self.save_result(MainWindow))

    def save_result(self, MainWindow):
        folder_selection = QtWidgets.QFileDialog.getExistingDirectory()

        if len(folder_selection) == 0:
            folder_selection = ROOT_FOLDER

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
        MainWindow.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
