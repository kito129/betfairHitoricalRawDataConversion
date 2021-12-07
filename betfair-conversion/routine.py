import os
from pathlib import Path
import shutil

from extract import extract_all_json
from paths import PathConfig
from process import process_all_json


def main():
    folder = Path(__file__).parent
    os.chdir(folder)

    raw_data = Path(PathConfig.INPUT_DIR)
    raw_input = Path(PathConfig.WORK_DIR)
    json_paths = extract_all_json(raw_data, raw_input)
    process_all_json(json_paths)
    shutil.rmtree(raw_input)


if __name__ == "__main__":
    main()
