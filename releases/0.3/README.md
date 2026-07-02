# PRO Nedvizh AI OS — Release 0.3 MVP

**Version:** 0.3  
**Date:** 2026-07-02  
**Scope:** URL intake → OpenRouter AI → Google Sheets write-back

## What this release delivers

A no-code MVP pipeline:

1. User pastes a real estate listing URL into Google Sheets (`STATUS = NEW`).
2. Make watches the sheet, picks up new rows, and sets `STATUS = PROCESSING`.
3. Make sends the URL to OpenRouter (Chat Completions API).
4. AI returns structured property data and channel content drafts as JSON.
5. Make writes fields back to the row and sets `STATUS = AI_DONE`.
6. On failure, Make sets `STATUS = ERROR` and writes the error message to `ERROR`.

## Package contents

| Path | Purpose |
|------|---------|
| [`google/PRO_NEDVIZH_DATABASE_TEMPLATE.csv`](google/PRO_NEDVIZH_DATABASE_TEMPLATE.csv) | Sheet column headers and sample row |
| [`make/property_intake_ai_v0_3.blueprint.json`](make/property_intake_ai_v0_3.blueprint.json) | Importable Make.com scenario |
| [`openrouter/openrouter_request_example.json`](openrouter/openrouter_request_example.json) | Reference API request body |
| [`prompts/property_ai_agent_prompt.md`](prompts/property_ai_agent_prompt.md) | System prompt for the AI agent |
| [`tests/test_urls.csv`](tests/test_urls.csv) | URLs for manual QA |
| [`INSTALL.md`](INSTALL.md) | Step-by-step setup |

## Status values (Release 0.3)

| Status | Meaning |
|--------|---------|
| `NEW` | Row created; URL entered; awaiting automation |
| `PROCESSING` | Make picked up the row; OpenRouter call in progress |
| `AI_DONE` | AI fields written; ready for human review |
| `READY_FOR_REVIEW` | Optional manual promotion after QC |
| `ERROR` | Automation failed; see `ERROR` column |
| `APPROVED` | Human approved content |
| `PUBLISHED` | Content published to channels |

## Placeholders to replace before go-live

| Placeholder | Where |
|-------------|-------|
| `GOOGLE_CONNECTION_ID` | Make Google Sheets modules |
| `SPREADSHEET_ID` | Make Google Sheets modules |
| `OPENROUTER_API_KEY` | Make HTTP module Authorization header |
| `MODEL_NAME` | Make HTTP module request body (`openai/gpt-4o-mini` recommended) |

## Prerequisites

- Google account with Sheets access
- Make.com account (paid plan recommended for polling frequency)
- OpenRouter API key with credits

See [`INSTALL.md`](INSTALL.md) for full setup.

## Out of scope (0.3)

- Application code
- Page fetch / HTML scraping (AI infers from URL context only)
- Publishing to Telegram, Instagram, or Reels
- Automated quality scoring beyond AI-provided `quality_score`

## Related docs

- Root repo: [`../../README.md`](../../README.md)
- Property schema: [`../../docs/property-schema.md`](../../docs/property-schema.md)
