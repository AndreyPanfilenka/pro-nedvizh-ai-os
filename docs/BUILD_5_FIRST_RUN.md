# BUILD 5 — First Run

Exact steps to verify the Make + Google Sheets + OpenRouter pipeline from zero. **No backend, no tunnel, no local server.**

---

## Prerequisites

| Service | Requirement |
|---------|-------------|
| Google account | Access to Google Sheets |
| Make.com | Active account with scenario quota |
| OpenRouter | API key with credits at [openrouter.ai/keys](https://openrouter.ai/keys) |

---

## Step 1 — Get an OpenRouter API key

1. Sign in at [openrouter.ai](https://openrouter.ai).
2. Go to **Keys** and create a new API key.
3. Copy the key — you will paste it into Make module 4 as `OPENROUTER_API_KEY`.
4. Confirm your account has credits (gpt-4o-mini is inexpensive; a few cents per run).

**Security:** Store the key only in Make's HTTP Authorization header. Never put it in the Google Sheet or commit it to git.

---

## Step 2 — Create the Google Sheet

1. Create a spreadsheet named **PRO Nedvizh Publications**.
2. Rename the first tab to `INBOX`.
3. Import [`../google/sheets/BUILD_5_SHEET_TEMPLATE.csv`](../google/sheets/BUILD_5_SHEET_TEMPLATE.csv).
4. Confirm 11 headers in row 1 (A–K):
   ```
   ID | STATUS | SOURCE_URL | TITLE | TELEGRAM_TEXT | INSTAGRAM_TEXT | REELS_SCRIPT | HASHTAGS | ERROR | CREATED_AT | UPDATED_AT
   ```
5. Apply STATUS dropdown on column B:
   ```
   NEW | PROCESSING | READY | ERROR | APPROVED | PUBLISHED
   ```
6. Freeze row 1; freeze columns A–B; text wrap on E, F, G.
7. Save `SPREADSHEET_ID` from the URL.
8. Note tab name as `SHEET_NAME` (default: `INBOX`).

---

## Step 3 — Import and configure Make

1. Follow [`../automation/make/BUILD_5_IMPORT_GUIDE.md`](../automation/make/BUILD_5_IMPORT_GUIDE.md).
2. Import [`../automation/make/build_5_direct_openrouter_pipeline.blueprint.json`](../automation/make/build_5_direct_openrouter_pipeline.blueprint.json).
3. Connect Google Sheets on all Google modules (1, 3, 7, 8, 9, 10).
4. Set placeholders:

| Placeholder | Your value |
|-------------|------------|
| `SPREADSHEET_ID` | From Step 2 |
| `SHEET_NAME` | e.g. `INBOX` |
| `OPENROUTER_API_KEY` | From Step 1 |
| `SYSTEM_PROMPT` | From [`../prompts/build_5_openrouter_prompt.md`](../prompts/build_5_openrouter_prompt.md) |

5. Open module **4. HTTP POST OpenRouter** and confirm:
   - URL: `https://openrouter.ai/api/v1/chat/completions`
   - Method: `POST`
   - Authorization: `Bearer <your key>`
   - Model: `openai/gpt-4o-mini`
   - Temperature: `0.4`
   - `response_format.type`: `json_object`
   - User message includes `{{1.`SOURCE_URL`}}` from the row
6. Save the scenario.
7. Turn the scenario **ON**.

---

## Step 4 — Add the first test row

In the sheet, row 2:

| Column | Value |
|--------|-------|
| A — ID | `f47ac10b-58cc-4372-a567-0e02b2c3d479` |
| B — STATUS | `NEW` |
| C — SOURCE_URL | One real listing URL you can open in a browser |
| D — TITLE | *(leave empty)* |
| E — TELEGRAM_TEXT | *(leave empty)* |
| F — INSTAGRAM_TEXT | *(leave empty)* |
| G — REELS_SCRIPT | *(leave empty)* |
| H — HASHTAGS | *(leave empty)* |
| I — ERROR | *(leave empty)* |
| J — CREATED_AT | `2026-07-03 09:00:00` |
| K — UPDATED_AT | `2026-07-03 09:00:00` |

Use any listing URL. Drafts will be conservative because Make sends only the URL — the AI cannot fetch the page.

---

## Step 5 — Trigger and watch

1. In Make, click **Run once**.
2. Open **History** — wait for completion (15–45 seconds typical).
3. Watch the sheet update in two stages:
   - First: `STATUS` changes to `PROCESSING`
   - Then: `STATUS` changes to `READY` with drafts filled

---

## Step 6 — Verify success

Refresh the sheet row and confirm:

| Check | Expected |
|-------|----------|
| STATUS | `READY` |
| TITLE | Non-empty Russian headline (may be neutral if URL has little info) |
| TELEGRAM_TEXT | Telegram post draft |
| INSTAGRAM_TEXT | Instagram caption draft |
| REELS_SCRIPT | Script with timing markers |
| HASHTAGS | Space-separated tags (no `#`) |
| ERROR | Empty |
| UPDATED_AT | Newer than CREATED_AT |
| SOURCE_URL | Unchanged (same URL you entered) |
| ID | Unchanged |

Open Make **History → successful run → module 4** and confirm:
- HTTP status 200
- Response contains `choices[0].message.content` with valid JSON

Open **module 5** and confirm parsed fields: `title`, `telegram_text`, `instagram_text`, `reels_script`, `hashtags`.

---

## Step 7 — Verify error handling

1. Add a second row with:
   - `STATUS` = `NEW`
   - `SOURCE_URL` = `not-a-valid-url`
   - Fresh UUID in `ID`
   - Timestamps in `CREATED_AT` / `UPDATED_AT`
2. Run the scenario once.
3. Confirm one of:
   - `STATUS` = `READY` with conservative generic drafts (AI may still respond), **or**
   - `STATUS` = `ERROR` with message in `ERROR` column

To test HTTP errors: temporarily set a wrong API key, run once, confirm `STATUS` = `ERROR`, then restore the key.

To retry any failed row: clear `ERROR`, set `STATUS` = `NEW`, run again.

---

## Step 8 — Human review (manual)

The pipeline stops at `READY`. No automatic posting in Build 5.

1. Read `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, and `REELS_SCRIPT`.
2. **Edit drafts in the sheet** — add verified facts from the listing page manually.
3. When satisfied, change `STATUS` to `APPROVED`.
4. After manual publish to Telegram/Instagram, set `STATUS` to `PUBLISHED`.

---

## Pipeline reference

```
User adds URL (STATUS = NEW)
  ↓
Make Watch Rows
  ↓
STATUS = PROCESSING
  ↓
POST OpenRouter /chat/completions (URL only)
  ↓
Parse JSON → title, telegram_text, instagram_text, reels_script, hashtags
  ↓
STATUS = READY (drafts in sheet)
  ↓
Human review + fact-check → APPROVED → manual publish → PUBLISHED
```

---

## If something fails

| Symptom | Action |
|---------|--------|
| Make run red on module 4 | Check API key; confirm OpenRouter credits; inspect History response body |
| JSON parse error on module 5 | Open module 4 output — `message.content` must be raw JSON, not markdown |
| Row stuck on PROCESSING | Check Make History; fix issue; set STATUS back to NEW |
| Empty drafts but STATUS = READY | Should not happen — validation requires all text fields; report as misconfiguration |
| Drafts missing price/address | Expected — URL-only MVP; add facts manually after READY |

---

## Next step

Complete [`BUILD_5_CHECKLIST.md`](BUILD_5_CHECKLIST.md) before processing live listings at volume.
