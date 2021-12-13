import os
from pathlib import Path
import shutil

from extract import extractAllJson
from paths import PathConfig
from process import processAllJson


def main():
    folder = Path(__file__).parent
    os.chdir(folder)

    raw_data = Path(PathConfig.INPUT_DIR)
    raw_input = Path(PathConfig.WORK_DIR)
    json_paths = extractAllJson(raw_data, raw_input)
    processAllJson(json_paths)
    shutil.rmtree(raw_input)


if __name__ == "__main__":
    main()
