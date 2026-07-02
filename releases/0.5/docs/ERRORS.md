# Errors — Release 0.5

Error states, causes, and recovery for the full pipeline.

## STATUS = ERROR

The automation sets `STATUS` = `ERROR` and writes a message to the `ERROR` column. Fix the cause, clear `ERROR`, set `STATUS` = `NEW`, and wait for the next run.

## Error categories

### HTTP errors (module 4)

| ERROR pattern | Cause | Fix |
|---------------|-------|-----|
| `HTTP 401` | Invalid or missing `OPENROUTER_API_KEY` | Regenerate key; update Make HTTP module |
| `HTTP 402` | Insufficient OpenRouter credits | Top up balance or raise spending limit |
| `HTTP 429` | Rate limit exceeded | Reduce scenario frequency; retry later |
| `HTTP 500` / `HTTP 502` / `HTTP 503` | OpenRouter or upstream provider outage | Wait and retry; check [OpenRouter status](https://status.openrouter.ai) |
| `HTTP 400` | Malformed request body | Confirm `MODEL` value and JSON body in HTTP module |
| Connection timeout | Network or slow response | Retry; increase Make HTTP timeout if available |

### JSON parse errors (module 5)

| ERROR pattern | Cause | Fix |
|---------------|-------|-----|
| `JSON parse failed` | Model returned non-JSON (markdown fences, prose, truncated output) | Confirm `response_format: json_object` in request; retry row |
| Empty content | Model returned blank response | Retry; check OpenRouter usage logs |
| Truncated JSON | `max_tokens` too low | Increase max_tokens to 8192 in HTTP body |

### JSON validation errors (module 6)

| ERROR pattern | Cause | Fix |
|---------------|-------|-----|
| `JSON validation failed: missing or invalid required fields` | Parsed JSON lacks title, content drafts, property_type, deal_type, or quality_score out of range | Retry row; if persistent, listing URL may be unreachable to the model |
| quality_score = 0 with otherwise valid data | Model returned zero score for ambiguous listing | Review manually; lower scores are valid but must be 0–100 |

## Stuck states

### Row stays NEW

| Cause | Fix |
|-------|-----|
| Scenario is OFF | Turn scenario ON |
| Wrong `SPREADSHEET_ID` | Update all Google modules |
| Wrong `SHEET_NAME` | Match tab name exactly |
| `SOURCE_URL` is empty | Paste a valid URL |
| STATUS is not exactly `NEW` | Fix typo or trailing spaces |
| Make polling delay | Wait up to 15 minutes (default watch interval) |

### Row stuck PROCESSING

| Cause | Fix |
|-------|-----|
| Run failed without error handler firing | Check Make history for incomplete execution |
| Scenario stopped mid-run | Set `STATUS` = `ERROR` manually, note cause, set `NEW` to retry |
| Concurrent edit on same row | Avoid manual edits while automation runs |

### Row reaches AI_DONE but fields empty

| Cause | Fix |
|-------|-----|
| Partial model output passed validation incorrectly | Report as bug; re-run with `NEW` |
| Sheet column mismatch | Confirm headers match [`MASTER_TABLE_FINAL.csv`](../google/MASTER_TABLE_FINAL.csv) exactly |
| `tableFirstRow` mismatch in Make | Set to `A1:X1` in all Google modules |

## Manual recovery procedure

1. Read the `ERROR` column message.
2. Fix the root cause (API key, URL, sheet config, credits).
3. Clear the `ERROR` cell.
4. Set `STATUS` = `NEW`.
5. Update `UPDATED_AT` to current UTC time.
6. Monitor Make history for the next run.

## Re-run policy

| Situation | Action |
|-----------|--------|
| Transient HTTP error | Clear ERROR → NEW → retry once |
| JSON parse failure | Retry up to 2 times |
| Validation failure on valid listing | Review AI output in Make history; adjust URL or retry |
| Invalid URL (404, unreachable) | Do not retry; archive or delete row |

## Monitoring

| Signal | Where |
|--------|-------|
| Failed runs | Make → Scenario → History |
| API usage and cost | OpenRouter → Activity |
| Rows in ERROR | Sheet filter: `STATUS` = `ERROR` |
| Rows awaiting review | Sheet filter: `STATUS` = `AI_DONE` |

## Escalation

If the same URL fails three consecutive times with different error types, stop automated retries and process the listing manually.
