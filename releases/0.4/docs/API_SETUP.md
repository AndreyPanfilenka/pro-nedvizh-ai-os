# API Setup — Release 0.4

Production setup for OpenRouter property parsing in PRO Nedvizh AI OS.

## Overview

| Item | Value |
|------|-------|
| Provider | [OpenRouter](https://openrouter.ai) |
| Endpoint | `POST https://openrouter.ai/api/v1/chat/completions` |
| Default model | `openai/gpt-4o-mini` |
| Input | `source_url` only (passed as user message) |
| Output | Strict JSON per [`response_schema.json`](../openrouter/response_schema.json) |

## 1. OpenRouter account

1. Sign up at [https://openrouter.ai](https://openrouter.ai).
2. Open [API Keys](https://openrouter.ai/keys) and create a key.
3. Set a monthly spending limit under [Settings → Limits](https://openrouter.ai/settings/limits).
4. Store the key in your secrets manager or Make scenario variable — **never commit to git**.

## 2. Request configuration

Reference files:

| File | Purpose |
|------|---------|
| [`openrouter/property_parser_prompt.md`](../openrouter/property_parser_prompt.md) | System prompt — forces strict JSON, no markdown, no explanations |
| [`openrouter/response_schema.json`](../openrouter/response_schema.json) | Output JSON Schema |
| [`openrouter/example_request.json`](../openrouter/example_request.json) | Request body template |
| [`openrouter/example_response.json`](../openrouter/example_response.json) | Full OpenRouter API response example |
| [`make/openrouter_http_module.json`](../make/openrouter_http_module.json) | Make.com HTTP module with placeholders |

### Required headers

```
Authorization: Bearer OPENROUTER_API_KEY
Content-Type: application/json
HTTP-Referer: https://pro-nedvizh.ai
X-Title: PRO Nedvizh AI OS 0.4
```

### Request body parameters

| Parameter | Placeholder | Default | Notes |
|-----------|-------------|---------|-------|
| `model` | `MODEL` | `openai/gpt-4o-mini` | Swap for other OpenRouter models if needed |
| `temperature` | `Temperature` | `0.2` | Keep low for consistent parsing |
| `max_tokens` | `Max tokens` | `4096` | Increase if drafts are truncated |
| `response_format.type` | — | `json_object` | Required for strict JSON output |

### Messages

1. **System** — full contents of `property_parser_prompt.md`.
2. **User** — the listing URL only, e.g. `https://www.cian.ru/sale/flat/312345678/`.

No other input fields are sent to the model.

## 3. Make.com HTTP module

1. Open Make.com → Scenarios → add or edit your scenario.
2. Add an **HTTP → Make a request** module (or import settings from [`make/openrouter_http_module.json`](../make/openrouter_http_module.json)).
3. Replace placeholders:

| Placeholder | Replace with |
|-------------|--------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `MODEL` | `openai/gpt-4o-mini` |
| `HEADERS` | Confirm Referer and X-Title values |
| `BODY` | Paste system prompt from `property_parser_prompt.md`; map `{{source_url}}` from upstream |
| `Temperature` | `0.2` |
| `Max tokens` | `4096` |

4. Enable **Parse response** = Yes.
5. Map downstream modules to parsed JSON at `choices[0].message.content`.

## 4. Response parsing

OpenRouter returns a chat completion envelope. The property JSON is a **string** inside:

```
choices[0].message.content
```

Parse that string as JSON. Validate against [`response_schema.json`](../openrouter/response_schema.json).

Expected top-level keys:

```
title, price, currency, city, district, address, rooms, floor,
total_area, living_area, kitchen_area, property_type, deal_type,
photos, description_ai, telegram_text, instagram_text, reels_script, quality_score
```

## 5. Smoke test

1. Send a test request using [`example_request.json`](../openrouter/example_request.json) with a real listing URL.
2. Confirm HTTP 200 and `finish_reason: "stop"`.
3. Parse `choices[0].message.content` — must be valid JSON with all required keys.
4. Confirm the model did not wrap output in markdown fences or add commentary.

Example with curl (replace `YOUR_KEY` and URL):

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: https://pro-nedvizh.ai" \
  -H "X-Title: PRO Nedvizh AI OS 0.4" \
  -d @releases/0.4/openrouter/example_request.json
```

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 401 | Invalid or missing API key | Regenerate key; update `OPENROUTER_API_KEY` |
| HTTP 402 | Insufficient credits | Top up OpenRouter balance or raise limit |
| HTTP 429 | Rate limit | Back off; reduce scenario frequency |
| Non-JSON content | Model ignored prompt | Re-paste full system prompt; confirm `json_object` format |
| Markdown fences in output | Prompt not applied | Use full `property_parser_prompt.md`; lower temperature |
| Truncated drafts | Token limit | Increase `Max tokens` to 8192 |
| Missing fields | Ambiguous listing | Expected — check `quality_score`; retry with clearer URL |
| Empty `photos` | Images not accessible to model | Normal for some sources; fill manually downstream |

## 7. Security checklist

- [ ] API key stored only in Make or secrets manager
- [ ] Spending limit configured on OpenRouter
- [ ] Scenario access restricted to operators
- [ ] No listing URLs or API keys logged in public channels
- [ ] `HTTP-Referer` and `X-Title` set for OpenRouter attribution
