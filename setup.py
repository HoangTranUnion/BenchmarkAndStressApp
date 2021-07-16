import PyInstaller.__main__
from settings import YANFEI_SMUG, MAIN_SCRIPT

PyInstaller.__main__.run(
    [
        '{}'.format(MAIN_SCRIPT),
        '--onefile',
        '--windowed',
        '-i{}'.format(YANFEI_SMUG),
        '-nDNS Tester'
        '--clean'
    ]
)

