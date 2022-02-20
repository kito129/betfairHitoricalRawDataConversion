from datetime import datetime
import functools
import json
from multiprocessing import cpu_count, Manager, Pool
from pathlib import Path
import time
import pymongo

from loguru import logger
from pandas import DataFrame
import simplejson as json

from dataframe import createMainDataframe, convertToObj
from paths import PathConfig
from object.markets import MarketInfo
from object.runners import RunnersDB
from sportAdditionalData import get_soccer_matches, get_tennis_matches
from utils import getProgress


# Remove adjacent duplicate rows in market data
def removeMarketUpdatesDuplicates(market: DataFrame) -> DataFrame:
    duplicate_data = market[["openDate", "status", "betDelay", "inPlay"]]
    return market.loc[(duplicate_data.shift() != duplicate_data).any(axis=1)]


def canonizeName(name: str) -> str:
    split = name.split()
    return f"{split[-1]}-{name[0]}"


def processJson(export_dir: Path, sport_info: tuple, path: Path) -> (Path, str, str, MarketInfo):
    soccer_matches, tennis_matches = sport_info

    status = "BASIC" if "BASIC" in path.parts else "ADVANCED"
    sport = path.parts[path.parts.index(status) + 1]
    basic_info = (path, sport, status, None)
    market_json_path = export_dir / "markets" / Path(*path.parts[path.parts.index(status):])
    if market_json_path.exists():
        return basic_info

    try:
        frame = createMainDataframe(path, status)
    except:
        return basic_info

    # remove unsupported markets
    frame["market"] = removeMarketUpdatesDuplicates(frame["market"])

    obj = convertToObj(frame, status, sport)
    info = obj.info

    if obj.status == "REMOVED":
        return basic_info
    # remove unsupported markets
    open_date = datetime.fromtimestamp(info["openDate"] / 1000)
    in_play_length = 0
    # runners
    for runner in obj.runners:
        if runner.get("status") == "REMOVED":
            return basic_info
    if info["openDate"] == 0 \
            or ((sport == "TENNIS" and (
            (open_date.year > 2018 and info["delay"] >= 5) or (open_date.year < 2018 and info["delay"] >= 7)))
                or (sport == "SOCCER" and info["delay"] >= 7)
                or (sport == "TENNIS" and "/" in info["eventName"])
                or (sport == "TENNIS" and info["delay"] == 0)
                or (open_date.year == 2020 and open_date.month in [3, 4, 5, 6, 7])
                or ((sport in ["SOCCER", "TENNIS"]) and (
                    (status == "BASIC" and info["metadata"]["inplayNumberOddsNumber"] < 10) or (
                    status == "ADVANCED" and info["metadata"]["inplayNumberOddsNumber"] < 50)))
    ):
        return basic_info

    renamed_obj = {
        "marketType": obj.status,
        "marketInfo": obj.info,
        "marketRunners": obj.runners,
        "marketUpdates": obj.marketUpdates,
        "marketOdds": obj.odds,
    }

    date = open_date.strftime("%Y-%m-%d")
    # Only add additional info for soccer markets with type MATCH_ODDS
    if sport == "SOCCER" and obj.info["marketType"] == "MATCH_ODDS":
        split = info["eventName"].split(" v ")
        match = f"{date}-{split[0]}-{split[1]}"
        if match in soccer_matches:
            renamed_obj["additionalInfoSoccer"] = soccer_matches[match]
            renamed_obj["additionalInfoTennis"] = {}
            renamed_obj["marketInfo"]["metadata"]["haveAdditionalInfo"] = True
    elif sport == "TENNIS":
        try:
            winner = canonizeName(next(r for r in obj.runners if r["status"] == "WINNER")["name"])
            loser = canonizeName(next(r for r in obj.runners if r["status"] == "LOSER")["name"])
            match = f"{date}-{winner}-{loser}"
            if match in tennis_matches:
                renamed_obj["additionalInfoTennis"] = tennis_matches[match]
                renamed_obj["additionalInfoSoccer"] = {}
                renamed_obj["marketInfo"]["metadata"]["haveAdditionalInfo"] = True
        except StopIteration:
            pass

    if "additionalInfoTennis" not in renamed_obj:
        renamed_obj["additionalInfoTennis"] = {}
        renamed_obj["additionalInfoSoccer"] = {}

    market_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(market_json_path, "w") as market_json_file:
        json.dump(renamed_obj, market_json_file, ignore_nan=True)

    #upload in DB
    upload(renamed_obj)

    return path, sport, status, obj


def upload(market):
    client = pymongo.MongoClient(
        "mongodb+srv://marco:4Nr1fD8mAOSypUur@cluster1.fzsll.mongodb.net/bf_historical?retryWrites=true&w=majority")
    db = client.bf_historical

    marketId = market['marketInfo']['id']
    marketType = market['marketType']
    marketInfo = market['marketInfo']
    marketUpdates = market['marketUpdates']
    marketRunners = market['marketRunners']
    marketOdds = market['marketOdds']
    marketAdditionalInfoTennis = market['additionalInfoTennis']
    marketAdditionalInfoSoccer = market['additionalInfoSoccer']

    # MARKET BASIC
    if market and market['marketType'] == "BASIC":
        find = db.marketInfoBasic.find_one({"marketId": marketId})
        if not find:
            db.marketInfoBasic.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketInfo": marketInfo
            })
        find = db.marketUpdatesBasic.find_one({"marketId": marketId})
        if not find:
            db.marketUpdatesBasic.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketUpdates": marketUpdates
            })
        find = db.marketRunnersBasic.find_one({"marketId": marketId})
        if not find:
            db.marketRunnersBasic.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketRunners": marketRunners
            })
        find = db.marketOddsBasic.find_one({"marketId": marketId})
        if not find:
            db.marketOddsBasic.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketOdds": marketOdds
            })
        if marketAdditionalInfoTennis:
            find = db.marketAdditionalInfoTennis.find_one({"marketId": marketId})
            if not find:
                db.marketAdditionalInfoTennis.insert_one({
                    "marketId": marketId,
                    "marketType": marketType,
                    "marketAdditionalInfoTennis": marketAdditionalInfoTennis
                })
        if marketAdditionalInfoSoccer:
            find = db.marketAdditionalInfoSoccer.find_one({"marketId": marketId})
            if not find:
                db.marketAdditionalInfoSoccer.insert_one({
                    "marketId": marketId,
                    "marketType": marketType,
                    "marketAdditionalInfoSoccer": marketAdditionalInfoSoccer
                })

    # MARKET ADVANCED
    if market and market['marketType'] == "ADVANCED":
        find = db.marketInfoAdvanced.find_one({"marketId": marketId})
        if not find:
            db.marketInfoAdvanced.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketInfo": marketInfo
            })
        find = db.marketUpdatesAdvanced.find_one({"marketId": marketId})
        if not find:
            db.marketUpdatesAdvanced.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketUpdates": marketUpdates
            })
        find = db.marketRunnersAdvanced.find_one({"marketId": marketId})
        if not find:
            db.marketRunnersAdvanced.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketRunners": marketRunners
            })
        find = db.marketOddsAdvanced.find_one({"marketId": marketId})
        if not find:
            db.marketOddsAdvanced.insert_one({
                "marketId": marketId,
                "marketType": marketType,
                "marketOdds": marketOdds
            })
        if marketAdditionalInfoTennis:
            find = db.marketAdditionalInfoTennis.find_one({"marketId": marketId})
            if not find:
                db.marketAdditionalInfoTennis.insert_one({
                    "marketId": marketId,
                    "marketType": marketType,
                    "marketAdditionalInfoTennis": marketAdditionalInfoTennis
                })
        if marketAdditionalInfoSoccer:
            find = db.marketAdditionalInfoSoccer.find_one({"marketId": marketId})
            if not find:
                db.marketAdditionalInfoTennis.insert_one({
                    "marketId": marketId,
                    "marketType": marketType,
                    "marketAdditionalInfoSoccer": marketAdditionalInfoSoccer
                })



def processAllJson(json_paths: list[Path]):
    logger.info(f"Files to process: {len(json_paths)}")
    process_start = time.perf_counter()

    runners_db = RunnersDB()
    now = datetime.now()
    export_output = Path(PathConfig.EXPORT_DIR) / now.strftime("%Y-%m-%d_%H-%M-%S")
    export_output.mkdir(parents=True, exist_ok=True)
    json_input = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"],
                           dtype="Int64").fillna(0)
    json_output = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"],
                            dtype="Int64").fillna(0)

    with getProgress() as progress:
        task = progress.add_task("JSON Files", total=len(json_paths))
        with Pool(processes=cpu_count()) as pool, Manager() as manager:
            soccer_matches = get_soccer_matches(manager.dict())
            tennis_matches = get_tennis_matches(manager.dict())

            for result in pool.imap(functools.partial(processJson, export_output, (soccer_matches, tennis_matches)),
                                    json_paths):
                progress.advance(task)
                path, sport, status, market = result
                json_input.at[sport, status] += 1

                if market:
                    runners_db.saveRunnersDb(market)
                    json_output.at[sport, status] += 1

            # Extra statement is needed to prevent hanging context manager.
            # Q: Why?
            # A: ???
            _ = 1

    runners_db.save(export_output / "runnerDB.json")

    logger.info(f"Processing completed in {time.perf_counter() - process_start:.2f}s")
    logger.info("Input:")
    logger.info(f"\n{json_input}")
    logger.info("Output:")
    logger.info(f"\n{json_output}")
