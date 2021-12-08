from os import PathLike

import simplejson as json

from .markets import MarketInfo


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
    def save_market(self, market: MarketInfo):
        for runner in market.runners:
            runner_id = runner["id"]
            if not self.contains(runner_id):
                self.runners[runner_id] = {"id": runner["id"], "name": runner["name"], "sport": market.info["sport"]}

    # get runner if present, -1 if is not present
    def contains(self, runner_id: int):
        return runner_id in self.runners

    def save(self, path: PathLike):
        with open(path, "w") as runners_file:
            json.dump(list(self.runners.values()), runners_file, indent=4, ignore_nan=True)
