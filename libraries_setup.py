import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == "__main__":
    package_list = ['PyQt5','numpy','dnspython','datetime','dnspython[doh]','win10toast','requests']
    for package in package_list:
        install(package)