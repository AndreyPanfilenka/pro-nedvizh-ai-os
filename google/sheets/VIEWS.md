# VIEWS

Filtered views and visual cues for the **INBOX** tab in `PRO Nedvizh — Inbox`.

Google Sheets **Filter views** (Data → Filter views → Create new filter view) give operators role-specific queues without duplicating data. Each view below is a named filter configuration to create manually when importing this specification.

**Version:** 1.0  
**Tab:** `INBOX`  
**Related:** [MASTER_TABLE.md](./MASTER_TABLE.md) · [COLUMNS.md](./COLUMNS.md) · [VALIDATIONS.md](./VALIDATIONS.md)

---

## Default sheet behavior

When no filter view is active:

| Setting | Value |
|---------|-------|
| **Sort** | `CREATED_AT` (column X) — Z → A (newest first) |
| **Filter** | None — show all non-header rows |
| **Hidden columns** | None by default |

Operators switch between named filter views for daily work.

---

## Named filter views

Create each view via **Data → Filter views → Create new filter view**. Name the view exactly as listed.

### 1. All Active

| Property | Value |
|----------|-------|
| **Purpose** | Main working view — everything except archived listings. |
| **Filter** | `STATUS` (B) — **does not equal** `ARCHIVED` |
| **Sort** | `UPDATED_AT` (Y) — Z → A |
| **Suggested visible columns** | A–G, H–K, V, W, X, Y |
| **Audience** | All operators |

---

### 2. New Intake

| Property | Value |
|----------|-------|
| **Purpose** | URLs waiting to enter the fetch pipeline. |
| **Filter** | `STATUS` (B) **equals** `NEW` |
| **Sort** | `CREATED_AT` (X) — A → Z (oldest first — FIFO) |
| **Suggested visible columns** | A, B, C, D, X, Y |
| **Audience** | Intake operator, automation monitor |

---

### 3. In Progress

| Property | Value |
|----------|-------|
| **Purpose** | Rows actively processed by automation. |
| **Filter** | `STATUS` (B) **is one of** `FETCHING`, `FETCHED`, `READY_FOR_AI`, `AI_PROCESSING` |
| **Sort** | `UPDATED_AT` (Y) — A → Z (stale jobs surface first) |
| **Suggested visible columns** | A, B, C, D, E, X, Y |
| **Audience** | Pipeline monitor, on-call |

**Alert hint:** Rows with `UPDATED_AT` older than 15 minutes in `FETCHING` or `AI_PROCESSING` may indicate a stuck job.

---

### 4. Review Queue

| Property | Value |
|----------|-------|
| **Purpose** | Listings awaiting human QC and approval. |
| **Filter** | `STATUS` (B) **equals** `READY_FOR_REVIEW` |
| **Sort** | `QUALITY_SCORE` (V) — A → Z (lowest scores first) |
| **Suggested visible columns** | A, B, E, F, G, H, I, K, L, Q, R, S, T, U, V, Y |
| **Audience** | Content reviewer, editor |

**Secondary sort (manual):** After quality score, sort by `CREATED_AT` ascending for fairness.

---

### 5. Approved — Ready to Publish

| Property | Value |
|----------|-------|
| **Purpose** | QC-cleared listings ready for scheduling or outbound publish. |
| **Filter** | `STATUS` (B) **equals** `APPROVED` **AND** `PUBLISH_STATUS` (W) **is one of** `Ready`, `Scheduled` |
| **Sort** | `UPDATED_AT` (Y) — A → Z |
| **Suggested visible columns** | A, B, E, H, K, L, Q, S, T, U, V, W, Y |
| **Audience** | Publishing operator |

---

### 6. Publishing — Live & Partial

| Property | Value |
|----------|-------|
| **Purpose** | Track channel rollout and partial publish state. |
| **Filter** | `STATUS` (B) **equals** `PUBLISHED` **OR** (`STATUS` **equals** `APPROVED` **AND** `PUBLISH_STATUS` **is one of** `Partially Published`, `Failed`) |
| **Sort** | `UPDATED_AT` (Y) — Z → A |
| **Suggested visible columns** | A, B, E, W, S, T, U, Y |
| **Audience** | Social operator, publishing automation monitor |

---

### 7. Failed Publish

| Property | Value |
|----------|-------|
| **Purpose** | Publish errors requiring retry or manual fix. |
| **Filter** | `PUBLISH_STATUS` (W) **equals** `Failed` |
| **Sort** | `UPDATED_AT` (Y) — Z → A |
| **Suggested visible columns** | A, B, D, E, W, S, T, U, Y |
| **Audience** | Publishing operator, on-call |

---

### 8. Archive

| Property | Value |
|----------|-------|
| **Purpose** | Historical and rejected listings. |
| **Filter** | `STATUS` (B) **equals** `ARCHIVED` |
| **Sort** | `UPDATED_AT` (Y) — Z → A |
| **Suggested visible columns** | A, B, C, D, E, X, Y |
| **Audience** | Admin, audit |

---

## Slice views (optional filters)

Apply these as additional filter views or temporary filters on top of the views above.

### By city

| View name | Filter |
|-----------|--------|
| **Moscow** | `CITY` (H) **equals** `Moscow` |
| **Saint Petersburg** | `CITY` (H) **equals** `Saint Petersburg` |

Extend with one view per primary market city as volume grows.

### By property type

| View name | Filter |
|-----------|--------|
| **Apartments only** | `PROPERTY_TYPE` (F) **equals** `Apartment` |
| **Commercial only** | `PROPERTY_TYPE` (F) **equals** `Commercial` |

### By deal type

| View name | Filter |
|-----------|--------|
| **For Sale** | `DEAL_TYPE` (G) **equals** `Sale` |
| **For Rent** | `DEAL_TYPE` (G) **equals** `Rent` |

### By source

| View name | Filter |
|-----------|--------|
| **Cian listings** | `SOURCE` (C) **equals** `Cian` |
| **Avito listings** | `SOURCE` (C) **equals** `Avito` |

---

## Conditional formatting

Apply via **Format → Conditional formatting** on the `INBOX` tab.

### STATUS column (B)

| Condition | Format |
|-----------|--------|
| Text is exactly `NEW` | Background `#fff3cd` (yellow) |
| Text is exactly `FETCHING` | Background `#fff3cd` (yellow) |
| Text is exactly `FETCHED` | Background `#cce5ff` (blue) |
| Text is exactly `READY_FOR_AI` | Background `#cce5ff` (blue) |
| Text is exactly `AI_PROCESSING` | Background `#cce5ff` (blue) |
| Text is exactly `READY_FOR_REVIEW` | Background `#f8d7da` (red tint — action needed) |
| Text is exactly `APPROVED` | Background `#d4edda` (green) |
| Text is exactly `PUBLISHED` | Background `#d1ecf1` (teal) |
| Text is exactly `ARCHIVED` | Background `#e2e3e5` (gray) |

### PUBLISH_STATUS column (W)

| Condition | Format |
|-----------|--------|
| Text is exactly `Failed` | Background `#f8d7da` |
| Text is exactly `Published` | Background `#d4edda` |
| Text is exactly `Scheduled` | Background `#fff3cd` |
| Text is exactly `Partially Published` | Background `#d1ecf1` |

### QUALITY_SCORE column (V)

| Condition | Format |
|-----------|--------|
| Number is less than `70` | Text color `#856404`, bold |
| Number is greater than or equal to `70` | Text color `#155724` |

Only applies meaningfully when `STATUS` is `READY_FOR_REVIEW` or later.

### Stale job highlight (optional)

| Range | Custom formula | Format |
|-------|----------------|--------|
| Entire row (A2:Y) | `=AND($B2="FETCHING", $Y2<NOW()-TIME(0,15,0))` | Background `#f8d7da` |
| Entire row (A2:Y) | `=AND($B2="AI_PROCESSING", $Y2<NOW()-TIME(0,15,0))` | Background `#f8d7da` |

Highlights rows stuck in processing for more than 15 minutes.

---

## Column visibility by role

Recommended column sets when a role uses a dedicated filter view:

| Role | Show | Hide (reduce noise) |
|------|------|---------------------|
| **Intake** | A–D, X, Y | R–U, V, W |
| **Reviewer** | A–B, E–Q, R–V | — |
| **Publisher** | A–B, E, H, K–L, Q, S–W, Y | M–P |
| **Monitor** | A–B, C, D, X, Y | R–U |

Hide columns via the filter view's column hide controls; do not delete columns.

---

## View creation checklist

When importing this specification into Google Sheets:

- [ ] Create filter view **All Active**
- [ ] Create filter view **New Intake**
- [ ] Create filter view **In Progress**
- [ ] Create filter view **Review Queue**
- [ ] Create filter view **Approved — Ready to Publish**
- [ ] Create filter view **Publishing — Live & Partial**
- [ ] Create filter view **Failed Publish**
- [ ] Create filter view **Archive**
- [ ] Apply STATUS conditional formatting on column B
- [ ] Apply PUBLISH_STATUS conditional formatting on column W
- [ ] Apply QUALITY_SCORE conditional formatting on column V
- [ ] (Optional) Apply stale-job row highlighting
- [ ] Freeze row 1 and columns A–B

---

## Related documents

- [MASTER_TABLE.md](./MASTER_TABLE.md) — spreadsheet layout and column order
- [VALIDATIONS.md](./VALIDATIONS.md) — dropdown values used in filters
- [Status flow](../../docs/status-flow.md) — pipeline stages referenced by views
