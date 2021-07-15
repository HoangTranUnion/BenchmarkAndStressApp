import subprocess
import sys
import os

from settings import *


def convert(target_name:str):
    if target_name[target_name.rfind('.') + 1:] == 'ui':
        subprocess.check_call([sys.executable, "-m", "PyQt5.uic.pyuic", "-x", target_name,  '-o', target_name[:target_name.rfind('.')]+".py"])


if __name__ == '__main__':
    # for file in os.listdir(UI_FOLDER):
    #     convert(os.path.join(UI_FOLDER,file))

    # list_of_modified_files = ['AddDifferentDomains.ui', 'Benchmark_Properties.ui', 'NewDomainUI.ui','NewMain.ui','RemoveDifferentDomains.ui',
    #                           'ReportUI.ui', 'Stress_Properties.ui']
    # for file in list_of_modified_files:
    #     convert(os.path.join(UI_FOLDER,file))

    convert(os.path.join(UI_FOLDER, 'ReportUI.ui'))


