from datetime import datetime
import json
from multiprocessing import cpu_count, Pool
from pathlib import Path
from typing import Optional

from loguru import logger
import pandas as pd
import simplejson as json

from dataframe import create_main_dataframe, convert_to_obj
from object.markets import MarketInfo
from object.runners import RunnersDB
from utils import get_progress


# Remove adjacent duplicate rows in market data
def remove_market_duplicates(market: pd.DataFrame) -> pd.DataFrame:
    duplicate_data = market[["openDate", "status", "betDelay", "inPlay"]]
    return market.loc[(duplicate_data.shift() != duplicate_data).any(axis=1)]


def process_json(path: Path) -> Optional[MarketInfo]:
    status = "BASIC" if "BASIC" in path.parts else "ADVANCED"
    market_json_path = "exportOutput/markets" / Path(*path.parts[path.parts.index(status):])
    if market_json_path.exists():
        return None

    frame = create_main_dataframe(path, status)
    frame["market"] = remove_market_duplicates(frame["market"])
    obj = convert_to_obj(frame, status)
    info = obj.info
    if obj.status == "REMOVED":
        return None
    open_date = datetime.fromtimestamp(info["openDate"] / 1000)
    # TODO: WE HAVE TO REMOVE ALL THE MARKET NEVER TURNED IN PLAY OR THAT STAY INPLAY LESS THAN 1 MINUTE
    #  (FOR FOOTBALL AND TENNIS)
    if ((info["sport"] == "TENNIS" and (
            (open_date.year > 2019 and info["delay"] > 3)
            or (open_date.year < 2019 and info["delay"] > 5))
    ) or (info["sport"] == "FOOTBALL" and info["delay"] > 7)
            or (info["sport"] == "TENNIS" and "/" in info["eventName"])):
        return None
    market_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(market_json_path, "w") as market_json_file:
        json.dump(vars(obj), market_json_file, indent=4, ignore_nan=True)

    return obj


def process_all_json(json_paths: list[Path]):
    logger.info(f"Files to process: {len(json_paths)}")

    runners_db = RunnersDB()

    with get_progress() as progress:
        task = progress.add_task("JSON Files", total=len(json_paths))
        with Pool(processes=cpu_count()) as pool:
            for market in pool.imap(process_json, json_paths):
                progress.advance(task)

                if market:
                    runners_db.save_market(market)

    now = datetime.now()
    runners_path = Path(f"exportOutput/runner/runnerDB_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json")
    runners_path.parent.mkdir(parents=True, exist_ok=True)
    runners_db.save(runners_path)
