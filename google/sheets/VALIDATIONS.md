# VALIDATIONS

Data validation rules for the **INBOX** tab in `PRO Nedvizh — Inbox`.

Apply via **Data → Data validation** in Google Sheets. All dropdowns use **Dropdown (from a list)** with **Reject input** for invalid entries unless noted otherwise.

**Version:** 1.0  
**Tab:** `INBOX`  
**Related:** [MASTER_TABLE.md](./MASTER_TABLE.md) · [COLUMNS.md](./COLUMNS.md)

---

## How to apply

| Step | Action |
|------|--------|
| 1 | Select the target column from row 2 downward (or entire column excluding header) |
| 2 | **Data → Data validation** |
| 3 | Criteria: **Dropdown (from a list)** or **Number** / **Text** as specified |
| 4 | On invalid data: **Reject input** (dropdowns and numeric ranges) |
| 5 | Show validation help text where noted below |

Repeat for each rule below. Range notation assumes data starts at row 2 and headers are in row 1.

---

## Dropdown validations

### STATUS

| Property | Value |
|----------|-------|
| **Column** | B |
| **Range** | `INBOX!B2:B` |
| **Type** | Dropdown (from a list) |
| **Reject invalid** | Yes |
| **Help text** | Pipeline stage. See status-flow documentation for allowed transitions. |

**Allow list (exact match, one value per line):**

```
NEW
FETCHING
FETCHED
READY_FOR_AI
AI_PROCESSING
READY_FOR_REVIEW
APPROVED
PUBLISHED
ARCHIVED
```

| Value | Meaning |
|-------|---------|
| **NEW** | Record created; URL accepted; awaiting fetch |
| **FETCHING** | Source page and media retrieval in progress |
| **FETCHED** | Raw listing data extracted into the row |
| **READY_FOR_AI** | Structured record complete; queued for AI content |
| **AI_PROCESSING** | Description and channel drafts being generated |
| **READY_FOR_REVIEW** | AI outputs present; awaiting human QC |
| **APPROVED** | QC passed; cleared for publishing |
| **PUBLISHED** | Content released to at least one target channel |
| **ARCHIVED** | Inactive — failed, rejected, cancelled, or closed |

---

### SOURCE

| Property | Value |
|----------|-------|
| **Column** | C |
| **Range** | `INBOX!C2:C` |
| **Type** | Dropdown (from a list) |
| **Reject invalid** | Yes |
| **Required when** | `STATUS` is `FETCHED` or later |
| **Help text** | Listing platform detected after fetch. |

**Allow list:**

```
Cian
Avito
Yandex Realty
Domclick
Custom Site
Unknown
Manual
```

| Value | Meaning |
|-------|---------|
| **Cian** | cian.ru family |
| **Avito** | avito.ru family |
| **Yandex Realty** | realty.yandex.ru family |
| **Domclick** | domclick.ru family |
| **Custom Site** | Other known site with dedicated extractor |
| **Unknown** | Detection failed; manual handling |
| **Manual** | Row created without automated fetch |

---

### PROPERTY_TYPE

| Property | Value |
|----------|-------|
| **Column** | F |
| **Range** | `INBOX!F2:F` |
| **Type** | Dropdown (from a list) |
| **Reject invalid** | Yes |
| **Required when** | `STATUS` is `FETCHED` or later |
| **Help text** | Category of real estate object. |

**Allow list:**

```
Apartment
House
Commercial
Garage
Land
```

| Value | Meaning |
|-------|---------|
| **Apartment** | Flat / apartment unit |
| **House** | Detached or semi-detached house, cottage, townhouse |
| **Commercial** | Office, retail, warehouse, other commercial space |
| **Garage** | Garage, parking box, car place |
| **Land** | Land plot |

---

### DEAL_TYPE

| Property | Value |
|----------|-------|
| **Column** | G |
| **Range** | `INBOX!G2:G` |
| **Type** | Dropdown (from a list) |
| **Reject invalid** | Yes |
| **Required when** | `STATUS` is `FETCHED` or later |
| **Help text** | Sale or rent. |

**Allow list:**

```
Sale
Rent
```

| Value | Meaning |
|-------|---------|
| **Sale** | Purchase offer |
| **Rent** | Long-term rental offer |

---

### CURRENCY

| Property | Value |
|----------|-------|
| **Column** | L |
| **Range** | `INBOX!L2:L` |
| **Type** | Dropdown (from a list) |
| **Reject invalid** | Yes |
| **Required when** | `PRICE` (column K) is not empty |
| **Help text** | ISO 4217 code for price. Default RUB for Russian listings. |

**Allow list:**

```
RUB
USD
EUR
```

| Value | Meaning |
|-------|---------|
| **RUB** | Russian ruble |
| **USD** | US dollar |
| **EUR** | Euro |

---

### PUBLISH_STATUS

| Property | Value |
|----------|-------|
| **Column** | W |
| **Range** | `INBOX!W2:W` |
| **Type** | Dropdown (from a list) |
| **Reject invalid** | Yes |
| **Required when** | `STATUS` is `APPROVED` or `PUBLISHED` |
| **Help text** | Channel distribution state. Separate from pipeline STATUS. |

**Allow list:**

```
Not Ready
Ready
Scheduled
Partially Published
Published
Failed
```

| Value | Meaning |
|-------|---------|
| **Not Ready** | Approved but not yet cleared for outbound publish |
| **Ready** | Cleared to publish; awaiting operator or schedule |
| **Scheduled** | Publish slot assigned on calendar |
| **Partially Published** | Live on one or more but not all target channels |
| **Published** | Live on all target channels for this listing |
| **Failed** | Publish attempt failed; requires retry or manual fix |

**Alignment with pipeline STATUS:**

| Pipeline STATUS | Typical PUBLISH_STATUS |
|-----------------|------------------------|
| Before APPROVED | Empty or `Not Ready` |
| APPROVED | `Ready` or `Scheduled` |
| PUBLISHED | `Partially Published` or `Published` |

---

## Non-dropdown validations

### SOURCE_URL

| Property | Value |
|----------|-------|
| **Column** | D |
| **Range** | `INBOX!D2:D` |
| **Type** | Custom formula |
| **Criteria** | `=AND(LEN(D2)>0, LEN(D2)<=2048, OR(LEFT(D2,7)="http://", LEFT(D2,8)="https://"))` |
| **Reject invalid** | Yes |
| **Help text** | Valid HTTP or HTTPS URL, max 2048 characters. |

---

### MAIN_PHOTO

| Property | Value |
|----------|-------|
| **Column** | Q |
| **Range** | `INBOX!Q2:Q` |
| **Type** | Custom formula (when not empty) |
| **Criteria** | `=OR(Q2="", LEFT(Q2,7)="http://", LEFT(Q2,8)="https://")` |
| **Reject invalid** | Yes |
| **Help text** | Empty or valid image URL. |

---

### PRICE

| Property | Value |
|----------|-------|
| **Column** | K |
| **Range** | `INBOX!K2:K` |
| **Type** | Number |
| **Criteria** | Greater than or equal to `0` |
| **Reject invalid** | Yes |

---

### ROOMS

| Property | Value |
|----------|-------|
| **Column** | M |
| **Range** | `INBOX!M2:M` |
| **Type** | Number |
| **Criteria** | Greater than or equal to `0` |
| **Reject invalid** | Yes |
| **Note** | Whole numbers only; use **Format → Number → Number** with 0 decimal places |

---

### AREA

| Property | Value |
|----------|-------|
| **Column** | N |
| **Range** | `INBOX!N2:N` |
| **Type** | Number |
| **Criteria** | Greater than `0` (when cell is not empty) |
| **Reject invalid** | Yes |
| **Note** | Optional for `Land` and `Garage`; required for `Apartment` and `House` at `READY_FOR_AI` |

---

### FLOOR

| Property | Value |
|----------|-------|
| **Column** | O |
| **Range** | `INBOX!O2:O` |
| **Type** | Number |
| **Criteria** | Between `-5` and `200` (inclusive) when not empty |
| **Reject invalid** | Yes |
| **Note** | Negative values allowed for basement levels |

---

### PHOTO_COUNT

| Property | Value |
|----------|-------|
| **Column** | P |
| **Range** | `INBOX!P2:P` |
| **Type** | Number |
| **Criteria** | Greater than or equal to `0` |
| **Reject invalid** | Yes |
| **Note** | Integer; automation-owned field |

---

### QUALITY_SCORE

| Property | Value |
|----------|-------|
| **Column** | V |
| **Range** | `INBOX!V2:V` |
| **Type** | Number |
| **Criteria** | Between `0` and `100` (inclusive) |
| **Reject invalid** | Yes |
| **Help text** | QC score 0–100. Approval threshold default: 70. |

---

### CREATED_AT / UPDATED_AT

| Property | Value |
|----------|-------|
| **Columns** | X, Y |
| **Range** | `INBOX!X2:Y` |
| **Type** | Date |
| **Criteria** | Valid date |
| **Reject invalid** | Yes |
| **Display format** | `yyyy-mm-dd hh:mm:ss` |
| **Note** | Store and display in UTC; document timezone in sheet note |

**Cross-field rule (documented, not enforced by Sheets natively):**

- `UPDATED_AT` must be ≥ `CREATED_AT` on every row.

---

## Plain text length guidance

Google Sheets does not enforce max length natively. Apply these limits during intake, automation, and QC:

| Column | Max length |
|--------|------------|
| ID | 36 |
| SOURCE_URL | 2048 |
| TITLE | 500 |
| CITY, DISTRICT | 200 each |
| ADDRESS | 500 |
| DESCRIPTION_AI, TELEGRAM, INSTAGRAM, REELS | 50000 (practical cell limit) |

---

## Validation summary table

| Column | Header | Validation type | Rule |
|:------:|--------|-----------------|------|
| B | STATUS | Dropdown | 9 pipeline statuses |
| C | SOURCE | Dropdown | 7 platform values |
| D | SOURCE_URL | Custom formula | HTTP(S) URL, 1–2048 chars |
| F | PROPERTY_TYPE | Dropdown | 5 property types |
| G | DEAL_TYPE | Dropdown | Sale, Rent |
| K | PRICE | Number | ≥ 0 |
| L | CURRENCY | Dropdown | RUB, USD, EUR |
| M | ROOMS | Number | ≥ 0, integer |
| N | AREA | Number | > 0 when set |
| O | FLOOR | Number | −5 to 200 when set |
| P | PHOTO_COUNT | Number | ≥ 0, integer |
| Q | MAIN_PHOTO | Custom formula | Empty or HTTP(S) URL |
| V | QUALITY_SCORE | Number | 0–100 |
| W | PUBLISH_STATUS | Dropdown | 6 publish states |
| X, Y | CREATED_AT, UPDATED_AT | Date | Valid datetime |

Columns E, H, I, J, R, S, T, U have no dropdown or numeric range validation; enforce completeness via stage rules in [COLUMNS.md](./COLUMNS.md#stage-requirement-matrix).

---

## Related documents

- [MASTER_TABLE.md](./MASTER_TABLE.md) — column summary and protected ranges
- [COLUMNS.md](./COLUMNS.md) — per-column examples and stage requirements
- [VIEWS.md](./VIEWS.md) — filtered views using these fields
- [Status flow](../../docs/status-flow.md) — transition rules for STATUS
