from datetime import datetime
import functools
import json
from multiprocessing import cpu_count, Manager, Pool
from pathlib import Path
import time

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
def removeMarketDuplicates(market: DataFrame) -> DataFrame:
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

    frame["market"] = removeMarketDuplicates(frame["market"])
    obj = convertToObj(frame, status, sport)
    info = obj.info
    if obj.status == "REMOVED":
        return basic_info
    open_date = datetime.fromtimestamp(info["openDate"] / 1000)
    in_play_length = 0
    for runner in obj.runners:
        if runner.get("lengthOddsInPlay"):
            in_play_length += runner.get("lengthOddsInPlay")
        if runner.get("status") == "REMOVED":
            return basic_info
    # evaluate to add delay == o -> remove
    if open_date \
            and ((sport == "TENNIS" and (
            (open_date.year > 2018 and info["delay"] >= 5)
            or (open_date.year < 2018 and info["delay"] >= 7)))
            or (sport == "SOCCER" and info["delay"] >= 7)
            or (sport == "TENNIS" and "/" in info["eventName"])
            or (sport in ["SOCCER", "TENNIS"] and in_play_length < 10)):
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
            renamed_obj["additionalInfo"] = soccer_matches[match]
    elif sport == "TENNIS":
        try:
            winner = canonizeName(next(r for r in obj.runners if r["status"] == "WINNER")["name"])
            loser = canonizeName(next(r for r in obj.runners if r["status"] == "LOSER")["name"])
            match = f"{date}-{winner}-{loser}"
            if match in tennis_matches:
                renamed_obj["additionalInfo"] = tennis_matches[match]
        except StopIteration:
            pass

    if "additionalInfo" not in renamed_obj:
        renamed_obj["additionalInfo"] = {}

    market_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(market_json_path, "w") as market_json_file:
        json.dump(renamed_obj, market_json_file, ignore_nan=True)

    return path, sport, status, obj


def processAllJson(json_paths: list[Path]):
    logger.info(f"Files to process: {len(json_paths)}")
    process_start = time.perf_counter()

    runners_db = RunnersDB()
    now = datetime.now()
    export_output = Path(PathConfig.EXPORT_DIR) / now.strftime("%Y-%m-%d_%H-%M-%S")
    export_output.mkdir(parents=True, exist_ok=True)
    json_input = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)
    json_output = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)

    with getProgress() as progress:
        task = progress.add_task("JSON Files", total=len(json_paths))
        with Pool(processes=cpu_count()) as pool, Manager() as manager:
            soccer_matches = get_soccer_matches(manager.dict())
            tennis_matches = get_tennis_matches(manager.dict())

            for result in pool.imap(functools.partial(processJson, export_output, (soccer_matches, tennis_matches)), json_paths):
                progress.advance(task)
                path, sport, status, market = result
                json_input.at[sport, status] += 1

                if market:
                    runners_db.saveMarket(market)
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
