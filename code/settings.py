from pathlib import Path

__author__ = "Daniel Ndegwa"
__credits__ = ["Daniel Ndegwa, MARCO SELVA"]

BASE_DIR = Path(__file__).resolve(True).parent.parent


# the path were al files are extract, you have to separate file extracted by sport and by type of data
# Destination DATA files locations
class PathConfig:
    # WORK_DIR = BASE_DIR / "code/rawInput/"
    WORK_DIR = BASE_DIR / "code/tmp/"

    DATA_ADVANCED_SOCCER = WORK_DIR / 'ADVANCED/SOCCER/'
    DATA_ADVANCED_TENNIS = WORK_DIR / 'ADVANCED/TENNIS/'
    DATA_ADVANCED_HORSE_RACING = WORK_DIR / 'ADVANCED/HORSE RACING/'

    DATA_BASIC_SOCCER = WORK_DIR / "BASIC/SOCCER/"
    DATA_BASIC_TENNIS = WORK_DIR / "BASIC/TENNIS/"
    DATA_BASIC_HORSE_RACING = WORK_DIR / "BASIC/HORSE RACING/"

    # RAW files locations
    RAW_DATA_DIR = BASE_DIR / "rawData"

    RAW_DATA_ADVANCED_SOCCER = RAW_DATA_DIR / 'ADVANCED/SOCCER/'
    RAW_DATA_ADVANCED_TENNIS = RAW_DATA_DIR / 'ADVANCED/TENNIS/'
    RAW_DATA_ADVANCED_HORSE_RACING = RAW_DATA_DIR / 'ADVANCED/HORSE RACING/'

    RAW_DATA_BASIC_SOCCER = RAW_DATA_DIR / 'BASIC/SOCCER/'
    RAW_DATA_BASIC_TENNIS = RAW_DATA_DIR / 'BASIC/TENNIS/'
    RAW_DATA_BASIC_HORSE_RACING = RAW_DATA_DIR / 'BASIC/HORSE RACING/'
