import os

ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
SRC_FOLDER = os.path.join(ROOT_FOLDER, "src")
MAIN_FOLDER = os.path.join(SRC_FOLDER, "main")
TEST_FOLDER = os.path.join(MAIN_FOLDER,"test")
MOCK_DATA_FOLDER = os.path.join(TEST_FOLDER, "mockData")

UI_SKETCH_FOLDER = os.path.join(ROOT_FOLDER, "AppResources")
UI_FINAL_FOLDER = os.path.join(ROOT_FOLDER, "src/UI")
DEFAULT_APP_DATA_FOLDER = os.path.join(ROOT_FOLDER, "data")
DEFAULT_NAMESERVER_DATA_LOC = os.path.join(DEFAULT_APP_DATA_FOLDER,"nameservers")
DEFAULT_DOMAIN_DATA_LOC = os.path.join(DEFAULT_APP_DATA_FOLDER, "domains")
DEFAULT_RESULTS_LOC = os.path.join(DEFAULT_APP_DATA_FOLDER,"reports")

APP_RESOURCES_FOLDER = os.path.join(ROOT_FOLDER,'AppResources')
ASSETS_FOLDER = os.path.join(APP_RESOURCES_FOLDER,'assets')
IMAGE_LOC = os.path.join(ASSETS_FOLDER, 'info-icon-23834 (1).png')

YANFEI_SMUG = os.path.join(ASSETS_FOLDER,'yanfei_smug.ico')

VALID_CONFIG_KEYWORDS = ['instance_count', 'domains_used']
