import logging
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "log"

TODAY = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y%m%d")
TODAY_FILE = DATA_DIR / "result_today.csv"

TRADE_COLUMNS = [
    "날짜", "시간", "종목명", "잔존기간", "신용등급",
    "수익률", "단가(원)", "거래량", "거래대금",
    "시장구분", "매매구분", "매매유형",
]


def setup_logging(name: str) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=LOG_DIR / f"{name}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def read_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    df.to_csv(tmp, index=False)
    os.replace(tmp, path)
