# Google Sheets Import Guide — Release 0.5

Production import for the PRO Nedvizh master table.

## Spreadsheet setup

1. Create a Google Spreadsheet named **PRO Nedvizh Database**.
2. Rename the first tab to `INBOX` (or your chosen name — must match `SHEET_NAME` in Make).
3. Import [`MASTER_TABLE_FINAL.csv`](MASTER_TABLE_FINAL.csv):
   - **File → Import → Upload**
   - Import location: **Replace current sheet**
   - Separator: **Comma**
   - Convert text to numbers/dates: **No**
4. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
5. Freeze row 1.
6. Freeze columns A–B (`ID`, `STATUS`).
7. Enable text wrap on columns `DESCRIPTION_AI`, `TELEGRAM_TEXT`, `INSTAGRAM_TEXT`, `REELS_SCRIPT`.

## Column layout (24 columns, A–X)

| Col | Header | Purpose |
|:---:|--------|---------|
| A | ID | UUID primary key |
| B | STATUS | Pipeline stage |
| C | SOURCE_URL | Intake listing URL |
| D | SOURCE | Platform (filled by automation) |
| E | TITLE | Listing headline |
| F | PROPERTY_TYPE | apartment, room, house, etc. |
| G | DEAL_TYPE | sale, rent, daily_rent |
| H | CITY | City name |
| I | DISTRICT | District |
| J | ADDRESS | Street address |
| K | PRICE | Numeric price |
| L | CURRENCY | ISO 4217 code |
| M | ROOMS | Room count (0 = studio) |
| N | AREA_TOTAL | Total area m² |
| O | FLOOR | Floor number |
| P | PHOTOS | Comma-separated photo URLs |
| Q | DESCRIPTION_AI | AI property description |
| R | TELEGRAM_TEXT | Telegram post draft |
| S | INSTAGRAM_TEXT | Instagram caption draft |
| T | REELS_SCRIPT | Reels script draft |
| U | QUALITY_SCORE | 0–100 completeness score |
| V | ERROR | Error message (automation only) |
| W | CREATED_AT | Row creation timestamp (UTC) |
| X | UPDATED_AT | Last update timestamp (UTC) |

## STATUS dropdown (column B)

Apply **Data → Data validation → Dropdown (from a list)** on `B2:B`:

```
NEW
PROCESSING
AI_DONE
READY_FOR_REVIEW
ERROR
APPROVED
PUBLISHED
```

Reject invalid input.

## Adding a listing

1. Generate a UUID for `ID`.
2. Set `STATUS` = `NEW`.
3. Paste the listing URL into `SOURCE_URL`.
4. Set `CREATED_AT` and `UPDATED_AT` (format: `YYYY-MM-DD HH:mm:ss`, UTC).
5. Leave all other columns empty — automation fills them.

## After automation

When the pipeline completes successfully:

- `STATUS` = `AI_DONE`
- Property fields, `QUALITY_SCORE`, and content drafts populated
- Row is ready for human review and Telegram/Instagram publishing stage

## Permissions

| Role | Access |
|------|--------|
| Make automation account | Editor |
| Operators | Editor |
| Reviewers | Commenter or Editor |

Share the spreadsheet only with required accounts.
