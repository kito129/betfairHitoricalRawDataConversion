"""
File Loaders - Extract all market files
"""

import os
from pathlib import Path
from typing import List, Dict, Union

from settings import PathConfig

__author__ = "Daniel Ndegwa"
__credits__ = ["Daniel Ndegwa, MARCO SELVA"]


def load_raw_files() -> Dict[str, Dict[str, List[Union[str, Path]]]]:
    """
    Load raw files and categorizes into a dictionary

    {"BASIC": {'HORSE RACING': [], 'SOCCER':[], 'TENNIS':[]}, "ADVANCED": {'HORSE RACING': [], 'SOCCER':[], 'TENNIS':[]}}

    :return: a dictionary with raw files
    """
    loaded_files = {"BASIC": {}, "ADVANCED": {}}

    dirs_ = [
        PathConfig.RAW_DATA_BASIC_SOCCER,
        PathConfig.RAW_DATA_BASIC_TENNIS,
        PathConfig.RAW_DATA_BASIC_HORSE_RACING,
        PathConfig.RAW_DATA_ADVANCED_SOCCER,
        PathConfig.RAW_DATA_ADVANCED_TENNIS,
        PathConfig.RAW_DATA_ADVANCED_HORSE_RACING
    ]

    for dir_ in dirs_:
        dir_files = []
        for root, dirs, files in os.walk(dir_):
            full_paths = list(map(lambda file_: os.path.join(root, file_), files))
            dir_files.extend(full_paths)

        loaded_files[dir_.parent.name.upper()][dir_.name] = dir_files

    return loaded_files
