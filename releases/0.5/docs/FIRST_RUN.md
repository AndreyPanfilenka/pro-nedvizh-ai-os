# First Run — Release 0.5

Launch the PRO Nedvizh full pipeline from zero.

## Prerequisites

| Service | Requirement |
|---------|-------------|
| Google account | Access to Google Sheets |
| Make.com | Active account with scenario quota |
| OpenRouter | Account with API key and credits |

## Step 1 — Google Sheet

1. Follow [`../google/IMPORT_GUIDE.md`](../google/IMPORT_GUIDE.md).
2. Confirm 24 headers in row 1 (A–X).
3. Confirm STATUS dropdown on column B.
4. Save `SPREADSHEET_ID` from the spreadsheet URL.
5. Note your tab name (default: `INBOX`) as `SHEET_NAME`.

## Step 2 — OpenRouter

1. Sign up at [https://openrouter.ai](https://openrouter.ai).
2. Create an API key at [https://openrouter.ai/keys](https://openrouter.ai/keys).
3. Set a spending limit under Settings → Limits.
4. Store the key securely — use only in Make, never in the sheet or git.
5. Default model: `openai/gpt-4o-mini`.

## Step 3 — Make.com scenario

1. Open Make.com → **Scenarios → Create a new scenario**.
2. **⋮ menu → Import Blueprint**.
3. Upload [`../make/full_pipeline.blueprint.json`](../make/full_pipeline.blueprint.json).
4. Connect **Google Sheets** on every Google module (Watch Row, Update Row modules).
5. Replace placeholders:

| Placeholder | Value |
|-------------|-------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `SPREADSHEET_ID` | Spreadsheet ID from Step 1 |
| `SHEET_NAME` | Tab name (e.g. `INBOX`) |
| `MODEL` | `openai/gpt-4o-mini` |

6. Open the **OpenRouter HTTP Request** module and confirm:
   - URL: `https://openrouter.ai/api/v1/chat/completions`
   - Authorization: `Bearer <your key>`
   - Body includes `"response_format": { "type": "json_object" }`
7. Save the scenario.
8. Turn the scenario **ON**.

## Step 4 — First test row

1. In the sheet, add one row:

| Column | Value |
|--------|-------|
| ID | New UUID |
| STATUS | `NEW` |
| SOURCE_URL | `https://www.cian.ru/sale/flat/123456789/` |
| CREATED_AT | Current UTC timestamp |
| UPDATED_AT | Same as CREATED_AT |

2. Leave all other columns empty.

## Step 5 — Verify execution

1. Open Make → scenario **History**.
2. Wait for a successful run (typically 30–90 seconds).
3. Refresh the sheet row and confirm:

| Check | Expected |
|-------|----------|
| STATUS | `AI_DONE` |
| SOURCE | `cian` (or detected platform) |
| TITLE | Populated |
| PROPERTY_TYPE, DEAL_TYPE | Populated |
| CITY, PRICE, CURRENCY | Populated or null |
| AREA_TOTAL, ROOMS, FLOOR | Populated or null |
| PHOTOS | Comma-separated URLs or empty |
| DESCRIPTION_AI | Russian description text |
| TELEGRAM_TEXT | Telegram draft |
| INSTAGRAM_TEXT | Instagram caption |
| REELS_SCRIPT | Reels script with timing |
| QUALITY_SCORE | Integer 0–100 |
| ERROR | Empty |
| UPDATED_AT | Refreshed timestamp |

4. Row is now ready for the Telegram/Instagram publishing stage.

## Step 6 — Failure test

1. Add a row with `SOURCE_URL` = `https://example.com/listing/not-found` and `STATUS` = `NEW`.
2. Confirm the run completes with `STATUS` = `ERROR` and a message in `ERROR`.
3. Clear `ERROR`, set `STATUS` back to `NEW` to retry any row.

## Pipeline reference

```
Google Sheets Watch Row
  ↓
Read URL (SOURCE_URL)
  ↓
HTTP request to OpenRouter
  ↓
Validate JSON
  ↓
Update Google Sheet
  ↓
STATUS = AI_DONE
  ↓
Store quality score
  ↓
Save generated texts
  ↓
Ready for Telegram/Instagram stage
```

## Next steps

- Run through [`CHECKLIST.md`](CHECKLIST.md) before production traffic.
- Consult [`ERRORS.md`](ERRORS.md) when rows fail or stall.
