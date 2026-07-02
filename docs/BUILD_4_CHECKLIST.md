# BUILD 4 — Production Checklist

Complete every item before accepting live listing traffic.

---

## Google Sheets

- [ ] Spreadsheet created and named **PRO Nedvizh Publications**
- [ ] Tab name matches `SHEET_NAME` placeholder in Make
- [ ] [`BUILD_4_SHEET_TEMPLATE.csv`](../google/sheets/BUILD_4_SHEET_TEMPLATE.csv) imported — 11 columns A–K
- [ ] Header row frozen
- [ ] Columns A–B frozen (`ID`, `STATUS`)
- [ ] Text wrap enabled on `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT`
- [ ] STATUS dropdown applied on column B with all six allowed values
- [ ] No extra or missing columns vs template
- [ ] `SPREADSHEET_ID` copied and verified in browser URL
- [ ] Make automation account has Editor access
- [ ] Sheet not publicly shared

---

## Backend

- [ ] Build 2 API deployed and reachable from Make (HTTPS for cloud Make)
- [ ] `GET /health` returns `{"status":"ok"}`
- [ ] `OPENROUTER_API_KEY` set in backend environment (not in sheet or Make)
- [ ] `POST /generate-publication` tested manually with curl or `/docs`
- [ ] Response includes `publication.title`, `telegram_text`, `instagram_text`, `reels_script`, `hashtags`
- [ ] Error responses return HTTP 502 with JSON `detail` message

---

## Make.com scenario

- [ ] [`build_4_auto_publication_pipeline.blueprint.json`](../automation/make/build_4_auto_publication_pipeline.blueprint.json) imported successfully
- [ ] Google Sheets connected on all Google modules (1, 3, 7, 8, 9, 10)
- [ ] `SPREADSHEET_ID` replaced in every Google module
- [ ] `SHEET_NAME` replaced in Watch Rows and all Update Row modules
- [ ] `BACKEND_URL` replaced in HTTP module (no trailing slash)
- [ ] HTTP URL ends with `/generate-publication`
- [ ] HTTP method is `POST`
- [ ] Request body sends `source_url` from row `SOURCE_URL`
- [ ] `tableFirstRow` = `A1:K1` on all Google modules
- [ ] Scenario saved
- [ ] Scenario turned ON

---

## Pipeline modules

- [ ] Module 1: Google Sheets Watch Rows — polls correct sheet and tab
- [ ] Module 3: Sets `STATUS` = `PROCESSING` only when `STATUS` = `NEW` and `SOURCE_URL` present
- [ ] Module 4: HTTP POST to `{BACKEND_URL}/generate-publication`
- [ ] Module 5: Parse JSON — reads HTTP response body
- [ ] Module 6: Validates `status` = `success` and publication fields present
- [ ] Module 7: Updates sheet with `STATUS` = `READY` and all publication fields
- [ ] Module 8: HTTP error handler sets `STATUS` = `ERROR`
- [ ] Module 9: JSON parse error handler sets `STATUS` = `ERROR`
- [ ] Module 10: Validation error handler sets `STATUS` = `ERROR`

---

## Smoke tests

- [ ] Valid listing URL: row reaches `READY` with all drafts populated
- [ ] `HASHTAGS` is space-separated text
- [ ] `UPDATED_AT` refreshed on success
- [ ] `ERROR` column empty on success
- [ ] Invalid URL: row reaches `ERROR` with message in `ERROR` column
- [ ] Re-run: clear `ERROR`, set `NEW` — row processes again
- [ ] Row with empty `SOURCE_URL` is not picked up
- [ ] Row with `STATUS` other than `NEW` is not picked up
- [ ] Row with `STATUS` = `PROCESSING` is not re-processed until reset to `NEW`

---

## Data quality

- [ ] `TITLE` is non-empty Russian headline after `READY`
- [ ] `TELEGRAM_TEXT` is ready-to-post prose
- [ ] `INSTAGRAM_TEXT` includes caption-style content
- [ ] `REELS_SCRIPT` includes timing markers (e.g. `[0:00]`)
- [ ] `HASHTAGS` contains 8–15 tags without `#` prefix
- [ ] Content matches Belarus / PRO Nedvizh brand tone

---

## Security

- [ ] No API keys in spreadsheet cells
- [ ] OpenRouter key stored only on backend server
- [ ] No secrets committed to git
- [ ] Make scenario access restricted to operators
- [ ] Backend URL uses HTTPS in production

---

## Operations

- [ ] [`BUILD_4_FIRST_RUN.md`](BUILD_4_FIRST_RUN.md) steps verified end-to-end
- [ ] [`BUILD_4_IMPORT_GUIDE.md`](../automation/make/BUILD_4_IMPORT_GUIDE.md) shared with operators
- [ ] Make history monitoring process defined
- [ ] ERROR row review process defined (daily or per-run)
- [ ] Human review workflow after `READY` documented (`APPROVED` → manual publish → `PUBLISHED`)
- [ ] Operator trained on manual recovery (reset `NEW`, clear `ERROR`)

---

## Go-live

- [ ] All checklist items above marked complete
- [ ] At least one operator trained on manual recovery
- [ ] First production listing processed successfully to `READY`
- [ ] Scenario left ON with confirmed polling interval

---

## Out of scope (Build 4)

These are intentionally **not** included:

- CRM integration
- Analytics
- Scaling / queue infrastructure
- Automatic posting to Telegram or Instagram
