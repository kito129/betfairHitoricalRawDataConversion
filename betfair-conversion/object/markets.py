from datetime import datetime
import pprint


def parse_date(date: str) -> int:
    return int(datetime.fromisoformat(date[:-1]).timestamp()) * 1000


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

        # convert open date to unix time in ms
        openDate = parse_date(lastMarketUpdate[4])

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
                "countryCode": lastMarketUpdate[obj["columns"].index("countryCode")] if "countryCode" in obj[
                    "columns"] else "",
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
                "countryCode": lastMarketUpdate[obj["columns"].index("countryCode")] if "countryCode" in obj[
                    "columns"] else "",
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
            if elem['inPlay'] and elem['status'] == 'OPEN' and elem['betDelay'] > 0:
                inPlayTime = int(elem['timestamp'])
                break

        self.info['openDate'] = int(inPlayTime)
        self.info['delay'] = self.marketUpdates[-1]['betDelay']

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
            inPlayOddsUnder2 = 0
            inPlayOddsOver2 = 0

            # volume for runner
            preMatchVolume = 0

            # iterate over odds
            for odd in odds:
                if odd['runnerId'] == run['id']:
                    # find inPlay index
                    inPlayindex = int(self.findInPlayIndex(odd, inPlay))
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
                                # check if under 2
                                if _odd['ltp'] < 2:
                                    inPlayOddsUnder2 += 1
                                # check if over 2
                                if _odd['ltp'] > 2:
                                    inPlayOddsOver2 += 1
                            # increment step counter
                            stepCounter = stepCounter + 1
                        # avg odds prematch 
                        if contPrematch != 0:
                            run['avgPrematch'] = round(sumPrematch / contPrematch, 2)
                        else:
                            run['avgPrematch'] = 0
                        # closed odds
                        run['closedOdds'] = odd['odds'][len(odd['odds']) - 1]['ltp']
                        # max and min prematch
                        run['maxPrematch'] = maxPrematch if contPrematch else None
                        run['minPrematch'] = minPrematch if contPrematch else None
                        # max and min inPlay
                        run['maxInPlay'] = maxInPlay
                        run['minInPlay'] = minInPlay
                        # odds metadata
                        run['inPlayIndex'] = inPlayindex
                        run['lengthOdds'] = stepCounter
                        run['lengthOddsPrematch'] = contPrematch
                        run['lengthOddsInPlay'] = stepCounter - contPrematch
                        # odds u/o 2
                        run['inPlayOddsOver2'] = inPlayOddsOver2
                        run['inPlayOddsUnder2'] = inPlayOddsUnder2
                        # volume for ADVANCED
                        if self.status == 'ADVANCED':
                            run['tradedVolume'] = round(odd['odds'][len(odd['odds']) - 1]['tv'], 2)
                            run['preMatchVolume'] = round(preMatchVolume, 2)
                            run['inPlayVolume'] = round(run['tradedVolume'] - preMatchVolume, 2)
                            if contPrematch == 0:
                                run["inPlayVolume"] += run["preMatchVolume"]
                                run["preMatchVolume"] = 0
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
            self.info['volume']['total'] = round(self.info['volume']['total'] + runnerVol['tradedVolume'], 2)
            self.info['volume']['preMatch'] = round(self.info['volume']['preMatch'] + runnerVol['preMatchVolume'], 2)
            self.info['volume']['inPlay'] = round(self.info['volume']['inPlay'] + runnerVol['inPlayVolume'], 2)

    # find inPlay index for this runner
    def findInPlayIndex(self, runnerOdds, inPlayTime):
        for (i, value) in enumerate(runnerOdds['odds']):
            if value['timestamp'] - inPlayTime >= 0:
                return i
        return -1

    # add metadeta to market info
    def addMetadata(self):

        tempSuspended = []
        tempClosed = []
        updateAfterInplay = []
        for update in self.marketUpdates:
            if update["betDelay"] > 0 and update["status"] == "SUSPENDED":
                tempSuspended.append(update)
            if update["status"] == "CLOSED":
                tempClosed.append(update)
            if update["betDelay"] > 0 and update['inPlay'] is True:
                updateAfterInplay.append(update)

        suspendTime = tempSuspended[len(tempSuspended) - 1]["timestamp"] if (
                    len(tempSuspended) and tempSuspended[len(tempSuspended) - 1]) else 0
        closeTime = tempClosed[len(tempClosed) - 1]["timestamp"] if tempClosed[len(tempClosed) - 1] else 0
        checkSuspendTimeIsLast = False

        openTime = self.info["openDate"]

        for idx, val in enumerate(self.marketUpdates):
            update = self.marketUpdates[idx]
            if update['status'] == "SUSPENDED" and self.marketUpdates[idx + 1]['status'] == "CLOSED":
                checkSuspendTimeIsLast = True

        runnersCorrectBSP = 0
        runnersPrematchNumberOdds = 0
        runnersInPlayNumberOdds = 0
        try:
            for runner in self.runners:
                if runner['status'] != 'REMOVED':
                    runnersPrematchNumberOdds += runner['lengthOddsPrematch']
                    runnersInPlayNumberOdds += runner['lengthOddsInPlay']
                    runnersCorrectBSP = runnersCorrectBSP + (1 if runner['inPlayTime'] == openTime else 0)
        except KeyError:
            runnersCorrectBSP = 0
            runnersPrematchNumberOdds = 0
            runnersInPlayNumberOdds = 0

        self.info["metadata"] = {
            "inPlayTime": openTime,
            "suspendTime": suspendTime if suspendTime > 0 else 0,
            "inplaySuspendUpdatesNumber": len(tempSuspended),
            "closeTime": closeTime if closeTime > 0 else 0,
            "correctSuspended": not (not suspendTime),
            "inPlayDuration": suspendTime - openTime if (
                    suspendTime > 0 and suspendTime > openTime and checkSuspendTimeIsLast) else closeTime - openTime if closeTime > 0 else 0,
            "haveAdditionalInfo": False,
            "runnersCorrectBSP": runnersCorrectBSP,
            "prematchNumberOddsNumber": runnersPrematchNumberOdds,
            "inplayNumberOddsNumber": runnersInPlayNumberOdds,
            "inplayUpdatesNumber": len(updateAfterInplay),
            "inplayUpdates": updateAfterInplay,
        }


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
                "openDate": parse_date(up[4]),
                "status": up[5],
                "betDelay": up[8],
                "inPlay": up[9],
            })
