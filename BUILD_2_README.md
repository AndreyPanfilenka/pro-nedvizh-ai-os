# BUILD 2 — Publication Generation

Extends the Build 1 backend with ready-to-publish social media content from a single property URL. No Telegram API, Instagram API, Google Sheets, frontend, or database.

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

Fetch a listing URL and return extracted page content (no AI parsing). Unchanged from Build 1.

### `POST /process-url`

Fetch a listing URL, extract page content, parse it via OpenRouter, and return normalized property JSON. Unchanged from Build 1.

### `POST /generate-publication`

Full pipeline: fetch URL → extract content → parse property → generate publication drafts for Telegram and Instagram.

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
  "source_url": "https://example.com/property",
  "property": {
    "title": "...",
    "price": 85000,
    "currency": "USD",
    "city": "Мозырь",
    "district": "...",
    "address": "...",
    "rooms": 2,
    "floor": 5,
    "total_area": 54.0,
    "living_area": 30.0,
    "kitchen_area": 9.0,
    "property_type": "apartment",
    "deal_type": "sale",
    "photos": [],
    "description_ai": "...",
    "telegram_text": "...",
    "instagram_text": "...",
    "reels_script": "...",
    "quality_score": 82
  },
  "publication": {
    "title": "2-комн. квартира в центре Мозыря",
    "telegram_text": "...",
    "instagram_text": "...",
    "reels_script": "...",
    "hashtags": ["недвижимость", "мозырь", "pronnedvizh"]
  }
}
```

Errors (fetch failure, OpenRouter error, validation failure) return HTTP 502 with a detail message.

## Publication content

Generated content is tailored for **Belarus real estate** in **Russian**, brand **PRO Nedvizh**, with regional focus on **Мозырь, Калинковичи, Наровля, Ельск** and nearby areas.

| Field | Description |
|-------|-------------|
| `title` | Short catchy headline |
| `telegram_text` | Ready-to-post Telegram message |
| `instagram_text` | Ready-to-post Instagram caption |
| `reels_script` | 30–45 second Reels voiceover script with timestamps |
| `hashtags` | 8–15 relevant hashtags (without `#` prefix) |

## Project layout (Build 2 additions)

```
app/
  models/
    publication.py            # Publication schema and request/response models
  services/
    publication_generator.py  # OpenRouter publication content generation
    property_processor.py     # + generate_publication() pipeline method
  main.py                     # + POST /generate-publication
```

## Pipeline

```
POST /generate-publication
  → url_fetcher.fetch()
  → content_extractor.extract()
  → openrouter_client.parse_property_content()   # property facts
  → publication_generator.generate()             # social content
  → Property + Publication JSON
```

## Scope (Build 2)

- One URL in → ready-to-publish content out
- Backend API only
- No frontend
- No database
- No Google Sheets
- No Telegram API
- No Instagram API
