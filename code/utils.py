import json
from datetime import datetime
import pprint


# save market (dict) as JSON in path
def saveMarketJSON(file):
    print("Saving MARKET " + file.info['name'] + " in " + './exportOutput/market/' + file.info['id'] + '.json')




    #it doesn't actualy works but here you have to separate by sport the output like /exportOutput/market/TENNIS, /exportOutput/market/SOCCER, /exportOutput/market/HORSE RACING
    t = int(file.info['openDate'] / 1000)
    time = datetime.utcfromtimestamp(t).strftime('%Y_%m_%d')

    # for the check if isnt preset / in file names
    path = './exportOutput/markets/' + time  + '_' + file.info['name'] + '_' +  file.info['id'] + '.json'

    with open(path, 'w') as outfile:
        json.dump(file.__dict__, outfile)


# save runners (list) as JSON in path

#it should save the file with the date so when i upload in the DB i know what is the last runner file to upload
def saveRunnersJSON(runnersDB):

    print('Saving RUNNERS DB in ./exportOutput/runners/runnersDB.json')

    path = './exportOutput/runners/runnersDB.json'

    with open(path, 'w') as outfile:
        json.dump(runnersDB.runners, outfile)

