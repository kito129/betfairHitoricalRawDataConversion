##
# BETFAIR TO JSON SCRIPT
# AUTHOR: MARCO SELVA
# DATE CREATION 11/06/2020
# VERSION: 2.00
# #
# v1.00: 11/06/2020
# v2.00: 11/14/2021

import logging
import os
from pathlib import Path
from typing import Dict, Union, List, Tuple

from pandas import DataFrame

import dataframe
import decompress
import dfToObject
import utils
from object.runners import RunnersDB

__author__ = "Daniel Ndegwa, MARCO SELVA"
__credits__ = ["Daniel Ndegwa, MARCO SELVA"]


def single_sport(raw_data_files: List[Union[str, Path]], sport: str, category: str) -> None:
    """
    Process Single sport in one category(data_type)

    :param raw_data_files: a list of raw files
    :param sport: sport being processed
    :param category: category/data_type i.e BASIC or ADVANCED
    """
    raw_data = {category: {sport: raw_data_files}}
    logging.info('------ 1 -EXTRACTION------ ')
    # extract all raw data in workPath
    json_files = decompress.extract_json(raw_data)

    _new_main(json_files)


def all_sports(raw_data: Dict[str, Dict[str, List[Union[str, Path]]]]) -> None:
    """
    Process all files and all sports and category

    :param raw_data: a dictionary with raw files categorised by sport and category data_type
    """
    logging.info('------ 1 -EXTRACTION------ ')
    # extract all raw data in workPath
    json_files = decompress.extract_json(raw_data)

    _new_main(json_files)


def _new_main(json_files: List[Tuple[str, str]]) -> None:
    logging.info('------ 2 -CREATING DATAFRAME------ ')

    df_counter = 0

    df_json_files = []  # type: List[Tuple[DataFrame, str, str]]
    for currentFile, dataType in json_files:
        try:
            raw_dataframe = dataframe.createMainDataframe(currentFile, dataType)
            df_json_files.append((raw_dataframe, currentFile, dataType))
            df_counter += 1
        except Exception as e:
            print(e)

    logging.info('NO. OF CORRECT DATAFRAME: ' + str(df_counter))

    # ##
    #  --- DATAFRAME TO PYTHON OBJECT ---
    # ##
    logging.info('------ 3 -MY OBJECT CREATION------')
    market_list = []
    for data, js_file, data_type in df_json_files:
        market_list.append(dfToObject.convertToMyObject(data, js_file, data_type))

    logging.info(f'NO. OF CORRECT OBJECT: {len(df_json_files)}')

    # save Market as JSON
    for _market in market_list:
        utils.saveMarketJSON(_market)

    # ##
    #  --- RUNNERS DB CREATOR ---
    # ##
    logging.info('------ 4 -GENEREATE RUNNERS INFO------')
    runners_db = RunnersDB()
    for market_list in market_list:
        runners_db.saveRunnersOfMarket(market_list)

    # save RunnersDB as JSON
    utils.saveRunnersJSON(runners_db)

    logging.info('------ COMPLETE ------')


def main(raw_data_path, work_path, data_type):
    # ##
    #  --- EXTRACTION FILE BZ2 -> JSON ---
    # ##
    logging.info('------ 1 -EXTRACTION------ ')
    # extract all raw data in workPath
    decompress.extract_json(raw_data_path)

    # ##
    #  --- JSON TO DATAFRAME ---
    # ##
    logging.info('------ 2 -CREATING DATAFRAME------ ')

    raw_json = []
    df = []
    market_list = []

    df_counter = 0
    for (dirPath, dirNames, files) in os.walk(work_path):
        for fileName in files:
            current_file = str(dirPath) + str(fileName)
            raw_json.append(current_file)
            try:
                raw_dataframe = dataframe.createMainDataframe(current_file, data_type)
                df.append(raw_dataframe)
                df_counter += 1
            except Exception as e:
                print(e)

    logging.info('NO. OF CORRECT DATAFRAME: ' + str(df_counter))

    # ##
    #  --- DATAFRAME TO PYTHON OBJECT ---
    # ##
    logging.info('------ 3 -MY OBJECT CREATION------')
    market_counter = 0
    for data in df:
        market_list.append(dfToObject.convertToMyObject(data, raw_json[market_counter], data_type))
        market_counter = market_counter + 1

    logging.info('NO. OF CORRECT OBJECT: ' + str(market_counter))

    # save Market as JSON
    for _market in market_list:
        utils.saveMarketJSON(_market)

    # ##
    #  --- RUNNERS DB CREATOR ---
    # ##
    logging.info('------ 4 -GENEREATE RUNNERS INFO------')
    runners_db = RunnersDB()
    for market_list in market_list:
        runners_db.saveRunnersOfMarket(market_list)

    # save RunnersDB as JSON
    utils.saveRunnersJSON(runners_db)

    logging.info('------ COMPLETE ------')
