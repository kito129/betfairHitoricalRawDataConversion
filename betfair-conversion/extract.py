from bz2 import BZ2File
from multiprocessing import cpu_count, Pool
import os
from pathlib import Path
import time

from loguru import logger

from utils import getProgress


# Credit for multiprocessing/progress bar code goes to willmcgugan, maintainer of rich:
# https://github.com/willmcgugan/rich/discussions/884#discussioncomment-269200
def extractJson(archive_path: Path, json_path: Path) -> list[Path]:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with BZ2File(archive_path, "rb") as archive_file, open(json_path, "wb") as json_file:
        data = archive_file.read()
        json_file.write(data)
    return json_path


def doExtractJson(params: tuple) -> list[Path]:
    return extractJson(*params)


def extractAllJson(data_path: Path, extract_path: Path) -> list[Path]:
    logger.info("Extracting files...")
    extract_start = time.perf_counter()

    data_path.mkdir(parents=True, exist_ok=True)

    bz2_files = [
        (
            Path(path, file),
            (extract_path / Path(path, file).relative_to(data_path)).with_suffix(".json"),
        )
        for (path, _, files) in os.walk(data_path)
        for file in files
        if not file.endswith(".json")
    ]
    json_paths = []
    to_extract = []
    for archive_path, json_path in bz2_files:
        if json_path.exists():
            json_paths.append(json_path)
        else:
            to_extract.append((archive_path, json_path))

    if to_extract:
        with getProgress() as progress:
            task = progress.add_task("BZ2 Files", total=len(to_extract))
            with Pool(processes=cpu_count()) as pool:
                for json_path in pool.imap(doExtractJson, to_extract):
                    json_paths.append(json_path)
                    progress.advance(task)

    logger.info(f"Extraction completed in {time.perf_counter() - extract_start:.2f}s!")
    logger.info(f"Files extracted: {len(to_extract)}")

    return json_paths
