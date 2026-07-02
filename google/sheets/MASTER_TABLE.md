# MASTER_TABLE

Google Sheets specification for the PRO Nedvizh AI OS **property inbox**.

This document defines **one spreadsheet** with a single operational tab. It is the intake-to-publish queue for listing URLs: extraction, AI content, human review, and publishing coordination.

**Version:** 1.0  
**Status:** Production-ready specification (documentation only)  
**Related:** [COLUMNS.md](./COLUMNS.md) · [VALIDATIONS.md](./VALIDATIONS.md) · [VIEWS.md](./VIEWS.md)

---

## Spreadsheet identity

| Property | Value |
|----------|-------|
| **Spreadsheet name** | `PRO Nedvizh — Inbox` |
| **Number of tabs** | 1 |
| **Tab 1 name** | `INBOX` |
| **Row 1** | Header row (frozen) |
| **Data starts** | Row 2 |
| **One row** | One property listing (`ID` unique per row) |
| **Primary key** | Column A — `ID` |

---

## Tab: INBOX

The INBOX tab is the single source of truth for all listings in the pipeline. Operators and automations read and write the same row as a property moves from URL intake through fetch, AI generation, review, approval, and publish.

### Layout rules

| Rule | Setting |
|------|---------|
| **Freeze** | Row 1 (headers); freeze columns A–B (`ID`, `STATUS`) |
| **Header style** | Bold, background `#f3f3f3`, text wrap OFF |
| **Default row height** | 21 px; auto-expand for long-text rows in review |
| **Timezone** | UTC for `CREATED_AT` and `UPDATED_AT` (document in sheet note) |
| **Sort default** | `CREATED_AT` descending (newest first) when no view is applied |

### Column order

Columns must appear **exactly** in this order (A → Y):

```
ID | STATUS | SOURCE | SOURCE_URL | TITLE | PROPERTY_TYPE | DEAL_TYPE | CITY | DISTRICT | ADDRESS | PRICE | CURRENCY | ROOMS | AREA | FLOOR | PHOTO_COUNT | MAIN_PHOTO | DESCRIPTION_AI | TELEGRAM | INSTAGRAM | REELS | QUALITY_SCORE | PUBLISH_STATUS | CREATED_AT | UPDATED_AT
```

---

## Column specification

For each column: **Purpose**, **Type**, **Validation**, **Editable by user**, **Editable by AI**.

| # | Col | Column | Purpose | Type | Validation | Editable by user | Editable by AI |
|:-:|-----|--------|---------|------|------------|:----------------:|:--------------:|
| 1 | A | **ID** | System-generated unique identifier for the listing row. Primary key across automations and agent context. Never derived from the source URL. | Plain text (UUID) | Required; unique per row; immutable after creation | No | No |
| 2 | B | **STATUS** | Current stage in the processing pipeline (fetch → AI → review → publish). Governs which fields may be written and which views apply. | Dropdown (enum) | Required; allow list — see [VALIDATIONS.md](./VALIDATIONS.md#status) | Yes* | Yes |
| 3 | C | **SOURCE** | Identified listing platform after source detection (e.g. Cian, Avito). Drives extraction and normalization rules. | Dropdown (enum) | Required from `FETCHED` onward; allow list — see [VALIDATIONS.md](./VALIDATIONS.md#source) | Yes | Yes |
| 4 | D | **SOURCE_URL** | Original listing URL submitted at intake. Canonical link back to the source page. | Plain text (URL) | Required; valid `http://` or `https://` URL; max 2048 characters | Yes | No |
| 5 | E | **TITLE** | Short headline for the listing, taken from the source or normalized during extraction. Used in views, review, and as AI input. | Plain text | Required from `FETCHED` onward; max 500 characters | Yes | Yes |
| 6 | F | **PROPERTY_TYPE** | High-level category of the real estate object. | Dropdown (enum) | Required from `FETCHED` onward; allow list — see [VALIDATIONS.md](./VALIDATIONS.md#property_type) | Yes | Yes |
| 7 | G | **DEAL_TYPE** | Transaction mode: sale or rent. | Dropdown (enum) | Required from `FETCHED` onward; allow list — see [VALIDATIONS.md](./VALIDATIONS.md#deal_type) | Yes | Yes |
| 8 | H | **CITY** | City or locality name for the listing. | Plain text | Required from `FETCHED` onward; max 200 characters | Yes | Yes |
| 9 | I | **DISTRICT** | District, microdistrict, or neighborhood within the city. | Plain text | Optional; max 200 characters | Yes | Yes |
| 10 | J | **ADDRESS** | Street-level address or best available location string. | Plain text | Required from `READY_FOR_AI` onward; max 500 characters | Yes | Yes |
| 11 | K | **PRICE** | Listing price as a number without currency symbols or thousand separators. | Number | Optional until available; number ≥ 0 | Yes | Yes |
| 12 | L | **CURRENCY** | ISO 4217 currency code for `PRICE`. | Dropdown (enum) | Required when `PRICE` is set; allow list — see [VALIDATIONS.md](./VALIDATIONS.md#currency) | Yes | Yes |
| 13 | M | **ROOMS** | Number of rooms. Use `0` for studio apartments. | Number | Optional; integer ≥ 0 | Yes | Yes |
| 14 | N | **AREA** | Total area in square meters. | Number | Required from `READY_FOR_AI` onward for residential types; number > 0 | Yes | Yes |
| 15 | O | **FLOOR** | Floor number of the unit. | Number | Optional; integer (negative allowed for basement levels per local convention) | Yes | Yes |
| 16 | P | **PHOTO_COUNT** | Count of photos associated with the listing after fetch. | Number | Optional from `FETCHED` onward; integer ≥ 0 | No | Yes |
| 17 | Q | **MAIN_PHOTO** | URL of the hero / cover image for review and publishing. | Plain text (URL) | Required from `READY_FOR_REVIEW` onward; valid URL | Yes | Yes |
| 18 | R | **DESCRIPTION_AI** | AI-generated property description for publishing. | Long text | Required from `READY_FOR_REVIEW` onward; wrap text ON | Yes | Yes |
| 19 | S | **TELEGRAM** | Draft post text for Telegram channel. | Long text | Required from `READY_FOR_REVIEW` onward; wrap text ON | Yes | Yes |
| 20 | T | **INSTAGRAM** | Draft caption for Instagram post. | Long text | Required from `READY_FOR_REVIEW` onward; wrap text ON | Yes | Yes |
| 21 | U | **REELS** | Script or caption for Reels / short-form video. | Long text | Required from `READY_FOR_REVIEW` onward; wrap text ON | Yes | Yes |
| 22 | V | **QUALITY_SCORE** | QC score (0–100) before approval. Higher is better. | Number | Required before `APPROVED`; integer 0–100 | Yes | Yes |
| 23 | W | **PUBLISH_STATUS** | Channel distribution state after approval. Separate from pipeline `STATUS`. | Dropdown (enum) | Required from `APPROVED` onward; allow list — see [VALIDATIONS.md](./VALIDATIONS.md#publish_status) | Yes | Yes |
| 24 | X | **CREATED_AT** | Timestamp when the row was first created (URL submitted). | Date time | Required; immutable; format `yyyy-mm-dd hh:mm:ss` UTC | No | No |
| 25 | Y | **UPDATED_AT** | Timestamp of the last change to any field on the row. | Date time | Required; must be ≥ `CREATED_AT`; updated on every write | No | Yes |

\* **STATUS — user edit policy:** Users may change `STATUS` only for operational decisions (e.g. `READY_FOR_REVIEW` → `APPROVED`, `APPROVED` → `ARCHIVED`). Automations own forward pipeline transitions (`NEW` → `FETCHING` → `FETCHED` → …). Invalid backward skips should be rejected by automation or highlighted in review views.

---

## Row lifecycle (summary)

| Stage | Typical `STATUS` values | Who writes |
|-------|---------------------------|------------|
| Intake | `NEW` | User / intake automation |
| Fetch & extract | `FETCHING`, `FETCHED` | Fetch automation |
| AI queue & run | `READY_FOR_AI`, `AI_PROCESSING` | Orchestrator, AI agents |
| Human QC | `READY_FOR_REVIEW` | Reviewer (edits drafts) |
| Cleared to publish | `APPROVED` | Reviewer |
| Live | `PUBLISHED` | Publishing automation |
| Closed | `ARCHIVED` | User, reviewer, or system |

Full transition rules: [status-flow.md](../../docs/status-flow.md) (note: INBOX omits the `ANALYZING` status; normalization is folded into `FETCHED` → `READY_FOR_AI`).

---

## Formatting recommendations

| Element | Setting |
|---------|---------|
| **Row 1** | Bold, `#f3f3f3` background, freeze |
| **Columns A–B** | Freeze panes |
| **URL columns** | D (`SOURCE_URL`), Q (`MAIN_PHOTO`) — plain text; optional helper column with `HYPERLINK` if operators prefer clickable links |
| **Long text** | R–U — wrap text ON, vertical align top |
| **Numbers** | K, M, N, O, P, V — right-aligned; no currency symbols in K |
| **Timestamps** | X, Y — `yyyy-mm-dd hh:mm:ss` |
| **STATUS (B)** | Conditional formatting by value — see [VIEWS.md](./VIEWS.md#conditional-formatting) |

---

## Protected ranges

| Column | Who may edit | Reason |
|--------|--------------|--------|
| A (`ID`) | System only | Primary key integrity |
| X (`CREATED_AT`) | System only | Immutable audit |
| B (`STATUS`) | Automation + leads/reviewers | Prevent accidental pipeline skips |
| P (`PHOTO_COUNT`) | Automation only | Derived from fetch; not hand-edited |

All other columns follow the **Editable by user** / **Editable by AI** flags in the table above.

---

## Import notes

When this specification is applied manually in Google Sheets:

1. Create spreadsheet `PRO Nedvizh — Inbox`.
2. Rename the default sheet to `INBOX`.
3. Enter headers in row 1 exactly as listed in [Column order](#column-order).
4. Apply data validation from [VALIDATIONS.md](./VALIDATIONS.md) to columns B, C, F, G, L, W.
5. Apply numeric validation to K, M, N, O, P, V.
6. Create filtered views from [VIEWS.md](./VIEWS.md).
7. Freeze row 1 and columns A–B.

No Apps Script, API, or code is required for initial setup.

---

## Related documents

- [COLUMNS.md](./COLUMNS.md) — expanded per-column reference
- [VALIDATIONS.md](./VALIDATIONS.md) — all dropdown and numeric rules
- [VIEWS.md](./VIEWS.md) — operator filtered views
- [Property schema](../../docs/property-schema.md) — canonical data model
- [Status flow](../../docs/status-flow.md) — pipeline state machine
