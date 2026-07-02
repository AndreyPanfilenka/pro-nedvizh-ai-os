# BUILD 1 — Backend Core

Minimal FastAPI backend for PRO Nedvizh AI OS. Fetches real estate listing URLs, extracts readable page content, sends it to OpenRouter, validates the JSON response, and returns a normalized property object ready for future Google Sheets export.

## Prerequisites

- Python 3.11+
- OpenRouter API key ([openrouter.ai](https://openrouter.ai))

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your OpenRouter credentials:

```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

## Run locally

```bash
uvicorn app.main:app --reload
```

The API starts at `http://127.0.0.1:8000`.

Interactive docs: `http://127.0.0.1:8000/docs`

## Endpoints

### `GET /health`

Health check.

### `POST /extract-url`

Fetch a listing URL and return extracted page content (no AI parsing).

**Request:**

```json
{
  "source_url": "https://example.com/property"
}
```

**Response:**

```json
{
  "status": "success",
  "source": {
    "url": "https://example.com/property",
    "domain": "example.com",
    "title": "...",
    "description": "...",
    "text": "...",
    "images": ["https://example.com/image.jpg"]
  }
}
```

Errors (fetch timeout, non-200 response, empty HTML) return HTTP 502 with a detail message.

### `POST /process-url`

Fetch a listing URL, extract page content, parse it via OpenRouter, and return normalized property JSON.

**Request:**

```json
{
  "source_url": "https://example.com/property"
}
```

**Response:**

```json
{
  "status": "success",
  "property": {
    "title": "...",
    "price": 18500000,
    "currency": "RUB",
    "city": "Москва",
    "district": "...",
    "address": "...",
    "rooms": 2,
    "floor": 7,
    "total_area": 58.4,
    "living_area": 32.1,
    "kitchen_area": 10.5,
    "property_type": "apartment",
    "deal_type": "sale",
    "photos": [],
    "description_ai": "...",
    "telegram_text": "...",
    "instagram_text": "...",
    "reels_script": "...",
    "quality_score": 87
  }
}
```

## Project layout

```
app/
  main.py                     # FastAPI app and routes
  config.py                   # Environment configuration
  models/
    property.py               # Pydantic property schema
    source_content.py         # Extracted page content schema
  services/
    url_fetcher.py            # HTTP fetch with browser user-agent
    content_extractor.py      # HTML → title, text, images
    openrouter_client.py      # OpenRouter Chat Completions client
    property_processor.py     # Fetch → extract → OpenRouter → normalize
  utils/
    json_validator.py         # Required-field validation
    logger.py                 # Logging setup
```

## Pipeline

```
POST /extract-url
  → url_fetcher.fetch()
  → content_extractor.extract()
  → SourceContent JSON

POST /process-url
  → url_fetcher.fetch()
  → content_extractor.extract()
  → openrouter_client.parse_property_content()
  → validate + Property model
```

## Scope (Build 1)

- Backend API only
- No frontend
- No database
- No Google Sheets integration
- No Telegram integration
