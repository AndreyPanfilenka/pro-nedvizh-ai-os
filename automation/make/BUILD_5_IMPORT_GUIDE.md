# BUILD 5 — Make Import Guide

Setup guide for the PRO Nedvizh **direct OpenRouter** pipeline — no backend, no tunnel, no local server.

**What this does:** You add a real estate URL to Google Sheets. Make sends the URL directly to OpenRouter. Ready-to-publish Telegram, Instagram, and Reels drafts appear in the same row.

---

## Before you start

You need:

| Item | What it is |
|------|------------|
| Google account | For the spreadsheet |
| Make.com account | For the automation scenario |
| OpenRouter API key | From [openrouter.ai/keys](https://openrouter.ai/keys) |

Prepare these values before import:

| Placeholder | Example | Where to find it |
|-------------|---------|------------------|
| `SPREADSHEET_ID` | `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms` | Google Sheet URL between `/d/` and `/edit` |
| `SHEET_NAME` | `INBOX` | Tab name at the bottom of the spreadsheet |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | [OpenRouter Keys](https://openrouter.ai/keys) |
| `SYSTEM_PROMPT` | *(long text)* | [`../../prompts/build_5_openrouter_prompt.md`](../../prompts/build_5_openrouter_prompt.md) |

---

## Step 1 — Create the Google Sheet

1. Create a new Google Spreadsheet named **PRO Nedvizh Publications**.
2. Rename the first tab to `INBOX`.
3. Import the template:
   - **File → Import → Upload**
   - Select [`../../google/sheets/BUILD_5_SHEET_TEMPLATE.csv`](../../google/sheets/BUILD_5_SHEET_TEMPLATE.csv)
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

Sheet columns (A–K):

```
ID | STATUS | SOURCE_URL | TITLE | TELEGRAM_TEXT | INSTAGRAM_TEXT | REELS_SCRIPT | HASHTAGS | ERROR | CREATED_AT | UPDATED_AT
```

---

## Step 2 — Import the blueprint into Make

1. Open [Make.com](https://www.make.com) and sign in.
2. Go to **Scenarios → Create a new scenario**.
3. Click the **⋮** menu (top right) → **Import Blueprint**.
4. Upload:
   ```
   automation/make/build_5_direct_openrouter_pipeline.blueprint.json
   ```
5. Make creates a scenario named **PRO Nedvizh Build 5 — Direct OpenRouter Pipeline**.

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

### HTTP module (4. HTTP POST OpenRouter)

| Field | Replace with |
|-------|--------------|
| Authorization header | `Bearer YOUR_OPENROUTER_API_KEY` |
| Body → system message | Full prompt from [`../../prompts/build_5_openrouter_prompt.md`](../../prompts/build_5_openrouter_prompt.md) |

Replace the literal string `SYSTEM_PROMPT` in the JSON body with the escaped system prompt.

**Tips for the system prompt:**

- Copy the prompt block from `build_5_openrouter_prompt.md`.
- In Make's JSON body editor, paste the prompt as the `"content"` value for the system message.
- Escape double quotes as `\"` if editing raw JSON text.
- Do **not** put the API key in the sheet — only in the Authorization header.

Confirm the request matches this shape:

```json
{
  "model": "openai/gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "<your system prompt>"
    },
    {
      "role": "user",
      "content": "Create publication drafts for this real estate listing URL: {{1.`SOURCE_URL`}}"
    }
  ],
  "temperature": 0.4,
  "response_format": {
    "type": "json_object"
  }
}
```

Make maps `{{1.`SOURCE_URL`}}` from module 1 automatically — do not hardcode a URL.

---

## Step 5 — Save and turn on

1. Click **Save** (disk icon).
2. Toggle the scenario **ON** (switch in the bottom-left).
3. Make now polls the sheet every few minutes for rows with `STATUS` = `NEW`.

---

## Step 6 — Run once (manual test)

Before waiting for automatic polling, trigger one run manually:

1. Add a test row to the sheet (see [`../../docs/BUILD_5_FIRST_RUN.md`](../../docs/BUILD_5_FIRST_RUN.md)).
2. In Make, click **Run once** on the scenario.
3. Open **History** and wait for a green checkmark (typically 15–45 seconds).
4. Refresh the sheet — the row should show `STATUS` = `READY` with publication drafts filled in.

---

## Step 7 — Test with one real URL

1. Pick one live listing URL.
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

Because Make sends only the URL (no page fetch), drafts may be conservative and include notes to verify details — this is expected.

---

## Pipeline overview

```
Google Sheets Watch Rows
  ↓
Filter STATUS = NEW
  ↓
Google Sheets Update Row → STATUS = PROCESSING
  ↓
HTTP POST https://openrouter.ai/api/v1/chat/completions
  ↓
Parse JSON from choices[0].message.content
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
| HTTP 401 in `ERROR` column | Check `OPENROUTER_API_KEY` in Authorization header |
| HTTP 402 / insufficient credits | Top up OpenRouter balance |
| JSON parse error | AI returned non-JSON; check module 4 response in History |
| Row stuck on `PROCESSING` | Scenario may have failed mid-run; set `STATUS` back to `NEW` after fixing |
| Permission denied on sheet | Reconnect Google Sheets; confirm Editor access |
| Drafts too generic | Expected for URL-only MVP — edit drafts in sheet before `APPROVED` |

---

## Next steps

- Complete the production checklist: [`../../docs/BUILD_5_CHECKLIST.md`](../../docs/BUILD_5_CHECKLIST.md)
- Follow the exact first-run test: [`../../docs/BUILD_5_FIRST_RUN.md`](../../docs/BUILD_5_FIRST_RUN.md)
