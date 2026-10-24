import logging

import pandas as pd

from kofia import fetch_rows
from util import TODAY, TODAY_FILE, TRADE_COLUMNS, read_csv, setup_logging, write_csv

SORT_KEYS = ["날짜", "시간"]


def fetch_trades() -> pd.DataFrame:
    rows = fetch_rows(
        "BISCurTrdDescSrchSO", "listTime", "mbni6GooFd8", {1: TODAY}, extra_slots=(9,)
    )
    if not rows:
        return pd.DataFrame(columns=TRADE_COLUMNS)
    df = pd.DataFrame([{"날짜": TODAY, **row} for row in rows])
    df = df.iloc[:, : len(TRADE_COLUMNS)]
    df.columns = TRADE_COLUMNS
    return df


def with_occurrence(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(numbering=df.groupby(TRADE_COLUMNS).cumcount())


def merge_trades(old: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    key = [*TRADE_COLUMNS, "numbering"]
    merged = pd.concat([with_occurrence(old), with_occurrence(new)])
    return (
        merged.drop_duplicates(subset=key)
        .drop(columns="numbering")
        .sort_values(SORT_KEYS, kind="stable")
    )


def main() -> None:
    new = fetch_trades()
    if new.empty:
        logging.info("Null data")
        return
    old = read_csv(TODAY_FILE, TRADE_COLUMNS)
    result = merge_trades(old, new)
    write_csv(result, TODAY_FILE)
    logging.info(f"Updated: new {new.shape}, old {old.shape}, result {result.shape}")


if __name__ == "__main__":
    setup_logging("crawling")
    try:
        main()
    except Exception:
        logging.exception("crawling failed")
        raise SystemExit(1)
    finally:
        logging.info("-----")
