# Evaluator Algorithm

## 1. Normalize Input
- Parse numeric fields to `float` or `int`.
- Treat missing values as `0`.
- Use male branch only when `gender == 1`; otherwise female branch.

## 2. Validate Model Inputs
- Apply model-specific required fields from the spec.
- If one or more requirements fail, set `status=1` and return immediately.

## 3. Set Version
- Set output `version=4` only after validation passes.

## 4. Compute BMI If Needed
- For Hypertension/Diabetes, if `bmi <= 0` and `height > 0` and `weight > 0`, compute BMI.

## 5. Compute Z and Risk
- Choose `(Z, S0)` from model + gender branch.
- Compute risk probability: `1 - S0^(exp(Z))`.
- Convert to percent with Java-compatible 2-decimal rounding.

## 6. Compute Population Average
- If `35 <= age <= 70`, use corresponding `avgArray[age-35]`.
- Convert to percent with the same rounding.
- Otherwise `populationAvg = 0`.

## 7. Compute Multiple Difference
- If `populationAvg > 0`: `multipleDiff = round((risk/populationAvg)*100)/100`.
- Else `multipleDiff = 0`.

## 8. Risk Type
- CHD/Stroke/Diabetes/MACE: `risk >= 20 => 2`, `risk >= 10 => 1`.
- Hypertension: `multipleDiff > 1.25 => 2`, `multipleDiff >= 0.75 => 1`.

## 9. Output
- Return full output object with all fields.
