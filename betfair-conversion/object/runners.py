from os import PathLike

import simplejson as json

from .markets import MarketInfo
import pymongo


# ##
#  --- DATAFRAME TO OBJECT ---
# ##

# definition of class Runners
class Runners:
    runners = []
    winner = {}
    runnerCount = 0

    # default constructor
    def __init__(self, obj):
        self.runners = []
        count = 0
        for runner in obj['data']:
            count += 1

            # Remove position from horse name
            split = runner[2].partition(". ")
            try:
                int(split[0])
                runner[2] = split[-1]
            except ValueError:
                pass

            self.runners.append(runner)
            if runner[0] == "WINNER":
                self.winner = runner
                pass
            pass
        self.runnerCount = count


class RunnersDB:
    # empty constructor
    def __init__(self):
        self.runners = {}

    # iterate over runner of this match and check if it's present
    def saveRunnersDb(self, market: MarketInfo):
        for runner in market.runners:
            runner_id = runner["id"]
            if not self.contains(runner_id):
                self.runners[runner_id] = {"id": runner["id"], "name": runner["name"], "sport": market.info["sport"]}




    # get runner if present, -1 if is not present
    def contains(self, runner_id: int):
        return runner_id in self.runners

    def save(self, path: PathLike):
        with open(path, "w") as runners_file:
            json.dump(list(self.runners.values()), runners_file, ignore_nan=True)

        #for runner in self.runners:
            #saveRunnersInMongo(runner)


def saveRunnersInMongo(runner):
    client = pymongo.MongoClient(
        "mongodb+srv://marco:4Nr1fD8mAOSypUur@cluster1.fzsll.mongodb.net/bf_historical?retryWrites=true&w=majority")
    db = client.bf_historical

    # upload in db
    find = db.runners.find_one({"id": runner['id']})
    if not find:
        db.runners.insert_one(runner)