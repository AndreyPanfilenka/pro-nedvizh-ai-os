# Property Schema

Production data model for a **single real estate object** in PRO Nedvizh AI OS.

This schema is the canonical record produced after URL intake, extraction, normalization, AI content generation, quality review, and publishing. All integrations (Google Sheets, Make, OpenRouter agents) read and write against this model.

**Version:** 1.0  
**Status:** Production-ready specification (documentation only)

---

## Design principles

| Principle | Rule |
|-----------|------|
| **Single object** | One schema instance = one listing / property offer |
| **Source fidelity** | Original extracted text and media are preserved alongside AI outputs |
| **Pipeline separation** | `status` tracks workflow stage; `publish_status` tracks channel readiness |
| **Nullable by stage** | Fields become required only when the pipeline reaches the stage that produces them |
| **Stable identifiers** | `id` is system-generated and never reused |

---

## Entity overview

```
Property
├── Identity & lifecycle (id, source, source_url, status, timestamps)
├── Classification (title, property_type, deal_type)
├── Location (country → address, coordinates)
├── Economics & size (price, currency, areas, floor, rooms)
├── Physical attributes (year_built, wall_material, amenities)
├── Content (descriptions, photos, channel drafts)
├── Contacts (contact_name, contact_phone, agency)
└── Quality & publishing (quality_score, publish_status)
```

---

## Field reference

### Identity and lifecycle

#### `id`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (UUID v4 recommended) |
| **Required** | Yes — always |
| **Description** | System-generated unique identifier for this property record. Assigned at creation (URL intake). Never derived from the source URL. Used as the primary key across Sheets, automations, and agent context. |
| **Example** | `a3f2c891-4b7e-4d2a-9c11-8e4f2a1b0d93` |
| **Constraints** | Immutable after creation. Must be globally unique within PRO Nedvizh AI OS. |

#### `source`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (controlled vocabulary) |
| **Required** | Yes — from `FETCHED` onward |
| **Description** | Identified listing platform or site family after source detection (e.g. `avito`, `cian`, `yandex_realty`, `domclick`, `custom_site`, `unknown`). Drives extraction strategy and normalization rules. |
| **Example** | `cian` |
| **Constraints** | Lowercase snake_case. Use `unknown` when detection fails but extraction still proceeds manually. |

#### `source_url`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (URL, max 2048 characters) |
| **Required** | Yes — always |
| **Description** | Original listing URL provided by the user or automation. Canonical link back to the source listing. |
| **Example** | `https://www.cian.ru/sale/flat/123456789/` |
| **Constraints** | Must be a valid HTTP/HTTPS URL. Duplicate URLs may exist historically but should trigger deduplication logic in downstream systems. |

#### `status`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` |
| **Required** | Yes — always |
| **Description** | Current stage in the property processing pipeline. Governs which operations are allowed and which fields must be populated. See [status-flow.md](./status-flow.md) for the full state machine. |
| **Allowed values** | `NEW`, `FETCHING`, `FETCHED`, `ANALYZING`, `READY_FOR_AI`, `AI_PROCESSING`, `READY_FOR_REVIEW`, `APPROVED`, `PUBLISHED`, `ARCHIVED` |
| **Default** | `NEW` |

#### `created_at`

| Attribute | Value |
|-----------|-------|
| **Type** | `datetime` (ISO 8601, UTC) |
| **Required** | Yes — always |
| **Description** | Timestamp when the property record was first created (URL submitted). |
| **Example** | `2026-07-02T14:30:00Z` |
| **Constraints** | Immutable. Set once at record creation. |

#### `updated_at`

| Attribute | Value |
|-----------|-------|
| **Type** | `datetime` (ISO 8601, UTC) |
| **Required** | Yes — always |
| **Description** | Timestamp of the last modification to any field on this record. |
| **Example** | `2026-07-02T15:45:12Z` |
| **Constraints** | Updated on every write. Must be ≥ `created_at`. |

---

### Classification

#### `title`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 500 characters) |
| **Required** | Yes — from `FETCHED` onward |
| **Description** | Short human-readable headline for the listing, typically taken from the source page or synthesized during normalization. Used in Sheets views, review UI, and as input to AI drafts. |
| **Example** | `3-room apartment, 78 m², Moscow, Presnensky district` |

#### `property_type`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` |
| **Required** | Yes — from `FETCHED` onward |
| **Description** | Category of real estate object. |
| **Allowed values** | `apartment`, `room`, `house`, `townhouse`, `land`, `commercial`, `garage`, `other` |
| **Example** | `apartment` |
| **Notes** | Map source-specific labels to this vocabulary during normalization. Use `other` only when no mapping exists; document the raw value in internal logs if needed. |

#### `deal_type`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` |
| **Required** | Yes — from `FETCHED` onward |
| **Description** | Transaction type offered in the listing. |
| **Allowed values** | `sale`, `rent`, `daily_rent` |
| **Example** | `sale` |

---

### Location

#### `country`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (ISO 3166-1 alpha-2 recommended) |
| **Required** | Yes — from `FETCHED` onward |
| **Description** | Country where the property is located. |
| **Example** | `RU` |

#### `region`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 200 characters) |
| **Required** | Recommended from `FETCHED`; required from `READY_FOR_AI` |
| **Description** | First-level administrative division (oblast, krai, republic, state, etc.). |
| **Example** | `Moscow Oblast` |

#### `city`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 200 characters) |
| **Required** | Yes — from `FETCHED` onward |
| **Description** | City or settlement name. |
| **Example** | `Moscow` |

#### `district`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 200 characters) |
| **Required** | No |
| **Description** | District, microdistrict, or neighborhood within the city. Often present on Russian listing sites. |
| **Example** | `Presnensky` |

#### `address`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 500 characters) |
| **Required** | Recommended from `FETCHED`; required from `READY_FOR_AI` |
| **Description** | Street-level address or approximate location as shown on the source listing. May be partial for privacy (e.g. street without building number). |
| **Example** | `Bolshaya Gruzinskaya St., building block 1` |

#### `latitude`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (−90.0 to 90.0, up to 7 decimal places) |
| **Required** | No |
| **Description** | WGS-84 latitude from geocoding or source map data. |
| **Example** | `55.7638120` |

#### `longitude`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (−180.0 to 180.0, up to 7 decimal places) |
| **Required** | No |
| **Description** | WGS-84 longitude from geocoding or source map data. |
| **Example** | `37.5623450` |
| **Notes** | If either coordinate is set, both should be set. |

---

### Economics and size

#### `price`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (non-negative, up to 2 decimal places) |
| **Required** | Yes — from `FETCHED` onward when price is available on source; nullable if source omits price |
| **Description** | Listed price in the currency specified by `currency`. Store the numeric amount only — no currency symbols or thousand separators. |
| **Example** | `18500000.00` |

#### `currency`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (ISO 4217, 3 letters) |
| **Required** | Yes — when `price` is set |
| **Description** | Currency of `price`. |
| **Example** | `RUB` |
| **Default** | `RUB` for PRO Nedvizh default market |

#### `area_total`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (positive, square meters, up to 2 decimal places) |
| **Required** | Recommended from `FETCHED`; required from `READY_FOR_AI` for residential types |
| **Description** | Total area of the object in square meters. |
| **Example** | `78.50` |

#### `area_living`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (positive, square meters) |
| **Required** | No |
| **Description** | Living area in square meters (жилая площадь). Common on CIS listings. |
| **Example** | `52.30` |

#### `area_kitchen`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (positive, square meters) |
| **Required** | No |
| **Description** | Kitchen area in square meters. |
| **Example** | `12.10` |

#### `floor`

| Attribute | Value |
|-----------|-------|
| **Type** | `integer` |
| **Required** | No (required for multi-story residential when available on source) |
| **Description** | Floor number of the unit. Ground floor = `1` unless source uses `0` — normalize to source convention and document in extraction notes if needed. |
| **Example** | `7` |

#### `floors_total`

| Attribute | Value |
|-----------|-------|
| **Type** | `integer` (positive) |
| **Required** | No |
| **Description** | Total floors in the building. |
| **Example** | `17` |

#### `rooms`

| Attribute | Value |
|-----------|-------|
| **Type** | `integer` (non-negative) or `string` for studio |
| **Required** | Recommended from `FETCHED` for residential types |
| **Description** | Number of rooms. Use `0` or the literal `studio` for studio apartments — pick one convention system-wide; recommended: integer with `0` = studio. |
| **Example** | `3` |

---

### Physical attributes

#### `year_built`

| Attribute | Value |
|-----------|-------|
| **Type** | `integer` (four digits, e.g. 1900–2100) |
| **Required** | No |
| **Description** | Year the building was constructed or commissioned. |
| **Example** | `2018` |

#### `wall_material`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` or `string` |
| **Required** | No |
| **Description** | Primary wall / structural material of the building. |
| **Allowed values (preferred)** | `brick`, `monolith`, `panel`, `block`, `wood`, `other` |
| **Example** | `monolith` |

#### `balcony`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` |
| **Required** | No |
| **Description** | Balcony or loggia availability. |
| **Allowed values** | `none`, `balcony`, `loggia`, `both`, `unknown` |
| **Example** | `loggia` |

#### `parking`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` |
| **Required** | No |
| **Description** | Parking availability associated with the property. |
| **Allowed values** | `none`, `street`, `yard`, `underground`, `garage`, `unknown` |
| **Example** | `underground` |

#### `heating`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` or `string` |
| **Required** | No |
| **Description** | Heating type for the unit or building. |
| **Allowed values (preferred)** | `central`, `individual_gas`, `individual_electric`, `none`, `unknown` |
| **Example** | `central` |

#### `condition`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` or `string` |
| **Required** | No |
| **Description** | Finish / repair condition of the interior. |
| **Allowed values (preferred)** | `needs_repair`, `cosmetic`, `good`, `euro`, `designer`, `unknown` |
| **Example** | `euro` |

---

### Content and media

#### `description_original`

| Attribute | Value |
|-----------|-------|
| **Type** | `text` (unbounded) |
| **Required** | Recommended from `FETCHED` |
| **Description** | Verbatim or lightly cleaned description text from the source listing. Preserved for audit, re-generation, and comparison with AI output. |
| **Example** | `Spacious three-room apartment with panoramic windows…` |

#### `description_ai`

| Attribute | Value |
|-----------|-------|
| **Type** | `text` (unbounded) |
| **Required** | Yes — from `READY_FOR_REVIEW` onward |
| **Description** | Marketing description generated by AI from structured fields and `description_original`. Primary long-form copy for review and channel adaptation. |
| **Example** | `Discover a bright 78 m² home in the heart of Presnensky…` |

#### `photo_urls`

| Attribute | Value |
|-----------|-------|
| **Type** | `array` of `string` (URLs), serialized as JSON in tabular storage |
| **Required** | Recommended from `FETCHED`; at least one URL required from `READY_FOR_REVIEW` |
| **Description** | Ordered list of image URLs extracted from the source or uploaded assets. Order reflects source gallery order unless explicitly reordered during QC. |
| **Example** | `["https://cdn.example/1.jpg", "https://cdn.example/2.jpg"]` |

#### `main_photo`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (URL) |
| **Required** | Yes — from `READY_FOR_REVIEW` onward |
| **Description** | Primary hero image for previews, Telegram, and Instagram. Must be one of `photo_urls` or a validated override URL. |
| **Example** | `https://cdn.example/1.jpg` |

---

### Contacts

#### `contact_name`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 200 characters) |
| **Required** | No |
| **Description** | Agent or owner name as shown on the listing. |
| **Example** | `Anna Petrova` |

#### `contact_phone`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (E.164 recommended) |
| **Required** | No |
| **Description** | Contact phone number. Normalize to E.164 when possible (`+79001234567`). |
| **Example** | `+79001234567` |
| **Notes** | Handle as sensitive PII in retention and access policies. |

#### `agency`

| Attribute | Value |
|-----------|-------|
| **Type** | `string` (max 300 characters) |
| **Required** | No |
| **Description** | Real estate agency or developer name associated with the listing. |
| **Example** | `PRO Nedvizh` |

---

### Channel drafts

#### `telegram_text`

| Attribute | Value |
|-----------|-------|
| **Type** | `text` (max ~4096 characters for Telegram compatibility) |
| **Required** | Yes — from `READY_FOR_REVIEW` onward |
| **Description** | Formatted draft post for Telegram (Markdown or plain text per channel rules). Includes key facts, CTA, and contact block as defined by PRO Nedvizh templates. |
| **Example** | `🏠 3-room · 78 m² · Presnensky\n\n18500000 ₽…` |

#### `instagram_text`

| Attribute | Value |
|-----------|-------|
| **Type** | `text` (max ~2200 characters) |
| **Required** | Yes — from `READY_FOR_REVIEW` onward |
| **Description** | Instagram caption draft including hooks, body copy, hashtags, and emoji per brand guidelines. |
| **Example** | `Your next home in Presnensky ✨\n\n3 rooms · 78 m²…\n\n#moscow #realestate` |

#### `reels_script`

| Attribute | Value |
|-----------|-------|
| **Type** | `text` (structured plain text or markdown) |
| **Required** | Yes — from `READY_FOR_REVIEW` onward |
| **Description** | Short-form video script: hook, scene list, on-screen text, voiceover lines, timing notes, and CTA. Consumed by video production or Reels publishing workflow. |
| **Example** | `[0:00] HOOK: "78 m² in the center"\n[0:03] SHOT: living room pan…` |

---

### Quality and publishing

#### `quality_score`

| Attribute | Value |
|-----------|-------|
| **Type** | `decimal` (0.0–100.0, up to 1 decimal place) |
| **Required** | Recommended at `READY_FOR_REVIEW`; required before `APPROVED` |
| **Description** | Composite quality score from automated checks and/or human rubric (completeness, accuracy, copy quality, media quality). Used to prioritize review and gate approval. |
| **Example** | `87.5` |
| **Constraints** | `0` = failed QC; typical approval threshold defined in workflow docs (e.g. ≥ 70). |

#### `publish_status`

| Attribute | Value |
|-----------|-------|
| **Type** | `enum` |
| **Required** | Yes — from `APPROVED` onward |
| **Description** | Channel-agnostic publishing readiness distinct from pipeline `status`. Tracks whether approved content has been scheduled or released. |
| **Allowed values** | `not_ready`, `ready`, `scheduled`, `partially_published`, `published`, `failed` |
| **Default** | `not_ready` |
| **Notes** | A record can have `status` = `APPROVED` and `publish_status` = `ready` before any channel post goes live. When all target channels are live, use `published`. |

---

## Required fields by pipeline stage

Summary of minimum field completeness before a status transition is allowed. See [status-flow.md](./status-flow.md) for transition rules.

| Stage | Minimum required fields |
|-------|-------------------------|
| **NEW** | `id`, `source_url`, `status`, `created_at`, `updated_at` |
| **FETCHED** | Above + `source`, `title`, `property_type`, `deal_type`, `country`, `city` |
| **READY_FOR_AI** | FETCHED minimum + `address` (or explicit geolocation), `area_total` for residential |
| **READY_FOR_REVIEW** | Above + `description_ai`, `main_photo`, `photo_urls` (≥1), `telegram_text`, `instagram_text`, `reels_script` |
| **APPROVED** | Above + `quality_score`, `publish_status` |
| **PUBLISHED** | Above + `publish_status` ∈ {`partially_published`, `published`} |

---

## Serialization notes

| Context | Convention |
|---------|------------|
| **Google Sheets** | See [PROPERTY_TABLE_SPEC.md](../google/sheets/PROPERTY_TABLE_SPEC.md) |
| **JSON APIs** | camelCase or snake_case — pick one per integration; canonical doc uses snake_case |
| **Arrays** | `photo_urls` stored as JSON string in Sheets; native JSON array in API payloads |
| **Enums** | Stored as uppercase strings in Sheets for `status`; lowercase snake_case for other enums unless noted |
| **Empty values** | Use empty cell / `null`, not placeholder strings like `N/A` |

---

## Related documents

- [Status flow](./status-flow.md) — pipeline state machine
- [Google Sheets property table](../google/sheets/PROPERTY_TABLE_SPEC.md) — operational column layout
- [Root README](../README.md) — end-to-end workflow overview
