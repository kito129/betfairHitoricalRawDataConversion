import os
from pathlib import Path

from extract import extract_all_json
from process import process_all_json


def main():
    folder = Path(__file__).parent
    os.chdir(folder)

    raw_data = folder / "rawData"
    raw_input = folder / "rawInput"
    json_paths = extract_all_json(raw_data, raw_input)
    process_all_json(json_paths)


if __name__ == "__main__":
    main()

# TODO please place a varible where i can change all times the path to my folder in other HD where i have all raw file (as a string), cause itsn't always the same
# TODO the same with output folder, please use a variable where i can past everitime the correct output folder (as a string)
# TODO uniform soccer and football name, use always SOCCER terms
# TODO uniform time, when you have to do with data or time please convert always in UTC millisecond timestamp
# TODO as i said yesterday please fix venue and county code where is present ( venue only for HORSE)
# TODO log info about how much market are generate, divided by sport an type (BASIC / ADVANCED)
# TODO in runner DB when add runner please set the sport to, (ex. {"id": 28602170, "name": "Hyde Park Barracks", "sport":"HORSE"}, {"id": 39258079, "name": "Inter Milan", "sport":"SOCCER"}, {"id": 56598184, "name": "Novak Djokovic", "sport":"TENNIS"}


