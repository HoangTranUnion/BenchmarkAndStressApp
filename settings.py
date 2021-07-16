import os

ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
SRC_FOLDER = os.path.join(ROOT_FOLDER, "src")
MAIN_FOLDER = os.path.join(SRC_FOLDER, "main")
TEST_FOLDER = os.path.join(MAIN_FOLDER,"test")
MOCK_DATA_FOLDER = os.path.join(TEST_FOLDER, "mockData")

UI_FOLDER = os.path.join(ROOT_FOLDER, "AppResources")

APP_RESOURCES_FOLDER = os.path.join(ROOT_FOLDER,'AppResources')
ASSETS_FOLDER = os.path.join(APP_RESOURCES_FOLDER,'assets')
IMAGE_LOC = os.path.join(ASSETS_FOLDER, 'info-icon-23834 (1).png')

YANFEI_SMUG = os.path.join(ASSETS_FOLDER,'yanfei_smug.ico')
MAIN_SCRIPT = os.path.join(ROOT_FOLDER, 'main.py')

VALID_CONFIG_KEYWORDS = ['instance_count', 'domains_used']
