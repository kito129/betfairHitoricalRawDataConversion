# ##
#  --- IMPORT ---
# ##
import bz2
import concurrent.futures
import logging
import os
from pathlib import Path
from typing import List, Dict, Union, Optional, Tuple

from settings import PathConfig

__author__ = "Daniel Ndegwa, MARCO SELVA"
__credits__ = ["Daniel Ndegwa, MARCO SELVA"]

OptStr = Optional[str]


def extract_json(data: Dict[str, Dict[str, List[Union[str, Path]]]]) -> List[Tuple[Union[str, Path], str]]:
    """
    Extracts all loaded bz2 files to Json files.

    :param data: categorical dictionary of file paths
    """
    flat = []  # List[Tuple[str, str, str]]
    processed_files = []

    for category in data:
        for sport, files in data[category].items():
            for file_ in files:
                flat.append((file_, sport, category))
    total_files = len(flat)

    logging.info(f"Files to process: {total_files}")

    processed, curr_percentage = 0, -1
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for _, json_file_category in zip(flat, executor.map(convert_bz2_to_json_adapter, flat)):
            processed_files.append(json_file_category)
            processed += 1
            percentage = round(processed / total_files, 2) * 100
            # if percentage > curr_percentage:
            logging.info(f"converting_bz2_to_json: -> {percentage:.02f}%")
            curr_percentage = percentage

    logging.info(f"Total Processed (converted) files : {processed}")
    logging.info("Extraction Completed!")

    return processed_files


def convert_bz2_to_json_adapter(file_store_category) -> Tuple[str, str]:
    return convert_bz2_to_json(*file_store_category)


def convert_bz2_to_json(filename, sport: OptStr, category: OptStr) -> Tuple[str, str]:
    """
    Converts a bzip2 into a json file

    If destination filename isn't provided, its created using the matching data directory path in `PathConfig`
    which is created using provide sport and category of the current file.

    :param filename: bzip2 filepath
    :param sport: can be either TENNIS, SOCCER or HORSE RACING
    :param category: the type, either ADVANCED OR BASIC
    """

    if sport is None and category is None:
        raise Exception("Provide destination path or sport and category of the current sport type")

    # save to WORK_DIR
    sport = "_".join(sport.split(" "))  # turns HORSE RACING --> HORSE_RACING
    dest_folder = getattr(PathConfig, f"DATA_{category}_{sport}".upper())
    os.makedirs(dest_folder, exist_ok=True)  # create destination if it doesn't exits
    json_file = str(dest_folder / (Path(filename).name + ".json"))

    with open(json_file, 'wb') as new_file, bz2.BZ2File(filename, 'rb') as file:
        for data in iter(lambda: file.read(), b''):
            new_file.write(data)

    return json_file, category


# loop on all folder in path and extract bz2 to JSON file
def extractJson(dataPath, extractPath):
    print("\nExtracting File...")
    countOK = 0
    for (dirpath, dirnames, files) in os.walk(dataPath):
        for fileName in files:
            # filter out decompressed files
            if fileName.endswith('.json'):
                continue

            # save file as .json
            filepath = os.path.join(dirpath, fileName)
            newFilepath = extractPath + fileName + '.json'

            # save JSON file
            with open(newFilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
                for data in iter(lambda: file.read(), b''):
                    new_file.write(data)
            file.close()
            countOK = countOK + 1

    # print recap
    print("Files Extracted: " + str(countOK))
    print('\nEnd of extraction..\n')
