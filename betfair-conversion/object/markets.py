from datetime import datetime
import pprint


# definition of class Market
class MarketInfo:

    # empty constructor
    def default(self, o):
        return o.__dict__

        # default constructor

    def __init__(self, obj, status: str, sport: str):
        self.status = status
        # get the last market update with correct openDate
        lastMarketUpdate = obj['data'][-1]

        #convert open date to unix time in ms
        openDate = int(datetime.fromisoformat(lastMarketUpdate[4][:-1]).timestamp()) * 1000

        # volume for ADVANCED
        if status == 'ADVANCED':
            self.info = {
                "id": lastMarketUpdate[1],
                "eventId": lastMarketUpdate[2],
                "eventName": lastMarketUpdate[6],
                "marketType": lastMarketUpdate[3],
                "openDate": openDate,
                "name": lastMarketUpdate[7],
                "numberOfActiveRunners": lastMarketUpdate[8],
                # is not always present but where there i need to copy here
                "countryCode": lastMarketUpdate[obj["columns"].index("countryCode")] if "countryCode" in obj["columns"] else "",
                # this will be complited with info based on where the file is placed
                "sport": sport,
                # is not always present but where there i need to copy here
                "venue": lastMarketUpdate[obj["columns"].index("venue")] if "venue" in obj["columns"] else "",
                # will comleted in second time, only for advanded data
                "volume": {
                    "total": 0,
                    "preMatch": 0,
                    "inPlay": 0
                }
            }
        elif status == 'BASIC':

            self.info = {
                "id": lastMarketUpdate[1],
                "eventId": lastMarketUpdate[2],
                "eventName": lastMarketUpdate[6],
                "marketType": lastMarketUpdate[3],
                "openDate": openDate,
                "name": lastMarketUpdate[7],
                "numberOfActiveRunners": lastMarketUpdate[8],
                # same comment ad advanced
                "countryCode": lastMarketUpdate[obj["columns"].index("countryCode")] if "countryCode" in obj["columns"] else "",
                "sport": sport,
                "venue": lastMarketUpdate[obj["columns"].index("venue")] if "venue" in obj["columns"] else "",
                # here there aren't info about volume
            }

            # i think we would save a prop like "type": ADVANCED | BASIC here to use in in future

        self.runners = []

    # save market updates in object
    def setMarketUpdates(self, updates):
        self.marketUpdates = updates.marketUpdate

    # add runners in market info
    def setRunners(self, runners):
        if len(runners.winner) > 0:
            tempWinner = {
                "id": runners.winner[1],
                "name": runners.winner[2],
                "status": runners.winner[0],
                "position": runners.winner[3],
            }
            self.info['winner'] = tempWinner

        count = 0
        for run_arr in runners.runners:
            run = {
                "id": run_arr[1],
                "name": run_arr[2],
                "status": run_arr[0],
                "position": run_arr[3],

            }
            self.runners.append(run)
            count += 1

        self.info['numberOfActiveRunners'] = count

    # return true for tennis spec of runners
    def _check_tennis(self, runners):
        for run in runners.runners:
            if ("The Draw" in str(run[2])) or ("over" in str(run[2])) or ("under" in str(run[2])):
                return False
            pass
        return True

    # return true for football spec of runners
    def _check_football(self, runners):
        for run in runners.runners:
            if "The Draw" in str(run[2]):
                return True
            pass
        return False

    # update object filed with passed odds main obj
    def setOdds(self, odds):
        self.odds = odds
        # order odds by timestamp
        for lista in self.odds:
            lista['odds'].sort(key=lambda x: x['timestamp'])

    # fix inlay time / error
    def fixUpdates(self):
        # start the routine to fix the openDate (inPlay) error
        
        # the current open time
        inPlayTime = 0
        # find open time for market Update
        for elem in self.marketUpdates:
            if elem['inPlay'] and elem['status'] == 'OPEN' and elem['betDelay'] > 0 :
                inPlayTime = int(elem['timestamp'])
                break

        self.info['openDate'] = int(inPlayTime / 1000000)
        self.info['delay'] = self.marketUpdates[len(self.marketUpdates)-1]['betDelay']

    # update odds for status in updates
    def updateRunnersStats(self):
        inPlay = self.info['openDate']
        runners = self.runners
        odds = self.odds

        # find inplay for all runners
        for run in runners:
            sumPrematch = 0
            stepCounter = 0
            contPrematch = 0
            maxPrematch = -100
            minPrematch = 1001
            maxInPlay = -100
            minInPlay = 1001
            found = False

            # volume for runner
            preMatchVolume = 0

            # iterate over odds
            for odd in odds:
                if odd['runnerId'] == run['id']:
                    # find inPlay index
                    inPlayindex = int(self._find_inPlay_index(odd, inPlay))
                    if len(odd['odds']) > 0 and inPlayindex > -1:
                        for _odd in odd['odds']:
                            # avg runner prematch odd
                            if stepCounter < inPlayindex:
                                # check if max prematch
                                if _odd['ltp'] > maxPrematch:
                                    maxPrematch = _odd['ltp']
                                # check if min prematch
                                if _odd['ltp'] < minPrematch:
                                    minPrematch = _odd['ltp']
                                # increment prematch counter
                                sumPrematch = sumPrematch + _odd['ltp']
                                contPrematch = contPrematch + 1

                            elif stepCounter >= inPlayindex:
                                # im in INPLAY
                                # set the first inplay ltp as inPlayOdds
                                if not found:
                                    # volume for ADVANCED only (check volume)
                                    if self.status == 'ADVANCED':
                                        preMatchVolume = _odd['tv']
                                    # inPlay time and odds
                                    run['inPlayOdds'] = _odd['ltp']
                                    run['inPlayTime'] = _odd['timestamp']
                                    found = True
                                # check if max inplay
                                if _odd['ltp'] > maxInPlay:
                                    maxInPlay = _odd['ltp']
                                # check if min inplay
                                if _odd['ltp'] < minInPlay:
                                    minInPlay = _odd['ltp']
                            # increment step counter
                            stepCounter = stepCounter + 1
                        # avg odds prematch 
                        if contPrematch != 0:
                            run['avgPrematch'] = round(sumPrematch / contPrematch,2)
                        else:
                            run['avgPrematch'] = 0
                        # closed odds
                        run['closedOdds'] = odd['odds'][len(odd['odds']) - 1]['ltp']
                        # max and min prematch
                        run['maxPrematch'] = maxPrematch
                        run['minPrematch'] = minPrematch
                        # max and min inPlay
                        run['maxInPlay'] = maxInPlay
                        run['minInPlay'] = minInPlay
                        # odds metadata
                        run['inPlayIndex'] = inPlayindex
                        run['lengthOdds'] = stepCounter
                        run['lengthOddsPrematch'] = contPrematch
                        run['lengthOddsInPlay'] = stepCounter - contPrematch
                        # volume for ADVANCED
                        if self.status == 'ADVANCED':
                            run['tradedVolume'] = round(odd['odds'][len(odd['odds']) - 1]['tv'],2)
                            run['preMatchVolume'] = round(preMatchVolume, 2)
                            run['inPlayVolume'] = round(run['tradedVolume'] - preMatchVolume,2)
                    # no odds for this runner
                    else:
                        run['inPlayOdds'] = 0
                        run['openOdds'] = 0
                        run['closedOdds'] = 0
                        run['maxPrematch'] = None
                        run['minPrematch'] = None
                        run['maxInPlay'] = 0
                        run['minInPlay'] = 0
                        # volume for ADVANCED
                        if self.status == 'ADVANCED':
                            run['tradedVolume'] = 0
                            run['preMatchVolume'] = 0
                            run['inPlayVolume'] = 0

    # update total market volume based on runner traded volume
    def updateVolume(self):
        for runnerVol in self.runners:
            self.info['volume']['total'] = round(self.info['volume']['total'] +  runnerVol['tradedVolume'],2)
            self.info['volume']['preMatch'] = round(self.info['volume']['preMatch'] +  runnerVol['preMatchVolume'],2)
            self.info['volume']['inPlay'] = round(self.info['volume']['inPlay'] +  runnerVol['inPlayVolume'],2)

    # find inPlay index for this runner
    def _find_inPlay_index(self, runnerOdds, inPlayTime):
        for (i, value) in enumerate(runnerOdds['odds']):
            if value['timestamp'] - inPlayTime >= 0:
                return i
        return -1

    # print main market
    def printMarketJSON(self):
        print("\n -------- MARKET ---------\n")
        print("\nMARKET INFO")
        pprint.pprint(self.info)
        print("\nMARKET UPDATES")
        pprint.pprint(self.marketUpdates)
        print("\nMARKET RUNNERS")
        pprint.pprint(self.runners)
        print("\nMARKET ODDS")
        #pprint.pprint(self.odds)



# definition of class Market
class MarketUpdate:

    # default constructor
    def __init__(self, obj):

        self.marketUpdate = []
        updates = obj['data']

        for up in updates:
            timeStamp = int(up[0].value / 1000000)
            self.marketUpdate.append({
                "timestamp": timeStamp,
                "openDate": up[4],
                "status": up[5],
                "betDelay": up[8],
                "inPlay": up[9],
                "complete": up[10],
            })


  