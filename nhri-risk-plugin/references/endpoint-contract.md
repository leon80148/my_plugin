# Endpoint Contract

## POST /risk/evaluate
Evaluate one model.

### Request
```json
{
  "model": "chd",
  "input": {
    "gender": 1,
    "age": 52,
    "sbp": 130,
    "tg": 120,
    "chol": 195,
    "hdlc": 48,
    "ldlc": 118,
    "glu": 97,
    "bmi": 0,
    "height": 170,
    "weight": 68,
    "waist": 86,
    "hbp": 1,
    "diabetes": 0,
    "smoke": 0
  }
}
```

### Success Response (200)
```json
{
  "status": 0,
  "error": "",
  "message": "",
  "risk": 20.02,
  "populationAvg": 10.3,
  "multipleDiff": 194.37,
  "riskType": 2,
  "version": 4
}
```

### Validation Error (422 or 400)
```json
{
  "status": 1,
  "error": "sbp must be > 0",
  "message": "",
  "risk": 0,
  "populationAvg": 0,
  "multipleDiff": 0,
  "riskType": 0,
  "version": 0
}
```

## POST /risk/evaluate-all
Evaluate all models for one input.

### Request
```json
{
  "input": { "gender": 0, "age": 58, "...": 0 }
}
```

### Response
```json
{
  "chd": { "status": 0, "risk": 17.21, "...": 0 },
  "stroke": { "status": 0, "risk": 18.38, "...": 0 },
  "hypertension": { "status": 0, "risk": 74.58, "...": 0 },
  "diabetes": { "status": 0, "risk": 40.1, "...": 0 },
  "mace": { "status": 0, "risk": 22.12, "...": 0 }
}
```
