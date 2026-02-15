# NHRI V4 Formulas

All calculations below were extracted from `RiskV4Helper.class`.

## Common

- `risk(%) = round((1 - S0^(exp(Z))) * 10000) / 100`
- `populationAvg(%) = round(avgArray[age-35] * 10000) / 100`, only when `35 <= age <= 70`
- `multipleDiff = round((risk / populationAvg) * 100) / 100`, only when `populationAvg > 0`
- Java-style rounding is required to match legacy outputs.

## CHD

Male (`gender == 1`):
- `Z = 8.3077*(log10(age)-1.7056) + 0.6715*(hbp-0.3485) + 0.0163*(waist-82.0694) - 0.0081*(hdlc-53.06)`
- `S0 = 0.8936`

Female:
- `Z = 9.3891*(log10(age)-1.6886) + 0.0425*(waist-76.36177) + 0.0015*(sbp-123.379) + 0.3581*((chol/hdlc)-3.5753) + 0.0001*(tg-107.9153)`
- `S0 = 0.9405`

## Stroke

Male (`gender == 1`):
- `Z = 8.9714*(log10(age)-1.7093) + 0.0238*(sbp-128.6824) + 0.0046*(glu-100.2177) + 0.0017*(tg-127.9926)`
- `S0 = 0.87`

Female:
- `Z = 5.1186*(log10(age)-1.6963) + 0.7794*(smoke-0.0522) + 0.023*(waist-77.1681) + 0.4908*(hbp-0.342) + 0.581*(diabetes-0.0914) + 0.0139*(sbp-126.0013)`
- `S0 = 0.91`

## Hypertension

Male (`gender == 1`):
- `Z = 6.6698*(log10(age)-1.6973) + 0.0224*(sbp-117.5462) + 0.0368*(bmi-23.1587) - 0.0113*(hdlc-53.37) + 0.0008*(ldlc-116.9147)`
- `S0 = 0.65`

Female:
- `Z = 4.1239*(log10(age)-1.6789) + 0.0647*(bmi-24.0371) + 0.3866*(smoke-0.051) + 0.0313*(sbp-115.6778) + 0.0024*(tg-105.1218) + 0.003*(glu-96.3894)`
- `S0 = 0.6`

## Diabetes

Male (`gender == 1`):
- `Z = 4.3665*(log10(age)-1.7126) + 0.1281*(bmi-23.8756) + 0.0332*(glu-94.1031) + 0.002*(chol-196.9184) + 0.0024*(tg-127.0042)`
- `S0 = 0.79`

Female:
- `Z = 2.8928*(log10(age)-1.6939) + 0.0723*(bmi-24.6413) + 0.0195*(waist-76.6563) + 0.0334*(glu-95.0456) + 0.0016*(tg-111.8046) - 0.009*(hdlc-59.737)`
- `S0 = 0.76`

## MACE

Male (`gender == 1`):
- `Z = 7.3146*(log10(age)-1.7056) + 0.0114*(waist-82.0694) + 0.027*(sbp-127.0251) - 0.0045*(hdlc-53.06)`
- `S0 = 0.82`

Female:
- `Z = 6.8833*(log10(age)-1.6886) + 0.1923*(smoke-0.0462) + 0.0257*(waist-76.3618) + 0.0128*(sbp-123.379) + 0.3054*((chol/hdlc)-3.5753)`
- `S0 = 0.9036`

## BMI

If BMI is required and not provided:
- `BMI = round((weight / (height/100)^2) * 100) / 100`
