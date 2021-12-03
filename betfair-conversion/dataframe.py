# ##
#  --- IMPORT ---
# ##

import json

from loguru import logger
import pandas as pd

from object.markets import MarketInfo, MarketUpdate
from object.odds import Odds
from object.runners import Runners


# ##
#  --- FUNCTION ---
# ##

# read JSON file and save in primary python list


def _json_file_to_list(path):
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

# Returns MARKETS in this file
def _get_markets(path):
    json_list = _json_file_to_list(path)
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
def _get_runners(path):
    json_list = _json_file_to_list(path)
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
def _get_prices_and_runners(path):
    json_list = _json_file_to_list(path)
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
def get_market_dataframe(path):
    try:
        _markets = _get_markets(path)
        markets = _markets['markets']
        markets_df = (pd.DataFrame.from_records(markets)
            .assign(publish_time=lambda df: pd.to_datetime(df['clk'], unit='ms'))
        [['publish_time', 'id', 'eventId', 'marketType', 'openDate', 'status', 'eventName', 'name', 'betDelay',
          'inPlay',
          'complete', 'numberOfActiveRunners', 'version']])
        # missing venue and country code cause in some file it could not be present,
        # so we have to check before if present and than save this value

        # print("Correctly get market info dataframe..")
    except KeyError:
        raise Exception('A MARKET INFO error occurred')

    return markets_df


# Returns PANDA dataframe RUNNERS in this file
def get_runner_dataframe(path):
    try:
        prices_and_runners = _get_prices_and_runners(path)
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
def get_prices_dataframe(path, status):
    prices_and_runners = _get_prices_and_runners(path)
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
        prices_df_long = prices_df_long.reindex(columns=prices_df_long.columns.union(["trd"]))

    # raised exception never caught

    try:
        prices_df_long = prices_df_long[columns]
    except KeyError as e:
        logger.error('A PRICE error occurred')
        raise e

    return prices_df_long


def create_main_dataframe(path, status):
    try:
        main_obj = {
            'market': get_market_dataframe(path),
            'runners': get_runner_dataframe(path),
            'odds': get_prices_dataframe(path, status),
        }
        return main_obj
    except Exception as e:
        logger.error(f"Error creating dataframe from path {path}")
        raise e


def print_dataframe(dataframe):
    print("MARKET INFO:\n")
    print(dataframe['market'])
    print("\nRUNNERS:\n")
    print(dataframe['runners'])
    print("\nODDS:\n")
    print(dataframe['odds'])


# get data frame and convert to main object
def convert_to_obj(dataframe, status):
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

    # TODO update market sports, TO FIX here we don't need this function cause sport no is determined by folder name where the file is placed
    mainMarket.setSport(mainRunners)

    # odds --> 3/3 part of object
    mainOdds = Odds(marketPrices, mainRunners, status)
    # update market with odds
    mainMarket.setOdds(mainOdds.odds)

    # fix start match error
    mainMarket.fixUpdates()

    # update updates with odds for the status
    mainMarket.updateRunnersStats()

    # update volume in market info if is ADVANCED
    if status == 'ADVANCED':
        mainMarket.updateVolume()

    # print market info, updates and runners stats
    #mainMarket.printMarketJSON()
    #print("\nConverted", mainMarket.info['name'], 'to first version JSON')


    return mainMarket
