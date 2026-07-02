# BUILD 4 — Make Import Guide

Simple setup guide for the PRO Nedvizh auto-publication pipeline.

**What this does:** You add a real estate URL to Google Sheets. Make calls your backend. Ready-to-publish Telegram, Instagram, and Reels drafts appear in the same row.

---

## Before you start

You need:

| Item | What it is |
|------|------------|
| Google account | For the spreadsheet |
| Make.com account | For the automation scenario |
| Running backend | Build 2 API with `POST /generate-publication` |

Prepare these values before import:

| Placeholder | Example | Where to find it |
|-------------|---------|------------------|
| `SPREADSHEET_ID` | `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms` | Google Sheet URL between `/d/` and `/edit` |
| `SHEET_NAME` | `INBOX` | Tab name at the bottom of the spreadsheet |
| `BACKEND_URL` | `https://api.example.com` | Your server base URL — **no trailing slash** |

---

## Step 1 — Create the Google Sheet

1. Create a new Google Spreadsheet named **PRO Nedvizh Publications**.
2. Rename the first tab to `INBOX`.
3. Import the template:
   - **File → Import → Upload**
   - Select [`../../google/sheets/BUILD_4_SHEET_TEMPLATE.csv`](../../google/sheets/BUILD_4_SHEET_TEMPLATE.csv)
   - Import location: **Replace current sheet**
   - Separator: **Comma**
4. Copy `SPREADSHEET_ID` from the browser URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
5. Freeze row 1. Freeze columns A–B.
6. Turn on text wrap for columns E, F, G (`TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT`).
7. Add a STATUS dropdown on column B with these values:
   ```
   NEW
   PROCESSING
   READY
   ERROR
   APPROVED
   PUBLISHED
   ```
8. Share the sheet with **Editor** access for the Google account you will connect in Make.

Column details: [`../../google/sheets/BUILD_4_COLUMNS.md`](../../google/sheets/BUILD_4_COLUMNS.md)

---

## Step 2 — Import the blueprint into Make

1. Open [Make.com](https://www.make.com) and sign in.
2. Go to **Scenarios → Create a new scenario**.
3. Click the **⋮** menu (top right) → **Import Blueprint**.
4. Upload:
   ```
   automation/make/build_4_auto_publication_pipeline.blueprint.json
   ```
5. Make creates a scenario named **PRO Nedvizh Build 4 — Auto Publication Pipeline**.

---

## Step 3 — Connect Google Sheets

Every Google Sheets module in the scenario needs your Google account:

1. Click module **1. Google Sheets Watch Rows**.
2. Click **Create a connection** (or select an existing Google connection).
3. Sign in with the Google account that has Editor access to the spreadsheet.
4. Repeat for modules **3**, **7**, **8**, **9**, and **10** (all Google Sheets Update Row modules).

After connecting, Make assigns a connection ID. If you export the scenario later, this becomes `GOOGLE_CONNECTION_ID`.

---

## Step 4 — Set placeholders

Open each module and replace the placeholder strings with your real values.

### Google Sheets modules (1, 3, 7, 8, 9, 10)

| Field | Replace with |
|-------|--------------|
| Spreadsheet ID | Your `SPREADSHEET_ID` |
| Sheet name | Your `SHEET_NAME` (e.g. `INBOX`) |
| Table contains headers | Row 1 = `A1:K1` |

In the Watch Rows module, set **Sheet name** to your tab name.

### HTTP module (4. HTTP POST /generate-publication)

| Field | Replace with |
|-------|--------------|
| URL | `BACKEND_URL/generate-publication` |

Example: if your backend runs at `https://api.pro-nedvizh.com`, set the URL to:

```
https://api.pro-nedvizh.com/generate-publication
```

Confirm the request body is:

```json
{
  "source_url": "{{SOURCE_URL from row}}"
}
```

Make maps this automatically from module 1 — do not hardcode a URL in the body.

---

## Step 5 — Save and turn on

1. Click **Save** (disk icon).
2. Toggle the scenario **ON** (switch in the bottom-left).
3. Make now polls the sheet every few minutes for rows with `STATUS` = `NEW`.

---

## Step 6 — Run once (manual test)

Before waiting for automatic polling, trigger one run manually:

1. Add a test row to the sheet (see [`../../docs/BUILD_4_FIRST_RUN.md`](../../docs/BUILD_4_FIRST_RUN.md)).
2. In Make, click **Run once** on the scenario.
3. Open **History** and wait for a green checkmark (typically 30–90 seconds).
4. Refresh the sheet — the row should show `STATUS` = `READY` with publication drafts filled in.

---

## Step 7 — Test with one real URL

1. Pick one live listing URL (Cian, Avito, or another supported site).
2. Add a row:

| Column | Value |
|--------|-------|
| ID | Any UUID |
| STATUS | `NEW` |
| SOURCE_URL | Your listing URL |
| CREATED_AT | Current UTC time, e.g. `2026-07-03 09:00:00` |
| UPDATED_AT | Same as CREATED_AT |

3. Leave all other columns empty.
4. Run the scenario (automatically or **Run once**).
5. Verify the row reaches `STATUS` = `READY` with:
   - `TITLE` filled
   - `TELEGRAM_TEXT` filled
   - `INSTAGRAM_TEXT` filled
   - `REELS_SCRIPT` filled
   - `HASHTAGS` filled (space-separated)
   - `ERROR` empty

---

## Pipeline overview

```
Google Sheets Watch Rows
  ↓
Filter STATUS = NEW
  ↓
Google Sheets Update Row → STATUS = PROCESSING
  ↓
HTTP POST BACKEND_URL/generate-publication
  ↓
Parse JSON response
  ↓
Google Sheets Update Row → STATUS = READY + publication fields
  ↓
(on failure) STATUS = ERROR + error message
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Scenario does not pick up the row | Confirm `STATUS` = `NEW` and `SOURCE_URL` is not empty |
| HTTP error in `ERROR` column | Check backend is running; verify `BACKEND_URL` has no trailing slash |
| JSON parse error | Backend returned non-JSON; check backend logs |
| Row stuck on `PROCESSING` | Scenario may have failed mid-run; set `STATUS` back to `NEW` after fixing |
| Permission denied on sheet | Reconnect Google Sheets; confirm Editor access |

---

## Next steps

- Complete the production checklist: [`../../docs/BUILD_4_CHECKLIST.md`](../../docs/BUILD_4_CHECKLIST.md)
- Follow the exact first-run test: [`../../docs/BUILD_4_FIRST_RUN.md`](../../docs/BUILD_4_FIRST_RUN.md)
