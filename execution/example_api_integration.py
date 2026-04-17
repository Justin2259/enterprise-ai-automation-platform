"""
Fetch records from a REST API and write them to a Google Sheet.

Usage:
    python execution/example_api_integration.py --days 7
"""

import argparse
import json
import os
import time
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
SHEET_ID = os.environ["SHEET_ID"]


def fetch_records(since: datetime) -> list[dict]:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"created_after": since.isoformat(), "limit": 100}
    records = []
    page = 1

    while True:
        params["page"] = page
        for attempt in range(3):
            resp = requests.get(f"{API_BASE_URL}/records", headers=headers, params=params, timeout=30)
            if resp.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            break

        data = resp.json()
        batch = data.get("results", [])
        records.extend(batch)

        if not data.get("has_more"):
            break
        page += 1

    return records


def transform(records: list[dict]) -> list[dict]:
    seen = set()
    rows = []
    for r in records:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        rows.append({
            "id": r["id"],
            "created_at": r["created_at"],
            "status": r.get("status", ""),
            "summary": r.get("summary", ""),
        })
    return rows


def write_to_sheet(rows: list[dict]) -> None:
    # Placeholder: swap in your Google Sheets client of choice
    # e.g. gspread, google-api-python-client, etc.
    print(f"Writing {len(rows)} rows to sheet {SHEET_ID}")
    # ... sheet write logic here ...


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    print(f"Fetching records since {since.date()}")

    records = fetch_records(since)
    if not records:
        print("Warning: 0 records returned. Exiting without writing.")
        return

    rows = transform(records)
    write_to_sheet(rows)
    print(f"Done. {len(rows)} rows written.")


if __name__ == "__main__":
    main()
