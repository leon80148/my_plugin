# Routing Table

Choose one row and load only that reference first.

## Spec and Coefficients
- Intent: formula audit, coefficient checks, age baseline values, risk type rules
- Open: `references/formulas.md`
- Script: `python scripts/run_module.py --module spec-popavg -- --model chd --gender male --age 52`

## Input Validation
- Intent: request pre-checks, required fields by branch, form/API validation
- Open: `references/validation-matrix.md`
- Script: `python scripts/run_module.py --module validate -- --model chd --json "{...}" --pretty`

## Evaluation
- Intent: compute risk for one model or all models
- Open: `references/evaluator-algorithm.md`
- Script: `python scripts/run_module.py --module evaluate -- --json "{...}" --pretty`

## Regression
- Intent: generate golden vectors or compare cross-language outputs
- Open: `references/regression-workflow.md`
- Script generate: `python scripts/run_module.py --module regress-generate -- --per-group 10 --output <vectors.json>`
- Script compare: `python scripts/run_module.py --module regress-compare -- --expected <vectors.json> --actual <actual.json>`

## API Adapter
- Intent: scaffold FastAPI/Express/Spring wrappers
- Open: `references/endpoint-contract.md`
- Script: `python scripts/run_module.py --module api-scaffold -- --platform fastapi --output adapters/fastapi`

## Report Rendering
- Intent: convert scoring outputs to markdown/text/json summary
- Open: `references/report-structure.md`
- Script: `python scripts/run_module.py --module report -- --input <result.json> --format markdown`
