import logging

from util import DATA_DIR, TODAY, TODAY_FILE, TRADE_COLUMNS, read_csv, setup_logging

if __name__ == "__main__":
    setup_logging("archive_today")
    if read_csv(TODAY_FILE, TRADE_COLUMNS).empty:
        logging.info(f"Empty data (today:{TODAY})")
    else:
        TODAY_FILE.rename(DATA_DIR / f"result_today_{TODAY}.csv")
        logging.info(f"Archived today data (today:{TODAY})")
    logging.info("-----")
