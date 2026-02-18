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
| Visualization | `references/visualization-guide.md` | `run_module.py --module report --format html` |

## Model Rules (V4)

- Models: `chd`, `stroke`, `hypertension`, `diabetes`, `mace`
- Gender routing: `gender == 1` → male branch; else → female branch
- Rounding: Java-style `round(value * 10000) / 100` for risk percentages
- Age range for population averages: 35-70 (index = `age - 35`); outside range → 0
- Risk type thresholds:
  - CHD/Stroke/Diabetes/MACE: `risk >= 20` → type 2, `risk >= 10` → type 1
  - Hypertension: `multipleDiff > 1.25` → type 2, `multipleDiff >= 0.75` → type 1

## Additional Platform Support

Beyond FastAPI, Express, and Spring, the scaffold generator also supports Go, Rust, and .NET platforms.

### Go (Gin)

Template: `assets/gin_risk_handler.go.tpl`

```bash
python scripts/run_module.py --module api-scaffold -- --platform gin --output adapters/gin
```

### Rust (Axum)

Template: `assets/axum_risk_handler.rs.tpl`

```bash
python scripts/run_module.py --module api-scaffold -- --platform axum --output adapters/axum
```

### .NET Minimal API

```bash
python scripts/run_module.py --module api-scaffold -- --platform dotnet --output adapters/dotnet
```

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
| `references/visualization-guide.md` | Risk visualization charts, color standards, embedding |

## Scripts

| Script | Description |
|---|---|
| `scripts/run_module.py` | Single-entry dispatcher for all operations |
| `scripts/nhri_risk_eval.py` | Reference evaluator (Python) |
| `scripts/validate_input.py` | Input validation CLI |
| `scripts/get_population_avg.py` | Population average lookup |
| `scripts/generate_vectors.py` | Regression vector generator |
| `scripts/compare_outputs.py` | Regression output comparator |
| `scripts/scaffold_adapter.py` | API adapter scaffold generator (supports fastapi, express, spring, gin, axum, dotnet) |
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
| `assets/gin_risk_handler.go.tpl` | Go Gin adapter template |
| `assets/axum_risk_handler.rs.tpl` | Rust Axum adapter template |

---

## CI/CD Pipeline（GitHub Actions）

### 基本 Workflow

```yaml
name: NHRI Risk CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt

      # 輸入驗證測試
      - name: Run validation tests
        run: python scripts/run_module.py --module validate -- --test-suite all

      # 回歸測試
      - name: Generate regression vectors
        run: python scripts/run_module.py --module regress-generate -- --per-group 5 --output /tmp/vectors.json

      - name: Run regression comparison
        run: python scripts/run_module.py --module regress-compare -- --expected assets/golden-vectors.sample.json --actual /tmp/vectors.json

      # 所有模型全量評估
      - name: Evaluate all models (smoke test)
        run: |
          python scripts/run_module.py --module evaluate -- \
            --json '{"gender":1,"age":50,"sbp":130,"dbp":85,"tc":200,"hdl":50,"ldl":130,"tg":150,"bmi":25,"smoke":0,"dm":0,"hpt_med":0,"waist":85,"fpg":100}' \
            --pretty

  scaffold:
    runs-on: ubuntu-latest
    needs: validate
    strategy:
      matrix:
        platform: [fastapi, express, spring, gin, axum, dotnet]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - name: Scaffold ${{ matrix.platform }} adapter
        run: python scripts/run_module.py --module api-scaffold -- --platform ${{ matrix.platform }} --output /tmp/${{ matrix.platform }}
      - name: Verify scaffold output exists
        run: ls -la /tmp/${{ matrix.platform }}/
```

### 建議的 CI 觸發條件

| 事件 | 執行內容 |
|------|---------|
| push to main | 全量回歸測試 + scaffold 驗證 |
| pull request | 驗證測試 + 回歸比對 |
| release tag | 全量測試 + 產生所有平台 adapter |
| schedule (weekly) | 完整回歸套件 + 效能基準 |

---

## Web UI Scaffolding

### 目錄結構

```
nhri-risk-web/
├── src/
│   ├── components/
│   │   ├── RiskForm.tsx          # 輸入表單
│   │   ├── RiskResult.tsx        # 結果顯示
│   │   ├── RiskChart.tsx         # 風險視覺化圖表
│   │   └── ModelSelector.tsx     # 模型選擇器
│   ├── hooks/
│   │   └── useRiskEvaluation.ts  # API 呼叫 hook
│   ├── utils/
│   │   ├── validation.ts         # 前端輸入驗證
│   │   └── formatters.ts         # 結果格式化
│   ├── types/
│   │   └── risk.ts               # TypeScript 型別定義
│   └── App.tsx
├── public/
├── package.json
└── tsconfig.json
```

### 前端輸入驗證（與後端一致）

| 欄位 | 範圍 | 型別 |
|------|------|------|
| age | 35-70 | integer |
| gender | 1 (男) / 2 (女) | integer |
| sbp | 80-250 | number |
| dbp | 40-150 | number |
| tc | 100-400 | number |
| hdl | 20-120 | number |
| bmi | 15-50 | number |
| waist | 50-150 | number |
| fpg | 50-300 | number |
| smoke | 0 / 1 | boolean → integer |
| dm | 0 / 1 | boolean → integer |
| hpt_med | 0 / 1 | boolean → integer |

---

## 模型版本管理

### 版本命名規則

```
NHRI-V{major}.{minor}.{patch}
例：NHRI-V4.1.0
```

| 欄位 | 變更時機 |
|------|---------|
| major | 模型架構改變（如 V3 → V4） |
| minor | 係數更新、新增模型 |
| patch | Bug 修復、文件更新 |

### Golden Vector 管理

每次模型更新時：
1. 使用舊版本和新版本分別生成 golden vectors
2. 比較差異，確認變更僅在預期範圍內
3. 更新 `assets/golden-vectors.sample.json`
4. 在 commit message 中註明係數變更細節
5. 為舊版本建立 git tag 以便回溯

### 多版本並存

```
references/
├── formulas.md              # 目前版本（V4）
├── formulas-v3.md           # 歷史版本（V3，供回溯）
└── migration-v3-to-v4.md    # 版本遷移指南
```
