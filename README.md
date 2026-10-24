# crawling_realtime_bond

KOFIA BIS bond trades and issues, stored as CSV under `data/`.

| Script | Output | Schedule (see `crontab_cmd`) |
|---|---|---|
| `crawling.py` | `data/result_today.csv`, merged with each fetch | every 15 min in the session |
| `archive_today.py` | renames it to `data/result_today_YYYYMMDD.csv` | 12:00 |
| `crawling_issue.py` | `data/kofia_bis_bond_issue_YYYYMMDD.csv` | 12:10 |

`kofia.py` holds the shared request code, `util.py` the paths, dates and CSV helpers.
`app_flask.py` serves `data/` for download on port 8000.
