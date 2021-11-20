# ##
#  --- MONGO CONNECTION CRUD ---
# ##

import pymongo
import certifi
import pprint
from dbStats import DBUploadStats




# ##
#  --- CONNECTION ---
# ##

def connectDB():
    # mongo connection string
    client = pymongo.MongoClient("mongodb+srv://marco:x48sJxAF3rmZ1Vez@cluster0.ajloz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    tlsCAFile=certifi.where())
    # db name
    db = client.bf_historical
    return db


# ##
#  --- CRUD ---
# ##

# CREATE
def _create_doc(db, doc, collection, stats):
    stats._to_add_append(doc.info['id'])


    try:
        if collection == "markets":
            _markets = db.markets
            # check if already present
            if _find_doc(db, doc, collection) is not None:
                stats._error_append(doc.info['id'] + ' markets')
            else:
                _markets.insert(doc.info)
                stats._uploaded_append(doc.info['id'] + ' markets')

        elif collection == "selections":
            _selection = db.selections
            # check if already present
            if _find_doc(db, doc, collection) is not None:
                stats._error_append(doc.selections['marketId'] + ' selections')
            else:
                _selection.insert(doc.selections)
                stats._uploaded_append(doc.selections['marketId'] + ' selections')

        elif collection == "prices":
            _prices = db.prices
            # check if already present
            if _find_doc(db, doc, collection) is not None:
                stats._error_append(doc.prices['marketId'] + ' prices')
            else:
                _prices.insert(doc.prices)
                stats._uploaded_append(doc.prices['marketId'] + ' prices')

        elif collection == "updates":
            _marketUpdates = db.marketUpdates
            # check if already present
            if _find_doc(db, doc, collection) is not None:
                stats._error_append(doc.marketUpdates['marketId'] + ' updates')
            else:
                _marketUpdates.insert(doc.marketUpdates)
                stats._uploaded_append(doc.marketUpdates['marketId'] + ' updates')

        # RUNNERS DB
        elif collection == "runnersDb":
            _runners = db.runners
            # check if already present
            if _find_doc(db, doc, collection) is not None:
                stats._error_append(str(doc.info['id']) + ' runnersDB')
            else:

                _runners.insert(doc.info)
                stats._uploaded_append(str(doc.info['id']) + ' runnersDB')

    except Exception as e:

        print("A MONGO exception occurred ::", e)



# READ
def _find_doc(db, doc, collection):
    resp = ""

    if collection == "markets":
        _markets = db.markets
        resp = _markets.find_one({"id": doc.info['id']})

    elif collection == "selections":
        _selection = db.selections
        resp = _selection.find_one({"marketId": doc.selections['marketId']})

    elif collection == "prices":
        _prices = db.prices
        resp = _prices.find_one({"marketId": doc.prices['marketId']})

    elif collection == "updates":
        _marketUpdates = db.marketUpdates
        resp = _marketUpdates.find_one({"marketId": doc.marketUpdates['marketId']})

    # RUNNERS DB
    elif collection == "runnersDb":
        _runners = db.runners
        resp = _runners.find_one({"id": doc.info['id']})

    return resp


# UPDATE
def _update_doc(db, doc, collection):
    print('1')


# DELETE
def _delete_doc(db, doc, collection):
    print('1')


# ##
#  --- MAIN ---
# ##

def _manage_markets(db, markets, status):
    stats = DBUploadStats()

    # upload market

    if status == 'ADVANCED':
        # info
        _create_doc_advanced(db, markets, 'markets', stats)
        # selections
        _create_doc_advanced(db, markets, 'selections', stats)
        # prices
        _create_doc_advanced(db, markets, 'prices', stats)
        # updates
        _create_doc_advanced(db, markets, 'updates', stats)

    elif status == 'BASIC':
        # info
        _create_doc(db, markets, 'markets', stats)
        # selections
        _create_doc(db, markets, 'selections', stats)
        # prices
        _create_doc(db, markets, 'prices', stats)
        # updates
        _create_doc(db, markets, 'updates', stats)

    print('Uploaded')
    # stats._print_stats()


def _manage_runners(db, runnersDb):
    stats = DBUploadStats()

    # for each runnerDocs
    for runner in runnersDb.runners:
        _create_doc(db, runner, 'runnersDb', stats)

    # print('\n\n\nRunners\n\n\n')
    # stats._print_stats()


# ##
#  --- CRUD ADVANCED DATA ---
# ##

def _create_doc_advanced(db, doc, collection, stats):
    stats._to_add_append(doc.info['id'])

    try:

        if collection == "markets":
            _markets = db.marketsAdvanced
            # check if already present
            if _find_doc_advanced(db, doc, collection) is not None:
                stats._error_append(doc.info['id'] + ' markets')
            else:
                _markets.insert(doc.info)
                stats._uploaded_append(doc.info['id'] + ' markets')

        elif collection == "selections":
            _selection = db.selectionsAdvanced
            # check if already present
            if _find_doc_advanced(db, doc, collection) is not None:
                stats._error_append(doc.selections['marketId'] + ' selections')
            else:
                _selection.insert(doc.selections)
                stats._uploaded_append(doc.selections['marketId'] + ' selections')

        elif collection == "prices":
            _prices = db.pricesAdvanced
            # check if already present
            if _find_doc_advanced(db, doc, collection) is not None:
                stats._error_append(doc.prices['marketId'] + ' prices')
            else:
                _prices.insert(doc.prices)
                stats._uploaded_append(doc.prices['marketId'] + ' prices')

        elif collection == "updates":
            _marketUpdates = db.marketUpdatesAdvanced
            # check if already present
            if _find_doc_advanced(db, doc, collection) is not None:
                stats._error_append(doc.marketUpdates['marketId'] + ' updates')
            else:
                _marketUpdates.insert(doc.marketUpdates)
                stats._uploaded_append(doc.marketUpdates['marketId'] + ' updates')

        # RUNNERS DB
        elif collection == "runnersDb":
            _runners = db.runners
            # check if already present
            if _find_doc(db, doc, collection) is not None:
                stats._error_append(str(doc.info['id']) + ' runnersDB')
            else:

                _runners.insert(doc.info)
                stats._uploaded_append(str(doc.info['id']) + ' runnersDB')


    except Exception as e:

        print("A MONGO exception occurred ::", e)


def _find_doc_advanced(db, doc, collection):
    resp = ""

    if collection == "markets":
        _markets = db.marketsAdvanced
        resp = _markets.find_one({"id": doc.info['id']})

    elif collection == "selections":
        _selection = db.selectionsAdvanced
        resp = _selection.find_one({"marketId": doc.selections['marketId']})

    elif collection == "prices":
        _prices = db.pricesAdvanced
        resp = _prices.find_one({"marketId": doc.prices['marketId']})

    elif collection == "updates":
        _marketUpdates = db.marketUpdatesAdvanced
        resp = _marketUpdates.find_one({"marketId": doc.marketUpdates['marketId']})

    # RUNNERS DB
    elif collection == "runnersDb":
        _runners = db.runnersAdvanced
        resp = _runners.find_one({"id": doc.info['id']})

    return resp
