import csv
from io import BytesIO
from pathlib import Path
from typing import Callable, TypeVar

import dateparser
import openpyxl_dictreader


T = TypeVar("T")


def get_val(row: dict, key: str, func: Callable[[str], T]) -> T:
    try:
        return func(row[key])
    except (KeyError, TypeError, ValueError):
        return None


def get_int(row: dict, key: str) -> int:
    return get_val(row, key, func=int)


def get_float(row: dict, key: str) -> float:
    return get_val(row, key, func=float)


EXCEL = Path("excel")

SOCCER_LEAGUES = {
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


def get_soccer_matches() -> dict:
    soccer_matches = {}

    for soccer_path in EXCEL.glob("SOCCER/*.csv"):
        with open(soccer_path) as soccer_file:
            soccer_csv = csv.DictReader(soccer_file)
            for row in soccer_csv:
                date = dateparser.parse(row["Date"], date_formats=["%d/%m/%y", "%d/%m/%Y"])
                match = f"{date.strftime('%Y-%m-%d')}-{row['HomeTeam']}-{row['AwayTeam']}"
                league, country_code = SOCCER_LEAGUES[row["Div"]]
                soccer_matches[match] = {
                    "league": league,
                    "countryCode": country_code,
                    "season": f"{date.year}/{date.year + 1}" if date.month > 5 else f"{date.year - 1}/{date.year}",
                    "finalResult": {
                        "home": {
                            "fthg": get_int(row, "FTHG"),
                            "hthg": get_int(row, "HTHG"),
                        },
                        "away": {
                            "ftag": get_int(row, "FTAG"),
                            "htag": get_int(row, "HTAG"),
                        },
                        "FTR": row.get("FTR"),
                        "HTR": row.get("HTR"),
                    },
                    "matchStats": {
                        "hs": get_int(row, "HS"),
                        "as": get_int(row, "AS"),
                        "hst": get_int(row, "HST"),
                        "ast": get_int(row, "AST"),
                        "hc": get_int(row, "HC"),
                        "ac": get_int(row, "AC"),
                        "hf": get_int(row, "HF"),
                        "af": get_int(row, "AF"),
                        "hy": get_int(row, "HY"),
                        "ay": get_int(row, "AY"),
                        "hr": get_int(row, "HR"),
                        "ar": get_int(row, "AR"),
                    },
                    "bookOdds": {
                        "bet365": {
                            "matchOdds": {
                                "home": get_float(row, "B365H"),
                                "draw": get_float(row, "B365D"),
                                "away": get_float(row, "B365A"),
                            },
                            "uo25": {
                                "under25": get_float(row, "B365<2.5"),
                                "over25": get_float(row, "B365>2.5"),
                            },
                        },
                        "pinnacle": {
                            "matchOdds": {
                                "home": get_float(row, "PSH"),
                                "draw": get_float(row, "PSD"),
                                "away": get_float(row, "PSA"),
                            },
                            "uo25": {
                                "under25": get_float(row, "P<2.5"),
                                "over25": get_float(row, "P>2.5"),
                            },
                        },
                    },
                }

    return soccer_matches


TENNIS_FEDERATIONS = {
    "ATP": "MALE",
    "WTA": "FEMALE",
}


def strip_name(name: str) -> str:
    # Get name before first first name shortening
    name = name.partition(".")[0]
    # Split words
    split = name.split()
    # Return "last word of last name-first letter of first name", e.g. Thompson-J
    return "-".join(split[-2:])


def get_tennis_matches() -> dict:
    tennis_matches = {}

    for tennis_path in EXCEL.glob("TENNIS/*/*.xlsx"):
        # Thanks to bmiller on StackOverflow: https://stackoverflow.com/a/43789779
        try:
            with open(tennis_path, "rb") as tennis_file:
                in_mem_file = BytesIO(tennis_file.read())
        except IOError:
            continue

        for row in openpyxl_dictreader.DictReader(in_mem_file, read_only=True)
            date = row["Date"]
            winner = strip_name(row["Winner"])
            loser = strip_name(row["Loser"])
            match = f"{date.strftime('%Y-%m-%d')}-{winner}-{loser}"
            federation = tennis_path.parts[-2]
            gender = TENNIS_FEDERATIONS[federation]
            tennis_matches[match] = {
                "federation": federation,
                "sex": gender,
                "season": date.year,
                "tennisTournament": {
                    "location": row.get("Location"),
                    "tournament": row.get("Tournament"),
                    "series": row.get("Series", row.get("Tier")),
                    "court": row.get("Court"),
                    "surface": row.get("Surface"),
                    "round": row.get("Round"),
                    "bestOf": row.get("Best of"),
                },
                "tennisRank": {
                    "winnerRank": get_int(row, "WRank"),
                    "winnerPoint": get_int(row, "WPts"),
                    "loserRank": get_int(row, "LRank"),
                    "loserPoint": get_int(row, "LPts"),
                },
                "finalResult": {
                    "winner": {
                        "s1": get_int(row, "W1"),
                        "s2": get_int(row, "W2"),
                        "s3": get_int(row, "W3"),
                        "s4": get_int(row, "W4"),
                        "s5": get_int(row, "W5"),
                        "totalSet": get_int(row, "Wsets"),
                    },
                    "loser": {
                        "s1": get_int(row, "L1"),
                        "s2": get_int(row, "L2"),
                        "s3": get_int(row, "L3"),
                        "s4": get_int(row, "L4"),
                        "s5": get_int(row, "L5"),
                        "totalSet": get_int(row, "Lsets"),
                    },
                },
                "bookOdds": {
                    "bet365": {
                        "winner": get_float(row, "B365W"),
                        "loser": get_float(row, "B365L"),
                    },
                    "pinnacle": {
                        "winner": get_float(row, "PSW"),
                        "loser": get_float(row, "PSL"),
                    },
                    "maxOddsPortal": {
                        "winner": get_float(row, "MaxW"),
                        "loser": get_float(row, "MaxL"),
                    },
                    "avgOddsPortal": {
                        "winner": get_float(row, "AvgW"),
                        "loser": get_float(row, "AvgL"),
                    },
                },
            }

    return tennis_matches
