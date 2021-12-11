from csv import DictReader
from datetime import datetime
import functools
import json
from multiprocessing import cpu_count, Pool
from pathlib import Path
import time
from typing import Optional

import dateparser
from loguru import logger
import openpyxl
from pandas import DataFrame
import simplejson as json

from dataframe import create_main_dataframe, convert_to_obj
from paths import PathConfig
from object.markets import MarketInfo
from object.runners import RunnersDB
from utils import get_progress


# Remove adjacent duplicate rows in market data
def remove_market_duplicates(market: DataFrame) -> DataFrame:
    duplicate_data = market[["openDate", "status", "betDelay", "inPlay"]]
    return market.loc[(duplicate_data.shift() != duplicate_data).any(axis=1)]


def canonize_name(name: str) -> str:
    split = name.split()
    return f"{split[-1]}-{name[0]}"


def process_json(export_dir: Path, sport_info: tuple, path: Path):
    tennis_matches, soccer_matches = sport_info

    status = "BASIC" if "BASIC" in path.parts else "ADVANCED"
    sport = path.parts[path.parts.index(status) + 1]
    basic_info = (path, sport, status, None)
    market_json_path = export_dir / "markets" / Path(*path.parts[path.parts.index(status):])
    if market_json_path.exists():
        return basic_info

    frame = create_main_dataframe(path, status)
    frame["market"] = remove_market_duplicates(frame["market"])
    obj = convert_to_obj(frame, status, sport)
    info = obj.info
    if obj.status == "REMOVED":
        return basic_info
    open_date = datetime.fromtimestamp(info["openDate"] / 1000)
    in_play_length = 0
    for runner in obj.runners:
        in_play_length += runner.get("lengthOddsInPlay", 0)
    if ((sport == "TENNIS" and (
            (open_date.year > 2018 and info["delay"] > 5)
            or (open_date.year < 2018 and info["delay"] > 7))
    ) or (sport == "SOCCER" and info["delay"] > 7)
            or (sport == "TENNIS" and "/" in info["eventName"])
            or (sport in ["SOCCER", "TENNIS"] and in_play_length == 0)):
        return basic_info

    renamed_obj = {
        "marketType": obj.status,
        "marketInfo": obj.info,
        "marketRunners": obj.runners,
        "marketUpdates": obj.marketUpdates,
        "marketOdds": obj.odds,
    }

    date = open_date.strftime("%Y-%m-%d")
    if sport == "TENNIS":
        try:
            winner = canonize_name(next(r for r in obj.runners if r["status"] == "WINNER")["name"])
            loser = canonize_name(next(r for r in obj.runners if r["status"] == "LOSER")["name"])
            match = f"{date}-{winner}-{loser}"
            if match in tennis_matches:
                federation, gender = tennis_matches[match]
                renamed_obj["additionalInfo"] = {
                    "federation": federation,
                    "sex": gender,
                    "season": open_date.year,
                }
        except StopIteration:
            pass
    elif sport == "SOCCER":
        split = info["eventName"].split(" v ")
        match = f"{date}-{split[0]}-{split[1]}"
        if match in soccer_matches:
            league, code = soccer_matches[match]
            renamed_obj["additionalInfo"] = {
                "league": league,
                "countryCode": code,
                "season":
            }

    if "additionalInfo" not in renamed_obj:
        renamed_obj["additionalInfo"] = {}

    market_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(market_json_path, "w") as market_json_file:
        json.dump(renamed_obj, market_json_file, indent=4, ignore_nan=True)

    return path, sport, status, obj


def process_all_json(json_paths: list[Path]):
    logger.info(f"Files to process: {len(json_paths)}")
    process_start = time.perf_counter()

    runners_db = RunnersDB()
    now = datetime.now()
    export_output = Path(PathConfig.EXPORT_DIR) / now.strftime("%Y-%m-%d_%H-%M-%S")
    export_output.mkdir(parents=True, exist_ok=True)
    json_input = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)
    json_output = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)



    with get_progress() as progress:
        task = progress.add_task("JSON Files", total=len(json_paths))
        with Pool(processes=cpu_count()) as pool:
            for result in pool.imap(functools.partial(process_json, export_output, (tennis_matches, soccer_matches)), json_paths):
                progress.advance(task)
                path, sport, status, market = result
                json_input.at[sport, status] += 1

                if market:
                    runners_db.save_market(market)
                    json_output.at[sport, status] += 1

    runners_db.save(export_output / "runnerDB.json")

    logger.info(f"Processing completed in {time.perf_counter() - process_start:.2f}s")
    logger.info("Input:")
    logger.info(f"\n{json_input}")
    logger.info("Output:")
    logger.info(f"\n{json_output}")
