__author__ = 'Hoang V. Tran'
__version__ = '1.1'

from src.main.MainComponents.LocalStorage import AppStorage
from src.UI.UISubclasses.MainMenu import MainMenu
from settings import YANFEI_SMUG
from PyQt5 import QtWidgets, QtGui
import sys


def main():
    # Main. Finally. I suppose we can end this program here.

    # This storage will (hypothetically) carry data through windows.

    new_storage = AppStorage()

    # Storage is there.
    # Now, Main Window should be loaded now.
    # And now we load the window.
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Benchmark and Stress")
    app.setWindowIcon(QtGui.QIcon(YANFEI_SMUG))
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow(new_storage)
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    mw = MainMenu(new_storage)
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

