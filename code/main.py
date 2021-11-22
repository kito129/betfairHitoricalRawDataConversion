##
# BETFAIR TO JSON SCRIPT
# AUTHOR: MARCO SELVA
# DATE CREATION 11/06/2020
# VERSION: 2.00
# #
# v1.00: 11/06/2020
# v2.00: 11/14/2021

# ##
#  --- IMPORT OTHER MODULE ---
# ##

from logging import error
import decompress
import dataframe
import dfToObject
import pprint
import json
import utils
from object.runners import RunnersDB
import os


# ##
#  --- PATH TO DATA ---
# ##

# ##
#  --- GLOBAL VARIABLES ---

def main(rawDataPath, workPath, dataType):


    # ##
    #  --- EXTRACTION FILE BZ2 -> JSON ---
    # ##
    print('\n\n------ 1 -EXTRACTION------ \n\n')
    # extract all raw data in workPath
    #decompress.extractJson(rawDataPath, workPath)
  

    # ##
    #  --- JSON TO DATAFRAMA ---
    # ##
    print('\n\n------ 2 -CREATING DATAFRAME------ \n\n')

    rawJSON = []
    df = []
    marketList = []

    dfCounter = 0
    for (dirPath, dirNames, files) in os.walk(workPath):
        for fileName in files:
            currentFile = str(dirPath) + str(fileName)
            rawJSON.append(currentFile)
            try:
                rawDataframe = dataframe.createMainDataframe(currentFile, dataType)
                df.append(rawDataframe)
                dfCounter += 1
            except Exception as e:
                print(e)
               
    pprint.pprint('N OF CORRECT DATAFRAME: ' + str(dfCounter))



    # ##
    #  --- DATAFRAME TO PYTHON OBJECT ---
    # ##
    print('\n\n------ 3 -MY OBJECT CREATION------ \n\n')
    marketCounter = 0
    for data in df:
        marketList.append(dfToObject.convertToMyObject(data, rawJSON[marketCounter], dataType))
        marketCounter = marketCounter + 1

    pprint.pprint('N OF CORRECT OBJECT: ' + str(marketCounter))

    # save Market as JSON
    for _market in marketList:
        utils.saveMarketJSON(_market)


    # ##
    #  --- RUNNERS DB CREATOR ---
    # ##
    print('\n\n------ 4 -GENEREATE RUNNERS INFO------')
    runnersDB = RunnersDB()
    for marketList in marketList:
        runnersDB.saveRunnersOfMarket(marketList)

    # save RunnersDB as JSON
    utils.saveRunnersJSON(runnersDB)

    print('\n\n------ COMPLETE ------')
