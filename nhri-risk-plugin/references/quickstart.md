# Quick Start

## Evaluate all models
python scripts/run_module.py --module evaluate -- --json "{\"gender\":0,\"age\":58,\"sbp\":132,\"tg\":145,\"chol\":210,\"hdlc\":52,\"glu\":101,\"waist\":82,\"ldlc\":129,\"height\":160,\"weight\":63,\"smoke\":0,\"hbp\":1,\"diabetes\":0}" --pretty

## Validate one model
python scripts/run_module.py --module validate -- --model chd --json "{\"gender\":1,\"age\":52,\"hbp\":1,\"waist\":88,\"hdlc\":45}" --pretty

## Generate regression vectors
python scripts/run_module.py --module regress-generate -- --per-group 3 --output assets/golden-vectors.sample.json

## Scaffold FastAPI adapter
python scripts/run_module.py --module api-scaffold -- --platform fastapi --output adapters/fastapi --service-name nhri-risk-api

## Render markdown report
python scripts/run_module.py --module report -- --input assets/sample-evaluator-output.json --format markdown
