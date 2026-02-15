# Interpretation Rules

## Status
- `status == 1`: invalid input or failed evaluation.
- `status == 0`: valid result.

## Risk Band Mapping

### CHD / Stroke / Diabetes / MACE
- `risk >= 20`: `high`
- `10 <= risk < 20`: `elevated`
- `risk < 10`: `lower`

### Hypertension
- `multipleDiff > 1.25`: `high`
- `0.75 <= multipleDiff <= 1.25`: `elevated`
- `multipleDiff < 0.75`: `lower`

## Narrative Guidance
- `high`: advise clinician review and short-interval follow-up.
- `elevated`: advise targeted lifestyle/biomarker management and routine follow-up.
- `lower`: advise ongoing monitoring and preventive care continuity.

## Output Consistency
Use the same terminology in all render targets (`high`, `elevated`, `lower`).
