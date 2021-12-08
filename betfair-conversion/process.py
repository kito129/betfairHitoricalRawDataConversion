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


def process_json(export_dir: Path, sport_info: tuple, path: Path) -> Optional[MarketInfo]:
    soccer_matches, soccer_leagues = sport_info

    status = "BASIC" if "BASIC" in path.parts else "ADVANCED"
    sport = path.parts[path.parts.index(status) + 1]
    market_json_path = export_dir / "markets" / Path(*path.parts[path.parts.index(status):])
    if market_json_path.exists():
        return None

    frame = create_main_dataframe(path, status)
    frame["market"] = remove_market_duplicates(frame["market"])
    obj = convert_to_obj(frame, status, sport)
    info = obj.info
    if obj.status == "REMOVED":
        return None
    open_date = datetime.fromtimestamp(info["openDate"] / 1000)
    # TODO: WE HAVE TO REMOVE ALL THE MARKET NEVER TURNED IN PLAY (FOR FOOTBALL AND TENNIS)
    if ((info["sport"] == "TENNIS" and (
            (open_date.year > 2018 and info["delay"] > 5)
            or (open_date.year < 2018 and info["delay"] > 7))
    ) or (info["sport"] == "SOCCER" and info["delay"] > 7)
            or (info["sport"] == "TENNIS" and "/" in info["eventName"])):
        return None

    renamed_obj = {
        "marketType": obj.status,
        "marketInfo": obj.info,
        "marketRunners": obj.runners,
        "marketUpdates": obj.marketUpdates,
        "marketOdds": obj.odds,
    }

    if sport == "SOCCER":
        split = info["eventName"].split(" v ")
        match = f"{open_date.strftime('%Y-%m-%d')}-{split[0]}-{split[1]}"
        if match in soccer_matches:
            league, code = soccer_leagues[soccer_matches[match]]
            renamed_obj["additionalInfo"] = {
                "league": league,
                "countryCode": code,
                "season": f"{open_date.year}/{open_date.year + 1}" if open_date.month > 5 else f"{open_date.year - 1}/{open_date.year}",
            }
    elif sport == "TENNIS":
        pass

    if "additionalInfo" not in renamed_obj:
        renamed_obj["additionalInfo"] = {}

    market_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(market_json_path, "w") as market_json_file:
        json.dump(renamed_obj, market_json_file, indent=4, ignore_nan=True)

    return obj


def process_all_json(json_paths: list[Path]):
    logger.info(f"Files to process: {len(json_paths)}")
    process_start = time.perf_counter()

    runners_db = RunnersDB()
    now = datetime.now()
    export_output = Path(PathConfig.EXPORT_DIR) / now.strftime("%Y-%m-%d_%H-%M-%S")
    export_output.mkdir(parents=True, exist_ok=True)
    summary = DataFrame(index=["HORSE", "SOCCER", "TENNIS", "OTHER"], columns=["BASIC", "ADVANCED"], dtype="Int64").fillna(0)

    soccer_matches = {}
    excel = Path("excel")
    for soccer_path in excel.glob("SOCCER/*.csv"):
        with open(soccer_path) as soccer_file:
            soccer_csv = DictReader(soccer_file)
            for row in soccer_csv:
                date = dateparser.parse(row["Date"], date_formats=["%d/%m/%y", "%d/%m/%Y"]).strftime("%Y-%m-%d")
                soccer_matches[f"{date}-{row['HomeTeam']}-{row['AwayTeam']}"] = row["Div"]
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

    with get_progress() as progress:
        task = progress.add_task("JSON Files", total=len(json_paths))
        with Pool(processes=cpu_count()) as pool:
            for market in pool.imap(functools.partial(process_json, export_output, (soccer_matches, soccer_leagues)), json_paths):
                progress.advance(task)

                if market:
                    runners_db.save_market(market)
                    summary.at[market.info["sport"], market.status] += 1

    runners_db.save(export_output / "runnerDB.json")

    logger.info(f"Processing completed in {time.perf_counter() - process_start:.2f}s")
    logger.info("Summary:")
    logger.info(f"\n{summary}")
