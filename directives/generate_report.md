# Directive: Generate Weekly Report

## Purpose

Aggregate data from one or more sources, generate a structured summary, and deliver it via email and/or Google Sheet.

## Inputs

| Input | Source | Notes |
|-------|--------|-------|
| `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` | `.env` | Email delivery credentials |
| `SHEET_ID` | `.env` | Google Sheet for raw data output |
| `RECIPIENT_EMAIL` | `.env` | Where to send the finished report |
| `--period` | CLI arg | `week`, `month`, or `custom:YYYY-MM-DD:YYYY-MM-DD` |

## Steps

1. Run `python execution/fetch_data.py --period <period>` to pull raw records into `.tmp/report_data.json`
2. Review the output for obvious anomalies before proceeding (e.g., 0 records means the data source may be down)
3. Run `python execution/generate_report.py --input .tmp/report_data.json --output .tmp/report.html`
4. Run `python execution/send_email.py --to $RECIPIENT_EMAIL --subject "Weekly Report" --body .tmp/report.html`
5. Optionally: run `python execution/write_sheet.py --input .tmp/report_data.json --sheet $SHEET_ID` for archival

## Output

- HTML email delivered to `RECIPIENT_EMAIL`
- Raw data appended to Google Sheet (one row per record)

## Error Handling

**Step 1 fails (no data):** Check if the upstream API is reachable. Check `.env` credentials. Do not proceed to step 3 with empty data.

**Step 4 fails (email bounce):** Verify SMTP credentials. Check that `RECIPIENT_EMAIL` is correct. The report HTML is saved in `.tmp/` so you can resend manually.

## Scheduling

This directive is designed to run weekly. Add a cron job or n8n scheduled trigger pointing at step 1.

To run on-demand:
```bash
python execution/fetch_data.py --period week
python execution/generate_report.py --input .tmp/report_data.json --output .tmp/report.html
python execution/send_email.py --to recipient@example.com --subject "Report" --body .tmp/report.html
```

## Learnings

- The data source API has a hard cap of 10,000 records per request. For monthly reports, batch by week and merge.
- HTML email renders correctly in Gmail and Outlook. Avoid inline CSS on `<table>` elements in Outlook.
