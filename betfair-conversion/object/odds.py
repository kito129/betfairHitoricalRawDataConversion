import pprint
import pandas as pd


# definition of class Market
class Odds():

    # default constructor
    def __init__(self, obj, runners, status):

        myData = []

        # populate with runner id
        i = 0
        while i < runners.runnerCount:
            temp = {
                "runnerId": runners.runners[i][1],
                "odds": []
            }

            myData.append(temp)
            i += 1

        last = 0
        # run over odds
        for odds in obj['data']:

            for runner in myData:

                if runner['runnerId'] == odds[1] and odds[3]>1 :
                    # TODO to fix this should be timestamp in ms too
                    time = int(odds[0].value / 1000000)

                    # BASIC data
                    if status == 'BASIC':

                        tempOdds = {
                            "timestamp": time,
                            "ltp": odds[3],
                        }
                    # ADVANCED data
                    elif status == 'ADVANCED':

                        # TODO if some value use null and not NaN
                        tempOdds = {
                            "timestamp": time,
                            "ltp": odds[3],
                            "tv": odds[4],
                            "trd": odds[5],
                            "batb": odds[6],
                            "batl": odds[7],
                        }

                    runner['odds'].append(tempOdds)

        self.odds = myData
