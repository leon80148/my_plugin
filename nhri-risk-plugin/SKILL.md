---
name: nhri-risk-plugin
description: 國衛院 NHRI V4 健康風險評估系統。涵蓋 CHD、中風、高血壓、糖尿病、MACE 五大疾病風險模型的公式規格、輸入驗證、風險計算、迴歸測試、API 適配器產生、報告渲染。
---

# NHRI Risk Plugin

## Overview

Use this skill for all NHRI V4 risk assessment workflows: formula lookup, input validation, risk evaluation, regression testing, API adapter scaffolding, and report rendering.

## When to Use

- Auditing NHRI V4 coefficients or formula logic
- Validating risk model input payloads
- Computing CHD / Stroke / Hypertension / Diabetes / MACE risk scores
- Generating golden regression vectors for cross-platform parity
- Scaffolding FastAPI / Express / Spring API wrappers
- Rendering risk evaluation results into reports

## Context Control

1. Read `references/routing-table.md` first to identify the relevant reference.
2. Load only one domain reference per task.
3. Prefer running scripts over loading large docs.
4. Open additional references only if output is insufficient.
5. See `references/context-budget.md` for the full loading policy.

## Routing by Intent

| Intent | Reference | Script |
|---|---|---|
| Formula audit, coefficients | `references/formulas.md` | `run_module.py --module spec-popavg` |
| Input validation | `references/validation-matrix.md` | `run_module.py --module validate` |
| Risk evaluation | `references/evaluator-algorithm.md` | `run_module.py --module evaluate` |
| Regression testing | `references/regression-workflow.md` | `run_module.py --module regress-generate` |
| API adapter scaffold | `references/endpoint-contract.md` | `run_module.py --module api-scaffold` |
| Report rendering | `references/report-structure.md` | `run_module.py --module report` |

## Model Rules (V4)

- Models: `chd`, `stroke`, `hypertension`, `diabetes`, `mace`
- Gender routing: `gender == 1` → male branch; else → female branch
- Rounding: Java-style `round(value * 10000) / 100` for risk percentages
- Age range for population averages: 35-70 (index = `age - 35`); outside range → 0
- Risk type thresholds:
  - CHD/Stroke/Diabetes/MACE: `risk >= 20` → type 2, `risk >= 10` → type 1
  - Hypertension: `multipleDiff > 1.25` → type 2, `multipleDiff >= 0.75` → type 1

## CLI Entrypoint

All scripts are invoked via `scripts/run_module.py`:

```bash
# Evaluate all models
python scripts/run_module.py --module evaluate -- --json "{...}" --pretty

# Validate one model
python scripts/run_module.py --module validate -- --model chd --json "{...}" --pretty

# Population average lookup
python scripts/run_module.py --module spec-popavg -- --model chd --gender male --age 52

# Generate regression vectors
python scripts/run_module.py --module regress-generate -- --per-group 10 --output assets/golden-vectors.sample.json

# Compare regression outputs
python scripts/run_module.py --module regress-compare -- --expected <vectors.json> --actual <actual.json>

# Scaffold API adapter
python scripts/run_module.py --module api-scaffold -- --platform fastapi --output adapters/fastapi

# Render report
python scripts/run_module.py --module report -- --input <result.json> --format markdown
```

## References

| File | Description |
|---|---|
| `references/routing-table.md` | Intent-to-reference routing map |
| `references/context-budget.md` | Low-token loading policy |
| `references/quickstart.md` | Common command patterns |
| `references/formulas.md` | Full equations and coefficients |
| `references/input-output-contract.json` | Canonical I/O contract |
| `references/population-averages.json` | Age-indexed baseline arrays (35-70) |
| `references/validation-rules.md` | Input validation matrix by model |
| `references/validation-matrix.md` | Required fields by model and branch |
| `references/error-codes.json` | Stable validation error codes |
| `references/evaluator-algorithm.md` | Step-by-step evaluation algorithm |
| `references/porting-checklist.md` | Cross-language parity checklist |
| `references/regression-workflow.md` | Recommended regression CI flow |
| `references/actual-output-format.md` | Required regression output shapes |
| `references/endpoint-contract.md` | Canonical API request/response |
| `references/platform-recipes.md` | Per-stack integration notes |
| `references/security-observability.md` | Production API guardrails |
| `references/interpretation-rules.md` | Risk band mapping and narrative hints |
| `references/report-structure.md` | Canonical report fields |

## Scripts

| Script | Description |
|---|---|
| `scripts/run_module.py` | Single-entry dispatcher for all operations |
| `scripts/nhri_risk_eval.py` | Reference evaluator (Python) |
| `scripts/validate_input.py` | Input validation CLI |
| `scripts/get_population_avg.py` | Population average lookup |
| `scripts/generate_vectors.py` | Regression vector generator |
| `scripts/compare_outputs.py` | Regression output comparator |
| `scripts/scaffold_adapter.py` | API adapter scaffold generator |
| `scripts/render_report.py` | Report renderer |

## Assets

| File | Description |
|---|---|
| `assets/golden-vectors.sample.json` | Sample regression vectors |
| `assets/express_app.js.tpl` | Express adapter template |
| `assets/fastapi_app.py.tpl` | FastAPI adapter template |
| `assets/spring_risk_controller.java.tpl` | Spring adapter template |
| `assets/report-template.md` | Markdown report layout template |
| `assets/sample-evaluator-output.json` | Sample evaluator output for testing |
| `assets/sample-report.md` | Sample rendered report |
