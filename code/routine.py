import logging

import main
from loader import load_raw_files
from settings import PathConfig

__author__ = "Daniel Ndegwa, MARCO SELVA"
__credits__ = ["Daniel Ndegwa, MARCO SELVA"]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# the path were al files are extract, you have to separate file extracted by sport and by type of data
workPath = PathConfig.WORK_DIR
raw_data_files = load_raw_files()
data_ADVANCED_TENNIS = raw_data_files["ADVANCED"]["TENNIS"]

logging.info("[*] starting the routine")

# main.main(str(data_ADVANCED_TENNIS), str(workPath), 'ADVANCED')
main.single_sport(data_ADVANCED_TENNIS, "TENNIS", 'ADVANCED')

logging.info(' -----  END ADVANCED ----')
logging.info("[*] finished the routine")
