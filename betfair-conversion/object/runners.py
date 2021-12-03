import pprint
import json


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
            count = count + 1
            self.runners.append(runner)
            if runner[0] == "WINNER":
                self.winner = runner
                pass
            pass
        self.runnerCount = count

# save runners list in JSON
def _save_runners_to_JSON(runnersList, path):
    print("Saving runners list in " + str(path) + "\n\n")

    with open(path, 'w') as outfile:
        json.dump(runnersList, outfile)


# read JSON runners list and return the object
def _read_JSON_runners(path):
    print("Reading runners list in " + str(path) + "\n\n")

    with open(path) as json_file:
        data = json.load(json_file)

    return data


class RunnersDB:
    # empty constructor
    def __init__(self):
        self.runners = {}

    # iterate over runner of this match and check if it's present
    def save_market(self, market):
        for runner in market.runners:
            runner_id = runner["id"]
            if not self.contains(runner_id):
                self.runners[runner_id] = runner

    # get runner if present, -1 if is not present
    def contains(self, runner_id):
        return runner_id in self.runners
