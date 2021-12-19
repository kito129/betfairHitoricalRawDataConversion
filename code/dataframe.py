# ##
#  --- IMPORT ---
# ##

import pandas as pd
import json



# ##
#  --- FUNCTION ---
# ##

# read JSON file and save in primary python list
def _json_file_to_list(path):
    try:
        with open(path, encoding='utf-8') as f:
            data_list = f.readlines()
            json_strings = json.loads(json.dumps(data_list))
            result = [json.loads(json_string) for json_string in json_strings]
            return result
    except:
        print(path)


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
def getMarketDataframe(path):
    try:
        _markets = _get_markets(path)
        markets = _markets['markets']
        markets_df = (pd.DataFrame.from_records(markets)
            .assign(publish_time=lambda df: pd.to_datetime(df['clk'], unit='ms'))
        [['publish_time', 'id', 'eventId', 'marketType', 'openDate', 'status', 'eventName', 'name', 'betDelay', 'inPlay',
        'complete', 'numberOfActiveRunners','version']])
        #missing venue and country code cause in some file it could not be present, so we have to check before if present and than save this value

        # print("Correctly get market info dataframe..")
    except:
        raise Exception('A MARKET INFO error occurred')

    return markets_df


# Returns PANDA dataframe RUNNERS in this file
def getRunnerDataframe(path):
    try:
        prices_and_runners = _get_prices_and_runners(path)
        runners = prices_and_runners['runners']


        runner_ids_df = (pd.DataFrame.from_records(runners)
            .drop_duplicates('sortPriority', keep='last')
        [['status', 'id', 'name', 'sortPriority']])

        # print(tabulate( runner_ids_df, tablefmt="pipe", headers="keys"))

        # print("Correctly get market runners dataframe..")
    except:
        raise Exception('A RUNNER INFO error occurred')

    return runner_ids_df

# Returns PANDA dataframe PRICE AND RUNNERS in this file
def getPricesDataframe(path, status):

    prices_and_runners = _get_prices_and_runners(path)
    prices = prices_and_runners['prices']
    runners = prices_and_runners['runners']
    runner_ids_df = (pd.DataFrame.from_records(runners)
                     .drop_duplicates('id'))

    # BASIC data
    if status == 'BASIC':
        try:
            prices_df_long = (pd.DataFrame.from_records(prices)
                .eval('odds=ltp', inplace=False)
                .assign(publish_time=lambda df: pd.to_datetime(df['pt'], unit='ms'))
                .drop(['ltp', 'pt'], axis=1)
                .merge(runner_ids_df[['id', 'name', 'sortPriority']], on='id')
                .rename(columns={'id': 'runner_id', 'name': 'runner_name'})
            [['publish_time', 'runner_id', 'runner_name', 'odds', 'sortPriority']])

            # print(tabulate( prices_df_long, tablefmt="pipe", headers="keys"))
            return prices_df_long

        except:
            raise Exception('A PRICE error occurred')

    # ADVANCED data
    elif status == 'ADVANCED':
        try:
            prices_df_long = (pd.DataFrame.from_records(prices)
                .eval('odds=ltp', inplace=False)
                .assign(publish_time=lambda df: pd.to_datetime(df['pt'], unit='ms'))
                .drop(['ltp', 'pt'], axis=1)
                .merge(runner_ids_df[['id', 'name', 'sortPriority']], on='id')
                .rename(columns={'id': 'runner_id', 'name': 'runner_name'})
            [['publish_time', 'runner_id', 'runner_name', 'odds', 'tv', 'trd', 'batb', 'batl', 'sortPriority']])



            # onlyfirst10line = prices_df_long[prices_df_long["runner_id"]  == 2249229]
            # last = onlyfirst10line[onlyfirst10line["odds"] >80 ]
            # print(tabulate( last, tablefmt="pipe", headers="keys"))

            return prices_df_long

        except:
            raise Exception('A PRICE error occurred')



def createMainDataframe(path, status):
    try:
        mainObj = {
            'market': getMarketDataframe(path),
            'runners': getRunnerDataframe(path),
            'odds': getPricesDataframe(path, status)
        }
        return mainObj
    except Exception as e:
        raise Exception(e,path)


def printDataframe(dataframe):
    print("MARKET INFO:\n")
    print(dataframe['market'])
    print("\nRUNNERS:\n")
    print(dataframe['runners'])
    print("\nODDS:\n")
    print(dataframe['odds'])
