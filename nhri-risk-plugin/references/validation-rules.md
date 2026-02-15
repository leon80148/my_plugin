# NHRI V4 Validation Rules

`age > 0` is mandatory for all models.

## CHD
- Required for both branches: `hdlc > 0`, `waist > 0`
- Female branch (`gender != 1`) requires additional: `sbp > 0`, `chol > 0`, `tg > 0`

## Stroke
- Required for both branches: `sbp > 0`
- Male branch (`gender == 1`) requires additional: `glu > 0`, `tg > 0`
- Female branch (`gender != 1`) requires additional: `waist > 0`

## Hypertension
- Required for both branches: `sbp > 0`
- Also require one of:
  - `bmi > 0`, or
  - both `height > 0` and `weight > 0`
- Male branch (`gender == 1`) requires additional: `hdlc > 0`, `ldlc > 0`
- Female branch (`gender != 1`) requires additional: `tg > 0`, `glu > 0`

## Diabetes
- Required for both branches: `glu > 0`, `tg > 0`
- Also require one of:
  - `bmi > 0`, or
  - both `height > 0` and `weight > 0`
- Male branch (`gender == 1`) requires additional: `chol > 0`
- Female branch (`gender != 1`) requires additional: `waist > 0`, `hdlc > 0`

## MACE
- Required for both branches: `sbp > 0`, `hdlc > 0`, `waist > 0`
- Female branch (`gender != 1`) requires additional: `chol > 0`

## Notes
- Legacy Java validation updates error text but does not stop at first failure.
- For compatibility, keep field thresholds strict (`> 0`, not `>= 0`).
