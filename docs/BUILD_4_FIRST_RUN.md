# BUILD 4 — First Run

Exact steps to verify the Make + Google Sheets + backend pipeline from zero.

---

## Prerequisites

| Service | Requirement |
|---------|-------------|
| Google account | Access to Google Sheets |
| Make.com | Active account with scenario quota |
| Backend | Build 2 API running with OpenRouter configured |

Backend must respond on `GET /health` with `{"status":"ok"}` and accept `POST /generate-publication`.

---

## Step 1 — Start the backend

```bash
cd pro-nedvizh-ai-os
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set OPENROUTER_API_KEY and OPENROUTER_MODEL
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify locally:

```bash
curl http://127.0.0.1:8000/health
```

Expected: `{"status":"ok"}`

Note your backend URL:

| Environment | BACKEND_URL |
|-------------|-------------|
| Local (Make Cloud) | Use a tunnel (ngrok, Cloudflare Tunnel) — Make cannot reach `127.0.0.1` |
| Local (Make on-prem) | `http://your-machine-ip:8000` |
| Deployed server | `https://your-domain.com` |

For this first run, if Make runs in the cloud, expose the backend with a tunnel and use the public HTTPS URL as `BACKEND_URL`.

---

## Step 2 — Create the Google Sheet

1. Follow [`../google/sheets/BUILD_4_COLUMNS.md`](../google/sheets/BUILD_4_COLUMNS.md) setup section.
2. Import [`../google/sheets/BUILD_4_SHEET_TEMPLATE.csv`](../google/sheets/BUILD_4_SHEET_TEMPLATE.csv).
3. Confirm 11 headers in row 1 (A–K):
   ```
   ID | STATUS | SOURCE_URL | TITLE | TELEGRAM_TEXT | INSTAGRAM_TEXT | REELS_SCRIPT | HASHTAGS | ERROR | CREATED_AT | UPDATED_AT
   ```
4. Apply STATUS dropdown on column B.
5. Save `SPREADSHEET_ID` from the URL.
6. Note tab name as `SHEET_NAME` (default: `INBOX`).

---

## Step 3 — Import and configure Make

1. Follow [`../automation/make/BUILD_4_IMPORT_GUIDE.md`](../automation/make/BUILD_4_IMPORT_GUIDE.md).
2. Import [`../automation/make/build_4_auto_publication_pipeline.blueprint.json`](../automation/make/build_4_auto_publication_pipeline.blueprint.json).
3. Connect Google Sheets on all Google modules.
4. Set placeholders:

| Placeholder | Your value |
|-------------|------------|
| `SPREADSHEET_ID` | From Step 2 |
| `SHEET_NAME` | e.g. `INBOX` |
| `BACKEND_URL` | From Step 1 (no trailing slash) |

5. Open module **4. HTTP POST /generate-publication** and confirm:
   - Method: `POST`
   - URL: `{BACKEND_URL}/generate-publication`
   - Body: `{"source_url": "<from row>"}`
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

Use a URL from a supported platform (Cian, Avito, Domclick, etc.).

---

## Step 5 — Trigger and watch

1. In Make, click **Run once**.
2. Open **History** — wait for completion (30–90 seconds typical).
3. Watch the sheet update in two stages:
   - First: `STATUS` changes to `PROCESSING`
   - Then: `STATUS` changes to `READY` with drafts filled

---

## Step 6 — Verify success

Refresh the sheet row and confirm:

| Check | Expected |
|-------|----------|
| STATUS | `READY` |
| TITLE | Non-empty Russian headline |
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
- Response body contains `"status": "success"` and a `publication` object

---

## Step 7 — Verify error handling

1. Add a second row with:
   - `STATUS` = `NEW`
   - `SOURCE_URL` = `https://example.com/not-a-real-listing`
   - Fresh UUID in `ID`
   - Timestamps in `CREATED_AT` / `UPDATED_AT`
2. Run the scenario once.
3. Confirm:
   - `STATUS` = `ERROR`
   - `ERROR` contains a readable message
   - Content columns remain empty

To retry any failed row: clear `ERROR`, set `STATUS` = `NEW`, run again.

---

## Step 8 — Human review (manual)

The pipeline stops at `READY`. No automatic posting in Build 4.

1. Read `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, and `REELS_SCRIPT`.
2. Edit if needed directly in the sheet.
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
POST /generate-publication { "source_url": "..." }
  ↓
Parse JSON → publication.title, telegram_text, instagram_text, reels_script, hashtags
  ↓
STATUS = READY (drafts in sheet)
  ↓
Human review → APPROVED → manual publish → PUBLISHED
```

---

## If something fails

| Symptom | Action |
|---------|--------|
| Make run red on module 4 | Test backend with `curl -X POST BACKEND_URL/generate-publication -H "Content-Type: application/json" -d '{"source_url":"YOUR_URL"}'` |
| Row stuck on PROCESSING | Check Make History for the failed module; fix issue; set STATUS back to NEW |
| Empty drafts but STATUS = READY | Should not happen — validation requires all publication fields; report as bug |
| Make cannot reach backend | Use HTTPS tunnel for local dev; confirm firewall allows inbound |

---

## Next step

Complete [`BUILD_4_CHECKLIST.md`](BUILD_4_CHECKLIST.md) before processing live listings at volume.
