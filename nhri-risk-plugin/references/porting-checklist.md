# Porting Checklist

Use this checklist when moving NHRI V4 logic to another language.

1. Preserve branch rule: `gender == 1` is male, everything else is female.
2. Preserve validation thresholds as strict `> 0` checks.
3. Preserve Java-style rounding (not bankers rounding).
4. Preserve computation order:
- validate
- set version
- optional BMI derive
- compute risk
- compute population average
- compute multiple difference
- compute risk type
5. Preserve age window for population average: `35..70` inclusive.
6. Preserve risk type thresholds exactly.
7. Keep output field names unchanged.
8. Run regression vectors before release.

## Common Drift Risks
- Using language-native `round()` and getting different tie behavior.
- Using female branch for `gender=0` only and forgetting non-1 values.
- Applying population average outside 35-70.
- Reordering calculations and changing floating-point behavior.
