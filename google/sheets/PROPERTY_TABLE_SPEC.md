# PROPERTY_TABLE_SPEC

Google Sheets layout for the PRO Nedvizh AI OS **property registry**.

This document maps the canonical [property schema](../../docs/property-schema.md) to a single spreadsheet tab operators use for intake, monitoring, review, and publishing coordination. It is the operational mirror of the data model — not a separate schema.

**Version:** 1.0  
**Status:** Production-ready specification (documentation only)

---

## Sheet identity

| Property | Value |
|----------|-------|
| **Spreadsheet name** | `PRO Nedvizh — Property Registry` (recommended) |
| **Tab name** | `Properties` |
| **Row 1** | Header row (frozen) |
| **Data starts** | Row 2 |
| **One row** | One property record (`id` unique per row) |

---

## Column layout

Columns are ordered for left-to-right operational priority: identity and pipeline state first, location and economics next, content and drafts last.

| Col | Header | Schema field | Type (Sheets) | Required | Notes |
|:---:|--------|--------------|---------------|:--------:|-------|
| A | `id` | `id` | Plain text | Yes | UUID; never edit after creation |
| B | `source_url` | `source_url` | Plain text (URL) | Yes | Intake URL; clickable |
| C | `status` | `status` | Plain text (enum) | Yes | Data validation — see below |
| D | `publish_status` | `publish_status` | Plain text (enum) | From APPROVED | Data validation — see below |
| E | `source` | `source` | Plain text | From FETCHED | e.g. `cian`, `avito` |
| F | `created_at` | `created_at` | Date time | Yes | UTC; format `yyyy-mm-dd hh:mm` |
| G | `updated_at` | `updated_at` | Date time | Yes | UTC; auto-updated by automation |
| H | `title` | `title` | Plain text | From FETCHED | Short listing headline |
| I | `property_type` | `property_type` | Plain text (enum) | From FETCHED | Data validation |
| J | `deal_type` | `deal_type` | Plain text (enum) | From FETCHED | Data validation |
| K | `country` | `country` | Plain text | From FETCHED | ISO alpha-2 preferred |
| L | `region` | `region` | Plain text | Recommended | Oblast / state |
| M | `city` | `city` | Plain text | From FETCHED | |
| N | `district` | `district` | Plain text | No | |
| O | `address` | `address` | Plain text | From READY_FOR_AI | |
| P | `latitude` | `latitude` | Number | No | Decimal degrees |
| Q | `longitude` | `longitude` | Number | No | Decimal degrees |
| R | `price` | `price` | Number | When available | No currency symbols |
| S | `currency` | `currency` | Plain text | When price set | Default `RUB` |
| T | `area_total` | `area_total` | Number | From READY_FOR_AI* | Square meters |
| U | `area_living` | `area_living` | Number | No | Square meters |
| V | `area_kitchen` | `area_kitchen` | Number | No | Square meters |
| W | `floor` | `floor` | Number | No | Integer |
| X | `floors_total` | `floors_total` | Number | No | Integer |
| Y | `rooms` | `rooms` | Number | Recommended | `0` = studio |
| Z | `year_built` | `year_built` | Number | No | Four-digit year |
| AA | `wall_material` | `wall_material` | Plain text (enum) | No | Data validation |
| AB | `balcony` | `balcony` | Plain text (enum) | No | Data validation |
| AC | `parking` | `parking` | Plain text (enum) | No | Data validation |
| AD | `heating` | `heating` | Plain text (enum) | No | Data validation |
| AE | `condition` | `condition` | Plain text (enum) | No | Data validation |
| AF | `quality_score` | `quality_score` | Number | Before APPROVED | 0–100 |
| AG | `contact_name` | `contact_name` | Plain text | No | PII — restrict sharing |
| AH | `contact_phone` | `contact_phone` | Plain text | No | E.164 preferred |
| AI | `agency` | `agency` | Plain text | No | |
| AJ | `main_photo` | `main_photo` | Plain text (URL) | From READY_FOR_REVIEW | Hero image URL |
| AK | `photo_urls` | `photo_urls` | Plain text (JSON) | From READY_FOR_REVIEW | JSON array of URLs |
| AL | `description_original` | `description_original` | Long text | Recommended | Wrap text ON |
| AM | `description_ai` | `description_ai` | Long text | From READY_FOR_REVIEW | Wrap text ON |
| AN | `telegram_text` | `telegram_text` | Long text | From READY_FOR_REVIEW | Wrap text ON |
| AO | `instagram_text` | `instagram_text` | Long text | From READY_FOR_REVIEW | Wrap text ON |
| AP | `reels_script` | `reels_script` | Long text | From READY_FOR_REVIEW | Wrap text ON |

\*Residential types: `apartment`, `room`, `house`, `townhouse`.

---

## Data validation rules

Apply via **Data → Data validation** on the `Properties` tab.

### `status` (column C)

Allow list (exact match, reject invalid):

```
NEW
FETCHING
FETCHED
ANALYZING
READY_FOR_AI
AI_PROCESSING
READY_FOR_REVIEW
APPROVED
PUBLISHED
ARCHIVED
```

### `publish_status` (column D)

```
not_ready
ready
scheduled
partially_published
published
failed
```

### `property_type` (column I)

```
apartment
room
house
townhouse
land
commercial
garage
other
```

### `deal_type` (column J)

```
sale
rent
daily_rent
```

### `wall_material` (column AA)

```
brick
monolith
panel
block
wood
other
```

### `balcony` (column AB)

```
none
balcony
loggia
both
unknown
```

### `parking` (column AC)

```
none
street
yard
underground
garage
unknown
```

### `heating` (column AD)

```
central
individual_gas
individual_electric
none
unknown
```

### `condition` (column AE)

```
needs_repair
cosmetic
good
euro
designer
unknown
```

### Numeric ranges

| Column | Rule |
|--------|------|
| `quality_score` (AF) | Number between 0 and 100 |
| `latitude` (P) | Number between -90 and 90 |
| `longitude` (Q) | Number between -180 and 180 |
| `price`, areas (R, T–V) | Number ≥ 0 |
| `floor`, `floors_total`, `rooms`, `year_built` (W, X, Y, Z) | Number ≥ 0 (year ≥ 1800 recommended) |

---

## Formatting recommendations

| Element | Setting |
|---------|---------|
| **Row 1** | Bold, background `#f3f3f3`, freeze |
| **Columns A–G** | Freeze panes (identity + pipeline visible while scrolling) |
| **URL columns** | B, AJ — plain text; use `=HYPERLINK(url, "open")` in a helper column if needed |
| **Long text** | AL–AP — wrap text, vertical align top, row height auto |
| **Timestamps** | F, G — consistent timezone (UTC) documented in sheet note |
| **Status column C** | Conditional formatting by status — see below |

### Conditional formatting for `status` (column C)

| Status | Background (suggested) |
|--------|------------------------|
| NEW, FETCHING | `#fff3cd` (yellow) |
| FETCHED, ANALYZING, READY_FOR_AI, AI_PROCESSING | `#cce5ff` (blue) |
| READY_FOR_REVIEW | `#f8d7da` (red tint — action needed) |
| APPROVED | `#d4edda` (green) |
| PUBLISHED | `#d1ecf1` (teal) |
| ARCHIVED | `#e2e3e5` (gray) |

### Conditional formatting for `publish_status` (column D)

| Value | Background (suggested) |
|-------|------------------------|
| `failed` | `#f8d7da` |
| `published` | `#d4edda` |
| `scheduled` | `#fff3cd` |

---

## `photo_urls` JSON format

Store as a **single cell** JSON array string. Automation and imports must parse valid JSON.

**Valid example:**

```json
["https://cdn.example/photo1.jpg","https://cdn.example/photo2.jpg"]
```

**Rules:**

- Double quotes around URLs
- No trailing comma
- `main_photo` (AJ) must equal one entry in this array (or approved override URL)
- Max practical cell length ~50,000 characters; if gallery exceeds limit, store first N URLs and link to Drive folder in internal notes (future extension)

---

## Row lifecycle (operator view)

| Action | How |
|--------|-----|
| **Intake new URL** | Append row with `source_url`, set `status` = `NEW`; automation fills `id`, timestamps |
| **Monitor pipeline** | Filter/sort by `status`, `updated_at` |
| **Review queue** | Filter `status` = `READY_FOR_REVIEW`; sort by `quality_score` ascending |
| **Approve** | Set `status` = `APPROVED`, set `publish_status` = `ready`, ensure `quality_score` set |
| **Mark published** | Set `status` = `PUBLISHED`, update `publish_status` |
| **Archive** | Set `status` = `ARCHIVED` |

Full transition rules: [status-flow.md](../../docs/status-flow.md).

---

## Protected ranges

| Range | Who can edit | Reason |
|-------|--------------|--------|
| A (`id`) | Automation only | Primary key integrity |
| F (`created_at`) | Automation only | Immutable audit |
| C (`status`) | Automation + leads | Prevent accidental skip of QC |
| AL (`description_original`) | Automation preferred | Source fidelity |

Editors may always adjust draft columns (AN–AP) during READY_FOR_REVIEW per team policy.

---

## Optional helper columns (not in canonical schema)

These may be added **after column AP** for operations. They are not part of the property schema v1.

| Header | Purpose |
|--------|---------|
| `_reviewer` | Email of approver |
| `_review_notes` | QC comments |
| `_archive_reason` | Why ARCHIVED |
| `_last_error` | Last automation error message |
| `_drive_folder` | Link to media folder in Google Drive |

Prefix with `_` to distinguish from schema fields.

---

## Import and export

| Direction | Format | Notes |
|-----------|--------|-------|
| **Export** | CSV / JSON | Serialize `photo_urls` as JSON string in CSV |
| **Import** | CSV | Validate enums before bulk load; generate new `id` per row |
| **Make.com** | Row watch / update | Watch `status` and `updated_at` for triggers |

---

## Related documents

- [Property schema](../../docs/property-schema.md) — field definitions and types
- [Status flow](../../docs/status-flow.md) — allowed status transitions
- [Google Sheets README](./README.md) — integration scope
