# Validation Matrix

## Global Rule
- `age > 0` is required for every model.

## CHD
- Base required: `hdlc > 0`, `waist > 0`
- Female branch (`gender != 1`) also requires: `sbp > 0`, `chol > 0`, `tg > 0`

## Stroke
- Base required: `sbp > 0`
- Male branch (`gender == 1`) also requires: `glu > 0`, `tg > 0`
- Female branch (`gender != 1`) also requires: `waist > 0`

## Hypertension
- Base required: `sbp > 0`
- Body composition rule: `bmi > 0` OR (`height > 0` AND `weight > 0`)
- Male branch (`gender == 1`) also requires: `hdlc > 0`, `ldlc > 0`
- Female branch (`gender != 1`) also requires: `tg > 0`, `glu > 0`

## Diabetes
- Base required: `glu > 0`, `tg > 0`
- Body composition rule: `bmi > 0` OR (`height > 0` AND `weight > 0`)
- Male branch (`gender == 1`) also requires: `chol > 0`
- Female branch (`gender != 1`) also requires: `waist > 0`, `hdlc > 0`

## MACE
- Base required: `sbp > 0`, `hdlc > 0`, `waist > 0`
- Female branch (`gender != 1`) also requires: `chol > 0`
