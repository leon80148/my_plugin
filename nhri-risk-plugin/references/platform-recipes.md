# Platform Recipes

## FastAPI (Python)
- Reuse `nhri_risk_eval.py` directly in-process.
- Validate body with Pydantic models.
- Return evaluator output as JSON without renaming fields.

## Express (Node.js)
- Keep adapter thin and call your evaluator module/service.
- Validate `model` and `input` existence before evaluation.
- Return stable JSON shape for all models.

## Spring Boot (Java)
- Keep controller layer minimal.
- Put model dispatch in a service bean.
- Use DTOs mirroring the canonical contract.

## Cross-Platform Rules
- Keep `model` names lowercase: `chd`, `stroke`, `hypertension`, `diabetes`, `mace`.
- Keep output keys unchanged.
- Preserve numeric precision and thresholds from the evaluator skill.
