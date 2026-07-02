# BUILD 4 — Google Sheet Columns

Production column reference for the **Build 4** publication pipeline sheet.

**Tab:** `INBOX` (or your chosen name — must match `SHEET_NAME` in Make)  
**Column count:** 11 (A–K)

---

## Quick reference

| Col | Header | Type | Dropdown |
|:---:|--------|------|:--------:|
| A | ID | Plain text (UUID) | — |
| B | STATUS | Dropdown | Yes |
| C | SOURCE_URL | Plain text (URL) | — |
| D | TITLE | Plain text | — |
| E | TELEGRAM_TEXT | Long text | — |
| F | INSTAGRAM_TEXT | Long text | — |
| G | REELS_SCRIPT | Long text | — |
| H | HASHTAGS | Plain text | — |
| I | ERROR | Plain text | — |
| J | CREATED_AT | Date time | — |
| K | UPDATED_AT | Date time | — |

---

## A — ID

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Immutable primary key for the listing row. |
| **Type** | Plain text — UUID v4 recommended |
| **Validation** | Required; unique; never empty |
| **Editable by user** | Yes — set when adding a row |
| **Editable by automation** | No |
| **Example** | `a3f2c891-4b7e-4d2a-9c11-8e4f2a1b0d93` |

---

## B — STATUS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Pipeline stage. Controls which rows Make picks up. |
| **Type** | Dropdown (enum) |
| **Validation** | Required; exact match from allow list |
| **Editable by user** | Yes — approval, publish, and manual recovery |
| **Editable by automation** | Yes — forward transitions during processing |
| **Default for new rows** | `NEW` |

**Allowed values:**

```
NEW
PROCESSING
READY
ERROR
APPROVED
PUBLISHED
```

| Status | Meaning |
|--------|---------|
| `NEW` | Row waiting for Make to process |
| `PROCESSING` | Make picked up the row; backend call in progress |
| `READY` | Publication drafts written; ready for human review |
| `ERROR` | Processing failed; see `ERROR` column |
| `APPROVED` | Operator approved content for publishing |
| `PUBLISHED` | Content published manually (future automation) |

Apply **Data → Data validation → Dropdown (from a list)** on `B2:B` with the values above. Reject invalid input.

---

## C — SOURCE_URL

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Real estate listing URL sent to the backend. |
| **Type** | Plain text (URL) |
| **Validation** | Required; must start with `http://` or `https://` |
| **Editable by user** | Yes — before processing starts |
| **Editable by automation** | No |
| **Example** | `https://www.cian.ru/sale/flat/123456789/` |

---

## D — TITLE

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Publication headline from backend `publication.title`. |
| **Type** | Plain text |
| **Editable by user** | Yes — edit during review |
| **Editable by automation** | Yes — set when `STATUS` = `READY` |
| **Example** | `2-комн. квартира в центре Мозыря` |

---

## E — TELEGRAM_TEXT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Ready-to-post Telegram draft. |
| **Type** | Long text — enable wrap text |
| **Editable by user** | Yes |
| **Editable by automation** | Yes — from `publication.telegram_text` |
| **Required from status** | `READY` |

---

## F — INSTAGRAM_TEXT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Ready-to-post Instagram caption. |
| **Type** | Long text — enable wrap text |
| **Editable by user** | Yes |
| **Editable by automation** | Yes — from `publication.instagram_text` |
| **Required from status** | `READY` |

---

## G — REELS_SCRIPT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Reels voiceover script with timestamps. |
| **Type** | Long text — enable wrap text |
| **Editable by user** | Yes |
| **Editable by automation** | Yes — from `publication.reels_script` |
| **Required from status** | `READY` |

---

## H — HASHTAGS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Hashtags from backend `publication.hashtags` array. |
| **Type** | Plain text |
| **Format** | Space-separated words without `#` prefix |
| **Editable by user** | Yes |
| **Editable by automation** | Yes |
| **Example** | `недвижимость мозырь pronnedvizh квартира` |

---

## I — ERROR

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Error message when processing fails. |
| **Type** | Plain text |
| **Editable by user** | Yes — clear before retry |
| **Editable by automation** | Yes — set when `STATUS` = `ERROR` |
| **Example** | `HTTP 502: Failed to fetch listing page` |

---

## J — CREATED_AT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Row creation timestamp. |
| **Type** | Date time (UTC) |
| **Format** | `YYYY-MM-DD HH:mm:ss` |
| **Editable by user** | Yes — set when adding a row |
| **Editable by automation** | No |
| **Example** | `2026-07-03 09:15:00` |

---

## K — UPDATED_AT

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Last modification timestamp. |
| **Type** | Date time (UTC) |
| **Format** | `YYYY-MM-DD HH:mm:ss` |
| **Editable by user** | Yes — set when adding a row |
| **Editable by automation** | Yes — refreshed on every write |
| **Example** | `2026-07-03 09:16:42` |

---

## Stage requirement matrix

| STATUS | Required columns |
|--------|------------------|
| **NEW** | ID, STATUS, SOURCE_URL, CREATED_AT, UPDATED_AT |
| **PROCESSING** | NEW minimum (set by automation) |
| **READY** | NEW + TITLE, TELEGRAM_TEXT, INSTAGRAM_TEXT, REELS_SCRIPT, HASHTAGS |
| **ERROR** | ID, STATUS, ERROR, UPDATED_AT |
| **APPROVED** | READY minimum + human review complete |
| **PUBLISHED** | APPROVED minimum |

---

## Sheet setup checklist

1. Import [`BUILD_4_SHEET_TEMPLATE.csv`](BUILD_4_SHEET_TEMPLATE.csv) into a new spreadsheet named **PRO Nedvizh Publications**.
2. Rename the tab to `INBOX` (or note your tab name for Make).
3. Freeze row 1.
4. Freeze columns A–B (`ID`, `STATUS`).
5. Enable text wrap on `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT`.
6. Apply STATUS dropdown on column B.
7. Share with Editor access for the Make automation account.

---

## Related documents

- [`BUILD_4_IMPORT_GUIDE.md`](../../automation/make/BUILD_4_IMPORT_GUIDE.md) — Make blueprint import
- [`BUILD_4_FIRST_RUN.md`](../../docs/BUILD_4_FIRST_RUN.md) — first test walkthrough
- [`BUILD_4_CHECKLIST.md`](../../docs/BUILD_4_CHECKLIST.md) — production checklist
