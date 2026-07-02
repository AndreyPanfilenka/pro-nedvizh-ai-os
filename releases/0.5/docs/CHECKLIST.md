# Production Checklist — Release 0.5

Complete every item before accepting live listing traffic.

## Google Sheets

- [ ] Spreadsheet created and named **PRO Nedvizh Database**
- [ ] Tab name matches `SHEET_NAME` placeholder in Make
- [ ] [`MASTER_TABLE_FINAL.csv`](../google/MASTER_TABLE_FINAL.csv) imported — 24 columns A–X
- [ ] Header row frozen
- [ ] Columns A–B frozen (`ID`, `STATUS`)
- [ ] Text wrap enabled on `DESCRIPTION_AI`, `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT`
- [ ] STATUS dropdown applied on column B with all allowed values
- [ ] No extra or missing columns vs template
- [ ] `SPREADSHEET_ID` copied and verified in browser URL
- [ ] Make automation account has Editor access
- [ ] Sheet not publicly shared

## OpenRouter

- [ ] Account created and verified
- [ ] API key generated
- [ ] Spending limit configured
- [ ] Sufficient credit balance for expected volume
- [ ] `OPENROUTER_API_KEY` stored only in Make (not sheet, not git)
- [ ] `MODEL` set to `openai/gpt-4o-mini` (or approved alternative)
- [ ] Test request returns HTTP 200 with JSON in `choices[0].message.content`

## Make.com scenario

- [ ] [`full_pipeline.blueprint.json`](../make/full_pipeline.blueprint.json) imported successfully
- [ ] Google Sheets connected on all Google modules
- [ ] `SPREADSHEET_ID` replaced in every Google module
- [ ] `SHEET_NAME` replaced in Watch Row and all Update Row modules
- [ ] `OPENROUTER_API_KEY` replaced in HTTP Authorization header
- [ ] `MODEL` replaced in HTTP request body
- [ ] HTTP URL is `https://openrouter.ai/api/v1/chat/completions`
- [ ] HTTP headers include `Content-Type`, `HTTP-Referer`, `X-Title`
- [ ] Request body includes `"response_format": { "type": "json_object" }`
- [ ] Parse response enabled on HTTP module
- [ ] `tableFirstRow` = `A1:X1` on all Google modules
- [ ] Scenario saved
- [ ] Scenario turned ON

## Pipeline modules

- [ ] Module 1: Google Sheets Watch Row — polls correct sheet
- [ ] Module 3: Sets `STATUS` = `PROCESSING` on `NEW` rows with URL
- [ ] Module 4: OpenRouter HTTP Request — reads `SOURCE_URL`
- [ ] Module 5: Parse JSON — maps `choices[].message.content`
- [ ] Module 6: Validate JSON — checks required fields and quality_score range
- [ ] Module 7: Updates sheet with all property fields and `STATUS` = `AI_DONE`
- [ ] Module 8: HTTP error handler sets `STATUS` = `ERROR`
- [ ] Module 9: JSON parse error handler sets `STATUS` = `ERROR`
- [ ] Module 10: Validation error handler sets `STATUS` = `ERROR`

## Smoke tests

- [ ] Valid Cian URL: row reaches `AI_DONE` with populated fields
- [ ] `QUALITY_SCORE` is integer 0–100
- [ ] `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT` populated
- [ ] `SOURCE` auto-detected from URL domain
- [ ] `UPDATED_AT` refreshed on success
- [ ] `ERROR` column empty on success
- [ ] Invalid URL: row reaches `ERROR` with message
- [ ] Re-run: clear ERROR, set NEW — row processes again
- [ ] Row with empty `SOURCE_URL` is not picked up
- [ ] Row with STATUS other than `NEW` is not picked up

## Data quality

- [ ] `TITLE` is non-empty after AI_DONE
- [ ] `PROPERTY_TYPE` is valid enum value
- [ ] `DEAL_TYPE` is valid enum value
- [ ] `DESCRIPTION_AI` is Russian prose, no markdown fences
- [ ] `TELEGRAM_TEXT` ≤ 3500 characters
- [ ] `INSTAGRAM_TEXT` includes hashtags
- [ ] `REELS_SCRIPT` includes `[0:00]` timing markers
- [ ] `PHOTOS` is comma-separated URLs or empty
- [ ] No fabricated address when source is ambiguous (null acceptable)

## Security

- [ ] No API keys in spreadsheet cells
- [ ] No API keys committed to git
- [ ] Make scenario access restricted to operators
- [ ] OpenRouter key rotatable without sheet changes
- [ ] Operator accounts use least-privilege sheet access

## Operations

- [ ] [`FIRST_RUN.md`](FIRST_RUN.md) steps verified end-to-end
- [ ] [`ERRORS.md`](ERRORS.md) shared with operators
- [ ] Make history monitoring process defined
- [ ] ERROR row review process defined (daily or per-run)
- [ ] Human review workflow after `AI_DONE` documented for team
- [ ] Telegram/Instagram publishing stage owner assigned

## Go-live

- [ ] All checklist items above marked complete
- [ ] At least one operator trained on manual recovery
- [ ] First production listing processed successfully
- [ ] Scenario left ON with confirmed polling interval
