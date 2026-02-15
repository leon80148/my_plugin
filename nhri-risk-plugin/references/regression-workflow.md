# Regression Workflow

## Goal
Detect behavior drift when NHRI V4 logic is moved to another stack.

## Recommended Steps
1. Generate vectors from the reference evaluator.
2. Execute vectors in the target implementation.
3. Compare expected vs actual.
4. Fail CI on any mismatch.

## Coverage Guidance
- Use both genders for all 5 models.
- Include age around baseline boundaries (`34, 35, 70, 71`).
- Include cases with provided BMI and derived BMI.
- Include high and low ranges for SBP, TG, GLU, HDL-C, LDL-C.

## Acceptance Rule
- `status`, `riskType`, `version`: exact match.
- `risk`, `populationAvg`, `multipleDiff`: compare within small tolerance (default `1e-9`).

## CI Recommendation
Run `generate_vectors.py` only when baseline changes. In normal CI, keep vectors committed and run only `compare_outputs.py`.
