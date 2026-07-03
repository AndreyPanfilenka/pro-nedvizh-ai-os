# BUILD 5 — Production Checklist

Complete every item before accepting live listing traffic.

**Architecture:** Google Sheets + Make + OpenRouter only. No backend, Render, Cloudflare, ngrok, or local server.

---

## Google Sheets

- [ ] Spreadsheet created and named **PRO Nedvizh Publications**
- [ ] Tab name matches `SHEET_NAME` placeholder in Make
- [ ] [`BUILD_5_SHEET_TEMPLATE.csv`](../google/sheets/BUILD_5_SHEET_TEMPLATE.csv) imported — 11 columns A–K
- [ ] Header row frozen
- [ ] Columns A–B frozen (`ID`, `STATUS`)
- [ ] Text wrap enabled on `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT`
- [ ] STATUS dropdown applied on column B with all six allowed values:
  - `NEW`, `PROCESSING`, `READY`, `ERROR`, `APPROVED`, `PUBLISHED`
- [ ] No extra or missing columns vs template
- [ ] `SPREADSHEET_ID` copied and verified in browser URL
- [ ] Make automation account has Editor access
- [ ] Sheet not publicly shared

---

## OpenRouter

- [ ] API key created at [openrouter.ai/keys](https://openrouter.ai/keys)
- [ ] Account has sufficient credits
- [ ] Key stored **only** in Make HTTP Authorization header (not in sheet, not in git)
- [ ] Model set to `openai/gpt-4o-mini`
- [ ] `response_format.type` = `json_object`

---

## System prompt

- [ ] [`build_5_openrouter_prompt.md`](../prompts/build_5_openrouter_prompt.md) copied into HTTP module system message
- [ ] Prompt language is Russian
- [ ] Prompt includes conservative / no-fake-facts instructions for URL-only input
- [ ] Prompt specifies PRO Nedvizh brand and region (Mozyr, Kalinkovichi, Narovlya, Yelsk)
- [ ] Prompt requires JSON shape: `title`, `telegram_text`, `instagram_text`, `reels_script`, `hashtags`

---

## Make.com scenario

- [ ] [`build_5_direct_openrouter_pipeline.blueprint.json`](../automation/make/build_5_direct_openrouter_pipeline.blueprint.json) imported successfully
- [ ] Google Sheets connected on all Google modules (1, 3, 7, 8, 9, 10)
- [ ] `SPREADSHEET_ID` replaced in every Google module
- [ ] `SHEET_NAME` replaced in Watch Rows and all Update Row modules
- [ ] `OPENROUTER_API_KEY` replaced in HTTP module Authorization header
- [ ] `SYSTEM_PROMPT` replaced in HTTP body (not left as literal placeholder)
- [ ] HTTP URL is `https://openrouter.ai/api/v1/chat/completions`
- [ ] HTTP method is `POST`
- [ ] Temperature is `0.4`
- [ ] User message sends row `SOURCE_URL` via `{{1.`SOURCE_URL`}}`
- [ ] `tableFirstRow` = `A1:K1` on all Google modules
- [ ] Scenario saved
- [ ] Scenario turned ON

---

## Pipeline modules

- [ ] Module 1: Google Sheets Watch Rows — polls correct sheet and tab
- [ ] Module 3: Sets `STATUS` = `PROCESSING` only when `STATUS` = `NEW` and `SOURCE_URL` present
- [ ] Module 4: HTTP POST to OpenRouter with Bearer auth and JSON body
- [ ] Module 5: Parse JSON from `{{4.data.choices[].message.content}}`
- [ ] Module 6: Validates `title`, `telegram_text`, `instagram_text`, `reels_script` present
- [ ] Module 7: Updates sheet with `STATUS` = `READY` and all publication fields
- [ ] Module 8: HTTP error handler sets `STATUS` = `ERROR`
- [ ] Module 9: JSON parse error handler sets `STATUS` = `ERROR`
- [ ] Module 10: Validation error handler sets `STATUS` = `ERROR`

---

## Smoke tests

- [ ] Valid listing URL: row reaches `READY` with all drafts populated
- [ ] `HASHTAGS` is space-separated text (from JSON array)
- [ ] `UPDATED_AT` refreshed on success
- [ ] `ERROR` column empty on success
- [ ] Invalid API key: row reaches `ERROR` with HTTP message
- [ ] Re-run: clear `ERROR`, set `NEW` — row processes again
- [ ] Row with empty `SOURCE_URL` is not picked up
- [ ] Row with `STATUS` other than `NEW` is not picked up
- [ ] Row with `STATUS` = `PROCESSING` is not re-processed until reset to `NEW`

---

## Data quality (URL-only MVP)

- [ ] `TITLE` is non-empty Russian headline after `READY`
- [ ] Drafts do not invent specific prices, addresses, or room counts unless derivable from URL
- [ ] Drafts include verification notes when facts are uncertain
- [ ] `TELEGRAM_TEXT` is ready-to-edit prose
- [ ] `INSTAGRAM_TEXT` includes caption-style content
- [ ] `REELS_SCRIPT` includes timing markers (e.g. `[0:00]`)
- [ ] `HASHTAGS` contains 8–15 tags without `#` prefix
- [ ] Content matches Belarus / PRO Nedvizh brand tone
- [ ] Operator workflow: fact-check listing page → edit drafts → `APPROVED`

---

## Security

- [ ] No API keys in spreadsheet cells
- [ ] OpenRouter key stored only in Make HTTP module
- [ ] No secrets committed to git
- [ ] Make scenario access restricted to operators
- [ ] `.env` not shared or committed (if used locally for other work)

---

## Operations

- [ ] [`BUILD_5_FIRST_RUN.md`](BUILD_5_FIRST_RUN.md) steps verified end-to-end
- [ ] [`BUILD_5_IMPORT_GUIDE.md`](../automation/make/BUILD_5_IMPORT_GUIDE.md) shared with operators
- [ ] Make history monitoring process defined
- [ ] ERROR row review process defined (daily or per-run)
- [ ] Human review workflow after `READY` documented (`APPROVED` → manual publish → `PUBLISHED`)
- [ ] Operator trained on manual recovery (reset `NEW`, clear `ERROR`)
- [ ] Operator trained on manual fact-checking (URL-only drafts require editing)

---

## Go-live

- [ ] All checklist items above marked complete
- [ ] At least one operator trained on manual recovery and fact-checking
- [ ] First production listing processed successfully to `READY`
- [ ] First listing edited and moved to `APPROVED` after human review
- [ ] Scenario left ON with confirmed polling interval

---

## Out of scope (Build 5)

These are intentionally **not** included:

- Custom backend / Python API
- Render, Cloudflare Tunnel, ngrok, local server
- Automatic page fetch / HTML parsing
- CRM integration
- Analytics
- Automatic posting to Telegram or Instagram
