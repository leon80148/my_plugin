# Report Structure

## Single Output Record
```json
{
  "model": "chd",
  "status": 0,
  "risk": 20.02,
  "populationAvg": 10.30,
  "multipleDiff": 194.37,
  "riskType": 2,
  "version": 4,
  "band": "high",
  "summary": "High risk level. Recommend clinician review and follow-up planning."
}
```

## Multi-Model Report
```json
{
  "title": "NHRI Risk Summary",
  "generatedAt": "2026-02-16T08:00:00Z",
  "models": [ ...single records... ],
  "overall": {
    "highestBand": "high",
    "highCount": 2,
    "elevatedCount": 1,
    "lowerCount": 2
  }
}
```

## Model Names
Allowed model keys:
- `chd`
- `stroke`
- `hypertension`
- `diabetes`
- `mace`
