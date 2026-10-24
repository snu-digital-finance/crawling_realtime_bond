import logging

import pandas as pd

from kofia import fetch_rows
from util import DATA_DIR, TODAY, setup_logging, write_csv

ISSUE_COLUMNS = [
    "종목명", "표준코드", "발행일", "만기일", "잔존기간",
    "발행액", "이자 지급유형", "이자 주기(월)", "표면금리",
]
UNKNOWN_TYPE = "알수없음"
BOND_TYPES = {
    name: str(i)
    for i, name in enumerate(
        ["국채", "지방채", "특수채", "통안증권", "은행채", "기타금융채", "회사채", "ABS"],
        start=1,
    )
}


def fetch_issues(bond_code: str) -> pd.DataFrame:
    rows = fetch_rows(
        "BISIssInfoSntcSrchSO", "list", "MupihE7A3ey",
        {1: "EXP", 2: TODAY, 3: "99991231", 4: bond_code},
    )
    if not rows:
        return pd.DataFrame(columns=ISSUE_COLUMNS)
    df = pd.DataFrame(rows).iloc[:, : len(ISSUE_COLUMNS)]
    df.columns = ISSUE_COLUMNS
    return df


def main() -> None:
    everything = fetch_issues("")
    if everything.empty:
        logging.info("Null data")
        return
    logging.info(f"Total: {everything.shape}")

    typed = []
    for name, code in BOND_TYPES.items():
        df = fetch_issues(code).assign(채권종류=name)
        logging.info(f"{name}: {df.shape}")
        typed.append(df)

    result = pd.concat([*typed, everything.assign(채권종류=UNKNOWN_TYPE)])
    result = result.drop_duplicates(subset=ISSUE_COLUMNS, keep="first")
    result["수집일"] = TODAY
    write_csv(result, DATA_DIR / f"kofia_bis_bond_issue_{TODAY}.csv")
    logging.info(f"Result: {result.shape}")


if __name__ == "__main__":
    setup_logging("crawling_issue")
    try:
        main()
    except Exception:
        logging.exception("crawling_issue failed")
        raise SystemExit(1)
    finally:
        logging.info("-----")
