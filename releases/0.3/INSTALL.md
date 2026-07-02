# Install Guide — Release 0.3 MVP

Step-by-step setup for the URL → OpenRouter → Google Sheets pipeline.

## 1. Google Sheet

1. Create a new Google Spreadsheet named **PRO Nedvizh Database**.
2. Rename the first tab to `INBOX` (or keep default and update the Make blueprint `sheetId`).
3. Import [`google/PRO_NEDVIZH_DATABASE_TEMPLATE.csv`](google/PRO_NEDVIZH_DATABASE_TEMPLATE.csv):
   - File → Import → Upload → Replace current sheet.
4. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
5. Optional: add data validation on column B (`STATUS`):
   - `NEW`, `PROCESSING`, `AI_DONE`, `READY_FOR_REVIEW`, `ERROR`, `APPROVED`, `PUBLISHED`
6. Freeze row 1. Enable wrap on long-text columns (`DESCRIPTION_AI` through `REELS_SCRIPT`).

### Adding a listing

1. Generate a UUID for `ID` (or use `=UUID()` in a helper column).
2. Set `STATUS` = `NEW`.
3. Paste the listing URL into `SOURCE_URL`.
4. Set `CREATED_AT` and `UPDATED_AT` (e.g. `2026-07-02 14:30:00`).

Leave AI columns empty. Automation fills them.

## 2. OpenRouter

1. Sign up at [https://openrouter.ai](https://openrouter.ai).
2. Create an API key.
3. Store the key securely (Make connection or scenario variable — never commit to git).
4. Recommended model: `openai/gpt-4o-mini` (set as `MODEL_NAME`).
5. Verify the request shape against [`openrouter/openrouter_request_example.json`](openrouter/openrouter_request_example.json).

### API endpoint

```
POST https://openrouter.ai/api/v1/chat/completions
Authorization: Bearer OPENROUTER_API_KEY
Content-Type: application/json
HTTP-Referer: https://pro-nedvizh.ai
X-Title: PRO Nedvizh AI OS 0.3
```

## 3. Make.com scenario

1. Open Make.com → Scenarios → Create a new scenario.
2. Import [`make/property_intake_ai_v0_3.blueprint.json`](make/property_intake_ai_v0_3.blueprint.json):
   - ⋮ menu → Import Blueprint → paste or upload JSON.
3. Connect Google Sheets:
   - Create or select a Google connection.
   - Note the connection ID (shown in module settings after linking).
4. Replace placeholders in every module:

| Placeholder | Replace with |
|-------------|--------------|
| `GOOGLE_CONNECTION_ID` | Your Google Sheets connection ID |
| `SPREADSHEET_ID` | Spreadsheet ID from step 1.4 |
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `MODEL_NAME` | `openai/gpt-4o-mini` |

5. Open the **OpenRouter Chat Completions** HTTP module and confirm:
   - URL: `https://openrouter.ai/api/v1/chat/completions`
   - Body includes `response_format: { "type": "json_object" }`
   - System message references [`prompts/property_ai_agent_prompt.md`](prompts/property_ai_agent_prompt.md)
6. Save and turn the scenario **ON**.

### Module flow (reference)

```
Watch Rows → Filter STATUS=NEW → Update PROCESSING
  → HTTP OpenRouter → Parse JSON → Update row + AI_DONE
Error handler → Update STATUS=ERROR + ERROR message
```

## 4. Smoke test

1. Add one row from [`tests/test_urls.csv`](tests/test_urls.csv) with `STATUS = NEW`.
2. Wait for Make to run (watch scenario history).
3. Confirm:
   - `STATUS` becomes `AI_DONE`
   - `SOURCE`, `TITLE`, content columns populated
   - `UPDATED_AT` refreshed
4. Test failure path with `test-005` URL; confirm `STATUS = ERROR` and `ERROR` message set.

## 5. Operations

| Action | How |
|--------|-----|
| Re-run AI on a row | Set `STATUS` back to `NEW` (clear `ERROR` first) |
| Human review | After `AI_DONE`, edit drafts; set `READY_FOR_REVIEW` → `APPROVED` |
| Troubleshoot | Check Make execution history + OpenRouter usage dashboard |

## 6. Security checklist

- [ ] API keys only in Make (not in the sheet or git)
- [ ] Sheet shared with minimum required Google accounts
- [ ] Make scenario access restricted to operators
- [ ] OpenRouter spending limit configured

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| Row stays `NEW` | Scenario off, wrong spreadsheet ID, or filter mismatch |
| Row stuck `PROCESSING` | Run failed mid-flight; check Make history; set `ERROR` manually and retry |
| `ERROR`: JSON parse | Model returned non-JSON; tighten prompt; enable `json_object` response format |
| `ERROR`: HTTP 401 | Invalid `OPENROUTER_API_KEY` |
| Empty AI fields | Model timeout; increase `max_tokens`; retry |
