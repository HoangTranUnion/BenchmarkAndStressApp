from pynotifier import Notification
from settings import YANFEI_SMUG, YANFEI_SMUG_LINUX
import sys


def send_notification(title, msg, time = 5):
    if sys.platform.startswith('win32'):
        icon_path = YANFEI_SMUG
        Notification(title=title, description = msg, icon_path = icon_path, duration=time).send()
    elif sys.platform.startswith('linux'):
        icon_path = YANFEI_SMUG_LINUX
        Notification(title=title, description= msg, icon_path = icon_path, duration= time).send()


if __name__ == "__main__":
    send_notification("Finished benchmarking", "Please check the app")
