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
