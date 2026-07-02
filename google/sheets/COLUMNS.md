# COLUMNS

Expanded column reference for the **INBOX** tab in `PRO Nedvizh — Inbox`.

This document supplements [MASTER_TABLE.md](./MASTER_TABLE.md) with examples, stage requirements, formatting, and edit-policy detail for each of the 25 columns.

**Version:** 1.0  
**Tab:** `INBOX`  
**Column count:** 25 (A–Y)

---

## Quick reference map

| Col | Header | Type | Dropdown |
|:---:|--------|------|:--------:|
| A | ID | Plain text (UUID) | — |
| B | STATUS | Dropdown | Yes |
| C | SOURCE | Dropdown | Yes |
| D | SOURCE_URL | Plain text (URL) | — |
| E | TITLE | Plain text | — |
| F | PROPERTY_TYPE | Dropdown | Yes |
| G | DEAL_TYPE | Dropdown | Yes |
| H | CITY | Plain text | — |
| I | DISTRICT | Plain text | — |
| J | ADDRESS | Plain text | — |
| K | PRICE | Number | — |
| L | CURRENCY | Dropdown | Yes |
| M | ROOMS | Number | — |
| N | AREA | Number | — |
| O | FLOOR | Number | — |
| P | PHOTO_COUNT | Number | — |
| Q | MAIN_PHOTO | Plain text (URL) | — |
| R | DESCRIPTION_AI | Long text | — |
| S | TELEGRAM | Long text | — |
| T | INSTAGRAM | Long text | — |
| U | REELS | Long text | — |
| V | QUALITY_SCORE | Number | — |
| W | PUBLISH_STATUS | Dropdown | Yes |
| X | CREATED_AT | Date time | — |
| Y | UPDATED_AT | Date time | — |

---

## A — ID

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Immutable primary key for the listing record. |
| **Type** | Plain text — UUID v4 recommended |
| **Validation** | Required on every row; unique; never empty; max 36 characters |
| **Editable by user** | No |
| **Editable by AI** | No |
| **Example** | `a3f2c891-4b7e-4d2a-9c11-8e4f2a1b0d93` |
| **Required from status** | `NEW` |
| **Format** | Lowercase hex with hyphens; no spaces |

---

## B — STATUS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Pipeline stage for the listing. Controls automation triggers and operator views. |
| **Type** | Dropdown (enum) |
| **Validation** | Required; exact match from allow list — [VALIDATIONS.md#status](./VALIDATIONS.md#status) |
| **Editable by user** | Yes — approval, rejection, archive, and manual recovery only |
| **Editable by AI** | Yes — forward transitions during automated processing |
| **Example** | `READY_FOR_REVIEW` |
| **Required from status** | `NEW` |
| **Default for new rows** | `NEW` |

**Allowed values:** `NEW`, `FETCHING`, `FETCHED`, `READY_FOR_AI`, `AI_PROCESSING`, `READY_FOR_REVIEW`, `APPROVED`, `PUBLISHED`, `ARCHIVED`

---

## C — SOURCE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Listing platform or site family detected after fetch. |
| **Type** | Dropdown (enum) |
| **Validation** | Required from `FETCHED`; allow list — [VALIDATIONS.md#source](./VALIDATIONS.md#source) |
| **Editable by user** | Yes — correction when detection is wrong |
| **Editable by AI** | Yes — set during source identification |
| **Example** | `Cian` |
| **Required from status** | `FETCHED` |

---

## D — SOURCE_URL

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Original intake URL; canonical back-link to the source listing. |
| **Type** | Plain text (URL) |
| **Validation** | Required; must start with `http://` or `https://`; max 2048 characters |
| **Editable by user** | Yes — before fetch starts; correction of typos in `NEW` |
| **Editable by AI** | No |
| **Example** | `https://www.cian.ru/sale/flat/123456789/` |
| **Required from status** | `NEW` |

---

## E — TITLE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Short listing headline for identification in views and AI prompts. |
| **Type** | Plain text |
| **Validation** | Required from `FETCHED`; max 500 characters |
| **Editable by user** | Yes |
| **Editable by AI** | Yes — normalization or light rewrite |
| **Example** | `3-room apartment, 78 m², Moscow, Presnensky` |
| **Required from status** | `FETCHED` |

---

## F — PROPERTY_TYPE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Category of real estate object. |
| **Type** | Dropdown (enum) |
| **Validation** | Required from `FETCHED`; allow list — [VALIDATIONS.md#property_type](./VALIDATIONS.md#property_type) |
| **Editable by user** | Yes |
| **Editable by AI** | Yes — map source labels to canonical values |
| **Example** | `Apartment` |
| **Required from status** | `FETCHED` |

**Allowed values:** `Apartment`, `House`, `Commercial`, `Garage`, `Land`

---

## G — DEAL_TYPE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Sale vs rent classification. |
| **Type** | Dropdown (enum) |
| **Validation** | Required from `FETCHED`; allow list — [VALIDATIONS.md#deal_type](./VALIDATIONS.md#deal_type) |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `Sale` |
| **Required from status** | `FETCHED` |

**Allowed values:** `Sale`, `Rent`

---

## H — CITY

| Attribute | Detail |
|-----------|--------|
| **Purpose** | City or primary locality of the listing. |
| **Type** | Plain text |
| **Validation** | Required from `FETCHED`; max 200 characters |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `Moscow` |
| **Required from status** | `FETCHED` |

---

## I — DISTRICT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | District or neighborhood within the city. |
| **Type** | Plain text |
| **Validation** | Optional; max 200 characters |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `Presnensky` |
| **Required from status** | — |

---

## J — ADDRESS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Street address or best available location string for the unit. |
| **Type** | Plain text |
| **Validation** | Required from `READY_FOR_AI`; max 500 characters |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `Bolshaya Gruzinskaya St, 14, bldg 2` |
| **Required from status** | `READY_FOR_AI` |

---

## K — PRICE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Numeric listing price without formatting symbols. |
| **Type** | Number |
| **Validation** | Number ≥ 0; no currency symbols or thousand separators in cell |
| **Editable by user** | Yes |
| **Editable by AI** | Yes — extract and normalize from source |
| **Example** | `18500000` |
| **Required from status** | When available (recommended from `FETCHED`) |

---

## L — CURRENCY

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Currency for `PRICE`. |
| **Type** | Dropdown (enum) |
| **Validation** | Required when `PRICE` is set; allow list — [VALIDATIONS.md#currency](./VALIDATIONS.md#currency) |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `RUB` |
| **Required from status** | When `PRICE` is populated |
| **Default** | `RUB` when price is in rubles |

---

## M — ROOMS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Room count; `0` = studio. |
| **Type** | Number (integer) |
| **Validation** | Integer ≥ 0 |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `3` (studio: `0`) |
| **Required from status** | Recommended from `FETCHED` |

---

## N — AREA

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Total area in square meters. |
| **Type** | Number |
| **Validation** | Number > 0 for residential types (`Apartment`, `House`); optional for `Land`, `Garage` |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `78.5` |
| **Required from status** | `READY_FOR_AI` for `Apartment` and `House` |

---

## O — FLOOR

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Floor number of the unit (if applicable). |
| **Type** | Number (integer) |
| **Validation** | Integer; negative values allowed for basement levels |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | `7` |
| **Required from status** | — |

---

## P — PHOTO_COUNT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Number of photos retrieved or referenced during fetch. |
| **Type** | Number (integer) |
| **Validation** | Integer ≥ 0 |
| **Editable by user** | No |
| **Editable by AI** | Yes — set by fetch/extraction automation |
| **Example** | `12` |
| **Required from status** | Recommended from `FETCHED` |

---

## Q — MAIN_PHOTO

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Hero image URL for review UI and publishing. |
| **Type** | Plain text (URL) |
| **Validation** | Required from `READY_FOR_REVIEW`; valid `http://` or `https://` URL |
| **Editable by user** | Yes — pick alternate hero image |
| **Editable by AI** | Yes — default to first gallery image |
| **Example** | `https://cdn.example/listings/123/hero.jpg` |
| **Required from status** | `READY_FOR_REVIEW` |

---

## R — DESCRIPTION_AI

| Attribute | Detail |
|-----------|--------|
| **Purpose** | AI-generated property description for publishing. |
| **Type** | Long text |
| **Validation** | Required from `READY_FOR_REVIEW`; wrap text ON |
| **Editable by user** | Yes — edit during QC |
| **Editable by AI** | Yes — generate and regenerate |
| **Example** | Multi-paragraph marketing description |
| **Required from status** | `READY_FOR_REVIEW` |

---

## S — TELEGRAM

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Draft Telegram channel post. |
| **Type** | Long text |
| **Validation** | Required from `READY_FOR_REVIEW`; wrap text ON; respect Telegram length limits in downstream publish step |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | Short post with emoji, price, and link |
| **Required from status** | `READY_FOR_REVIEW` |

---

## T — INSTAGRAM

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Draft Instagram caption. |
| **Type** | Long text |
| **Validation** | Required from `READY_FOR_REVIEW`; wrap text ON |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | Caption with hashtags and call to action |
| **Required from status** | `READY_FOR_REVIEW` |

---

## U — REELS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Script or on-screen text for Reels / short video. |
| **Type** | Long text |
| **Validation** | Required from `READY_FOR_REVIEW`; wrap text ON |
| **Editable by user** | Yes |
| **Editable by AI** | Yes |
| **Example** | Hook + 3 beats + CTA script |
| **Required from status** | `READY_FOR_REVIEW` |

---

## V — QUALITY_SCORE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | QC score (0–100) gating approval. Default approval threshold: ≥ 70. |
| **Type** | Number (integer) |
| **Validation** | Integer from 0 to 100 inclusive |
| **Editable by user** | Yes — reviewer override |
| **Editable by AI** | Yes — automated rubric |
| **Example** | `82` |
| **Required from status** | `APPROVED` |

---

## W — PUBLISH_STATUS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Tracks distribution to Telegram, Instagram, and Reels after human approval. Independent of pipeline `STATUS`. |
| **Type** | Dropdown (enum) |
| **Validation** | Required from `APPROVED`; allow list — [VALIDATIONS.md#publish_status](./VALIDATIONS.md#publish_status) |
| **Editable by user** | Yes |
| **Editable by AI** | Yes — updated by publish automation |
| **Example** | `Ready` |
| **Required from status** | `APPROVED` |
| **Default for new approved rows** | `Not Ready` until explicitly cleared |

---

## X — CREATED_AT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Record creation timestamp (URL submitted). |
| **Type** | Date time |
| **Validation** | Required; immutable; UTC; format `yyyy-mm-dd hh:mm:ss` |
| **Editable by user** | No |
| **Editable by AI** | No |
| **Example** | `2026-07-02 14:30:00` |
| **Required from status** | `NEW` |

---

## Y — UPDATED_AT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Last modification timestamp for any field on the row. |
| **Type** | Date time |
| **Validation** | Required; must be ≥ `CREATED_AT`; updated on every write; UTC |
| **Editable by user** | No |
| **Editable by AI** | Yes — automation updates on each write |
| **Example** | `2026-07-02 15:45:12` |
| **Required from status** | `NEW` |

---

## Stage requirement matrix

Minimum fields populated before a row may hold the given `STATUS`:

| STATUS | Required columns |
|--------|------------------|
| **NEW** | ID, STATUS, SOURCE_URL, CREATED_AT, UPDATED_AT |
| **FETCHING** | NEW minimum |
| **FETCHED** | NEW + SOURCE, TITLE, PROPERTY_TYPE, DEAL_TYPE, CITY |
| **READY_FOR_AI** | FETCHED + ADDRESS, AREA (for Apartment/House) |
| **AI_PROCESSING** | READY_FOR_AI minimum |
| **READY_FOR_REVIEW** | DESCRIPTION_AI, TELEGRAM, INSTAGRAM, REELS, MAIN_PHOTO |
| **APPROVED** | READY_FOR_REVIEW + QUALITY_SCORE, PUBLISH_STATUS |
| **PUBLISHED** | APPROVED minimum; PUBLISH_STATUS reflects live channels |
| **ARCHIVED** | ID, STATUS, UPDATED_AT |

---

## Related documents

- [MASTER_TABLE.md](./MASTER_TABLE.md) — spreadsheet identity and summary table
- [VALIDATIONS.md](./VALIDATIONS.md) — dropdown values and numeric rules
- [VIEWS.md](./VIEWS.md) — filtered views by pipeline stage
