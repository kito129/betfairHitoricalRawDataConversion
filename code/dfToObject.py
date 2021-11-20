# ##
#  --- IMPORT ---
# ##

import pandas as pd
import pprint

# import object definition
from object.markets import MarketInfo
from object.markets import MarketUpdate
from object.runners import Runners
from object.odds import Odds

import dataframe as data


# ##
#  --- FUNCTION ---
# ##

# get data frame and convert to main object
def convertToMyObject(dataframe, path, status):
    # print("Start in converting dataframe to object..")

    # convert to dict
    marketInfo = dataframe['market'].to_dict(orient="split")
    marketSelections = dataframe['runners'].to_dict(orient="split")
    marketPrices = dataframe['odds'].to_dict(orient="split")

    # main market info --> 1/3 part of object
    mainMarket = MarketInfo(marketInfo, status)

    # main market update --> part of object market
    mainMarketUpdate = MarketUpdate(marketInfo)
    # update mainMarket with the updates of market
    mainMarket.setMarketUpdates(mainMarketUpdate)

    # runners --> 2/3 part of object
    mainRunners = Runners(marketSelections)
    mainMarket.setRunners(mainRunners)

    # update market sports, TO FIX here we don't need this function cause sport no is determined by folder name where the file is placed
    mainMarket.setSport(mainRunners)

    # odds --> 3/3 part of object
    mainOdds = Odds(marketPrices, mainRunners, status)
    # update market with odds
    mainMarket.setOdds(mainOdds.odds)

    # fix start match error
    mainMarket.fixUpdates()

    # update updates with odds for the status
    mainMarket.updateRunnersStats(status)

    # update volume in market info if is ADVANCED
    if status == 'ADVANCED':
        mainMarket.updateVolume()

    # print market info, updates and runners stats
    #mainMarket.printMarketJSON()
    #print("\nConverted", mainMarket.info['name'], 'to first version JSON')


    return mainMarket
