from src.main.MainComponents.extract_domain import ExtractDomain
from src.main.MainComponents.LocalStorage import LocalStorage
from src.main.MainComponents.DomainRandomizer import domain_random
from src.UI.NewMain import Ui_MainWindow
from settings import *

from PyQt5 import QtWidgets
import os
import sys


def _confirm_dir():
    # Before that, does folder data exist?
    if not os.path.isdir(DEFAULT_APP_DATA_FOLDER):
        os.mkdir(DEFAULT_APP_DATA_FOLDER, mode=0o777)

    # Now, 1
    if not os.path.isdir(DEFAULT_RESULTS_LOC):
        os.mkdir(DEFAULT_RESULTS_LOC, mode=0o777)

    # 2
    if not os.path.isdir(DEFAULT_NAMESERVER_DATA_LOC):
        os.mkdir(DEFAULT_NAMESERVER_DATA_LOC, mode=0o777)

    # 3
    if not os.path.isdir(DEFAULT_DOMAIN_DATA_LOC):
        os.mkdir(DEFAULT_DOMAIN_DATA_LOC, mode=0o777)


def main():
    # Main. Finally. I suppose we can end this program here.
    # First, check if the directory exists or not. If the directory does not exist,
    #   either by running the app for the first time, or deleting the director(y/ies),
    #   please create a new one, automatically.

    # Directories to check:
    # 1. The directory for the folders containing report files
    # 2. The directory for the folders containing nameserver data
    # 3. The directory for the folders containing domain data
    # 4. The directory for the config file

    _confirm_dir()

    # Folders are checked. Nice.
    # Secondly, we need a "temporary" storage for the app.

    # Before that, we should load the config

    # and we now have the data from the loaded config...

    # This storage will (hypothetically) carry data through windows.

    new_storage = LocalStorage()

    # Storage is there.
    # Now, Main Window should be loaded now.
    # And now we load the window.
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(new_storage)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

