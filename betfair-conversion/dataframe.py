import json

from loguru import logger
import pandas as pd

from object.markets import MarketInfo, MarketUpdate
from object.odds import Odds
from object.runners import Runners


# read JSON file and save in primary python list
def jsonFilesToList(path):
    json_lines = []
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                json_lines.append(json.loads(line))
    except (IOError, json.decoder.JSONDecodeError) as e:
        logger.error("Error in decoding JSON!")
        raise e
    return json_lines


# ##
#  --- GET MAIN OBJECT: MARKETS,RUNNERS, PRICE ---
# ##

# returns MARKET in this file
def getMarkets(path):
    json_list = jsonFilesToList(path)
    markets = []
    clock = ""
    _id = ""
    for entry in json_list:
        mc = entry['mc'][0]
        clock = entry['pt']
        _id = mc['id']
        try:
            market = mc['marketDefinition']
            market['clk'] = clock
            market['id'] = _id
            markets.append(market)
        except KeyError:
            pass

    return {'markets': markets}


# Returns RUNNERS in this file
def getRunners(path):
    json_list = jsonFilesToList(path)
    runners = []
    for entry in json_list:
        mc = entry['mc'][0]
        try:
            runner = mc['marketDefinition']['runners']
            runners.append(runner)
        except KeyError:
            pass

    return {'runners': runners}


# Returns PRICE in this file
def getPricesAndRunners(path):
    json_list = jsonFilesToList(path)
    prices = []
    runners = []
    for entry in json_list:
        mc = entry['mc'][0]
        try:
            runner_sublist = mc['marketDefinition']['runners']
            for runner in runner_sublist:
                runners.append(runner)
        except KeyError:
            pass
        try:
            for item in mc['rc']:
                item['pt'] = entry['pt']
                prices.append(item)
        except KeyError:
            pass

    return {'prices': prices, 'runners': runners}


# ##
#  --- DATAFRAME OF MAIN OBJECT: MARKET,RUNNERS, PRICE ---
# ##

# Returns PANDA dataframe MARKETS in this file
def getMarketDataframe(path):
    try:
        _markets = getMarkets(path)
        markets = _markets['markets']
        markets_df = (pd.DataFrame.from_records(markets)
                      .assign(publish_time=lambda df: pd.to_datetime(df['clk'], unit='ms')))
        markets_df = (markets_df.reindex(columns=markets_df.columns.union(["countryCode", "venue"]))
        [['publish_time', 'id', 'eventId', 'marketType', 'openDate', 'status', 'eventName', 'name', 'betDelay',
          'inPlay', 'numberOfActiveRunners', 'version', "countryCode", "venue"]])
    except KeyError as e:
        logger.error('A MARKET INFO error occurred')
        raise e

    return markets_df


# Returns PANDA dataframe RUNNERS in this file
def getRunnerDataframe(path):
    try:
        prices_and_runners = getPricesAndRunners(path)
        runners = prices_and_runners['runners']

        runner_ids_df = (pd.DataFrame.from_records(runners)
            .drop_duplicates('sortPriority', keep='last')
        [['status', 'id', 'name', 'sortPriority']])

        # print(tabulate( runner_ids_df, tablefmt="pipe", headers="keys"))

        # print("Correctly get market runners dataframe..")
    except KeyError as e:
        logger.error('A RUNNER INFO error occurred')
        raise e

    return runner_ids_df


# Returns PANDA dataframe PRICE AND RUNNERS in this file
def getPricesDataframe(path, status):
    prices_and_runners = getPricesAndRunners(path)
    prices = prices_and_runners['prices']
    runners = prices_and_runners['runners']
    runner_ids_df = (pd.DataFrame.from_records(runners)
                     .drop_duplicates('id'))
    prices_df_long = pd.DataFrame.from_records(prices)
    if len(prices_df_long) == 0:
        return prices_df_long
    prices_df_long = (prices_df_long
                      .eval('odds=ltp', inplace=False)
                      .assign(publish_time=lambda df: pd.to_datetime(df['pt'], unit='ms'))
                      .drop(['ltp', 'pt'], axis=1)
                      .merge(runner_ids_df[['id', 'name', 'sortPriority']], on='id')
                      .rename(columns={'id': 'runner_id', 'name': 'runner_name'}))
    if status == "BASIC":
        columns = ['publish_time', 'runner_id', 'runner_name', 'odds', 'sortPriority']
    elif status == "ADVANCED":
        columns = ['publish_time', 'runner_id', 'runner_name', 'odds', 'tv', 'trd', 'batb', 'batl', 'sortPriority']
    prices_df_long = prices_df_long.reindex(columns=prices_df_long.columns.union(columns))

    try:
        prices_df_long = prices_df_long[columns]
    except KeyError as e:
        logger.error('A PRICE error occurred')
        raise e

    return prices_df_long


def createMainDataframe(path, status):
    try:
        main_obj = {
            'market': getMarketDataframe(path),
            'runners': getRunnerDataframe(path),
            'odds': getPricesDataframe(path, status),
        }
        return main_obj
    except Exception as e:
        logger.error(f"Error creating dataframe from path {path}")
        raise e


# get data frame and convert to main object
def convertToObj(dataframe, status: str, sport: str):
    # print("Start in converting dataframe to object..")

    # convert to dict
    marketInfo = dataframe['market'].to_dict(orient="split")
    marketSelections = dataframe['runners'].to_dict(orient="split")
    marketPrices = dataframe['odds'].to_dict(orient="split")

    # main market info --> 1/3 part of object
    mainMarket = MarketInfo(marketInfo, status, sport)

    # main market update --> part of object market
    mainMarketUpdate = MarketUpdate(marketInfo)
    # update mainMarket with the updates of market
    mainMarket.setMarketUpdates(mainMarketUpdate)

    # runners --> 2/3 part of object
    mainRunners = Runners(marketSelections)
    mainMarket.setRunners(mainRunners)

    # odds --> 3/3 part of object
    mainOdds = Odds(marketPrices, mainRunners, status)
    # update market with odds
    mainMarket.setOdds(mainOdds.odds)

    # fix start match error
    mainMarket.fixUpdates()

    # update updates with odds for the status
    mainMarket.updateRunnersStats()

    # update marketinfo with metadata
    mainMarket.addMetadata()

    # update volume in market info if is ADVANCED
    if status == 'ADVANCED':
        mainMarket.updateVolume()

    # print market info, updates and runners stats
    # mainMarket.printMarketJSON()
    # print("\nConverted", mainMarket.info['name'], 'to first version JSON')

    return mainMarket
