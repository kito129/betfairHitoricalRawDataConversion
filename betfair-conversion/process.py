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
                "season": f"{open_date.year}/{open_date.year + 1}" if open_date.month > 5 else f"{open_date.year - 1}/{open_date.year}",
            }

    if "additionalInfo" not in renamed_obj:
        renamed_obj["additionalInfo"] = {}

    market_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(market_json_path, "w") as market_json_file:
        json.dump(renamed_obj, market_json_file, indent=4, ignore_nan=True)

    return path, sport, status, obj


def strip_name(name: str) -> str:
    # Get name before first first name shortening
    name = name.partition(".")[0]
    # Split words
    split = name.split()
    # Return "last word of last name-first letter of first name", e.g. Thompson-J
    return "-".join(split[-2:])


def process_all_json(json_paths: list[Path]):
    logger.info(f"Files to process: {len(json_paths)}")
    process_start = time.perf_counter()

    runners_db = RunnersDB()
    now = datetime.now()
    export_output = Path(PathConfig.EXPORT_DIR) / now.strftime("%Y-%m-%d_%H-%M-%S")
    export_output.mkdir(parents=True, exist_ok=True)
    json_input = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)
    json_output = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)

    soccer_leagues = {
        "E0": ("Premier League", "GBR"),
        "E1": ("Championship", "GBR"),
        "SC0": ("Premier League", "SCOT"),
        "SC1": ("Division 1", "SCOT"),
        "D1": ("Budesliga 1", "GER"),
        "D2": ("Budesliga 2", "GER"),
        "I1": ("Serie A", "ITA"),
        "I2": ("Serie B", "ITA"),
        "SP1": ("La Liga Primera Division", "ESP"),
        "SP2": ("La Liga Segunda Division", "ESP"),
        "F1": ("Ligue 1", "FRA"),
        "F2": ("Ligue 2", "FRA"),
        "N1": ("Eredivise", "NLD"),
        "B1": ("Jupiler League", "BEL"),
        "P1": ("Liga I", "PRT"),
        "T1": ("Futbol Ligi 1", "TUR"),
        "G1": ("Ethniki Katigoria", "GRE"),
    }
    soccer_matches = {}
    excel = Path("excel")
    for soccer_path in excel.glob("SOCCER/*.csv"):
        with open(soccer_path) as soccer_file:
            soccer_csv = DictReader(soccer_file)
            for row in soccer_csv:
                date = dateparser.parse(row["Date"], date_formats=["%d/%m/%y", "%d/%m/%Y"]).strftime("%Y-%m-%d")
                match = f"{date}-{row['HomeTeam']}-{row['AwayTeam']}"
                soccer_matches[match] = soccer_leagues[row["Div"]]

    tennis_federations = {
        "ATP": "MALE",
        "WTA": "FEMALE",
    }
    tennis_matches = {}
    for tennis_path in excel.glob("TENNIS/*/*.xlsx"):
        try:
            ws = openpyxl.open(tennis_path, read_only=True).active
        except IOError:
            continue
        for row in ws.iter_rows(min_row=2, min_col=4, max_col=11, values_only=True):
            match = f"{row[0].strftime('%Y-%m-%d')}-{strip_name(row[-2])}-{strip_name(row[-1])}"
            federation = tennis_path.parts[-2]
            tennis_matches[match] = (federation, tennis_federations[federation])

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
