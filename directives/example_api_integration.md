# Directive: Example API Integration

## Purpose

Pull records from an external REST API, transform them, and write results to a Google Sheet.

Use this directive as a template when building new API integrations. The pattern is always: fetch, transform, write.

## Inputs

| Input | Source | Notes |
|-------|--------|-------|
| `API_BASE_URL` | `.env` | Base URL for the target API |
| `API_KEY` | `.env` | Auth token or API key |
| `SHEET_ID` | `.env` | Google Sheet ID for output |
| `--days` | CLI arg | How many days of records to pull (default: 7) |

## Script

```bash
python execution/example_api_integration.py --days 7
```

Output: writes results to the configured Google Sheet. Prints row count on completion.

## Output Format

Each row in the sheet contains:
- `id` - Record ID from the API
- `created_at` - ISO 8601 timestamp
- `status` - Record status string
- `summary` - Short description field

## Error Handling

**Rate limit (429):** The script retries with exponential backoff up to 3 times. If still failing, reduce `--days` and run again.

**Auth failure (401):** API key is invalid or expired. Rotate in `.env` and re-run.

**Sheet write failure:** Check that `SHEET_ID` is correct and the service account has edit access to the sheet.

## Edge Cases

- If the API returns 0 records, the script exits cleanly with a warning. No sheet write occurs.
- Records older than 90 days may not be available depending on the API's retention policy.
- The script deduplicates by `id` before writing. Safe to re-run.

## Learnings

- This API paginates at 100 records per page. The script handles pagination automatically.
- The `created_at` field is UTC. Convert to local timezone before displaying to users.
