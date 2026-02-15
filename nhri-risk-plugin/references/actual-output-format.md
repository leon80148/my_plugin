# Actual Output Format

## Expected Vector File (`--expected`)

`generate_vectors.py` writes a list of records:

```json
[
  {
    "id": "chd-male-001",
    "model": "chd",
    "input": {"gender": 1, "age": 52, "...": 0},
    "expected": {
      "status": 0,
      "risk": 12.34,
      "populationAvg": 5.67,
      "multipleDiff": 2.18,
      "riskType": 1,
      "version": 4,
      "error": "",
      "message": ""
    }
  }
]
```

## Actual File (`--actual`)

Use the same `id` and place implementation result in one of these keys:
- `output`
- `actual`
- `result`
- `expected`

Example:

```json
[
  {
    "id": "chd-male-001",
    "output": {
      "status": 0,
      "risk": 12.34,
      "populationAvg": 5.67,
      "multipleDiff": 2.18,
      "riskType": 1,
      "version": 4,
      "error": "",
      "message": ""
    }
  }
]
```

`compare_outputs.py` matches by `id`.
